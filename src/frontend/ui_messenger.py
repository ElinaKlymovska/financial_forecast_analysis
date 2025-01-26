import json

import streamlit as st
from io import BytesIO
from pypdf import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import AIMessage, HumanMessage
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate

from src.configuration.config import CHUNK_SIZE, CHUNK_OVERLAP
from src.messenger.initialization import init_chromadb, init_chat_model, init_memory
from src.messenger.session_state_manager import initialize_session_state, verify_session_state


def display_chat_interface():
    initialize_session_state()

    if st.session_state.vectorstore is None:
        st.session_state.vectorstore = init_chromadb()

    if st.session_state.llm is None:
        st.session_state.llm = init_chat_model()

    if st.session_state.memory is None:
        st.session_state.memory = init_memory()

    if st.session_state.chain is None:
        prompt = ChatPromptTemplate.from_template(
            """You are a helpful assistant who answers questions based on document context.

            Relevant context:
            {context}

            Question:
            {question}

            Answer:"""
        )
        retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 3})

        st.session_state.chain = ConversationalRetrievalChain.from_llm(
            llm=st.session_state.llm,
            retriever=retriever,
            memory=st.session_state.memory,
            combine_docs_chain_kwargs={"prompt": prompt},
            return_source_documents=True,
            verbose=True
        )

    verify_session_state()

    display_sidebar()
    display_chat()

def display_sidebar():
    with st.sidebar:
        st.header("📄 Document Upload")
        uploaded_files = st.file_uploader(
            "Upload documents",
            type=["txt", "md", "pdf"],
            accept_multiple_files=True,
            key="file_uploader"
        )

        if uploaded_files:
            process_files(uploaded_files)
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.session_state.memory.clear()
            st.rerun()

def process_files(uploaded_files):
    for file in uploaded_files:
        if file.name not in st.session_state.processed_files:
            with st.spinner(f"Processing {file.name}..."):
                try:
                    if file.type == "application/pdf":
                        pdf_reader = PdfReader(BytesIO(file.read()))
                        content = "\n".join(page.extract_text() for page in pdf_reader.pages)
                    elif file.type in ["text/plain", "text/markdown"]:
                        content = file.read().decode()
                    else:
                        st.error(f"Unsupported file type: {file.type}")
                        continue

                    # Обробка тексту
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
                    )
                    chunks = text_splitter.split_text(content)
                    st.session_state.vectorstore.add_texts(
                        texts=chunks,
                        metadatas=[{"filename": file.name}] * len(chunks)
                    )
                    st.session_state.processed_files.add(file.name)
                    st.success(f"Processed {file.name}")
                except Exception as e:
                    st.error(f"Error processing file {file.name}: {str(e)}")


def display_chat():
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message("assistant" if isinstance(message, AIMessage) else "user"):
                st.write(message.content)
    if question := st.chat_input("Ask a question about your documents or chat with me"):
        process_chat(question)


def process_chat(question):
    st.session_state.chat_history.append(HumanMessage(content=question))
    try:
        result = st.session_state.chain.invoke({"question": question})
        answer = result["answer"]
        st.session_state.chat_history.append(AIMessage(content=answer))
        # Відображаємо результат
        display_result(result)

        # Зберігаємо історію
        save_chat_history(st.session_state.chat_history)
    except Exception as e:
        st.error(f"Error: {str(e)}")


def display_result(result):
    # Відображаємо відповідь
    st.write("### Answer")
    st.write(result["answer"])

    # Відображаємо джерела
    if "source_documents" in result:
        st.write("### Sources")
        for doc in result["source_documents"]:
            st.write(f"**Filename**: {doc.metadata['filename']}")
            st.write(f"**Content**: {doc.page_content[:500]}...")  # Відображаємо перші 500 символів


def save_chat_history(chat_history, file_path="chat_history.json"):
    history = [{"role": "user" if isinstance(msg, HumanMessage) else "assistant", "content": msg.content} for msg in chat_history]
    with open(file_path, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)


def summarize_sources(source_documents):
    summary = []
    for doc in source_documents:
        filename = doc.metadata.get("filename", "Unknown")
        content_preview = doc.page_content[:300]  # Перегляд перших 300 символів
        summary.append(f"Filename: {filename}\nPreview: {content_preview}")
    return "\n\n".join(summary)
