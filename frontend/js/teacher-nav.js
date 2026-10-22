// Teacher Navigation Sidebar Component
(function() {
  const currentPath = window.location.pathname.replace(/\/$/, "");
  
  const menuItems = [
    { label: "Bosh sahifa", path: "/teacher/index.html", cleanPath: "/teacher", icon: "layout-dashboard" },
    { label: "Chat", path: "/teacher/chat.html", cleanPath: "/teacher/chat", icon: "message-circle" },
    { label: "Guruhlarim", path: "/teacher/groups.html", cleanPath: "/teacher/groups", icon: "users" },
    { label: "Uyga vazifa", path: "/teacher/homework.html", cleanPath: "/teacher/homework", icon: "clipboard-list" },
    { label: "O'quvchilar", path: "/teacher/students.html", cleanPath: "/teacher/students", icon: "graduation-cap" },
    { label: "Test Markaz", path: "/teacher/test.html", cleanPath: "/teacher/test", icon: "file-check" },
    { label: "Statistika", path: "/teacher/stats.html", cleanPath: "/teacher/stats", icon: "bar-chart-3" },
    { label: "AI Yordamchi", path: "/teacher/ai-assistant.html", cleanPath: "/teacher/ai-assistant", icon: "sparkles" },
    { label: "O'quvchi qo'shish", path: "/teacher/add-student.html", cleanPath: "/teacher/add-student", icon: "user-plus" }
  ];

  window.renderTeacherSidebar = function(activeKey = "") {
    const user = (window.Auth && window.Auth.getCurrentUser()) || { fullName: "Aziza Rahimova", subject: "Biologiya", avatar: "A" };

    const navLinksHtml = menuItems.map(item => {
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

    const sidebarContainer = document.getElementById("teacher-sidebar");
    if (!sidebarContainer) return;

    sidebarContainer.innerHTML = `
      <!-- Desktop Sidebar -->
      <aside class="hidden lg:flex flex-col w-72 h-screen sticky top-0 bg-white border-r border-slate-200/80 p-4 shadow-sm z-30">
        <!-- Logo -->
        <div class="flex items-center gap-3 px-2 py-2 mb-4">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center text-white shadow-md shadow-indigo-500/25">
            <i data-lucide="award" class="w-6 h-6"></i>
          </div>
          <div>
            <h1 class="text-base font-bold text-slate-800 leading-tight">BioEdu Ustoz</h1>
            <span class="text-[11px] font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full">O'qituvchi Portali</span>
          </div>
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

      <!-- Mobile Header & Drawer -->
      <div class="lg:hidden sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 px-4 py-3 flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
            <i data-lucide="award" class="w-5 h-5"></i>
          </div>
          <span class="font-bold text-slate-800 text-sm">BioEdu Ustoz Portali</span>
        </div>
        <button id="mobile-menu-btn" class="p-2 text-slate-600 hover:bg-slate-100 rounded-lg">
          <i data-lucide="menu" class="w-6 h-6"></i>
        </button>
      </div>

      <!-- Mobile Drawer Modal -->
      <div id="mobile-drawer" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 hidden">
        <div class="bg-white w-72 h-full p-5 flex flex-col shadow-2xl">
          <div class="flex items-center justify-between pb-4 border-b border-slate-100 mb-3">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
                <i data-lucide="award" class="w-5 h-5"></i>
              </div>
              <span class="font-bold text-slate-800">O'qituvchi Portali</span>
            </div>
            <button id="close-drawer-btn" class="p-1.5 text-slate-400 hover:text-slate-700">
              <i data-lucide="x" class="w-5 h-5"></i>
            </button>
          </div>
          <nav class="space-y-1 flex-1 overflow-y-auto">
            ${navLinksHtml}
          </nav>
          <div class="pt-4 border-t border-slate-100 mt-auto">
            <button onclick="Auth.logout()" class="w-full flex items-center justify-center gap-2 p-3 text-red-600 bg-red-50 hover:bg-red-100 rounded-xl font-medium transition text-sm">
              <i data-lucide="log-out" class="w-4 h-4"></i>
              Tizimdan chiqish
            </button>
          </div>
        </div>
      </div>
    `;

    // Initialize icons
    if (window.lucide) {
      window.lucide.createIcons();
    }

    // Attach drawer events
    const menuBtn = document.getElementById("mobile-menu-btn");
    const drawer = document.getElementById("mobile-drawer");
    const closeBtn = document.getElementById("close-drawer-btn");

    if (menuBtn && drawer && closeBtn) {
      menuBtn.addEventListener("click", () => drawer.classList.remove("hidden"));
      closeBtn.addEventListener("click", () => drawer.classList.add("hidden"));
      drawer.addEventListener("click", (e) => {
        if (e.target === drawer) drawer.classList.add("hidden");
      });
    }
  };
})();
