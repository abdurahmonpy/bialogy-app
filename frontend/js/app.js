/**
 * Biologiya & Fanlar Test Bot - Pure Frontend Application Logic
 */

// Application State
const state = {
  currentRole: localStorage.getItem('user_role') || 'student', // 'student' | 'teacher'
  currentTab: 'syllabus', // 'syllabus' | 'test' | 'tutor' | 'glossary' | 'diagram' | 'teacher'
  currentSubject: 'Biologiya',
  selectedClassId: '5',
  syllabusSearch: '',
  activeLesson: null,
  
  // Student Profile
  studentProfile: (() => {
    try {
      const saved = localStorage.getItem('student_profile');
      return saved ? JSON.parse(saved) : {
        id: 'stud-1',
        fullName: 'Jasurbek Aliyev',
        classGrade: '8-A sinf',
        school: '14-sonli umumiy o\'rta ta\'lim maktabi'
      };
    } catch {
      return { id: 'stud-1', fullName: 'Jasurbek Aliyev', classGrade: '8-A sinf', school: '14-maktab' };
    }
  })(),

  // Teacher Profile
  teacherProfile: (() => {
    try {
      const saved = localStorage.getItem('teacher_profile');
      return saved ? JSON.parse(saved) : {
        id: 'teacher-1',
        fullName: 'Aziza Rahimova',
        subject: 'Biologiya',
        isAuthorized: false
      };
    } catch {
      return { id: 'teacher-1', fullName: 'Aziza Rahimova', subject: 'Biologiya', isAuthorized: false };
    }
  })(),

  // Active Quiz State
  quiz: {
    inProgress: false,
    subject: 'Biologiya',
    topic: '',
    difficulty: 'O\'rtacha',
    questions: [],
    currentIndex: 0,
    selectedOption: null,
    isAnswered: false,
    score: 0,
    answers: [],
    startTime: null,
    timeSpentSeconds: 0,
    timerInterval: null
  },

  // AI Tutor Chat State
  tutorMessages: [
    {
      role: 'model',
      text: 'Assalomu alaykum! Men sizning Biologiya bo\'yicha shaxsiy AI repetitoringizman. Istalgan mavzu, hujayra yoki atama haqida so\'rang, sodda va qiziqarli qilib tushuntirib beraman!'
    }
  ],

  // AI Glossary State
  glossary: (() => {
    try {
      const saved = localStorage.getItem('biologiya_glossary_v1');
      return saved ? JSON.parse(saved) : [
        {
          term: "Mitoxondriya",
          origin: "Yunoncha 'mitos' - ip, 'chondrion' - donacha",
          definition: "Hujayraning energiya stansiyasi bo'lib, organik moddalarni oksidlab ATF shaklida energiya ishlab chiqaradi.",
          analogy: "Xuddi butun shaharga tok beruvchi ulkan elektr stansiyasiga o'xshaydi.",
          examFocus: "DTM testlarida uning o'z DNK si va 70S ribosomasiga ega bo'lgan 2 qavat membranali organoid ekani so'raladi."
        },
        {
          term: "Xloroplast",
          origin: "Yunoncha 'chloros' - yashil, 'plastos' - yasalgan",
          definition: "O'simlik hujayrasida fotosintez jarayonini amalga oshiruvchi yashil plastida.",
          analogy: "Quyosh nuri energiyasini ushlab olib qand (oziq) pishiradigan kichik quyosh oshxonasi.",
          examFocus: "Ichki tilakoid membranalari va granalarning joylashuvi ko'p tushadi."
        }
      ];
    } catch {
      return [];
    }
  })(),

  // Teacher Cabinet Data
  submissions: [],
  teacherTests: []
};

// -------------------------------------------------------------
// Initialization
// -------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  initUI();
  setupEventListeners();
  renderClassesSelector();
  renderLessonsList();
  renderSubjectsBar();
  renderGlossary();
  updateRoleBadge();
});

function initUI() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

// -------------------------------------------------------------
// UI Switching & Navigation
// -------------------------------------------------------------
function switchTab(tabId) {
  state.currentTab = tabId;

  // Update nav buttons
  document.querySelectorAll('.nav-tab-btn').forEach(btn => {
    if (btn.dataset.tab === tabId) {
      btn.classList.add('bg-emerald-600', 'text-white', 'shadow-sm');
      btn.classList.remove('text-slate-600', 'hover:bg-slate-100');
    } else {
      btn.classList.remove('bg-emerald-600', 'text-white', 'shadow-sm');
      btn.classList.add('text-slate-600', 'hover:bg-slate-100');
    }
  });

  // Toggle tab contents
  document.querySelectorAll('.tab-content').forEach(pane => {
    pane.classList.remove('active');
  });

  const activePane = document.getElementById(`tab-${tabId}`);
  if (activePane) {
    activePane.classList.add('active');
  }

  // Load specific tab data
  if (tabId === 'teacher') {
    checkTeacherAuthorization();
  } else if (tabId === 'diagram' && state.activeLesson) {
    loadLessonDiagram(state.activeLesson.title, state.activeLesson.topic, state.activeLesson.content);
  }

  if (window.lucide) window.lucide.createIcons();
}

function updateRoleBadge() {
  const badge = document.getElementById('user-role-badge');
  const studentBtn = document.getElementById('switch-role-btn');
  if (state.currentRole === 'teacher') {
    badge.className = 'px-3 py-1 text-xs font-bold rounded-full bg-amber-100 text-amber-800 border border-amber-300 flex items-center gap-1.5';
    badge.innerHTML = '<i data-lucide="shield-check" class="w-3.5 h-3.5"></i> O\'qituvchi Rejimi';
    studentBtn.textContent = 'O\'quvchiga o\'tish';
  } else {
    badge.className = 'px-3 py-1 text-xs font-bold rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300 flex items-center gap-1.5';
    badge.innerHTML = '<i data-lucide="graduation-cap" class="w-3.5 h-3.5"></i> O\'quvchi: ' + state.studentProfile.fullName;
    studentBtn.textContent = 'O\'qituvchi Kabineti';
  }
  if (window.lucide) window.lucide.createIcons();
}

// -------------------------------------------------------------
// Subjects & Classes Bar
// -------------------------------------------------------------
function renderSubjectsBar() {
  const container = document.getElementById('subjects-scroll-bar');
  if (!container || !window.APP_DATA) return;

  container.innerHTML = window.APP_DATA.SUBJECTS_LIST.map(sub => {
    const isSelected = sub.name === state.currentSubject;
    const activeClass = isSelected
      ? 'bg-emerald-600 text-white shadow-md border-emerald-700'
      : 'bg-white text-slate-700 border-slate-200 hover:border-emerald-400 hover:bg-slate-50';

    return `
      <button onclick="selectSubject('${sub.name}')" class="flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold border transition-all whitespace-nowrap ${activeClass}">
        <span>${sub.name}</span>
      </button>
    `;
  }).join('');
}

function selectSubject(subjectName) {
  state.currentSubject = subjectName;
  renderSubjectsBar();
  renderSubjectPresetTests();
  // If in quiz tab, update subject
  if (state.currentTab === 'test') {
    renderSubjectPresetTests();
  }
}

function renderClassesSelector() {
  const container = document.getElementById('classes-selector');
  if (!container || !window.APP_DATA) return;

  container.innerHTML = window.APP_DATA.CLASSES_LIST.map(c => {
    const isSelected = c.id === state.selectedClassId;
    const activeStyle = isSelected
      ? 'bg-emerald-600 text-white font-bold shadow-md scale-105'
      : 'bg-slate-100 text-slate-700 hover:bg-slate-200';

    return `
      <button onclick="selectClass('${c.id}')" class="px-3.5 py-1.5 rounded-xl text-xs transition-all ${activeStyle}">
        ${c.name}
      </button>
    `;
  }).join('');
}

function selectClass(classId) {
  state.selectedClassId = classId;
  renderClassesSelector();
  renderLessonsList();
}

// -------------------------------------------------------------
// Lessons & Syllabus
// -------------------------------------------------------------
function renderLessonsList() {
  const container = document.getElementById('lessons-grid');
  if (!container || !window.APP_DATA) return;

  const lessons = window.APP_DATA.SYLLABUS.filter(l => {
    const matchClass = l.classId === state.selectedClassId;
    const matchSearch = !state.syllabusSearch || 
      l.title.toLowerCase().includes(state.syllabusSearch.toLowerCase()) ||
      l.topic.toLowerCase().includes(state.syllabusSearch.toLowerCase());
    return matchClass && matchSearch;
  });

  if (lessons.length === 0) {
    container.innerHTML = `
      <div class="col-span-full py-12 text-center text-slate-400">
        <i data-lucide="book-open" class="w-12 h-12 mx-auto mb-2 opacity-40"></i>
        <p>Ushbu sinf yoki qidiruv bo'yicha darslar topilmadi.</p>
      </div>
    `;
    if (window.lucide) window.lucide.createIcons();
    return;
  }

  container.innerHTML = lessons.map(lesson => {
    return `
      <div class="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-xs hover:shadow-md hover:border-emerald-300 transition-all flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-2.5">
            <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-100">
              ${lesson.topic}
            </span>
            <span class="text-xs text-slate-400 font-medium">${lesson.difficulty}</span>
          </div>
          <h3 class="text-base font-bold text-slate-800 mb-2 line-clamp-1">${lesson.title}</h3>
          <p class="text-xs text-slate-500 line-clamp-2 leading-relaxed mb-4">${lesson.shortDesc}</p>
        </div>

        <div class="flex items-center gap-2 pt-3 border-t border-slate-100">
          <button onclick="openLesson('${lesson.id}')" class="flex-1 py-2 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors flex items-center justify-center gap-1.5">
            <i data-lucide="book-open" class="w-3.5 h-3.5"></i> O'qish
          </button>
          <button onclick="startQuizForLesson('${lesson.id}')" class="flex-1 py-2 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs transition-colors flex items-center justify-center gap-1.5">
            <i data-lucide="play" class="w-3.5 h-3.5"></i> Test
          </button>
        </div>
      </div>
    `;
  }).join('');

  if (window.lucide) window.lucide.createIcons();
}

function openLesson(lessonId) {
  const lesson = window.APP_DATA.SYLLABUS.find(l => l.id === lessonId);
  if (!lesson) return;

  state.activeLesson = lesson;
  const modal = document.getElementById('lesson-modal');
  const titleEl = document.getElementById('lesson-modal-title');
  const metaEl = document.getElementById('lesson-modal-meta');
  const bodyEl = document.getElementById('lesson-modal-body');
  const termsEl = document.getElementById('lesson-modal-terms');
  const analogiesEl = document.getElementById('lesson-modal-analogies');

  titleEl.textContent = lesson.title;
  metaEl.textContent = `${lesson.classId}-sinf • ${lesson.topic} • ${lesson.difficulty}`;
  
  // Format markdown headers
  const formattedContent = lesson.content
    .replace(/### (.*?)\n/g, '<h4 class="text-base font-bold text-slate-800 mt-4 mb-2">$1</h4>')
    .replace(/\*\*(.*?)\*\*/g, '<strong class="text-slate-900">$1</strong>')
    .replace(/\n\n/g, '<br/><br/>');
  bodyEl.innerHTML = formattedContent;

  // Key terms
  termsEl.innerHTML = lesson.keyTerms.map(t => `
    <div class="p-3 bg-emerald-50/60 rounded-xl border border-emerald-100">
      <span class="font-bold text-emerald-900 text-xs">${t.term}:</span>
      <span class="text-xs text-emerald-800 leading-relaxed ml-1">${t.meaning}</span>
    </div>
  `).join('');

  // Analogies
  analogiesEl.innerHTML = lesson.analogies.map(a => `
    <li class="flex items-start gap-2 text-xs text-slate-600">
      <span class="text-emerald-600 font-bold">•</span>
      <span>${a}</span>
    </li>
  `).join('');

  modal.classList.remove('hidden');
  if (window.lucide) window.lucide.createIcons();
}

function closeLessonModal() {
  document.getElementById('lesson-modal').classList.add('hidden');
}

// -------------------------------------------------------------
// Interactive Quiz Engine
// -------------------------------------------------------------
async function startQuizForLesson(lessonId) {
  const lesson = window.APP_DATA.SYLLABUS.find(l => l.id === lessonId);
  if (!lesson) return;
  startCustomQuiz(lesson.topic, lesson.title, lesson.difficulty, 5, lesson.classId);
}

async function startCustomQuiz(subjectOrTopic, title, difficulty = 'O\'rtacha', count = 5, classId = null) {
  switchTab('test');

  const quizContainer = document.getElementById('quiz-view');
  const loadingEl = document.getElementById('quiz-loading');
  const listEl = document.getElementById('preset-tests-container');

  listEl.classList.add('hidden');
  loadingEl.classList.remove('hidden');
  quizContainer.classList.add('hidden');

  try {
    const res = await fetch('/api/generate-quiz', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        subject: state.currentSubject,
        topic: subjectOrTopic,
        lessonTitle: title,
        difficulty: difficulty,
        count: count,
        classId: classId || state.selectedClassId
      })
    });

    const data = await res.json();
    const questions = data.questions || [];

    if (questions.length === 0) {
      alert("Savollar yuklab bo'lmadi. Iltimos, qayta urinib ko'ring.");
      listEl.classList.remove('hidden');
      loadingEl.classList.add('hidden');
      return;
    }

    // Initialize Quiz
    state.quiz = {
      inProgress: true,
      subject: state.currentSubject,
      topic: title || subjectOrTopic,
      difficulty: difficulty,
      questions: questions,
      currentIndex: 0,
      selectedOption: null,
      isAnswered: false,
      score: 0,
      answers: [],
      startTime: Date.now(),
      timeSpentSeconds: 0,
      timerInterval: null
    };

    loadingEl.classList.add('hidden');
    quizContainer.classList.remove('hidden');
    startQuizTimer();
    renderCurrentQuestion();

  } catch (err) {
    console.error('Quiz start error:', err);
    alert("Testni boshlashda xatolik yuz berdi.");
    listEl.classList.remove('hidden');
    loadingEl.classList.add('hidden');
  }
}

function startQuizTimer() {
  if (state.quiz.timerInterval) clearInterval(state.quiz.timerInterval);
  const timerEl = document.getElementById('quiz-timer');

  state.quiz.timerInterval = setInterval(() => {
    state.quiz.timeSpentSeconds++;
    const mins = Math.floor(state.quiz.timeSpentSeconds / 60).toString().padStart(2, '0');
    const secs = (state.quiz.timeSpentSeconds % 60).toString().padStart(2, '0');
    if (timerEl) timerEl.textContent = `${mins}:${secs}`;
  }, 1000);
}

function renderCurrentQuestion() {
  const q = state.quiz.questions[state.quiz.currentIndex];
  if (!q) return;

  const total = state.quiz.questions.length;
  const currentNum = state.quiz.currentIndex + 1;

  document.getElementById('quiz-progress-text').textContent = `Savol ${currentNum} / ${total}`;
  document.getElementById('quiz-progress-bar').style.width = `${(currentNum / total) * 100}%`;
  document.getElementById('quiz-question-text').textContent = q.question;
  document.getElementById('quiz-explanation-box').classList.add('hidden');
  document.getElementById('quiz-next-btn').disabled = true;

  const optionsContainer = document.getElementById('quiz-options-grid');
  state.quiz.selectedOption = null;
  state.quiz.isAnswered = false;

  optionsContainer.innerHTML = q.options.map((opt, idx) => {
    return `
      <button onclick="handleOptionSelect(${idx})" id="opt-btn-${idx}" class="w-full text-left p-4 rounded-2xl border-2 border-slate-200/80 bg-white hover:border-emerald-400 hover:bg-emerald-50/30 transition-all font-medium text-slate-700 text-sm flex items-center justify-between">
        <span>${opt}</span>
        <div id="opt-icon-${idx}" class="w-5 h-5 rounded-full border border-slate-300 flex items-center justify-center text-xs"></div>
      </button>
    `;
  }).join('');
}

function handleOptionSelect(index) {
  if (state.quiz.isAnswered) return;

  const q = state.quiz.questions[state.quiz.currentIndex];
  state.quiz.selectedOption = index;
  state.quiz.isAnswered = true;

  const isCorrect = index === q.answerIndex;
  if (isCorrect) state.quiz.score++;

  state.quiz.answers.push({
    questionId: q.id,
    questionText: q.question,
    options: q.options,
    userAnswerIndex: index,
    correctAnswerIndex: q.answerIndex,
    isCorrect: isCorrect,
    explanation: q.explanation
  });

  // Highlight choices
  q.options.forEach((_, idx) => {
    const btn = document.getElementById(`opt-btn-${idx}`);
    const icon = document.getElementById(`opt-icon-${idx}`);
    btn.disabled = true;

    if (idx === q.answerIndex) {
      btn.className = 'w-full text-left p-4 rounded-2xl border-2 border-emerald-500 bg-emerald-50 text-emerald-900 font-bold transition-all text-sm flex items-center justify-between';
      icon.className = 'w-5 h-5 rounded-full bg-emerald-600 text-white flex items-center justify-center text-xs font-bold';
      icon.innerHTML = '✓';
    } else if (idx === index && !isCorrect) {
      btn.className = 'w-full text-left p-4 rounded-2xl border-2 border-rose-500 bg-rose-50 text-rose-900 font-bold transition-all text-sm flex items-center justify-between';
      icon.className = 'w-5 h-5 rounded-full bg-rose-600 text-white flex items-center justify-center text-xs font-bold';
      icon.innerHTML = '✕';
    } else {
      btn.className = 'w-full text-left p-4 rounded-2xl border border-slate-200 bg-slate-50 text-slate-400 opacity-60 text-sm flex items-center justify-between';
    }
  });

  // Show explanation
  const expBox = document.getElementById('quiz-explanation-box');
  const expText = document.getElementById('quiz-explanation-text');
  expText.textContent = q.explanation || "To'g'ri javob darslik qoidalariga muvofiq belgilangan.";
  expBox.classList.remove('hidden');

  // Enable Next button
  const nextBtn = document.getElementById('quiz-next-btn');
  nextBtn.disabled = false;
  if (state.quiz.currentIndex === state.quiz.questions.length - 1) {
    nextBtn.innerHTML = 'Natijalarni ko\'rish <i data-lucide="award" class="w-4 h-4"></i>';
  } else {
    nextBtn.innerHTML = 'Keyingi savol <i data-lucide="chevron-right" class="w-4 h-4"></i>';
  }
  if (window.lucide) window.lucide.createIcons();
}

function handleNextQuestion() {
  if (state.quiz.currentIndex < state.quiz.questions.length - 1) {
    state.quiz.currentIndex++;
    renderCurrentQuestion();
  } else {
    finishQuiz();
  }
}

async function finishQuiz() {
  if (state.quiz.timerInterval) clearInterval(state.quiz.timerInterval);

  const total = state.quiz.questions.length;
  const score = state.quiz.score;
  const percent = Math.round((score / total) * 100);

  let gradeBadge = "Qoniqarsiz (2)";
  let gradeColor = "text-rose-600 bg-rose-50 border-rose-200";
  if (percent >= 85) {
    gradeBadge = "A'lo (5)";
    gradeColor = "text-emerald-600 bg-emerald-50 border-emerald-200";
  } else if (percent >= 70) {
    gradeBadge = "Yaxshi (4)";
    gradeColor = "text-blue-600 bg-blue-50 border-blue-200";
  } else if (percent >= 50) {
    gradeBadge = "Qoniqarli (3)";
    gradeColor = "text-amber-600 bg-amber-50 border-amber-200";
  }

  // Hide quiz, show results
  document.getElementById('quiz-view').classList.add('hidden');
  const resultView = document.getElementById('quiz-result-view');
  resultView.classList.remove('hidden');

  document.getElementById('result-score-text').textContent = `${score} / ${total}`;
  document.getElementById('result-percent-text').textContent = `${percent}%`;
  
  const badgeEl = document.getElementById('result-grade-badge');
  badgeEl.className = `px-4 py-1 rounded-full text-sm font-bold border ${gradeColor}`;
  badgeEl.textContent = gradeBadge;

  // Automatically submit results to backend (Teacher Cabinet)
  try {
    await fetch('/api/submissions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        studentName: state.studentProfile.fullName,
        studentClass: state.studentProfile.classGrade,
        school: state.studentProfile.school,
        subject: state.quiz.subject,
        topic: state.quiz.topic,
        difficulty: state.quiz.difficulty,
        score: score,
        total: total,
        timeSpentSeconds: state.quiz.timeSpentSeconds,
        answers: state.quiz.answers
      })
    });
    console.log("Natijalar o'qituvchi kabinetiga muvaffaqiyatli topshirildi.");
  } catch (err) {
    console.warn("Natijani saqlashda xatolik:", err);
  }
}

function exitQuiz() {
  if (state.quiz.timerInterval) clearInterval(state.quiz.timerInterval);
  state.quiz.inProgress = false;
  document.getElementById('quiz-view').classList.add('hidden');
  document.getElementById('quiz-result-view').classList.add('hidden');
  document.getElementById('preset-tests-container').classList.remove('hidden');
}

function renderSubjectPresetTests() {
  const container = document.getElementById('preset-tests-list');
  if (!container || !window.APP_DATA) return;

  const presets = window.APP_DATA.INITIAL_PRESET_TESTS.filter(t => 
    t.subject.toLowerCase() === state.currentSubject.toLowerCase()
  );

  if (presets.length === 0) {
    container.innerHTML = `
      <div class="col-span-full py-8 text-center text-slate-400 text-xs">
        Ushbu fan uchun tayyor testlar hozircha yo'q. Quyidagi tugma orqali AI bilan generatsiya qilishingiz mumkin.
      </div>
    `;
    return;
  }

  container.innerHTML = presets.map(pt => `
    <div class="p-4 bg-white rounded-2xl border border-slate-200 hover:border-emerald-400 hover:shadow-xs transition-all flex items-center justify-between">
      <div>
        <h4 class="text-sm font-bold text-slate-800 mb-1">${pt.title}</h4>
        <div class="flex items-center gap-2 text-xs text-slate-400">
          <span>${pt.topic}</span> • <span>${pt.difficulty}</span> • <span>${pt.questions.length} ta savol</span>
        </div>
      </div>
      <button onclick="startPresetTest('${pt.id}')" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-700 text-white transition-colors">
        Boshlash
      </button>
    </div>
  `).join('');
}

function startPresetTest(testId) {
  const test = window.APP_DATA.INITIAL_PRESET_TESTS.find(t => t.id === testId);
  if (!test) return;

  document.getElementById('preset-tests-container').classList.add('hidden');
  const quizContainer = document.getElementById('quiz-view');
  quizContainer.classList.remove('hidden');

  state.quiz = {
    inProgress: true,
    subject: test.subject,
    topic: test.title,
    difficulty: test.difficulty,
    questions: test.questions,
    currentIndex: 0,
    selectedOption: null,
    isAnswered: false,
    score: 0,
    answers: [],
    startTime: Date.now(),
    timeSpentSeconds: 0,
    timerInterval: null
  };

  startQuizTimer();
  renderCurrentQuestion();
}

// -------------------------------------------------------------
// AI Tutor Chat
// -------------------------------------------------------------
function renderTutorMessages() {
  const container = document.getElementById('tutor-messages-container');
  if (!container) return;

  container.innerHTML = state.tutorMessages.map(msg => {
    const isUser = msg.role === 'user';
    return `
      <div class="flex ${isUser ? 'justify-end' : 'justify-start'} mb-3">
        <div class="max-w-[80%] p-3.5 rounded-2xl text-xs leading-relaxed ${
          isUser 
            ? 'bg-emerald-600 text-white rounded-br-none shadow-xs' 
            : 'bg-white text-slate-800 border border-slate-200/90 rounded-bl-none shadow-xs'
        }">
          ${msg.text}
        </div>
      </div>
    `;
  }).join('');

  container.scrollTop = container.scrollHeight;
}

async function sendTutorMessage() {
  const input = document.getElementById('tutor-input');
  const message = input.value.trim();
  if (!message) return;

  input.value = '';
  state.tutorMessages.push({ role: 'user', text: message });
  renderTutorMessages();

  const lessonTitle = state.activeLesson ? state.activeLesson.title : 'Umumiy Biologiya';
  const lessonContent = state.activeLesson ? state.activeLesson.content : '';

  try {
    const res = await fetch('/api/tutor-chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: message,
        lessonTitle: lessonTitle,
        lessonContent: lessonContent,
        classId: state.selectedClassId,
        chatHistory: state.tutorMessages.slice(-6)
      })
    });

    const data = await res.json();
    state.tutorMessages.push({ role: 'model', text: data.reply || 'Javob olishda xatolik bo\'ldi.' });
  } catch (err) {
    state.tutorMessages.push({ role: 'model', text: 'Tarmoq xatosi. Iltimos qayta urinib ko\'ring.' });
  }

  renderTutorMessages();
}

// -------------------------------------------------------------
// AI Glossary / Term Lookup
// -------------------------------------------------------------
function renderGlossary() {
  const container = document.getElementById('glossary-grid');
  if (!container) return;

  container.innerHTML = state.glossary.map(item => `
    <div class="p-5 bg-white rounded-2xl border border-slate-200/90 shadow-xs hover:border-emerald-300 transition-all">
      <div class="flex items-center justify-between mb-2">
        <h4 class="text-base font-bold text-slate-800">${item.term}</h4>
        <span class="text-xs text-slate-400 italic">${item.origin || ''}</span>
      </div>
      <p class="text-xs text-slate-600 mb-3 leading-relaxed">${item.definition}</p>
      ${item.analogy ? `
        <div class="p-3 bg-amber-50 rounded-xl border border-amber-100 text-xs text-amber-900 mb-2">
          <strong>Analogiya:</strong> ${item.analogy}
        </div>
      ` : ''}
      ${item.examFocus ? `
        <div class="p-3 bg-emerald-50 rounded-xl border border-emerald-100 text-xs text-emerald-900">
          <strong>Imtihon Diqqat Markazi:</strong> ${item.examFocus}
        </div>
      ` : ''}
    </div>
  `).join('');
}

async function lookupTerm() {
  const input = document.getElementById('glossary-search-input');
  const term = input.value.trim();
  if (!term) return;

  const btn = document.getElementById('glossary-search-btn');
  btn.disabled = true;
  btn.textContent = 'Qidirilmoqda...';

  try {
    const res = await fetch('/api/explain-term', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ term })
    });

    const data = await res.json();
    if (data.term) {
      state.glossary.unshift(data);
      localStorage.setItem('biologiya_glossary_v1', JSON.stringify(state.glossary));
      renderGlossary();
      input.value = '';
    }
  } catch (err) {
    alert("Termin ma'lumotlarini olishda xatolik yuz berdi.");
  } finally {
    btn.disabled = false;
    btn.textContent = 'Qidirish';
  }
}

// -------------------------------------------------------------
// Interactive SVG Diagram Viewer
// -------------------------------------------------------------
async function loadLessonDiagram(title, topic, content) {
  const container = document.getElementById('diagram-container');
  const hotspotsContainer = document.getElementById('diagram-hotspots-info');
  if (!container) return;

  container.innerHTML = '<div class="py-12 text-center text-slate-400">Diagramma yuklanmoqda...</div>';

  try {
    const res = await fetch('/api/generate-illustration', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, topic, content })
    });

    const data = await res.json();
    container.innerHTML = data.svg || '<p>Diagramma mavjud emas</p>';

    if (data.points && hotspotsContainer) {
      hotspotsContainer.innerHTML = data.points.map(pt => `
        <div class="p-3 bg-white rounded-xl border border-slate-200 text-xs shadow-xs">
          <span class="font-bold text-emerald-800">${pt.name}:</span>
          <p class="text-slate-600 mt-0.5">${pt.desc}</p>
        </div>
      `).join('');
    }
  } catch (err) {
    container.innerHTML = '<p class="text-xs text-rose-500">Diagrammani yuklashda xatolik.</p>';
  }
}

// -------------------------------------------------------------
// Teacher Cabinet & PIN Authorization
// -------------------------------------------------------------
function checkTeacherAuthorization() {
  const pinModal = document.getElementById('teacher-pin-modal');
  const dashboard = document.getElementById('teacher-dashboard-view');

  if (state.teacherProfile.isAuthorized) {
    pinModal.classList.add('hidden');
    dashboard.classList.remove('hidden');
    loadTeacherSubmissions();
    loadTeacherTests();
  } else {
    pinModal.classList.remove('hidden');
    dashboard.classList.add('hidden');
  }
}

async function verifyTeacherPin() {
  const pinInput = document.getElementById('teacher-pin-input');
  const pin = pinInput.value.trim();
  const errorEl = document.getElementById('teacher-pin-error');

  try {
    const res = await fetch('/api/teacher/verify-pin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pin })
    });

    const data = await res.json();
    if (data.authorized) {
      state.teacherProfile.isAuthorized = true;
      state.currentRole = 'teacher';
      localStorage.setItem('user_role', 'teacher');
      localStorage.setItem('teacher_profile', JSON.stringify(state.teacherProfile));
      updateRoleBadge();
      checkTeacherAuthorization();
    } else {
      errorEl.textContent = data.error || 'PIN kod xato!';
      errorEl.classList.remove('hidden');
    }
  } catch (err) {
    errorEl.textContent = 'Tarmoq xatosi yoki noto\'g\'ri PIN!';
    errorEl.classList.remove('hidden');
  }
}

async function loadTeacherSubmissions() {
  const tableBody = document.getElementById('teacher-submissions-tbody');
  if (!tableBody) return;

  try {
    const res = await fetch('/api/submissions');
    const data = await res.json();
    state.submissions = data.submissions || [];

    if (state.submissions.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="6" class="text-center py-8 text-slate-400 text-xs">O'quvchilar natijalari hozircha yo'q</td>
        </tr>
      `;
      return;
    }

    tableBody.innerHTML = state.submissions.map(sub => `
      <tr class="border-b border-slate-100 hover:bg-slate-50/80 text-xs text-slate-700">
        <td class="p-3 font-semibold">${sub.studentName}</td>
        <td class="p-3 text-slate-500">${sub.studentClass}</td>
        <td class="p-3">${sub.subject} - ${sub.topic}</td>
        <td class="p-3 font-bold">${sub.score}/${sub.total} (${sub.percentage}%)</td>
        <td class="p-3">
          <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${
            sub.percentage >= 85 ? 'bg-emerald-100 text-emerald-800' :
            sub.percentage >= 70 ? 'bg-blue-100 text-blue-800' :
            sub.percentage >= 50 ? 'bg-amber-100 text-amber-800' :
            'bg-rose-100 text-rose-800'
          }">${sub.gradeBadge}</span>
        </td>
        <td class="p-3 text-right">
          <button onclick="promptFeedback('${sub.id}')" class="px-2 py-1 bg-slate-100 hover:bg-slate-200 rounded text-slate-700 text-xs font-semibold mr-1">
            Fikr yozish
          </button>
          <button onclick="deleteSubmission('${sub.id}')" class="px-2 py-1 bg-rose-50 hover:bg-rose-100 text-rose-600 rounded text-xs font-semibold">
            O'chirish
          </button>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Submissions load error:', err);
  }
}

async function promptFeedback(subId) {
  const feedback = prompt("O'quvchiga izoh yoki tavsiya yozing:");
  if (feedback === null) return;

  try {
    await fetch(`/api/submissions/${subId}/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ feedback })
    });
    alert("Izoh saqlandi!");
    loadTeacherSubmissions();
  } catch (err) {
    alert("Izohni saqlashda xatolik yuz berdi.");
  }
}

async function deleteSubmission(subId) {
  if (!confirm("Haqiqatan ham ushbu natijani o'chirmoqchimisiz?")) return;

  try {
    await fetch(`/api/submissions/${subId}`, { method: 'DELETE' });
    loadTeacherSubmissions();
  } catch (err) {
    alert("O'chirishda xatolik yuz berdi.");
  }
}

async function loadTeacherTests() {
  const container = document.getElementById('teacher-leveled-tests-list');
  if (!container) return;

  try {
    const res = await fetch('/api/teacher-tests');
    const data = await res.json();
    state.teacherTests = data.tests || [];

    container.innerHTML = state.teacherTests.map(test => `
      <div class="p-4 bg-white rounded-2xl border border-slate-200/90 shadow-xs mb-3">
        <div class="flex items-center justify-between mb-2">
          <h4 class="text-sm font-bold text-slate-800">${test.subject}: ${test.topic}</h4>
          <span class="text-xs text-slate-400">${test.classGrade}</span>
        </div>
        <p class="text-xs text-slate-500 mb-3">${test.description || '3 bosqichli tabaqalangan bilim sinovi'}</p>
        <div class="flex items-center gap-2">
          <span class="px-2.5 py-0.5 rounded text-xs bg-emerald-50 text-emerald-700 font-semibold">1-bosqich: Oson</span>
          <span class="px-2.5 py-0.5 rounded text-xs bg-blue-50 text-blue-700 font-semibold">2-bosqich: O'rtacha</span>
          <span class="px-2.5 py-0.5 rounded text-xs bg-purple-50 text-purple-700 font-semibold">3-bosqich: Qiyin (DTM)</span>
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error('Teacher tests load error:', err);
  }
}

// -------------------------------------------------------------
// Role Switch & Profile Modal
// -------------------------------------------------------------
function toggleRole() {
  if (state.currentRole === 'student') {
    state.currentRole = 'teacher';
    localStorage.setItem('user_role', 'teacher');
    switchTab('teacher');
  } else {
    state.currentRole = 'student';
    localStorage.setItem('user_role', 'student');
    switchTab('syllabus');
  }
  updateRoleBadge();
}

function setupEventListeners() {
  // Search in syllabus
  const searchInput = document.getElementById('syllabus-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      state.syllabusSearch = e.target.value.trim();
      renderLessonsList();
    });
  }

  // Tutor input enter key
  const tutorInput = document.getElementById('tutor-input');
  if (tutorInput) {
    tutorInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') sendTutorMessage();
    });
  }
}
