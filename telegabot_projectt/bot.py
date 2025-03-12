import logging
import os
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

# .env файлын жүктеу
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# /start командасы
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/chat", "/gdz", "/quiz", "/learn", "/referal"]
    keyboard.add(*buttons)
    await message.answer("Сәлем! Ботқа қош келдіңіз.\nТөмендегі командаларды пайдалана аласыз:", reply_markup=keyboard)

# /help командасы
@dp.message_handler(commands=["help"])
async def help_cmd(message: types.Message):
    help_text = (
        "/chat - Еркін чат (GPT немесе Gemini)\n"
        "/gdz - Үй тапсырмаларының шешімдері\n"
        "/quiz - Мұғалімдерге арналған викторина\n"
        "/learn - Курстар (ақылы/тегін)\n"
        "/referal - Реферал жүйесі (бонус алу)"
    )
    await message.answer(help_text)

# /chat - Еркін чат (Gemini)
@dp.message_handler(commands=["chat"])
async def chat_start(message: types.Message):
    await message.answer("Сәлем! Маған сұрағыңызды қойыңыз. 😊")

# Барлық басқа хабарламаларды өңдеу (чатты іске қосу)
@dp.message_handler()
async def chat_gemini(message: types.Message):
    try:
        response = model.generate_content(message.text)
        answer = response.candidates[0].content if response.candidates else "Кешіріңіз, жауап табылмады."
        await message.answer(answer)
    except Exception as e:
        await message.answer(f"Кешіріңіз, жауап алу кезінде қате кетті. 😞\nҚате: {str(e)}")

# /gdz командасы
@dp.message_handler(commands=["gdz"])
async def gdz_cmd(message: types.Message):
    await message.answer("ГДЗ жүйесі жақында іске қосылады!")

# /quiz командасы
@dp.message_handler(commands=["quiz"])
async def quiz_cmd(message: types.Message):
    await message.answer("Викторина жүйесі әзірлену үстінде!")

# /learn командасы
@dp.message_handler(commands=["learn"])
async def learn_cmd(message: types.Message):
    await message.answer("Курстар жүйесі жақында іске қосылады!")

# /referal командасы
@dp.message_handler(commands=["referal"])
async def referal_cmd(message: types.Message):
    await message.answer("Реферал жүйесі әзірлену үстінде!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
