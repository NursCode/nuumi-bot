import logging
import os
import openai
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)

user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📝 Контент-менеджер", "🎨 Дизайнер"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Командир, с чего начнём?", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "🎨 Дизайнер":
        keyboard = [["🖼 Создать пост 4:5", "📱 Сторис для Instagram"],
                    ["🧷 Вставить текст", "🎨 Изменить фон"],
                    ["⬅️ Назад"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Выбери действие дизайнера:", reply_markup=reply_markup)

    elif text == "🖼 Создать пост 4:5":
        user_states[user_id] = "awaiting_prompt"
        await update.message.reply_text("Что должно быть на изображении? Опиши коротко.")

    elif text == "⬅️ Назад":
        keyboard = [["📝 Контент-менеджер", "🎨 Дизайнер"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Командир, с чего начнём?", reply_markup=reply_markup)

    elif user_states.get(user_id) == "awaiting_prompt":
        prompt = text
        await update.message.reply_text("Генерирую изображение... 🎨")

        try:
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            image_url = response.data[0].url
            await update.message.reply_photo(photo=image_url, caption="Готово, Командир ✅")
        except Exception as e:
            await update.message.reply_text(f"Ошибка генерации: {e}")

        user_states.pop(user_id, None)

    else:
        await update.message.reply_text("Скоро подключу интеллект и визуал, жаным. Это только начало 🎨")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()