def calculate_average_score(conversation_history: list[dict]) -> float:
    if not conversation_history:
        return 0.0

    scores = [
        item["score"]
        for item in conversation_history
        if isinstance(item.get("score"), (int, float))
    ]

    if not scores:
        return 0.0

    return round(sum(scores) / len(scores), 2)


def get_report_summary(conversation_history: list[dict]) -> dict:
    total_questions = len(conversation_history)

    scores = [
        item["score"]
        for item in conversation_history
        if isinstance(item.get("score"), (int, float))
    ]

    strengths = []
    improvement_areas = []

    for item in conversation_history:
        feedback = item.get("feedback", "")
        missing_concepts = item.get("missing_concepts", [])

        if item.get("is_satisfactory"):
            strengths.append(feedback)

        if missing_concepts:
            improvement_areas.extend(missing_concepts)

    return {
        "total_evaluated_answers": total_questions,
        "average_score": calculate_average_score(conversation_history),
        "highest_score": max(scores) if scores else 0.0,
        "lowest_score": min(scores) if scores else 0.0,
        "strengths": strengths,
        "improvement_areas": sorted(set(improvement_areas))
    }
