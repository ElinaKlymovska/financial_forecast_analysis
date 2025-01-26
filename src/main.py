import subprocess


if __name__ == "__main__":
    print("Launching Streamlit...")
    subprocess.run(["python3", "-m", "streamlit", "run", "frontend/streamlit_app.py"])


# import json
# import logging
#
# from models.nlp_model import query_bedrock
# from src.ingestion.data_ingestion import ingest_data
# from src.configuration.log_config import configure_logging
# from src.preprocessing.vector_store import preprocess_data
#
# configure_logging()
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#
#     # Крок 1: Збір даних
#     logging.info("Step 1: Starting data ingestion...")
#     ingested_data = ingest_data("crypto, blockchain, global events")
#     logging.info(f"Step 1: Data ingestion complete. {len(ingested_data)} articles ingested.")
#
#     # Крок 2: Попередня обробка
#     logging.info("Step 2: Preprocessing data...")
#     preprocessed_data = preprocess_data(ingested_data)
#     logging.info(f"Step 2: Data preprocessing complete. {len(preprocessed_data)} chunks generated.")
#
#     # Крок 3: Аналіз за допомогою Bedrock
#     logging.info("Step 3: Analyzing data with Bedrock...")
#
#     # Дані для аналізу
#     prompt_example = [
#         "What is the impact of rising interest rates on Bitcoin prices?",
#         "How does regulatory uncertainty affect Ethereum's adoption?"
#     ]
#     model_name = "anthropic.claude-3-sonnet-20240229-v1:0"
#
#     try:
#         summaries = query_bedrock(prompt_example, model_name)
#         for i, summary in enumerate(summaries):
#             if summary:
#                 logging.info(f"Summary {i+1}: {json.dumps(summary, indent=2)}")
#             else:
#                 logging.error(f"Summary {i+1} failed.")
#     except Exception as e:
#         logging.error(f"Failed to process queries: {str(e)}")


