from typing import List
from dataclasses import dataclass

from src.analysis.models.nlp_model import analyze_text_with_bedrock
from src.configuration.log_config import configure_logging
from src.ingestion.data_reception.base_datasource import NormalizedData

# Налаштування логування
logging = configure_logging(process_name="analyze_articles")


@dataclass
class AnalysisResult:
    initial_data: NormalizedData
    analyze_result: str


def parse_result(result: list) -> str:
    """
    Парсинг результатів аналізу.
    """
    return " ".join([item["text"] for item in result])



def analyze_articles(data: List[NormalizedData]) -> List[AnalysisResult]:
    """
    Анализ статей за помощью AWS Bedrock.
    """
    analyzed_results: List[AnalysisResult] = []

    for item in data:
        try:
            result = analyze_text_with_bedrock(item.content)
            text = parse_result(result)
            analyzed_results.append(AnalysisResult(initial_data=item, analyze_result= text))
        except Exception as e:
            logging.error(f"Failed to analyze article '{item.short_title}': {e}")

    return analyzed_results