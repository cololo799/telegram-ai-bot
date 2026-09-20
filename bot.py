import os
from google import genai
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text
        )

        await update.message.reply_text(response.text)

    except Exception as e:
        print(e)
        await update.message.reply_text("Произошла ошибка. Попробуй ещё раз.")


app = Application.builder().token(TELEGRAM_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
)

print("Бот запущен!")

app.run_polling()