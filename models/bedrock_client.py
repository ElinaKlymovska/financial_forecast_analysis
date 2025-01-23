import boto3
import json
import time
from random import randint
import botocore.exceptions
from dotenv import load_dotenv
import os

load_dotenv()

BEDROCK_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"
REGION = os.getenv("AWS_REGION")
MAX_RETRIES = 4
BASE_WAIT_TIME = 2

bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name=REGION
)

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
            response = bedrock_client.invoke_model(
                modelId=BEDROCK_MODEL,
                contentType="application/json",
                accept="*/*",
                body=body
            )
            return parse_response(response)

        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'ThrottlingException':
                retries += 1
                wait_time = BASE_WAIT_TIME * 2 ** retries + randint(0, BASE_WAIT_TIME)
                time.sleep(wait_time)
            else:
                raise error

        except Exception as e:
            raise e

    raise RuntimeError("Throttling limit reached")


def process_text(text: str):
    bedrock_results = analyze_text_with_bedrock(text)

    # Формування результатів для відправки
    processed_data = {
        "text": text,
        "bedrock_sentiment": bedrock_results["sentiment"],
        "bedrock_entities": bedrock_results["entities"],
        "bedrock_summary": bedrock_results["summary"]
    }
    return processed_data