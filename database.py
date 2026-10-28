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
    status = Column(String, default="pending") # "pending" or "approved"
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
            "status": self.status or ("approved" if self.role == "teacher" else "pending"),
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
    fileUrl = Column(String, nullable=True)
    fileName = Column(String, nullable=True)
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
            "fileUrl": self.fileUrl,
            "fileName": self.fileName,
            "createdAt": self.createdAt,
            "submissions": self.submissions or []
        }

class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, index=True)
    channel = Column(String, index=True)
    channelId = Column(String, nullable=True)
    receiverId = Column(String, nullable=True)
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
            "receiverId": getattr(self, "receiverId", None) or self.channelId,
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
    category = Column(String, default="Mavzulashtirilgan")
    tags = Column(JSON, default=list)
    questions = Column(JSON, default=list)
    createdAt = Column(BigInteger, default=lambda: int(time.time() * 1000))
    levels = Column(JSON, default=list)

    def to_dict(self) -> Dict[str, Any]:
        qs = self.questions or []
        if not qs and self.levels:
            # Flatten levels into questions array for universal access
            for lvl in self.levels:
                diff = lvl.get("difficulty", "O'rtacha")
                for q in lvl.get("questions", []):
                    item = dict(q)
                    item["difficulty"] = diff
                    qs.append(item)

        return {
            "id": self.id,
            "subject": self.subject,
            "topic": self.topic,
            "classGrade": self.classGrade,
            "description": self.description,
            "teacherName": self.teacherName,
            "category": self.category or "Mavzulashtirilgan",
            "tags": self.tags or [],
            "questions": qs,
            "totalQuestions": len(qs),
            "createdAt": self.createdAt,
            "levels": self.levels or []
        }

class LiveTestSessionModel(Base):
    __tablename__ = "live_test_sessions"

    id = Column(String, primary_key=True, index=True)
    code = Column(String, unique=True, index=True) # 6-digit numeric join code
    testId = Column(String, index=True)
    testTitle = Column(String)
    subject = Column(String, default="Biologiya")
    classGrade = Column(String, nullable=True)
    teacherId = Column(String, index=True)
    teacherName = Column(String)
    groupId = Column(String, nullable=True) # assigned group or "all"
    groupName = Column(String, nullable=True)
    status = Column(String, default="lobby") # lobby, active, paused, finished
    settings = Column(JSON, default=dict)
    questions = Column(JSON, default=list)
    startTime = Column(BigInteger, default=0)
    endTime = Column(BigInteger, default=0)
    pausedAt = Column(BigInteger, default=0)
    totalPausedDuration = Column(Integer, default=0)
    timeExtendedSeconds = Column(Integer, default=0)
    createdAt = Column(BigInteger, default=lambda: int(time.time() * 1000))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "code": self.code,
            "testId": self.testId,
            "testTitle": self.testTitle,
            "subject": self.subject or "Biologiya",
            "classGrade": self.classGrade or "",
            "teacherId": self.teacherId,
            "teacherName": self.teacherName,
            "groupId": self.groupId,
            "groupName": self.groupName or "Barcha o'quvchilar",
            "status": self.status,
            "settings": self.settings or {},
            "questionsCount": len(self.questions or []),
            "questions": self.questions or [],
            "startTime": self.startTime,
            "endTime": self.endTime,
            "pausedAt": self.pausedAt,
            "totalPausedDuration": self.totalPausedDuration or 0,
            "timeExtendedSeconds": self.timeExtendedSeconds or 0,
            "createdAt": self.createdAt
        }

class LiveParticipantModel(Base):
    __tablename__ = "live_participants"

    id = Column(String, primary_key=True, index=True)
    sessionId = Column(String, index=True)
    studentId = Column(String, index=True)
    studentName = Column(String)
    isGuest = Column(Integer, default=0)
    isOnline = Column(Integer, default=1)
    currentQuestionIndex = Column(Integer, default=0)
    score = Column(Integer, default=0)
    correctCount = Column(Integer, default=0)
    incorrectCount = Column(Integer, default=0)
    totalAnswered = Column(Integer, default=0)
    answers = Column(JSON, default=dict) # { questionId: { answer, isCorrect, pointsEarned, timeSpentMs } }
    cheatLogs = Column(JSON, default=list) # [ { type, time, count } ]
    cheatCount = Column(Integer, default=0)
    status = Column(String, default="lobby") # lobby, in_progress, submitted, timed_out
    joinedAt = Column(BigInteger, default=lambda: int(time.time() * 1000))
    finishedAt = Column(BigInteger, default=0)
    lastActiveAt = Column(BigInteger, default=lambda: int(time.time() * 1000))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sessionId": self.sessionId,
            "studentId": self.studentId,
            "studentName": self.studentName,
            "isGuest": bool(self.isGuest),
            "isOnline": bool(self.isOnline),
            "currentQuestionIndex": self.currentQuestionIndex,
            "score": self.score,
            "correctCount": self.correctCount,
            "incorrectCount": self.incorrectCount,
            "totalAnswered": self.totalAnswered,
            "answers": self.answers or {},
            "cheatLogs": self.cheatLogs or [],
            "cheatCount": self.cheatCount or 0,
            "status": self.status,
            "joinedAt": self.joinedAt,
            "finishedAt": self.finishedAt,
            "lastActiveAt": self.lastActiveAt
        }

class ResourceModel(Base):
    __tablename__ = "resources"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subject = Column(String, default="Biologiya")
    classGrade = Column(String, nullable=True) # "5-sinf", "6-sinf", ..., "Abituriyent", "Barchasi"
    category = Column(String, default="Darslik") # "Darslik", "Metodik qo'llanma", "Atlas", "Laboratoriya", "Test to'plami"
    author = Column(String, nullable=True)
    year = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    fileUrl = Column(String, nullable=False)
    fileName = Column(String, nullable=True)
    fileSize = Column(String, nullable=True)
    coverColor = Column(String, default="emerald")
    downloads = Column(Integer, default=0)
    createdAt = Column(BigInteger, default=lambda: int(time.time() * 1000))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "subject": self.subject or "Biologiya",
            "classGrade": self.classGrade or "Barchasi",
            "category": self.category or "Darslik",
            "author": self.author or "",
            "year": self.year or "",
            "description": self.description or "",
            "fileUrl": self.fileUrl,
            "fileName": self.fileName or "fayl.pdf",
            "fileSize": self.fileSize or "10 MB",
            "coverColor": self.coverColor or "emerald",
            "downloads": self.downloads or 0,
            "createdAt": self.createdAt
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

    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE homework ADD COLUMN fileUrl VARCHAR"))
            conn.commit()
    except Exception:
        pass

    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE homework ADD COLUMN fileName VARCHAR"))
            conn.commit()
    except Exception:
        pass

    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN status VARCHAR DEFAULT 'approved'"))
            conn.commit()
    except Exception:
        pass

    # Ensure all resources columns exist on existing databases (Render / Railway PostgreSQL migrations)
    resource_columns = [
        ("title", "VARCHAR"),
        ("subject", "VARCHAR DEFAULT 'Biologiya'"),
        ("classGrade", "VARCHAR"),
        ("category", "VARCHAR DEFAULT 'Darslik'"),
        ("author", "VARCHAR"),
        ("year", "VARCHAR"),
        ("description", "TEXT"),
        ("fileUrl", "VARCHAR"),
        ("fileName", "VARCHAR"),
        ("fileSize", "VARCHAR"),
        ("coverColor", "VARCHAR DEFAULT 'emerald'"),
        ("downloads", "INTEGER DEFAULT 0"),
        ("createdAt", "BIGINT")
    ]
    for col_name, col_type in resource_columns:
        try:
            with engine.connect() as conn:
                conn.execute(text(f"ALTER TABLE resources ADD COLUMN IF NOT EXISTS \"{col_name}\" {col_type}"))
                conn.commit()
        except Exception:
            try:
                with engine.connect() as conn:
                    conn.execute(text(f"ALTER TABLE resources ADD COLUMN \"{col_name}\" {col_type}"))
                    conn.commit()
            except Exception:
                pass

    # Ensure teacher_tests columns exist
    test_columns = [
        ("category", "VARCHAR DEFAULT 'Mavzulashtirilgan'"),
        ("tags", "JSON"),
        ("questions", "JSON")
    ]
    for col_name, col_type in test_columns:
        try:
            with engine.connect() as conn:
                conn.execute(text(f"ALTER TABLE teacher_tests ADD COLUMN IF NOT EXISTS \"{col_name}\" {col_type}"))
                conn.commit()
        except Exception:
            try:
                with engine.connect() as conn:
                    conn.execute(text(f"ALTER TABLE teacher_tests ADD COLUMN \"{col_name}\" {col_type}"))
                    conn.commit()
            except Exception:
                pass

    # Ensure chat_messages columns exist
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS \"receiverId\" VARCHAR"))
            conn.commit()
    except Exception:
        try:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE chat_messages ADD COLUMN \"receiverId\" VARCHAR"))
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

def _generate_sample_pdf_if_missing(file_path: str, title: str, author: str, grade: str, desc: str):
    """Generate a valid, styled educational PDF for the seeded resource if not already existing."""
    try:
        if os.path.exists(file_path):
            return
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib import colors

        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        # Header background banner
        c.setFillColor(colors.HexColor("#047857"))  # emerald-700
        c.rect(0, height - 130, width, 130, fill=1, stroke=0)

        # Header text
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(45, height - 55, "BioEdu Ta'lim Platformasi")
        c.setFont("Helvetica", 12)
        c.drawString(45, height - 80, "Elektron Darsliklar va O'quv-Metodik Resurslar Markazi")
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(45, height - 102, f"Raqamlashtirilgan ta'limiy nashr | {grade}")

        # Book Title
        c.setFillColor(colors.HexColor("#0f172a"))
        c.setFont("Helvetica-Bold", 16)
        c.drawString(45, height - 170, title)

        # Author and Meta info
        c.setFillColor(colors.HexColor("#475569"))
        c.setFont("Helvetica", 11)
        c.drawString(45, height - 195, f"Muallif(lar): {author}  |  Sinf / Bosqich: {grade}")

        # Horizontal separator
        c.setStrokeColor(colors.HexColor("#cbd5e1"))
        c.setLineWidth(1.5)
        c.line(45, height - 215, width - 45, height - 215)

        # Overview Header
        c.setFillColor(colors.HexColor("#1e293b"))
        c.setFont("Helvetica-Bold", 13)
        c.drawString(45, height - 245, "Resurs haqida qisqacha ma'lumot va mundarija:")

        # Summary box
        c.setFillColor(colors.HexColor("#f8fafc"))
        c.setStrokeColor(colors.HexColor("#e2e8f0"))
        c.roundRect(45, height - 370, width - 90, 110, 8, fill=1, stroke=1)

        c.setFillColor(colors.HexColor("#334155"))
        c.setFont("Helvetica", 10)
        c.drawString(60, height - 275, f"Tavsif: {desc[:90]}...")
        if len(desc) > 90:
            c.drawString(60, height - 295, f"{desc[90:185]}...")

        c.drawString(60, height - 325, "Ushbu elektron darslik umumiy o'rta va ixtisoslashtirilgan ta'lim talablari asosida")
        c.drawString(60, height - 345, "o'quvchilar hamda pedagoglar foydalanishi uchun tayyorlangan.")

        # Chapters listing
        c.setFillColor(colors.HexColor("#0f172a"))
        c.setFont("Helvetica-Bold", 12)
        c.drawString(45, height - 405, "Asosiy boblar va mavzular:")

        c.setFont("Helvetica", 10)
        c.setFillColor(colors.HexColor("#334155"))
        chapters = [
            "1-bob. Kirish: fanning predmeti, vazifalari va ilmiy metodlari",
            "2-bob. Biologik tizimlar, ularning o'ziga xos tuzilishi va qonuniyatlari",
            "3-bob. Moddalar va energiya almashinuvi jarayonlari",
            "4-bob. Hayot faoliyatining boshqarilishi va muhitga moslashuv",
            "5-bob. Laboratoriya va amaliy tajriba mashg'ulotlari",
            "6-bob. O'zlashtirishni tekshirish uchun test va mantiqiy savollar"
        ]
        curr_y = height - 430
        for ch in chapters:
            c.drawString(55, curr_y, f"•  {ch}")
            curr_y -= 22

        # Note at bottom
        c.setFillColor(colors.HexColor("#f1f5f9"))
        c.setStrokeColor(colors.HexColor("#cbd5e1"))
        c.roundRect(45, 90, width - 90, 50, 6, fill=1, stroke=1)
        c.setFillColor(colors.HexColor("#475569"))
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(60, 120, "Eslatma: Ushbu darslik BioEdu platformasi foydalanuvchilari uchun onlayn mutolaa")
        c.drawString(60, 104, "va yuklab olish imkoniyati bilan bepul taqdim etiladi.")

        # Footer
        c.setFillColor(colors.HexColor("#94a3b8"))
        c.setFont("Helvetica", 9)
        c.drawString(45, 45, "© BioEdu Online Education System. Barcha huquqlar himoyalangan.")

        c.save()
    except Exception as e:
        print(f"Error generating sample PDF for {title}: {e}")

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
                status="approved",
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

        # 3. Seed Standard Textbooks & Educational Resources if empty
        if db.query(ResourceModel).count() == 0:
            res_dir = os.path.join(os.path.dirname(__file__), "uploads", "resources")
            os.makedirs(res_dir, exist_ok=True)

            sample_resources = [
                {
                    "id": "res-bio-5",
                    "title": "Biologiya (Tabiiy fanlar) - 5-sinf darsligi",
                    "subject": "Biologiya",
                    "classGrade": "5-sinf",
                    "category": "Darslik",
                    "author": "A. Bahromov, Sh. Sharipov",
                    "year": "2022",
                    "description": "Umumiy o'rta ta'lim maktablarining 5-sinfi uchun tabiiy fanlar, tirik tabiat asoslari va organizmlar xilma-xilligi darsligi.",
                    "fileName": "Biologiya_5_sinf.pdf",
                    "fileSize": "12.4 MB",
                    "coverColor": "emerald",
                    "downloads": 142
                },
                {
                    "id": "res-bio-6",
                    "title": "Botanika: O'simliklar dunyosi - 6-sinf darsligi",
                    "subject": "Biologiya",
                    "classGrade": "6-sinf",
                    "category": "Darslik",
                    "author": "O. Pratov, A. To'xtayev, F. Azimova",
                    "year": "2021",
                    "description": "O'simliklar morfologiyasi, hujayra va to'qimalar, ildiz, poya, barg hamda generativ organlar anatomiyasi.",
                    "fileName": "Botanika_6_sinf.pdf",
                    "fileSize": "16.8 MB",
                    "coverColor": "teal",
                    "downloads": 198
                },
                {
                    "id": "res-bio-7",
                    "title": "Zoologiya: Hayvonot olami - 7-sinf darsligi",
                    "subject": "Biologiya",
                    "classGrade": "7-sinf",
                    "category": "Darslik",
                    "author": "F. Mavlonov, S. Dadayev, Q. Saparov",
                    "year": "2022",
                    "description": "Bir hujayralilar, umurtqasizlar va umurtqali hayvonlar sistematikasi, ularning ichki tuzilishi va ekologiyasi.",
                    "fileName": "Zoologiya_7_sinf.pdf",
                    "fileSize": "18.2 MB",
                    "coverColor": "blue",
                    "downloads": 215
                },
                {
                    "id": "res-bio-8",
                    "title": "Odam va uning salomatligi - 8-sinf darsligi",
                    "subject": "Biologiya",
                    "classGrade": "8-sinf",
                    "category": "Darslik",
                    "author": "J. Tolipova, M. Umarova, A. G'ofurov",
                    "year": "2023",
                    "description": "Odam anatomiyasi, fiziologiyasi, asab va gumoral boshqaruv, nafas olish, qon aylanish va gigiyena qoidalari.",
                    "fileName": "Odam_anatomiyasi_8_sinf.pdf",
                    "fileSize": "15.6 MB",
                    "coverColor": "indigo",
                    "downloads": 320
                },
                {
                    "id": "res-bio-9",
                    "title": "Sitologiya va genetika asoslari - 9-sinf darsligi",
                    "subject": "Biologiya",
                    "classGrade": "9-sinf",
                    "category": "Darslik",
                    "author": "A. Zikiryayev, A. To'xtayev",
                    "year": "2022",
                    "description": "Hujayra tuzilishi, ATF, biosintez, mitoz, meyoz bo'linish, Mendel qonunlari va seleksiya yutuqlari.",
                    "fileName": "Sitologiya_Genetika_9_sinf.pdf",
                    "fileSize": "21.0 MB",
                    "coverColor": "violet",
                    "downloads": 274
                },
                {
                    "id": "res-bio-10",
                    "title": "Umumiy biologiya - 10-sinf darsligi",
                    "subject": "Biologiya",
                    "classGrade": "10-sinf",
                    "category": "Darslik",
                    "author": "A. G'ofurov, A. Abdukarimov, J. Tolipova",
                    "year": "2023",
                    "description": "Molekulyar biologiya, biokimyoviy jarayonlar, ontogenez, biotexnologiya va genetik muhandislik asoslari.",
                    "fileName": "Umumiy_biologiya_10_sinf.pdf",
                    "fileSize": "19.5 MB",
                    "coverColor": "cyan",
                    "downloads": 185
                },
                {
                    "id": "res-bio-11",
                    "title": "Umumiy biologiya va ekologiya - 11-sinf darsligi",
                    "subject": "Biologiya",
                    "classGrade": "11-sinf",
                    "category": "Darslik",
                    "author": "A. G'ofurov, J. Tolipova, M. Umarova",
                    "year": "2024",
                    "description": "Darvin ta'limoti, mikroevolyutsiya, makroevolyutsiya, Yerda hayotning paydo bo'lishi va biosfera muhofazasi.",
                    "fileName": "Biologiya_11_sinf.pdf",
                    "fileSize": "22.3 MB",
                    "coverColor": "emerald",
                    "downloads": 240
                },
                {
                    "id": "res-dtm-bio",
                    "title": "DTM / BMBA Biologiya test to'plami va yechimlari",
                    "subject": "Biologiya",
                    "classGrade": "Abituriyent",
                    "category": "Test to'plami",
                    "author": "Davlat Test Markazi (BMBA ekspertlari)",
                    "year": "2024",
                    "description": "OTMlarga kirish imtihonlari uchun yangi formatdagi 1500+ murakkab testlar, masalalar va grafik tahlillar to'plami.",
                    "fileName": "DTM_Biologiya_2024.pdf",
                    "fileSize": "28.5 MB",
                    "coverColor": "rose",
                    "downloads": 580
                },
                {
                    "id": "res-atlas-bio",
                    "title": "Odam anatomiyasi va gistologiyasi rangli atlasi",
                    "subject": "Biologiya",
                    "classGrade": "8-sinf",
                    "category": "Atlas",
                    "author": "Respublika Ta'lim Markazi",
                    "year": "2023",
                    "description": "Inson suyagi, mushaklari, ichki a'zolari va to'qimalarining yuqori sifatli rangli illyustratsiyalar to'plami.",
                    "fileName": "Anatomiya_Atlas_Rangli.pdf",
                    "fileSize": "34.1 MB",
                    "coverColor": "amber",
                    "downloads": 412
                },
                {
                    "id": "res-lab-bio",
                    "title": "Biologiya fanidan laboratoriya ishlari daftari",
                    "subject": "Biologiya",
                    "classGrade": "7-sinf",
                    "category": "Laboratoriya",
                    "author": "O'zbekiston Metodistlar Assotsiatsiyasi",
                    "year": "2023",
                    "description": "Mikroskop bilan ishlash, vaqtinchalik mikropreparatlar tayyorlash va tajribalarni mustaqil o'tkazish yo'riqnomasi.",
                    "fileName": "Laboratoriya_Daftari_Biologiya.pdf",
                    "fileSize": "9.2 MB",
                    "coverColor": "teal",
                    "downloads": 164
                },
                {
                    "id": "res-chem-7",
                    "title": "Umumiy Kimyo - 7-sinf darsligi",
                    "subject": "Kimyo",
                    "classGrade": "7-sinf",
                    "category": "Darslik",
                    "author": "I. Asqarov, N. To'xtaboyev",
                    "year": "2022",
                    "description": "Kimyoning asosiy tushunchalari, kimyoviy elementlar, davriy qonun va oddiy moddalarning xossalari.",
                    "fileName": "Kimyo_7_sinf.pdf",
                    "fileSize": "14.5 MB",
                    "coverColor": "indigo",
                    "downloads": 128
                },
                {
                    "id": "res-metod-bio",
                    "title": "Biologiya o'qitish metodikasi va dars ishlanmalari",
                    "subject": "Biologiya",
                    "classGrade": "Barchasi",
                    "category": "Metodik qo'llanma",
                    "author": "J. Tolipova, N. Alimova",
                    "year": "2023",
                    "description": "O'qituvchilar uchun zamonaviy pedagogik texnologiyalar, STEAM yondashuvi va interaktiv dars rejalari.",
                    "fileName": "Biologiya_Metodik_Qollanma.pdf",
                    "fileSize": "11.7 MB",
                    "coverColor": "blue",
                    "downloads": 205
                }
            ]

            initial_resources = []
            for item in sample_resources:
                pdf_path = os.path.join(res_dir, item["fileName"])
                _generate_sample_pdf_if_missing(
                    file_path=pdf_path,
                    title=item["title"],
                    author=item["author"],
                    grade=item["classGrade"],
                    desc=item["description"]
                )
                initial_resources.append(
                    ResourceModel(
                        id=item["id"],
                        title=item["title"],
                        subject=item["subject"],
                        classGrade=item["classGrade"],
                        category=item["category"],
                        author=item["author"],
                        year=item["year"],
                        description=item["description"],
                        fileUrl=f"/uploads/resources/{item['fileName']}",
                        fileName=item["fileName"],
                        fileSize=item["fileSize"],
                        coverColor=item["coverColor"],
                        downloads=item["downloads"],
                        createdAt=int(time.time() * 1000)
                    )
                )

            db.add_all(initial_resources)

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()
