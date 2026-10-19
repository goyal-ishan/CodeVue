import React, { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, ArrowRight, Search } from "lucide-react";
import { questions } from "../data/questions";
import {useAuth} from "../context/AuthContext.jsx"
import "./TrackQuestions.css";

const topicNames = {
  "arrays-strings": "Arrays & Strings",
  "greedy-constructive": "Greedy & Constructive",
  "dynamic-programming": "Dynamic Programming",
  graphs: "Graphs",
  "number-theory": "Number Theory",
  "trees-advanced-ds": "Trees & Advanced DS",
};

export default function TrackQuestions(){
  const {user}=useAuth();
  const userName = user?.fullName || "there";
  const { topicId } = useParams();
  const [search, setSearch] = useState("");
  const [difficulty, setDifficulty] = useState("All");

  const topicQuestions = questions[topicId] || [];

  const filteredQuestions = topicQuestions.filter((question) => {
    const matchesSearch = question.title
      .toLowerCase()
      .includes(search.toLowerCase());

    const matchesDifficulty =
      difficulty === "All" || question.difficulty === difficulty;

    return matchesSearch && matchesDifficulty;
  });

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
          <a href="/dashboard" className="inactive">Dashboard</a>
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
       <div className="cv-back-wrapper">
         <Link to="/dashboard" className="cv-back-link">
             <ArrowLeft size={16} />
              Back to Dashboard
         </Link>
       </div>
      <main className="cv-questions-main">
        
        <p className="cv-eyebrow">PRACTICE BY TOPIC</p>

        <h1>{topicNames[topicId] || "Questions"}</h1>

        <p className="cv-questions-subtitle">
          Choose a problem and practice at your own pace.
        </p>

        <div className="cv-question-tools">
          <div className="cv-question-search">
            <Search size={17} />
            <input
              type="text"
              placeholder="Search questions..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            aria-label="Filter by difficulty"
          >
            <option value="All">All difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>

        <div className="cv-question-list-header">
          <span>Problem</span>
          <span>Difficulty</span>
          <span></span>
        </div>

        <div className="cv-question-list">
          {filteredQuestions.map((question, index) => (
            <Link
              to={`/questions/${question.id}`}
              className="cv-question-row"
              key={question.id}
            >
              <div className="cv-question-title">
                <span className="cv-question-number">{index + 1}</span>
                <span>{question.title}</span>
              </div>

              <span
                className={`cv-difficulty cv-difficulty-${question.difficulty.toLowerCase()}`}
              >
                {question.difficulty}
              </span>

              <ArrowRight size={17} className="cv-question-arrow" />
            </Link>
          ))}

          {filteredQuestions.length === 0 && (
            <div className="cv-question-empty">
              No questions found. Try another search or difficulty.
            </div>
          )}
        </div>

        <p className="cv-question-count">
          Showing {filteredQuestions.length} of {topicQuestions.length} questions
        </p>
      </main>
    </div>
  );
}