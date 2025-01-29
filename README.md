# 📊 Financial Forecast Analysis System

## 📝 Опис проекту
**Financial Forecast Analysis System** — це система аналізу фінансових прогнозів, яка використовує **LangChain**, **Amazon Bedrock**, **Streamlit** та **векторні сховища** для обробки та аналізу фінансових даних. Вона підтримує роботу з новинами, звітами та іншими джерелами, дозволяючи отримувати прогнози щодо ринкових трендів та потенційних ризиків.

## 🚀 Основні можливості
- **RAG (Retrieval-Augmented Generation)** для пошуку релевантної інформації в документах.
- **Аналіз ринкових новин** та автоматичне створення прогнозів.
- **Чат-бот** з підтримкою історії розмов та пам'яті.
- **Обробка PDF, TXT та інших форматів** для фінансового аналізу.
- **Інтерактивний UI на Streamlit** для взаємодії з системою.
- **Векторне сховище (Chroma)** для пошуку релевантних документів.
- **Підтримка багатокористувацької пам'яті** через LangGraph.

## 🏗️ Технологічний стек
- **Мова програмування:** Python 3.12
- **Фреймворки та бібліотеки:**
    - LangChain
    - Streamlit
    - Amazon Bedrock
    - ChromaDB
    - PyPDF для обробки PDF
    - Boto3 для роботи з AWS
- **Інструменти:**
    - `Docker` (за бажанням, для розгортання)
    - `virtualenv / conda` (рекомендовано для ізоляції залежностей)

## 📦 Встановлення та запуск
### 🔧 1. Клонування репозиторію
```bash
git clone https://github.com/your-repo/financial-forecast-analysis.git
cd financial-forecast-analysis
```

### 📌 2. Створення та активація віртуального середовища (virtualenv або conda)
```bash
# Використання virtualenv
python -m venv venv  # для Windows
source venv/bin/activate  # для MacOS/Linux
venv\Scripts\activate  # для Windows

# Використання conda
conda create --name financial_forecast python=3.12
conda activate financial_forecast
```

### 📥 3. Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 🔑 4. Налаштування `.env` 
Для коректної роботи необхідно створити `.env` файл у кореневій директорії проєкту. Приклад:

```env
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
OPENAI_API_KEY=your_openai_api_key
KINESIS_STREAM_NAME=market-data-stream
CRYPTOCOMPARE_API_KEY=your_cryptocompare_api_key
NEWS_API_KEY=your_news_api_key
TWITTER_API_KEY=your_twitter_api_key
ACCESS_TOKEN=your_twitter_access_token
ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
BEARER_TOKEN=your_twitter_bearer_token
```

Також у файлі `.aws/credentials` можуть зберігатися додаткові дані доступу до aws-сервісів.

### 🏁 5. Запуск системи
```bash
streamlit run src/frontend/streamlit_app.py
```

## 📂 Структура проекту
```
financial-forecast-analysis/
│── src/
│   ├── frontend/
│   │   ├── streamlit_app.py        # Головний UI-додаток
│   │   ├── ui_messenger.py         # Чат-інтерфейс
│   │   ├── common_ui_elem.py       # Спільні UI-компоненти
│   ├── messenger/
│   │   ├── session_state_manager.py # Управління станом сесії
│   │   ├── initialization.py        # Ініціалізація LLM та сховищ
│   ├── analysis/
│   │   ├── vector_store.py          # Робота з векторними сховищами
│   ├── models/
│   │   ├── nlp_model.py             # Аналіз тексту з Amazon Bedrock
│── requirements.txt                 # Залежності проекту
│── .env                              # Файл змінних середовища
│── credentials                       # Файл з доступами до сервісів
│── README.md                         # Документація
```

## ⚙️ Налаштування змінних середовища
Перед запуском налаштуйте змінні середовища (можна створити `.env` файл, як вказано вище) та перевірте `credentials`.


## 📌 Подальші плани
- 🔄 Оптимізація LangGraph для збереження пам'яті між сесіями.
- 📊 Додавання графічного аналізу трендів.
- 🔍 Інтеграція більшої кількості джерел фінансової інформації.

## 👥 Автори та контакти
- 📧 Контакт: klymovska.elina@gmail.com
- GitHub: https://github.com/ElinaKlymovska/financial_forecast_analysis.git

