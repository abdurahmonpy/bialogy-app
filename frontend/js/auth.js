// ============================================================
// Auth & Session Management Module (Pure JS, No Node.js)
// ============================================================

const Auth = {
  USER_KEY: "bio_current_user",
  ROLE_KEY: "bio_user_role",

  getCurrentUser() {
    try {
      const data = localStorage.getItem(this.USER_KEY);
      return data ? JSON.parse(data) : null;
    } catch (e) {
      console.error("Auth.getCurrentUser error:", e);
      return null;
    }
  },

  getUserRole() {
    const user = this.getCurrentUser();
    return user ? user.role : localStorage.getItem(this.ROLE_KEY) || null;
  },

  setCurrentUser(user) {
    if (!user) {
      localStorage.removeItem(this.USER_KEY);
      localStorage.removeItem(this.ROLE_KEY);
    } else {
      localStorage.setItem(this.USER_KEY, JSON.stringify(user));
      localStorage.setItem(this.ROLE_KEY, user.role);
    }
  },

  logout() {
    localStorage.removeItem(this.USER_KEY);
    localStorage.removeItem(this.ROLE_KEY);
    window.location.replace("/login.html");
  },

  async login(loginStr, password) {
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ login: loginStr.trim(), password: password.trim() })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Kirishda xatolik yuz berdi");
      }
      this.setCurrentUser(data.user);
      return data.user;
    } catch (err) {
      console.error("Login xatoligi:", err);
      throw err;
    }
  },

  async register(formData) {
    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Ro'yxatdan o'tishda xatolik yuz berdi");
      }
      this.setCurrentUser(data.user);
      return data.user;
    } catch (err) {
      console.error("Register xatoligi:", err);
      throw err;
    }
  },

  requireAuth(requiredRole = null) {
    const user = this.getCurrentUser();
    if (!user) {
      const currentPath = encodeURIComponent(window.location.pathname + window.location.search);
      window.location.replace(`/login.html?redirect=${currentPath}`);
      return null;
    }

    if (requiredRole && user.role !== requiredRole) {
      if (user.role === "teacher") {
        window.location.replace("/teacher/");
      } else {
        window.location.replace("/student/");
      }
      return null;
    }

    // Check student approval status
    if (user.role === "student") {
      if (user.status === "pending") {
        this.showPendingApprovalOverlay();
      }

      // Silently sync latest status from server
      this.syncUserStatus();
    }

    return user;
  },

  async syncUserStatus() {
    try {
      const user = this.getCurrentUser();
      if (!user || !user.id || user.role !== "student") return;

      const res = await fetch(`/api/auth/me?userId=${user.id}`);
      if (res.ok) {
        const data = await res.json();
        if (data && data.user) {
          const freshUser = data.user;
          const oldStatus = user.status;
          this.setCurrentUser(freshUser);

          // If recently approved, remove overlay and unblock UI
          if (oldStatus === "pending" && freshUser.status === "approved") {
            const overlay = document.getElementById("pending-approval-overlay");
            if (overlay) overlay.remove();
            document.body.style.overflow = "";
            window.location.reload();
          } else if (freshUser.status === "pending") {
            this.showPendingApprovalOverlay();
          }
        }
      }
    } catch (e) {
      // Ignore background sync errors
    }
  },

  showPendingApprovalOverlay() {
    if (document.getElementById("pending-approval-overlay")) return;

    const overlay = document.createElement("div");
    overlay.id = "pending-approval-overlay";
    overlay.className = "fixed inset-0 bg-slate-950/85 backdrop-blur-md z-[99999] flex items-center justify-center p-4 select-none";
    overlay.style.pointerEvents = "auto";

    overlay.innerHTML = `
      <div class="bg-white rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl border border-slate-100 text-center animate-in fade-in zoom-in duration-200">
        <div class="w-16 h-16 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center mx-auto mb-4 border border-amber-200 shadow-sm">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
          </svg>
        </div>
        <h2 class="text-lg font-extrabold text-slate-800 mb-2">Hisob tasdiqlanishi kutilmoqda</h2>
        <div class="p-3 bg-amber-50/70 border border-amber-200/80 rounded-2xl mb-4 text-center">
          <p class="text-sm font-bold text-amber-900 leading-relaxed">
            Your account has not been approved by a teacher yet. Please wait.
          </p>
        </div>
        <p class="text-xs text-slate-500 mb-6 leading-relaxed">
          Sizning hisobingiz hali o'qituvchi tomonidan tasdiqlanmagan. O'qituvchingiz sizni guruhga qo'shgach yoki hisobingizni tasdiqlagach, platformadan to'liq foydalanishingiz mumkin bo'ladi.
        </p>
        <div class="flex flex-col gap-2.5">
          <button onclick="Auth.checkStatusAndReload()" id="check-status-btn" class="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-xs transition shadow-md shadow-emerald-500/20 flex items-center justify-center gap-2 cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            <span>Statusni qayta tekshirish</span>
          </button>
          <button onclick="Auth.logout()" class="w-full py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-600 font-bold rounded-xl text-xs transition cursor-pointer">
            Tizimdan chiqish
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);
    document.body.style.overflow = "hidden";
  },

  async checkStatusAndReload() {
    const btn = document.getElementById("check-status-btn");
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = `<span>Tekshirilmoqda...</span>`;
    }

    try {
      const user = this.getCurrentUser();
      const res = await fetch(`/api/auth/me?userId=${user?.id}`);
      if (res.ok) {
        const data = await res.json();
        if (data && data.user) {
          this.setCurrentUser(data.user);
          if (data.user.status === "approved") {
            const overlay = document.getElementById("pending-approval-overlay");
            if (overlay) overlay.remove();
            document.body.style.overflow = "";
            window.location.reload();
            return;
          }
        }
      }
      alert("Hisobingiz hali o'qituvchi tomonidan tasdiqlanmadi. Iltimos, biroz kuting.");
    } catch (e) {
      alert("Tekshirishda xatolik: " + e.message);
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = `<span>Statusni qayta tekshirish</span>`;
      }
    }
  }
};

// Transparently hook fetch to attach current user identity and role to all requests
(function() {
  const originalFetch = window.fetch;
  window.fetch = function(url, options = {}) {
    try {
      const user = Auth.getCurrentUser();
      if (user && user.id) {
        options.headers = options.headers || {};
        if (typeof Headers !== "undefined" && options.headers instanceof Headers) {
          if (!options.headers.has("X-User-Id")) options.headers.set("X-User-Id", String(user.id));
          if (!options.headers.has("X-User-Role")) options.headers.set("X-User-Role", String(user.role));
        } else if (Array.isArray(options.headers)) {
          options.headers.push(["X-User-Id", String(user.id)]);
          options.headers.push(["X-User-Role", String(user.role)]);
        } else {
          options.headers["X-User-Id"] = String(user.id);
          options.headers["X-User-Role"] = String(user.role);
        }
      }
    } catch (e) {
      console.warn("Auth header injection error:", e);
    }
    return originalFetch(url, options);
  };
})();

window.Auth = Auth;
