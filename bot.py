import os
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

# 1. عند الضغط على أمر البدء /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بكِ يا رحمة 🌸\n\n"
        "حسناً، تم تفعيل وضع استخراج المعرفات.\n"
        "الآن، قومي بإرسال أو تحويل تسجيلات الدروس (أو الملفات) إلى هنا، وسأرسل لكِ معرف كل تسجيل (`file_id`) فوراً لتقومي بنسخه!"
    )

# 2. استقبال التسجيلات والملفات وإرسال المعرفات الخاصة بها
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
        # الرد في المحادثة مباشرة بنص الـ file_id لسهولة النسخ
        response_text = (
            f"✅ **تم استخراج المعرف بنجاح!**\n"
            f"📂 النوع: {file_type}\n\n"
            f"🔹 انسخي هذا المعرف:\n"
            f"`{file_id}`"
        )
        await message.reply_text(response_text, parse_mode="Markdown")
    else:
        await message.reply_text("عذراً، لم أتمكن من قراءة هذا الملف. تأكدي من إرساله كـ تسجيل صوتي أو ملف.")

if __name__ == '__main__':
    keep_alive()
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # معالج أمر /start
    application.add_handler(CommandHandler('start', start))
    
    # معالج استقبال التسجيلات والملفات
    application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.DOCUMENT | filters.VIDEO, get_file_id))
    
    print("البوت جاهز ويستقبل التسجيلات الآن...")
    application.run_polling()
