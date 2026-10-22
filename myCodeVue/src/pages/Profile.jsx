import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import {
  Award,
  CheckCircle2,
  Code2,
  Globe,
  Key,
  LogOut,
  Mail,
  Save,
  Shield,
  User,
} from "lucide-react";
import "./Profile.css";

const API_BASE_URL = (
  import.meta.env.VITE_AI_SERVICE_URL || "http://localhost:8000"
).replace(/\/$/, "");

export default function Profile() {
  const { user, setUser, logout } = useAuth();
  const navigate = useNavigate();

  const userName = user?.fullName || "User";
  const userEmail = user?.email || "candidate@codevue.dev";

  // Persistent user preferences
  const [defaultLang, setDefaultLang] = useState(() => {
    return localStorage.getItem("codevue_default_lang") || "cpp";
  });
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Quick stats
  const [stats, setStats] = useState({ total: 0, completed: 0, avgScore: "0.0" });

  useEffect(() => {
    if (!userEmail) return;

    async function fetchStats() {
      try {
        const res = await fetch(
          `${API_BASE_URL}/interviews/user/${encodeURIComponent(userEmail)}/history`
        );
        if (res.ok) {
          const data = await res.json();
          setStats({
            total: data.total_interviews || 0,
            completed: data.completed_interviews || 0,
            avgScore: data.average_overall_score ?? "0.0",
          });
        }
      } catch (e) {
        // Fallback default stats
      }
    }

    fetchStats();
  }, [userEmail]);

  const handleSavePreferences = (e) => {
    e.preventDefault();
    localStorage.setItem("codevue_default_lang", defaultLang);
    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 2500);
  };

  const handleSignOut = () => {
    // Execute centralized logout
    if (logout) {
      logout();
    } else {
      localStorage.clear();
    }

    // Redirect to login or home
    navigate("/login", { replace: true });
  };

  return (
    <div className="cv-dashboard">
      {/* Top Navbar */}
      <header className="cv-navbar">
        <Link to="/dashboard" className="cv-brand" aria-label="CodeVue dashboard">
          <div className="cv-brand-icon">
            <span>&lt;</span>
            <span className="greaterThan">&gt;</span>
          </div>
          <span>
            Code<span className="cv-brand-accent">Vue</span>
          </span>
        </Link>

        <nav className="cv-nav-links" aria-label="Main navigation">
          <Link to="/">Home</Link>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/mock-interviews">Mock Interviews</Link>
          <Link to="/progress">My Progress</Link>
        </nav>

        <Link to="/profile" className="cv-profile-link active" aria-label="My profile">
          <span className="cv-avatar">
            {userName !== "User" ? userName.trim().charAt(0).toUpperCase() : "U"}
          </span>
          <span className="cv-profile-name">{userName}</span>
        </Link>
      </header>

      <main className="cv-main">
        {/* Header */}
        <section className="cv-profile-header">
          <div>
            <p className="cv-eyebrow">ACCOUNT SETTINGS</p>
            <h1>Candidate Profile</h1>
            <p className="cv-profile-subtitle">
              Manage your personal details, workspace preferences, and interview environment.
            </p>
          </div>
          <button className="cv-btn-danger" onClick={handleSignOut}>
            <LogOut size={16} />
            Sign Out
          </button>
        </section>

        <div className="cv-profile-layout">
          {/* Left Column: Identity Card */}
          <div className="cv-profile-card">
            <div className="cv-profile-avatar-large">
              {userName.trim().charAt(0).toUpperCase()}
            </div>
            <h2>{userName}</h2>
            <p className="cv-profile-email">
              <Mail size={14} />
              {userEmail}
            </p>
            <span className="cv-profile-badge">Technical Candidate</span>

            <div className="cv-profile-card-divider" />

            <div className="cv-profile-quick-stats">
              <div className="cv-pstat-item">
                <span className="cv-pstat-val">{stats.total}</span>
                <span className="cv-pstat-lbl">Attempts</span>
              </div>
              <div className="cv-pstat-item">
                <span className="cv-pstat-val">{stats.completed}</span>
                <span className="cv-pstat-lbl">Completed</span>
              </div>
              <div className="cv-pstat-item">
                <span className="cv-pstat-val">{stats.avgScore}</span>
                <span className="cv-pstat-lbl">Avg Score</span>
              </div>
            </div>
          </div>

          {/* Right Column: Preferences Form */}
          <div className="cv-profile-settings">
            <form onSubmit={handleSavePreferences} className="cv-settings-form">
              <div className="cv-settings-section">
                <h3>Interview Workspace Defaults</h3>
                <p>Choose your default configuration when launching into coding exercises.</p>

                <div className="cv-form-field">
                  <label htmlFor="default-lang">Default Programming Language</label>
                  <select
                    id="default-lang"
                    value={defaultLang}
                    onChange={(e) => setDefaultLang(e.target.value)}
                    className="cv-profile-select"
                  >
                    <option value="cpp">C++ (GCC 10.2 / C++17)</option>
                    <option value="python">Python (Python 3.10)</option>
                    <option value="java">Java (OpenJDK 17)</option>
                  </select>
                  <span className="cv-field-hint">
                    New interview sessions will automatically open Monaco Editor in this language.
                  </span>
                </div>
              </div>

              <div className="cv-settings-section">
                <h3>Account Security</h3>
                <div className="cv-security-item">
                  <div className="cv-sec-left">
                    <Shield size={18} className="cv-sec-icon" />
                    <div>
                      <strong>Authentication Mode</strong>
                      <p>JWT-secured credential login</p>
                    </div>
                  </div>
                  <span className="cv-status-badge cv-status-finished">Active</span>
                </div>
              </div>

              <div className="cv-form-actions">
                <button type="submit" className="cv-btn-primary">
                  <Save size={16} />
                  Save Workspace Settings
                </button>
                {saveSuccess && (
                  <span className="cv-save-msg">
                    <CheckCircle2 size={16} /> Settings saved!
                  </span>
                )}
              </div>
            </form>
          </div>
        </div>
      </main>

      <footer className="cv-footer">
        <span>© {new Date().getFullYear()} CodeVue</span>
        <span>Practice with purpose.</span>
      </footer>
    </div>
  );
}