from typing import TypedDict
from langgraph.graph import StateGraph, START

# Визначення структури даних
class TaskState(TypedDict):
    query: str
    route: str
    result: list

def initialize_data(state):
    """Ініціалізація даних і визначення маршруту."""
    return {"query": state["query"], "route": "prompt_1" if len(state["query"]) < 100 else "prompt_2"}

def route_query(state):
    """Маршрутизація даних."""
    return {"route": state["route"]}

def prompt_1(state):
    """Обробка коротких запитів."""
    result = [{"event": f"Short-{i}", "sentiment_score": len(doc) % 10} for i, doc in enumerate(state["query"])]
    return {"result": result}

def prompt_2(state):
    """Обробка довгих запитів."""
    result = [{"event": f"Long-{i}", "sentiment_score": len(doc) % 10} for i, doc in enumerate(state["query"])]
    return {"result": result}


def correlation_analysis(state):
    """Аналіз кореляцій для ринкових подій."""
    result = [{"event": f"Correlated-{i}", "impact_score": len(doc) % 5} for i, doc in enumerate(state["query"])]
    return {"result": result}


def analyze_with_state_graph(data):
    """Аналіз із використанням StateGraph."""
    graph = StateGraph(state_schema=TaskState)

    # Додавання вузлів
    graph.add_node("initialize", initialize_data)
    graph.add_node("route_query", route_query)
    graph.add_node("prompt_1", prompt_1)
    graph.add_node("prompt_2", prompt_2)
    graph.add_node("correlation_analysis", correlation_analysis)

    # Зв'язки між вузлами
    graph.add_edge(START, "initialize")
    graph.add_edge("initialize", "route_query")
    graph.add_edge("prompt_1", "correlation_analysis")
    graph.add_conditional_edges("route_query", lambda state: state["route"])
    graph.add_edge("prompt_1", "__end__")
    graph.add_edge("prompt_2", "__end__")
    graph.add_edge("correlation_analysis", "__end__")


    app = graph.compile()

    # Запуск графа
    results = []
    for event in app.stream({"query": data}, stream_mode="values"):
        results.append(event)
    return results
