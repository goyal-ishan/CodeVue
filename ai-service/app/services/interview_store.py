
from datetime import datetime, timezone
from typing import Any

from pymongo import ReturnDocument

from app.db.mongodb import interviews_collection
from app.graph.state import InterviewStateSchema


def initialize_interview_store() -> None:
    """Create the unique index required for interview persistence."""
    interviews_collection.create_index(
        [("interview_id", 1)],
        unique=True,
        name="unique_interview_id",
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


def get_interview(
    interview_id: str,
) -> dict[str, Any] | None:
    """Retrieve the complete persisted interview state."""
    return interviews_collection.find_one(
        {"interview_id": interview_id},
        {"_id": 0},
    )


def update_interview(
    interview_id: str,
    updates: dict[str, Any],
    expected_version: int,
) -> dict[str, Any] | None:
    """
    Update an existing interview only if its version matches.

    Returns the updated document, or None if the interview
    does not exist or its version has changed.
    """
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
