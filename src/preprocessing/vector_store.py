from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import CharacterTextSplitter
from langchain_aws import BedrockEmbeddings, BedrockLLM
from langchain_community.vectorstores import FAISS

from src.configuration.config import AWS_REGION, BEDROCK_MODEL
from src.configuration.log_config import configure_logging

logger = configure_logging(process_name="vector_store")


def preprocess_data(data) -> list:
    """Попередня обробка: текст очищується та розбивається на частини."""
    logger.info("Попередня обробка даних...")
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_data = [splitter.split_text(str(doc)) for doc in data]
    result = [item for sublist in split_data for item in sublist]
    logger.info("Попередня обробка завершена.")
    return result


def create_vector_store(data):
    """Створення векторного сховища з використанням Amazon Bedrock Embeddings."""
    if not data:
        raise ValueError("No data provided for vector store creation.")

    # Ініціалізація BedrockEmbeddings без client_kwargs
    embeddings_model = BedrockEmbeddings(region_name=AWS_REGION)

    cleaned_data = [str(doc) if isinstance(doc, dict) else doc for doc in data]
    # Генерація embedding для кожного документа
    embeddings_and_texts = [(embeddings_model.embed_query(doc), doc) for doc in cleaned_data]

    # Перевірка, чи є валідні вектори
    if not embeddings_and_texts:
        raise ValueError("No valid embeddings generated. Check your input data or Bedrock configuration.")

    embeddings, texts = zip(*embeddings_and_texts)

    # Створення FAISS векторного сховища
    vector_store = FAISS.from_texts(list(texts), embeddings_model)
    return vector_store


def search_vector_store(vector_store, query, k=5):
    """
    Пошук релевантної інформації у векторному сховищі.

    :param vector_store: Векторне сховище (наприклад, FAISS).
    :param query: Запит користувача.
    :param k: Кількість найбільш релевантних результатів (за замовчуванням 5).
    :return: Список релевантних документів.
    """
    try:
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})
        relevant_docs = retriever.get_relevant_documents(query)
        return relevant_docs
    except Exception as e:
        print(f"Error searching vector store: {e}")
        return []


def create_retrieval_chain(vector_store):
    logger.info("Створення RetrievalQA ланцюга...")
    try:
        llm = BedrockLLM(model=BEDROCK_MODEL)

        # Пошук векторів
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})  # 3 найбільш релевантні документи

        # Створення RetrievalQA з джерелами
        qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm=llm,
            chain_type="stuff",  # Можна замінити на map_reduce чи refine для складніших сценаріїв
            retriever=retriever,
            return_source_documents=True
        )

        logger.info("RetrievalQA ланцюг створено успішно.")
        return qa_chain
    except Exception as e:
        logger.error("Помилка створення RetrievalQA: %s", e)
        return None
