from src.analysis.state_graph_analysis import analyze_with_state_graph
from src.ingestion.data_ingestion import ingest_data
from src.preprocessing.vector_store import preprocess_data, create_vector_store


def main():
    """Основний процес збору, обробки та аналізу даних."""

    # Завантаження даних через API
    query = "crypto"  # Приклад запиту
    combined_data = ingest_data(query=query)

    if not combined_data:
        print("No data found for the given query.")
        return

    print(f"Fetched {len(combined_data)} articles from APIs.")

    # Попередня обробка
    processed_data = preprocess_data(combined_data)

    # Створення векторного сховища
    vector_store = create_vector_store(processed_data)

    # Пошук у векторному сховищі
    retriever = vector_store.as_retriever()  # Перетворення в retriever
    query_text = "What are the latest trends in cryptocurrency?"
    search_results = retriever.get_relevant_documents(query_text)
    print(f"Search results for query '{query_text}':", search_results)

    # Аналіз через StateGraph
    state_graph_results = analyze_with_state_graph(processed_data)
    print("State Graph Analysis Results:", state_graph_results)

    # Аналіз через Bedrock
    # for text in processed_data:
    #     bedrock_result = analyze_text_with_bedrock(f"Analyze this text: {text}")
    #     print(f"Bedrock Result for '{text}':", bedrock_result)
    #
    #     # Відправка у Kinesis
    #     send_to_kinesis({"text": text, "analysis": bedrock_result})
    #     print(f"Sent to Kinesis: {text}")

if __name__ == "__main__":
    main()
