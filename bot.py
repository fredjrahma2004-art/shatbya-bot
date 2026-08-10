from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

# توكن البوت الخاص بكِ
TOKEN = "8166656056:AAE6DU8y_ju-esPYQBLb40Qfc-yFJKoSeZw"



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  # إنشاء الأزرار لكل الدروس والكتاب
  keyboard = [
      [
          InlineKeyboardButton(
              "📚 (ملف) كتاب تحفة الأطفال", callback_data="send_book"
          )
      ],
      [InlineKeyboardButton("🎧 الدرس 1", callback_data="lesson_1")],
      [InlineKeyboardButton("🎧 الدرس 2", callback_data="lesson_2")],
      [InlineKeyboardButton("🎧 الدرس 3", callback_data="lesson_3")],
      [InlineKeyboardButton("🎧 الدرس 4", callback_data="lesson_4")],
      [InlineKeyboardButton("🎧 الدرس 5", callback_data="lesson_5")],
      [InlineKeyboardButton("🎧 الدرس 6", callback_data="lesson_6")],
      [InlineKeyboardButton("🎧 الدرس 7", callback_data="lesson_7")],
      [InlineKeyboardButton("🎧 الدرس 8", callback_data="lesson_8")],
      [InlineKeyboardButton("🎧 الدرس 9", callback_data="lesson_9")],
      [InlineKeyboardButton("🎧 الدرس 10", callback_data="lesson_10")],
      [InlineKeyboardButton("🎧 الدرس 11", callback_data="lesson_11")],
      [InlineKeyboardButton("🎧 الدرس 12", callback_data="lesson_12")],
      [InlineKeyboardButton("🎧 الدرس 13", callback_data="lesson_13")],
      [InlineKeyboardButton("🎧 الدرس 14", callback_data="lesson_14")],
      [InlineKeyboardButton("🎧 الدرس 15", callback_data="lesson_15")],
      [InlineKeyboardButton("🎧 الدرس 16", callback_data="lesson_16")],
      [InlineKeyboardButton("🎧 الدرس 17", callback_data="lesson_17")],
      [InlineKeyboardButton("🎧 الدرس 18", callback_data="lesson_18")],
      [InlineKeyboardButton("🎧 الدرس 19 / الخاتمة", callback_data="lesson_19")],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)
  await update.message.reply_text(
      "أهلاً بكِ في مقرأة الشّاطبية 🌸\nاخترِ الدرس الصوتي أو الكتاب المراد استعراضه:",
      reply_markup=reply_markup,
  )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  data = query.data

  # إذا طلبت الطالبة الكتاب
  if data == "send_book":
    await query.message.reply_text(
        "هذا هو رابط أو ملف كتاب تحفة الأطفال (يمكننا ربطه بملفه الخاص قريباً)."
    )

  # إذا طلبت أي درس من الدروس الـ 19
  elif data.startswith("lesson_"):
    lesson_num = data.split("_")[1]
    await query.message.reply_text(
        f"أهلاً بكِ. جاري إرسال التسجيل الصوتي لـ [ الدرس رقم {lesson_num} ] 🎧"
    )
    # ملاحظة: يمكنكِ لاحقاً وضع رابط الملف الصوتي المباشر أو الـ File ID هنا لكل درس بسهولة تامة.


def main():
  application = Application.builder().token(TOKEN).build()

  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button_handler))

  application.run_polling()


if __name__ == "__main__":
  main()
