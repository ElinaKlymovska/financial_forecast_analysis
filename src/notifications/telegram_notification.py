import requests

TELEGRAM_API_URL = "https://api.telegram.org/bot{}/sendMessage"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

def send_alert(message="Нова фінансова новина: ринок на підйомі!") -> str:
    url = TELEGRAM_API_URL.format(TELEGRAM_TOKEN)
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return "Сповіщення надіслано успішно!"
    else:
        return "Помилка надсилання сповіщення."
