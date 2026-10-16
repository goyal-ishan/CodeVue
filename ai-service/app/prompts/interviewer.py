import time
from fastapi import APIRouter
from app.graph.state import InterviewState
from pydantic import BaseModel

router = APIRouter()

class StartInterviewRequest(BaseModel):
    topic: str
    difficulty: str
    duration_seconds: int


@router.post("/start")
def start_interview(request: StartInterviewRequest):

    initial_state: InterviewState = {
        "started_at": time.time(),
        "duration_seconds": request.duration_seconds,

        "topic": request.topic,
        "difficulty": request.difficulty,

        "current_question": "",
        "current_answer": "",

        "answer_score": 0.0,
        "answer_feedback": "",
        "missing_concepts": [],
        "is_satisfactory": False,

        "followup_question": "",
        "followup_answer": "",
        "followup_count": 0,
        "max_followups": 2,

        "next_action": "next_question",

        "question_count": 0,
        "conversation_history": [],
        "final_report": None
    }

    return initial_state