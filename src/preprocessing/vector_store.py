from langchain.text_splitter import CharacterTextSplitter
from langchain_aws import BedrockEmbeddings


def preprocess_data(data):
    """Попередня обробка: текст очищується та розбивається на частини."""
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_data = [splitter.split_text(str(doc)) for doc in data]
    return [item for sublist in split_data for item in sublist]


def create_vector_store(data):
    """Створення векторного сховища з використанням Amazon Bedrock Embeddings."""
    if not data:
        raise ValueError("No data provided for vector store creation.")

    # Ініціалізація BedrockEmbeddings без client_kwargs
    embeddings_model = BedrockEmbeddings(region_name="us-east-1")

    # Генерація embedding для кожного документа
    embeddings_and_texts = [(embeddings_model.embed_query(doc), doc) for doc in data]

    # Перевірка, чи є валідні вектори
    if not embeddings_and_texts:
        raise ValueError("No valid embeddings generated. Check your input data or Bedrock configuration.")

    embeddings, texts = zip(*embeddings_and_texts)

    # Створення FAISS векторного сховища
    from langchain_community.vectorstores import FAISS
    vector_store = FAISS.from_texts(list(texts), embeddings_model)
    return vector_store
