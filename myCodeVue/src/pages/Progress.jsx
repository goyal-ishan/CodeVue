import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import {
  Award,
  BarChart3,
  CheckCircle2,
  Clock,
  Code2,
  Flame,
  Layers,
  Loader2,
  Play,
  Target,
  TrendingUp,
  Zap,
} from "lucide-react";
import "./Progress.css";

const API_BASE_URL = (
  import.meta.env.VITE_AI_SERVICE_URL || "http://localhost:8000"
).replace(/\/$/, "");

const TRACK_DEFINITIONS = [
  { id: "arrays-strings", name: "Array/String", total: 18 },
  { id: "two-pointers", name: "Two Pointers", total: 5 },
  { id: "sliding-window", name: "Sliding Window", total: 4 },
  { id: "linked-list", name: "Linked List", total: 5 },
  { id: "stack", name: "Stack", total: 5 },
  { id: "greedy-constructive", name: "Greedy & Constructive", total: 14 },
  { id: "backtracking", name: "Backtracking", total: 5 },
  { id: "dynamic-programming", name: "Dynamic Programming", total: 24 },
  { id: "graphs", name: "Graphs", total: 20 },
  { id: "number-theory", name: "Number Theory", total: 12 },
  { id: "trees-advanced-ds", name: "Trees & Advanced DS", total: 22 },
];

export default function Progress() {
  const { user } = useAuth();
  const userName = user?.fullName || "there";
  const userEmail = user?.email || "";

  const [historyData, setHistoryData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!userEmail) {
      setLoading(false);
      return;
    }

    async function fetchProgress() {
      try {
        const res = await fetch(
          `${API_BASE_URL}/interviews/user/${encodeURIComponent(userEmail)}/history`
        );
        if (res.ok) {
          const data = await res.json();
          setHistoryData(data);
        }
      } catch (err) {
        console.error("Failed to fetch progress metrics:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchProgress();
  }, [userEmail]);

  const interviews = historyData?.interviews || [];
  const completed = interviews.filter((i) => i.phase === "finished");

  // Phase score aggregations
  const avgBruteForce = completed.length
    ? (
        completed.reduce((acc, curr) => acc + (curr.brute_force_score || 0), 0) /
        completed.length
      ).toFixed(1)
    : "0.0";

  const avgOptimized = completed.length
    ? (
        completed.reduce((acc, curr) => acc + (curr.optimized_score || 0), 0) /
        completed.length
      ).toFixed(1)
    : "0.0";

  const avgCode = completed.length
    ? (
        completed.reduce((acc, curr) => acc + (curr.code_score || 0), 0) /
        completed.length
      ).toFixed(1)
    : "0.0";

  // Difficulty counts
  const easyCount = interviews.filter((i) => i.difficulty === "Easy").length;
  const mediumCount = interviews.filter((i) => i.difficulty === "Medium").length;
  const hardCount = interviews.filter((i) => i.difficulty === "Hard").length;

  // Track breakdown mapping
  const trackStats = TRACK_DEFINITIONS.map((t) => {
    const attempts = interviews.filter(
      (i) => i.topic?.toLowerCase() === t.name.toLowerCase() || i.topic === t.id
    ).length;
    return {
      ...t,
      attempts,
      percentage: Math.min(100, Math.round((attempts / t.total) * 100)),
    };
  });

  return (
    <div className="cv-dashboard">
      {/* Top Navigation */}
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
          <Link to="/progress" className="active">
            My Progress
          </Link>
        </nav>

        <Link to="/profile" className="cv-profile-link" aria-label="My profile">
          <span className="cv-avatar">
            {userName !== "there" ? userName.trim().charAt(0).toUpperCase() : "U"}
          </span>
          <span className="cv-profile-name">{userName}</span>
        </Link>
      </header>

      <main className="cv-main">
        {/* Header */}
        <section className="cv-progress-header">
          <div>
            <p className="cv-eyebrow">SKILL ANALYTICS & MASTERY</p>
            <h1>My Interview Progress</h1>
            <p className="cv-progress-subtitle">
              Detailed breakdown of your algorithmic explanations, coding accuracy, and topic coverage.
            </p>
          </div>
          <Link to="/dashboard" className="cv-btn-primary">
            <Play size={16} fill="currentColor" />
            Practice Next Topic
          </Link>
        </section>

        {loading ? (
          <div className="cv-history-loading">
            <Loader2 size={24} className="cv-spin" />
            <span>Analyzing your interview performance...</span>
          </div>
        ) : (
          <>
            {/* Top Stat Cards */}
            <section className="cv-metrics-row">
              <div className="cv-metric-box">
                <div className="cv-metric-header">
                  <span className="cv-metric-title">Interviews Completed</span>
                  <CheckCircle2 size={16} className="cv-metric-icon cv-text-green" />
                </div>
                <div className="cv-metric-number">{completed.length}</div>
                <span className="cv-metric-sub">
                  Out of {interviews.length} sessions started
                </span>
              </div>

              <div className="cv-metric-box">
                <div className="cv-metric-header">
                  <span className="cv-metric-title">Overall Score</span>
                  <Award size={16} className="cv-metric-icon cv-text-red" />
                </div>
                <div className="cv-metric-number">
                  {historyData?.average_overall_score ?? "0.0"}{" "}
                  <span className="cv-stat-dim">/ 10</span>
                </div>
                <span className="cv-metric-sub">Across all 3 interview phases</span>
              </div>

              <div className="cv-metric-box">
                <div className="cv-metric-header">
                  <span className="cv-metric-title">Completion Rate</span>
                  <TrendingUp size={16} className="cv-metric-icon" />
                </div>
                <div className="cv-metric-number">
                  {interviews.length > 0
                    ? Math.round((completed.length / interviews.length) * 100)
                    : 0}
                  %
                </div>
                <span className="cv-metric-sub">Finished full evaluation cycle</span>
              </div>
            </section>

            {/* Performance by Interview Phase */}
            <section className="cv-progress-section">
              <div className="cv-section-heading">
                <div>
                  <p className="cv-eyebrow">SCORE BREAKDOWN</p>
                  <h2>Performance by Phase</h2>
                  <p className="cv-section-subtitle">
                    Average score out of 10 for each stage evaluated by the AI interviewer.
                  </p>
                </div>
              </div>

              <div className="cv-phase-grid">
                <div className="cv-phase-card">
                  <div className="cv-phase-header">
                    <span className="cv-phase-pill">Phase 1</span>
                    <span className="cv-phase-score">{avgBruteForce} / 10</span>
                  </div>
                  <h3>Brute Force Formulation</h3>
                  <p>
                    Evaluates initial problem comprehension, time/space complexity analysis, and edge case identification.
                  </p>
                  <div className="cv-progress-bar-bg">
                    <div
                      className="cv-progress-bar-fill cv-fill-yellow"
                      style={{ width: `${(avgBruteForce / 10) * 100}%` }}
                    />
                  </div>
                </div>

                <div className="cv-phase-card">
                  <div className="cv-phase-header">
                    <span className="cv-phase-pill">Phase 2</span>
                    <span className="cv-phase-score">{avgOptimized} / 10</span>
                  </div>
                  <h3>Optimization Reasoning</h3>
                  <p>
                    Measures capability to identify bottlenecks and transition to optimal data structures.
                  </p>
                  <div className="cv-progress-bar-bg">
                    <div
                      className="cv-progress-bar-fill cv-fill-red"
                      style={{ width: `${(avgOptimized / 10) * 100}%` }}
                    />
                  </div>
                </div>

                <div className="cv-phase-card">
                  <div className="cv-phase-header">
                    <span className="cv-phase-pill">Phase 3</span>
                    <span className="cv-phase-score">{avgCode} / 10</span>
                  </div>
                  <h3>Code Execution & Syntax</h3>
                  <p>
                    Pass rate on public and hidden sandbox test cases under strict runtime execution constraints.
                  </p>
                  <div className="cv-progress-bar-bg">
                    <div
                      className="cv-progress-bar-fill cv-fill-green"
                      style={{ width: `${(avgCode / 10) * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            </section>

            {/* Difficulty & Track Progress Row */}
            <section className="cv-progress-split-row">
              {/* Difficulty Breakdown */}
              <div className="cv-progress-panel cv-panel-diff">
                <div className="cv-section-heading">
                  <div>
                    <p className="cv-eyebrow">DIFFICULTY TIERS</p>
                    <h2>Problems Attempted</h2>
                  </div>
                </div>

                <div className="cv-diff-list">
                  <div className="cv-diff-row">
                    <div className="cv-diff-label">
                      <span className="cv-diff-badge cv-diff-easy">Easy</span>
                      <span>{easyCount} Attempted</span>
                    </div>
                    <div className="cv-progress-bar-bg">
                      <div
                        className="cv-progress-bar-fill cv-fill-green"
                        style={{
                          width: `${
                            interviews.length ? (easyCount / interviews.length) * 100 : 0
                          }%`,
                        }}
                      />
                    </div>
                  </div>

                  <div className="cv-diff-row">
                    <div className="cv-diff-label">
                      <span className="cv-diff-badge cv-diff-medium">Medium</span>
                      <span>{mediumCount} Attempted</span>
                    </div>
                    <div className="cv-progress-bar-bg">
                      <div
                        className="cv-progress-bar-fill cv-fill-yellow"
                        style={{
                          width: `${
                            interviews.length ? (mediumCount / interviews.length) * 100 : 0
                          }%`,
                        }}
                      />
                    </div>
                  </div>

                  <div className="cv-diff-row">
                    <div className="cv-diff-label">
                      <span className="cv-diff-badge cv-diff-hard">Hard</span>
                      <span>{hardCount} Attempted</span>
                    </div>
                    <div className="cv-progress-bar-bg">
                      <div
                        className="cv-progress-bar-fill cv-fill-red"
                        style={{
                          width: `${
                            interviews.length ? (hardCount / interviews.length) * 100 : 0
                          }%`,
                        }}
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* Topic Coverage Breakdown */}
              <div className="cv-progress-panel cv-panel-tracks">
                <div className="cv-section-heading">
                  <div>
                    <p className="cv-eyebrow">CURRICULUM COVERAGE</p>
                    <h2>Track Progress</h2>
                  </div>
                </div>

                <div className="cv-track-bars-list">
                  {trackStats.map((track) => (
                    <div key={track.id} className="cv-track-bar-item">
                      <div className="cv-track-bar-info">
                        <span className="cv-track-bar-name">{track.name}</span>
                        <span className="cv-track-bar-counts">
                          {track.attempts} / {track.total}
                        </span>
                      </div>
                      <div className="cv-progress-bar-bg">
                        <div
                          className="cv-progress-bar-fill cv-fill-red"
                          style={{ width: `${track.percentage}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </section>
          </>
        )}
      </main>

      <footer className="cv-footer">
        <span>© {new Date().getFullYear()} CodeVue</span>
        <span>Practice with purpose.</span>
      </footer>
    </div>
  );
}