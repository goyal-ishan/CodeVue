from typing import List, Literal
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from app.services.llm import get_llm
from app.data.questions_bank import QUESTION_BANK
from app.prompts.interviewer import (
    INTERVIEWER_SYSTEM_PROMPT,
    ANSWER_EVALUATION_PROMPT,
    FOLLOWUP_QUESTION_PROMPT,
    FINAL_REPORT_PROMPT,
)
from app.graph.state import InterviewStateSchema


class CodingProblem(BaseModel):
    problem: str = Field(description="Complete coding problem statement")
    constraints: List[str] = Field(description="Problem constraints")
    examples: List[dict[str,any]] = Field(description="Input-output examples")

class AnswerEvaluation(BaseModel):
    score: float = Field(ge=0, le=10)
    feedback: str
    missing_concepts: List[str]
    is_satisfactory: bool

class FollowupResponse(BaseModel):
    question: str

def generate_problem(state: InterviewStateSchema) -> InterviewStateSchema:
    problem_id = state["problem_id"]

    if problem_id not in QUESTION_BANK:
        raise ValueError(f"Unknown problem ID: {problem_id}")

    selected_problem = QUESTION_BANK[problem_id]

    if selected_problem["difficulty"] != state["difficulty"]:
        raise ValueError("Selected problem difficulty does not match.")

    return {
        "problem": selected_problem["description"],
        "constraints": selected_problem["constraints"],
        "examples": selected_problem["examples"],
        "problem_title": selected_problem["title"],
        "test_cases": selected_problem["test_cases"],
        "phase": "brute_force",
    }

def evaluate_brute_force(state: InterviewStateSchema) -> dict:
    llm = get_llm().with_structured_output(AnswerEvaluation)

    followup_question = state.get("brute_force_followup_question", "")
    followup_answer = state.get("brute_force_followup_answer", "")

    if followup_question and followup_answer:
        candidate_response = f"""
Original brute-force explanation:
{state["brute_force_answer"]}

Follow-up question:
{followup_question}

Candidate's follow-up answer:
{followup_answer}
"""
    else:
        candidate_response = state["brute_force_answer"]

    result = llm.invoke([
        SystemMessage(content=ANSWER_EVALUATION_PROMPT),
        HumanMessage(content=f"""
Interview phase: Brute-force approach

Problem:
{state["problem"]}

Constraints:
{state["constraints"]}

{candidate_response}

Evaluate whether the proposed brute-force approach is correct.
Do not require an optimized solution at this stage.

If a follow-up answer is provided, use it to reassess the candidate's
understanding alongside the original explanation. Do not penalize
the candidate merely because they needed a hint.
""")
    ])

    return {
        "brute_force_score": result.score,
        "brute_force_feedback": result.feedback,
        "brute_force_satisfactory": result.is_satisfactory,
        "brute_force_missing_concepts": result.missing_concepts,
    }

def generate_brute_force_followup(state: InterviewStateSchema) -> InterviewStateSchema:
    llm = get_llm().with_structured_output(FollowupResponse)

    result = llm.invoke([
        SystemMessage(content=FOLLOWUP_QUESTION_PROMPT),
        HumanMessage(content=f"""
Problem:
{state["problem"]}

Candidate's brute-force explanation:
{state["brute_force_answer"]}

Evaluation feedback:
{state["brute_force_feedback"]}

Missing concepts:
{state.get("brute_force_missing_concepts", [])}

Follow-ups already used:
{state["brute_force_followup_count"]}

Generate one relevant follow-up question or small hint.
Do not reveal the complete solution.
""")
    ])

    return {
        "brute_force_followup_question":result.question,
        "brute_force_followup_count": (
            state["brute_force_followup_count"] + 1
        ),
    }

def ask_for_optimization(state: InterviewStateSchema) -> dict:
    return {
        "current_question": (
            "Good. Now try to optimize your approach. "
            "Can you improve its time or space complexity?"
        ),
        "phase": "optimized",
    }

def evaluate_optimized(state: InterviewStateSchema) -> dict:
    llm = get_llm().with_structured_output(AnswerEvaluation)

    followup_question = state.get("optimized_followup_question", "")
    followup_answer = state.get("optimized_followup_answer", "")

    if followup_question and followup_answer:
        candidate_response = f"""
Original optimized explanation:
{state["optimized_answer"]}

Follow-up question:
{followup_question}

Candidate's follow-up answer:
{followup_answer}
"""
    else:
        candidate_response = state["optimized_answer"]

    result = llm.invoke([
        SystemMessage(content=ANSWER_EVALUATION_PROMPT),
        HumanMessage(content=f"""
Interview phase: Optimized approach

Problem:
{state["problem"]}

Candidate's original brute-force approach:
{state["brute_force_answer"]}

{candidate_response}

Evaluate correctness, time complexity, space complexity, and edge cases.
Accept any valid and sufficiently efficient approach.

If a follow-up answer is provided, use it to reassess the candidate's
understanding alongside the original explanation. Do not penalize
the candidate merely because they needed a hint.
""")
    ])

    return {
        "optimized_score": result.score,
        "optimized_feedback": result.feedback,
        "optimized_satisfactory": result.is_satisfactory,
        "optimized_missing_concepts": result.missing_concepts,
    }


def generate_optimized_followup(state: dict) -> dict:
    llm = get_llm().with_structured_output(FollowupResponse)

    result = llm.invoke([
        SystemMessage(content=FOLLOWUP_QUESTION_PROMPT),
        HumanMessage(content=f"""
Problem:
{state["problem"]}

Candidate's optimized explanation:
{state["optimized_answer"]}

Evaluation feedback:
{state["optimized_feedback"]}

Missing concepts:
{state.get("optimized_missing_concepts", [])}

Follow-ups already used:
{state["optimized_followup_count"]}

Generate one relevant follow-up question or small hint.
Do not reveal the complete optimized solution.
""")
    ])

    return {
        "optimized_followup_question": result.question,
        "optimized_followup_count": (
            state["optimized_followup_count"] + 1
        ),
    }


def generate_report(state: dict) -> dict:
    llm = get_llm()

    response = llm.invoke([
        SystemMessage(content=FINAL_REPORT_PROMPT),
        HumanMessage(content=f"""
Generate the final report using the interview data below.

Problem:
{state.get("problem", "Not available")}

Brute-force explanation:
{state.get("brute_force_answer", "Not provided")}

Brute-force score:
{state.get("brute_force_score", "Not evaluated")}

Brute-force feedback:
{state.get("brute_force_feedback", "Not available")}

Optimized explanation:
{state.get("optimized_answer", "Not provided")}

Optimized score:
{state.get("optimized_score", "Not evaluated")}

Optimized feedback:
{state.get("optimized_feedback", "Not available")}

Programming language:
{state.get("programming_language", "Not specified")}

Submitted code:
{state.get("submitted_code", "No code submitted")}

Code submitted:
{state.get("code_submitted", False)}

Code score:
{state.get("code_score", "Not evaluated")}

Code feedback:
{state.get("code_feedback", "Not available")}

Test results:
{state.get("test_results", [])}

Finish reason:
{state.get("finish_reason", "Not specified")}

Instructions:
- Summarize the candidate's performance in each interview phase.
- Highlight strengths and areas for improvement.
- Use only the supplied evidence; do not invent scores, test results, or candidate responses.
- Clearly state whether code was submitted and whether it was actually executed against test cases.
- If code was not submitted, mark the coding assessment as not completed rather than assigning an unsupported conclusion.
- If test results are unavailable, explicitly state that correctness could not be verified through execution.
- Provide actionable recommendations for improvement.
""")
    ])

    return {
        "final_report": response.content,
        "phase": "finished",
    }
