import logging
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: CallbackContext):
    keyboard = [["📝 Контент-менеджер", "🎨 Дизайнер"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Командир, с чего начнём?", reply_markup=reply_markup)

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "🎨 Дизайнер":
        keyboard = [["🖼 Создать пост 4:5", "📱 Сторис для Instagram"],
                    ["🧷 Вставить текст", "🎨 Изменить фон"],
                    ["⬅️ Назад"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Выбери действие дизайнера:", reply_markup=reply_markup)
    elif text == "⬅️ Назад":
        keyboard = [["📝 Контент-менеджер", "🎨 Дизайнер"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Командир, с чего начнём?", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Скоро подключу интеллект и визуал, жаным. Это только начало 🎨")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()