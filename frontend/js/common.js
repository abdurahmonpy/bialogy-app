/**
 * Biologiya & Fanlar Test Bot - Shared Common Utilities with Left Sidebar
 */

// Streak Badges System (As in original app)
const STREAK_BADGES = [
  {
    id: 'badge-1',
    name: "Biologik Start",
    daysRequired: 1,
    badgeLevel: "1 kunlik streak",
    description: "Birinchi darsni muvaffaqiyatli o'zlashtirgan biolog",
    icon: "sprout",
    category: "Boshlang'ich",
    color: "from-emerald-500 to-green-600"
  },
  {
    id: 'badge-2',
    name: "Olovli Ishtiyoq",
    daysRequired: 3,
    badgeLevel: "3 kunlik streak",
    description: "Ketma-ket 3 kun dars o'qib test topshirgan iqtidor",
    icon: "flame",
    category: "Boshlang'ich",
    color: "from-amber-500 to-orange-600"
  },
  {
    id: 'badge-3',
    name: "Yashin Tezligi",
    daysRequired: 7,
    badgeLevel: "7 kunlik streak",
    description: "Bir hafta davomida to'xtovsiz bilim olgan abituriyent",
    icon: "zap",
    category: "O'rta",
    color: "from-blue-500 to-indigo-600"
  },
  {
    id: 'badge-4',
    name: "Olimpiada Chempioni",
    daysRequired: 14,
    badgeLevel: "14 kunlik streak",
    description: "2 hafta tinimsiz mustahkam natija ko'rsatgan bilimdon",
    icon: "trophy",
    category: "O'rta",
    color: "from-purple-500 to-pink-600"
  },
  {
    id: 'badge-5',
    name: "DNK Ustasi",
    daysRequired: 30,
    badgeLevel: "30 kunlik streak",
    description: "Bir oy mobaynida barcha sinf darsliklarini zabt etgan ekspert",
    icon: "dna",
    category: "Professional",
    color: "from-teal-500 to-cyan-600"
  },
  {
    id: 'badge-6',
    name: "Biologiya Qiroli",
    daysRequired: 60,
    badgeLevel: "60 kunlik streak",
    description: "Oliy toifali natijaga erishgan chinakam chempion",
    icon: "crown",
    category: "Professional",
    color: "from-yellow-500 to-amber-600"
  }
];

function getStudentProfile() {
  try {
    const saved = localStorage.getItem('student_profile');
    return saved ? JSON.parse(saved) : {
      id: 'stud-1',
      fullName: 'Jasurbek Aliyev',
      classGrade: '8-A sinf',
      school: "14-sonli umumiy o'rta ta'lim maktabi",
      streakDays: 4
    };
  } catch {
    return { id: 'stud-1', fullName: 'Jasurbek Aliyev', classGrade: '8-A sinf', school: "14-maktab", streakDays: 4 };
  }
}

function saveStudentProfile(profile) {
  localStorage.setItem('student_profile', JSON.stringify(profile));
}

function getTeacherProfile() {
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
}

function saveTeacherProfile(profile) {
  localStorage.setItem('teacher_profile', JSON.stringify(profile));
}

// Render dynamic Left Sidebar Navigation
function renderCommonNavbar(activePage) {
  const navContainer = document.getElementById('common-navbar');
  if (!navContainer) return;

  const student = getStudentProfile();
  const isTeacherAuth = getTeacherProfile().isAuthorized;

  const links = [
    { id: 'home', label: 'Bosh Sahifa', href: '/', icon: 'book-open' },
    { id: 'student', label: 'O\'quvchi Kabineti', href: '/student.html', icon: 'graduation-cap' },
    { id: 'test', label: 'Test Markazi', href: '/test.html', icon: 'award' },
    { id: 'leveled', label: '3 Bosqichli Test', href: '/leveled-test.html', icon: 'target' },
    { id: 'tutor', label: 'AI Repetitor', href: '/tutor.html', icon: 'message-square' },
    { id: 'glossary', label: 'Terminlar Lug\'ati', href: '/glossary.html', icon: 'book-marked' },
    { id: 'diagram', label: 'Diagramma', href: '/diagram.html', icon: 'sparkles' },
    { id: 'cabinet', label: 'O\'qituvchi Kabineti', href: '/cabinet.html', icon: 'shield-check' }
  ];

  navContainer.innerHTML = `
    <!-- Mobile Top Header Bar (Only visible on small screens) -->
    <div class="md:hidden sticky top-0 z-40 bg-white border-b border-slate-200 px-4 py-3 flex items-center justify-between shadow-2xs">
      <a href="/" class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white">
          <i data-lucide="dna" class="w-5 h-5"></i>
        </div>
        <span class="font-extrabold text-slate-900 text-sm">Biologiya Bot</span>
      </a>

      <div class="flex items-center gap-2">
        <div class="flex items-center gap-1 px-2.5 py-1 rounded-full bg-amber-50 text-amber-800 text-[11px] font-bold border border-amber-200">
          <i data-lucide="flame" class="w-3.5 h-3.5 text-amber-500 fill-amber-500"></i>
          <span>${student.streakDays || 4}d</span>
        </div>
        <button onclick="toggleMobileSidebar()" class="p-2 rounded-xl text-slate-600 hover:bg-slate-100">
          <i data-lucide="menu" class="w-5 h-5"></i>
        </button>
      </div>
    </div>

    <!-- Left Sidebar (Desktop Fixed / Mobile Slide-over) -->
    <aside id="left-sidebar" class="hidden md:flex flex-col w-64 lg:w-72 bg-white border-r border-slate-200/90 h-screen sticky top-0 shrink-0 overflow-y-auto p-4 justify-between z-50">
      
      <!-- Top Brand & Navigation -->
      <div class="space-y-6">
        <!-- Logo & Header -->
        <a href="/" class="flex items-center gap-3 px-2 py-1.5 hover:opacity-90 transition-opacity">
          <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white shadow-xs">
            <i data-lucide="dna" class="w-6 h-6"></i>
          </div>
          <div>
            <div class="flex items-center gap-1.5">
              <span class="text-base font-extrabold text-slate-900 tracking-tight">Biologiya Bot</span>
              <span class="px-1.5 py-0.5 text-[9px] font-black rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">AI 2.0</span>
            </div>
            <p class="text-[10px] text-slate-400 font-medium leading-tight">Milliy darsliklar platformasi</p>
          </div>
        </a>

        <!-- Navigation Links Menu (Chap tomondagi asosiy menyu) -->
        <div class="space-y-1">
          <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 px-3 block mb-2">Asosiy Menyu</span>
          ${links.map(l => {
            const isActive = l.id === activePage;
            const activeStyle = isActive
              ? 'bg-emerald-600 text-white font-bold shadow-xs'
              : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900 font-semibold';

            return `
              <a href="${l.href}" class="flex items-center gap-3 px-3.5 py-2.5 rounded-2xl text-xs transition-all ${activeStyle}">
                <i data-lucide="${l.icon}" class="w-4 h-4"></i>
                <span>${l.label}</span>
              </a>
            `;
          }).join('')}
        </div>
      </div>

      <!-- Bottom User Profile & Streak Widget -->
      <div class="space-y-3 pt-4 border-t border-slate-100">
        <!-- Streak Card -->
        <div class="p-3.5 bg-gradient-to-br from-amber-50 to-orange-50/70 rounded-2xl border border-amber-200/80">
          <div class="flex items-center gap-2 mb-1">
            <i data-lucide="flame" class="w-4 h-4 text-amber-500 fill-amber-500"></i>
            <span class="text-xs font-black text-amber-950">${student.streakDays || 4} kunlik streak! 🔥</span>
          </div>
          <p class="text-[10px] text-amber-800/80 leading-relaxed font-medium">
            Har kuni test ishlab yangi nishon va darajalarni oching
          </p>
        </div>

        <!-- User Profile Card -->
        <a href="/student.html" class="p-3 bg-slate-50 hover:bg-slate-100/90 rounded-2xl border border-slate-200/90 flex items-center justify-between transition-colors">
          <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center font-black text-xs">
              ${student.fullName ? student.fullName[0] : 'J'}
            </div>
            <div class="leading-tight">
              <h4 class="text-xs font-bold text-slate-900">${student.fullName}</h4>
              <span class="text-[10px] text-slate-400 font-semibold">${student.classGrade}</span>
            </div>
          </div>
          <i data-lucide="chevron-right" class="w-4 h-4 text-slate-400"></i>
        </a>
      </div>

    </aside>

    <!-- Mobile Slideover Backdrop & Menu -->
    <div id="mobile-sidebar-backdrop" class="hidden fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs md:hidden" onclick="toggleMobileSidebar()">
      <div class="w-64 bg-white h-full p-4 flex flex-col justify-between" onclick="event.stopPropagation()">
        <div class="space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-100">
            <span class="font-extrabold text-slate-900 text-sm">Menyu</span>
            <button onclick="toggleMobileSidebar()" class="p-1.5 text-slate-400">✕</button>
          </div>
          <div class="space-y-1">
            ${links.map(l => `
              <a href="${l.href}" class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold ${l.id === activePage ? 'bg-emerald-600 text-white font-bold' : 'text-slate-700 hover:bg-slate-100'}">
                <i data-lucide="${l.icon}" class="w-4 h-4"></i>
                <span>${l.label}</span>
              </a>
            `).join('')}
          </div>
        </div>
      </div>
    </div>
  `;

  if (window.lucide) window.lucide.createIcons();
}

function toggleMobileSidebar() {
  const backdrop = document.getElementById('mobile-sidebar-backdrop');
  if (backdrop) {
    backdrop.classList.toggle('hidden');
  }
}

// Render dynamic footer
function renderCommonFooter() {
  const footerContainer = document.getElementById('common-footer');
  if (!footerContainer) return;

  footerContainer.innerHTML = `
    <footer class="bg-white border-t border-slate-200 mt-12 py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-400">
        <div class="flex items-center gap-2">
          <div class="w-5 h-5 rounded bg-emerald-600 flex items-center justify-center text-white">
            <i data-lucide="dna" class="w-3 h-3"></i>
          </div>
          <span class="font-bold text-slate-700">Biologiya & Fanlar Test Bot</span>
          <span>© 2026 Maktab darsliklari va DTM test bazasi</span>
        </div>
        <div class="flex items-center gap-4 text-[11px] font-medium">
          <a href="/test.html" class="hover:text-emerald-600 transition-colors">Test markazi</a>
          <a href="/leveled-test.html" class="hover:text-emerald-600 transition-colors">3 Bosqichli sinov</a>
          <a href="/tutor.html" class="hover:text-emerald-600 transition-colors">AI Repetitor</a>
          <a href="/cabinet.html" class="hover:text-emerald-600 transition-colors">O'qituvchi</a>
        </div>
      </div>
    </footer>
  `;
  if (window.lucide) window.lucide.createIcons();
}
