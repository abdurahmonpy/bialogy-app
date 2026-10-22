# 🌿 BioEdu Platform — Zamonaviy Biologiya Ta'lim Tizimi

O'quvchilar va biologiya o'qituvchilari uchun maxsus ishlab chiqilgan to'liq funksional ikki bosqichli ta'lim platformasi.

---

## 🚀 Texnologiyalar

- **Backend:** FastAPI (Python 3.10+), SQLAlchemy 2.0 ORM, Uvicorn
- **Database:** PostgreSQL (Production / Railway), SQLite (Lokal test uchun)
- **Frontend:** Pure HTML5, CSS3 (Modern Glassmorphism & Responsive Design), Vanilla JavaScript (Modular API Client)
- **AI Integratsiyasi:** Google Gemini AI (Savollarni tahlil qilish, biologik yordamchi)
- **Deploy:** 
  - Backend: [Railway.app](https://railway.app) (Nixpacks / Procfile)
  - Frontend: [Vercel](https://vercel.com) (`vercel.json`)

---

## 👥 Foydalanuvchi Rollari va Sahifalar

### 🎓 1. O'quvchi Kabineti (`/student`)
- **Bosh sahifa:** O'quvchining shaxsiy ko'rsatkichlari, biologik iqtiboslar, tezkor harakatlar
- **Chat:** O'qituvchi va guruh bilan real-vaqt muloqoti
- **Uyga vazifa:** Berilgan vazifalar ro'yxati, topshirish va natijalarni ko'rish
- **Test:** Bilimni sinovdan o'tkazish, test savollari va natijalar

### 👨‍🏫 2. O'qituvchi Kabineti (`/teacher`)
- **Bosh sahifa:** Umumiy analitika (o'quvchilar soni, topshiriqlar, guruhlar)
- **Chat:** O'quvchilar bilan muloqot va e'lonlar
- **Guruhlarim:** Guruhlar ro'yxati, yangi guruh ochish va boshqarish
- **Uyga vazifa:** Yangi vazifa yaratish, muddat belgilash, o'quvchilar javoblarini tekshirish va baholash
- **O'quvchilar:** Barcha o'quvchilar ro'yxati, qidiruv va faollik
- **Test Markazi:** Yangi biologik testlar yaratish, variantlar va to'g'ri javoblarni kiritish
- **Statistika:** Vizual diagrammalar, o'zlashtirish foizi va faollik ko'rsatkichlari
- **AI Yordamchi:** Gemini AI asosidagi biologiya o'qitish bo'yicha maslahatchi
- **O'quvchi qo'shish:** Yangi o'quvchilarni tizimga va guruhga biriktirish

### 🔐 3. Avtorizatsiya
- **Kirish (`/login.html`):** Rolga qarab (O'qituvchi yoki O'quvchi) avtomatik yo'naltirish
- **Ro'yxatdan o'tish (`/register.html`):** Yangi hisob yaratish

---

## 💻 Lokal Muhitda Ishga Tushirish

1. **Repozitoriyani yuklab oling va virtual muhit yarating:**
   ```bash
   git clone https://github.com/abdurahmonpy/bialogy-app.git
   cd bialogy-app
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux / macOS:
   source venv/bin/activate
   ```

2. **Kutubxonalarni o'rnating:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Muhit o'zgaruvchilarini sozlang (ixtiyoriy):**
   ```bash
   cp .env.example .env
   ```
   *Agar `DATABASE_URL` berilmasa, tizim avtomatik ravishda `biology.db` SQLite bazasidan foydalanadi va birlamchi ma'lumotlarni generatsiya qiladi.*

4. **Serverni ishga tushiring:**
   ```bash
   uvicorn main:app --reload --port 3000
   ```
   Brauzerda oching: `http://localhost:3000`

---

## 🚂 Railway.app da Backend va PostgreSQL ni Deploy Qilish

1. [Railway.app](https://railway.app) ga kiring va yangi loyiha oching (**New Project**).
2. **Provision PostgreSQL** ni tanlang (Railway sizga avtomatik PostgreSQL bazasi va `DATABASE_URL` o'zgaruvchisini taqdim etadi).
3. **Deploy from GitHub Repo** ni tanlang va `bialogy-app` repozitoriyasini ulang.
4. Xizmat sozlamalarida (**Variables**):
   - `DATABASE_URL` avtomatik ulanadi (agar ulanmasa, PostgreSQL xizmatidagi `DATABASE_URL` ni nusxalab qo'ying).
   - `GEMINI_API_KEY`: Google AI studio dan olingan kalit (ixtiyoriy).
5. Railway loyihangizga avtomatik domen beradi: `https://your-backend.up.railway.app`.

---

## ▲ Vercel da Frontendni Deploy Qilish

1. [Vercel.com](https://vercel.com) ga kiring va **Add New... -> Project** ni bosing.
2. `bialogy-app` repozitoriyasini import qiling.
3. Loyiha papkasida `frontend/` papkasi yoki root orqali deploy qilinadi (`vercel.json` tayyorlab qo'yilgan).
4. `frontend/js/api.js` faylidagi yoki `BACKEND_URL` sozlamasini Railway backend URL manziliga yo'naltiring.

---

## 🔑 Birlamchi Test Hisoblari

Baza birinchi marta ishga tushganda avtomatik quyidagi hisoblar yaratiladi:
- **O'qituvchi:** Logini: `teacher` / Parol: `123`
- **O'quvchi:** Logini: `student` / Parol: `123`
