import React, { useState, useEffect, useRef, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import Editor from "@monaco-editor/react";
import {
  ArrowLeft,
  Clock,
  Send,
  Code2,
  CheckCircle2,
  XCircle,
  AlertCircle,
  Loader2,
  Terminal,
  FileText,
  AlertTriangle,
  Play,
  RotateCcw,
  ChevronUp,
  ChevronDown
} from "lucide-react";
import "./InterviewWorkspace.css";

const API_BASE_URL = (
  import.meta.env.VITE_AI_SERVICE_URL || "http://localhost:8000"
).replace(/\/$/, "");

const DEFAULT_FALLBACK_CODE = {
  cpp: `class Solution {\npublic:\n    // Implement your solution\n};`,
  python: `class Solution:\n    # Implement your solution\n    pass`,
  java: `class Solution {\n    // Implement your solution\n}`
};

export default function InterviewWorkspace() {
  const { questionId } = useParams();

  // Core state
  const [interview, setInterview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Discussion state
  const [userAnswer, setUserAnswer] = useState("");
  const [isSubmittingAnswer, setIsSubmittingAnswer] = useState(false);
  const [discussionHistory, setDiscussionHistory] = useState([]);

  // Code editor state
  const [language, setLanguage] = useState("python");
  const [code, setCode] = useState(DEFAULT_FALLBACK_CODE.python);
  const [isSubmittingCode, setIsSubmittingCode] = useState(false);

  // Execution & Test Console state
  const [isRunningCode, setIsRunningCode] = useState(false);
  const [testOutput, setTestOutput] = useState(null);
  const [isConsoleOpen, setIsConsoleOpen] = useState(false);

  // Final Report state
  const [report, setReport] = useState(null);
  const [loadingReport, setLoadingReport] = useState(false);

  // Timers
  const [overallTimeRemaining, setOverallTimeRemaining] = useState(null);
  const [codingTimeRemaining, setCodingTimeRemaining] = useState(null);

  const startedQuestionRef = useRef(null);
  const chatScrollRef = useRef(null);

  const getProblemStarterCode = (interviewData, lang) => {
    if (interviewData?.starter_code && interviewData.starter_code[lang]) {
      return interviewData.starter_code[lang];
    }
    return DEFAULT_FALLBACK_CODE[lang] || "";
  };

  // 1. Initialize Interview
  useEffect(() => {
    if (!questionId) return;
    if (startedQuestionRef.current === questionId) return;

    startedQuestionRef.current = questionId;

    async function startSession() {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`${API_BASE_URL}/interviews/start`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ problem_id: questionId.trim() }),
        });

        if (!response.ok) {
          const errData = await response.json().catch(() => ({}));
          throw new Error(errData.detail || `Failed to start interview (${response.status})`);
        }

        const data = await response.json();
        setInterview(data);

        const initialCode = getProblemStarterCode(data, "python");
        setCode(initialCode);

        if (data.current_question) {
          setDiscussionHistory([
            { role: "interviewer", text: data.current_question, phase: data.phase },
          ]);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    startSession();
  }, [questionId]);

  // 2. Poll Status
  const pollStatus = useCallback(async () => {
    if (!interview?.interview_id || interview.phase === "finished") return;

    try {
      const res = await fetch(`${API_BASE_URL}/interviews/${interview.interview_id}`);
      if (!res.ok) return;

      const data = await res.json();
      setInterview((prev) => ({ ...prev, ...data }));

      if (data.phase === "finished" && !report) {
        fetchReport(data.interview_id);
      }
    } catch {
      // Ignore background fetch blips
    }
  }, [interview?.interview_id, interview?.phase, report]);

  useEffect(() => {
    if (!interview || interview.phase === "finished") return;
    const interval = setInterval(pollStatus, 3000);
    return () => clearInterval(interval);
  }, [interview, pollStatus]);

  // 3. Countdown Timers
  useEffect(() => {
    if (!interview || interview.phase === "finished") return;

    const timer = setInterval(() => {
      const now = Date.now() / 1000;

      if (interview.started_at && interview.duration_seconds) {
        const deadline = interview.started_at + interview.duration_seconds;
        setOverallTimeRemaining(Math.max(0, Math.floor(deadline - now)));
      }

      if (interview.phase === "coding" && interview.coding_started_at && interview.coding_duration_seconds) {
        const codingDeadline = interview.coding_started_at + interview.coding_duration_seconds;
        setCodingTimeRemaining(Math.max(0, Math.floor(codingDeadline - now)));
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [interview]);

  useEffect(() => {
    if (chatScrollRef.current) {
      chatScrollRef.current.scrollTop = chatScrollRef.current.scrollHeight;
    }
  }, [discussionHistory]);

  const formatTime = (secs) => {
    if (secs === null || secs === undefined) return "--:--";
    const minutes = Math.floor(secs / 60);
    const seconds = secs % 60;
    return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
  };

  // 4. Handle Discussion Submission
  const handleAnswerSubmit = async (e) => {
    e.preventDefault();
    if (!userAnswer.trim() || isSubmittingAnswer || !interview) return;

    const answerText = userAnswer.trim();
    setUserAnswer("");
    setIsSubmittingAnswer(true);

    setDiscussionHistory((prev) => [...prev, { role: "candidate", text: answerText }]);

    try {
      const res = await fetch(`${API_BASE_URL}/interviews/${interview.interview_id}/answer`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ answer: answerText }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Failed to submit explanation.");
      }

      const updated = await res.json();
      setInterview(updated);

      let feedback = updated.optimized_feedback || updated.brute_force_feedback || "";
      const nextMessages = [];

      if (feedback) {
        nextMessages.push({ role: "system_feedback", text: feedback });
      }

      if (updated.current_question && updated.phase !== "finished") {
        nextMessages.push({ role: "interviewer", text: updated.current_question, phase: updated.phase });
      }

      setDiscussionHistory((prev) => [...prev, ...nextMessages]);
    } catch (err) {
      setDiscussionHistory((prev) => [...prev, { role: "error", text: err.message }]);
    } finally {
      setIsSubmittingAnswer(false);
    }
  };

  // 5. Handle Run Code (Sandbox Execution)
  const handleRunCode = async () => {
    if (!interview || isRunningCode) return;

    setIsRunningCode(true);
    setIsConsoleOpen(true);
    setTestOutput({ status: "running" });

    try {
      const res = await fetch(`${API_BASE_URL}/interviews/${interview.interview_id}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code: code,
          programming_language: language,
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Failed to execute code.");
      }

      setTestOutput(data);
    } catch (err) {
      setTestOutput({
        success: False,
        error: err.message,
        results: [],
      });
    } finally {
      setIsRunningCode(false);
    }
  };

  // 6. Handle Final Code Submission
  const handleCodeSubmit = async () => {
    if (!interview || isSubmittingCode) return;

    const confirmSubmit = window.confirm(
      "Submit final code? Your solution will be compiled and evaluated against all hidden test cases to complete the interview."
    );
    if (!confirmSubmit) return;

    setIsSubmittingCode(true);

    try {
      const res = await fetch(`${API_BASE_URL}/interviews/${interview.interview_id}/code`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code: code,
          programming_language: language,
        }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Failed to submit code.");
      }

      const updated = await res.json();
      setInterview(updated);
      fetchReport(updated.interview_id);
    } catch (err) {
      alert(`Submission error: ${err.message}`);
    } finally {
      setIsSubmittingCode(false);
    }
  };

  const fetchReport = async (interviewId) => {
    setLoadingReport(true);
    try {
      const res = await fetch(`${API_BASE_URL}/interviews/${interviewId}/report`);
      if (res.ok) {
        const data = await res.json();
        setReport(data);
      }
    } catch (err) {
      console.error("Could not fetch report:", err);
    } finally {
      setLoadingReport(false);
    }
  };

  const handleLanguageChange = (newLang) => {
    setLanguage(newLang);
    setCode(getProblemStarterCode(interview, newLang));
  };

  if (loading) {
    return (
      <div className="cv-workspace-state-screen">
        <Loader2 className="cv-spin" size={40} />
        <h2>Setting up your interview workspace...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="cv-workspace-state-screen">
        <AlertCircle size={44} className="cv-danger-icon" />
        <h2>Unable to Initialize Workspace</h2>
        <p className="cv-error-message">{error}</p>
        <div className="cv-state-actions">
          <Link to="/dashboard" className="cv-btn cv-btn-primary">
            <ArrowLeft size={16} /> Return to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="cv-workspace-container">
      {/* Top Navbar */}
      <header className="cv-workspace-header">
        <div className="cv-workspace-header-left">
          <Link to={`/tracks/${interview?.topic || "arrays-strings"}`} className="cv-back-link" title="Exit">
            <ArrowLeft size={18} />
          </Link>
          <div className="cv-problem-meta">
            <h1 className="cv-problem-title">{interview?.problem_title || "Coding Interview"}</h1>
            <span className={`cv-badge cv-badge-${interview?.difficulty?.toLowerCase()}`}>
              {interview?.difficulty}
            </span>
            <span className="cv-topic-tag">{interview?.topic}</span>
          </div>
        </div>

        {/* Phase Stepper */}
        <div className="cv-phase-stepper">
          <div className={`cv-step ${interview?.phase === "brute_force" ? "active" : "completed"}`}>
            1. Brute Force
          </div>
          <div className="cv-step-divider" />
          <div
            className={`cv-step ${
              interview?.phase === "optimized"
                ? "active"
                : ["coding", "finished"].includes(interview?.phase)
                ? "completed"
                : ""
            }`}
          >
            2. Optimization
          </div>
          <div className="cv-step-divider" />
          <div
            className={`cv-step ${
              interview?.phase === "coding"
                ? "active"
                : interview?.phase === "finished"
                ? "completed"
                : ""
            }`}
          >
            3. Code
          </div>
        </div>

        {/* Timers */}
        <div className="cv-workspace-header-right">
          <div className="cv-timer-group">
            <Clock size={16} className="cv-timer-icon" />
            <div className="cv-timer-labels">
              <span className="cv-timer-sub">Interview</span>
              <span className="cv-timer-val">{formatTime(overallTimeRemaining)}</span>
            </div>
          </div>

          {interview?.phase === "coding" && (
            <div className="cv-timer-group cv-timer-coding">
              <Code2 size={16} className="cv-timer-icon-red" />
              <div className="cv-timer-labels">
                <span className="cv-timer-sub">Coding Time</span>
                <span className="cv-timer-val cv-text-red">{formatTime(codingTimeRemaining)}</span>
              </div>
            </div>
          )}
        </div>
      </header>

      {/* Main Split Layout */}
      <div className="cv-workspace-body">
        {/* Left Pane: Description & Discussion */}
        <section className="cv-pane cv-left-pane">
          <div className="cv-card cv-problem-card">
            <div className="cv-card-header">
              <FileText size={16} className="cv-card-icon" />
              <h3>Problem Description</h3>
            </div>
            <div className="cv-card-body">
              <p className="cv-problem-description">{interview?.problem}</p>

              {interview?.examples?.length > 0 && (
                <div className="cv-section-block">
                  <h4>Examples</h4>
                  {interview.examples.map((ex, idx) => (
                    <div key={idx} className="cv-example-box">
                      {typeof ex === "string" ? (
                        <pre>{ex}</pre>
                      ) : (
                        <>
                          <div><strong>Input:</strong> <code>{ex.input}</code></div>
                          <div><strong>Output:</strong> <code>{ex.output}</code></div>
                          {ex.explanation && <div><strong>Explanation:</strong> {ex.explanation}</div>}
                        </>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {interview?.constraints?.length > 0 && (
                <div className="cv-section-block">
                  <h4>Constraints</h4>
                  <ul className="cv-constraints-list">
                    {interview.constraints.map((c, idx) => (
                      <li key={idx}><code>{c}</code></li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          <div className="cv-card cv-discussion-card">
            <div className="cv-card-header">
              <Terminal size={16} className="cv-card-icon" />
              <h3>AI Interviewer Discussion</h3>
              <span className="cv-active-phase-label">{interview?.phase}</span>
            </div>

            <div className="cv-discussion-history" ref={chatScrollRef}>
              {discussionHistory.map((item, index) => (
                <div key={index} className={`cv-chat-bubble cv-bubble-${item.role}`}>
                  {item.role === "interviewer" && <div className="cv-bubble-title">Interviewer</div>}
                  {item.role === "candidate" && <div className="cv-bubble-title cv-candidate-title">You</div>}
                  {item.role === "system_feedback" && (
                    <div className="cv-bubble-title cv-feedback-title">
                      <CheckCircle2 size={13} /> Evaluation Feedback
                    </div>
                  )}
                  {item.role === "error" && (
                    <div className="cv-bubble-title cv-error-title">
                      <AlertTriangle size={13} /> Error
                    </div>
                  )}
                  <p className="cv-bubble-text">{item.text}</p>
                </div>
              ))}
            </div>

            {["brute_force", "optimized"].includes(interview?.phase) ? (
              <form onSubmit={handleAnswerSubmit} className="cv-discussion-input-panel">
                <textarea
                  className="cv-textarea"
                  rows={3}
                  placeholder="Explain your approach, complexity, and boundary checks..."
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  disabled={isSubmittingAnswer}
                />
                <button
                  type="submit"
                  className="cv-btn cv-btn-primary"
                  disabled={isSubmittingAnswer || !userAnswer.trim()}
                >
                  {isSubmittingAnswer ? (
                    <><Loader2 className="cv-spin" size={14} /> Evaluating...</>
                  ) : (
                    <><Send size={14} /> Submit Explanation</>
                  )}
                </button>
              </form>
            ) : interview?.phase === "coding" ? (
              <div className="cv-discussion-notice">
                <CheckCircle2 size={18} className="cv-text-green" />
                <span>Discussion completed. Write, test, and submit your code in the editor.</span>
              </div>
            ) : (
              <div className="cv-discussion-notice">
                <span>The interview has concluded.</span>
              </div>
            )}
          </div>
        </section>

        {/* Right Pane: Code Editor & Execution Console */}
        <section className="cv-pane cv-right-pane">
          <div className="cv-card cv-editor-card">
            {/* Toolbar */}
            <div className="cv-editor-toolbar">
              <div className="cv-editor-toolbar-left">
                <label htmlFor="lang-select" className="cv-field-label">Language:</label>
                <select
                  id="lang-select"
                  className="cv-select"
                  value={language}
                  onChange={(e) => handleLanguageChange(e.target.value)}
                  disabled={interview?.phase === "finished"}
                >
                  <option value="python">Python 3</option>
                  <option value="cpp">C++ (GCC)</option>
                  <option value="java">Java 17</option>
                </select>
              </div>

              <div className="cv-editor-toolbar-right">
                <button
                  type="button"
                  className="cv-btn cv-btn-secondary"
                  onClick={() => setCode(getProblemStarterCode(interview, language))}
                  disabled={interview?.phase === "finished"}
                  title="Reset code"
                >
                  <RotateCcw size={14} /> Reset
                </button>
              </div>
            </div>

            {/* Monaco Container */}
            <div className="cv-monaco-wrapper">
              <Editor
                height="100%"
                language={language === "cpp" ? "cpp" : language === "python" ? "python" : "java"}
                theme="vs-dark"
                value={code}
                onChange={(val) => setCode(val || "")}
                options={{
                  fontSize: 14,
                  minimap: { enabled: false },
                  scrollBeyondLastLine: false,
                  automaticLayout: true,
                  tabSize: 4,
                  readOnly: interview?.phase === "finished",
                }}
              />
            </div>

            {/* Expandable Test Results Drawer */}
            {isConsoleOpen && (
              <div className="cv-console-drawer">
                <div className="cv-console-header" onClick={() => setIsConsoleOpen(!isConsoleOpen)}>
                  <div className="cv-console-title">
                    <Terminal size={14} />
                    <span>Test Cases Output</span>
                    {testOutput && !testOutput.error && (
                      <span className={`cv-console-badge ${testOutput.passed_tests === testOutput.total_tests ? "passed" : "failed"}`}>
                        {testOutput.passed_tests} / {testOutput.total_tests} Passed
                      </span>
                    )}
                  </div>
                  <button type="button" className="cv-console-toggle">
                    {isConsoleOpen ? <ChevronDown size={14} /> : <ChevronUp size={14} />}
                  </button>
                </div>

                <div className="cv-console-body">
                  {testOutput?.status === "running" ? (
                    <div className="cv-console-loading">
                      <Loader2 className="cv-spin" size={18} />
                      <span>Running code in execution sandbox...</span>
                    </div>
                  ) : testOutput?.error ? (
                    <div className="cv-console-error">
                      <AlertCircle size={16} />
                      <pre>{testOutput.error}</pre>
                    </div>
                  ) : testOutput?.results ? (
                    <div className="cv-console-tests-list">
                      {testOutput.results.map((r, i) => (
                        <div key={i} className={`cv-console-test-item ${r.passed ? "test-pass" : "test-fail"}`}>
                          <div className="cv-test-item-header">
                            {r.passed ? (
                              <CheckCircle2 size={14} className="cv-text-green" />
                            ) : (
                              <XCircle size={14} className="cv-text-red" />
                            )}
                            <strong>Test Case {r.test_case}</strong>
                            <span className="cv-test-status">{r.status}</span>
                          </div>
                          <div className="cv-test-io-grid">
                            <div>
                              <span>Input:</span> <code>{JSON.stringify(r.input)}</code>
                            </div>
                            <div>
                              <span>Expected:</span> <code>{JSON.stringify(r.expected)}</code>
                            </div>
                            <div>
                              <span>Actual:</span> <code>{JSON.stringify(r.actual)}</code>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : null}
                </div>
              </div>
            )}

            {/* Actions Bar */}
            <div className="cv-editor-actions">
              <div className="cv-actions-left">
                <button
                  type="button"
                  className="cv-btn cv-btn-secondary"
                  onClick={handleRunCode}
                  disabled={isRunningCode || interview?.phase === "finished"}
                >
                  {isRunningCode ? (
                    <><Loader2 className="cv-spin" size={14} /> Running...</>
                  ) : (
                    <><Play size={14} /> Run Code</>
                  )}
                </button>
              </div>

              <div className="cv-actions-right">
                {interview?.phase === "coding" ? (
                  <button
                    type="button"
                    className="cv-btn cv-btn-primary"
                    onClick={handleCodeSubmit}
                    disabled={isSubmittingCode || !code.trim()}
                  >
                    {isSubmittingCode ? (
                      <><Loader2 className="cv-spin" size={14} /> Evaluating...</>
                    ) : (
                      <><CheckCircle2 size={14} /> Submit Final Code</>
                    )}
                  </button>
                ) : interview?.phase === "finished" ? (
                  <span className="cv-tag-finished">Interview Finished</span>
                ) : (
                  <span className="cv-sub-hint">
                    Complete discussion phase to unlock final submission
                  </span>
                )}
              </div>
            </div>
          </div>
        </section>
      </div>

      {/* Final Report Modal */}
      {interview?.phase === "finished" && (
        <div className="cv-report-overlay">
          <div className="cv-report-modal">
            <div className="cv-report-header">
              <h2>Interview Complete</h2>
              <span className="cv-badge cv-badge-red">
                Status: {interview.finish_reason || "Finished"}
              </span>
            </div>

            <div className="cv-report-content">
              {loadingReport ? (
                <div className="cv-report-loading">
                  <Loader2 className="cv-spin" size={24} />
                  <p>Generating comprehensive interview evaluation...</p>
                </div>
              ) : report ? (
                <div className="cv-report-details">
                  <div className="cv-scores-grid">
                    <div className="cv-score-card">
                      <span className="cv-score-label">Brute Force Score</span>
                      <span className="cv-score-val">{report.brute_force_score ?? "--"} / 10</span>
                    </div>
                    <div className="cv-score-card">
                      <span className="cv-score-label">Optimization Score</span>
                      <span className="cv-score-val">{report.optimized_score ?? "--"} / 10</span>
                    </div>
                    <div className="cv-score-card">
                      <span className="cv-score-label">Code Score</span>
                      <span className="cv-score-val">{report.code_score ?? "--"} / 10</span>
                    </div>
                  </div>

                  <div className="cv-report-text-block">
                    <h3>AI Evaluator Evaluation</h3>
                    <div className="cv-report-markdown">
                      {report.final_report || "Report generated."}
                    </div>
                  </div>
                </div>
              ) : (
                <p>Could not load report.</p>
              )}
            </div>

            <div className="cv-report-footer">
              <Link to={`/tracks/${interview?.topic || "arrays-strings"}`} className="cv-btn cv-btn-primary">
                Return to Track Questions
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}