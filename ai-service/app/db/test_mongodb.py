
from uuid import uuid4

from app.services.interview_store import (
    save_interview,
    get_interview,
)

test_id = str(uuid4())

test_state = {
    "interview_id": test_id,
    "phase": "brute_force",
    "topic": "Arrays",
    "brute_force_answer": "",
    "optimized_answer": "",
    "brute_force_followup_count": 0,
    "optimized_followup_count": 0,
}

save_interview(test_state)

saved_state = get_interview(test_id)

print("Saved interview:", saved_state)
