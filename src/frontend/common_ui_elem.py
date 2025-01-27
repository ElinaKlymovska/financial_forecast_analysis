from typing import List

import streamlit as st

from src.analysis.analyze_articles import analyze_articles, AnalysisResult
from src.analysis.models.system_prompt import DEFAULT_QUERIES
from src.configuration.log_config import configure_logging
from src.ingestion.data_ingestion import ingest_data

logging = configure_logging("common_ui_elem")


def display_title():
    st.set_page_config(page_title="Crypto Market Analysis", page_icon="📈", layout="wide")
    st.title("📊 Crypto Market Insights")
    st.markdown("""
    Welcome to the AI-powered crypto analysis tool! Here, you can:
    - Upload documents for analysis
    - Ask questions about the cryptocurrency market
    - Explore connections between global events and crypto trends
    """)


def load_and_analyze_data():
    st.write("⏳ Loading and analyzing data...")
    queries = DEFAULT_QUERIES

    # Fetching data
    articles = []
    for query in queries:
        data = ingest_data(query=query)
        articles.extend(data[:1])

    # Analyzing data
    analysis_results = analyze_articles(articles[:3])

    # Display results
    st.write("### Crypto news and insights:")
    display_analysis_results(analysis_results)


def display_analysis_results(results: List[AnalysisResult]) -> None:
    """
    Відображає результати аналізу новин із можливістю розгортання деталей.
    :param results: Список результатів аналізу.
    """
    st.write("## Analysis Results")
    for result in results:
        with st.expander(result.initial_data.title, expanded=False):
            st.write(f"### {result.initial_data.title}")
            st.write(f"**Published At:** {result.initial_data.published_at or 'Unknown'}")
            st.write(f"**Source:** {result.initial_data.source or 'Unknown'}")
            st.write(f"**Analysis:** {result.analyze_result}")
            if result.initial_data.url:
                st.markdown(f"[Read Full Article]({result.initial_data.url})", unsafe_allow_html=True)
