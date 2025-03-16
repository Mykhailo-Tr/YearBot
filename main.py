import telebot
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

# Токен бота
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

# Завантаження історичних даних
def load_data():
    with open("history_data.json", "r", encoding="utf-8") as file:
        return json.load(file)

data = load_data()

# Отримати всі роки з історичними подіями
@bot.message_handler(commands=['years'])
def list_years(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for year in data["years"].keys():
        keyboard.add(KeyboardButton(year))
    bot.send_message(message.chat.id, "Оберіть рік для перегляду подій:", reply_markup=keyboard)

# Отримати всі персон
@bot.message_handler(commands=['personalities'])
def list_personalities(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for name in data["personalities"].keys():
        keyboard.add(KeyboardButton(name))
    bot.send_message(message.chat.id, "Оберіть історичну особу:", reply_markup=keyboard)

# Отримати події за рік
@bot.message_handler(func=lambda message: message.text in data["years"])
def send_year_info(message):
    year = message.text
    events = "\n".join(data["years"][year])
    bot.send_message(message.chat.id, f"Історичні події {year} року:\n{events}")

# Отримати інформацію про історичну особу без врахування регістру
@bot.message_handler(func=lambda message: message.text.lower() in map(str.lower, data["personalities"]))
def send_personality_info(message):
    name = next(key for key in data["personalities"].keys() if key.lower() == message.text.lower())
    person = data["personalities"][name]
    bot.send_photo(message.chat.id, person["photo"], caption=f"{name}\n{person['info']}")

# Запуск бота
bot.polling(none_stop=True)
