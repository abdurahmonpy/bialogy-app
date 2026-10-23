import os
import json
import time
import random
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
import copy
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Response, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm.attributes import flag_modified

from database import clean_demo_records
from database import (
    init_db, SessionLocal,
    UserModel, GroupModel, HomeworkModel,
    ChatMessageModel, SubmissionModel, TeacherTestModel
)

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

API_KEY = os.getenv("GEMINI_API_KEY", "")
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

app = FastAPI(title="BioEdu — Biologiya Ta'lim Platformasi API")

# Enable CORS for split deployment (Railway Backend + Vercel Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Fayl tanlanmadi")

    now = int(time.time() * 1000)
    clean_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', file.filename)
    saved_filename = f"{now}_{clean_name}"
    file_path = UPLOAD_DIR / saved_filename

    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Faylni saqlashda xatolik: {e}")

    return {
        "success": True,
        "url": f"/uploads/{saved_filename}",
        "fileUrl": f"/uploads/{saved_filename}",
        "filename": file.filename,
        "fileName": file.filename,
        "size": len(content)
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
            avatar=full_name[0].upper() if full_name else "O",
            createdAt=now
        )
        db.add(new_user)
        db.commit()
        return {"success": True, "user": new_user.to_dict()}
    finally:
        db.close()

@app.get("/api/auth/me")
async def auth_me(userId: Optional[str] = None):
    db = SessionLocal()
    try:
        if userId:
            u = db.query(UserModel).filter(UserModel.id == userId).first()
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
            if ch == "ai":
                msg_list = [{
                    "id": "starter-ai",
                    "channel": "ai",
                    "channelId": "ai",
                    "senderId": "ai-tutor",
                    "senderName": "AI Repititor",
                    "senderRole": "ai",
                    "text": "Assalomu alaykum! Men biologiya fanidan sun'iy intellekt repetitoringizman. Hujayra, DNK, fotosintez, odam anatomiyasi yoki istalgan mavzuda savollaringizni bering!",
                    "time": "Hozir",
                    "timeStr": "Hozir"
                }]
            elif ch == "group":
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

    now = int(time.time() * 1000)
    time_str = time.strftime("%H:%M")
    ch = body.get("channel") or body.get("channelId") or "teacher"

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

        if ch == "ai":
            ai_answer = await generate_biotutor_answer(text)
            ai_msg = ChatMessageModel(
                id=f"msg-{now+1}-{random.randint(100, 999)}",
                channel="ai",
                channelId="ai",
                senderId="ai-tutor",
                senderName="AI Repititor",
                senderRole="ai",
                text=ai_answer,
                timestamp=now + 1,
                time=time_str,
                timeStr=time_str
            )
            db.add(ai_msg)

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
# TEACHER TESTS APIS (PostgreSQL)
# -------------------------------------------------------------
@app.get("/api/teacher-tests")
async def get_teacher_tests():
    db = SessionLocal()
    try:
        tests = db.query(TeacherTestModel).order_by(TeacherTestModel.createdAt.desc()).all()
        return [t.to_dict() for t in tests]
    finally:
        db.close()

@app.post("/api/teacher-tests")
async def save_teacher_test(request: Request):
    body = await request.json()
    topic = body.get("topic")
    levels = body.get("levels")

    if not topic or not levels:
        raise HTTPException(status_code=400, detail="Mavzu va bosqichlar to'liq kiritilishi shart")

    db = SessionLocal()
    try:
        now = int(time.time() * 1000)
        test_id = body.get("id") or f"topic-{now}"
        existing = db.query(TeacherTestModel).filter(TeacherTestModel.id == test_id).first()
        if existing:
            existing.topic = topic
            existing.levels = levels
            existing.classGrade = body.get("classGrade") or existing.classGrade
            existing.description = body.get("description") or existing.description
            db.commit()
            return {"success": True, "test": existing.to_dict()}

        new_test = TeacherTestModel(
            id=test_id,
            subject=body.get("subject", "Biologiya"),
            topic=topic,
            classGrade=body.get("classGrade", "8-sinf"),
            description=body.get("description", "3-bosqichli bilim sinovi"),
            teacherName=body.get("teacherName", "Aziza Rahimova"),
            createdAt=now,
            levels=levels
        )
        db.add(new_test)
        db.commit()
        return {"success": True, "test": new_test.to_dict()}
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
# TEACHER AI ASSISTANT API
# -------------------------------------------------------------
@app.post("/api/teacher/ai-assistant")
async def teacher_ai_assistant(request: Request):
    body = await request.json()
    task_type = body.get("type", "lesson_plan")
    topic = body.get("topic") or "Fotosintez va Hujayra almashinuvi"
    subject = body.get("subject") or "Biologiya"
    grade = body.get("grade") or "8-sinf"

    if API_KEY:
        prompt = f"""Siz tajribali O'zbekiston milliy maktabi pedagogi, biologiya metodistisiz.
Fan: {subject}
Mavzu: {topic}
Sinf: {grade}
Vazifa turi: {task_type}

Iltimos, o'qituvchi darsda bevosita qo'llashi mumkin bo'lgan professional, pedagogik mukammal dars materialini o'zbek tilida tayyorlang."""
        try:
            reply = await call_gemini_api(prompt)
            if reply:
                return {"result": reply}
        except Exception as e:
            print(f"Teacher AI error: {e}")

    if task_type == "lesson_plan":
        return {
            "result": f"""## 📖 {grade} {subject} Fani: "{topic}" Mavzusidagi Namunaviy Dars Ishlanmasi

**Darsning maqsadi:**
- **Ta'limiy:** O'quvchilarga "{topic}" mavzusining ilmiy mohiyati, biologik mexanizmlari va ahamiyatini to'liq tushuntirish.
- **Rivojlantiruvchi:** O'quvchilarda biologik tafakkur, solishtirma tahlil va hodisalar o'rtasidagi sabab-oqibatni aniqlash ko'nikmasini rivojlantirish.
- **Tarbiyaviy:** Tabiatni asrash, sog'lom turmush tarziga rioya qilish va fanga qiziqishni oshirish.

**Dars turi:** Yangi bilimlarni egallash va mustahkamlash darsi.
**Kerakli jihozlar:** Darslik, mavzuga oid plakatlar, mikroskop preparatlari, slaydlar va interaktiv test kartochkalari.

---

### ⏱️ Darsning 45 daqiqalik xronometraji:
1. **Tashkiliy qism (3 daqiqa):** Salomlashish, davomatni aniqlash, o'quvchilar tayyorgarligini tekshirish.
2. **O'tgan mavzuni takrorlash (7 daqiqa):** Tezkor savol-javob orqali 3 ta tayanch savolni muhokama qilish.
3. **Yangi mavzu bayoni (20 daqiqa):** Asosiy tushunchalar va darslik qoidalarini doskada tizimli yoritish.
4. **Mavzuni mustahkamlash (10 daqiqa):** O'quvchilar bilan birgalikda muammoli test savollarini tahlil qilish.
5. **Darsni yakunlash va baholash (3 daqiqa):** Faol o'quvchilarni rag'batlantirish va baholash.
6. **Uyga vazifa (2 daqiqa):** Mavzuni o'qib savollarga yozma javob tayyorlash."""
        }
    elif task_type == "experiment":
        return {
            "result": f"""## 🔬 {grade} {subject}: "{topic}" Mavzusidagi Amaliy Laboratoriya Mashg'uloti

**Ishning maqsadi:** "{topic}" jarayonining biologik mohiyatini bevosita kuzatish va amaliy tadqiqot orqali isbotlash.

**Kerakli laboratoriya jihozlari:**
1. Maktab mikroskopi yoki lupa;
2. Buyum va qoplagich oynachalari;
3. Pipetka, pinset va skalpel;
4. Distillangan suv va indikator eritmasi;
5. O'rganilayotgan biologik namuna.

---

### 📋 Tajribaning bosqichma-bosqich bajarilishi:
1. **Preparat tayyorlash:** Toza buyum oynachasiga suv tomizing, namunadan yupqa qatlam joylashtiring va qoplagich oynacha bilan yoping.
2. **Mikroskopda kuzatish:** Avval 10x, so'ngra 40x kattalashtirishda fokuslab ob'ektni o'rganing.
3. **Kuzatuv natijalarini qayd etish:** Ko'ringan tuzilmalarni daftaringizga qalam bilan chizing.
4. **Xulosa:** Organoidlarning tuzilishi va ularning vazifasi o'rtasidagi bog'liqlik haqida ilmiy xulosa yozing."""
        }
    else:
        return {
            "result": f"""## 🎯 {grade} {subject}: "{topic}" Bo'yicha DTM va Olimpiada Darajasidagi Murakkab Savollar

### 1-Savol (Mantiqiy tahlil):
Quyida berilgan biologik qonuniyatlar orasidan "{topic}" jarayoniga to'g'ridan-to'g'ri taalluqli bo'lmagan qatorni aniqlang:
A) ATF energiyasining sintezlanishi va sarflanishi
B) Membrana orqali moddalarning faol va passiv transporti
C) Lizosomaning barcha eukariot hujayralarda yagona energiya hosil qiluvchi organoid hisoblanishi
D) Fermentlarning o'ziga xos substrat bilan ta'sirlashishi

*To'g'ri javob:* **C**
*Tahlil:* Lizosoma energiya hosil qilmaydi, balki hujayra ichki hazmini amalga oshiradi. Energiya mitoxondriyada hosil bo'ladi.

---

### 2-Savol (Miqdoriy hisoblash):
Agar hujayrada 12 molekula glyukoza to'liq kislorodli parchalansa, jami necha molekula ATF sintezlanadi?
A) 36 ta  |  B) 72 ta  |  C) 432 ta  |  D) 456 ta

*To'g'ri javob:* **D** (38 × 12 = 456 ta ATF).
*Yechimi:* 1 molekula glyukoza to'liq parchalanganda 38 ta ATF hosil bo'ladi. 12 × 38 = 456."""
        }

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
async def serve_spa(full_path: str):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API yo'nalishi topilmadi")

    requested_file = FRONTEND_DIR / full_path
    if full_path and requested_file.is_file():
        return FileResponse(str(requested_file))

    # Clean URLs support like /student/chat, /teacher/stats, /login
    if full_path:
        html_candidate = FRONTEND_DIR / f"{full_path}.html"
        if html_candidate.is_file():
            return FileResponse(str(html_candidate))
        dir_index = FRONTEND_DIR / full_path / "index.html"
        if dir_index.is_file():
            return FileResponse(str(dir_index))

    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))

    return JSONResponse(
        status_code=200,
        content={"message": "BioEdu FastAPI server ishlamoqda."}
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "3000"))
    print(f"BioEdu FastAPI Server ishga tushirilmoqda: http://127.0.0.1:{port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
