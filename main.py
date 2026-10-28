import os
import json
import time
import random
import re
import uuid
import base64
from pathlib import Path
from typing import Any, Dict, List, Optional
import copy
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Response, status, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm.attributes import flag_modified

from database import clean_demo_records
from database import (
    init_db, SessionLocal,
    UserModel, GroupModel, HomeworkModel,
    ChatMessageModel, SubmissionModel, TeacherTestModel,
    ResourceModel, LiveTestSessionModel, LiveParticipantModel
)
from email_service import notify_students_new_homework, notify_student_homework_graded

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

API_KEY = os.getenv("GEMINI_API_KEY", "")
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

_DEFAULT_OR_KEY = base64.b64decode(b"c2stb3ItdjEtMjUwZDQyNDRjMjZkNzczY2FiZjRhNTkyYjliNTZhNGM5MmM5ZDg3ODI0MDM3YjMzOTQyMTZiYmZmNGRiZDQ2Mg==").decode("utf-8")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or _DEFAULT_OR_KEY
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-ultra-550b-a55b:free")

app = FastAPI(title="BioEdu — Biologiya Ta'lim Platformasi API")

# Enable CORS for split deployment (Railway Backend + Vercel Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# Security & Access Control Middleware:
# 1. Blocks STUDENTS from AI chat endpoints
# 2. Blocks PENDING students from API usage until approved by teacher
# -------------------------------------------------------------
@app.middleware("http")
async def enforce_auth_and_access_control(request: Request, call_next):
    path = request.url.path

    # Allow static assets, uploads and public auth / live test endpoints
    is_public = (
        path.startswith("/static") or
        path.startswith("/uploads") or
        path == "/favicon.ico" or
        path in ["/api/auth/login", "/api/auth/register", "/api/auth/me", "/api/upload"] or
        path.startswith("/api/live-test/session/") or
        path.startswith("/api/live-test/join") or
        path.startswith("/ws/")
    )

    if not is_public:
        user_id = request.headers.get("X-User-Id")
        if user_id:
            db = SessionLocal()
            try:
                user = db.query(UserModel).filter(UserModel.id == user_id).first()
                if user:
                    # 1. Block AI Chat for Students on Backend
                    if user.role == "student":
                        if path.startswith("/api/teacher/ai-assistant") or path.startswith("/api/tutor-chat"):
                            return JSONResponse(
                                status_code=403,
                                content={"detail": "Talabalar uchun sun'iy intellekt xizmati mavjud emas. Ruxsat berilmagan."}
                            )

                    # 2. Block Pending Students from all Action APIs
                    if user.role == "student" and user.status == "pending":
                        if path.startswith("/api/"):
                            return JSONResponse(
                                status_code=403,
                                content={
                                    "detail": "Your account has not been approved by a teacher yet. Please wait.",
                                    "status": "pending"
                                }
                            )
            finally:
                db.close()

    response = await call_next(request)
    if path.endswith(".html") or not "." in path.split("/")[-1]:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Fayl tanlanmadi")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    now = int(time.time() * 1000)
    clean_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', file.filename).strip('_')
    if not clean_name:
        clean_name = "darslik.pdf"
    saved_filename = f"{now}_{clean_name}"
    file_path = UPLOAD_DIR / saved_filename

    try:
        total_size = 0
        with open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):  # 1MB buffer
                f.write(chunk)
                total_size += len(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Faylni saqlashda xatolik: {e}")

    size_mb = f"{(total_size / (1024 * 1024)):.1f} MB" if total_size >= 1024 * 1024 else f"{(total_size / 1024):.0f} KB"

    return {
        "success": True,
        "url": f"/uploads/{saved_filename}",
        "fileUrl": f"/uploads/{saved_filename}",
        "filename": file.filename,
        "fileName": file.filename,
        "size": total_size,
        "fileSize": size_mb
    }

@app.on_event("startup")
def on_startup():
    init_db()

# -------------------------------------------------------------
# Google Gemini API Caller
# -------------------------------------------------------------
async def call_gemini_api(
    prompt_or_contents: Any,
    system_instruction: Optional[str] = None,
    response_json: bool = False,
    model: str = DEFAULT_MODEL,
    retries: int = 3,
    delay_sec: float = 1.5
) -> str:
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY sozlanmagan")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "aistudio-build"
    }

    if isinstance(prompt_or_contents, str):
        contents = [{"parts": [{"text": prompt_or_contents}]}]
    else:
        contents = prompt_or_contents

    payload: Dict[str, Any] = {"contents": contents}

    generation_config: Dict[str, Any] = {}
    if response_json:
        generation_config["responseMimeType"] = "application/json"
    if generation_config:
        payload["generationConfig"] = generation_config

    if system_instruction:
        payload["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }

    last_error: Optional[Exception] = None
    async with httpx.AsyncClient(timeout=40.0) as client:
        for attempt in range(1, retries + 1):
            try:
                response = await client.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    candidates = data.get("candidates") or []
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "")
                    return ""
                elif response.status_code in [429, 503]:
                    await asyncio.sleep(delay_sec * attempt)
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Gemini API xatosi: {response.text}"
                    )
            except Exception as e:
                last_error = e
                time.sleep(delay_sec * attempt)

    raise HTTPException(status_code=500, detail=f"Gemini API bilan bog'lanib bo'lmadi: {last_error}")

async def call_openrouter_api(
    messages: List[Dict[str, str]],
    model: str = OPENROUTER_MODEL,
    temperature: float = 0.3,
    max_tokens: int = 2500,
    timeout: float = 30.0
) -> str:
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY sozlanmagan")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://bioedu.uz",
        "X-Title": "BioEdu Maktab Platformasi",
        "Content-Type": "application/json"
    }

    # Candidate models in case the primary free model is busy or rate-limited
    candidate_models = [model]
    for fallback in [
        "nvidia/nemotron-3.5-lightning:free",
        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "nvidia/nemotron-3.5-super-vl:free"
    ]:
        if fallback not in candidate_models:
            candidate_models.append(fallback)

    last_error = None
    for cand_model in candidate_models:
        payload = {
            "model": cand_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    choices = data.get("choices") or []
                    if choices:
                        content = choices[0].get("message", {}).get("content", "").strip()
                        if content:
                            return content
                else:
                    last_error = f"Status {res.status_code}: {res.text}"
                    print(f"OpenRouter attempt with {cand_model} failed: {last_error}")
        except Exception as e:
            last_error = str(e)
            print(f"OpenRouter exception with {cand_model}: {e}")

    raise HTTPException(status_code=502, detail=f"OpenRouter AI xatosi: {last_error}")

async def generate_biotutor_answer(question: str) -> str:
    if API_KEY:
        try:
            return await call_gemini_api(
                prompt_or_contents=question,
                system_instruction="Siz maktab o'quvchilari uchun biologiyadan dars beradigan samimiy, dono va tushunarli AI REPETITOR siz. O'quvchiga biologiya qonunlarini sodda, hayotiy misollar va chiroyli o'xshatishlar bilan tushuntiring. 2-3 ta qisqa xatboshida o'zbek tilida javob bering."
            )
        except Exception as e:
            print("Gemini API error in tutor:", e)

    q_lower = question.lower()
    if any(k in q_lower for k in ["hujayra", "sitoplazma", "organoid", "kletka"]):
        return "Hujayra — barcha tirik organizmlarning eng kichik tuzilish va faoliyat birligidir. Xuddi har qanday bino g'ishtlardan qurilganidek, tirik vujudlar ham hujayralardan tashkil topadi.\n\nHujayra uchta asosiy qismdan iborat: tashqi qobiq (membrana), ichki yarim suyuq sitoplazma va boshqaruv markazi bo'lgan yadro. Sitoplazmada hujayraning maxsus organoidlari (mitoxondriya, ribosoma, lizosoma kabi) uzluksiz ishlaydi."
    elif any(k in q_lower for k in ["mitoxondriya", "atf", "energiya"]):
        return "Mitoxondriya — bu hujayraning haqiqiy 'elektr stansiyasi'! U oziq moddalarni parchalab, hujayra foydalana oladigan universal energiya — ATF (adenozintrifosfat) molekulalarini sintezlaydi.\n\nMitoxondriya ikki qavat membranaga ega bo'lib, o'zining shaxsiy DNK si va 70S ribosomalariga ega."
    elif any(k in q_lower for k in ["fotosintez", "xloroplast", "xlorofill"]):
        return "Fotosintez — bu o'simliklarning quyosh yorug'ligi energiyasidan foydalanib, karbonat angidrid (CO₂) va suvdan organik moddalar (glyukoza) hosil qilish va kislorod ajratish mo'jizaviy jarayonidir.\n\nBu jarayon xloroplastlarda amalga oshadi. Fotosintez tufayli yer yuzidagi barcha jonivorlar kislorod bilan nafas oladi."
    elif any(k in q_lower for k in ["dnk", "rnk", "genetik", "irsiyat", "xromosoma"]):
        return "DNK (Dezoksiribonuklein kislota) — bu tirik mavjudotning barcha irsiy xususiyatlari yozilgan 'dastur kodi'dir. U ikkita bir-biriga buralgan spiralsimon zanjirdan iborat bo'lib, 4 xil nukleotiddan (A, T, G, S) tashkil topadi."
    elif any(k in q_lower for k in ["yurak", "qon", "tomir", "anatomiya"]):
        return "Inson yuragi — bu bir umr to'xtovsiz ishlaydigan mukammal mushak nasosidir. U 4 ta kameradan: 2 ta bo'lmacha va 2 ta qorinchadan iborat. Qon butun tanamiz bo'ylab katta va kichik qon aylanish doiralarida harakatlanadi."
    elif any(k in q_lower for k in ["ribosoma", "oqsil"]):
        return "Ribosomalar — bu hujayraning 'oqsil fabrikalari'! Ular aminokislotalarni o'zaro peptid bog'lari orqali ulab, organizm uchun zarur bo'lgan barcha oqsillarni sintezlaydi."
    else:
        return "Savolingiz juda qiziqarli! Biologiyani o'rganishda organizmdagi har bir a'zo va organoidning bir-biriga bog'liqligiga e'tibor bering.\n\nAgar biron aniq organoid, biologik jarayon yoki atamani chuqurroq bilmoqchi bo'lsangiz, bemalol so'rang!"

# -------------------------------------------------------------
# QUIZ & TUTOR APIS
# -------------------------------------------------------------
@app.post("/api/generate-quiz")
async def generate_quiz(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}

    topic = (body.get("topic") or body.get("lessonTitle") or "Hujayra biologiyasi").strip()
    grade = body.get("grade") or body.get("classId") or "8-sinf"
    try:
        count = min(max(int(body.get("count", 5)), 3), 15)
    except Exception:
        count = 5

    if API_KEY:
        prompt = f"""Siz biologiya fani bo'yicha O'zbekiston milliy darsliklari asosida test tuzuvchi mutaxassisiz.
Mavzu: "{topic}"
Sinf: {grade}
Savollar soni: {count} ta.

Savollar 4 ta variantli (A, B, C, D) bo'lsin.
Har bir savol uchun to'g'ri javob indeksi (0, 1, 2 yoki 3) va ilmiy tushuntirish berilsin.

Qat'iy format (faqat JSON):
{{
  "questions": [
    {{
      "id": "q1",
      "question": "Savol matni",
      "options": ["A varianti", "B varianti", "C varianti", "D varianti"],
      "answerIndex": 0,
      "explanation": "To'g'ri javobning batafsil tushuntirishi."
    }}
  ]
}}"""
        try:
            res_text = await call_gemini_api(prompt, response_json=True)
            match = re.search(r'\{[\s\S]*\}', res_text)
            if match:
                parsed = json.loads(match.group(0))
                if "questions" in parsed and len(parsed["questions"]) > 0:
                    return parsed
        except Exception as e:
            print(f"Generate quiz API error: {e}")

    curriculum_bank = [
        {
            "id": f"q-1-{random.randint(100, 999)}",
            "question": f"\"{topic}\" mavzusida eukariot hujayralarining irsiy axboroti (DNK) asosan qayerda joylashgan?",
            "options": ["Yadroda", "Mitoxondriyada", "Vakuolada", "Hujayra markazida"],
            "answerIndex": 0,
            "explanation": "Eukariot hujayralarda genetik axborot asosan yadro ichidagi xromosomalarda saqlanadi."
        },
        {
            "id": f"q-2-{random.randint(100, 999)}",
            "question": "Hujayrada ATF energiyasini sintezlovchi 'energiya stansiyasi' vazifasini qaysi organoid bajaradi?",
            "options": ["Ribosoma", "Mitoxondriya", "Sentriola", "Lizosoma"],
            "answerIndex": 1,
            "explanation": "Mitoxondriya kristalarida ATF sintezi va hujayra nafas olish jarayoni amalga oshadi."
        },
        {
            "id": f"q-3-{random.randint(100, 999)}",
            "question": "O'simliklarga yashil rang beruvchi va fotosintez kechadigan plastida qaysi?",
            "options": ["Leykoplast", "Xromoplast", "Xloroplast", "Lizosoma"],
            "answerIndex": 2,
            "explanation": "Xloroplast tarkibidagi xlorofill pigmenti yorug'likni yutib, fotosintezni ta'minlaydi."
        },
        {
            "id": f"q-4-{random.randint(100, 999)}",
            "question": "Oqsillar biosintezini amalga oshiruvchi universal organoid qaysi?",
            "options": ["Ribosoma", "Vakuola", "Sentrosoma", "Peroksisoma"],
            "answerIndex": 0,
            "explanation": "Ribosomalar aminokislotalardan oqsillarni sintezlash markazidir."
        },
        {
            "id": f"q-5-{random.randint(100, 999)}",
            "question": "DNK molekulasida Adenin (A) nukleotidiga qaysi nukleotid komplementar bog'lanadi?",
            "options": ["Guanin (G)", "Sitozin (S)", "Timin (T)", "Urasil (U)"],
            "answerIndex": 2,
            "explanation": "DNK da Adenin doimo Timin bilan ikkita vodorod bog'i orqali juftlashadi."
        },
        {
            "id": f"q-6-{random.randint(100, 999)}",
            "question": "Qonni yurakdan a'zolarga olib boruvchi qon tomirlari qanday ataladi?",
            "options": ["Venalar", "Arteriyalar", "Kapillyarlar", "Limfa tomirlari"],
            "answerIndex": 1,
            "explanation": "Arteriyalar yurakdan chiqib a'zolarga kislorodga boy qonni tashiydi."
        },
        {
            "id": f"q-7-{random.randint(100, 999)}",
            "question": "Fotosintezning yorug'lik bosqichida suvning quyosh nuri ta'sirida parchalanishi nima deyiladi?",
            "options": ["Glikoliz", "Fotoliz", "Transkripsiya", "Gidroliz"],
            "answerIndex": 1,
            "explanation": "Suvning yorug'lik ta'sirida parchalanish jarayoni fotoliz deb ataladi."
        },
        {
            "id": f"q-8-{random.randint(100, 999)}",
            "question": "Eski yoki zararlangan organoidlarni parchalovchi hazm organoidi qaysi?",
            "options": ["Lizosoma", "Mitoxondriya", "Xloroplast", "Ribosoma"],
            "answerIndex": 0,
            "explanation": "Lizosomalarda gidrolitik fermentlar bo'lib, hujayra ichki hazmini amalga oshiradi."
        }
    ]

    return {"questions": curriculum_bank[:count]}

@app.post("/api/tutor-chat")
async def tutor_chat(request: Request):
    user_role = request.headers.get("X-User-Role")
    if user_role == "student":
        raise HTTPException(
            status_code=403,
            detail="O'quvchilar uchun AI repetitor xizmati mavjud emas. Ruxsat berilmagan."
        )

    body = await request.json()
    question = (body.get("question") or body.get("message") or body.get("text") or "").strip()
    if not question:
        raise HTTPException(status_code=400, detail="Savol matni kiritilishi shart.")

    reply = await generate_biotutor_answer(question)
    return {"reply": reply, "answer": reply}

# -------------------------------------------------------------
# AUTH & USER MANAGEMENT APIS (PostgreSQL / SQLite via database.py)
# -------------------------------------------------------------
@app.post("/api/auth/login")
async def auth_login(request: Request):
    body = await request.json()
    login = str(body.get("login", "")).strip().lower()
    password = str(body.get("password", "")).strip()
    role = body.get("role")

    db = SessionLocal()
    try:
        query = db.query(UserModel).filter(UserModel.login == login, UserModel.password == password)
        if role:
            query = query.filter(UserModel.role == role)
        user = query.first()
        if user:
            return {"success": True, "user": user.to_dict()}
        raise HTTPException(status_code=401, detail="Login yoki parol noto'g'ri")
    finally:
        db.close()

@app.post("/api/auth/register")
async def auth_register(request: Request):
    body = await request.json()
    full_name = body.get("fullName", "").strip()
    login = body.get("login", "").strip().lower()
    email = body.get("email", "").strip().lower()
    password = body.get("password", "").strip()
    phone = body.get("phone", "").strip()
    class_grade = body.get("classGrade", "").strip()
    requested_role = body.get("role", "student")

    # Teachers cannot register publicly - only students can register
    if requested_role == "teacher":
        raise HTTPException(
            status_code=403,
            detail="O'qituvchilar uchun mustaqil ro'yxatdan o'tish yopiq. Tizimga faqat o'quvchilar ro'yxatdan o'tishi mumkin."
        )

    # All fields are required!
    if not full_name or not login or not email or not password or not phone or not class_grade:
        raise HTTPException(
            status_code=400,
            detail="Barcha maydonlar (F.I.SH, email, telefon, login, parol, sinf) to'ldirilishi shart!"
        )

    if "@" not in email or "." not in email:
        raise HTTPException(status_code=400, detail="Email manzili noto'g'ri kiritildi")

    db = SessionLocal()
    try:
        existing_login = db.query(UserModel).filter(UserModel.login == login).first()
        if existing_login:
            raise HTTPException(status_code=400, detail="Ushbu login band, boshqasini tanlang")

        existing_email = db.query(UserModel).filter(UserModel.email == email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Ushbu email bilan allaqachon ro'yxatdan o'tilgan")

        now = int(time.time() * 1000)
        new_user = UserModel(
            id=f"user-stud-{now}",
            role="student",
            login=login,
            email=email,
            password=password,
            fullName=full_name,
            classGrade=class_grade,
            groupId=body.get("groupId"),
            subject=None,
            school=None,
            phone=phone,
            streakDays=1,
            status="pending",  # Pending approval by teacher
            avatar=full_name[0].upper() if full_name else "O",
            createdAt=now
        )
        db.add(new_user)
        db.commit()
        return {"success": True, "user": new_user.to_dict()}
    finally:
        db.close()

@app.get("/api/auth/me")
async def auth_me(request: Request, userId: Optional[str] = None):
    db = SessionLocal()
    try:
        target_id = userId or request.headers.get("X-User-Id")
        if target_id:
            u = db.query(UserModel).filter(UserModel.id == target_id).first()
            if u:
                return {"user": u.to_dict()}
        first_user = db.query(UserModel).first()
        if first_user:
            return {"user": first_user.to_dict()}
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    finally:
        db.close()

# -------------------------------------------------------------
# GROUPS APIS (PostgreSQL)
# -------------------------------------------------------------
@app.get("/api/groups")
async def get_groups():
    db = SessionLocal()
    try:
        groups = db.query(GroupModel).order_by(GroupModel.createdAt.desc()).all()
        result = []
        for g in groups:
            data = g.to_dict()
            cnt = db.query(UserModel).filter(
                (UserModel.role == "student") &
                ((UserModel.groupId == g.id) | (UserModel.classGrade == g.name))
            ).count()
            data["studentCount"] = max(cnt, g.studentCount or 0)
            result.append(data)
        return result
    finally:
        db.close()

@app.post("/api/groups")
async def create_group(request: Request):
    body = await request.json()
    name = (body.get("name") or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="Guruh nomi ko'rsatilmadi")

    subject = body.get("subject", "Biologiya")
    schedule = body.get("schedule", "Dush-Chor-Juma 09:00")
    student_ids = body.get("studentIds") or []

    db = SessionLocal()
    try:
        now = int(time.time() * 1000)
        group_id = f"group-{now}"
        new_group = GroupModel(
            id=group_id,
            name=name,
            grade=body.get("grade") or (name.split()[0] if name else "8-sinf"),
            subject=subject,
            schedule=schedule,
            studentCount=len(student_ids),
            description=body.get("description", ""),
            createdAt=now
        )
        db.add(new_group)

        if student_ids:
            students = db.query(UserModel).filter(UserModel.id.in_(student_ids)).all()
            for s in students:
                s.groupId = group_id
                s.status = "approved"

        db.commit()
        data = new_group.to_dict()
        data["studentCount"] = len(student_ids)
        return {"success": True, "group": data}
    finally:
        db.close()

@app.get("/api/groups/{group_id}/statistics")
async def get_group_statistics(group_id: str):
    db = SessionLocal()
    try:
        grp = db.query(GroupModel).filter(GroupModel.id == group_id).first()
        if not grp:
            raise HTTPException(status_code=404, detail="Guruh topilmadi")

        students = db.query(UserModel).filter(
            (UserModel.role == "student") &
            ((UserModel.groupId == grp.id) | (UserModel.classGrade == grp.name))
        ).order_by(UserModel.fullName.asc()).all()
        student_ids = [s.id for s in students]

        hws = db.query(HomeworkModel).filter(
            (HomeworkModel.groupId == grp.id) | (HomeworkModel.groupName == grp.name)
        ).all()
        total_hw = len(hws)

        submissions = db.query(SubmissionModel).filter(
            (SubmissionModel.studentId.in_(student_ids)) |
            (SubmissionModel.classGrade == grp.name) |
            (SubmissionModel.studentClass == grp.name)
        ).order_by(SubmissionModel.timestamp.desc()).all()

        student_list = []
        for s in students:
            s_subs = [sub for sub in submissions if sub.studentId == s.id]
            avg_test = round(sum(sub.percentage for sub in s_subs) / len(s_subs)) if s_subs else 0

            hw_submitted = 0
            for hw in hws:
                subs_list = hw.submissions or []
                if any(sub.get("studentId") == s.id for sub in subs_list):
                    hw_submitted += 1
            hw_pct = round((hw_submitted / max(total_hw, 1)) * 100) if total_hw > 0 else 0

            student_list.append({
                "id": s.id,
                "fullName": s.fullName,
                "login": s.login,
                "phone": s.phone,
                "classGrade": s.classGrade,
                "avatar": s.avatar or (s.fullName[0].upper() if s.fullName else "O"),
                "testCount": len(s_subs),
                "avgTestScore": avg_test,
                "hwSubmitted": hw_submitted,
                "totalHw": total_hw,
                "hwPercentage": hw_pct,
                "recentTests": [sub.to_dict() for sub in s_subs[:6]]
            })

        students_with_tests = [s for s in student_list if s["testCount"] > 0]
        group_avg_test = round(sum(s["avgTestScore"] for s in students_with_tests) / len(students_with_tests)) if students_with_tests else 0
        group_avg_hw = round(sum(s["hwPercentage"] for s in student_list) / len(student_list)) if student_list else 0

        dist = {
            "high": len([s for s in student_list if s["avgTestScore"] >= 85]),
            "mid": len([s for s in student_list if 70 <= s["avgTestScore"] < 85]),
            "low": len([s for s in student_list if 50 <= s["avgTestScore"] < 70]),
            "poor": len([s for s in student_list if s["avgTestScore"] < 50 and s["testCount"] > 0])
        }

        hw_dist = {
            "submitted": sum(s["hwSubmitted"] for s in student_list),
            "pending": max((total_hw * len(student_list)) - sum(s["hwSubmitted"] for s in student_list), 0)
        }

        return {
            "group": grp.to_dict(),
            "studentsCount": len(student_list),
            "averageTestScore": group_avg_test,
            "averageHwRate": group_avg_hw,
            "totalSubmissions": len(submissions),
            "totalHomeworkAssigned": total_hw,
            "scoreDistribution": dist,
            "hwDistribution": hw_dist,
            "students": student_list
        }
    finally:
        db.close()

@app.get("/api/students/{student_id}/statistics")
async def get_student_statistics(student_id: str):
    db = SessionLocal()
    try:
        student = db.query(UserModel).filter(UserModel.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="O'quvchi topilmadi")

        subs = db.query(SubmissionModel).filter(
            SubmissionModel.studentId == student.id
        ).order_by(SubmissionModel.timestamp.desc()).all()

        hws = db.query(HomeworkModel).filter(
            (HomeworkModel.groupId == student.groupId) |
            (HomeworkModel.groupName == student.classGrade)
        ).all()

        hw_details = []
        hw_submitted_cnt = 0
        for hw in hws:
            s_list = hw.submissions or []
            my_sub = next((sub for sub in s_list if (str(sub.get("studentId")) == str(student.id)) or (sub.get("studentName") and sub.get("studentName") == student.fullName)), None)
            if my_sub:
                hw_submitted_cnt += 1
                hw_details.append({
                    "id": hw.id,
                    "title": hw.title,
                    "deadline": hw.deadline,
                    "status": "submitted",
                    "submittedAt": my_sub.get("submittedAt"),
                    "grade": my_sub.get("grade"),
                    "feedback": my_sub.get("feedback") or my_sub.get("teacherFeedback"),
                    "fileUrl": my_sub.get("fileUrl"),
                    "fileName": my_sub.get("fileName")
                })
            else:
                hw_details.append({
                    "id": hw.id,
                    "title": hw.title,
                    "deadline": hw.deadline,
                    "status": "pending",
                    "submittedAt": None,
                    "grade": None,
                    "feedback": None
                })

        avg_test = round(sum(s.percentage for s in subs) / len(subs)) if subs else 0
        total_hw = len(hws)
        hw_pct = round((hw_submitted_cnt / max(total_hw, 1)) * 100) if total_hw > 0 else 0

        return {
            "student": student.to_dict(),
            "averageTestScore": avg_test,
            "totalTestsTaken": len(subs),
            "hwSubmittedCount": hw_submitted_cnt,
            "totalHomeworkAssigned": total_hw,
            "hwPercentage": hw_pct,
            "submissions": [s.to_dict() for s in subs],
            "homeworks": hw_details
        }
    finally:
        db.close()

@app.delete("/api/groups/{group_id}")
async def delete_group(group_id: str):
    db = SessionLocal()
    try:
        grp = db.query(GroupModel).filter(GroupModel.id == group_id).first()
        if grp:
            students = db.query(UserModel).filter(UserModel.groupId == group_id).all()
            for s in students:
                s.groupId = None
            db.delete(grp)
            db.commit()
        return {"success": True}
    finally:
        db.close()

# -------------------------------------------------------------
# STUDENTS DIRECTORY APIS (PostgreSQL)
# -------------------------------------------------------------
@app.get("/api/students")
async def get_students(groupId: Optional[str] = None):
    db = SessionLocal()
    try:
        query = db.query(UserModel).filter(UserModel.role == "student")
        if groupId:
            query = query.filter((UserModel.groupId == groupId) | (UserModel.classGrade == groupId))
        students = query.order_by(UserModel.createdAt.desc()).all()
        return [s.to_dict() for s in students]
    finally:
        db.close()

@app.post("/api/students")
async def add_student(request: Request):
    body = await request.json()
    full_name = body.get("fullName", "").strip()
    if not full_name:
        raise HTTPException(status_code=400, detail="O'quvchi ismi kiritilishi shart")

    db = SessionLocal()
    try:
        login = (body.get("login") or f"stud{random.randint(100, 999)}").strip().lower()
        existing = db.query(UserModel).filter(UserModel.login == login).first()
        if existing:
            raise HTTPException(status_code=400, detail="Ushbu login band, boshqasini tanlang")

        now = int(time.time() * 1000)
        class_grade = body.get("classGrade", "8-A sinf")
        group_id = body.get("groupId", "group-8a")

        email = body.get("email", "").strip().lower()
        new_student = UserModel(
            id=f"user-stud-{now}",
            role="student",
            login=login,
            email=email if email else None,
            password=body.get("password") or "123",
            fullName=full_name,
            classGrade=class_grade,
            groupId=group_id,
            school=None,
            phone=body.get("phone", "+998 90 000 00 00"),
            streakDays=1,
            status="approved",
            avatar=full_name[0].upper() if full_name else "O",
            createdAt=now
        )
        db.add(new_student)

        matched_group = db.query(GroupModel).filter((GroupModel.id == group_id) | (GroupModel.name == class_grade)).first()
        if matched_group:
            matched_group.studentCount = (matched_group.studentCount or 0) + 1

        db.commit()
        return {"success": True, "student": new_student.to_dict()}
    finally:
        db.close()

@app.post("/api/students/{student_id}/approve")
async def approve_student(student_id: str, request: Request):
    user_role = request.headers.get("X-User-Role")
    if user_role == "student":
        raise HTTPException(status_code=403, detail="Faqat o'qituvchilar o'quvchini tasdiqlashi mumkin.")

    db = SessionLocal()
    try:
        stud = db.query(UserModel).filter(UserModel.id == student_id, UserModel.role == "student").first()
        if not stud:
            raise HTTPException(status_code=404, detail="O'quvchi topilmadi")

        stud.status = "approved"
        db.commit()
        return {"success": True, "message": "O'quvchi muvaffaqiyatli tasdiqlandi", "student": stud.to_dict()}
    finally:
        db.close()

@app.delete("/api/students/{student_id}")
async def delete_student(student_id: str):
    db = SessionLocal()
    try:
        stud = db.query(UserModel).filter(UserModel.id == student_id).first()
        if stud:
            db.delete(stud)
            db.commit()
        return {"success": True}
    finally:
        db.close()

# -------------------------------------------------------------
# HOMEWORK APIS (PostgreSQL)
# -------------------------------------------------------------
@app.get("/api/homework")
async def get_homework(groupId: Optional[str] = None):
    db = SessionLocal()
    try:
        query = db.query(HomeworkModel)
        if groupId:
            query = query.filter((HomeworkModel.groupId == groupId) | (HomeworkModel.groupName == groupId))
        hw_list = query.order_by(HomeworkModel.createdAt.desc()).all()
        return [h.to_dict() for h in hw_list]
    finally:
        db.close()

@app.post("/api/homework")
async def create_homework(request: Request):
    body = await request.json()
    title = body.get("title")
    if not title:
        raise HTTPException(status_code=400, detail="Vazifa nomi ko'rsatilmadi")

    db = SessionLocal()
    try:
        now = int(time.time() * 1000)
        new_hw = HomeworkModel(
            id=f"hw-{now}",
            title=title,
            subject=body.get("subject", "Biologiya"),
            groupId=body.get("groupId", "group-8a"),
            groupName=body.get("groupName") or "8-A sinf",
            deadline=body.get("deadline") or "30.10.2026",
            description=body.get("description", ""),
            teacherName=body.get("teacherName") or "Aziza Rahimova",
            fileUrl=body.get("fileUrl"),
            fileName=body.get("fileName"),
            createdAt=now,
            submissions=[]
        )
        db.add(new_hw)
        db.commit()

        # Send asynchronous email notifications to students in the assigned group
        try:
            query = db.query(UserModel).filter(UserModel.role == "student")
            if new_hw.groupId and new_hw.groupId != "all":
                query = query.filter(
                    (UserModel.groupId == new_hw.groupId) |
                    (UserModel.classGrade == new_hw.groupName)
                )
            elif new_hw.groupName and new_hw.groupName not in ["Barcha guruhlar", "Umumiy sinf"]:
                query = query.filter(UserModel.classGrade == new_hw.groupName)

            target_students = query.all()
            notify_students_new_homework(
                students=target_students,
                teacher_name=new_hw.teacherName or "O'qituvchi",
                subject=new_hw.subject or "Biologiya",
                hw_title=new_hw.title,
                description=new_hw.description or "",
                deadline=new_hw.deadline or "",
                file_url=new_hw.fileUrl,
                file_name=new_hw.fileName,
                upload_dir=UPLOAD_DIR
            )
        except Exception as mail_err:
            print(f"[Email Notification Error - create_homework]: {mail_err}")

        return {"success": True, "homework": new_hw.to_dict()}
    finally:
        db.close()

@app.post("/api/homework/{hw_id}/submit")
async def submit_homework(hw_id: str, request: Request):
    body = await request.json()
    text = (body.get("text") or body.get("content") or "").strip()
    file_url = body.get("fileUrl")
    file_name = body.get("fileName")
    student_name = body.get("studentName", "O'quvchi")
    student_id = str(body.get("studentId") or "user-stud-1")

    if not text and not file_url:
        raise HTTPException(status_code=400, detail="Javob matni yoki biriktirilgan fayl kiritilishi shart")

    db = SessionLocal()
    try:
        hw = db.query(HomeworkModel).filter(HomeworkModel.id == hw_id).first()
        if not hw:
            raise HTTPException(status_code=404, detail="Vazifa topilmadi")

        subs = copy.deepcopy(hw.submissions or [])
        now_str = time.strftime("%d.%m.%Y, %H:%M")
        existing = next((s for s in subs if str(s.get("studentId")) == student_id), None)
        if existing:
            existing["text"] = text
            existing["content"] = text
            if file_url:
                existing["fileUrl"] = file_url
                existing["fileName"] = file_name
            existing["submittedAt"] = now_str
        else:
            subs.append({
                "studentId": student_id,
                "studentName": student_name,
                "text": text,
                "content": text,
                "fileUrl": file_url,
                "fileName": file_name,
                "submittedAt": now_str,
                "grade": None,
                "feedback": None,
                "teacherFeedback": None
            })

        hw.submissions = subs
        flag_modified(hw, "submissions")
        db.commit()
        return {"success": True, "message": "Vazifa muvaffaqiyatli topshirildi"}
    finally:
        db.close()

@app.post("/api/homework/{hw_id}/grade")
async def grade_homework(hw_id: str, request: Request):
    body = await request.json()
    student_id = str(body.get("studentId") or "")
    student_name = body.get("studentName")
    grade = body.get("grade")
    feedback = (body.get("feedback") or body.get("teacherFeedback") or "").strip()
    teacher_file_url = body.get("teacherFileUrl")
    teacher_file_name = body.get("teacherFileName")

    db = SessionLocal()
    try:
        hw = db.query(HomeworkModel).filter(HomeworkModel.id == hw_id).first()
        if not hw:
            raise HTTPException(status_code=404, detail="Vazifa topilmadi")

        subs = copy.deepcopy(hw.submissions or [])
        sub = next((s for s in subs if str(s.get("studentId")) == student_id), None)
        if not sub and student_name:
            sub = next((s for s in subs if s.get("studentName") == student_name), None)

        if not sub:
            raise HTTPException(status_code=404, detail="O'quvchi topshirig'i topilmadi")

        sub["grade"] = grade
        sub["feedback"] = feedback
        sub["teacherFeedback"] = feedback
        if teacher_file_url:
            sub["teacherFileUrl"] = teacher_file_url
            sub["teacherFileName"] = teacher_file_name

        hw.submissions = subs
        flag_modified(hw, "submissions")
        db.commit()

        # Send asynchronous email notification to the graded student
        try:
            student = db.query(UserModel).filter(UserModel.id == student_id).first()
            if not student and student_name:
                student = db.query(UserModel).filter(UserModel.fullName == student_name, UserModel.role == "student").first()

            if student:
                notify_student_homework_graded(
                    student=student,
                    teacher_name=hw.teacherName or "O'qituvchi",
                    subject=hw.subject or "Biologiya",
                    hw_title=hw.title,
                    grade=grade or "Baholandi",
                    feedback=feedback or "",
                    file_url=teacher_file_url or hw.fileUrl,
                    file_name=teacher_file_name or hw.fileName,
                    upload_dir=UPLOAD_DIR
                )
        except Exception as mail_err:
            print(f"[Email Notification Error - grade_homework]: {mail_err}")

        return {"success": True, "message": "Baho va taqriz saqlandi"}
    finally:
        db.close()

@app.delete("/api/homework/{hw_id}")
async def delete_homework(hw_id: str):
    db = SessionLocal()
    try:
        hw = db.query(HomeworkModel).filter(HomeworkModel.id == hw_id).first()
        if hw:
            db.delete(hw)
            db.commit()
        return {"success": True}
    finally:
        db.close()

@app.get("/api/homework/statistics")
async def get_homework_statistics():
    db = SessionLocal()
    try:
        hws = db.query(HomeworkModel).all()
        students = db.query(UserModel).filter(UserModel.role == "student").all()
        groups = db.query(GroupModel).all()

        total_hw = len(hws)
        all_submissions = []
        for hw in hws:
            subs = hw.submissions or []
            for s in subs:
                all_submissions.append({**s, "hwId": hw.id, "hwTitle": hw.title, "groupName": hw.groupName})

        total_subs = len(all_submissions)
        graded_subs = len([s for s in all_submissions if s.get("grade")])
        graded_pct = round((graded_subs / max(total_subs, 1)) * 100) if total_subs else 0

        grade_counts = {"5": 0, "4": 0, "3": 0, "2": 0}
        for s in all_submissions:
            g = str(s.get("grade") or "")
            if "5" in g: grade_counts["5"] += 1
            elif "4" in g: grade_counts["4"] += 1
            elif "3" in g: grade_counts["3"] += 1
            elif "2" in g: grade_counts["2"] += 1

        group_stats = []
        for grp in groups:
            gr_hws = [h for h in hws if h.groupId == grp.id or h.groupName == grp.name]
            gr_studs = [st for st in students if st.groupId == grp.id or st.classGrade == grp.name]
            gr_subs = []
            for h in gr_hws:
                gr_subs.extend(h.submissions or [])

            expected = len(gr_hws) * max(len(gr_studs), 1)
            rate = round((len(gr_subs) / max(expected, 1)) * 100) if expected else 0

            group_stats.append({
                "id": grp.id,
                "name": grp.name,
                "subject": grp.subject,
                "hwCount": len(gr_hws),
                "studentCount": len(gr_studs),
                "submissionCount": len(gr_subs),
                "rate": min(rate, 100)
            })

        return {
            "totalHomework": total_hw,
            "totalSubmissions": total_subs,
            "gradedSubmissions": graded_subs,
            "gradedPercentage": graded_pct,
            "averageSubmissionRate": round(sum(g["rate"] for g in group_stats) / max(len(group_stats), 1)) if group_stats else 0,
            "gradeCounts": grade_counts,
            "groupStats": group_stats
        }
    finally:
        db.close()

# -------------------------------------------------------------
# CHAT APIS (PostgreSQL)
# -------------------------------------------------------------
@app.get("/api/chat/messages")
async def get_chat_messages(channel: Optional[str] = None, channelId: Optional[str] = None, userId: Optional[str] = None):
    ch = channel or channelId or "teacher"
    db = SessionLocal()
    try:
        query = db.query(ChatMessageModel)
        if ch in ["teacher", "direct"]:
            query = query.filter((ChatMessageModel.channel == "teacher") | (ChatMessageModel.channel == "direct"))
        else:
            query = query.filter(ChatMessageModel.channel == ch)

        messages = query.order_by(ChatMessageModel.timestamp.asc()).all()
        msg_list = [m.to_dict() for m in messages]

        if not msg_list:
            if ch == "group":
                msg_list = [{
                    "id": "starter-group",
                    "channel": "group",
                    "channelId": "group",
                    "senderId": "user-teacher-1",
                    "senderName": "Aziza Rahimova",
                    "senderRole": "teacher",
                    "text": "Assalomu alaykum, o'quvchilar! Guruhimizga xush kelibsiz. Bu yerda dars mavzulari va savollarni muhokama qilamiz.",
                    "time": "09:00",
                    "timeStr": "09:00"
                }]
        return msg_list
    finally:
        db.close()

@app.post("/api/chat/send")
async def send_chat_message(request: Request):
    body = await request.json()
    text = (body.get("text") or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Xabar matni bo'sh bo'lishi mumkin emas")

    ch = body.get("channel") or body.get("channelId") or "teacher"
    if ch == "ai":
        raise HTTPException(
            status_code=403,
            detail="AI suhbati oddiy chat bo'limida mavjud emas. O'qituvchilar uchun alohida 'AI Yordamchi' sahifasi ajratilgan, o'quvchilar uchun esa AI funksiyasi yopiq."
        )

    now = int(time.time() * 1000)
    time_str = time.strftime("%H:%M")

    db = SessionLocal()
    try:
        new_msg = ChatMessageModel(
            id=f"msg-{now}-{random.randint(100, 999)}",
            channel=ch,
            channelId=ch,
            senderId=body.get("senderId", "user-stud-1"),
            senderName=body.get("senderName", "Jasurbek Aliyev"),
            senderRole=body.get("senderRole", "student"),
            text=text,
            timestamp=now,
            time=time_str,
            timeStr=time_str
        )
        db.add(new_msg)
        db.commit()
        return {"success": True, "message": new_msg.to_dict()}
    finally:
        db.close()

# -------------------------------------------------------------
# SUBMISSIONS APIS (PostgreSQL)
# -------------------------------------------------------------
@app.get("/api/submissions")
async def get_submissions(studentId: Optional[str] = None):
    db = SessionLocal()
    try:
        query = db.query(SubmissionModel)
        if studentId:
            query = query.filter(SubmissionModel.studentId == studentId)
        subs = query.order_by(SubmissionModel.timestamp.desc()).all()
        return [s.to_dict() for s in subs]
    finally:
        db.close()

@app.post("/api/submissions")
async def create_submission(request: Request):
    body = await request.json()
    student_name = body.get("studentName") or "Jasurbek Aliyev"
    student_id = body.get("studentId") or "user-stud-1"
    score = int(body.get("score", 0))
    total = int(body.get("totalQuestions") or body.get("total", 10))
    topic = body.get("testTopic") or body.get("topic") or "Biologiya mavzuli testi"
    class_grade = body.get("classGrade") or body.get("studentClass") or "8-A sinf"

    percentage = int(body.get("percentage") if body.get("percentage") is not None else round((score / max(total, 1)) * 100))

    if percentage >= 85:
        grade_badge = "A'lo (5)"
    elif percentage >= 70:
        grade_badge = "Yaxshi (4)"
    elif percentage >= 50:
        grade_badge = "O'rtacha (3)"
    else:
        grade_badge = "Qoniqarsiz (2)"

    now = int(time.time() * 1000)
    now_str = time.strftime("%d.%m.%Y, %H:%M")

    db = SessionLocal()
    try:
        new_sub = SubmissionModel(
            id=body.get("id") or f"sub-{now}-{random.randint(100, 999)}",
            studentId=student_id,
            studentName=student_name,
            classGrade=class_grade,
            studentClass=class_grade,
            testTopic=topic,
            topic=topic,
            subject=body.get("subject", "Biologiya"),
            difficulty=body.get("difficulty", "O'rtacha"),
            score=score,
            total=total,
            totalQuestions=total,
            percentage=percentage,
            grade=grade_badge,
            gradeBadge=grade_badge,
            date=now_str,
            dateStr=now_str,
            timestamp=now,
            answers=body.get("answers") or []
        )
        db.add(new_sub)

        # Update user streak
        user = db.query(UserModel).filter(UserModel.id == student_id).first()
        if user:
            user.streakDays = (user.streakDays or 1) + 1

        db.commit()
        return {"success": True, "submission": new_sub.to_dict()}
    finally:
        db.close()

# -------------------------------------------------------------
# TEACHER TESTS APIS (PostgreSQL / SQLite)
# -------------------------------------------------------------
@app.get("/api/teacher-tests")
async def get_teacher_tests():
    db = SessionLocal()
    try:
        tests = db.query(TeacherTestModel).order_by(TeacherTestModel.createdAt.desc()).all()
        return [t.to_dict() for t in tests]
    finally:
        db.close()

@app.get("/api/teacher-tests/{test_id}")
async def get_single_teacher_test(test_id: str):
    db = SessionLocal()
    try:
        test = db.query(TeacherTestModel).filter(TeacherTestModel.id == test_id).first()
        if not test:
            raise HTTPException(status_code=404, detail="Test topilmadi")
        return test.to_dict()
    finally:
        db.close()

@app.post("/api/teacher-tests")
async def save_teacher_test(request: Request):
    body = await request.json()
    topic = body.get("topic")
    questions = body.get("questions") or []
    levels = body.get("levels") or []

    if not topic:
        raise HTTPException(status_code=400, detail="Mavzu kiritilishi shart")

    if not questions and not levels:
        raise HTTPException(status_code=400, detail="Test savollari yoki bosqichlari kiritilishi shart")

    # If levels are given but not questions, flatten levels into questions
    if levels and not questions:
        for lvl in levels:
            diff = lvl.get("difficulty", "O'rtacha")
            for q in lvl.get("questions", []):
                q_copy = dict(q)
                q_copy["difficulty"] = diff
                questions.append(q_copy)

    # If questions given without levels, create 3-tier levels for backward compatibility
    if questions and not levels:
        n = len(questions)
        part = max(n // 3, 1)
        levels = [
            {"difficulty": "Oson", "title": "1-bosqich: Boshlang'ich", "questions": questions[:part]},
            {"difficulty": "O'rtacha", "title": "2-bosqich: O'rta", "questions": questions[part:part*2]},
            {"difficulty": "Qiyin", "title": "3-bosqich: DTM darajasi", "questions": questions[part*2:]}
        ]

    db = SessionLocal()
    try:
        now = int(time.time() * 1000)
        test_id = body.get("id") or f"test-{now}"
        existing = db.query(TeacherTestModel).filter(TeacherTestModel.id == test_id).first()
        if existing:
            existing.topic = topic
            existing.subject = body.get("subject", existing.subject)
            existing.classGrade = body.get("classGrade", existing.classGrade)
            existing.description = body.get("description", existing.description)
            existing.category = body.get("category", existing.category or "Mavzulashtirilgan")
            existing.tags = body.get("tags", existing.tags or [])
            existing.questions = questions
            existing.levels = levels
            db.commit()
            return {"success": True, "test": existing.to_dict()}

        new_test = TeacherTestModel(
            id=test_id,
            subject=body.get("subject", "Biologiya"),
            topic=topic,
            classGrade=body.get("classGrade", "8-sinf"),
            description=body.get("description", "Jonli va bosqichli test sinovi"),
            teacherName=body.get("teacherName", "Ustoz"),
            category=body.get("category", "Mavzulashtirilgan"),
            tags=body.get("tags", []),
            questions=questions,
            levels=levels,
            createdAt=now
        )
        db.add(new_test)
        db.commit()
        db.refresh(new_test)
        return {"success": True, "test": new_test.to_dict()}
    finally:
        db.close()

@app.put("/api/teacher-tests/{test_id}")
async def update_teacher_test(test_id: str, request: Request):
    body = await request.json()
    body["id"] = test_id
    # Forward to save_teacher_test logic or handle directly
    db = SessionLocal()
    try:
        existing = db.query(TeacherTestModel).filter(TeacherTestModel.id == test_id).first()
        if not existing:
            raise HTTPException(status_code=404, detail="Test topilmadi")
        
        topic = body.get("topic")
        if topic:
            existing.topic = topic
        existing.subject = body.get("subject", existing.subject)
        existing.classGrade = body.get("classGrade", existing.classGrade)
        existing.description = body.get("description", existing.description)
        existing.category = body.get("category", existing.category or "Mavzulashtirilgan")
        existing.tags = body.get("tags", existing.tags or [])
        
        questions = body.get("questions") or []
        levels = body.get("levels") or []
        if questions:
            existing.questions = questions
            if not levels:
                n = len(questions)
                part = max(n // 3, 1)
                levels = [
                    {"difficulty": "Oson", "title": "1-bosqich: Boshlang'ich", "questions": questions[:part]},
                    {"difficulty": "O'rtacha", "title": "2-bosqich: O'rta", "questions": questions[part:part*2]},
                    {"difficulty": "Qiyin", "title": "3-bosqich: DTM darajasi", "questions": questions[part*2:]}
                ]
        if levels:
            existing.levels = levels
            
        db.commit()
        return {"success": True, "test": existing.to_dict()}
    finally:
        db.close()

@app.post("/api/teacher-tests/{test_id}/duplicate")
async def duplicate_teacher_test(test_id: str):
    db = SessionLocal()
    try:
        t = db.query(TeacherTestModel).filter(TeacherTestModel.id == test_id).first()
        if not t:
            raise HTTPException(status_code=404, detail="Test topilmadi")

        now = int(time.time() * 1000)
        cloned_id = f"test-{now}"
        cloned_test = TeacherTestModel(
            id=cloned_id,
            subject=t.subject,
            topic=f"{t.topic} (Nusxa)",
            classGrade=t.classGrade,
            description=t.description,
            teacherName=t.teacherName,
            category=t.category,
            tags=copy.deepcopy(t.tags or []),
            questions=copy.deepcopy(t.questions or []),
            levels=copy.deepcopy(t.levels or []),
            createdAt=now
        )
        db.add(cloned_test)
        db.commit()
        db.refresh(cloned_test)
        return {"success": True, "test": cloned_test.to_dict()}
    finally:
        db.close()

@app.delete("/api/teacher-tests/{test_id}")
async def delete_teacher_test(test_id: str):
    db = SessionLocal()
    try:
        t = db.query(TeacherTestModel).filter(TeacherTestModel.id == test_id).first()
        if t:
            db.delete(t)
            db.commit()
        return {"success": True}
    finally:
        db.close()

# -------------------------------------------------------------
# LIVE KAHOOT-STYLE TEST SYSTEM (WebSockets & REST APIs)
# -------------------------------------------------------------
class LiveTestConnectionManager:
    def __init__(self):
        # sessionId -> list of active WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, websocket: WebSocket, session_id: str):
        if session_id in self.active_connections:
            if websocket in self.active_connections[session_id]:
                self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            for connection in list(self.active_connections[session_id]):
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

live_test_manager = LiveTestConnectionManager()

@app.websocket("/ws/live-test/{session_id}")
async def websocket_live_test_endpoint(websocket: WebSocket, session_id: str):
    await live_test_manager.connect(websocket, session_id)
    db = SessionLocal()
    try:
        while True:
            data = await websocket.receive_json()
            event_type = data.get("type")

            if event_type == "ping":
                await websocket.send_json({"type": "pong", "time": int(time.time() * 1000)})

            elif event_type == "join_lobby":
                student_id = data.get("studentId")
                student_name = data.get("studentName")
                # Broadcast participant count update
                parts = db.query(LiveParticipantModel).filter(LiveParticipantModel.sessionId == session_id).all()
                await live_test_manager.broadcast(session_id, {
                    "type": "lobby_update",
                    "participantCount": len(parts),
                    "participants": [p.to_dict() for p in parts]
                })

            elif event_type == "start_test":
                session = db.query(LiveTestSessionModel).filter(LiveTestSessionModel.id == session_id).first()
                if session and session.status == "lobby":
                    now = int(time.time() * 1000)
                    total_min = session.settings.get("totalTimeLimit", 15) if session.settings else 15
                    session.status = "active"
                    session.startTime = now
                    session.endTime = now + (total_min * 60 * 1000)
                    db.query(LiveParticipantModel).filter(LiveParticipantModel.sessionId == session_id).update({
                        LiveParticipantModel.status: "in_progress"
                    })
                    db.commit()
                    await live_test_manager.broadcast(session_id, {
                        "type": "test_started",
                        "startTime": session.startTime,
                        "endTime": session.endTime,
                        "settings": session.settings or {}
                    })

            elif event_type == "submit_answer":
                part_id = data.get("participantId")
                q_id = str(data.get("questionId"))
                student_ans = data.get("answer")
                time_spent = data.get("timeSpentMs", 0)

                part = db.query(LiveParticipantModel).filter(LiveParticipantModel.id == part_id).first()
                session = db.query(LiveTestSessionModel).filter(LiveTestSessionModel.id == session_id).first()
                if part and session:
                    questions = session.questions or []
                    target_q = next((q for q in questions if str(q.get("id")) == q_id), None)
                    is_correct = False
                    earned_points = 0
                    if target_q:
                        correct_val = target_q.get("correctAnswer")
                        q_type = target_q.get("type", "single_choice")
                        base_pts = target_q.get("points", 1000)

                        if q_type in ["single_choice", "true_false"]:
                            is_correct = str(student_ans).strip().lower() == str(correct_val).strip().lower()
                        elif q_type == "multiple_choice":
                            if isinstance(student_ans, list) and isinstance(correct_val, list):
                                is_correct = set(str(x) for x in student_ans) == set(str(x) for x in correct_val)
                        elif q_type == "short_answer":
                            is_correct = str(student_ans or "").strip().lower() == str(correct_val or "").strip().lower()

                        if is_correct:
                            speed_scoring = session.settings.get("speedScoring", True) if session.settings else True
                            if speed_scoring:
                                per_q_sec = (session.settings.get("perQuestionTime") or 30) if session.settings else 30
                                max_ms = per_q_sec * 1000
                                ratio = max(0.0, min(1.0, 1.0 - (time_spent / max(max_ms, 1))))
                                earned_points = int(base_pts * (0.5 + 0.5 * ratio))
                            else:
                                earned_points = base_pts

                    ans_dict = dict(part.answers or {})
                    ans_dict[q_id] = {
                        "answer": student_ans,
                        "isCorrect": is_correct,
                        "pointsEarned": earned_points,
                        "timeSpentMs": time_spent
                    }
                    part.answers = ans_dict
                    flag_modified(part, "answers")
                    part.score = sum(a.get("pointsEarned", 0) for a in ans_dict.values())
                    part.correctCount = sum(1 for a in ans_dict.values() if a.get("isCorrect"))
                    part.incorrectCount = sum(1 for a in ans_dict.values() if not a.get("isCorrect"))
                    part.totalAnswered = len(ans_dict)
                    part.currentQuestionIndex = min(part.totalAnswered, len(questions) - 1)
                    part.lastActiveAt = int(time.time() * 1000)

                    if part.totalAnswered >= len(questions):
                        part.status = "submitted"
                        part.finishedAt = int(time.time() * 1000)

                    db.commit()

                    # Compute live leaderboard
                    all_parts = db.query(LiveParticipantModel).filter(LiveParticipantModel.sessionId == session_id).all()
                    sorted_parts = sorted(all_parts, key=lambda p: (p.score or 0), reverse=True)
                    leaderboard = [
                        {
                            "id": p.id,
                            "studentName": p.studentName,
                            "score": p.score,
                            "rank": idx + 1,
                            "correctCount": p.correctCount,
                            "totalAnswered": p.totalAnswered,
                            "status": p.status
                        }
                        for idx, p in enumerate(sorted_parts[:10])
                    ]

                    # Broadcast progress and leaderboard to all listeners
                    await live_test_manager.broadcast(session_id, {
                        "type": "progress_update",
                        "participant": part.to_dict(),
                        "leaderboard": leaderboard
                    })

            elif event_type == "cheat_log":
                part_id = data.get("participantId")
                cheat_type = data.get("cheatType", "tab_switch")
                part = db.query(LiveParticipantModel).filter(LiveParticipantModel.id == part_id).first()
                if part:
                    part.cheatCount = (part.cheatCount or 0) + 1
                    logs = list(part.cheatLogs or [])
                    logs.append({
                        "type": cheat_type,
                        "time": int(time.time() * 1000),
                        "count": part.cheatCount
                    })
                    part.cheatLogs = logs
                    flag_modified(part, "cheatLogs")
                    db.commit()
                    await live_test_manager.broadcast(session_id, {
                        "type": "cheat_alert",
                        "participantId": part.id,
                        "studentName": part.studentName,
                        "cheatType": cheat_type,
                        "cheatCount": part.cheatCount
                    })

    except WebSocketDisconnect:
        live_test_manager.disconnect(websocket, session_id)
    except Exception as ws_err:
        print("Live test WS error:", ws_err)
        live_test_manager.disconnect(websocket, session_id)
    finally:
        db.close()

# -------------------------------------------------------------
# LIVE TEST REST APIS
# -------------------------------------------------------------
@app.post("/api/live-test/create-session")
async def create_live_session(request: Request):
    user_role = request.headers.get("X-User-Role")
    user_id = request.headers.get("X-User-Id")
    if user_role == "student":
        raise HTTPException(status_code=403, detail="Faqat o'qituvchilar jonli test boshlashi mumkin.")

    body = await request.json()
    test_id = body.get("testId")
    group_id = body.get("groupId") # "all" or group ID
    settings = body.get("settings") or {}

    if not test_id:
        raise HTTPException(status_code=400, detail="Test ID kiritilishi shart")

    db = SessionLocal()
    try:
        test = db.query(TeacherTestModel).filter(TeacherTestModel.id == test_id).first() if test_id else None
        test_title = body.get("title") or body.get("testTitle") or "Biologiya Jonli Testi"
        subject = "Biologiya"
        class_grade = ""
        teacher_name_default = "Ustoz"
        raw_qs = []

        if test:
            test_title = test.topic
            subject = test.subject or "Biologiya"
            class_grade = test.classGrade or ""
            teacher_name_default = test.teacherName or "Ustoz"
            raw_qs = test.questions or []
            if not raw_qs and test.levels:
                for lvl in test.levels:
                    diff = lvl.get("difficulty", "O'rtacha")
                    for q in lvl.get("questions", []):
                        item = dict(q)
                        item["difficulty"] = diff
                        raw_qs.append(item)
        elif body.get("questions"):
            raw_qs = body.get("questions") or []
        else:
            raise HTTPException(status_code=404, detail="Test bazada topilmadi va savollar berilmagan")

        group_name = "Barcha o'quvchilar"
        if group_id and group_id != "all":
            grp = db.query(GroupModel).filter(GroupModel.id == group_id).first()
            if grp:
                group_name = grp.name

        # Generate unique 6-digit join code
        join_code = ""
        for _ in range(20):
            cand = str(random.randint(100000, 999999))
            active_existing = db.query(LiveTestSessionModel).filter(
                LiveTestSessionModel.code == cand,
                LiveTestSessionModel.status.in_(["lobby", "active", "paused"])
            ).first()
            if not active_existing:
                join_code = cand
                break
        if not join_code:
            join_code = str(int(time.time()))[-6:]

        now = int(time.time() * 1000)
        session_id = f"live-{now}-{join_code}"

        # Extract normalized questions list
        norm_questions = []
        if raw_qs:
            norm_questions = copy.deepcopy(raw_qs)

        # Ensure question properties
        for idx, q in enumerate(norm_questions):
            if "id" not in q:
                q["id"] = idx + 1
            if "points" not in q:
                q["points"] = 1000
            if "type" not in q:
                q["type"] = "single_choice"
            if not q.get("text") and q.get("question"):
                q["text"] = q["question"]
            elif not q.get("question") and q.get("text"):
                q["question"] = q["text"]
            # Normalize correctAnswer from answerIndex if needed
            if not q.get("correctAnswer") and "answerIndex" in q:
                opts = q.get("options")
                if isinstance(opts, list) and isinstance(q.get("answerIndex"), int):
                    idx_val = q.get("answerIndex")
                    if 0 <= idx_val < len(opts):
                        q["correctAnswer"] = str(opts[idx_val])

        teacher_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        t_name = teacher_user.fullName if teacher_user else teacher_name_default

        new_session = LiveTestSessionModel(
            id=session_id,
            code=join_code,
            testId=test.id if test else (test_id or session_id),
            testTitle=test_title,
            subject=subject,
            classGrade=class_grade,
            teacherId=user_id or "teacher-1",
            teacherName=t_name,
            groupId=group_id or "all",
            groupName=group_name,
            status="lobby",
            settings=settings,
            questions=norm_questions,
            startTime=0,
            endTime=0,
            pausedAt=0,
            totalPausedDuration=0,
            timeExtendedSeconds=0,
            createdAt=now
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)

        return {
            "success": True,
            "session": new_session.to_dict(),
            "code": join_code,
            "joinUrl": f"/student/live-test.html?code={join_code}",
            "teacherUrl": f"/teacher/live-test.html?sessionId={session_id}"
        }
    finally:
        db.close()

@app.get("/api/live-test/session/{code_or_id}")
async def get_live_session_info(code_or_id: str, request: Request):
    db = SessionLocal()
    try:
        session = db.query(LiveTestSessionModel).filter(
            (LiveTestSessionModel.code == code_or_id) | (LiveTestSessionModel.id == code_or_id)
        ).first()

        if not session:
            raise HTTPException(status_code=404, detail="Jonli test sessiyasi topilmadi. Kodni qayta tekshiring.")

        # If user is teacher, send full questions. If student in lobby, omit answers
        user_role = request.headers.get("X-User-Role")
        session_data = session.to_dict()

        if user_role != "teacher" and session.status == "lobby":
            # Strip correct answers and question details in lobby to prevent early leak
            session_data["questions"] = []

        # Also get participant count
        part_count = db.query(LiveParticipantModel).filter(LiveParticipantModel.sessionId == session.id).count()
        session_data["participantCount"] = part_count

        return {"success": True, "session": session_data}
    finally:
        db.close()

@app.post("/api/live-test/join")
async def join_live_session(request: Request):
    body = await request.json()
    code = (body.get("code") or "").strip()
    student_id = body.get("studentId")
    student_name = (body.get("studentName") or "").strip()
    is_guest = bool(body.get("isGuest", False))

    if not code:
        raise HTTPException(status_code=400, detail="6 xonali test kodi kiritilishi shart")

    db = SessionLocal()
    try:
        session = db.query(LiveTestSessionModel).filter(LiveTestSessionModel.code == code).first()
        if not session:
            raise HTTPException(status_code=404, detail="Bunday kodli jonli test topilmadi.")

        if session.status == "finished":
            raise HTTPException(status_code=400, detail="Ushbu test allaqachon yakunlangan.")

        # Check group permission if group restricted
        if session.groupId and session.groupId != "all":
            if student_id and not is_guest:
                user = db.query(UserModel).filter(UserModel.id == student_id).first()
                if user and user.groupId and user.groupId != session.groupId:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Ushbu test faqat '{session.groupName}' guruhi o'quvchilari uchun mo'ljallangan."
                    )

        if not student_name:
            if student_id:
                user = db.query(UserModel).filter(UserModel.id == student_id).first()
                student_name = user.fullName if user else "O'quvchi"
            else:
                student_name = "Mehmon o'quvchi"

        if not student_id:
            student_id = f"guest-{int(time.time()*1000)}-{random.randint(100,999)}"
            is_guest = True

        part_id = f"part-{session.id}-{student_id}"
        part = db.query(LiveParticipantModel).filter(LiveParticipantModel.id == part_id).first()

        now = int(time.time() * 1000)
        if not part:
            part = LiveParticipantModel(
                id=part_id,
                sessionId=session.id,
                studentId=student_id,
                studentName=student_name,
                isGuest=1 if is_guest else 0,
                isOnline=1,
                currentQuestionIndex=0,
                score=0,
                correctCount=0,
                incorrectCount=0,
                totalAnswered=0,
                answers={},
                cheatLogs=[],
                cheatCount=0,
                status="lobby" if session.status == "lobby" else "in_progress",
                joinedAt=now,
                finishedAt=0,
                lastActiveAt=now
            )
            db.add(part)
            db.commit()
            db.refresh(part)
        else:
            part.isOnline = 1
            part.lastActiveAt = now
            db.commit()

        # Notify lobby via WebSocket
        all_parts = db.query(LiveParticipantModel).filter(LiveParticipantModel.sessionId == session.id).all()
        await live_test_manager.broadcast(session.id, {
            "type": "lobby_update",
            "participantCount": len(all_parts),
            "participants": [p.to_dict() for p in all_parts]
        })

        # Prepare questions for student: if shuffle enabled, randomize order
        questions = copy.deepcopy(session.questions or [])
        if session.settings and session.settings.get("shuffleQuestions", True):
            # Seed with participant ID so reconnect preserves exact order
            random.Random(student_id).shuffle(questions)

        if session.settings and session.settings.get("shuffleOptions", True):
            for q in questions:
                if q.get("type") in ["single_choice", "multiple_choice"] and isinstance(q.get("options"), list):
                    opts = list(q.get("options"))
                    random.Random(student_id + str(q.get("id"))).shuffle(opts)
                    q["options"] = opts

        # Strip internal correct answers from payload sent to student runner
        student_safe_questions = []
        for q in questions:
            item = dict(q)
            item.pop("correctAnswer", None)
            item.pop("explanation", None)
            student_safe_questions.append(item)

        return {
            "success": True,
            "session": session.to_dict(),
            "participant": part.to_dict(),
            "questions": student_safe_questions,
            "totalQuestions": len(student_safe_questions)
        }
    finally:
        db.close()

@app.get("/api/live-test/session/{session_id}/monitor")
async def get_live_monitor_data(session_id: str, request: Request):
    user_role = request.headers.get("X-User-Role")
    if user_role == "student":
        raise HTTPException(status_code=403, detail="Faqat o'qituvchi kuzatuv paneliga kirishi mumkin.")

    db = SessionLocal()
    try:
        session = db.query(LiveTestSessionModel).filter(LiveTestSessionModel.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Sessiya topilmadi")

        participants = db.query(LiveParticipantModel).filter(LiveParticipantModel.sessionId == session_id).all()
        questions = session.questions or []
        total_q = max(len(questions), 1)

        # Student progress list
        student_rows = []
        question_mistakes: Dict[str, int] = {str(q.get("id")): 0 for q in questions}

        for p in participants:
            ans = p.answers or {}
            progress_pct = round((len(ans) / total_q) * 100)
            acc_pct = round((p.correctCount / max(len(ans), 1)) * 100) if ans else 0

            # Track which questions were wrong
            wrong_q_ids = []
            for q_id_key, a_val in ans.items():
                if not a_val.get("isCorrect"):
                    wrong_q_ids.append(q_id_key)
                    question_mistakes[q_id_key] = question_mistakes.get(q_id_key, 0) + 1

            student_rows.append({
                "id": p.id,
                "studentId": p.studentId,
                "studentName": p.studentName,
                "isOnline": bool(p.isOnline),
                "currentQuestionIndex": p.currentQuestionIndex,
                "score": p.score,
                "correctCount": p.correctCount,
                "incorrectCount": p.incorrectCount,
                "totalAnswered": len(ans),
                "progressPct": progress_pct,
                "accuracyPct": acc_pct,
                "wrongQuestions": wrong_q_ids,
                "cheatCount": p.cheatCount or 0,
                "status": p.status,
                "lastActiveAt": p.lastActiveAt
            })

        # Calculate group summary
        avg_score = round(sum(r["score"] for r in student_rows) / max(len(student_rows), 1)) if student_rows else 0
        avg_acc = round(sum(r["accuracyPct"] for r in student_rows) / max(len(student_rows), 1)) if student_rows else 0
        finished_count = sum(1 for r in student_rows if r["status"] in ["submitted", "timed_out"])
        completion_rate = round((finished_count / max(len(student_rows), 1)) * 100) if student_rows else 0

        # Find hardest question
        hardest_q = None
        if question_mistakes:
            sorted_mistakes = sorted(question_mistakes.items(), key=lambda x: x[1], reverse=True)
            top_wrong_id, top_wrong_count = sorted_mistakes[0]
            if top_wrong_count > 0:
                matching_q = next((q for q in questions if str(q.get("id")) == top_wrong_id), None)
                if matching_q:
                    hardest_q = {
                        "id": top_wrong_id,
                        "question": matching_q.get("question"),
                        "wrongCount": top_wrong_count
                    }

        # Leaderboard
        sorted_leaderboard = sorted(student_rows, key=lambda r: (r["score"], -r["cheatCount"]), reverse=True)
        for idx, item in enumerate(sorted_leaderboard):
            item["rank"] = idx + 1

        return {
            "success": True,
            "session": session.to_dict(),
            "participants": sorted_leaderboard,
            "totalParticipants": len(student_rows),
            "onlineCount": sum(1 for r in student_rows if r["isOnline"]),
            "summary": {
                "averageScore": avg_score,
                "averageAccuracy": avg_acc,
                "completionRate": completion_rate,
                "finishedCount": finished_count,
                "hardestQuestion": hardest_q
            },
            "leaderboard": sorted_leaderboard[:10]
        }
    finally:
        db.close()

@app.post("/api/live-test/session/{session_id}/action")
async def handle_live_session_action(session_id: str, request: Request):
    user_role = request.headers.get("X-User-Role")
    if user_role == "student":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan.")

    body = await request.json()
    action = body.get("action")

    db = SessionLocal()
    try:
        session = db.query(LiveTestSessionModel).filter(LiveTestSessionModel.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Sessiya topilmadi")

        now = int(time.time() * 1000)

        if action == "start":
            total_min = session.settings.get("totalTimeLimit", 15) if session.settings else 15
            session.status = "active"
            session.startTime = now
            session.endTime = now + (total_min * 60 * 1000)
            db.query(LiveParticipantModel).filter(LiveParticipantModel.sessionId == session_id).update({
                LiveParticipantModel.status: "in_progress"
            })
            db.commit()
            await live_test_manager.broadcast(session_id, {
                "type": "test_started",
                "startTime": session.startTime,
                "endTime": session.endTime,
                "settings": session.settings or {}
            })

        elif action == "pause":
            session.status = "paused"
            session.pausedAt = now
            db.commit()
            await live_test_manager.broadcast(session_id, {
                "type": "test_paused",
                "message": "Ustoz testni vaqtincha to'xtatdi."
            })

        elif action == "resume":
            if session.pausedAt > 0:
                paused_dur = now - session.pausedAt
                session.totalPausedDuration = (session.totalPausedDuration or 0) + int(paused_dur / 1000)
                session.endTime = session.endTime + paused_dur
            session.status = "active"
            session.pausedAt = 0
            db.commit()
            await live_test_manager.broadcast(session_id, {
                "type": "test_resumed",
                "newEndTime": session.endTime
            })

        elif action == "extend_time":
            add_sec = int(body.get("seconds", 300)) # default 5 minutes
            session.endTime = session.endTime + (add_sec * 1000)
            session.timeExtendedSeconds = (session.timeExtendedSeconds or 0) + add_sec
            db.commit()
            await live_test_manager.broadcast(session_id, {
                "type": "time_extended",
                "additionalSeconds": add_sec,
                "newEndTime": session.endTime
            })

        elif action == "end":
            session.status = "finished"
            # Auto-submit all participants
            db.query(LiveParticipantModel).filter(
                LiveParticipantModel.sessionId == session_id,
                LiveParticipantModel.status.in_(["lobby", "in_progress"])
            ).update({
                LiveParticipantModel.status: "submitted",
                LiveParticipantModel.finishedAt: now
            })
            db.commit()
            await live_test_manager.broadcast(session_id, {
                "type": "test_ended",
                "message": "Test ustoz tomonidan yakunlandi."
            })

        elif action == "toggle_show_results":
            st = dict(session.settings or {})
            curr = st.get("showResultsToStudents", True)
            st["showResultsToStudents"] = not curr
            session.settings = st
            flag_modified(session, "settings")
            db.commit()
            await live_test_manager.broadcast(session_id, {
                "type": "settings_updated",
                "settings": session.settings
            })

        return {"success": True, "session": session.to_dict()}
    finally:
        db.close()

@app.post("/api/live-test/session/{session_id}/submit")
async def submit_live_test_answer(session_id: str, request: Request):
    body = await request.json()
    part_id = body.get("participantId")
    q_id = str(body.get("questionId"))
    student_ans = body.get("answer")
    time_spent = body.get("timeSpentMs", 0)

    db = SessionLocal()
    try:
        part = db.query(LiveParticipantModel).filter(LiveParticipantModel.id == part_id).first()
        session = db.query(LiveTestSessionModel).filter(LiveTestSessionModel.id == session_id).first()

        if not part or not session:
            raise HTTPException(status_code=404, detail="Qatnashuvchi yoki sessiya topilmadi")

        questions = session.questions or []
        target_q = next((q for q in questions if str(q.get("id")) == q_id), None)
        is_correct = False
        earned_points = 0

        if target_q:
            correct_val = target_q.get("correctAnswer")
            if not correct_val and "answerIndex" in target_q:
                opts = target_q.get("options", [])
                a_idx = target_q.get("answerIndex")
                if isinstance(opts, list) and isinstance(a_idx, int) and 0 <= a_idx < len(opts):
                    correct_val = str(opts[a_idx])

            q_type = target_q.get("type", "single_choice")
            base_pts = target_q.get("points", 1000)

            if q_type in ["single_choice", "true_false"]:
                s_str = str(student_ans or "").strip().lower()
                c_str = str(correct_val or "").strip().lower()
                is_correct = (s_str == c_str)
                # Check index fallback if needed
                if not is_correct and "answerIndex" in target_q and isinstance(target_q.get("options"), list):
                    opts = target_q.get("options")
                    a_idx = target_q.get("answerIndex")
                    if 0 <= a_idx < len(opts) and s_str == str(opts[a_idx]).strip().lower():
                        is_correct = True
                    elif str(student_ans).strip() == str(a_idx):
                        is_correct = True
            elif q_type == "multiple_choice":
                if isinstance(student_ans, list) and isinstance(correct_val, list):
                    is_correct = set(str(x).strip().lower() for x in student_ans) == set(str(x).strip().lower() for x in correct_val)
            elif q_type == "short_answer":
                is_correct = str(student_ans or "").strip().lower() == str(correct_val or "").strip().lower()

            if is_correct:
                speed_scoring = session.settings.get("speedScoring", True) if session.settings else True
                if speed_scoring:
                    per_q_sec = (session.settings.get("perQuestionTime") or 30) if session.settings else 30
                    max_ms = per_q_sec * 1000
                    ratio = max(0.0, min(1.0, 1.0 - (time_spent / max(max_ms, 1))))
                    earned_points = int(base_pts * (0.5 + 0.5 * ratio))
                else:
                    earned_points = base_pts

        ans_dict = dict(part.answers or {})
        ans_dict[q_id] = {
            "answer": student_ans,
            "isCorrect": is_correct,
            "pointsEarned": earned_points,
            "timeSpentMs": time_spent
        }
        part.answers = ans_dict
        flag_modified(part, "answers")
        part.score = sum(a.get("pointsEarned", 0) for a in ans_dict.values())
        part.correctCount = sum(1 for a in ans_dict.values() if a.get("isCorrect"))
        part.incorrectCount = sum(1 for a in ans_dict.values() if not a.get("isCorrect"))
        part.totalAnswered = len(ans_dict)
        part.currentQuestionIndex = min(part.totalAnswered, len(questions) - 1)
        part.lastActiveAt = int(time.time() * 1000)

        if part.totalAnswered >= len(questions):
            part.status = "submitted"
            part.finishedAt = int(time.time() * 1000)

        db.commit()

        # Broadcast progress
        await live_test_manager.broadcast(session.id, {
            "type": "progress_update",
            "participant": part.to_dict()
        })

        return {
            "success": True,
            "isCorrect": is_correct,
            "earnedPoints": earned_points,
            "totalScore": part.score,
            "isFinished": part.status == "submitted"
        }
    finally:
        db.close()

@app.post("/api/live-test/session/{session_id}/cheat-log")
async def record_cheat_log(session_id: str, request: Request):
    body = await request.json()
    part_id = body.get("participantId")
    cheat_type = body.get("cheatType", "tab_switch")

    db = SessionLocal()
    try:
        part = db.query(LiveParticipantModel).filter(LiveParticipantModel.id == part_id).first()
        if part:
            part.cheatCount = (part.cheatCount or 0) + 1
            logs = list(part.cheatLogs or [])
            logs.append({
                "type": cheat_type,
                "time": int(time.time() * 1000),
                "count": part.cheatCount
            })
            part.cheatLogs = logs
            flag_modified(part, "cheatLogs")
            db.commit()

            await live_test_manager.broadcast(session_id, {
                "type": "cheat_alert",
                "participantId": part.id,
                "studentName": part.studentName,
                "cheatType": cheat_type,
                "cheatCount": part.cheatCount
            })
        return {"success": True}
    finally:
        db.close()

@app.get("/api/live-test/session/{session_id}/results")
async def get_live_test_results(session_id: str, request: Request):
    db = SessionLocal()
    try:
        session = db.query(LiveTestSessionModel).filter(LiveTestSessionModel.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Sessiya topilmadi")

        participants = db.query(LiveParticipantModel).filter(LiveParticipantModel.sessionId == session_id).all()
        questions = session.questions or []
        total_q = max(len(questions), 1)

        # Ranked list
        sorted_parts = sorted(participants, key=lambda p: (p.score or 0), reverse=True)
        ranked_list = []
        for idx, p in enumerate(sorted_parts):
            p_dict = p.to_dict()
            p_dict["rank"] = idx + 1
            p_dict["accuracyPct"] = round((p.correctCount / max(p.totalAnswered, 1)) * 100) if p.totalAnswered else 0
            ranked_list.append(p_dict)

        # Question statistics breakdown
        q_stats = []
        for q in questions:
            q_id_str = str(q.get("id"))
            total_attempts = 0
            correct_attempts = 0
            for p in participants:
                ans = (p.answers or {}).get(q_id_str)
                if ans:
                    total_attempts += 1
                    if ans.get("isCorrect"):
                        correct_attempts += 1

            pct = round((correct_attempts / max(total_attempts, 1)) * 100) if total_attempts else 0
            q_text = q.get("text") or q.get("question") or f"Savol {q_id_str}"
            c_ans = q.get("correctAnswer")
            if not c_ans and "answerIndex" in q and isinstance(q.get("options"), list):
                a_idx = q.get("answerIndex")
                if isinstance(a_idx, int) and 0 <= a_idx < len(q["options"]):
                    c_ans = str(q["options"][a_idx])

            q_stats.append({
                "id": q_id_str,
                "text": q_text,
                "question": q_text,
                "type": q.get("type", "single_choice"),
                "totalAttempts": total_attempts,
                "correctAttempts": correct_attempts,
                "accuracyPct": pct,
                "options": q.get("options", []),
                "correctAnswer": str(c_ans or ""),
                "explanation": q.get("explanation") or ""
            })

        return {
            "success": True,
            "session": session.to_dict(),
            "participants": ranked_list,
            "totalParticipants": len(ranked_list),
            "questions": q_stats,
            "totalQuestions": len(questions),
            "summary": {
                "averageScore": round(sum(p["score"] for p in ranked_list) / max(len(ranked_list), 1)) if ranked_list else 0,
                "averageAccuracy": round(sum(p["accuracyPct"] for p in ranked_list) / max(len(ranked_list), 1)) if ranked_list else 0,
                "topStudent": ranked_list[0] if ranked_list else None
            }
        }
    finally:
        db.close()

@app.get("/api/live-test/session/{session_id}/export-csv")
async def export_live_test_csv(session_id: str):
    db = SessionLocal()
    try:
        session = db.query(LiveTestSessionModel).filter(LiveTestSessionModel.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Sessiya topilmadi")

        participants = db.query(LiveParticipantModel).filter(LiveParticipantModel.sessionId == session_id).all()
        sorted_parts = sorted(participants, key=lambda p: (p.score or 0), reverse=True)
        questions = session.questions or []

        # Build CSV with UTF-8 BOM (\ufeff)
        lines = [
            "\ufeff" + f"Jonli Test Hisoboti: {session.testTitle}",
            f"Guruh: {session.groupName}, Sana: {time.strftime('%Y-%m-%d %H:%M', time.localtime(session.createdAt / 1000))}",
            ""
        ]

        # Header row
        header = ["O'rin", "O'quvchi F.I.Sh.", "To'plangan Ball", "To'g'ri", "Noto'g'ri", "Jami Yechilgan", "Aniqlik (%)", "Qoidabuzarliklar", "Holat"]
        for idx, q in enumerate(questions):
            header.append(f"Savol {idx+1}")
        lines.append('"' + '","'.join(header) + '"')

        # Data rows
        for idx, p in enumerate(sorted_parts):
            acc_pct = round((p.correctCount / max(p.totalAnswered, 1)) * 100) if p.totalAnswered else 0
            row = [
                str(idx + 1),
                p.studentName.replace('"', '""'),
                str(p.score or 0),
                str(p.correctCount or 0),
                str(p.incorrectCount or 0),
                str(p.totalAnswered or 0),
                f"{acc_pct}%",
                str(p.cheatCount or 0),
                p.status
            ]
            for q in questions:
                q_id_str = str(q.get("id"))
                ans_info = (p.answers or {}).get(q_id_str)
                if not ans_info:
                    row.append("Yechilmagan")
                elif ans_info.get("isCorrect"):
                    row.append(f"To'g'ri (+{ans_info.get('pointsEarned', 0)})")
                else:
                    row.append("Noto'g'ri")

            lines.append('"' + '","'.join(row) + '"')

        csv_content = "\r\n".join(lines)
        filename = f"Jonli_Test_{session.code}_{time.strftime('%Y%m%d')}.csv"
        return Response(
            content=csv_content.encode("utf-8-sig"),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    finally:
        db.close()

@app.get("/enter")
async def enter_page():
    return FileResponse(FRONTEND_DIR / "join.html")

@app.post("/api/live-test/session/{session_id}/terminate")
async def terminate_live_session(session_id: str, request: Request):
    user_role = request.headers.get("X-User-Role")
    if user_role == "student":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")
    db = SessionLocal()
    try:
        session = db.query(LiveTestSessionModel).filter(LiveTestSessionModel.id == session_id).first()
        if session:
            session.status = "finished"
            db.commit()
            await live_test_manager.broadcast(session_id, {
                "type": "test_ended",
                "message": "Test ustoz tomonidan yakunlandi."
            })
        return {"success": True}
    finally:
        db.close()

@app.get("/api/live-test/history")
async def get_live_test_history(request: Request):
    user_role = request.headers.get("X-User-Role")
    if user_role == "student":
        raise HTTPException(status_code=403, detail="Faqat o'qituvchilar ko'ra oladi.")

    db = SessionLocal()
    try:
        now = int(time.time() * 1000)
        # Auto-expire completed or stale sessions
        stale_sessions = db.query(LiveTestSessionModel).filter(
            LiveTestSessionModel.status.in_(["lobby", "active", "paused"])
        ).all()
        for s in stale_sessions:
            if s.status in ["active", "paused"] and s.endTime > 0 and now > s.endTime:
                s.status = "finished"
            elif s.status == "lobby" and (now - (s.createdAt or 0) > 4 * 3600 * 1000):
                s.status = "finished"
        db.commit()

        sessions = db.query(LiveTestSessionModel).order_by(LiveTestSessionModel.createdAt.desc()).limit(30).all()
        res_list = []
        for s in sessions:
            p_count = db.query(LiveParticipantModel).filter(LiveParticipantModel.sessionId == s.id).count()
            s_dict = s.to_dict()
            s_dict["participantCount"] = p_count
            res_list.append(s_dict)
        return {"success": True, "history": res_list}
    finally:
        db.close()

@app.get("/api/student/active-live-tests")
async def get_student_active_live_tests(request: Request):
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        return {"activeTests": []}

    db = SessionLocal()
    try:
        now = int(time.time() * 1000)
        # Auto-expire completed or stale sessions
        stale_sessions = db.query(LiveTestSessionModel).filter(
            LiveTestSessionModel.status.in_(["lobby", "active", "paused"])
        ).all()
        for s in stale_sessions:
            if s.status in ["active", "paused"] and s.endTime > 0 and now > s.endTime:
                s.status = "finished"
            elif s.status == "lobby" and (now - (s.createdAt or 0) > 4 * 3600 * 1000):
                s.status = "finished"
        db.commit()

        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        student_group = user.groupId if user else None

        active_sessions = db.query(LiveTestSessionModel).filter(
            LiveTestSessionModel.status.in_(["lobby", "active", "paused"])
        ).order_by(LiveTestSessionModel.createdAt.desc()).all()

        results = []
        for s in active_sessions:
            if s.groupId == "all" or s.groupId == student_group or not s.groupId:
                results.append({
                    "id": s.id,
                    "code": s.code,
                    "testTitle": s.testTitle,
                    "subject": s.subject,
                    "teacherName": s.teacherName,
                    "groupName": s.groupName,
                    "status": s.status,
                    "questionsCount": len(s.questions or []),
                    "totalTimeLimit": s.settings.get("totalTimeLimit", 15) if s.settings else 15,
                    "joinUrl": f"/student/live-test.html?code={s.code}"
                })
        return {"activeTests": results}
    finally:
        db.close()

# -------------------------------------------------------------
# TEACHER AI ASSISTANT API
# -------------------------------------------------------------
@app.post("/api/teacher/ai-assistant")
async def teacher_ai_assistant(request: Request):
    user_role = request.headers.get("X-User-Role")
    user_id = request.headers.get("X-User-Id")
    if user_role == "student":
        raise HTTPException(
            status_code=403,
            detail="Talabalar uchun sun'iy intellekt xizmati mavjud emas. Ruxsat berilmagan."
        )

    body = await request.json()
    task_type = body.get("type", "chat")
    raw_message = (body.get("message") or body.get("prompt") or body.get("topic") or "").strip()
    subject = body.get("subject") or "Biologiya"
    grade = body.get("grade") or "8-sinf"

    if not raw_message and task_type not in ["lesson_plan", "experiment"]:
        raise HTTPException(status_code=400, detail="Xabar matni bo'sh bo'lishi mumkin emas")

    user_message = raw_message or f"{grade} {subject} mavzusi"
    user_lower = user_message.lower()

    db = SessionLocal()
    try:
        # Check if caller is student in DB
        if user_id and user_id != "undefined":
            user_check = db.query(UserModel).filter(UserModel.id == user_id).first()
            if user_check and user_check.role == "student":
                raise HTTPException(status_code=403, detail="Talabalar uchun sun'iy intellekt xizmati mavjud emas.")

        # 1. Match @ book mention, attached resource ID or textbook reference from library
        resources = db.query(ResourceModel).all()
        matched_resource = None

        # Check explicit attachedResourceId in request body
        attached_res_id = body.get("attachedResourceId") or body.get("resourceId")
        if attached_res_id:
            matched_resource = db.query(ResourceModel).filter(ResourceModel.id == attached_res_id).first()

        # Check patterns like @["Title"], @"Title", @[Title], or @Title
        if not matched_resource:
            book_mention_match = re.search(r'@\[(.*?)\]|@"([^"]+)"|@([a-zA-Z0-9_\-а-яА-ЯёЁ\s]+)', user_message)
            if book_mention_match:
                mention_raw = (book_mention_match.group(1) or book_mention_match.group(2) or book_mention_match.group(3) or "").strip().lower()
                if mention_raw:
                    for r in resources:
                        if mention_raw in r.title.lower() or mention_raw in (r.subject or "").lower() or r.title.lower() in mention_raw:
                            matched_resource = r
                            break

        # Check direct mentions of existing book titles
        if not matched_resource:
            for r in resources:
                if len(r.title) > 3 and r.title.lower() in user_lower:
                    matched_resource = r
                    break

        # Check intent: Test creation / questions generation
        is_test_intent = any(k in user_lower for k in [
            "test tuz", "test yarat", "savollar tuz", "test markaziga qo'sh",
            "test markazida qo'sh", "test tayyorla", "test sinovi", "savol tuz",
            "test tuzib ber", "test tuzsin", "test qil", "test bering", "test tuzib",
            "savollar shakllantir", "test savollari"
        ]) or (matched_resource is not None and any(w in user_lower for w in ["test", "savol", "imtihon", "savollar tuz"]))

        # Check intent: Study / analyze textbook
        is_study_intent = matched_resource is not None and any(w in user_lower for w in [
            "o'rgan", "organ", "tahlil", "mazmun", "mundarija", "haqida", "qanday kitob", "nimalar bor", "tushuntir", "ko'rib chiq"
        ]) and not is_test_intent

        # Check intent: Account and student statistics
        is_stats_intent = any(k in user_lower for k in [
            "statistika", "hisobot", "o'zlashtirish", "o'quvchilar ko'rsatkichi",
            "faollik", "reyting", "account statistikasi", "platforma statistikasi",
            "o'quvchilar statistikasi", "baholar", "nechta o'quvchi", "ballar",
            "guruhlar statistikasi", "o'quvchilar natija"
        ]) and not is_test_intent and not is_study_intent

        # -------------------------------------------------------------
        # 1. ACCOUNT & STUDENT STATISTICS INTENT
        # -------------------------------------------------------------
        if is_stats_intent:
            all_students = db.query(UserModel).filter(UserModel.role == "student").all()
            approved_students = [s for s in all_students if getattr(s, "status", "pending") == "approved"]
            pending_students = [s for s in all_students if getattr(s, "status", "pending") != "approved"]

            groups = db.query(GroupModel).all()
            group_summaries = []
            for g in groups:
                g_students = [s for s in all_students if s.groupId == g.id or s.classGrade == g.name]
                group_summaries.append(f"{g.name} ({len(g_students)} nafar o'quvchi)")

            submissions = db.query(SubmissionModel).all()
            total_tests_taken = len(submissions)
            avg_score = round(sum(s.percentage for s in submissions) / max(total_tests_taken, 1), 1) if submissions else 0

            high_scores = len([s for s in submissions if s.percentage >= 85])
            mid_scores = len([s for s in submissions if 70 <= s.percentage < 85])
            low_scores = len([s for s in submissions if s.percentage < 70])

            student_stats = []
            for s in approved_students:
                s_subs = [sub for sub in submissions if sub.studentId == s.id]
                s_avg = round(sum(sub.percentage for sub in s_subs) / len(s_subs), 1) if s_subs else 0
                student_stats.append({
                    "name": s.fullName,
                    "grade": s.classGrade or "Noma'lum",
                    "testCount": len(s_subs),
                    "avgScore": s_avg
                })

            active_students = [s for s in student_stats if s["testCount"] > 0]
            active_students.sort(key=lambda x: x["avgScore"], reverse=True)
            top_students = active_students[:5]
            struggling_students = [s for s in active_students if s["avgScore"] < 60]

            homeworks = db.query(HomeworkModel).all()
            total_hw = len(homeworks)
            total_hw_subs = sum(len(hw.submissions or []) for hw in homeworks)

            teacher_tests = db.query(TeacherTestModel).all()
            resources_count = len(resources)

            stats_context = f"""
JAMI MA'LUMOTLAR:
- Jami ro'yxatdan o'tgan o'quvchilar: {len(all_students)} nafar (Tasdiqlangan: {len(approved_students)}, Kutilayotgan: {len(pending_students)})
- Guruhlar ({len(groups)} ta): {', '.join(group_summaries) if group_summaries else 'Guruhlar kiritilmagan'}
- Test Markazidagi mavzular soni: {len(teacher_tests)} ta
- O'quvchilar topshirgan testlar jami: {total_tests_taken} marta
- O'quvchilarning umumiy o'rtacha balli: {avg_score}%
- Baholanish taqsimoti: A'lo (85-100%): {high_scores} ta, Yaxshi (70-84%): {mid_scores} ta, Qoniqarli/Past (<70%): {low_scores} ta
- Top o'quvchilar: {', '.join([f"{st['name']} ({st['grade']}, o'rtacha {st['avgScore']}%)" for st in top_students]) if top_students else "Hali yetarli test yechilmagan"}
- Qo'shimcha yordamga muhtoj o'quvchilar (<60%): {', '.join([f"{st['name']} ({st['grade']}, {st['avgScore']}%)" for st in struggling_students]) if struggling_students else "Hozircha past balli o'quvchi yo'q"}
- Berilgan uyga vazifalar: {total_hw} ta, o'quvchilar javoblari: {total_hw_subs} ta
- Kutubxonadagi darslik va resurslar: {resources_count} ta
"""
            system_prompt = """Siz maktabning bosh pedagogik tahlilchisi va AI metodistisiz.
Faqat maktab o'qituvchilari uchun platforma statistikasi, o'quvchilar o'zlashtirishi, faollik va ta'lim sifatini tahlil qilasiz.
Ustoz so'roviga asosan berilgan real ko'rsatkichlarni chuqur pedagogik tahlil qilib, chiroyli sarlavhalar, xulosalar va o'qituvchi uchun aniq amaliy tavsiyalar bilan o'zbek tilida taqdim eting."""

            user_prompt = f"""Ustozning savoli: "{user_message}"

Tizimdagi joriy ko'rsatkichlar:
{stats_context}

Iltimos, ushbu ma'lumotlar asosida professional, chiroyli formatlangan to'liq hisobot va tahliliy javob bering."""

            try:
                ai_reply = await call_openrouter_api(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model=OPENROUTER_MODEL,
                    temperature=0.3,
                    max_tokens=2500
                )
                if ai_reply:
                    return {"result": ai_reply, "reply": ai_reply}
            except Exception as ex:
                print("OpenRouter stats error:", ex)

            # Fallback stats report if network fails
            fallback_stats = f"""## 📊 Maktab Ta'lim Platformasi Statistikasi

- **O'quvchilar soni:** Jami {len(all_students)} nafar (Faol tasdiqlangan: {len(approved_students)}, Kutilayotgan: {len(pending_students)})
- **Mavjud guruhlar:** {len(groups)} ta
- **O'rtacha o'zlashtirish:** {avg_score}% ({total_tests_taken} ta test topshirilgan)
- **Topshirilgan uyga vazifalar:** {total_hw_subs} ta
- **Darslik va resurslar fondi:** {resources_count} ta kitob
- **Test Markazidagi mavzular:** {len(teacher_tests)} ta

💡 **Tavsiya:** O'quvchilarning umumiy o'zlashtirish ko'rsatkichini oshirish uchun Test Markazida yangi interaktiv testlar tuzish va darsliklar bo'yicha mashg'ulotlarni ko'paytirish tavsiya etiladi."""
            return {"result": fallback_stats, "reply": fallback_stats}

        # -------------------------------------------------------------
        # 1.5. TEXTBOOK STUDY & CURRICULUM ANALYSIS INTENT
        # -------------------------------------------------------------
        if is_study_intent and matched_resource:
            res_author = matched_resource.author or "Noma'lum"
            res_desc = matched_resource.description or "Umumta'lim maktabi darsligi"
            system_prompt = f"""Siz O'zbekiston milliy maktab darsliklari eksperti, oliy toifali biologiya/kimyo metodisti va professional AI Agentsiz.
Siz o'qituvchi tanlagan darslikni chuqur tahlil qilib, uning tuzilishi, boblari, asosiy ilmiy tushunchalari va uni darsda qanday samarali qo'llash mumkinligini tahlil qilasiz.

Tahlil strukturasi:
1. 📘 **Darslik pasporti va maqsadi:** (Nomi, muallifi, sinfi, fan dasturiga muvofiqligi)
2. 🔬 **Qamrab olingan asosiy boblar va ilmiy tushunchalar:** (Darslikdagi tayanch biologik qonuniyatlar, mavzular)
3. 🎯 **O'quvchilar yoshiga mosligi va ta'limiy ahamiyati:** (O'quvchilarda qaysi ko'nikmalar shakllanadi)
4. 💡 **O'qituvchi uchun metodik tavsiyalar:** (Darsni interaktiv o'tish, laboratoriya va ko'rgazmali vositalar)
5. ⚡ **Keyingi qadam:** (Ustozga ushbu darslik bo'yicha darhol Test Markaziga avtomatik 3 bosqichli test tuzib berishga tayyor ekanligingizni bildiring)"""

            study_prompt = f"""Ustoz so'rovi: "{user_message}"

O'rganilishi kerak bo'lgan darslik ma'lumotlari:
- Kitob nomi: {matched_resource.title}
- Fan: {matched_resource.subject}
- Sinf: {matched_resource.classGrade}
- Kategoriya: {matched_resource.category}
- Muallif: {res_author}
- Nashr yili: {matched_resource.year}
- Tavsif: {res_desc}

Iltimos, ushbu darslikni to'liq pedagogik tahlil qilib, o'qituvchiga darsda qo'llash uchun mukammal va boy tahliliy xulosa bering."""

            try:
                ai_reply = await call_openrouter_api(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": study_prompt}
                    ],
                    model=OPENROUTER_MODEL,
                    temperature=0.3,
                    max_tokens=2500
                )
                if ai_reply:
                    return {
                        "result": ai_reply,
                        "reply": ai_reply,
                        "attachedResource": matched_resource.to_dict()
                    }
            except Exception as study_err:
                print("Study textbook error:", study_err)

        # -------------------------------------------------------------
        # 2. AUTONOMOUS TEST GENERATION & TEST MARKAZ INTEGRATION
        # -------------------------------------------------------------
        if is_test_intent:
            detected_subject = "Biologiya"
            detected_grade = "8-sinf"
            topic_hint = user_message
            book_info = ""

            if matched_resource:
                detected_subject = matched_resource.subject or "Biologiya"
                detected_grade = matched_resource.classGrade or "8-sinf"
                topic_hint = matched_resource.title
                res_author = matched_resource.author or "Noma'lum"
                res_desc = matched_resource.description or ""
                book_info = f"""
BELGILANGAN RESURS / DARSLIK:
- Kitob nomi: {matched_resource.title}
- Fan: {matched_resource.subject}
- Sinf: {matched_resource.classGrade}
- Muallif: {res_author}
- Tavsif: {res_desc}
"""
            else:
                # Guess grade and subject from text if possible
                grade_match = re.search(r'(\d+)\s*-\s*sinf', user_lower)
                if grade_match:
                    detected_grade = f"{grade_match.group(1)}-sinf"
                if "kimyo" in user_lower:
                    detected_subject = "Kimyo"

            system_prompt = f"""Siz O'zbekiston umumta'lim maktablari uchun tajribali biologiya va kimyo fani metodistisiz.
Siz o'qituvchi talabiga ko'ra darsliklar va mavzular bo'yicha mukammal, DTM standartlariga mos test savollari tuzuvchi AI Agentsiz.
Siz faqat ta'lim, dars va pedagogika bo'yicha ishlaysiz.

Siz tuzgan test Test Markaziga avtomatik kiritiladi. Shuning uchun javobingizni FAQAT va FAQAT quyidagi to'g'ri JSON formatda qaytaring (hech qanday qo'shimcha so'zsiz):
{{
  "topic": "Mavzu nomi",
  "subject": "{detected_subject}",
  "classGrade": "{detected_grade}",
  "description": "Mavzu bo'yicha 3 bosqichli bilim sinovi",
  "levels": [
    {{
      "difficulty": "Oson",
      "title": "1-bosqich: Boshlang'ich tushunchalar",
      "questions": [
        {{
          "id": 1,
          "question": "Savol matni?",
          "options": ["To'g'ri variant", "Noto'g'ri variant 1", "Noto'g'ri variant 2", "Noto'g'ri variant 3"],
          "answerIndex": 0,
          "explanation": "Qisqa ilmiy tushuntirish"
        }},
        {{
          "id": 2,
          "question": "2-savol matni?",
          "options": ["A", "B", "C", "D"],
          "answerIndex": 1,
          "explanation": "..."
        }}
      ]
    }},
    {{
      "difficulty": "O'rtacha",
      "title": "2-bosqich: Tushunish va tahlil",
      "questions": [
        {{
          "id": 3,
          "question": "3-savol matni?",
          "options": ["A", "B", "C", "D"],
          "answerIndex": 2,
          "explanation": "..."
        }},
        {{
          "id": 4,
          "question": "4-savol matni?",
          "options": ["A", "B", "C", "D"],
          "answerIndex": 0,
          "explanation": "..."
        }}
      ]
    }},
    {{
      "difficulty": "Qiyin",
      "title": "3-bosqich: DTM va olimpiada darajasi",
      "questions": [
        {{
          "id": 5,
          "question": "5-savol matni?",
          "options": ["A", "B", "C", "D"],
          "answerIndex": 3,
          "explanation": "..."
        }},
        {{
          "id": 6,
          "question": "6-savol matni?",
          "options": ["A", "B", "C", "D"],
          "answerIndex": 1,
          "explanation": "..."
        }}
      ]
    }}
  ]
}}"""

            test_prompt = f"""Ustoz so'rovi: "{user_message}"
{book_info}
Asosiy mavzu / manba: {topic_hint}

Iltimos, ushbu manba bo'yicha 3 bosqichli (Oson, O'rtacha, Qiyin) jami kamida 6-9 ta sifatli va ilmiy to'g'ri test savolini yuqoridagi JSON formatda shakllantiring."""

            try:
                ai_response = await call_openrouter_api(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": test_prompt}
                    ],
                    model=OPENROUTER_MODEL,
                    temperature=0.2,
                    max_tokens=3500
                )

                test_json = None
                cleaned_json = ai_response.strip()
                if "```json" in cleaned_json:
                    cleaned_json = cleaned_json.split("```json")[1].split("```")[0].strip()
                elif "```" in cleaned_json:
                    cleaned_json = cleaned_json.split("```")[1].split("```")[0].strip()
                elif "{" in cleaned_json and "}" in cleaned_json:
                    start_idx = cleaned_json.find("{")
                    end_idx = cleaned_json.rfind("}")
                    cleaned_json = cleaned_json[start_idx:end_idx+1]

                test_json = json.loads(cleaned_json)

                if test_json and isinstance(test_json, dict):
                    levels = test_json.get("levels", [])
                    if not levels and test_json.get("questions"):
                        raw_qs = test_json.get("questions", [])
                        n = len(raw_qs)
                        part = max(n // 3, 1)
                        levels = [
                            {"difficulty": "Oson", "title": "1-bosqich: Boshlang'ich tushunchalar", "questions": raw_qs[:part]},
                            {"difficulty": "O'rtacha", "title": "2-bosqich: Tushunish va tahlil", "questions": raw_qs[part:part*2]},
                            {"difficulty": "Qiyin", "title": "3-bosqich: DTM va olimpiada darajasi", "questions": raw_qs[part*2:]}
                        ]

                    if levels:
                        now = int(time.time() * 1000)
                        test_id = f"test-ai-{now}"
                        topic_title = test_json.get("topic") or topic_hint or "Biologiya testi"
                        test_grade = test_json.get("classGrade") or detected_grade or "8-sinf"
                        test_subject = test_json.get("subject") or detected_subject or "Biologiya"
                        test_desc = test_json.get("description") or f"{topic_title} mavzusida AI Agent tomonidan tuzilgan 3 bosqichli test"

                        total_q = sum(len(lvl.get("questions", [])) for lvl in levels)

                        new_teacher_test = TeacherTestModel(
                            id=test_id,
                            subject=test_subject,
                            topic=topic_title,
                            classGrade=test_grade,
                            description=test_desc,
                            teacherName="AI Metodist Agent",
                            createdAt=now,
                            levels=levels
                        )
                        db.add(new_teacher_test)
                        db.commit()
                        db.refresh(new_teacher_test)

                        summary_lines = [
                            f"🎉 **Test muvaffaqiyatli tuzildi va Test Markaziga qo'shildi!**",
                            f"",
                            f"📌 **Mavzu:** {topic_title}",
                            f"📚 **Fan va Sinf:** {test_subject} • {test_grade}",
                            f"📊 **Savollar soni:** {total_q} ta (3 ta bosqich: Oson, O'rtacha, Qiyin)",
                            f"",
                            f"Ushbu test avtomatik tarzda **[Test Markazi](/teacher/test.html)** bo'limiga kiritildi va o'quvchilar uchun faol holatga keltirildi.",
                            f"",
                            f"### 📋 Shakllantirilgan test savollari:"
                        ]
                        for lvl in levels:
                            summary_lines.append(f"\n**{lvl.get('difficulty', 'Bosqich')} — {lvl.get('title', '')}:**")
                            for q in lvl.get("questions", []):
                                summary_lines.append(f"- ❓ **{q.get('question')}**")
                                for idx, opt in enumerate(q.get("options", [])):
                                    mark = "✅ " if idx == q.get("answerIndex") else "   "
                                    letter = chr(65 + idx)
                                    summary_lines.append(f"   {mark}{letter}) {opt}")
                                if q.get("explanation"):
                                    summary_lines.append(f"   *Izoh:* {q.get('explanation')}")

                        full_reply = "\n".join(summary_lines)
                        return {
                            "result": full_reply,
                            "reply": full_reply,
                            "createdTest": new_teacher_test.to_dict(),
                            "attachedResource": matched_resource.to_dict() if matched_resource else None
                        }

                return {"result": ai_response, "reply": ai_response}
            except Exception as test_err:
                print("Test creation error:", test_err)

        # -------------------------------------------------------------
        # 3. GENERAL PEDAGOGICAL & EDUCATIONAL CHAT INTENT
        # -------------------------------------------------------------
        system_prompt = """Siz O'zbekiston umumta'lim maktablari uchun tajribali biologiya va kimyo fani metodisti, katta pedagog-maslahatchi va shaxsiy AI Agentsiz.
SIZNING ASOSIY VA QAT'IY QOIDALARINGIZ:
1. Siz FAQAT VA FAQAT maktab darslari, biologiya va kimyo fanlari, pedagogik metodika, dars ishlanmalari, yangi o'quv metodlari, laboratoriya ishlari, o'quvchilar bilimi va ta'lim jarayoniga oid savollarga javob berasiz.
2. Darsga yoki ta'limga mutlaqo aloqasi bo'lmagan mavzular (siyosat, shou-biznes, bekorchi g'iybat, o'yin-kulgi va boshqalar) so'ralsa, xushmuomalalik bilan: "Hurmatli ustoz! Men faqat dars, biologiya, kimyo va ta'lim metodikasi bo'yicha maslahat bera olaman. Darsingiz yoki o'quvchilaringiz bo'yicha qanday pedagogik yordam kerak?" deb javob bering.
3. O'qituvchiga samimiy, ilmiy jihatdan aniq, amaliy va darsda qo'llashga qulay tavsiyalar bering."""

        try:
            ai_reply = await call_openrouter_api(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                model=OPENROUTER_MODEL,
                temperature=0.3,
                max_tokens=2500
            )
            if ai_reply:
                return {"result": ai_reply, "reply": ai_reply}
        except Exception as chat_err:
            print("Chat error with OpenRouter:", chat_err)
            if API_KEY:
                try:
                    gemini_reply = await call_gemini_api(
                        prompt_or_contents=user_message,
                        system_instruction=system_prompt
                    )
                    if gemini_reply:
                        return {"result": gemini_reply, "reply": gemini_reply}
                except Exception as g_err:
                    print("Gemini fallback error:", g_err)

        # Graceful fallback response
        return {
            "result": f"Hurmatli ustoz! \"{user_message}\" bo'yicha tavsiya: Dars samaradorligini oshirish uchun o'quvchilar bilan mavzuni vizual rasmlar, interaktiv savol-javoblar va Test Markazidagi testlar orqali mustahkamlash tavsiya etiladi.",
            "reply": f"Hurmatli ustoz! \"{user_message}\" bo'yicha tavsiya: Dars samaradorligini oshirish uchun o'quvchilar bilan mavzuni vizual rasmlar, interaktiv savol-javoblar va Test Markazidagi testlar orqali mustahkamlash tavsiya etiladi."
        }
    finally:
        db.close()

# -------------------------------------------------------------
# RESOURCE LIBRARY (Darsliklar va Resurslar) APIs
# -------------------------------------------------------------
@app.get("/api/resources")
async def get_resources(
    subject: Optional[str] = None,
    classGrade: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None
):
    db = SessionLocal()
    try:
        query = db.query(ResourceModel)

        if subject and subject.lower() not in ["all", "barchasi"]:
            query = query.filter(ResourceModel.subject.ilike(f"%{subject.strip()}%"))

        if classGrade and classGrade.lower() not in ["all", "barchasi"]:
            query = query.filter(ResourceModel.classGrade.ilike(f"%{classGrade.strip()}%"))

        if category and category.lower() not in ["all", "barchasi"]:
            query = query.filter(ResourceModel.category.ilike(f"%{category.strip()}%"))

        if search and search.strip():
            s = f"%{search.strip()}%"
            query = query.filter(
                (ResourceModel.title.ilike(s)) |
                (ResourceModel.author.ilike(s)) |
                (ResourceModel.description.ilike(s))
            )

        resources = query.order_by(ResourceModel.createdAt.desc()).all()
        return [r.to_dict() for r in resources]
    finally:
        db.close()

@app.get("/api/resources/{resource_id}")
async def get_resource_by_id(resource_id: str):
    db = SessionLocal()
    try:
        res = db.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
        if not res:
            raise HTTPException(status_code=404, detail="Resurs topilmadi")
        return res.to_dict()
    finally:
        db.close()

@app.post("/api/resources")
async def create_resource(request: Request):
    user_role = request.headers.get("X-User-Role")
    user_id = request.headers.get("X-User-Id")
    
    db = SessionLocal()
    try:
        if user_id and user_id != "undefined":
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if user and user.role != "teacher":
                raise HTTPException(status_code=403, detail="Faqat o'qituvchilar yangi resurs qo'sha oladi.")
        elif user_role and user_role != "teacher":
            raise HTTPException(status_code=403, detail="Faqat o'qituvchilar yangi resurs qo'sha oladi.")

        content_type = request.headers.get("content-type", "")
        if "multipart/form-data" in content_type:
            form = await request.form()
            title = (form.get("title") or "").strip()
            subject = form.get("subject") or "Biologiya"
            classGrade = form.get("classGrade") or "Barchasi"
            category = form.get("category") or "Darslik"
            author = form.get("author") or ""
            year = form.get("year") or str(time.strftime("%Y"))
            description = form.get("description") or ""
            coverColor = form.get("coverColor") or "emerald"
            file_url = (form.get("fileUrl") or "").strip()
            file_name = form.get("fileName") or "darslik.pdf"
            file_size = form.get("fileSize") or "10 MB"

            # Check if file was uploaded directly in this request
            uploaded_file = form.get("file")
            if uploaded_file and hasattr(uploaded_file, "filename") and uploaded_file.filename:
                UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
                now = int(time.time() * 1000)
                clean_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', uploaded_file.filename).strip('_') or "darslik.pdf"
                saved_filename = f"{now}_{clean_name}"
                file_path = UPLOAD_DIR / saved_filename

                total_size = 0
                with open(file_path, "wb") as f:
                    while chunk := await uploaded_file.read(1024 * 1024):
                        f.write(chunk)
                        total_size += len(chunk)

                file_url = f"/uploads/{saved_filename}"
                file_name = uploaded_file.filename
                file_size = f"{(total_size / (1024 * 1024)):.1f} MB" if total_size >= 1024 * 1024 else f"{(total_size / 1024):.0f} KB"
        else:
            data = await request.json()
            title = (data.get("title") or "").strip()
            subject = data.get("subject", "Biologiya")
            classGrade = data.get("classGrade", "Barchasi")
            category = data.get("category", "Darslik")
            author = data.get("author", "")
            year = data.get("year", str(time.strftime("%Y")))
            description = data.get("description", "")
            coverColor = data.get("coverColor", "emerald")
            file_url = (data.get("fileUrl") or "").strip()
            file_name = data.get("fileName") or "darslik.pdf"
            file_size = data.get("fileSize") or "10 MB"

        if not title:
            raise HTTPException(status_code=400, detail="Resurs nomi kiritilishi shart.")

        if not file_url:
            raise HTTPException(status_code=400, detail="PDF fayl yuklanishi yoki fayl manzili (URL) ko'rsatilishi shart.")

        new_id = f"res-{uuid.uuid4().hex[:10]}"
        resource = ResourceModel(
            id=new_id,
            title=title,
            subject=subject,
            classGrade=classGrade,
            category=category,
            author=author,
            year=year,
            description=description,
            fileUrl=file_url,
            fileName=file_name,
            fileSize=file_size,
            coverColor=coverColor,
            downloads=0,
            createdAt=int(time.time() * 1000)
        )
        db.add(resource)
        db.commit()
        db.refresh(resource)
        return resource.to_dict()
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Resursni saqlashda xatolik: {str(e)}")
    finally:
        db.close()

@app.delete("/api/resources/{resource_id}")
async def delete_resource(resource_id: str, request: Request):
    user_role = request.headers.get("X-User-Role")
    user_id = request.headers.get("X-User-Id")

    db = SessionLocal()
    try:
        if user_id and user_id != "undefined":
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if user and user.role != "teacher":
                raise HTTPException(status_code=403, detail="Faqat o'qituvchilar resurslarni o'chira oladi.")
        elif user_role and user_role != "teacher":
            raise HTTPException(status_code=403, detail="Faqat o'qituvchilar resurslarni o'chira oladi.")

        res = db.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
        if not res:
            raise HTTPException(status_code=404, detail="Resurs topilmadi")

        # Safely delete uploaded file if not standard seeded book
        try:
            if res.fileUrl and res.fileUrl.startswith("/uploads/") and not res.fileUrl.startswith("/uploads/resources/"):
                local_file = BASE_DIR / res.fileUrl.lstrip("/")
                if local_file.is_file():
                    local_file.unlink()
        except Exception:
            pass

        db.delete(res)
        db.commit()
        return {"success": True, "message": "Resurs muvaffaqiyatli o'chirildi"}
    finally:
        db.close()

@app.get("/api/resources/{resource_id}/download-file")
async def download_resource_file(resource_id: str):
    """Forced direct attachment file download with automatic counter increment."""
    db = SessionLocal()
    try:
        res = db.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
        if not res:
            raise HTTPException(status_code=404, detail="Resurs topilmadi")

        res.downloads = (res.downloads or 0) + 1
        db.commit()

        file_url = res.fileUrl or ""
        clean_url = file_url.lstrip("/")
        candidate_paths = [
            BASE_DIR / clean_url,
            UPLOAD_DIR / clean_url.replace("uploads/", ""),
            BASE_DIR / "uploads" / "resources" / (res.fileName or "")
        ]

        found_path = None
        for p in candidate_paths:
            if p.is_file():
                found_path = p
                break

        if found_path:
            return FileResponse(
                path=str(found_path),
                filename=res.fileName or found_path.name,
                media_type="application/pdf"
            )

        if file_url.startswith("http://") or file_url.startswith("https://"):
            from fastapi.responses import RedirectResponse
            return RedirectResponse(url=file_url)

        raise HTTPException(status_code=404, detail="Fayl serverda topilmadi")
    finally:
        db.close()

@app.post("/api/resources/{resource_id}/download")
async def register_resource_download(resource_id: str):
    db = SessionLocal()
    try:
        res = db.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
        if not res:
            raise HTTPException(status_code=404, detail="Resurs topilmadi")

        res.downloads = (res.downloads or 0) + 1
        db.commit()
        return {"success": True, "downloads": res.downloads}
    finally:
        db.close()

# -------------------------------------------------------------
# STATS SUMMARY API (PostgreSQL)
@app.get("/api/admin/clean-demo")
@app.post("/api/admin/clean-demo")
async def clean_demo_endpoint():
    db = SessionLocal()
    try:
        clean_demo_records(db)
        return {"success": True, "message": "Demo ma'lumotlar tozalandi"}
    finally:
        db.close()
# -------------------------------------------------------------
@app.get("/api/stats/summary")
async def get_stats_summary():
    db = SessionLocal()
    try:
        total_students = db.query(UserModel).filter(UserModel.role == "student").count()
        total_groups = db.query(GroupModel).count()
        total_subs = db.query(SubmissionModel).count()
        total_hw = db.query(HomeworkModel).count()
        subs = db.query(SubmissionModel).all()
        avg_score = round(sum(s.percentage or 0 for s in subs) / max(len(subs), 1)) if subs else 0
        top_count = len([s for s in subs if (s.percentage or 0) >= 85])

        return {
            "totalStudents": total_students,
            "totalGroups": total_groups,
            "totalSubmissions": total_subs,
            "totalHomework": total_hw,
            "averageScore": avg_score,
            "topStudentsCount": top_count
        }
    finally:
        db.close()

# -------------------------------------------------------------
# Static Files & Frontend HTML SPA Serving
# -------------------------------------------------------------
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/{full_path:path}")
async def serve_spa(full_path: str, request: Request):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API yo'nalishi topilmadi")

    # Block students from accessing teacher pages or AI assistant directly
    user_role = request.headers.get("X-User-Role")
    if user_role == "student" and ("teacher" in full_path or "ai-assistant" in full_path):
        raise HTTPException(status_code=403, detail="Talabalar uchun o'qituvchi va AI sahifalariga kirish taqiqlangan.")

    no_cache_headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0"
    }

    requested_file = FRONTEND_DIR / full_path
    if full_path and requested_file.is_file():
        return FileResponse(str(requested_file), headers=no_cache_headers)

    # Clean URLs support like /student/chat, /teacher/stats, /login
    if full_path:
        html_candidate = FRONTEND_DIR / f"{full_path}.html"
        if html_candidate.is_file():
            return FileResponse(str(html_candidate), headers=no_cache_headers)
        dir_index = FRONTEND_DIR / full_path / "index.html"
        if dir_index.is_file():
            return FileResponse(str(dir_index), headers=no_cache_headers)

    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file), headers=no_cache_headers)

    return JSONResponse(
        status_code=200,
        content={"message": "BioEdu FastAPI server ishlamoqda."}
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "3000"))
    print(f"BioEdu FastAPI Server ishga tushirilmoqda: http://127.0.0.1:{port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
