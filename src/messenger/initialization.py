import os
import streamlit as st
from langchain_community.chat_models import BedrockChat
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory


from src.configuration.config import BEDROCK_MODEL, PERSIST_DIR, TEMPERATURE, AWS_REGION, EMBEDDING_MODEL

# Initialize ChromaDB with persistence
os.makedirs(PERSIST_DIR, exist_ok=True)


# Initialize LangChain chat model
@st.cache_resource(show_spinner=False)
def init_chat_model():
    return BedrockChat(
        model_id=BEDROCK_MODEL,
        model_kwargs={"temperature": TEMPERATURE},
        region_name=AWS_REGION
    )


# Initialize embeddings
@st.cache_resource(show_spinner=False)
def init_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )


# Initialize ChromaDB and create retriever
@st.cache_resource(show_spinner=False)
def init_chromadb():
    """Initialize ChromaDB with persistence and transformer embeddings"""
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # Initialize embeddings
    embeddings = init_embeddings()

    # Create or load Chroma vector store
    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="documents"
    )

    return vectorstore


# Initialize conversation memory
@st.cache_resource(show_spinner=False)
def init_memory():
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )