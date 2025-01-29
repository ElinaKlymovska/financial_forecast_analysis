import boto3
import json
import os
from dotenv import load_dotenv
from src.configuration.config import AWS_REGION


load_dotenv()
KINESIS_STREAM_NAME = os.getenv("KINESIS_STREAM_NAME")


def send_to_kinesis(data, stream_name=KINESIS_STREAM_NAME, region_name=AWS_REGION):
    """Відправка даних у потік Kinesis."""
    kinesis_client = boto3.client("kinesis", region_name=region_name)
    response = kinesis_client.put_record(
        StreamName=stream_name,
        Data=json.dumps(data),
        PartitionKey="partition_key"
    )
    return response







if __name__ == "__main__":
    example_data = {
        "headline": "Trump launches new cryptocurrency",
        "source": "Example News",
        "published_at": "2025-01-22T12:00:00Z"
    }

    while True:
        response = send_to_kinesis(example_data)
        time.sleep(5)
