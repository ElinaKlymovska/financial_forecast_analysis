import time
from random import randint

import boto3
import json
import logging

from botocore.exceptions import ClientError

from src.analysis.models.system_prompt import SYSTEM_PROMPT
from src.configuration.config import BEDROCK_MODEL, AWS_REGION, TEMPERATURE, MAX_TOKENS, MAX_RETRIES, BASE_WAIT_TIME
from langchain.prompts import PromptTemplate


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


def build_request_body(prompt_text):
    return json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [{"role": "user", "content": prompt_text}],
        "max_tokens": 500,
        "temperature": 0.7
    })


def parse_response(response):
    response_body = json.loads(response['body'].read().decode('utf-8'))
    return response_body.get("content", "Error parsing response")


def analyze_text_with_bedrock(prompt_text):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            body = build_request_body(prompt_text)
            bedrock_client = init_bedrock_client()
            response = bedrock_client.invoke_model(
                modelId=BEDROCK_MODEL,
                contentType="application/json",
                accept="*/*",
                body=body
            )
            return parse_response(response)

        except ClientError as error:
            if error.response['Error']['Code'] == 'ThrottlingException':
                retries += 1
                wait_time = BASE_WAIT_TIME * 2 ** retries + randint(0, BASE_WAIT_TIME)
                time.sleep(wait_time)
            else:
                raise error

        except Exception as e:
            raise e

    raise RuntimeError("Throttling limit reached")

