import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from flask import Flask
from threading import Thread

TOKEN = "8166656056:AAE6DU8y_ju-esPYQBLb40Qfc-yFJKoSeZw"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- خادم الويب الوهمي لإبقاء البوت شغالاً ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_web)
    t.start()
# ---------------------------------------------

# دالة أمر البدء /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بكِ يا رحمة 🌸\n\n"
        "تم استلام أمر البدء بنجاح!\n"
        "الآن أرسلي أو حولي لي أي تسجيل صوتي أو ملف، وسأرسل لكِ المعرف الخاص به فوراً."
    )

# دالة استقبال الملفات وإرجاع المعرف
async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    file_id = None
    file_type = ""

    if message.voice:
        file_id = message.voice.file_id
        file_type = "تسجيل صوتي (Voice)"
    elif message.audio:
        file_id = message.audio.file_id
        file_type = "ملف صوتي (Audio)"
    elif message.document:
        file_id = message.document.file_id
        file_type = "ملف/مستند (Document)"

    if file_id:
        await message.reply_text(f"📂 **نوع الملف:** {file_type}\n\n🔹 **المعرف (انسخيه):**\n`{file_id}`", parse_mode="Markdown")
    else:
        await message.reply_text("عذراً، لم أتعرف على الملف. أرسليه كـ تسجيل صوتي أو ملف.")

def main():
    # بناء التطبيق بالطريقة الصحيحة للنسخ الحديثة
    application = ApplicationBuilder().token(TOKEN).build()

    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, get_file_id))

    print("البوت يعمل الآن ومستعد لاستقبال الأوامر والتسجيلات...")
    application.run_polling()

if __name__ == '__main__':
    keep_alive()
    main()
