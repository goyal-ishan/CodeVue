from typing import TypedDict, List, Optional, Literal


class InterviewStateSchema(TypedDict):
    # Interview details
    interview_id: str
    topic: str
    difficulty: str
    started_at: float
    duration_seconds: int
    coding_duration_seconds:int
    # Coding problem
    problem: str
    constraints: List[str]
    examples: List[str]

    problem_id: str
    problem_title: str
    test_cases: List[dict]

    # Current interview phase
    phase: Literal[
        "brute_force",
        "optimized",
        "coding",
        "finished"
    ]

    # Brute-force approach
    brute_force_answer: str
    brute_force_score: float
    brute_force_feedback: str
    brute_force_satisfactory: bool
    brute_force_followup_count: int  # maximum 2 
    brute_force_followup_question: str
    brute_force_followup_answer: str

    # Optimized approach
    optimized_answer: str
    optimized_score: float
    optimized_feedback: str
    optimized_satisfactory: bool
    optimized_followup_count: int  # maximum 2
    optimized_followup_question: str
    optimized_followup_answer: str

        # Current interaction
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

    # Brute-force approach
    brute_force_missing_concepts: List[str]

    # Optimized approach
    optimized_missing_concepts: List[str]

    # Coding round
    coding_started_at: Optional[float]
    coding_duration_seconds: int
    programming_language: str
    submitted_code: str
    code_submitted: bool
    test_results: List[dict]
    code_score: float
    code_feedback: str


    # Interview termination
    finish_reason: Optional[
        Literal["submitted", "timeout"]
    ]

    # Final report
    final_report: Optional[str]