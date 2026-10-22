# CodeVue — AI-Powered Technical Interview & Code Execution Platform

CodeVue is an intelligent, full-stack technical interview simulation platform engineered to replicate the real-world rigor of FAANG and Tier-1 software engineering interviews.

While platforms like LeetCode provide extensive problem lists (such as the Top 150 Interview Study Plan), they operate primarily as automated unit-test checkers. In real technical interviews, candidates rarely fail solely because of syntax or math; **they fail because they cannot articulate their thoughts, rush to code without discussing trade-offs, and struggle to communicate with the interviewer under pressure.**

CodeVue bridges this gap by introducing an active AI interviewer agent that conducts structured, conversational mock interviews. It enforces a strict 3-phase technical state machine: requiring candidates to formulate brute-force baselines, discuss algorithmic optimizations, answer probe questions, and only then write verified code in a live, sandboxed IDE.

---

## 🎯 Core Motivation

When engineers prepare using traditional online judges, they build habits that hurt them in actual interviews:

1. **Coding in Silence**: Immediately jumping into the code editor without clarifying constraints or baseline approaches.
2. **Skipping Naive Baselines**: Failing to explain a simple brute-force idea, which interviewers expect before any optimization.
3. **Unarticulated Trade-Offs**: Inability to defend time and space complexity ($O(N)$ vs. $O(N \log N)$) or explain why a specific data structure was chosen.
4. **Fragile Communication**: Struggling when an interviewer pushes back with follow-up questions, edge cases, or hints.

**CodeVue enforces interview best practices through an active agent loop:**

- Candidates cannot write a single line of code until their algorithmic reasoning is approved by the interviewer.
- If an explanation lacks depth or ignores edge cases, the AI interviewer proactively probes with targeted follow-up questions.
- Separate, realistic timers manage the discussion and coding phases independently.

---

## 🤖 Interview State Machine & Agent Flow

The interview follows an adaptive state machine with dynamic follow-up loops and dual-timer deadlines:

```mermaid
flowchart TD
    Start([Candidate Starts Interview]) --> LLM{AI Interviewer\nState Engine}

    %% Phase 1: Brute Force
    LLM -->|Initialize Phase 1| BF[Phase 1: Brute Force\nExplain naive approach & constraints]
    BF --> BF_Eval{LLM Satisfied?}
    BF_Eval -->|Yes| LLM
    BF_Eval -->|Not Satisfied| BFFollow[Brute Force Follow-up\nProbing missing edge cases & Big-O]
    BFFollow -->|Candidate Clarifies| BF_Eval

    %% Phase 2: Optimization
    LLM -->|Transition Phase 2| OPT[Phase 2: Optimization\nDiscuss optimal DS & bottleneck analysis]
    OPT --> OPT_Eval{LLM Satisfied?}
    OPT_Eval -->|Yes| LLM
    OPT_Eval -->|Not Satisfied| OPTFollow[Optimization Follow-up\nInvariants, space/time trade-offs]
    OPTFollow -->|Candidate Refines| OPT_Eval

    %% Phase 3: Coding Sandbox
    LLM -->|Unlock Phase 3| Coding[Phase 3: Live Coding\nMonaco Editor with Starter Code]
    Coding --> DryRun[Dry Run Mode\nExecutes against Public Test Cases]
    DryRun --> Coding
    Coding --> Submit[Candidate Submits Code\nGraded on Public + Hidden Test Cases]

    %% Timers & Deadlines
    BF -.->|interview_duration reached| Timeout[Time Limit Exceeded]
    OPT -.->|interview_duration reached| Timeout
    Coding -.->|coding_duration reached| Timeout
    Timeout --> Finished

    %% Completion & Scorecard
    Submit --> Finished[Phase 4: Finished\nEvaluate Test Suites & Discussions]
    Finished --> Report[Comprehensive Report Page\nScorecard • AI Feedback • Transcripts • Diffs]
    Report --> EndNode([Session Complete])

    %% Styling
    classDef timer fill:#2a1b1e,stroke:#ef4444,stroke-width:1.5px,color:#f87171;
    classDef phase fill:#18191d,stroke:#3b82f6,stroke-width:1.5px,color:#93c5fd;
    classDef success fill:#12281d,stroke:#22c55e,stroke-width:1.5px,color:#86efac;

    class Timeout timer;
    class BF,OPT,Coding phase;
    class Finished,Report success;
```

---

## ⚡ Key Architectural Features

### 1. Hybrid Authentication System
- **Custom JWT Authentication**: Secure password hashing and custom JSON Web Token generation for email/password registrations.
- **Google OAuth 2.0 Integration**: One-click Google Sign-In for streamlined authentication.
- **Unified Identity**: Mock interview progress, problem attempts, code submissions, and analytics seamlessly tie to the candidate's canonical email identity regardless of sign-in provider.

### 2. Dual-Timer State Machine Lifecycle
To mirror real technical interviews, CodeVue separates the session into two independent clocks:
- **`interview_duration` (Discussion Clock)**: Enforces pacing across the Brute Force and Optimization discussion phases. If a candidate stalls or fails to defend their ideas within the limit, the session terminates cleanly.
- **`coding_duration` (Live Coding Clock)**: A dedicated countdown timer that activates only when the candidate successfully defends their approach and unlocks the editor.

### 3. Dual-Mode Multi-Language Execution Engine
- **Remote / Containerized Mode**: Integrates with the Piston API for containerized code execution.
- **Zero-Docker Native Fallback**: Compiles and executes code locally using native subprocesses for:
  - **C++ (C++17 / GCC `g++`)**
  - **Python (Python 3.10+)**
  - **Java (OpenJDK 17 `javac` & `java`)**
- **Automated Harness Injection**: Wraps user-submitted solutions inside custom test-harness templates, executing test cases in memory and returning structured JSON outputs using delimiter markers (`__CODEVUE_RESULTS_START__`).

### 4. Split Test-Suite Architecture
- **Public Test Cases**: Visible in the candidate's Monaco workspace for debugging and dry runs (`POST /interviews/{id}/run`).
- **Hidden Test Cases**: Evaluated only upon final submission (`POST /interviews/{id}/code`) to test boundary conditions, extreme constraints, negative values, and stress inputs.

### 5. Candidate Analytics & Progress Suite
- **11 Topic Tracks**: Practice across Array/String, Sliding Window, Two Pointers, Linked Lists, Stacks, Trees, DP, Graphs, Backtracking, Greedy, and Number Theory.
- **Mastery Analytics**: Track phase performance (Brute Force / 10, Optimization / 10, Code Execution / 10) and curriculum completion rates.
- **Dedicated Scorecard & Review (`/interview/:id/report`)**: Review past sessions with composite candidate ratings (*Strong Hire*, *Hire*, *Lean Hire*, *Needs Practice*), side-by-side transcripts of user explanations vs. AI feedback, and syntax-highlighted code submissions.

---

## 🛠️ Architecture & Tech Stack

```text
                     ┌──────────────────────────────────────────────┐
                     │            React (Vite) Frontend             │
                     │ Monaco Editor | React Router | Lucide Icons │
                     └──────────────────────┬───────────────────────┘
                                            │ HTTP / JSON API
                                            ▼
                     ┌──────────────────────────────────────────────┐
                     │           FastAPI Backend Service            │
                     │  Phase Validation | Deadline Check | State   │
                     └───────┬──────────────────────────────┬───────┘
                             │                              │
              Optimistic     │                              │ Subprocess / HTTP
             State Updates   ▼                              ▼
          ┌──────────────────────┐             ┌─────────────────────────┐
          │     MongoDB Atlas    │             |    Native Execution     │
          │ Versioned Interviews │             │     Host Compilers      │
          │ User Progress Logs   │             │   (Python, C++, Java)   │
          └──────────────────────┘             └─────────────────────────┘
```

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite, Monaco Editor (`@monaco-editor/react`), Lucide React, React Router v6 |
| **Backend** | FastAPI, Python 3.10+, Pydantic v2, Uvicorn, HTTPX |
| **Database** | MongoDB Atlas, Motor / PyMongo (Optimistic concurrency control via `$inc: { version: 1 }`) |
| **Code Execution**| Subprocess Sandboxing (`g++`, `javac`, `python`) + Remote Piston API |
| **Authentication** | Custom JWT (PBKDF2/HMAC) + Google OAuth 2.0 |
| **Styling** | Custom Responsive CSS (Dark Theme: `#121316` background, `#ef4444` accent) |

---

## 📁 Repository Structure

```text
CodeVue/
├── ai-service/                   # FastAPI Backend Service
│   ├── app/
│   │   ├── data/
│   │   │   └── questions_bank.py # 31+ problems with starter code, public & hidden tests
│   │   ├── db/
│   │   │   └── mongodb.py        # MongoDB connection client & collections
│   │   ├── routes/
│   │   │   ├── interview.py      # State machine endpoints & code execution routes
│   │   │   └── auth.py           # JWT generation, Google OAuth verification
│   │   ├── services/
│   │   │   ├── code_executor.py  # Language test harnesses & local/Piston runners
│   │   │   └── interview_store.py# Atomic versioned persistence in MongoDB
│   │   └── main.py               # FastAPI entrypoint & CORS middleware
│   ├── .env.example              # Environment variables template
│   └── requirements.txt          # Python dependencies
│
├── frontend/                     # React + Vite Web Client
│   ├── src/
│   │   ├── context/
│   │   │   └── AuthContext.jsx   # Auth state (Custom JWT + Google OAuth)
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx     # Topic tracks & launchpad
│   │   │   ├── InterviewWorkspace.jsx # Split IDE, AI chat, live console, phase stepper
│   │   │   ├── MockInterviews.jsx# Filterable interview history log & scorecard links
│   │   │   ├── Progress.jsx      # Phase performance & curriculum coverage metrics
│   │   │   ├── Profile.jsx       # User preferences & default editor language
│   │   │   └── InterviewReport.jsx # Post-interview scorecard & AI review transcripts
│   │   ├── App.jsx               # Client routes & ProtectedRoute wrappers
│   │   └── index.css             # Theme variables & base styling
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Make sure the following tools are installed:
* **Node.js**: v18+ and `npm`
* **Python**: v3.10+
* **Local Compilers** (for zero-Docker execution):
  * `g++` (MinGW-w64 on Windows or GCC on Linux/macOS)
  * `javac` and `java` (OpenJDK 17+)
  * `python` added to system `PATH`
* **MongoDB**: A MongoDB Atlas connection URI or local MongoDB instance

---

### Backend Setup (`ai-service`)

1. Navigate to the `ai-service` directory:
   ```bash
   cd ai-service
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file inside `ai-service/` (or copy from `.env.example`):
   ```env
   INTERVIEW_MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/codevue?retryWrites=true&w=majority
   PISTON_API_URL=[https://emkc.org/api/v2/piston](https://emkc.org/api/v2/piston)
   GROQ_API_KEY=your_optional_llm_key
   JWT_SECRET=your_jwt_secret_key
   ```

5. Start the backend service:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   The API will be available at `http://localhost:8000`. Interactive documentation can be viewed at `http://localhost:8000/docs`.

---

### Frontend Setup (`frontend`)

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment variables:
   Create a `.env` file inside `frontend/`:
   ```env
   VITE_AI_SERVICE_URL=http://localhost:8000
   ```

4. Launch the development server:
   ```bash
   npm run dev
   ```
   Open your browser to `http://localhost:5173`.

---

## 📡 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/interviews/start` | Starts an interview session, initializes state, and sets timers. |
| `GET` | `/interviews/{id}` | Fetches current interview status, active phase, and deadlines. |
| `POST` | `/interviews/{id}/answer` | Submits answers for Brute Force or Optimization phases with follow-up support. |
| `POST` | `/interviews/{id}/run` | Dry-runs candidate code strictly against **public test cases**. |
| `POST` | `/interviews/{id}/code` | Submits code for final grading against **public + hidden test cases**. |
| `GET` | `/interviews/{id}/report` | Retrieves the post-interview evaluation report, scorecard, and diffs. |
| `GET` | `/interviews/user/{email}/history` | Aggregates user interview attempts, completions, and phase score averages. |

---

## 🔒 Concurrency & Reliability

CodeVue utilizes **optimistic concurrency control** in MongoDB to avoid race conditions during candidate polling and code submissions:
* Every interview document maintains a sequential integer `version` field.
* Updates use atomic conditional queries:
  ```python
  interviews_collection.update_one(
      {"interview_id": interview_id, "version": current_version},
      {"$set": update_fields, "$inc": {"version": 1}}
  )
  ```
* If a write conflict occurs while a background deadline check or client request updates the document, the update is safely aborted, preventing dirty writes and inconsistent state.
