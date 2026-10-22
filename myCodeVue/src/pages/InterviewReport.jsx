import React, { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import {
  ArrowLeft,
  Award,
  CheckCircle2,
  Clock,
  Code2,
  Copy,
  Check,
  FileText,
  Loader2,
  Play,
  RotateCcw,
  Sparkles,
  XCircle,
  AlertTriangle,
  Calendar,
} from "lucide-react";
import "./InterviewReport.css";

const API_BASE_URL = (
  import.meta.env.VITE_AI_SERVICE_URL || "http://localhost:8000"
).replace(/\/$/, "");

export default function InterviewReport() {
  const { interviewId } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();

  const userName =
    user?.fullName || localStorage.getItem("userName") || "there";

  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("overview");
  const [copiedCode, setCopiedCode] = useState(false);

  useEffect(() => {
    async function fetchReport() {
      try {
        const res = await fetch(`${API_BASE_URL}/interviews/${interviewId}/report`);
        if (!res.ok) {
          throw new Error(
            res.status === 409
              ? "This interview is still in progress and has not finished yet."
              : "Failed to retrieve interview report."
          );
        }
        const data = await res.json();
        setReport(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    if (interviewId) {
      fetchReport();
    }
  }, [interviewId]);

  const copyCodeToClipboard = () => {
    if (!report?.submitted_code) return;
    navigator.clipboard.writeText(report.submitted_code);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  const formatDate = (timestamp) => {
    if (!timestamp) return "Recent";
    const date = new Date(timestamp * 1000);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (loading) {
    return (
      <div className="cv-dashboard">
        <header className="cv-navbar">
          <Link to="/dashboard" className="cv-brand">
            <div className="cv-brand-icon">
              <span>&lt;</span>
              <span className="greaterThan">&gt;</span>
            </div>
            <span>
              Code<span className="cv-brand-accent">Vue</span>
            </span>
          </Link>
        </header>
        <div className="cv-report-loading-container">
          <Loader2 size={32} className="cv-spin" />
          <h2>Compiling Interview Report...</h2>
          <p>Gathering AI performance evaluations, code reviews, and test telemetry.</p>
        </div>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="cv-dashboard">
        <header className="cv-navbar">
          <Link to="/dashboard" className="cv-brand">
            <div className="cv-brand-icon">
              <span>&lt;</span>
              <span className="greaterThan">&gt;</span>
            </div>
            <span>
              Code<span className="cv-brand-accent">Vue</span>
            </span>
          </Link>
        </header>
        <div className="cv-report-error-container">
          <AlertTriangle size={36} className="cv-text-red" />
          <h2>Report Not Available</h2>
          <p>{error || "Unable to locate this interview record."}</p>
          <div className="cv-error-actions">
            <Link to="/mock-interviews" className="cv-btn-secondary">
              <ArrowLeft size={16} /> Back to History
            </Link>
            <Link to="/dashboard" className="cv-btn-primary">
              Launch New Interview
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Calculate composite metrics
  const bfScore = report.brute_force_score || 0;
  const optScore = report.optimized_score || 0;
  const codeScore = report.code_score || 0;
  const overallScore = Number(((bfScore + optScore + codeScore) / 3).toFixed(1));

  // Hiring recommendation tier
  let recommendation = { label: "Strong Hire", color: "cv-rec-strong" };
  if (overallScore < 5.0) {
    recommendation = { label: "Needs Practice", color: "cv-rec-needs-work" };
  } else if (overallScore < 7.0) {
    recommendation = { label: "Lean Hire", color: "cv-rec-lean" };
  } else if (overallScore < 8.5) {
    recommendation = { label: "Hire", color: "cv-rec-hire" };
  }

  const testResults = report.test_results || [];
  const passedTestsCount = testResults.filter((t) => t.passed).length;

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

        <Link to="/profile" className="cv-profile-link" aria-label="My profile">
          <span className="cv-avatar">
            {userName !== "there" ? userName.trim().charAt(0).toUpperCase() : "U"}
          </span>
          <span className="cv-profile-name">{userName}</span>
        </Link>
      </header>

      <main className="cv-main">
        {/* Navigation Breadcrumb */}
        <div className="cv-report-breadcrumb">
          <Link to="/mock-interviews" className="cv-back-link">
            <ArrowLeft size={14} /> Back to Mock Interviews
          </Link>
          <span className="cv-breadcrumb-dot">•</span>
          <span className="cv-breadcrumb-id">Session: {report.interview_id.slice(0, 8)}...</span>
        </div>

        {/* Executive Summary Hero */}
        <section className="cv-report-hero">
          <div className="cv-report-hero-info">
            <div className="cv-report-badges-row">
              <span className="cv-topic-badge">{report.topic}</span>
              <span className={`cv-diff-badge cv-diff-${report.difficulty?.toLowerCase()}`}>
                {report.difficulty}
              </span>
              <span className="cv-date-badge">
                <Calendar size={13} /> {formatDate(report.started_at)}
              </span>
            </div>
            <h1>{report.problem_title}</h1>
            <p className="cv-report-subtitle">
              Interview Evaluation Report & Technical Assessment Breakdown
            </p>
          </div>

          <div className="cv-report-hero-actions">
            <Link
              to={`/interview/${report.problem_id}`}
              className="cv-btn-secondary"
            >
              <RotateCcw size={15} /> Retake Problem
            </Link>
            <Link to="/dashboard" className="cv-btn-primary">
              <Play size={15} fill="currentColor" /> Next Problem
            </Link>
          </div>
        </section>

        {/* Scorecard Hero Cards */}
        <section className="cv-scorecard-grid">
          {/* Main Rating */}
          <div className="cv-scorecard-box cv-scorecard-main">
            <div className="cv-scorecard-header">
              <span>Overall Evaluation</span>
              <Award size={18} className="cv-text-red" />
            </div>
            <div className="cv-scorecard-value">
              {overallScore} <span className="cv-scorecard-dim">/ 10</span>
            </div>
            <div className={`cv-recommendation-pill ${recommendation.color}`}>
              {recommendation.label}
            </div>
          </div>

          {/* Phase 1: Brute Force */}
          <div className="cv-scorecard-box">
            <div className="cv-scorecard-header">
              <span>1. Brute Force</span>
              <Sparkles size={16} className="cv-metric-icon" />
            </div>
            <div className="cv-scorecard-value">
              {bfScore} <span className="cv-scorecard-dim">/ 10</span>
            </div>
            <span className="cv-scorecard-sub">Algorithmic baseline</span>
          </div>

          {/* Phase 2: Optimization */}
          <div className="cv-scorecard-box">
            <div className="cv-scorecard-header">
              <span>2. Optimization</span>
              <Award size={16} className="cv-metric-icon" />
            </div>
            <div className="cv-scorecard-value">
              {optScore} <span className="cv-scorecard-dim">/ 10</span>
            </div>
            <span className="cv-scorecard-sub">Data structure reasoning</span>
          </div>

          {/* Phase 3: Code Execution */}
          <div className="cv-scorecard-box">
            <div className="cv-scorecard-header">
              <span>3. Code Sandbox</span>
              <Code2 size={16} className="cv-metric-icon" />
            </div>
            <div className="cv-scorecard-value">
              {codeScore} <span className="cv-scorecard-dim">/ 10</span>
            </div>
            <span className="cv-scorecard-sub">
              {passedTestsCount}/{testResults.length} test cases passed
            </span>
          </div>
        </section>

        {/* Tab Navigation */}
        <div className="cv-report-tabs">
          <button
            className={`cv-report-tab ${activeTab === "overview" ? "active" : ""}`}
            onClick={() => setActiveTab("overview")}
          >
            <FileText size={15} /> AI Summary Report
          </button>
          <button
            className={`cv-report-tab ${activeTab === "discussion" ? "active" : ""}`}
            onClick={() => setActiveTab("discussion")}
          >
            <Sparkles size={15} /> Discussion Transcripts
          </button>
          <button
            className={`cv-report-tab ${activeTab === "code" ? "active" : ""}`}
            onClick={() => setActiveTab("code")}
          >
            <Code2 size={15} /> Submitted Code & Tests
          </button>
        </div>

        {/* Tab 1: AI Summary Report */}
        {activeTab === "overview" && (
          <section className="cv-report-panel">
            <div className="cv-panel-header">
              <div className="cv-panel-title-group">
                <FileText size={18} className="cv-text-red" />
                <h3>Comprehensive AI Feedback</h3>
              </div>
              <span className="cv-finish-badge">
                Submission Status: {report.finish_reason === "submitted" ? "Completed" : "Timed Out"}
              </span>
            </div>

            <div className="cv-markdown-content">
              {report.final_report ? (
                <div className="cv-report-text-block">
                  {report.final_report.split("\n\n").map((para, idx) => (
                    <p key={idx}>{para}</p>
                  ))}
                </div>
              ) : (
                <p className="cv-empty-text">No narrative report text recorded for this session.</p>
              )}
            </div>
          </section>
        )}

        {/* Tab 2: Discussion Transcripts */}
        {activeTab === "discussion" && (
          <div className="cv-discussions-container">
            {/* Brute Force Phase Box */}
            <div className="cv-report-panel">
              <div className="cv-panel-header">
                <div className="cv-panel-title-group">
                  <span className="cv-phase-pill">Phase 1</span>
                  <h3>Brute Force Discussion</h3>
                </div>
                <span className="cv-panel-score">{bfScore} / 10</span>
              </div>

              <div className="cv-discussion-block">
                <div className="cv-bubble-group">
                  <div className="cv-bubble-author candidate">Your Explanation</div>
                  <div className="cv-bubble-text">
                    {report.brute_force_answer || <em>No explanation submitted.</em>}
                  </div>
                </div>

                <div className="cv-bubble-group">
                  <div className="cv-bubble-author interviewer">Interviewer Feedback</div>
                  <div className="cv-bubble-text feedback">
                    {report.brute_force_feedback || <em>No critique generated.</em>}
                  </div>
                </div>
              </div>
            </div>

            {/* Optimization Phase Box */}
            <div className="cv-report-panel">
              <div className="cv-panel-header">
                <div className="cv-panel-title-group">
                  <span className="cv-phase-pill">Phase 2</span>
                  <h3>Optimization Discussion</h3>
                </div>
                <span className="cv-panel-score">{optScore} / 10</span>
              </div>

              <div className="cv-discussion-block">
                <div className="cv-bubble-group">
                  <div className="cv-bubble-author candidate">Your Explanation</div>
                  <div className="cv-bubble-text">
                    {report.optimized_answer || <em>No explanation submitted.</em>}
                  </div>
                </div>

                <div className="cv-bubble-group">
                  <div className="cv-bubble-author interviewer">Interviewer Feedback</div>
                  <div className="cv-bubble-text feedback">
                    {report.optimized_feedback || <em>No critique generated.</em>}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: Submitted Code & Sandbox Execution */}
        {activeTab === "code" && (
          <div className="cv-code-tab-container">
            {/* Code Editor Preview */}
            <div className="cv-report-panel">
              <div className="cv-panel-header">
                <div className="cv-panel-title-group">
                  <Code2 size={18} className="cv-text-red" />
                  <h3>Submitted Solution</h3>
                  <span className="cv-lang-tag">
                    {report.programming_language?.toUpperCase() || "CPP"}
                  </span>
                </div>
                <button
                  className="cv-copy-btn"
                  onClick={copyCodeToClipboard}
                  title="Copy code to clipboard"
                >
                  {copiedCode ? <Check size={14} /> : <Copy size={14} />}
                  {copiedCode ? "Copied" : "Copy Code"}
                </button>
              </div>

              {report.submitted_code ? (
                <pre className="cv-code-display">
                  <code>{report.submitted_code}</code>
                </pre>
              ) : (
                <div className="cv-no-code">
                  <AlertTriangle size={24} className="cv-subtle" />
                  <p>No code was submitted before the coding deadline elapsed.</p>
                </div>
              )}
            </div>

            {/* Test Case Breakdown */}
            <div className="cv-report-panel">
              <div className="cv-panel-header">
                <div className="cv-panel-title-group">
                  <CheckCircle2 size={18} className="cv-text-green" />
                  <h3>Sandbox Test Results</h3>
                </div>
                <span className="cv-panel-score">
                  {passedTestsCount} / {testResults.length} Passed
                </span>
              </div>

              {testResults.length > 0 ? (
                <div className="cv-test-results-list">
                  {testResults.map((tc, idx) => (
                    <div
                      key={idx}
                      className={`cv-test-case-card ${tc.passed ? "passed" : "failed"}`}
                    >
                      <div className="cv-tc-header">
                        <span className="cv-tc-index">Test Case #{tc.test_case || idx + 1}</span>
                        <span className={`cv-tc-badge ${tc.passed ? "passed" : "failed"}`}>
                          {tc.passed ? (
                            <>
                              <CheckCircle2 size={13} /> Passed
                            </>
                          ) : (
                            <>
                              <XCircle size={13} /> {tc.status || "Failed"}
                            </>
                          )}
                        </span>
                      </div>

                      <div className="cv-tc-body">
                        <div className="cv-tc-io">
                          <span className="cv-tc-label">Input</span>
                          <span className="cv-tc-value">
                            {typeof tc.input === "object"
                              ? JSON.stringify(tc.input)
                              : String(tc.input)}
                          </span>
                        </div>

                        <div className="cv-tc-io">
                          <span className="cv-tc-label">Expected</span>
                          <span className="cv-tc-value">
                            {typeof tc.expected === "object"
                              ? JSON.stringify(tc.expected)
                              : String(tc.expected)}
                          </span>
                        </div>

                        <div className="cv-tc-io">
                          <span className="cv-tc-label">Actual</span>
                          <span className={`cv-tc-value ${tc.passed ? "" : "cv-diff-failed"}`}>
                            {tc.actual !== undefined && tc.actual !== null
                              ? typeof tc.actual === "object"
                                ? JSON.stringify(tc.actual)
                                : String(tc.actual)
                              : tc.error || "null"}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="cv-empty-text">No individual test executions were recorded.</p>
              )}
            </div>
          </div>
        )}
      </main>

      <footer className="cv-footer">
        <span>© {new Date().getFullYear()} CodeVue</span>
        <span>Practice with purpose.</span>
      </footer>
    </div>
  );
}