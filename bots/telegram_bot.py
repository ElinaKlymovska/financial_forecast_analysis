from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
from src.notifications.notification_service import send_alert

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Стартова команда
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Вітаю! Я бот для фінансового аналізу. Використовуйте /alerts для налаштування сповіщень.")

# Команда для активації сповіщень
def alerts(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Сповіщення активовано. Ви отримаєте новини та аналітику в реальному часі.")

    # Тестове сповіщення
    example_message = send_alert()
    update.message.reply_text(example_message)

# Основний обробник повідомлень
def handle_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Введіть команду. Доступні команди: /start, /alerts")

# Основна функція для запуску бота
def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("alerts", alerts))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
