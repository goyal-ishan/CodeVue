import React, { useState } from 'react';
import { Play, Upload, Mic, CheckCircle2, FileCode2, Check } from 'lucide-react';
import './InterviewSession.css';

export default function InterviewSession() {
    const [isRunning, setIsRunning] = useState(false);

    const lineNumbers = Array.from(
        { length: 15 },
        (_, i) => String(i + 1).padStart(2, '0')
    );

    return (
        <div className="codevue-session-container">

            <header className="session-header">
                <div className="session-header-left">
                    <div className="mac-traffic-dots">
                        <span className="dot close" />
                        <span className="dot minimize" />
                        <span className="dot expand" />
                    </div>

                    <span className="session-title">
                        Session #8492 // Live Stage: Round 2 System &amp; Algorithmic Logic
                    </span>
                </div>

                <div className="session-header-right">
                    <div className="voice-badge">
                        <span>VOICE STREAMING ACTIVE</span>

                        <div className="voice-wave-mini">
                            <span className="wave-bar" />
                            <span className="wave-bar" />
                            <span className="wave-bar" />
                        </div>
                    </div>

                    <span className="session-timer">42:15</span>
                </div>
            </header>


            <div className="session-body">

                <aside className="interviewer-sidebar">

                    <div>

                        <div className="interviewer-profile">

                            <div className="interviewer-profile-info">

                                <div className="interviewer-avatar">
                                    <img
                                        src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80"
                                        alt="Maya Vance"
                                    />
                                </div>

                                <div>
                                    <h4 className="interviewer-name">
                                        Maya Vance
                                    </h4>

                                    <p className="interviewer-role">
                                        Principal Systems AI • CodeVue
                                    </p>
                                </div>

                            </div>

                            <div className="voice-wave-mini">
                                <span className="wave-bar" />
                                <span className="wave-bar" />
                                <span className="wave-bar" />
                            </div>

                        </div>


                        <div className="equalizer-live">
                            <span className="eq-bar" />
                            <span className="eq-bar" />
                            <span className="eq-bar active" />
                            <span className="eq-bar" />
                            <span className="eq-bar" />
                            <span className="eq-bar" />
                            <span className="eq-bar active" />
                            <span className="eq-bar" />
                            <span className="eq-bar" />
                            <span className="eq-bar active" />
                            <span className="eq-bar" />
                            <span className="eq-bar" />
                        </div>


                        <div className="interviewer-prompt-card">
                            Maya: "Your hashmap lookup is clean. But in{' '}
                            <strong>get()</strong>, how do we guarantee{' '}
                            <strong>O(1)</strong> node reordering without
                            mutating existing references?"
                        </div>


                        <div className="problem-spec-section">

                            <div className="problem-spec-header">
                                <span className="spec-label">
                                    // PROBLEM SPECIFICATION
                                </span>

                                <span className="badge-hard">
                                    HARD
                                </span>
                            </div>

                            <h3 className="problem-title">
                                Design LRU Cache
                            </h3>

                            <p className="problem-description">
                                Design a data structure that follows the
                                constraints of a Least Recently Used (LRU)
                                cache. Implement both get and put operations
                                with average O(1) time complexity.
                            </p>

                            <ul className="problem-checklist">

                                <li>
                                    <Check />
                                    Capacity bounds: 1 &le; capacity &le; 3000
                                </li>

                                <li>
                                    <Check />
                                    Thread-safe evaluation harness
                                </li>

                            </ul>

                        </div>

                    </div>


                    <div className="speech-input-bar">

                        <span className="speech-label">
                            SPEECH INPUT
                        </span>

                        <div className="listening-indicator">
                            <Mic size={14} />
                            <span>Listening...</span>
                        </div>

                    </div>

                </aside>


                <main className="editor-main">

                    <div>

                        <div className="editor-tabs-bar">

                            <div className="tab-group">

                                <div className="editor-tab">
                                    <FileCode2 size={13} color="#f87171" />
                                    <span>solution.py</span>
                                </div>

                                <span className="editor-lang">
                                    Python 3.11
                                </span>

                            </div>


                            <div className="editor-actions">

                                <button
                                    type="button"
                                    className="btn-secondary"
                                    onClick={() => setIsRunning(!isRunning)}
                                >
                                    <Play
                                        size={11}
                                        fill="currentColor"
                                    />
                                    <span>Run Tests</span>
                                </button>

                                <button
                                    type="button"
                                    className="btn-primary"
                                >
                                    <Upload size={11} />
                                    <span>Submit Solution</span>
                                </button>

                            </div>

                        </div>


                        <div className="code-canvas">

                            <div className="line-numbers">
                                {lineNumbers.map((num) => (
                                    <div key={num}>{num}</div>
                                ))}
                            </div>


                            <pre className="code-content">
                                <code>
                                    <span className="kw">class</span>{' '}
                                    <span className="fn">Node</span>:
                                    {"\n"}

                                    {'  '}
                                    <span className="kw">def</span>{' '}
                                    <span className="fn">__init__</span>
                                    (<span className="var">self, key, val</span>):
                                    {"\n"}

                                    {'  '}
                                    <span className="var">
                                        self.key, self.val = key, val
                                    </span>
                                    {"\n"}

                                    {'  '}
                                    <span className="var">
                                        self.prev = self.next = None
                                    </span>
                                    {"\n\n"}

                                    <span className="kw">class</span>{' '}
                                    <span className="fn">LRUCache</span>:
                                    {"\n"}

                                    {'  '}
                                    <span className="kw">def</span>{' '}
                                    <span className="fn">__init__</span>
                                    (<span className="var">self, capacity: int</span>):
                                    {"\n"}

                                    {'  '}
                                    <span className="var">
                                        self.cap = capacity
                                    </span>
                                    {"\n"}

                                    {'  '}
                                    <span className="var">
                                        self.cache = &#123;&#125;
                                    </span>{' '}

                                    <span className="comment">
                                        // map key to node
                                    </span>

                                    {"\n"}

                                    {'  '}
                                    <span className="var">
                                        self.left, self.right = Node(0, 0), Node(0, 0)
                                    </span>

                                    {"\n"}

                                    {'  '}
                                    <span className="var">
                                        self.left.next, self.right.prev = self.right, self.left
                                    </span>

                                    {"\n\n"}

                                    <div className="code-active-line">
                                        {'  '}
                                        <span className="kw">def</span>{' '}
                                        <span className="fn">get</span>
                                        (<span className="var">self, key: int</span>)
                                        -&gt; <span className="kw">int</span>:
                                    </div>

                                    {"\n"}

                                    {'  '}
                                    <span className="kw">if</span>{' '}
                                    <span className="var">key</span>{' '}
                                    <span className="kw">in</span>{' '}
                                    <span className="var">self.cache</span>:
                                    {"\n"}

                                    {'  '}
                                    <span className="var">
                                        self.remove(self.cache[key])
                                    </span>
                                </code>
                            </pre>

                        </div>

                    </div>


                    <footer className="test-harness-bar">

                        <div className="harness-summary">
                            <span className="harness-tag">
                                // TEST EXECUTION HARNESS
                            </span>

                            <span className="harness-status">
                                12/12 assertions passed
                            </span>
                        </div>


                        <div className="test-cases-group">

                            <div className="test-case-item">
                                <CheckCircle2 size={13} />
                                <span>Case 1: Standard Put/Get</span>
                            </div>

                            <div className="test-case-item">
                                <CheckCircle2 size={13} />
                                <span>Case 2: Eviction Boundary</span>
                            </div>

                            <div className="test-case-item">
                                <CheckCircle2 size={13} />
                                <span>Case 3: Concurrent Ops</span>
                            </div>

                            <span className="benchmark-stat">
                                Execution: 44ms (Faster than 94.2%)
                            </span>

                        </div>

                    </footer>

                </main>

            </div>

        </div>
    );
}