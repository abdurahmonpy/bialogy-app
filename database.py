import os
import time
from typing import Any, Dict, List, Optional
from sqlalchemy import create_engine, Column, String, Integer, BigInteger, Text, JSON, text
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
    email = Column(String, nullable=True, index=True)
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
            "email": self.email,
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
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN email VARCHAR"))
            conn.commit()
    except Exception:
        pass
    seed_initial_data()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def clean_demo_records(db: Session):
    """Purge all dummy/demo students, groups, submissions, homework, and chat."""
    try:
        # Delete demo students
        db.query(UserModel).filter(
            (UserModel.id.in_(["user-stud-1", "user-stud-2", "user-stud-3"])) |
            (UserModel.login.in_(["student", "madina", "bekzod"]))
        ).delete(synchronize_session=False)

        # Delete demo groups
        db.query(GroupModel).filter(
            GroupModel.id.in_(["group-8a", "group-9b", "group-abitur"])
        ).delete(synchronize_session=False)

        # Delete demo homework
        db.query(HomeworkModel).filter(
            HomeworkModel.id.in_(["hw-1", "hw-2"])
        ).delete(synchronize_session=False)

        # Delete demo submissions
        db.query(SubmissionModel).filter(
            SubmissionModel.id.in_(["sub-101", "sub-102", "sub-103"])
        ).delete(synchronize_session=False)

        # Delete demo chat
        db.query(ChatMessageModel).filter(
            ChatMessageModel.id.in_(["msg-1", "msg-2", "msg-3"])
        ).delete(synchronize_session=False)

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error cleaning demo records: {e}")

def seed_initial_data():
    db = SessionLocal()
    try:
        # Purge any old demo data first
        clean_demo_records(db)

        # 1. Seed Default Teacher only if no users exist
        if db.query(UserModel).count() == 0:
            default_teacher = UserModel(
                id="user-teacher-1",
                role="teacher",
                login="teacher",
                password="123",
                fullName="O'qituvchi",
                classGrade=None,
                groupId=None,
                subject="Biologiya va Tabiiy fanlar",
                school="Umumiy o'rta ta'lim maktabi",
                phone="+998 90 000 00 00",
                streakDays=1,
                avatar="O",
                createdAt=int(time.time() * 1000)
            )
            db.add(default_teacher)

        # Note: Groups, Students, Homework, Submissions, Chat are NOT seeded!
        # They will be created authentically by the teacher and students.

        # 2. Seed Standard Biology Test Bank if empty
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
