from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time


def scrape_yahoo_finance_news(url="https://finance.yahoo.com/topic/cryptocurrency/"):
    # Шлях до ChromeDriver
    driver_path = "/chromedriver-mac-arm64/chromedriver"
    service = Service(driver_path)

    # Налаштування браузера
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Безголовий режим
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Запуск браузера
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    time.sleep(5)  # Затримка для завантаження сторінки

    # Знаходимо заголовки новин
    news_elements = driver.find_elements(By.CSS_SELECTOR, "h3 a")
    news = []
    for elem in news_elements[:10]:  # Обмежимо до 10 новин
        try:
            headline = elem.text.strip()
            link = elem.get_attribute("href")
            news.append({"headline": headline, "link": link})
        except Exception as e:
            print(f"Error extracting news: {e}")

    driver.quit()
    return news


if __name__ == "__main__":
    yahoo_news = scrape_yahoo_finance_news()
    if not yahoo_news:
        print("No news found.")
    else:
        for i, article in enumerate(yahoo_news, 1):
            print(f"{i}. {article['headline']}")
            print(f"Link: {article['link']}")
