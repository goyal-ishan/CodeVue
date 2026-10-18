import time
from app.graph.state import InterviewStateSchema


def is_interview_expired(state: InterviewStateSchema) -> bool:
    return time.time() - state["started_at"] >= state["duration_seconds"]


def route_after_brute_force(state: InterviewStateSchema) -> str:
    if is_interview_expired(state):
        return "report"

    if state["brute_force_satisfactory"]:
        return "optimized"

    if state["brute_force_followup_count"] < 2:
        return "brute_force_followup"

    return "optimized"


def route_after_optimized(state: InterviewStateSchema) -> str:
    if is_interview_expired(state):
        return "report"

    if state["optimized_satisfactory"]:
        return "coding"

    if state["optimized_followup_count"] < 2:
        return "optimized_followup"

    return "coding"


def route_after_coding(state: InterviewStateSchema) -> str:
    if state["code_submitted"]:
        return "report"

    if is_interview_expired(state):
        return "report"

    return "coding"