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

    return user;
  }
};

window.Auth = Auth;
