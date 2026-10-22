from typing import TypedDict, List, Optional, Literal, Dict, Any


class InterviewStateSchema(TypedDict):
    # Persistence & Versioning
    interview_id: str
    version: Optional[int]

    # User Association
    user_email: Optional[str]
    user_id: Optional[str]

    # Problem details
    problem_id: str
    problem_title: str
    topic: str
    difficulty: str
    problem: str
    constraints: List[str]
    examples: List[Dict[str, Any]]
    starter_code: Optional[Dict[str, str]]
    test_cases: List[Dict[str, Any]]

    # Interview timing
    started_at: float
    duration_seconds: int
    coding_started_at: Optional[float]
    coding_duration_seconds: int

    # Lifecycle & Stepper
    phase: Literal[
        "brute_force",
        "optimized",
        "coding",
        "finished",
    ]
    current_question: str
    pending_question_type: Literal[
        "brute_force_initial",
        "brute_force_followup",
        "optimization",
        "optimized_initial",
        "optimized_followup",
        "coding",
        "finished",
    ]

    # Brute-force phase evaluation
    brute_force_answer: str
    brute_force_score: float
    brute_force_feedback: str
    brute_force_satisfactory: bool
    brute_force_missing_concepts: List[str]
    brute_force_followup_count: int
    brute_force_followup_question: str
    brute_force_followup_answer: str

    # Optimization phase evaluation
    optimized_answer: str
    optimized_score: float
    optimized_feedback: str
    optimized_satisfactory: bool
    optimized_missing_concepts: List[str]
    optimized_followup_count: int
    optimized_followup_question: str
    optimized_followup_answer: str

    # Coding phase & Sandbox results
    programming_language: str
    submitted_code: str
    code_submitted: bool
    test_results: List[Dict[str, Any]]
    code_score: float
    code_feedback: str

    # Termination
    finish_reason: Optional[Literal["submitted", "timeout"]]
    final_report: Optional[str]