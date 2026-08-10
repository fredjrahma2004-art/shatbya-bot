import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

TOKEN = "8166656056:AAE8xNDpBCjUJ3D1II0twNyV7goQiyYKOIo"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "📚 كتاب تحفة الأطفال (ملف PDF)",
                callback_data="send_pdf_book",
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = "مرحباً بكِ أيتها الطالبة الكريمة في بوت مقرأة الشّاطبية.\n\nاختارِي ما تحتاجينه من القائمة أدناه:"

    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "send_pdf_book":
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="📖 إليك كتاب تحفة الأطفال بصيغة ملف:"
        )
        
        # ضعي رابط ملف الـ PDF المباشر الخاص بكِ هنا بين علامتي التنصيص
        pdf_url = "https://t.me/booktajweedqiraat/1536"
        
        keyboard = [[InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="back_to_start")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_document(
            chat_id=query.message.chat_id,
            document=pdf_url,
            caption="📚 كتاب تحفة الأطفال في علم التجويد",
            reply_markup=reply_markup
        )
        
    elif query.data == "back_to_start":
        keyboard = [
            [
                InlineKeyboardButton(
                    "📚 كتاب تحفة الأطفال (ملف PDF)",
                    callback_data="send_pdf_book",
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = "مرحباً بكِ أيتها الطالبة الكريمة في بوت مقرأة الشّاطبية.\n\nاختارِي ما تحتاجينه من القائمة أدناه:"
        
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=welcome_text,
            reply_markup=reply_markup
        )

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("بوت مقرأة الشاطبية يعمل الآن...")
    application.run_polling()

if __name__ == "__main__":
    main()
