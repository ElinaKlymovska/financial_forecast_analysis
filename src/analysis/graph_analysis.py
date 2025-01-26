from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.errors import InvalidUpdateError

from src.configuration.log_config import configure_logging

logging = configure_logging("graph_analysis.log")

# Визначення схеми стану
class TaskState(TypedDict):
    query: str
    route: Optional[str]  # Наступний вузол у графі
    results: Optional[List[dict]]  # Результати аналізу


def validate_data(data: TaskState) -> bool:
    return all(key in data and data[key] is not None for key in ["query", "route"])


# Функція для маршрутизації
def route_query(data: TaskState) -> TaskState:
    """
    Route the data based on its length.
    """
    if len(data["query"]) < 100:
        return {"route": "prompt_1", "results": None, "query": data["query"]}
    else:
        return {"route": "prompt_2", "results": None, "query": data["query"]}

# Вузол для короткого аналізу
def prompt_1(data: TaskState) -> TaskState:
    """
    Analyze short text using Bedrock.
    """
    # Замініть на реальну функцію для аналізу через Bedrock
    analysis = f"Short analysis of '{data['query']}'"
    return {"route": None, "results": [{"event": "Short analysis", "data": analysis}], "query": data["query"]}

# Вузол для детального аналізу
def prompt_2(data: TaskState) -> TaskState:
    """
    Analyze long text using Bedrock.
    """
    # Замініть на реальну функцію для аналізу через Bedrock
    analysis = f"Detailed analysis of '{data['query']}'"
    return {"route": None, "results": [{"event": "Detailed analysis", "data": analysis}], "query": data["query"]}

# Головна функція для аналізу
def analyze_sentiment_and_correlations_with_state_graph(data: list) -> List[dict]:
    """
    Perform sentiment analysis and correlation extraction using StateGraph.
    :param data: List of text items to analyze.
    :return: List of processed results with sentiment scores and analysis.
    """
    # Створення графа станів із визначеною схемою
    graph = StateGraph(state_schema=TaskState)
    graph.add_node("route_query", route_query)
    graph.add_node("prompt_1", prompt_1)
    graph.add_node("prompt_2", prompt_2)

    graph.add_edge(START, "route_query")
    graph.add_conditional_edges("route_query", lambda state: state["route"])
    graph.add_edge("prompt_1", END)
    graph.add_edge("prompt_2", END)

    app = graph.compile()

    # Обробка даних через граф
    processed_results = []
    for item in data:
        state_input = {"query": item, "route": None, "results": None}
        if not validate_data(state_input):
            logging.warning(f"Invalid data: {state_input}")
            continue
        try:
            for event in app.stream(state_input, stream_mode="values"):
                if event["results"]:
                    processed_results.append(event["results"])
                else:
                    logging.error(f"No results for: {state_input}")
        except InvalidUpdateError as e:
            logging.error(f"StateGraph Error: {e}. Data: {state_input}")

    return processed_results
