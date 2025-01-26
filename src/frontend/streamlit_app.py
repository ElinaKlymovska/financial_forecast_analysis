import pandas as pd
import streamlit as st

from models.system_prompt import DEFAULT_DATA
from src.ingestion.data_ingestion import ingest_data
from src.analysis.graph_analysis import analyze_sentiment_and_correlations_with_state_graph

# Page configuration
st.set_page_config(page_title="Crypto Market Analysis", page_icon="📈", layout="wide")
st.title("📊 Crypto Market Insights")
st.markdown("""
Welcome to the AI-powered crypto analysis tool! Here, you can:
- Upload documents for analysis
- Ask questions about the cryptocurrency market
- Explore connections between global events and crypto trends
""")


# User-defined additional parameters
st.sidebar.header("Additional Analysis Parameters")
additional_query = st.sidebar.text_input("Add keywords (comma-separated):", "")
filters = st.sidebar.multiselect(
    "Category Filters", ["Bitcoin", "Ethereum", "Altcoins", "Market Trends"], default=[]
)


def display_default_data():
    """
    Display default data in the Streamlit interface as a table.
    """
    df = pd.DataFrame(DEFAULT_DATA)
    st.subheader("Default Data: Sample Analysis of Global Factors")
    st.table(df)


def load_and_analyze_data():
    st.write("⏳ Loading and analyzing data...")
    queries = DEFAULT_QUERIES
    if additional_query:
        queries.extend([q.strip() for q in additional_query.split(",")])

    # Fetching data
    articles = []
    for query in queries:
        data = ingest_data(query=query)
        articles.extend(data)

    # Analyzing data
    analysis_results = analyze_sentiment_and_correlations_with_state_graph(articles)

    # Display results
    st.write("### Analysis Results")
    for idx, result in enumerate(analysis_results):
        st.write(f"**Query {idx + 1}:** {queries[idx]}")
        st.json(result)

    # Display events table
    st.write("### Most Interesting Events")
    for article in articles[:10]:  # Displaying the first 10 articles
        st.write(f"- **{article['title']}**: {article['content']}")

# Відобразити дефолтні дані
if st.sidebar.checkbox("Show default data", value=True):
    display_default_data()
