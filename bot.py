import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

TOKEN = "8166656056:AAE6DU8y_ju-esPYQBLb40Qfc-yFJKoSeZw"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# جدول معرفات الملفات الكامل للكتب الثلاثة وتسجيلاتها
FILE_IDS = {
    # الكتاب الأول: فتح الأقفال
    "book_1_pdf": "BQACAgIAAxkBAAN3anm0vFpU9DdtE7CIxsBTUZ8zur0AAtunAAIRI1hLNEyoGg-SS9o9BA",
    "b1_lesson_1": "CQACAgIAAxkBAAN4anm0vM5PGE9F5IC2q3nPbezlbB0AAlyJAAK_UAFJXRrTfhF53Hs9BA",
    "b1_lesson_2": "CQACAgIAAxkBAAN5anm0vI5Qw96xB6rZEY7IxAbeiyQAAoWDAALqfAhJ4b-1nX1sM9k9BA",
    "b1_lesson_3": "CQACAgIAAxkBAAN6anm0vNBkh7Cbk_TKVZ7ZAAEQiYXYAAL0jwACxxwAAUn8oFvd64yUwz0E",
    "b1_lesson_4": "CQACAgIAAxkBAAN7anm0vGQzyCaWUp6BIEFIplaS0KoAAot5AAL86RhJD2zNRmnzTIY9BA",
    "b1_lesson_5": "CQACAgIAAxkBAAN8anm0vLSQH3MMZD7cUUQNRXeWk9AAAo55AAL86RhJ4Fn1CITVYN89BA",
    "b1_lesson_6": "CQACAgIAAxkBAAN9anm0vDqRm_o9zlbBy7Rx0zCuWYUAAp2GAAI8thhJ5baDyiXpVoQ9BA",
    "b1_lesson_7": "CQACAgIAAxkBAAN-anm0vKlvXq1Jow9oIK85YGMu_oQAAqODAAKPghlJwOuDPJyWu1A9BA",
    "b1_lesson_8": "CQACAgIAAxkBAAN_anm0vJUAAcL5d4e_ECB4S26D2E8aAAJrigAC7b4gSXJGVXXg4bb2PQQ",
    "b1_lesson_9": "CQACAgIAAxkBAAOAanm0vEA9BectWXIt4Td3Izn7s-EAAtOSAAJ3mhlJOwd4UarpnF49BA",
    "b1_lesson_10": "CQACAgIAAxkBAAOBanm0vJeXskUNbWALShzfb6oIQBgAAniKAALtviBJgU8jGCJPPKU9BA",
    "b1_lesson_11": "CQACAgIAAxkBAAOCanm0vEFsT4bf8vrbDSlCWCFmktIAApGMAALkuhlJtSVXw1px6uM9BA",
    "b1_lesson_12": "CQACAgIAAxkBAAODanm0vITy-j79GCyX78EWDOmkwq0AAmuWAAI8thhJosFbfNrZUdQ9BA",
    "b1_lesson_13": "CQACAgIAAxkBAAOEanm0vMA_zjY1YfyPjc4H_os-lAkAAnOWAAI8thhJ2uM43U0VIZs9BA",
    "b1_lesson_14": "CQACAgIAAxkBAAOFanm0vMnlhpx970Da2394GUfBqBsAAqiMAALkuhlJ0sX_xeQhfYk9BA",
    "b1_lesson_15": "CQACAgIAAxkBAAOGanm0vPI1fQM50BAZA3koYujKAU0AAg2OAAK9XxlJEjBNWsnLIPc9BA",
    "b1_lesson_16": "CQACAgIAAxkBAAOHanm0vC1NjvhD3qdcgNQgkzPUncwAAouWAAI8thhJQqW7l4yW2eE9BA",
    "b1_lesson_17": "CQACAgIAAxkBAAOIanm0vPFzhI2nmkF3SNivPZpqXTYAApqCAAJgsyFJrC_vy_TMBYw9BA",
    "b1_lesson_18": "CQACAgIAAxkBAAOJanm0vMxrL5pVzJEIEusYkgRAcDQAAveSAAJ3mhlJ2jbIURWoG-89BA",
    "b1_lesson_19": "CQACAgIAAxkBAAOKanm0vPwgh5A7-B81kZudW5wjURYAAi-OAAK9XxlJy0j2r0nO7dw9BA",

    # الكتاب الثاني: منحة ذي الجلال
    "book_2_pdf": "BQACAgQAAxkBAAPDannDwblPwsBVcYDWZENzrG5BIbcAAg4MAAJiF8lQEUOvW6-XrGk9BA",
    "b2_lesson_1": "CQACAgIAAxkBAAPEannDwQ6AAAFo8Yq6iJT7xhFK27-cAAIhkwACd5oZSQElzghzAAFJiz0E",
    "b2_lesson_2": "CQACAgIAAxkBAAPFannDwWVDwMZHylwW7fn7_j6JYGQAAgmNAALkuhlJH_t1wgNd8x09BA",
    "b2_lesson_3": "CQACAgIAAxkBAAPGannDwYGR0J-vJ-nQzSmspldH9ZEAAsWKAALtviBJDqcAAc9YvLHAPQQ",
    "b2_lesson_4": "CQACAgIAAxkBAAPHannDwXkU3XLNYtXWCqP3iGM_0TEAAsqCAAJgsyFJtrApH4zJlV89BA",
    "b2_lesson_5": "CQACAgIAAxkBAAPIannDwWYdy74GOcJ1hDQFAAHvR64eAALIigAC7b4gSXW2CbM7nBMuPQQ",
    "b2_lesson_6": "CQACAgIAAxkBAAPJannDwZxCS9xQrp658k2mD3fLsgYAAtiRAAKPghlJfEO1pU7Xz7g9BA",
    "b2_lesson_7": "CQACAgIAAxkBAAPKannDwWPUQi4z79UVU8ugTYJ0cW0AAtqRAAKPghlJ68QWkjv7qAY9BA",
    "b2_lesson_8": "CQACAgIAAxkBAAPLannDwVneVwR62Fyk2Ux_PGj8GPYAAjiHAAL86RhJZn9eBF-J6Vg9BA",
    "b2_lesson_9": "CQACAgIAAxkBAAPMannDwTQ5Yqru0w4s-F0JonOMtPQAAuiWAAI8thhJkg-xVvDlWdY9BA",
    "b2_lesson_10": "CQACAgIAAxkBAAPNannDweZl14dHo9qO2JYihbrha78AAg-JAAKJ9yFJcYtDUm6MrRw9BA",
    "b2_lesson_11": "CQACAgIAAxkBAAPOannDwauR57TWxNd8DBU5CnqaGEYAAtSKAALtviBJCdBoMUajIl89BA",
    "b2_lesson_12": "CQACAgIAAxkBAAPPannDwYaNTHGEzBI7aVohdsNVXRcAAhOKAAI0DBhJnzg3r47wNJQ9BA",
    "b2_lesson_13": "CQACAgIAAxkBAAPQannDwUIgWvPoxd6W967O3IjPugkAAkWTAAJ3mhlJMLtQ33KvkwU9BA",
    "b2_lesson_14": "CQACAgIAAxkBAAPRannDwRD224b_TdG3MSpsMODTOsMAAgmXAAI8thhJf-8QHkg56k89BA",
    "b2_lesson_15": "CQACAgIAAxkBAAPSannDwRXoQm4RGRzJ_-3Jg3dVtVwAAkuNAALkuhlJaANJIOGS1Ig9BA",
    "b2_lesson_16": "CQACAgIAAxkBAAPTannDwd9pjIyaZ7DeFWzyhXiRfz0AAguXAAI8thhJsKBrGBOkQn49BA",
    "b2_lesson_17": "CQACAgIAAxkBAAPUannDwXEP2WTP3GwQdiI2S4dC8RoAAvqRAAKPghlJVot9RzVIv949BA",
    "b2_lesson_18": "CQACAgIAAxkBAAPVannDwYl1tpf2whxFUR__MUnQL_kAAviOAAK9XxlJqlI7rQYAAUlhPQQ",
    "b2_lesson_19": "CQACAgIAAxkBAAPWannDwR1IUupPkkW53YvXUz3bGS8AAg6XAAI8thhJkJ62sO-fghE9BA",
    "b2_lesson_20": "CQACAgIAAxkBAAPXannDwat3npXdtvUIg-BnWFoPiXcAAv2RAAKPghlJG3CPGHgttFU9BA",
    "b2_lesson_21": "CQACAgIAAxkBAAPYannDwfEJvX_3f9_3_edZrakRTxgAAjaJAAKJ9yFJ4F2OxJnL7wo9BA",
    "b2_lesson_22": "CQACAgIAAxkBAAPZannDwUg_22xppqI3aLlSAUzJFToAAhCXAAI8thhJpilKuByK4c89BA",
    "b2_lesson_23": "CQACAgIAAxkBAAPaannDwYpboPR0YGSnIQ4wHlcUaBkAAgODAAJgsyFJYw5OccNGqmc9BA",
    "b2_lesson_24": "CQACAgIAAxkBAAPbannDwbwftCdWk8iMopnNDwIdzqEAAliHAAL86RhJRBfAiQ-aJ8I9BA",
    "b2_lesson_25": "CQACAgIAAxkBAAPcannDwY8ilUo1mmpySYcZB-iBW2gAAi-KAAI0DBhJrziVf39pYO49BA",
    "b2_lesson_26": "CQACAgIAAxkBAAPdannDweWMlI0bPboyQDxsL5KO8IEAAs-WAAKRJxhJoO5P3QY2IGU9BA",
    "b2_lesson_27": "CQACAgIAAxkBAAPeannDwWnxTNF--PLi6I9SPnxCCSwAAjyJAAKJ9yFJ8Uu7hBXgKhg9BA",
    "b2_lesson_28": "CQACAgIAAxkBAAPfannDwZzB9uMJI1GYEZ5QNhyXzAoAAlqHAAL86RhJAAEQ6Mb8Bd6IPQQ",
    "b2_lesson_29": "CQACAgIAAxkBAAPgannDwbCzH2HXUrG5ol78LNYUKwIAAgGSAAKPghlJFy-3rljd2a09BA",
    "b2_lesson_30": "CQACAgIAAxkBAAPhannDwTA9a6mVvDBx03c6PC2ziJ4AAsyKAALiHSBJuWAdH2hOuTQ9BA",
    "b2_lesson_31": "CQACAgIAAxkBAAPiannDwWa-JNfAOeb1aqnRb0JgU1MAAgSPAAK9XxlJI7ARnKZGLVg9BA",
    "b2_lesson_32": "CQACAgIAAxkBAAPjannDwXWhdF0Q7Pn5bCQZ0yd6plgAAs-KAALiHSBJJ9SeDvXkL9U9BA",
    "b2_lesson_33": "CQACAgIAAxkBAAPkannDwd7-XGZl0bqGO-E228xjaRMAAvKKAALtviBJWg31cI0YMEo9BA",
    "b2_lesson_34": "CQACAgIAAxkBAAPlannDwSKouFCDrE5okuS2dtg7HxUAAl-HAAL86RhJinbzszkrQ5E9BA",
    "b2_lesson_35": "CQACAgIAAxkBAAPmannDwVNEmopHtyEWbCEQ2cJbcZgAAgqPAAK9XxlJvB4KnaNA_1w9BA",

    # الكتاب الثالث: فتح الملك المتعال
    "book_3_pdf": "BQACAgQAAxkBAAPnannDwZlQWUF3E72SbR_61ZyL_swAAgsMAAJiF8lQFFfBSJad3YA9BA",
    "b3_lesson_1": "CQACAgIAAxkBAAPoannDwRAJjWRRiiGgpZS2_Z9rNWoAAuOiAAIJjNFKgaxLoE9IxUo9BA",
    "b3_lesson_2": "CQACAgIAAxkBAAPpannDwSoghP4sT83x35ADSGd1AsIAAkapAAIJjNFKR4byK7kihng9BA",
    "b3_lesson_3": "CQACAgIAAxkBAAPqannDwcbn-nHHnM5wY89qDwmqbe4AAs6RAAKPgNFKCZPPxDNWTPk9BA",
    "b3_lesson_4": "CQACAgIAAxkBAAPrannDwfzd71yzUd-wob--CHuz-b8AAgieAAKMbdlKEQbXIKqNEBw9BA",
    "b3_lesson_5": "CQACAgIAAxkBAAPsannDwUDDAUnJMcPXQ7gI4QABBFpSAAIukAACYqXQSvoO_oBHGcenPQQ",
    "b3_lesson_6": "CQACAgIAAxkBAAPtannDwXAr-QL0WervIg5JRFeUtzgAAtuSAAIJjNlK5V3nOgNL4Cw9BA",
    "b3_lesson_7": "CQACAgIAAxkBAAPuannDwWP3RjgS3XVa1jiqw7QqslsAAqKYAAIn59BKfwHnpgyzS0c9BA",
    "b3_lesson_8": "CQACAgIAAxkBAAPvannDwVMU28oGF0c3sgJegRT1xrsAAjGeAAKMbdlKdrMtSXNiH-E9BA",
    "b3_lesson_9": "CQACAgIAAxkBAAPwannDwVsMxPxjXy4YTF6nBYN_4BUAAumSAAIJjNlKGzk2KUqS6og9BA",
    "b3_lesson_10": "CQACAgIAAxkBAAPxannDwaDFMkDp6isVklxnB7HUnL8AAq6YAAIn59BKHHY_4Rm1F7A9BA",
    "b3_lesson_11": "CQACAgIAAxkBAAPyannDwae9DiMNc72JC-j8wEv8tHgAAr-YAAIn59BK5uxb3dNSWWM9BA",
    "b3_lesson_12": "CQACAgIAAxkBAAPzannDwW-8jd8IbotuOVYpsFzcmQ4AAjSQAAJpI9BKSiGa2-6lqN89BA"
}

# 1. أمر البداية (يعرض زر تحفة الأطفال)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📚 تحفة الأطفال", callback_data="tuhafa_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("أهلاً بكِ يا رحمة في مقرأة الشّاطبية 🌸\nاضغطي على الزر أدناه للبدء:", reply_markup=reply_markup)

# 2. معالج الأزرار والقوائم المتداخلة
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    chat_id = query.message.chat_id
    
    # القائمة الرئيسية لمتن تحفة الأطفال (الكتب الثلاثة)
    if data == "tuhafa_menu":
        keyboard = [
            [InlineKeyboardButton("📖 فتح الأقفال", callback_data="book_1")],
            [InlineKeyboardButton("📖 منحة ذي الجلال", callback_data="book_2")],
            [InlineKeyboardButton("📖 فتح الملك المتعال", callback_data="book_3")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="اختر الكتاب المطلوب من تحفة الأطفال:", reply_markup=reply_markup)
        
    # محتويات الكتاب الأول: فتح الأقفال (19 درس)
    elif data == "book_1":
        keyboard = [[InlineKeyboardButton("📄 كتاب فتح الأقفال (PDF)", callback_data="book_1_pdf")]]
        for i in range(1, 20):
            keyboard.append([InlineKeyboardButton(f"🎧 التسجيل الصوتي {i}", callback_data=f"b1_lesson_{i}")])
        keyboard.append([InlineKeyboardButton("⬅️ رجوع للكتب", callback_data="tuhafa_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="محتويات كتاب فتح الأقفال:", reply_markup=reply_markup)

    # محتويات الكتاب الثاني: منحة ذي الجلال (35 درس)
    elif data == "book_2":
        keyboard = [[InlineKeyboardButton("📄 كتاب منحة ذي الجلال (PDF)", callback_data="book_2_pdf")]]
        for i in range(1, 36):
            keyboard.append([InlineKeyboardButton(f"🎧 التسجيل الصوتي {i}", callback_data=f"b2_lesson_{i}")])
        keyboard.append([InlineKeyboardButton("⬅️ رجوع للكتب", callback_data="tuhafa_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="محتويات كتاب منحة ذي الجلال:", reply_markup=reply_markup)

    # محتويات الكتاب الثالث: فتح الملك المتعال (12 درس)
    elif data == "book_3":
        keyboard = [[InlineKeyboardButton("📄 كتاب فتح الملك المتعال (PDF)", callback_data="book_3_pdf")]]
        for i in range(1, 13):
            keyboard.append([InlineKeyboardButton(f"🎧 التسجيل الصوتي {i}", callback_data=f"b3_lesson_{i}")])
        keyboard.append([InlineKeyboardButton("⬅️ رجوع للكتب", callback_data="tuhafa_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="محتويات كتاب فتح الملك المتعال:", reply_markup=reply_markup)
        
    # إرسال الملفات أو التسجيلات الصوتية مباشرة داخل المحادثة
    elif data in FILE_IDS:
        file_id = FILE_IDS[data]
        if "pdf" in data:
            book_names = {
                "book_1_pdf": "كتاب فتح الأقفال",
                "book_2_pdf": "كتاب منحة ذي الجلال",
                "book_3_pdf": "كتاب فتح الملك المتعال"
            }
            await context.bot.send_document(chat_id=chat_id, document=file_id, caption=f"📖 تفضلي {book_names[data]}")
        else:
            parts = data.split("_")
            book_num = parts[0].replace("b", "")
            lesson_num = parts[2]
            await context.bot.send_voice(chat_id=chat_id, voice=file_id, caption=f"🎧 التسجيل الصوتي {lesson_num} (الكتاب {book_num})")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("البوت يعمل الآن بكامل قوائم تحفة الأطفال...")
    application.run_polling()
