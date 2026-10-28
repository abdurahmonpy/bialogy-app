// Student Navigation Sidebar Component
(function() {
  const currentPath = window.location.pathname.replace(/\/$/, "");
  
  const menuItems = [
    { label: "Bosh sahifa", path: "/student/index.html", cleanPath: "/student", icon: "layout-dashboard" },
    { label: "Resurslar", path: "/student/resources.html", cleanPath: "/student/resources", icon: "book-open" },
    { label: "Chat", path: "/student/chat.html", cleanPath: "/student/chat", icon: "message-circle" },
    { label: "Uyga vazifa", path: "/student/homework.html", cleanPath: "/student/homework", icon: "clipboard-list" },
    { label: "Test", path: "/student/test.html", cleanPath: "/student/test", icon: "check-circle-2" }
  ];

  window.renderStudentSidebar = function(activeKey = "") {
    const user = (window.Auth && window.Auth.getCurrentUser()) || { fullName: "O'quvchi", classGrade: "O'quvchi", avatar: "O" };

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
      <aside id="desktop-sidebar" class="hidden lg:flex flex-col w-72 h-screen sticky top-0 bg-white border-r border-slate-200/80 p-5 shadow-sm z-30 transition-all duration-200">
        <!-- Logo -->
        <div class="flex items-center justify-between px-2 py-3 mb-6">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white shadow-md shadow-emerald-500/25">
              <i data-lucide="dna" class="w-6 h-6"></i>
            </div>
            <div>
              <h1 class="text-base font-bold text-slate-800 leading-tight">BioEdu Maktab</h1>
              <span class="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full">O'quvchi Kabineti</span>
            </div>
          </div>
          <button onclick="window.toggleSidebar()" title="Menyuni yashirish" class="hidden lg:flex p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition">
            <i data-lucide="panel-left-close" class="w-4 h-4"></i>
          </button>
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

      <!-- Desktop Sidebar Reopen Button (shown only on lg+ when sidebar is closed) -->
      <button id="sidebar-reopen-btn" onclick="window.toggleSidebar()" title="Menyuni ochish"
        class="hidden fixed left-0 top-5 z-40 bg-white border border-l-0 border-slate-200 shadow-md py-2 px-1.5 rounded-r-xl text-slate-500 hover:text-emerald-600 hover:bg-slate-50 transition cursor-pointer">
        <i data-lucide="panel-left-open" class="w-5 h-5"></i>
      </button>

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

    const isClosed = localStorage.getItem("student_sidebar_closed") === "true";
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

  window.toggleSidebar = function() {
    const desktopSidebar = document.getElementById("desktop-sidebar");
    const reopenBtn = document.getElementById("sidebar-reopen-btn");
    if (!desktopSidebar) return;
    desktopSidebar.classList.toggle("lg:hidden");
    const isClosed = desktopSidebar.classList.contains("lg:hidden");
    localStorage.setItem("student_sidebar_closed", isClosed ? "true" : "false");
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

  // ==============================================================
  // Real-Time Active Live Test Notification System
  // ==============================================================
  let activeTestPollInterval = null;
  let lastNotifiedSessionId = null;

  function initLiveTestWatcher() {
    if (window.location.pathname.includes("/student/live-test.html") || window.location.pathname.includes("/join.html")) {
      return; // Already in test runner or join page
    }

    const checkActiveTests = async () => {
      const user = window.Auth ? window.Auth.getCurrentUser() : null;
      if (!user || !user.id || user.role === "teacher") return;

      try {
        const res = await fetch("/api/student/active-live-tests", {
          headers: {
            "X-User-Id": user.id,
            "X-User-Role": user.role || "student"
          }
        });
        if (!res.ok) return;

        const data = await res.json();
        const activeList = data.activeTests || [];

        if (activeList.length > 0) {
          const latestTest = activeList[0];
          showLiveTestBanner(latestTest);
        } else {
          hideLiveTestBanner();
        }
      } catch (err) {
        // Silent network retry
      }
    };

    // Initial check + 5s polling
    checkActiveTests();
    activeTestPollInterval = setInterval(checkActiveTests, 5000);
  }

  function showLiveTestBanner(test) {
    let banner = document.getElementById("global-live-test-banner");
    const isNewSession = lastNotifiedSessionId !== test.id;

    if (!banner) {
      banner = document.createElement("div");
      banner.id = "global-live-test-banner";
      banner.className = "fixed top-3 left-1/2 -translate-x-1/2 z-50 w-[94%] max-w-2xl bg-gradient-to-r from-red-600 via-orange-600 to-amber-600 text-white p-3.5 sm:p-4 rounded-2xl shadow-2xl border-2 border-white/40 flex flex-col sm:flex-row items-center justify-between gap-3 animate-bounce-small transition-all";
      document.body.appendChild(banner);
    }

    banner.innerHTML = `
      <div class="flex items-center gap-3 w-full sm:w-auto">
        <div class="w-10 h-10 rounded-xl bg-white/20 backdrop-blur-md flex items-center justify-center text-white flex-shrink-0 animate-pulse">
          <i data-lucide="zap" class="w-6 h-6 fill-current"></i>
        </div>
        <div class="overflow-hidden">
          <div class="flex items-center gap-2">
            <span class="inline-block w-2 h-2 rounded-full bg-yellow-300 animate-ping"></span>
            <span class="text-[11px] font-black uppercase tracking-wider text-yellow-200">Jonli Test Boshlandi!</span>
            <span class="text-[10px] bg-black/25 px-2 py-0.5 rounded-full font-bold">PIN: ${test.code}</span>
          </div>
          <h4 class="text-sm font-extrabold text-white truncate leading-tight">${test.title || "Biologiya Jonli Testi"}</h4>
          <p class="text-[11px] text-white/80 truncate">Guruh: ${test.groupName || "Barcha o'quvchilar"}</p>
        </div>
      </div>
      <div class="flex items-center gap-2 w-full sm:w-auto justify-end">
        <a href="/student/live-test.html?code=${test.code}" 
           class="flex-1 sm:flex-none px-5 py-2.5 bg-white hover:bg-yellow-100 text-slate-950 font-black text-xs rounded-xl shadow-lg transition-transform hover:scale-105 active:scale-95 flex items-center justify-center gap-1.5 cursor-pointer">
          <span>Testga Kirish</span>
          <i data-lucide="arrow-right" class="w-4 h-4"></i>
        </a>
      </div>
    `;

    if (window.lucide) window.lucide.createIcons();

    if (isNewSession) {
      lastNotifiedSessionId = test.id;
      // Play a gentle notification beep
      try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (AudioContext) {
          const ctx = new AudioContext();
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = "sine";
          osc.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
          osc.frequency.setValueAtTime(880, ctx.currentTime + 0.15); // A5
          gain.gain.setValueAtTime(0.15, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.4);
        }
      } catch (e) {}
    }
  }

  function hideLiveTestBanner() {
    const banner = document.getElementById("global-live-test-banner");
    if (banner) {
      banner.remove();
    }
    lastNotifiedSessionId = null;
  }

  // Start watcher on DOM load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initLiveTestWatcher);
  } else {
    initLiveTestWatcher();
  }

})();
