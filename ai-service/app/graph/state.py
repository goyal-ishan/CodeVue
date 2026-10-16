from typing import TypedDict, List, Optional, Literal


class InterviewState(TypedDict):

    started_at: float
    duration_seconds: int
    
    topic: str
    difficulty: str
    
    current_question: str
    current_answer: str
    
    answer_score: float
    answer_feedback: str
    missing_concepts: List[str]
    is_satisfactory: bool
    
    followup_question: str
    followup_answer: str
    followup_count: int
    max_followups: int

    next_action: Literal[
        "followup",
        "next_question",
        "finish"
    ]

    question_count: int
    conversation_history: List[dict]
    final_report: Optional[str]