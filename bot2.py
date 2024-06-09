import os
import requests
from telebot import TeleBot
from datetime import datetime
from dateutil.parser import parse

# Muhit o'zgaruvchisi orqali bot tokenini olish
BOT_TOKEN = os.environ.get("7210839302:AAHIcZcCKsQlJqmLbVVN8mAzo9St7umo-qY")  # Muhit o'zgaruvchisi to'g'ri o'rnatilganligiga ishonch hosil qiling
POLLING_TIMEOUT = None

# Botni ishga tushirish
bot = TeleBot('7210839302:AAHIcZcCKsQlJqmLbVVN8mAzo9St7umo-qY')


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Assalomualeykum, Men sizga qanday yordam berishim mumkin?")


@bot.message_handler(commands=["holiday"])
def ask_country_code(message):
    """Dam olish kunlari uchun davlat kodini so'raydi."""
    prompt_message = "Dam olish kunlari uchun davlat kodini kiriting (masalan, UZ):"
    bot.send_message(message.chat.id, prompt_message)
    bot.register_next_step_handler(message, fetch_holidays)


def fetch_holidays(message):
    country_code = message.text.upper()
    year = 2024
    api_key = "nP5EjQWi9KDHNzVOySuULjOKLdgn6oWW"
    url = f"https://calendarific.com/api/v2/holidays?&api_key={api_key}&country={country_code}&year={year}"

    response = requests.get(url)

    if response.status_code == 200:
        holidays = response.json().get('response', {}).get('holidays', [])
        if holidays:
            holiday_message = "Dam olish kunlari:\n\n"
            for holiday in holidays:
                name = holiday['name']
                start_date = holiday['date']['iso']
                end_date = holiday['date'].get('end', start_date)  # Agar tugash sanasi ko'rsatilmagan bo'lsa, boshlanish sanasini ishlating

                # Kunlar sonini hisoblash
                start_date_obj = parse(start_date)
                end_date_obj = parse(end_date)
                duration = (end_date_obj - start_date_obj).days + 1

                holiday_message += f"{name} - {start_date[:10]} (Jami {duration} kun dam olish)\n"
            bot.send_message(message.chat.id, holiday_message)
        else:
            bot.send_message(message.chat.id, "Hech qanday dam olish kuni yo'q.")
    else:
        bot.send_message(message.chat.id, "Ma'lumotni olishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")

    # Yana bir davlat kodini so'rash
    ask_country_code(message)


if __name__ == "main":
    bot.polling(timeout=POLLING_TIMEOUT)