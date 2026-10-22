// Student Navigation Sidebar Component
(function() {
  const currentPath = window.location.pathname.replace(/\/$/, "");
  
  const menuItems = [
    { label: "Bosh sahifa", path: "/student/index.html", cleanPath: "/student", icon: "layout-dashboard" },
    { label: "Chat", path: "/student/chat.html", cleanPath: "/student/chat", icon: "message-circle" },
    { label: "Uyga vazifa", path: "/student/homework.html", cleanPath: "/student/homework", icon: "book-open" },
    { label: "Test", path: "/student/test.html", cleanPath: "/student/test", icon: "check-circle-2" }
  ];

  window.renderStudentSidebar = function(activeKey = "") {
    const user = (window.Auth && window.Auth.getCurrentUser()) || { fullName: "Jasurbek Aliyev", classGrade: "8-A sinf", avatar: "J" };

    const navLinksHtml = menuItems.map(item => {
      const isActive = activeKey 
        ? item.label.toLowerCase() === activeKey.toLowerCase()
        : (currentPath === item.cleanPath || currentPath === item.path || (item.cleanPath === "/student" && (currentPath === "" || currentPath === "/student")));

      const activeClasses = isActive
        ? "bg-emerald-600 text-white shadow-md shadow-emerald-500/20 font-semibold"
        : "text-slate-600 hover:bg-slate-100 hover:text-slate-900 font-medium";

      return `
        <a href="${item.path}" class="flex items-center gap-3.5 px-4 py-3 rounded-xl transition-all duration-200 ${activeClasses}">
          <i data-lucide="${item.icon}" class="w-5 h-5 flex-shrink-0"></i>
          <span class="text-sm tracking-wide">${item.label}</span>
          ${isActive ? `<span class="ml-auto w-1.5 h-5 rounded-full bg-white"></span>` : ""}
        </a>
      `;
    }).join("");

    const sidebarContainer = document.getElementById("student-sidebar");
    if (!sidebarContainer) return;

    sidebarContainer.innerHTML = `
      <!-- Desktop Sidebar -->
      <aside class="hidden lg:flex flex-col w-72 h-screen sticky top-0 bg-white border-r border-slate-200/80 p-5 shadow-sm z-30">
        <!-- Logo -->
        <div class="flex items-center gap-3 px-2 py-3 mb-6">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white shadow-md shadow-emerald-500/25">
            <i data-lucide="dna" class="w-6 h-6"></i>
          </div>
          <div>
            <h1 class="text-base font-bold text-slate-800 leading-tight">BioEdu Maktab</h1>
            <span class="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full">O'quvchi Kabineti</span>
          </div>
        </div>

        <!-- Navigation Menu -->
        <nav class="space-y-1.5 flex-1 overflow-y-auto">
          <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-3 mb-2">Asosiy Bo'limlar</div>
          ${navLinksHtml}
        </nav>

        <!-- User Profile Card & Logout -->
        <div class="pt-4 border-t border-slate-100 mt-auto">
          <div class="p-3 bg-slate-50 rounded-2xl flex items-center gap-3 border border-slate-100 mb-2">
            <div class="w-10 h-10 rounded-full bg-emerald-500 text-white font-bold flex items-center justify-center shadow-sm">
              ${user.avatar || user.fullName?.[0] || 'O'}
            </div>
            <div class="overflow-hidden flex-1">
              <p class="text-sm font-semibold text-slate-800 truncate">${user.fullName || "O'quvchi"}</p>
              <p class="text-xs text-slate-500 truncate">${user.classGrade || "8-A sinf"}</p>
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
          <div class="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white">
            <i data-lucide="dna" class="w-5 h-5"></i>
          </div>
          <span class="font-bold text-slate-800 text-sm">BioEdu O'quvchi</span>
        </div>
        <button id="mobile-menu-btn" class="p-2 text-slate-600 hover:bg-slate-100 rounded-lg">
          <i data-lucide="menu" class="w-6 h-6"></i>
        </button>
      </div>

      <!-- Mobile Drawer Modal -->
      <div id="mobile-drawer" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 hidden">
        <div class="bg-white w-72 h-full p-5 flex flex-col shadow-2xl">
          <div class="flex items-center justify-between pb-4 border-b border-slate-100 mb-4">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white">
                <i data-lucide="dna" class="w-5 h-5"></i>
              </div>
              <span class="font-bold text-slate-800">O'quvchi Kabineti</span>
            </div>
            <button id="close-drawer-btn" class="p-1.5 text-slate-400 hover:text-slate-700">
              <i data-lucide="x" class="w-5 h-5"></i>
            </button>
          </div>
          <nav class="space-y-1.5 flex-1">
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
