from langgraph.graph import StateGraph, START, END
from app.graph.state import InterviewState
from app.graph.nodes import(
    generate_question,
    analyze_answer,
    generate_followup,
    generate_report
)
from app.graph.routing import route_next_action

def build_graph():
    graph = StateGraph(InterviewState)

    graph.add_node("generate_question", generate_question)
    graph.add_node("analyze_answer", analyze_answer)
    graph.add_node("generate_followup", generate_followup)
    graph.add_node("generate_report", generate_report)

    graph.add_edge(START, "generate_question")
    graph.add_edge("generate_question", END)

    graph.add_conditional_edges(
        "analyze_answer",
        route_next_action,
        {
            "followup": "generate_followup",
            "next_question": "generate_question",
            "finish": "generate_report"
        }
    )

    graph.add_edge("generate_followup", END)

    graph.add_edge("generate_report", END)

    return graph.compile()