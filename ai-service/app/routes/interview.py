import time
from uuid import uuid4
from typing import Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.graph.state import InterviewState
from app.graph.builder import build_graph
from app.graph.routing import route_start
from fastapi import UploadFile, File
from app.services.stt import transcribe_audio

router = APIRouter(prefix="/interviews", tags=["Interviews"])

graph = build_graph()

# Temporary in-memory storage for interviews.
interviews: Dict[str, InterviewState] = {}


class StartInterviewRequest(BaseModel):
    topic: str
    difficulty: str
    duration_seconds: int = Field(gt=0)


class SubmitAnswerRequest(BaseModel):
    answer: str = Field(min_length=1)


@router.post("/start")
def start_interview(request: StartInterviewRequest):
    interview_id = str(uuid4())

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

    result = graph.invoke(initial_state)
    interviews[interview_id] = result

    return {
        "interview_id": interview_id,
        "topic": result["topic"],
        "difficulty": result["difficulty"],
        "question": result["current_question"],
        "question_count": result["question_count"]
    }


@router.post("/{interview_id}/answer")
def submit_answer(
    interview_id: str,
    request: SubmitAnswerRequest
):
    return process_answer(interview_id, request.answer)

def process_answer(interview_id: str, answer: str):
    if interview_id not in interviews:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    state = dict(interviews[interview_id])

    if state["next_action"] == "finish" or state["final_report"] is not None:
        raise HTTPException(
            status_code=400,
            detail="This interview has already finished"
        )

    if time.time() - state["started_at"] >= state["duration_seconds"]:
        state["next_action"] = "finish"
        result = graph.invoke(state)
        interviews[interview_id] = result

        return {
            "interview_id": interview_id,
            "action": "finish",
            "report": result["final_report"]
        }

    state["current_answer"] = answer
    result = graph.invoke(state)
    print("GRAPH RESULT:", result)
    print("QUESTION:", result.get("current_question"))
    print("QUESTION COUNT:", result.get("question_count"))
    interviews[interview_id] = result

    if result["next_action"] == "finish":
        action = "finish"
    elif result["followup_count"] > state["followup_count"]:
        action = "followup"
    else:
        action = "next_question"

    return {
        "interview_id": interview_id,
        "action": action,
        "transcribed_answer": answer,
        "question": result["current_question"] if action != "finish" else None,
        "score": result["answer_score"],
        "feedback": result["answer_feedback"],
        "missing_concepts": result["missing_concepts"],
        "report": result["final_report"]
    }


@router.post("/{interview_id}/answer-audio")
async def submit_audio_answer(
    interview_id: str,
    audio: UploadFile = File(...)
):
    if interview_id not in interviews:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    audio_bytes = await audio.read()

    if not audio_bytes:
        raise HTTPException(
            status_code=400,
            detail="Audio file is empty"
        )

    try:
        answer_text = transcribe_audio(
            audio_bytes=audio_bytes,
            filename=audio.filename or "answer.webm"
        )
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Audio transcription failed"
        )

    if not answer_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No speech detected. Please try again."
        )

    return process_answer(interview_id, answer_text)

@router.post("/{interview_id}/end")
def end_interview(interview_id: str):
    if interview_id not in interviews:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    state = dict(interviews[interview_id])
    state["next_action"] = "finish"

    result = graph.invoke(state)
    interviews[interview_id] = result

    return {
        "interview_id": interview_id,
        "action": "finish",
        "report": result["final_report"]
    }
