import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = "8166656056:AAE6DU8y_ju-esPYQBLb40Qfc-yFJKoSeZw"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً يا رحما! الآن أرسلي لي ملف الـ PDF والتسجيلات الصوتية هنا في المحادثة لكي أستخرج لكِ معرفاتها فوراً.")

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.document:
        file_id = update.message.document.file_id
        await update.message.reply_text(f"هذا هو معرف الـ PDF:\n`{file_id}`", parse_mode="Markdown")
    elif update.message.audio:
        file_id = update.message.audio.file_id
        await update.message.reply_text(f"هذا هو معرف التسجيل الصوتي:\n`{file_id}`", parse_mode="Markdown")
    elif update.message.voice:
        file_id = update.message.voice.file_id
        await update.message.reply_text.reply_text(f"هذا هو معرف التسجيل الصوتي (Voice):\n`{file_id}`", parse_mode="Markdown")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Document.ALL | filters.AUDIO | filters.VOICE, get_file_id))
    application.run_polling()
