import boto3
import json
import logging

from langchain_core.prompts import PromptTemplate

from models.system_prompt import SYSTEM_PROMPT
from src.configuration.config import BEDROCK_MODEL, AWS_REGION, TEMPERATURE, MAX_TOKENS


# Ініціалізація клієнта Bedrock
def init_bedrock_client():
    """
    Initialize Bedrock client.
    """
    try:
        logging.info("Initializing Bedrock client...")
        return boto3.client("bedrock-runtime", region_name=AWS_REGION)
    except Exception as e:
        logging.error(f"Failed to initialize Bedrock client: {str(e)}")
        raise


# Запит до AWS Bedrock
def _query_bedrock(prompt: str):
    """
    Query AWS Bedrock with the correct API format for Anthropic Claude.
    """
    client = init_bedrock_client()

    logging.info(
        f"Sending request to Bedrock model: {BEDROCK_MODEL} with temperature={TEMPERATURE}, max_tokens={MAX_TOKENS}")

    # Формування запиту
    request_to_bedrock = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }
    try:
        response = client.invoke_model(
            modelId=BEDROCK_MODEL,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_to_bedrock)
        )
        response_body = response['body'].read().decode('utf-8')
        logging.info(f"Raw response: {response_body}")

        # Парсинг відповіді
        result = json.loads(response_body)
        return result
    except Exception as e:
        logging.error(f"Error querying Bedrock: {str(e)}")
        raise


from langchain.prompts import PromptTemplate

def query_bedrock(data_chunks: list, model_name: str, temperature: float = 0.7, max_tokens: int = 1000):
    """
    Query AWS Bedrock using LangChain's PromptTemplate for Anthropic Claude.
    """
    client = init_bedrock_client()

    # Шаблон для промпту
    template = """
    You are a professional analyst specializing in the connections between global events and the cryptocurrency market.
    Your task is to analyze how political, economic, business, and technological factors influence the value of specific cryptocurrencies.

    Human: {user_input}
    Assistant:
    """
    prompt_template = PromptTemplate(input_variables=["user_input"], template=template)

    results = []

    for i, chunk in enumerate(data_chunks):
        # Формуємо промпт для кожного чанка
        formatted_prompt = prompt_template.format(user_input=chunk.strip())
        messages = [
            {"role": "user", "content": formatted_prompt}
        ]

        payload = {
            "messages": messages,
            "anthropic_version": "bedrock-2023-05-31",
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        logging.info(f"Processing chunk {i+1}/{len(data_chunks)}")
        try:
            response = client.invoke_model(
                modelId=model_name,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload)
            )
            response_body = response['body'].read().decode('utf-8')
            logging.info(f"Raw response for chunk {i+1}: {response_body}")

            result = json.loads(response_body)
            results.append(result)
        except Exception as e:
            logging.error(f"Error processing chunk {i+1}: {str(e)}")
            results.append(None)

    return results
