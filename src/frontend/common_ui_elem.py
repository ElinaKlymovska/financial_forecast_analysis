from itertools import islice
from typing import List, Set

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
    all_articles = ingest_data(query=DEFAULT_QUERIES)

    selected_articles = set(islice(all_articles, 5))

    # Analyzing data
    analysis_results = analyze_articles(selected_articles)

    # Display results
    st.write("### Crypto news and insights:")
    display_analysis_results(analysis_results)


def display_analysis_results(results: Set[AnalysisResult]) -> None:
    st.write("## Analysis Results")
    for result in results:
        with st.expander(result.initial_data.short_title, expanded=False):
            col1, col2 = st.columns([1, 3])
            with col1:
                image_path = result.initial_data.image_url or "data/images/newspaper with cartoon eyes.webp"
                st.image(image_path, use_container_width=True)
            with col2:
                st.write(f"### {result.initial_data.title}")
                st.write(f"**Published At:** {result.initial_data.published_at or 'Unknown'}")
                st.write(f"**Source:** {result.initial_data.source or 'Unknown'}")
                st.write(f"**Analysis:** {result.analyze_result}")
                if result.initial_data.url:
                    st.markdown(f"[Read Full Article]({result.initial_data.url})", unsafe_allow_html=True)
