import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from flask import Flask
from threading import Thread

TOKEN = "8166656056:AAE6DU8y_ju-esPYQBLb40Qfc-yFJKoSeZw"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- كود إبقاء البوت شغالاً 24 ساعة (خادم ويب وهمي) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running 24/7!"

def run_web():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_web)
    t.start()
# --------------------------------------------------

# 1. أمر البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بكِ يا رحمة 🌸\n"
        "هذا وضع استخراج المعرفات.\n"
        "قومي بإرسال أو تحويل أي تسجيل صوتي أو ملف PDF إلى هنا، وسأعطيكِ الـ (file_id) الخاص به فوراً!"
    )

# 2. وظيفة التقاط المعرفات تلقائياً عند إرسال الملفات
async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    file_id = None
    file_type = ""

    # التحقق من نوع الملف المرسل
    if message.voice:
        file_id = message.voice.file_id
        file_type = "تسجيل صوتي (Voice)"
    elif message.audio:
        file_id = message.audio.file_id
        file_type = "ملف صوتي (Audio)"
    elif message.document:
        file_id = message.document.file_id
        file_type = "مستند/ملف PDF (Document)"
    elif message.video:
        file_id = message.video.file_id
        file_type = "فيديو (Video)"

    if file_id:
        # طباعة المعرف في الكونسول للتأكد
        print(f"\n--- تم استخراج معرف جديد ({file_type}) ---")
        print(file_id)
        print("-----------------------------------------\n")
        
        # الرد في المحادثة مباشرة لسهولة النسخ
        response_text = (
            f"✅ تم التعرف على الملف بنجاح!\n"
            f"📂 النوع: {file_type}\n\n"
            f"🔹 معرف الملف (انسخي ما بين القوسين):\n"
            f"`{file_id}`"
        )
        await message.reply_text(response_text, parse_mode="Markdown")
    else:
        await message.reply_text("عذراً، لم أتمكن من العثور على معرف لهذا الملف. تأكدي من إرساله كملف صوتي أو مستند.")

if __name__ == '__main__':
    keep_alive()
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # أوامر البوت
    application.add_handler(CommandHandler('start', start))
    
    # هذا المعالج يلتقط أي ملف يتم إرساله للبوت (صوت، مستند، إلخ)
    application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.DOCUMENT | filters.VIDEO, get_file_id))
    
    print("البوت يعمل الآن في وضع استخراج المعرفات...")
    application.run_polling()
