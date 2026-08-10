import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

TOKEN = "8166656056:AAE6DU8y_ju-esPYQBLb40Qfc-yFJKoSeZw"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# جدول معرفات الملفات (File IDs)
FILE_IDS = {
    "book_pdf": "BQACAgIAAxkBAAN3anm0vFpU9DdtE7CIxsBTUZ8zur0AAtunAAIRI1hLNEyoGg-SS9o9BA",
    "lesson_1": "CQACAgIAAxkBAAN4anm0vM5PGE9F5IC2q3nPbezlbB0AAlyJAAK_UAFJXRrTfhF53Hs9BA",
    "lesson_2": "CQACAgIAAxkBAAN5anm0vI5Qw96xB6rZEY7IxAbeiyQAAoWDAALqfAhJ4b-1nX1sM9k9BA",
    "lesson_3": "CQACAgIAAxkBAAN6anm0vNBkh7Cbk_TKVZ7ZAAEQiYXYAAL0jwACxxwAAUn8oFvd64yUwz0E",
    "lesson_4": "CQACAgIAAxkBAAN7anm0vGQzyCaWUp6BIEFIplaS0KoAAot5AAL86RhJD2zNRmnzTIY9BA",
    "lesson_5": "CQACAgIAAxkBAAN8anm0vLSQH3MMZD7cUUQNRXeWk9AAAo55AAL86RhJ4Fn1CITVYN89BA",
    "lesson_6": "CQACAgIAAxkBAAN9anm0vDqRm_o9zlbBy7Rx0zCuWYUAAp2GAAI8thhJ5baDyiXpVoQ9BA",
    "lesson_7": "CQACAgIAAxkBAAN-anm0vKlvXq1Jow9oIK85YGMu_oQAAqODAAKPghlJwOuDPJyWu1A9BA",
    "lesson_8": "CQACAgIAAxkBAAN_anm0vJUAAcL5d4e_ECB4S26D2E8aAAJrigAC7b4gSXJGVXXg4bb2PQQ",
    "lesson_9": "CQACAgIAAxkBAAOAanm0vEA9BectWXIt4Td3Izn7s-EAAtOSAAJ3mhlJOwd4UarpnF49BA",
    "lesson_10": "CQACAgIAAxkBAAOBanm0vJeXskUNbWALShzfb6oIQBgAAniKAALtviBJgU8jGCJPPKU9BA",
    "lesson_11": "CQACAgIAAxkBAAOCanm0vEFsT4bf8vrbDSlCWCFmktIAApGMAALkuhlJtSVXw1px6uM9BA",
    "lesson_12": "CQACAgIAAxkBAAODanm0vITy-j79GCyX78EWDOmkwq0AAmuWAAI8thhJosFbfNrZUdQ9BA",
    "lesson_13": "CQACAgIAAxkBAAOEanm0vMA_zjY1YfyPjc4H_os-lAkAAnOWAAI8thhJ2uM43U0VIZs9BA",
    "lesson_14": "CQACAgIAAxkBAAOFanm0vMnlhpx970Da2394GUfBqBsAAqiMAALkuhlJ0sX_xeQhfYk9BA",
    "lesson_15": "CQACAgIAAxkBAAOGanm0vPI1fQM50BAZA3koYujKAU0AAg2OAAK9XxlJEjBNWsnLIPc9BA",
    "lesson_16": "CQACAgIAAxkBAAOHanm0vC1NjvhD3qdcgNQgkzPUncwAAouWAAI8thhJQqW7l4yW2eE9BA",
    "lesson_17": "CQACAgIAAxkBAAOIanm0vPFzhI2nmkF3SNivPZpqXTYAApqCAAJgsyFJrC_vy_TMBYw9BA",
    "lesson_18": "CQACAgIAAxkBAAOJanm0vMxrL5pVzJEIEusYkgRAcDQAAveSAAJ3mhlJ2jbIURWoG-89BA",
    "lesson_19": "CQACAgIAAxkBAAOKanm0vPwgh5A7-B81kZudW5wjURYAAi-OAAK9XxlJy0j2r0nO7dw9BA"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "أهلاً بكِ في مقرأة الشّاطبية 🌸\n"
        "اختاري الدرس الصوتي أو الكتاب المراد استعراضه:"
    )
    
    keyboard = []
    # إضافة زر الكتاب أولاً
    keyboard.append([InlineKeyboardButton("📖 كتاب فتح الأقفال", callback_data="book_pdf")])
    
    # إضافة أزرار الدروس من 1 إلى 19
    for i in range(1, 20):
        keyboard.append([InlineKeyboardButton(f"الدرس الصوتي {i}", callback_data=f"lesson_{i}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    chat_id = query.message.chat_id
    
    if data in FILE_IDS:
        file_id = FILE_IDS[data]
        if data == "book_pdf":
            await context.bot.send_document(chat_id=chat_id, document=file_id, caption="📖 تفضلي كتاب فتح الأقفال")
        else:
            lesson_num = data.split("_")[1]
            await context.bot.send_voice(chat_id=chat_id, voice=file_id, caption=f"🎧 التسجيل الصوتي للدرس {lesson_num}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("البوت يعمل الآن بكامل الميزات...")
    application.run_polling()
