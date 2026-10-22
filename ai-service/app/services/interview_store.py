from datetime import datetime, timezone
from typing import Any, List

from pymongo import ReturnDocument, DESCENDING

from app.db.mongodb import interviews_collection
from app.graph.state import InterviewStateSchema


def initialize_interview_store() -> None:
    """Create indexes required for interview persistence and user history lookups."""
    interviews_collection.create_index(
        [("interview_id", 1)],
        unique=True,
        name="unique_interview_id",
    )
    # Index for fast user history and progress queries
    interviews_collection.create_index(
        [("user_email", 1), ("started_at", DESCENDING)],
        name="user_email_started_at_idx",
    )


def create_interview(state: InterviewStateSchema) -> None:
    """Persist a newly initialized interview."""
    now = datetime.now(timezone.utc)

    document: dict[str, Any] = {
        **state,
        "created_at": now,
        "updated_at": now,
        "version": 1,
    }

    interviews_collection.insert_one(document)


def get_interview(interview_id: str) -> dict[str, Any] | None:
    """Retrieve the complete persisted interview state."""
    return interviews_collection.find_one(
        {"interview_id": interview_id},
        {"_id": 0},
    )


def get_interviews_by_user(user_email: str) -> List[dict[str, Any]]:
    """Retrieve all interviews associated with a user, newest first."""
    cursor = interviews_collection.find(
        {"user_email": user_email},
        {"_id": 0, "test_cases": 0},  # Exclude internal test cases from user list
    ).sort("started_at", DESCENDING)

    return list(cursor)


def update_interview(
    interview_id: str,
    updates: dict[str, Any],
    expected_version: int,
) -> dict[str, Any] | None:
    """Update an existing interview only if its version matches."""
    protected_fields = {
        "_id",
        "interview_id",
        "created_at",
        "updated_at",
        "version",
    }

    if protected_fields.intersection(updates):
        raise ValueError("Cannot update protected persistence fields")

    if not updates:
        return get_interview(interview_id)

    return interviews_collection.find_one_and_update(
        {
            "interview_id": interview_id,
            "version": expected_version,
        },
        {
            "$set": {
                **updates,
                "updated_at": datetime.now(timezone.utc),
            },
            "$inc": {"version": 1},
        },
        return_document=ReturnDocument.AFTER,
        projection={"_id": 0},
    )