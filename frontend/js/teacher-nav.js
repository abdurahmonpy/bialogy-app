// Teacher Navigation Sidebar Component
(function() {
  const currentPath = window.location.pathname.replace(/\/$/, "");
  
  const menuItems = [
    { label: "Bosh sahifa", path: "/teacher/index.html", cleanPath: "/teacher", icon: "layout-dashboard" },
    { label: "Chat", path: "/teacher/chat.html", cleanPath: "/teacher/chat", icon: "message-circle" },
    { label: "Guruhlarim", path: "/teacher/groups.html", cleanPath: "/teacher/groups", icon: "users" },
    {
      label: "Uyga vazifa",
      icon: "clipboard-list",
      subItems: [
        { label: "Uyga vazifa berish", path: "/teacher/homework.html", cleanPath: "/teacher/homework", icon: "plus-circle" },
        { label: "Baholash", path: "/teacher/homework-grade.html", cleanPath: "/teacher/homework-grade", icon: "check-circle" },
        { label: "Statistika qismi", path: "/teacher/homework-stats.html", cleanPath: "/teacher/homework-stats", icon: "bar-chart-2" }
      ]
    },
    { label: "Resurslar", path: "/teacher/resources.html", cleanPath: "/teacher/resources", icon: "book-open" },
    { label: "O'quvchilar", path: "/teacher/students.html", cleanPath: "/teacher/students", icon: "graduation-cap" },
    { label: "Test Markaz", path: "/teacher/test.html", cleanPath: "/teacher/test", icon: "file-check" },
    { label: "Statistika", path: "/teacher/stats.html", cleanPath: "/teacher/stats", icon: "bar-chart-3" },
    { label: "AI Yordamchi", path: "/teacher/ai-assistant.html?v=3.0", cleanPath: "/teacher/ai-assistant", icon: "sparkles" },
    { label: "O'quvchi qo'shish", path: "/teacher/add-student.html", cleanPath: "/teacher/add-student", icon: "user-plus" }
  ];

  function renderNavItems(activeKey = "", isMobile = false) {
    const prefix = isMobile ? "mobile-" : "";
    return menuItems.map(item => {
      if (item.subItems) {
        const isAnySubActive = item.subItems.some(sub => 
          (activeKey && activeKey.toLowerCase() === sub.label.toLowerCase()) ||
          currentPath === sub.cleanPath || currentPath === sub.path
        );

        return `
          <div class="space-y-1">
            <button type="button" onclick="window.toggleHwMenu()" 
              class="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl transition-all duration-200 cursor-pointer ${isAnySubActive ? 'bg-indigo-50 text-indigo-700 font-semibold' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900 font-medium'}">
              <div class="flex items-center gap-3.5 min-w-0">
                <i data-lucide="${item.icon}" class="w-5 h-5 flex-shrink-0 ${isAnySubActive ? 'text-indigo-600' : ''}"></i>
                <span class="text-sm tracking-wide truncate">${item.label}</span>
              </div>
              <i data-lucide="chevron-down" id="${prefix}hw-chevron" class="w-4 h-4 text-slate-400 transition-transform duration-200 ${isAnySubActive ? 'rotate-180 text-indigo-600' : ''}"></i>
            </button>
            <div id="${prefix}hw-submenu" class="pl-6 pr-1 space-y-1 ${isAnySubActive ? '' : 'hidden'}">
              ${item.subItems.map(sub => {
                const isSubActive = (activeKey && activeKey.toLowerCase() === sub.label.toLowerCase()) ||
                  currentPath === sub.cleanPath || currentPath === sub.path;
                return `
                  <a href="${sub.path}" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs transition ${isSubActive ? 'bg-indigo-600 text-white font-bold shadow-sm' : 'text-slate-500 hover:text-indigo-600 hover:bg-slate-50 font-medium'}">
                    <i data-lucide="${sub.icon}" class="w-3.5 h-3.5 flex-shrink-0"></i>
                    <span class="truncate">${sub.label}</span>
                  </a>
                `;
              }).join("")}
            </div>
          </div>
        `;
      }

      const isActive = activeKey 
        ? item.label.toLowerCase() === activeKey.toLowerCase()
        : (currentPath === item.cleanPath || currentPath === item.path || (item.cleanPath === "/teacher" && (currentPath === "" || currentPath === "/teacher")));

      const activeClasses = isActive
        ? "bg-indigo-600 text-white shadow-md shadow-indigo-500/20 font-semibold"
        : "text-slate-600 hover:bg-slate-100 hover:text-slate-900 font-medium";

      return `
        <a href="${item.path}" class="flex items-center gap-3.5 px-3.5 py-2.5 rounded-xl transition-all duration-200 ${activeClasses}">
          <i data-lucide="${item.icon}" class="w-5 h-5 flex-shrink-0"></i>
          <span class="text-sm tracking-wide truncate">${item.label}</span>
          ${isActive ? `<span class="ml-auto w-1.5 h-4 rounded-full bg-white flex-shrink-0"></span>` : ""}
        </a>
      `;
    }).join("");
  }

  window.toggleHwMenu = function() {
    ['', 'mobile-'].forEach(prefix => {
      const sub = document.getElementById(`${prefix}hw-submenu`);
      const chev = document.getElementById(`${prefix}hw-chevron`);
      if (sub) {
        const isHidden = sub.classList.contains("hidden");
        if (isHidden) {
          sub.classList.remove("hidden");
          if (chev) chev.classList.add("rotate-180");
        } else {
          sub.classList.add("hidden");
          if (chev) chev.classList.remove("rotate-180");
        }
      }
    });
    if (window.lucide) window.lucide.createIcons();
  };

  // Inject mobile bottom padding style globally
  if (!document.getElementById("bioedu-teacher-bottom-style")) {
    const style = document.createElement("style");
    style.id = "bioedu-teacher-bottom-style";
    style.textContent = `
      @media (max-width: 1023px) {
        body {
          padding-bottom: 74px !important;
        }
      }
    `;
    document.head.appendChild(style);
  }

  // Teacher Core Bottom Bar Destinations (Asosiy -> Guruhlar -> Testlar (Markaz) -> Vazifalar -> Yana)
  const teacherBottomItems = [
    { label: "Bosh sahifa", shortLabel: "Asosiy", path: "/teacher/index.html", cleanPath: "/teacher", icon: "layout-dashboard" },
    { label: "Guruhlarim", shortLabel: "Guruhlar", path: "/teacher/groups.html", cleanPath: "/teacher/groups", icon: "users" },
    { label: "Test Markaz", shortLabel: "Testlar", path: "/teacher/test.html", cleanPath: "/teacher/test", icon: "file-check", isCenter: true },
    { label: "Uyga vazifa", shortLabel: "Vazifalar", path: "/teacher/homework.html", cleanPath: "/teacher/homework", icon: "clipboard-list" }
  ];

  // Secondary items in the "Yana" (More) Bottom Sheet
  const teacherMoreItems = [
    { label: "AI Yordamchi", path: "/teacher/ai-assistant.html?v=3.0", cleanPath: "/teacher/ai-assistant", icon: "sparkles", bg: "bg-purple-50 text-purple-600 border-purple-200", desc: "Dars & test generatori" },
    { label: "Chat", path: "/teacher/chat.html", cleanPath: "/teacher/chat", icon: "message-circle", bg: "bg-blue-50 text-blue-600 border-blue-200", desc: "Xabarlar & muloqot" },
    { label: "Resurslar", path: "/teacher/resources.html", cleanPath: "/teacher/resources", icon: "book-open", bg: "bg-emerald-50 text-emerald-600 border-emerald-200", desc: "Kitoblar & darsliklar" },
    { label: "O'quvchilar", path: "/teacher/students.html", cleanPath: "/teacher/students", icon: "graduation-cap", bg: "bg-amber-50 text-amber-600 border-amber-200", desc: "O'quvchilar ro'yxati" },
    { label: "Statistika", path: "/teacher/stats.html", cleanPath: "/teacher/stats", icon: "bar-chart-3", bg: "bg-cyan-50 text-cyan-600 border-cyan-200", desc: "Umumiy ko'rsatkichlar" },
    { label: "O'quvchi qo'shish", path: "/teacher/add-student.html", cleanPath: "/teacher/add-student", icon: "user-plus", bg: "bg-teal-50 text-teal-600 border-teal-200", desc: "Yangi akkaunt yaratish" },
    { label: "Topshiriqni Baholash", path: "/teacher/homework-grade.html", cleanPath: "/teacher/homework-grade", icon: "check-circle", bg: "bg-indigo-50 text-indigo-600 border-indigo-200", desc: "Vazifalarni tekshirish" },
    { label: "Topshiriq Statistikasi", path: "/teacher/homework-stats.html", cleanPath: "/teacher/homework-stats", icon: "bar-chart-2", bg: "bg-rose-50 text-rose-600 border-rose-200", desc: "Topshirish hisoboti" }
  ];

  window.renderTeacherSidebar = function(activeKey = "") {
    const user = (window.Auth && window.Auth.getCurrentUser()) || { fullName: "O'qituvchi", subject: "Biologiya fani", avatar: "O" };

    const navLinksHtml = renderNavItems(activeKey, false);

    // Is any "More" item currently active?
    const isMoreActive = teacherMoreItems.some(item => 
      (activeKey && activeKey.toLowerCase() === item.label.toLowerCase()) ||
      currentPath === item.cleanPath || currentPath === item.path
    );

    // Build bottom navigation bar HTML
    const bottomNavHtml = teacherBottomItems.map(item => {
      const isActive = activeKey 
        ? (item.label.toLowerCase() === activeKey.toLowerCase() || item.shortLabel.toLowerCase() === activeKey.toLowerCase())
        : (currentPath === item.cleanPath || currentPath === item.path || (item.cleanPath === "/teacher" && (currentPath === "" || currentPath === "/teacher")));

      if (item.isCenter) {
        return `
          <a href="${item.path}" class="flex flex-col items-center justify-center flex-1 py-1 transition-transform active:scale-95 select-none ${isActive ? 'text-indigo-600' : 'text-slate-500'}">
            <div class="relative flex items-center justify-center w-11 h-11 -mt-4 rounded-full ${isActive ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/35 ring-4 ring-white' : 'bg-gradient-to-tr from-indigo-600 to-purple-600 text-white shadow-md shadow-indigo-500/25 ring-4 ring-white'} transition-all">
              <i data-lucide="${item.icon}" class="w-5 h-5"></i>
            </div>
            <span class="text-[10px] ${isActive ? 'font-black text-indigo-600' : 'font-bold text-slate-600'} tracking-tight mt-0.5">${item.shortLabel}</span>
          </a>
        `;
      }

      const activeClasses = isActive
        ? "text-indigo-600 font-extrabold"
        : "text-slate-400 hover:text-slate-600 font-semibold";

      const iconPill = isActive
        ? "bg-indigo-50 text-indigo-600"
        : "text-slate-400";

      return `
        <a href="${item.path}" class="flex flex-col items-center justify-center flex-1 py-1 transition-transform active:scale-90 select-none ${activeClasses}">
          <div class="relative flex items-center justify-center px-2.5 py-1 rounded-full ${iconPill} transition-all">
            <i data-lucide="${item.icon}" class="w-5 h-5"></i>
          </div>
          <span class="text-[10px] tracking-tight mt-0.5 leading-none">${item.shortLabel}</span>
        </a>
      `;
    }).join("");

    // Add 5th "Yana" button
    const moreBtnHtml = `
      <button type="button" onclick="window.openTeacherMoreSheet()" 
        class="flex flex-col items-center justify-center flex-1 py-1 transition-transform active:scale-90 select-none cursor-pointer ${isMoreActive ? 'text-indigo-600 font-extrabold' : 'text-slate-400 hover:text-slate-600 font-semibold'}">
        <div class="relative flex items-center justify-center px-2.5 py-1 rounded-full ${isMoreActive ? 'bg-indigo-50 text-indigo-600' : 'text-slate-400'} transition-all">
          <i data-lucide="grid" class="w-5 h-5"></i>
        </div>
        <span class="text-[10px] tracking-tight mt-0.5 leading-none">Yana</span>
      </button>
    `;

    const sidebarContainer = document.getElementById("teacher-sidebar");
    if (!sidebarContainer) return;

    sidebarContainer.innerHTML = `
      <!-- Desktop Sidebar (Only on lg+) -->
      <aside id="desktop-sidebar" class="hidden lg:flex flex-col w-72 h-screen sticky top-0 bg-white border-r border-slate-200/80 p-4 shadow-sm z-30 transition-all duration-200">
        <!-- Logo -->
        <div class="flex items-center justify-between px-2 py-2 mb-4">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center text-white shadow-md shadow-indigo-500/25">
              <i data-lucide="award" class="w-6 h-6"></i>
            </div>
            <div>
              <h1 class="text-base font-bold text-slate-800 leading-tight">BioEdu Ustoz</h1>
              <span class="text-[11px] font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full">O'qituvchi Portali</span>
            </div>
          </div>
          <button onclick="window.toggleSidebar()" title="Menyuni yashirish" class="hidden lg:flex p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition">
            <i data-lucide="panel-left-close" class="w-4 h-4"></i>
          </button>
        </div>

        <!-- Navigation Menu -->
        <nav class="space-y-1 flex-1 overflow-y-auto pr-1">
          <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-3 mb-2">Boshqaruv Paneli</div>
          ${navLinksHtml}
        </nav>

        <!-- User Profile Card & Logout -->
        <div class="pt-3 border-t border-slate-100 mt-auto">
          <div class="p-2.5 bg-slate-50 rounded-2xl flex items-center gap-3 border border-slate-100">
            <div class="w-10 h-10 rounded-full bg-indigo-600 text-white font-bold flex items-center justify-center shadow-sm">
              ${user.avatar || user.fullName?.[0] || 'U'}
            </div>
            <div class="overflow-hidden flex-1">
              <p class="text-xs font-bold text-slate-800 truncate">${user.fullName || "O'qituvchi"}</p>
              <p class="text-[11px] text-indigo-600 truncate font-medium">${user.subject || "Biologiya fani"}</p>
            </div>
            <button onclick="Auth.logout()" title="Tizimdan chiqish" class="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition">
              <i data-lucide="log-out" class="w-4 h-4"></i>
            </button>
          </div>
        </div>
      </aside>

      <!-- Desktop Sidebar Reopen Button (shown only on lg+ when sidebar is closed) -->
      <button id="sidebar-reopen-btn" onclick="window.toggleSidebar()" title="Menyuni ochish"
        class="hidden fixed left-0 top-5 z-40 bg-white border border-l-0 border-slate-200 shadow-md py-2 px-1.5 rounded-r-xl text-slate-500 hover:text-indigo-600 hover:bg-slate-50 transition cursor-pointer">
        <i data-lucide="panel-left-open" class="w-5 h-5"></i>
      </button>

      <!-- Mobile Top App Header (Clean & Modern Native Feel) -->
      <div class="lg:hidden sticky top-0 z-30 bg-white/95 backdrop-blur-md border-b border-slate-200/80 px-4 py-2.5 flex items-center justify-between shadow-xs">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center text-white shadow-sm shadow-indigo-500/20">
            <i data-lucide="award" class="w-4.5 h-4.5"></i>
          </div>
          <div>
            <span class="font-extrabold text-slate-800 text-sm tracking-tight block leading-tight">BioEdu Ustoz</span>
            <span class="text-[10px] text-indigo-600 font-bold leading-none">${user.subject || "Biologiya fani"}</span>
          </div>
        </div>

        <!-- User Chip & Logout (No hamburger menu needed!) -->
        <div class="flex items-center gap-2">
          <div class="flex items-center gap-2 pl-2.5 pr-1.5 py-1 bg-slate-100/80 border border-slate-200/80 rounded-full">
            <span class="text-xs font-bold text-slate-700 truncate max-w-[110px]">${(user.fullName || "Ustoz").split(" ")[0]}</span>
            <div class="w-6 h-6 rounded-full bg-indigo-600 text-white font-black text-[10px] flex items-center justify-center shadow-xs">
              ${user.avatar || user.fullName?.[0] || 'U'}
            </div>
          </div>
          <button onclick="Auth.logout()" title="Tizimdan chiqish" class="p-1.5 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-xl transition cursor-pointer">
            <i data-lucide="log-out" class="w-4 h-4"></i>
          </button>
        </div>
      </div>

      <!-- Mobile App Bottom Navigation Bar -->
      <nav id="teacher-bottom-nav" class="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-xl border-t border-slate-200/90 shadow-[0_-4px_24px_rgba(0,0,0,0.06)] px-2 pt-1 pb-[calc(env(safe-area-inset-bottom,4px)+6px)]">
        <div class="flex items-center justify-around max-w-md mx-auto">
          ${bottomNavHtml}
          ${moreBtnHtml}
        </div>
      </nav>

      <!-- Mobile "Yana" (More) Bottom Sheet Modal -->
      <div id="teacher-more-sheet" class="fixed inset-0 bg-slate-900/50 backdrop-blur-xs z-50 hidden flex flex-col justify-end">
        <div class="bg-white rounded-t-3xl max-h-[85vh] flex flex-col shadow-2xl animate-in slide-in-from-bottom duration-200">
          <!-- Handle & Header -->
          <div class="p-4 border-b border-slate-100 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
                <i data-lucide="grid" class="w-4 h-4"></i>
              </div>
              <h3 class="text-sm font-extrabold text-slate-800">Qo'shimcha Bo'limlar</h3>
            </div>
            <button onclick="window.closeTeacherMoreSheet()" class="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-xl transition cursor-pointer">
              <i data-lucide="x" class="w-5 h-5"></i>
            </button>
          </div>

          <!-- Sheet Body with Grid of Actions -->
          <div class="p-4 overflow-y-auto space-y-4">
            
            <!-- User summary card -->
            <div class="p-3 bg-slate-50 border border-slate-100 rounded-2xl flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-indigo-600 text-white font-black flex items-center justify-center shadow-xs">
                  ${user.avatar || user.fullName?.[0] || 'U'}
                </div>
                <div>
                  <p class="text-xs font-bold text-slate-800">${user.fullName || "O'qituvchi"}</p>
                  <p class="text-[11px] text-indigo-600 font-medium">${user.subject || "Biologiya fani"}</p>
                </div>
              </div>
              <button onclick="Auth.logout()" class="px-3 py-1.5 bg-red-50 text-red-600 text-xs font-bold rounded-xl hover:bg-red-100 transition flex items-center gap-1 cursor-pointer">
                <i data-lucide="log-out" class="w-3.5 h-3.5"></i>
                <span>Chiqish</span>
              </button>
            </div>

            <!-- Grid of Cards -->
            <div class="grid grid-cols-2 gap-2.5">
              ${teacherMoreItems.map(item => {
                const isActive = (activeKey && activeKey.toLowerCase() === item.label.toLowerCase()) ||
                  currentPath === item.cleanPath || currentPath === item.path;

                return `
                  <a href="${item.path}" class="p-3 rounded-2xl border transition-all active:scale-95 flex flex-col justify-between ${isActive ? 'bg-indigo-600 text-white border-indigo-600 shadow-md shadow-indigo-500/20' : 'bg-white border-slate-100 hover:border-slate-200 shadow-xs'}">
                    <div class="w-8 h-8 rounded-xl flex items-center justify-center mb-2 ${isActive ? 'bg-white/20 text-white' : item.bg}">
                      <i data-lucide="${item.icon}" class="w-4 h-4"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold leading-tight ${isActive ? 'text-white' : 'text-slate-800'}">${item.label}</h4>
                      <p class="text-[10px] mt-0.5 ${isActive ? 'text-indigo-100' : 'text-slate-400'} truncate">${item.desc}</p>
                    </div>
                  </a>
                `;
              }).join("")}
            </div>

          </div>
        </div>
      </div>
    `;

    // Initialize icons
    if (window.lucide) {
      window.lucide.createIcons();
    }

    // Attach sheet backdrop click listener
    const moreSheet = document.getElementById("teacher-more-sheet");
    if (moreSheet) {
      moreSheet.addEventListener("click", (e) => {
        if (e.target === moreSheet) {
          window.closeTeacherMoreSheet();
        }
      });
    }

    const isClosed = localStorage.getItem("teacher_sidebar_closed") === "true";
    const desktopSidebar = document.getElementById("desktop-sidebar");
    const reopenBtn = document.getElementById("sidebar-reopen-btn");
    if (isClosed && desktopSidebar) {
      desktopSidebar.classList.add("lg:hidden");
      if (reopenBtn) {
        reopenBtn.classList.remove("hidden");
        reopenBtn.classList.add("lg:flex");
      }
    }
  };

  window.openTeacherMoreSheet = function() {
    const sheet = document.getElementById("teacher-more-sheet");
    if (sheet) {
      sheet.classList.remove("hidden");
      if (window.lucide) window.lucide.createIcons();
    }
  };

  window.closeTeacherMoreSheet = function() {
    const sheet = document.getElementById("teacher-more-sheet");
    if (sheet) {
      sheet.classList.add("hidden");
    }
  };

  window.toggleSidebar = function() {
    const desktopSidebar = document.getElementById("desktop-sidebar");
    const reopenBtn = document.getElementById("sidebar-reopen-btn");
    if (!desktopSidebar) return;
    desktopSidebar.classList.toggle("lg:hidden");
    const isClosed = desktopSidebar.classList.contains("lg:hidden");
    localStorage.setItem("teacher_sidebar_closed", isClosed ? "true" : "false");
    if (reopenBtn) {
      if (isClosed) {
        reopenBtn.classList.remove("hidden");
        reopenBtn.classList.add("lg:flex");
      } else {
        reopenBtn.classList.remove("lg:flex");
        reopenBtn.classList.add("hidden");
      }
    }
    if (window.lucide) window.lucide.createIcons();
  };
})();
