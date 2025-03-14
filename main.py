import telebot
import json
import os

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

year_data = {
    "1969": "В 1969 році люди вперше приземлилися на Місяць 🚀🌕.",
    "1989": "У 1989 році відбулося падіння Берлінської стіни 🧱💔.",
    "2000": "У 2000 році почався новий тисячолітній цикл, і всі хвилювались щодо Y2K проблеми 📅💻."
}


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привіт! 👋 Напишіть рік, і я розкажу, що сталося в тому році. 📅")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()

    if text.isdigit():
        year = text
        if year in year_data:
            bot.send_message(message.chat.id, year_data[year])
        else:
            bot.send_message(message.chat.id, f"У мене немає інформації про рік {year} 😕.")
    else:
        bot.send_message(message.chat.id, "Будь ласка, введіть рік 🗓️.")


if __name__ == '__main__':
    bot.polling(none_stop=True)
