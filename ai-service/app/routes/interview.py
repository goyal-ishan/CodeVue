
import time
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.graph.nodes import (
    generate_problem,
    evaluate_brute_force,
    generate_brute_force_followup,
    ask_for_optimization,
    evaluate_optimized,
    generate_optimized_followup,
    generate_report,
)
from app.graph.state import InterviewStateSchema
from app.services.interview_store import (
    initialize_interview_store,
    create_interview,
    get_interview,
    update_interview,
)


router = APIRouter(prefix="/interviews", tags=["Interviews"])

MAX_FOLLOWUPS = 2
DEFAULT_INTERVIEW_DURATION = 3600
DEFAULT_CODING_DURATION = 1800

class StartInterviewRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=100)
    difficulty: Literal["Easy", "Medium", "Hard"]
    duration_seconds: int = Field(default=3600, ge=300, le=7200)
    coding_duration_seconds: int = Field(default=1800, ge=300, le=3600)

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Topic cannot be empty or whitespace.")
        return value


class AnswerRequest(BaseModel):
    answer: str = Field(min_length=1, max_length=20000)

    @field_validator("answer")
    @classmethod
    def validate_answer(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Answer cannot be empty or whitespace.")
        return value


class CodeSubmissionRequest(BaseModel):
    code: str = Field(min_length=1, max_length=100000)
    programming_language: str = Field(min_length=1, max_length=50)

    @field_validator("code")
    @classmethod
    def validate_code(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Code cannot be empty or whitespace.")
        return value

    @field_validator("programming_language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Programming language cannot be empty.")
        return value


def _now() -> float:
    return time.time()


def _public_interview(state: dict) -> dict:
    """Return interview data safe for the frontend."""
    fields = [
        "interview_id",
        "topic",
        "difficulty",
        "problem",
        "constraints",
        "examples",
        "phase",
        "current_question",
        "pending_question_type",
        "brute_force_score",
        "brute_force_feedback",
        "brute_force_satisfactory",
        "brute_force_followup_count",
        "brute_force_followup_question",
        "optimized_score",
        "optimized_feedback",
        "optimized_satisfactory",
        "optimized_followup_count",
        "optimized_followup_question",
        "coding_started_at",
        "coding_duration_seconds",
        "programming_language",
        "code_submitted",
        "code_score",
        "code_feedback",
        "finish_reason",
        "final_report",
        "started_at",
        "duration_seconds",
    ]

    return {key: state.get(key) for key in fields}


def _load_interview(interview_id: str) -> dict:
    state = get_interview(interview_id)

    if state is None:
        raise HTTPException(status_code=404, detail="Interview not found")

    return state


def _persist(state: dict, updates: dict) -> dict:
    """Persist updates using optimistic concurrency control."""
    updated = update_interview(
        interview_id=state["interview_id"],
        updates=updates,
        expected_version=state["version"],
    )

    if updated is None:
        raise HTTPException(
            status_code=409,
            detail="Interview changed concurrently. Reload and try again.",
        )

    return updated


def _finish_interview(state: dict, reason: str) -> dict:
    """Generate and persist the final report."""
    updates = {
        "phase": "finished",
        "pending_question_type": "finished",
        "finish_reason": reason,
        "current_question": "",
    }

    finished_state = {**state, **updates}
    report_result = generate_report(finished_state)

    updates.update(report_result)

    return _persist(state, updates)


def _start_coding(state: dict) -> dict:
    """Start the coding phase and its server-enforced deadline."""
    coding_started_at = _now()

    updates = {
        "phase": "coding",
        "pending_question_type": "coding",
        "coding_started_at": coding_started_at,
        "current_question": (
            "Now implement your solution in the code editor. "
            "Submit your code before the coding timer expires."
        ),
    }

    return _persist(state, updates)


def _advance_after_brute_force(state: dict) -> dict:
    """Move to optimization after brute-force evaluation."""
    transition = ask_for_optimization(state)

    return _persist(
        state,
        {
            **transition,
            "pending_question_type": "optimized_initial",
        },
    )


def _advance_after_optimized(state: dict) -> dict:
    """Move to coding after optimized explanation evaluation."""
    return _start_coding(state)


def _evaluate_brute_force_answer(state: dict, answer: str) -> dict:
    """Evaluate an initial brute-force explanation or follow-up answer."""
    pending_type = state["pending_question_type"]

    if pending_type == "brute_force_initial":
        state = _persist(
            state,
            {"brute_force_answer": answer},
        )

        result = evaluate_brute_force(state)
        state = _persist(state, result)

    elif pending_type == "brute_force_followup":
        state = _persist(
            state,
            {"brute_force_followup_answer": answer},
        )

        result = evaluate_brute_force(state)
        state = _persist(state, result)

    else:
        raise HTTPException(
            status_code=400,
            detail="The interview is not awaiting a brute-force answer.",
        )

    if state["brute_force_satisfactory"]:
        return _advance_after_brute_force(state)

    if state["brute_force_followup_count"] < MAX_FOLLOWUPS:
        followup = generate_brute_force_followup(state)

        return _persist(
            state,
            {
                **followup,
                "pending_question_type": "brute_force_followup",
                "current_question": followup[
                    "brute_force_followup_question"
                ],
            },
        )

    # The follow-up limit is reached. Continue the interview while
    # preserving the evaluation result for the final report.
    return _advance_after_brute_force(state)


def _evaluate_optimized_answer(state: dict, answer: str) -> dict:
    """Evaluate an initial optimized explanation or follow-up answer."""
    pending_type = state["pending_question_type"]

    if pending_type == "optimized_initial":
        state = _persist(
            state,
            {"optimized_answer": answer},
        )

        result = evaluate_optimized(state)
        state = _persist(state, result)

    elif pending_type == "optimized_followup":
        state = _persist(
            state,
            {"optimized_followup_answer": answer},
        )

        result = evaluate_optimized(state)
        state = _persist(state, result)

    else:
        raise HTTPException(
            status_code=400,
            detail="The interview is not awaiting an optimized answer.",
        )

    if state["optimized_satisfactory"]:
        return _advance_after_optimized(state)

    if state["optimized_followup_count"] < MAX_FOLLOWUPS:
        followup = generate_optimized_followup(state)

        return _persist(
            state,
            {
                **followup,
                "pending_question_type": "optimized_followup",
                "current_question": followup[
                    "optimized_followup_question"
                ],
            },
        )

    # Continue to coding after the permitted follow-ups.
    return _advance_after_optimized(state)


def _check_deadlines(state: dict) -> dict:
    """Enforce interview and coding deadlines using server time."""
    now = _now()

    if state["phase"] == "finished":
        return state

    interview_deadline = (
        state["started_at"] + state["duration_seconds"]
    )

    if now >= interview_deadline:
        return _finish_interview(state, "timeout")

    if state["phase"] == "coding":
        coding_started_at = state.get("coding_started_at")

        if coding_started_at is None:
            raise HTTPException(
                status_code=500,
                detail="Coding deadline was not initialized.",
            )

        coding_deadline = (
            coding_started_at + state["coding_duration_seconds"]
        )

        if now >= coding_deadline:
            return _finish_interview(state, "timeout")

    return state


@router.post("/start")
def start_interview(request: StartInterviewRequest):
    """Generate a problem and persist a complete interview state."""
    initialize_interview_store()

    interview_id = str(uuid4())

    state: InterviewStateSchema = {
        "interview_id": interview_id,
        "topic": request.topic.strip(),
        "difficulty": request.difficulty,
        "started_at": _now(),
        "duration_seconds": request.duration_seconds,
        "problem": "",
        "constraints": [],
        "examples": [],
        "phase": "brute_force",
        "current_question": "",
        "pending_question_type": "brute_force_initial",
        "brute_force_answer": "",
        "brute_force_score": 0.0,
        "brute_force_feedback": "",
        "brute_force_satisfactory": False,
        "brute_force_missing_concepts": [],
        "brute_force_followup_count": 0,
        "brute_force_followup_question": "",
        "brute_force_followup_answer": "",
        "optimized_answer": "",
        "optimized_score": 0.0,
        "optimized_feedback": "",
        "optimized_satisfactory": False,
        "optimized_missing_concepts": [],
        "optimized_followup_count": 0,
        "optimized_followup_question": "",
        "optimized_followup_answer": "",
        "coding_started_at": None,
        "coding_duration_seconds": request.coding_duration_seconds,
        "programming_language": "",
        "submitted_code": "",
        "code_submitted": False,
        "test_results": [],
        "code_score": 0.0,
        "code_feedback": "Code has not been submitted.",
        "finish_reason": None,
        "final_report": None,
    }

    # Save first so the interview ID exists even if problem generation fails.
    create_interview(state)

    try:
        problem_result = generate_problem(state)
    except Exception:
        # Preserve the record for diagnostics, but do not return a
        # successful interview response.
        raise HTTPException(
            status_code=502,
            detail=(
                "Problem generation failed. "
                "The interview record was retained."
            ),
        )

    updated = update_interview(
        interview_id=interview_id,
        updates={
            **problem_result,
            "current_question": (
                "Explain your brute-force approach to solve this problem. "
                "Discuss the algorithm, time complexity, space complexity, "
                "and important edge cases."
            ),
        },
        expected_version=1,
    )

    if updated is None:
        raise HTTPException(
            status_code=409,
            detail="Could not persist the generated problem.",
        )

    return _public_interview(updated)


@router.get("/{interview_id}")
def get_interview_status(interview_id: str):
    """Retrieve the current question and interview status."""
    state = _load_interview(interview_id)
    state = _check_deadlines(state)

    return _public_interview(state)


@router.post("/{interview_id}/answer")
def submit_answer(interview_id: str, request: AnswerRequest):
    """Process the answer expected by the interview's current phase."""
    state = _load_interview(interview_id)
    state = _check_deadlines(state)

    if state["phase"] == "finished":
        raise HTTPException(
            status_code=409,
            detail="This interview has already finished.",
        )

    if state["phase"] == "coding":
        raise HTTPException(
            status_code=400,
            detail="The interview is in the coding phase.",
        )

    if state["pending_question_type"] in (
        "brute_force_initial",
        "brute_force_followup",
    ):
        state = _evaluate_brute_force_answer(state, request.answer.strip())

    elif state["pending_question_type"] in (
        "optimized_initial",
        "optimized_followup",
    ):
        state = _evaluate_optimized_answer(state, request.answer.strip())

    else:
        raise HTTPException(
            status_code=400,
            detail="The interview is not awaiting an explanation answer.",
        )

    return _public_interview(state)


@router.post("/{interview_id}/code")
def submit_code(
    interview_id: str,
    request: CodeSubmissionRequest,
):
    """
    Store submitted code and finish the interview.

    Actual code execution is not performed here. A sandboxed execution
    service must be connected before test results can be reported.
    """
    state = _load_interview(interview_id)
    state = _check_deadlines(state)

    if state["phase"] == "finished":
        raise HTTPException(
            status_code=409,
            detail="This interview has already finished.",
        )

    if state["phase"] != "coding":
        raise HTTPException(
            status_code=400,
            detail="The interview has not reached the coding phase.",
        )

    if state["code_submitted"]:
        raise HTTPException(
            status_code=409,
            detail="Code has already been submitted.",
        )

    state = _persist(
        state,
        {
            "submitted_code": request.code,
            "programming_language": request.programming_language,
            "code_submitted": True,
            "code_feedback": (
                "Code was submitted but has not been executed. "
                "Correctness is not verified."
            ),
            "test_results": [],
        },
    )

    state = _finish_interview(state, "submitted")

    return _public_interview(state)


@router.get("/{interview_id}/report")
def get_interview_report(interview_id: str):
    """Return the final report only after the interview has finished."""
    state = _load_interview(interview_id)
    state = _check_deadlines(state)

    if state["phase"] != "finished":
        raise HTTPException(
            status_code=409,
            detail="The interview has not finished yet.",
        )

    return {
        "interview_id": state["interview_id"],
        "finish_reason": state["finish_reason"],
        "final_report": state["final_report"],
        "brute_force_score": state["brute_force_score"],
        "optimized_score": state["optimized_score"],
        "code_score": state["code_score"],
        "code_submitted": state["code_submitted"],
        "test_results": state["test_results"],
    }
