from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from typing import List, Literal
from pydantic import BaseModel, Field
from app.graph.state import InterviewState
from app.services.llm import get_llm

class AnswerEvaluation(BaseModel):
    answer_score: float = Field(ge=0, le=10)
    answer_feedback: str
    missing_concepts: List[str]
    is_satisfactory: bool
    next_action: Literal["followup", "next_question", "finish"]


def generate_question(state: InterviewState) -> dict:
    llm = get_llm()

    system_message = SystemMessage(content="""
    You are an experienced technical interviewer conducting a
    structured interview for CodeVue.

    Follow these rules:

    1. Ask exactly ONE new main interview question at a time.
    2. Every question must be relevant to the selected topic.
    3. Match the selected difficulty level.
    4. Progress step by step:
       - Start with fundamental concepts.
       - Move to conceptual understanding.
       - Progress to application and problem-solving.
       - Ask more challenging questions as appropriate.
    5. Use the interview history to understand which concepts
       have already been covered.
    6. Do not repeat previous questions or test the same concept
       unnecessarily.
    7. Choose the next logical concept based on the topic,
       previous questions, and the candidate's performance.
    8. Ask a new main question, not a follow-up to the previous
       question.
    9. Do not reveal the answer or include an explanation.
    10. Return only the interview question.
    """)

    human_message = HumanMessage(content=f"""
    Selected topic: {state['topic']}
    Selected difficulty: {state['difficulty']}
    Main question number: {state['question_count'] + 1}

    Previous interview history:
    {state['conversation_history']}

    Latest answer feedback:
    {state['answer_feedback']}

    Missing concepts identified:
    {state['missing_concepts']}

    Generate the next appropriate main interview question.
    """)

def analyze_answer(state: InterviewState) -> dict:
    llm = get_llm().with_structured_output(AnswerEvaluation)

    prompt = f"""
    You are evaluating a candidate in a technical interview.

    Interview topic: {state['topic']}
    Difficulty: {state['difficulty']}
    Question: {state['current_question']}
    Candidate's answer: {state['current_answer']}

    Evaluate the answer fairly.

    Rules:
    - Give a score from 0 to 10.
    - Explain what was correct and what needs improvement.
    - List important missing concepts.
    - Set is_satisfactory to true if the answer is sufficiently correct.
    - Choose followup if a focused follow-up would help assess
      an important missing concept.
    - Choose next_question if the answer has been adequately assessed
      and no follow-up is needed.
    - Choose finish only if the interview should end.

    Return the evaluation using the required structured fields.
    """

    evaluation = llm.invoke(prompt)

    history = list(state["conversation_history"])
    history.append({
        "question": state["current_question"],
        "answer": state["current_answer"],
        "score": evaluation.answer_score,
        "feedback": evaluation.answer_feedback,
        "missing_concepts": evaluation.missing_concepts,
        "is_satisfactory": evaluation.is_satisfactory
    })

    return {
        "answer_score": evaluation.answer_score,
        "answer_feedback": evaluation.answer_feedback,
        "missing_concepts": evaluation.missing_concepts,
        "is_satisfactory": evaluation.is_satisfactory,
        "next_action": evaluation.next_action,
        "conversation_history": history,
        "current_answer": ""
    }


def generate_followup(state: InterviewState) -> dict:
    llm = get_llm()

    prompt = f"""
    You are a technical interviewer for CodeVue.

    Topic: {state['topic']}
    Difficulty: {state['difficulty']}
    Previous question: {state['current_question']}
    Candidate's answer: {state['conversation_history'][-1]['answer']}
    Missing concepts: {state['missing_concepts']}

    Generate exactly one concise follow-up question.
    Focus on one or more important missing concepts.
    Do not give away the answer.
    Return only the question.
    """

    response = llm.invoke(prompt)
    question = response.content.strip()

    return {
        "current_question": question,
        "current_answer": "",
        "followup_question": question,
        "followup_answer": "",
        "followup_count": state["followup_count"] + 1,
        "next_action": "followup"
    }


def generate_report(state: InterviewState) -> dict:
    llm = get_llm()

    prompt = f"""
    Generate a final technical interview report for CodeVue.

    Topic: {state['topic']}
    Difficulty: {state['difficulty']}
    Duration: {state['duration_seconds']} seconds

    Interview history:
    {state['conversation_history']}

    Include:
    1. Overall performance summary
    2. Strengths
    3. Weaknesses and missing concepts
    4. Scores and feedback for individual answers
    5. Specific recommendations for improvement

    Be constructive and base the report on the interview history.
    If there are no evaluated answers, clearly state that
    insufficient answers were provided to assess performance.
    """

    response = llm.invoke(prompt)

    return {
        "final_report": response.content.strip(),
        "next_action": "finish"
    }
