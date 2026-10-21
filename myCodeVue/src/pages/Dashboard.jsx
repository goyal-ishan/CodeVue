import React, {useRef, useState} from 'react';
import {useAuth} from "../context/AuthContext.jsx"

import {
  Code2,
  Flame,
  ArrowRight,
  Play,
  GitBranch,
  Layers,
  Network,
  Hash,
  TreeDeciduous,
  MoveHorizontal,
  PanelsTopLeft,
  Link,
  Braces,
} from 'lucide-react';
import './Dashboard.css';


const tracks = [
  {
    id: 'arrays-strings',
    topic: 'Array/String',
    icon: Braces,
    description: 'Two pointers, sliding window, prefix sums, and hashing.',
    interviews: 18,
  },
  {
    id: 'greedy-constructive',
    topic: 'Greedy & Constructive',
    icon: ZapIcon,
    description: 'Greedy strategies, sorting, intervals, and constructive.',
    interviews: 14,
  },
  {
  id: 'two-pointers',
  topic: 'Two Pointers',
  icon: MoveHorizontal,
  description: 'Master left and right pointer techniques to solve array and string problems efficiently.',
  interviews: 5,
},
{
  id: 'sliding-window',
  topic: 'Sliding Window',
  icon: PanelsTopLeft,
  description: 'Solve substring and subarray problems using fixed and variable sliding windows.',
  interviews: 4,
},
{
  id: 'linked-list',
  topic: 'Linked List',
  icon: Link,
  description: 'Practice pointer manipulation, list reversal, cycle detection, and merging linked lists.',
  interviews: 5,
},
{
  id: 'stack',
  topic: 'Stack',
  icon: Layers,
  description: 'Learn stack-based problem solving, expression evaluation, and matching parentheses.',
  interviews: 5,
},
{
  id: 'backtracking',
  topic: 'Backtracking',
  icon: GitBranch,
  description: 'Explore recursive search, permutations, combinations, and constraint-based problems.',
  interviews: 5,
},
  {
    id: 'dynamic-programming',
    topic: 'Dynamic Programming',
    icon: Layers,
    description: 'Memoization, tabulation, knapsack, and subsequences.',
    interviews: 24,
  },
  {
    id: 'graphs',
    topic: 'Graphs',
    icon: Network,
    description: 'BFS, DFS, shortest paths, DSU, and topological sorting.',
    interviews: 20,
  },
  {
    id: 'number-theory',
    topic: 'Number Theory',
    icon: Hash,
    description: 'GCD, primes, sieve, modular arithmetic, and exponentiation.',
    interviews: 12,
  },
  {
    id: 'trees-advanced-ds',
    topic: 'Trees & Advanced DS',
    icon: TreeDeciduous,
    description: 'Trees, BSTs, heaps, tries, Fenwick trees, and segment trees.',
    interviews: 22,
  },
];

function ZapIcon(props) {
  return <Code2 {...props} />;
}

export default function DSADashboard() {
  const {user}=useAuth();
  const userName = user?.fullName || "there";
  const [highlightTracks, setHighlightTracks]=useState(false);
  const tracksRef=useRef(null);
  const startInterview = () => {
        tracksRef.current?.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });

      setHighlightTracks(true);

      setTimeout(() => {
        setHighlightTracks(false);
      },2000);
  };
  
 
  return (
    <div className="cv-dashboard">
      <header className="cv-navbar">
        <a href="/dashboard" className="cv-brand" aria-label="CodeVue dashboard">
          <div className="cv-brand-icon">
               <span>&lt;</span>
               <span className="greaterThan">&gt;</span>
          </div>
          <span>Code<span className="cv-brand-accent">Vue</span></span>
        </a>

        <nav className="cv-nav-links" aria-label="Main navigation">
          <a href="/">Home</a>
          <a href="/dashboard" className="active">Dashboard</a>
          <a href="/mock-interviews">Mock Interviews</a>
          <a href="/progress">My Progress</a>
        </nav>

        <a href="/profile" className="cv-profile-link" aria-label="My profile">
          <span className="cv-avatar">
                {userName !== "there" ? userName.trim().charAt(0).toUpperCase() : "U"}
          </span>
          <span className="cv-profile-name">{userName}</span>
        </a>
      </header>

      <main className="cv-main">
        <section className="cv-welcome">
          <div className="cv-welcome-copy">
            <p className="cv-eyebrow">YOUR INTERVIEW PRACTICE</p>
            <h1>Welcome back, {userName}.</h1>
            <p className="cv-welcome-text">
              Build confidence with topic-wise DSA mock interviews and track your progress as you improve.
            </p>
            <div className="cv-welcome-actions">
              <button className="cv-btn-primary" onClick={startInterview}>
                <Play size={16} fill="currentColor" />
                Start a Mock Interview
                <ArrowRight size={16} />
              </button>
              <a className="cv-btn-secondary" href="/progress">View My Progress</a>
            </div>
          </div>
          {/* <div className="cv-streak-card">
            <span className="cv-streak-icon"><Flame size={21} /></span>
            <div>
              <p className="cv-streak-label">Current streak</p>
              <p className="cv-streak-value">14 days</p>
              <p className="cv-streak-note">Keep showing up!</p>
            </div>
          </div> */}
        </section>

        <section ref={tracksRef} className="cv-tracks-section" id="interview-tracks">
          <div  className={`cv-section-heading ${highlightTracks ? 'cv-heading-highlight' : ''}`}>
            <div>
              <p className="cv-eyebrow">CHOOSE YOUR FOCUS</p>
              <h2>DSA Interview Tracks</h2>
              <p className="cv-section-subtitle">Pick a topic to explore its mock interviews.</p>
            </div>
            <span className="cv-track-count">11 topics</span>
          </div>

          <div className="cv-tracks-grid">
            {tracks.map((track) => {
              const Icon = track.icon;
              return (
                <a
                  key={track.id}
                  href={`/tracks/${track.id}`}
                  className="cv-track-card"
                >
                  <div className="cv-track-card-top">
                    <span className="cv-track-icon"><Icon size={21} /></span>
                    <ArrowRight size={17} className="cv-card-arrow" />
                  </div>
                  <h3>{track.topic}</h3>
                  <p>{track.description}</p>
                  <div className="cv-track-card-bottom">
                    <span>{track.interviews} mock interviews</span>
                    <span className="cv-explore">Explore topic</span>
                  </div>
                </a>
              );
            })}
          </div>
        </section>

        {/* <section className="cv-bottom-panel">
          <div className="cv-bottom-icon"><GitBranch size={20} /></div>
          <div className="cv-bottom-copy">
            <h2>Ready for your next interview?</h2>
            <p>Choose a topic or start a mock interview to keep your preparation moving.</p>
          </div>
          <button className="cv-btn-primary" onClick={startInterview}>
            Start Interview <ArrowRight size={16} />
          </button>
        </section> */}
      </main>

      <footer className="cv-footer">
        <span>© {new Date().getFullYear()} CodeVue</span>
        <span>Practice with purpose.</span>
      </footer>
    </div>
  );
}
