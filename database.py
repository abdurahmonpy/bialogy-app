import os
import time
from typing import Any, Dict, List, Optional
from sqlalchemy import create_engine, Column, String, Integer, BigInteger, Text, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

# Read DATABASE_URL. In Railway, PostgreSQL connection URL is passed via DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./biology.db")

# SQLAlchemy 1.4+ requires postgresql:// instead of postgres:// (Railway format)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

is_sqlite = DATABASE_URL.startswith("sqlite")

connect_args = {"check_same_thread": False} if is_sqlite else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# -------------------------------------------------------------
# Database Models
# -------------------------------------------------------------
class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    role = Column(String, index=True) # "student" or "teacher"
    login = Column(String, unique=True, index=True)
    password = Column(String)
    fullName = Column(String)
    classGrade = Column(String, nullable=True)
    groupId = Column(String, nullable=True)
    subject = Column(String, nullable=True)
    school = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    streakDays = Column(Integer, default=1)
    avatar = Column(String, nullable=True)
    createdAt = Column(BigInteger, default=lambda: int(time.time() * 1000))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "login": self.login,
            "password": self.password,
            "fullName": self.fullName,
            "classGrade": self.classGrade,
            "groupId": self.groupId,
            "subject": self.subject,
            "school": self.school,
            "phone": self.phone,
            "streakDays": self.streakDays,
            "avatar": self.avatar,
            "createdAt": self.createdAt
        }

class GroupModel(Base):
    __tablename__ = "groups"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    grade = Column(String, nullable=True)
    subject = Column(String, nullable=True)
    schedule = Column(String, nullable=True)
    studentCount = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    createdAt = Column(BigInteger, default=lambda: int(time.time() * 1000))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "grade": self.grade,
            "subject": self.subject,
            "schedule": self.schedule,
            "studentCount": self.studentCount,
            "description": self.description,
            "createdAt": self.createdAt
        }

class HomeworkModel(Base):
    __tablename__ = "homework"

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    subject = Column(String, nullable=True)
    groupId = Column(String, nullable=True)
    groupName = Column(String, nullable=True)
    deadline = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    teacherName = Column(String, nullable=True)
    createdAt = Column(BigInteger, default=lambda: int(time.time() * 1000))
    submissions = Column(JSON, default=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "subject": self.subject,
            "groupId": self.groupId,
            "groupName": self.groupName,
            "deadline": self.deadline,
            "description": self.description,
            "teacherName": self.teacherName,
            "createdAt": self.createdAt,
            "submissions": self.submissions or []
        }

class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, index=True)
    channel = Column(String, index=True)
    channelId = Column(String, nullable=True)
    senderId = Column(String)
    senderName = Column(String)
    senderRole = Column(String)
    text = Column(Text)
    timestamp = Column(BigInteger, default=lambda: int(time.time() * 1000))
    time = Column(String, nullable=True)
    timeStr = Column(String, nullable=True)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "channel": self.channel,
            "channelId": self.channelId,
            "senderId": self.senderId,
            "senderName": self.senderName,
            "senderRole": self.senderRole,
            "text": self.text,
            "timestamp": self.timestamp,
            "time": self.time,
            "timeStr": self.timeStr
        }

class SubmissionModel(Base):
    __tablename__ = "submissions"

    id = Column(String, primary_key=True, index=True)
    studentId = Column(String, index=True)
    studentName = Column(String)
    classGrade = Column(String, nullable=True)
    studentClass = Column(String, nullable=True)
    testTopic = Column(String)
    topic = Column(String, nullable=True)
    subject = Column(String, default="Biologiya")
    difficulty = Column(String, default="O'rtacha")
    score = Column(Integer)
    total = Column(Integer)
    totalQuestions = Column(Integer)
    percentage = Column(Integer)
    grade = Column(String, nullable=True)
    gradeBadge = Column(String, nullable=True)
    date = Column(String, nullable=True)
    dateStr = Column(String, nullable=True)
    timestamp = Column(BigInteger, default=lambda: int(time.time() * 1000))
    answers = Column(JSON, default=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "studentId": self.studentId,
            "studentName": self.studentName,
            "classGrade": self.classGrade,
            "studentClass": self.studentClass or self.classGrade,
            "testTopic": self.testTopic,
            "topic": self.topic or self.testTopic,
            "subject": self.subject,
            "difficulty": self.difficulty,
            "score": self.score,
            "total": self.total,
            "totalQuestions": self.totalQuestions,
            "percentage": self.percentage,
            "grade": self.grade,
            "gradeBadge": self.gradeBadge or self.grade,
            "date": self.date,
            "dateStr": self.dateStr or self.date,
            "timestamp": self.timestamp,
            "answers": self.answers or []
        }

class TeacherTestModel(Base):
    __tablename__ = "teacher_tests"

    id = Column(String, primary_key=True, index=True)
    subject = Column(String, default="Biologiya")
    topic = Column(String)
    classGrade = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    teacherName = Column(String, nullable=True)
    createdAt = Column(BigInteger, default=lambda: int(time.time() * 1000))
    levels = Column(JSON, default=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "subject": self.subject,
            "topic": self.topic,
            "classGrade": self.classGrade,
            "description": self.description,
            "teacherName": self.teacherName,
            "createdAt": self.createdAt,
            "levels": self.levels or []
        }

# -------------------------------------------------------------
# Database Init & Seeding
# -------------------------------------------------------------
def init_db():
    Base.metadata.create_all(bind=engine)
    seed_initial_data()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_initial_data():
    db = SessionLocal()
    try:
        # 1. Seed Users if empty
        if db.query(UserModel).count() == 0:
            initial_users = [
                UserModel(
                    id="user-stud-1",
                    role="student",
                    login="student",
                    password="123",
                    fullName="Jasurbek Aliyev",
                    classGrade="8-A sinf",
                    groupId="group-8a",
                    school="14-sonli umumiy o'rta ta'lim maktabi",
                    phone="+998 90 123 45 67",
                    streakDays=5,
                    avatar="J",
                    createdAt=int(time.time() * 1000) - 86400000 * 5
                ),
                UserModel(
                    id="user-stud-2",
                    role="student",
                    login="madina",
                    password="123",
                    fullName="Madina Umarova",
                    classGrade="8-A sinf",
                    groupId="group-8a",
                    school="14-sonli umumiy o'rta ta'lim maktabi",
                    phone="+998 93 987 65 43",
                    streakDays=6,
                    avatar="M",
                    createdAt=int(time.time() * 1000) - 86400000 * 6
                ),
                UserModel(
                    id="user-stud-3",
                    role="student",
                    login="bekzod",
                    password="123",
                    fullName="Bekzod Toshmatov",
                    classGrade="9-B sinf",
                    groupId="group-9b",
                    school="14-sonli umumiy o'rta ta'lim maktabi",
                    phone="+998 97 555 44 33",
                    streakDays=3,
                    avatar="B",
                    createdAt=int(time.time() * 1000) - 86400000 * 3
                ),
                UserModel(
                    id="user-teacher-1",
                    role="teacher",
                    login="teacher",
                    password="123",
                    fullName="Aziza Rahimova",
                    classGrade=None,
                    groupId=None,
                    subject="Biologiya va Tabiiy fanlar",
                    school="14-sonli umumiy o'rta ta'lim maktabi",
                    phone="+998 91 234 56 78",
                    streakDays=14,
                    avatar="A",
                    createdAt=int(time.time() * 1000) - 86400000 * 14
                )
            ]
            db.add_all(initial_users)

        # 2. Seed Groups if empty
        if db.query(GroupModel).count() == 0:
            initial_groups = [
                GroupModel(
                    id="group-8a",
                    name="8-A sinf Biologiya",
                    grade="8-sinf",
                    subject="Biologiya",
                    schedule="Dush-Chor-Juma 09:00",
                    studentCount=24,
                    description="Odam anatomiyasi va fiziologiyasi kursi"
                ),
                GroupModel(
                    id="group-9b",
                    name="9-B sinf Sitologiya",
                    grade="9-sinf",
                    subject="Biologiya",
                    schedule="Sesh-Pay-Shanba 10:30",
                    studentCount=22,
                    description="Sitologiya, genetika va evolutsiya asoslari"
                ),
                GroupModel(
                    id="group-abitur",
                    name="Abituriyent 2026 DTM Guruh",
                    grade="10-11 sinf",
                    subject="Biologiya & Kimyo",
                    schedule="Har kuni 15:00",
                    studentCount=18,
                    description="DTM testlariga tayyorgarlik va chuqurlashtirilgan masalalar"
                )
            ]
            db.add_all(initial_groups)

        # 3. Seed Homework if empty
        if db.query(HomeworkModel).count() == 0:
            initial_hw = [
                HomeworkModel(
                    id="hw-1",
                    title="Hujayra organoidlari: Mitoxondriya va Xloroplast solishtirma jadvali",
                    subject="Biologiya",
                    groupId="group-8a",
                    groupName="8-A sinf Biologiya",
                    deadline="28.10.2026, 18:00",
                    description="Darslikdagi ma'lumotlar asosida mitoxondriya va xloroplast organoidlarining o'xshash va farqli tomonlarini 5 ta bandda yozib topshiring.",
                    teacherName="Aziza Rahimova",
                    submissions=[
                        {
                            "studentId": "user-stud-1",
                            "studentName": "Jasurbek Aliyev",
                            "text": "1. Har ikkisi ham 2 qavat membranali. 2. Har ikkisida o'z halqasimon DNK si va 70S ribosomasi bor. 3. Mitoxondriya ATF sintezlaydi, xloroplast fotosintez qiladi. 4. Xloroplast faqat o'simlikda, mitoxondriya esa barcha eukariotlarda uchraydi.",
                            "content": "1. Har ikkisi ham 2 qavat membranali. 2. Har ikkisida o'z halqasimon DNK si va 70S ribosomasi bor. 3. Mitoxondriya ATF sintezlaydi, xloroplast fotosintez qiladi. 4. Xloroplast faqat o'simlikda, mitoxondriya esa barcha eukariotlarda uchraydi.",
                            "submittedAt": "21.10.2026, 11:30",
                            "grade": "5 (A'lo)",
                            "feedback": "Barakalla, Jasurbek! Solishtirma tahlil juda aniq va xatosiz bajarilgan."
                        }
                    ]
                ),
                HomeworkModel(
                    id="hw-2",
                    title="Yurak qon aylanish doiralari sxemasini tahlil qilish",
                    subject="Biologiya",
                    groupId="group-8a",
                    groupName="8-A sinf Biologiya",
                    deadline="30.10.2026, 20:00",
                    description="Katta va kichik qon aylanish doiralarining boshlanish va tugash kameralarini daftarga yozib tushuntiring.",
                    teacherName="Aziza Rahimova",
                    submissions=[]
                )
            ]
            db.add_all(initial_hw)

        # 4. Seed Chat Messages if empty
        if db.query(ChatMessageModel).count() == 0:
            initial_chat = [
                ChatMessageModel(
                    id="msg-1",
                    channel="teacher",
                    channelId="teacher",
                    senderId="user-teacher-1",
                    senderName="Aziza Rahimova",
                    senderRole="teacher",
                    text="Assalomu alaykum, Jasurbek! Dars mavzusi bo'yicha qanday savollaringiz bor?",
                    time="09:15",
                    timeStr="09:15"
                ),
                ChatMessageModel(
                    id="msg-2",
                    channel="teacher",
                    channelId="teacher",
                    senderId="user-stud-1",
                    senderName="Jasurbek Aliyev",
                    senderRole="student",
                    text="Assalomu alaykum, ustoz! Uyga vazifani topshirdim, tekshirib bera olasizmi?",
                    time="11:32",
                    timeStr="11:32"
                ),
                ChatMessageModel(
                    id="msg-3",
                    channel="group",
                    channelId="group",
                    senderId="user-teacher-1",
                    senderName="Aziza Rahimova",
                    senderRole="teacher",
                    text="Assalomu alaykum, 8-A sinf o'quvchilari! Ertangi darsimiz 'Odam anatomiyasi: Yurak faoliyati' mavzusida bo'ladi.",
                    time="12:00",
                    timeStr="12:00"
                )
            ]
            db.add_all(initial_chat)

        # 5. Seed Submissions if empty
        if db.query(SubmissionModel).count() == 0:
            initial_subs = [
                SubmissionModel(
                    id="sub-101",
                    studentId="user-stud-1",
                    studentName="Jasurbek Aliyev",
                    classGrade="8-A sinf",
                    studentClass="8-A sinf",
                    testTopic="Hujayra tuzilishi va organoidlari",
                    topic="Hujayra tuzilishi va organoidlari",
                    score=8,
                    total=9,
                    totalQuestions=9,
                    percentage=89,
                    grade="A'lo (5)",
                    gradeBadge="A'lo (5)",
                    date="21.10.2026, 14:15",
                    dateStr="21.10.2026, 14:15",
                    answers=[]
                ),
                SubmissionModel(
                    id="sub-102",
                    studentId="user-stud-2",
                    studentName="Madina Umarova",
                    classGrade="8-A sinf",
                    studentClass="8-A sinf",
                    testTopic="Hujayra tuzilishi va organoidlari",
                    topic="Hujayra tuzilishi va organoidlari",
                    score=9,
                    total=9,
                    totalQuestions=9,
                    percentage=100,
                    grade="A'lo (5)",
                    gradeBadge="A'lo (5)",
                    date="21.10.2026, 14:35",
                    dateStr="21.10.2026, 14:35",
                    answers=[]
                ),
                SubmissionModel(
                    id="sub-103",
                    studentId="user-stud-3",
                    studentName="Bekzod Toshmatov",
                    classGrade="9-B sinf",
                    studentClass="9-B sinf",
                    testTopic="Fotosintez va Hujayra nafas olishi",
                    topic="Fotosintez va Hujayra nafas olishi",
                    score=7,
                    total=10,
                    totalQuestions=10,
                    percentage=70,
                    grade="Yaxshi (4)",
                    gradeBadge="Yaxshi (4)",
                    date="21.10.2026, 15:00",
                    dateStr="21.10.2026, 15:00",
                    answers=[]
                )
            ]
            db.add_all(initial_subs)

        # 6. Seed Teacher Tests if empty
        if db.query(TeacherTestModel).count() == 0:
            initial_tests = [
                TeacherTestModel(
                    id="topic-bio-1",
                    subject="Biologiya",
                    topic="Hujayra tuzilishi va organoidlari",
                    classGrade="6-7 sinf",
                    description="Boshlang'ichdan chuqur tushunchagacha 3 bosqichli bilim sinovi",
                    teacherName="Aziza Rahimova",
                    levels=[
                        {
                            "difficulty": "Oson",
                            "title": "1-bosqich: Boshlang'ich tushunchalar",
                            "description": "Hujayra va uning asosiy qismlari haqidagi sodda savollar",
                            "questions": [
                                {
                                    "id": "bio-oson-1",
                                    "question": "O'simlik hujayrasining eng tashqi qattiq qobig'i qanday nomlanadi?",
                                    "options": ["Hujayra devori (qobig'i)", "Ribosoma", "Mitoxondriya", "Sitoplazma"],
                                    "answerIndex": 0,
                                    "explanation": "O'simlik hujayrasi tashqi tomondan kletchatkadan iborat qattiq hujayra devori bilan o'ralgan."
                                },
                                {
                                    "id": "bio-oson-2",
                                    "question": "O'simlikka yashil rang beruvchi va fotosintez amalga oshadigan plastida qaysi?",
                                    "options": ["Xloroplast", "Xromoplast", "Leykoplast", "Lizosoma"],
                                    "answerIndex": 0,
                                    "explanation": "Xloroplast tarkibidagi xlorofill pigmenti hisobiga o'simlik yashil ko'rinadi va unda fotosintez kechadi."
                                },
                                {
                                    "id": "bio-oson-3",
                                    "question": "Hujayra ichidagi irsiy axborot (DNK) asosan qaysi organda saqlanadi?",
                                    "options": ["Yadroda", "Vakuolada", "Golji majmuasida", "Hujayra devorida"],
                                    "answerIndex": 0,
                                    "explanation": "Eukariot hujayralarda genetik axborot asosan hujayra yadrosidagi xromosomalarda saqlanadi."
                                }
                            ]
                        },
                        {
                            "difficulty": "O'rtacha",
                            "title": "2-bosqich: Tushunish va vazifalar",
                            "description": "Organoidlar funktsiyalari va metabolizm jarayonlari",
                            "questions": [
                                {
                                    "id": "bio-orta-1",
                                    "question": "Hujayraning 'energiya stansiyasi' hisoblangan va ATF sintezlaydigan organoid qaysi?",
                                    "options": ["Mitoxondriya", "Lizosoma", "Ribosoma", "Sentriola"],
                                    "answerIndex": 0,
                                    "explanation": "Mitoxondriya ATF sintezlaydi va hujayrani energiya bilan ta'minlaydi."
                                },
                                {
                                    "id": "bio-orta-2",
                                    "question": "Hujayrada oqsillar sintezi qaysi organoidda amalga oshiriladi?",
                                    "options": ["Ribosomalarda", "Vakuolada", "Xromoplastda", "Yadroning qobig'ida"],
                                    "answerIndex": 0,
                                    "explanation": "Ribosomalar aminokislotalardan oqsil molekulalarini sintezlash uchun javobgardir."
                                },
                                {
                                    "id": "bio-orta-3",
                                    "question": "Eski yoki keraksiz organoidlarni parchalovchi organoid qaysi?",
                                    "options": ["Lizosoma", "Plastida", "Sentrosoma", "Endoplazmatik to'r"],
                                    "answerIndex": 0,
                                    "explanation": "Lizosomalar tarkibidagi gidrolitik fermentlar hujayra ichki hazmini amalga oshiradi."
                                }
                            ]
                        },
                        {
                            "difficulty": "Qiyin",
                            "title": "3-bosqich: DTM va Olimpiada darajasi",
                            "description": "Murakkab biokimyoviy qonuniyatlar va solishtirma tahlil",
                            "questions": [
                                {
                                    "id": "bio-qiyin-1",
                                    "question": "Quyidagi qaysi organoidlar o'zining shaxsiy halqasimon DNK si va 70S ribosomasiga ega?",
                                    "options": ["Mitoxondriya va xloroplast", "Lizosoma va peroksisoma", "Golji majmuasi va vakuola", "Ribosoma va sentriola"],
                                    "answerIndex": 0,
                                    "explanation": "Mitoxondriya va xloroplastlar o'zining DNK va 70S ribosomasiga ega bo'lib yarim avtonomdir."
                                }
                            ]
                        }
                    ]
                )
            ]
            db.add_all(initial_tests)

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()
