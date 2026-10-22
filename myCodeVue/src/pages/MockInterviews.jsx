import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import {
  ArrowRight,
  Search,
  CheckCircle2,
  Clock,
  Award,
  Loader2,
  BarChart3,
  Calendar,
  Play,
  RotateCcw,
} from "lucide-react";
import "./MockInterviews.css";

const API_BASE_URL = (
  import.meta.env.VITE_AI_SERVICE_URL || "http://localhost:8000"
).replace(/\/$/, "");

export default function MockInterviews() {
  const { user } = useAuth();
  const userName = user?.fullName || "there";
  const userEmail = user?.email || "";
  
  const [historyData, setHistoryData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");

  useEffect(() => {
    if (!userEmail) {
      setLoading(false);
      return;
    }

    async function fetchHistory() {
      try {
        const res = await fetch(
          `${API_BASE_URL}/interviews/user/${encodeURIComponent(userEmail)}/history`
        );
        if (res.ok) {
          const data = await res.json();
          setHistoryData(data);
        }
      } catch (err) {
        console.error("Could not fetch user history:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchHistory();
  }, [userEmail]);

  const formatDate = (timestamp) => {
    if (!timestamp) return "Recent";
    const date = new Date(timestamp * 1000);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const interviewsList = historyData?.interviews || [];

  const filteredInterviews = interviewsList.filter((item) => {
    const matchesSearch =
      item.problem_title?.toLowerCase().includes(search.toLowerCase()) ||
      item.topic?.toLowerCase().includes(search.toLowerCase());

    const matchesStatus =
      statusFilter === "All" ||
      (statusFilter === "Completed" && item.phase === "finished") ||
      (statusFilter === "In Progress" && item.phase !== "finished");

    return matchesSearch && matchesStatus;
  });

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
          <Link to="/mock-interviews" className="active">
            Mock Interviews
          </Link>
          <Link to="/progress">My Progress</Link>
        </nav>

        <Link to="/profile" className="cv-profile-link" aria-label="My profile">
          <span className="cv-avatar">
            {userName !== "there" ? userName.trim().charAt(0).toUpperCase() : "U"}
          </span>
          <span className="cv-profile-name">{userName}</span>
        </Link>
      </header>

      <main className="cv-main">
        {/* Page Heading */}
        <section className="cv-interviews-header">
          <div>
            <p className="cv-eyebrow">YOUR ATTEMPTS & REVIEWS</p>
            <h1>Mock Interview History</h1>
            <p className="cv-interviews-subtitle">
              Review your previous responses, code submissions, test verdicts, and AI evaluation reports.
            </p>
          </div>
          <Link to="/dashboard" className="cv-btn-primary">
            <Play size={16} fill="currentColor" />
            New Interview
          </Link>
        </section>

        {/* Aggregate Stats Cards */}
        <section className="cv-metrics-row">
          <div className="cv-metric-box">
            <div className="cv-metric-header">
              <span className="cv-metric-title">Total Attempted</span>
              <BarChart3 size={16} className="cv-metric-icon" />
            </div>
            <div className="cv-metric-number">{historyData?.total_interviews ?? 0}</div>
            <span className="cv-metric-sub">Interview sessions started</span>
          </div>

          <div className="cv-metric-box">
            <div className="cv-metric-header">
              <span className="cv-metric-title">Completed Rounds</span>
              <CheckCircle2 size={16} className="cv-metric-icon cv-text-green" />
            </div>
            <div className="cv-metric-number">{historyData?.completed_interviews ?? 0}</div>
            <span className="cv-metric-sub">Fully evaluated and finalized</span>
          </div>

          <div className="cv-metric-box">
            <div className="cv-metric-header">
              <span className="cv-metric-title">Average Score</span>
              <Award size={16} className="cv-metric-icon cv-text-red" />
            </div>
            <div className="cv-metric-number">
              {historyData?.average_overall_score ?? "0.0"}{" "}
              <span className="cv-stat-dim">/ 10</span>
            </div>
            <span className="cv-metric-sub">Across brute force, optimization, & code</span>
          </div>
        </section>

        {/* Filters and Search Bar */}
        <section className="cv-history-tools">
          <div className="cv-search-input-box">
            <Search size={16} />
            <input
              type="text"
              placeholder="Search problem title or topic..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="cv-filter-group">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="cv-status-select"
            >
              <option value="All">All Statuses</option>
              <option value="Completed">Completed</option>
              <option value="In Progress">In Progress</option>
            </select>
          </div>
        </section>

        {/* History Table */}
        <section className="cv-history-content">
          {loading ? (
            <div className="cv-history-loading">
              <Loader2 size={24} className="cv-spin" />
              <span>Loading your mock interviews...</span>
            </div>
          ) : filteredInterviews.length > 0 ? (
            <div className="cv-history-table-wrapper">
              <table className="cv-history-table">
                <thead>
                  <tr>
                    <th>Problem</th>
                    <th>Topic</th>
                    <th>Difficulty</th>
                    <th>Status</th>
                    <th>Brute Force</th>
                    <th>Optimized</th>
                    <th>Code Score</th>
                    <th>Date</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredInterviews.map((item) => (
                    <tr key={item.interview_id}>
                      <td className="cv-table-problem">
                        <span className="cv-problem-name">{item.problem_title}</span>
                      </td>
                      <td>
                        <span className="cv-topic-badge">{item.topic}</span>
                      </td>
                      <td>
                        <span className={`cv-diff-badge cv-diff-${item.difficulty?.toLowerCase()}`}>
                          {item.difficulty}
                        </span>
                      </td>
                      <td>
                        <span className={`cv-status-badge cv-status-${item.phase}`}>
                          {item.phase === "finished" ? "Completed" : "In Progress"}
                        </span>
                      </td>
                      <td className="cv-score-cell">
                        {item.brute_force_score != null ? `${item.brute_force_score}/10` : "--"}
                      </td>
                      <td className="cv-score-cell">
                        {item.optimized_score != null ? `${item.optimized_score}/10` : "--"}
                      </td>
                      <td className="cv-score-cell">
                        {item.code_score != null ? `${item.code_score}/10` : "--"}
                      </td>
                      <td className="cv-date-cell">
                        <Calendar size={13} />
                        {formatDate(item.started_at)}
                      </td>
                      <td>
                        <Link
                          to={
                            item.phase === "finished"
                              ? `/interview/${item.interview_id}/report`
                              : `/interview/${item.problem_id}`
                          }
                          className="cv-resume-btn"
                        >
                          {item.phase === "finished" ? (
                            <>
                              Review <ArrowRight size={13} />
                            </>
                          ) : (
                            <>
                              Resume <RotateCcw size={13} />
                            </>
                          )}
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="cv-history-empty">
              <Clock size={34} className="cv-muted-icon" />
              <h3>No Mock Interviews Found</h3>
              <p>
                {search || statusFilter !== "All"
                  ? "No sessions match your search or filter criteria."
                  : "You haven't conducted any mock interviews yet. Pick a track to get started."}
              </p>
              <Link to="/dashboard" className="cv-btn-primary">
                Browse Interview Tracks
              </Link>
            </div>
          )}
        </section>
      </main>

      <footer className="cv-footer">
        <span>© {new Date().getFullYear()} CodeVue</span>
        <span>Practice with purpose.</span>
      </footer>
    </div>
  );
}