import time
from app.graph.state import InterviewState


def route_next_action(state: InterviewState) -> str:
    # Finish if the interview duration has expired
    if time.time() - state["started_at"] >= state["duration_seconds"]:
        return "finish"

    # Finish if the interview is explicitly ended
    if state["next_action"] == "finish":
        return "finish"

    # Follow-up question, if the limit has not been reached
    if state["next_action"] == "followup":
        if state["followup_count"] < state["max_followups"]:
            return "followup"

        return "next_question"

    # Otherwise, move to the next main question
    return "next_question"