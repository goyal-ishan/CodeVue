from langgraph.graph import StateGraph, START, END
from app.graph.state import InterviewStateSchema

from app.graph.nodes import (
    generate_problem,
    evaluate_brute_force,
    generate_brute_force_followup,
    ask_for_optimization,
    evaluate_optimized,
    generate_optimized_followup,
    generate_report,
)

from app.graph.routing import (
    route_after_brute_force,
    route_after_optimized,
)


graph = StateGraph(InterviewStateSchema)

graph.add_node("generate_problem", generate_problem)

graph.add_node(
    "evaluate_brute_force",
    evaluate_brute_force
)

graph.add_node(
    "brute_force_followup",
    generate_brute_force_followup
)

graph.add_node(
    "ask_for_optimization",
    ask_for_optimization
)

graph.add_node(
    "evaluate_optimized",
    evaluate_optimized
)

graph.add_node(
    "optimized_followup",
    generate_optimized_followup
)

graph.add_node("generate_report", generate_report)


graph.add_edge(START, "generate_problem")
graph.add_edge("generate_problem", END)


graph.add_conditional_edges(
    "evaluate_brute_force",
    route_after_brute_force,
    {
        "optimized": "ask_for_optimization",
        "brute_force_followup": "brute_force_followup",
        "report": "generate_report",
    },
)

graph.add_edge("brute_force_followup", END)


graph.add_edge("ask_for_optimization", END)


graph.add_conditional_edges(
    "evaluate_optimized",
    route_after_optimized,
    {
        "coding": END,
        "optimized_followup": "optimized_followup",
        "report": "generate_report",
    },
)

graph.add_edge("optimized_followup", END)


graph.add_edge("generate_report", END)


# Compile graph
interview_graph = graph.compile()
