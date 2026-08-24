import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from flask import Flask
from threading import Thread

TOKEN = "8166656056:AAE6DU8y_ju-esPYQBLb40Qfc-yFJKoSeZw"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# جدول معرفات الملفات الكامل للكتب الثلاثة، كتاب السيرة، وتسجيلات السيرة النبوية
FILE_IDS = {
    # كتاب السيرة النبوية (PDF)
    "seera_pdf": "BQACAgQAAxkBAAICPWqL0NqcoYoRkEhFXJrL9heiSQ1lAAJRHAACsxSxUg_Jxp4rTzjiPQQ",

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
    "b3_lesson_12": "CQACAgIAAxkBAAPzannDwW-8jd8IbotuOVYpsFzcmQ4AAjSQAAJpI9BKSiGa2-6lqN89BA",

    # 📜 دروس السيرة النبوية
    "seera_1": "CQACAgIAAxkBAAIBz2qLC47A2K4YS7_zf7vGBX97gl_fAAJmmwAC9ZrISqvv_uvafkIkPQQ",
    "seera_2": "CQACAgIAAxkBAAIB0GqLC44wpIYuN1BR809sHmY8Ia0eAAJbnQACcOv5SoXGax_RU-4SPQQ",
    "seera_3": "CQACAgIAAxkBAAIB0WqLC46F1iF60EqVzuleJwh60mDuAAL8nAACtNwAAUsxwId3kZx60j0E",
    "seera_4": "CQACAgIAAxkBAAIB0mqLC47S8Rx8_JhM17dUTOXDVCTLAAJpmQACsv0ZSxbk78bdwIU0PQQ",
    "seera_5": "CQACAgIAAxkBAAIB02qLC46U7HPuGXR3MpxEJ-ANooOiAAJ8oAAC-IdASwWfY7CPLkz3PQQ",
    "seera_6": "CQACAgIAAxkBAAIB1GqLC44DB5wW-6GlgrlwXxmcCRavAAJziAACX19RSyA7oAGUt00jPQQ",
    "seera_7": "CQACAgIAAxkBAAIB1WqLC45aV1DpBsqOaHL4S6PpmhEWAAKHowACrRZhSwUbzvSrB1NBPQQ",
    "seera_8": "CQACAgIAAxkBAAIB1mqLC441vToe15AqHAAB7CeOcDa-bwACnKUAAnkiiEtXCC_EI8DeDD0E",
    "seera_9": "CQACAgIAAxkBAAIB12qLC452bDqceO3RtFOour4xQ7ghAALpnQACxOaQS2be3-aZWbVwPQQ",
    "seera_10": "CQACAgIAAxkBAAIB2GqLC47Eywa5XG6KCgLgMEHxhxGrAAL3nwACSR6pS4L9QIFiW9wwPQQ",
    "seera_11": "CQACAgIAAxkBAAIB2WqLC44w8j6kVBlPbtQGHLs4IwYhAALxmQACFA_wSzEcYQVATzwnPQQ",
    "seera_12": "CQACAgIAAxkBAAIB2mqLC45XbmapQhC0zHvMgfZ2NikgAAIlqQACvcEhSHLLVEznXv3EPQQ",
    "seera_13": "CQACAgIAAxkBAAIB22qLC45FdbWKS2EBpFEEyrk2mdd3AAL8pgAC8dEpSMMahAtCfvqEPQQ",
    "seera_14": "CQACAgIAAxkBAAIB3GqLC45Al4z2dWYrwJlx1dKGoTT4AAKYmQAC_-VASD1a2-_sNaW-PQQ",
    "seera_15": "CQACAgIAAxkBAAIB3WqLC47miEi7gSPboM36rlkZAZb3AALVjwACMitpSPvLN6sOjmPZPQQ",
    "seera_16": "CQACAgIAAxkBAAIB3mqLC46N_DZNmMzlpY1fO4LGcrjWAALYowACguuJSCJdH_d1ilbZPQQ",
    "seera_17": "CQACAgIAAxkBAAIB32qLC45ZtB5_i-6_Kttc_IFPRu1mAAIgmwACLYsISWOyXQMV53KlPQQ",
    "seera_18": "CQACAgIAAxkBAAIB4GqLC46vjT6o_ApV8Kma6JVu8z0wAALUmgAC0zMgSRD1Unmgx_tiPQQ",
    "seera_19": "CQACAgIAAxkBAAIB4WqLC44RWgsRtSQngXNsVrgcCvBkAALlpAAC1kVBSeMqXLTg5PntPQQ",
    "seera_20": "CQACAgIAAxkBAAIB4mqLC47aatWb-L7Ws4ferX1jEFcJAALQnQACtG9RSYwFbpwELmTOPQQ",
    "seera_21": "CQACAgIAAxkBAAIB42qLC47WD5n4LOApPSeOdg0olDiMAALLngACh_ZpSciSUo5_v9m9PQQ",
    "seera_21_takmela": "CQACAgIAAxkBAAIB5GqLC442wt15UyH2fNFtFpNpd6YKAAIepQACqQlhSUdrq_n5xiF0PQQ",
    "seera_22": "CQACAgIAAxkBAAIB5WqLC47XQ0mrbJpODy3obyV7Db7WAAI8qgACJ-2QSVhODhRNTCNUPQQ",
    "seera_23": "CQACAgIAAxkBAAIB5mqLC473LaYDtjQZM46VaH7sMz2MAAJxnwACyAAB0EkhQri_H7q-rj0E",
    "seera_24": "CQACAgIAAxkBAAIB52qLC453VT69mZh-YkL-YDuk_EZqAAKOmwACf-D5SfhTk-Pr3Gz5PQQ",
    "seera_26": "CQACAgIAAxkBAAIB6GqLC47t7Rv_9KYC1jqlrBaGtvGQAAJTmgACs14hSmkQlSsXJGE9PQQ",
    "seera_27": "CQACAgIAAxkBAAICBWqLC7FUExxHkbsz4VVsp0X-BbI8AAINqwACLithSp6I6BSUf7kJPQQ",
    "seera_28": "CQACAgIAAxkBAAICB2qLC9lL1h0jRrPlxJY71Jl8-tfwAAL7oQACfqxwSusDl7S2gg9mPQQ",
    "seera_28_takmela": "CQACAgIAAxkBAAICCGqLC9mN8XQTUIJXxKrrSs9V1i3XAAKFoQAC48pxSvUDd7g4ONhMPQQ",
    "seera_29": "CQACAgIAAxkBAAICCWqLC9n3nxGokcxZRbvPE5latq9jAAJzngACYgG5SnTi3aHQrFCYPQQ",
    "seera_30": "CQACAgIAAxkBAAICCmqLC9kiFSQiGbJm5NmPjKzPrG_sAALtnwACnhTBSrCUgLBDJ74XPQQ",
    "seera_31": "CQACAgIAAxkBAAICC2qLC9mkG_r4pqeiBzfwbSOg6TYrAALToQACu_jRSsCr0BS5xlboPQQ",
    "seera_32": "CQACAgIAAxkBAAICDGqLC9kCgBy8Ral2p_X6WM0ejQn3AAJ-ogACXV_5Sic2etxjgSF-PQQ",
    "seera_33": "CQACAgIAAxkBAAICDWqLC9neY8IEM8CzIyBI_Xa_yyOOAAJgqQACnJcgS4cgiss2-kScPQQ",
    "seera_34": "CQACAgIAAxkBAAICDmqLC9l25lsIYTsjCFl6JQdAnZkdAAJWrgACR9dJS0VpxJRL4P0rPQQ",
    "seera_35": "CQACAgIAAxkBAAICD2qLC9mhP9dqMdJmGXuNXNkfiLyZAAL4pgAC59GRS-UZCy0QY6s7PQQ",
    "seera_36": "CQACAgIAAxkBAAICEGqLC9lyycBLdNJqmdo4RWGC37DgAAIwpgACDqygS_ytljvr2TF-PQQ",
    "seera_37": "CQACAgIAAxkBAAICEWqLC9nQNbg02N9jgIPWO0LIuca0AAJGpwACWGqxS8ETlXqivaluPQQ",
    "seera_37_takmela": "CQACAgIAAxkBAAIBymqK9oxl22JnKhJS1aVw-yLUUJM7AAINqgACo6GxS3NkffGVKUn9PQQ",
    "seera_38": "CQACAgIAAxkBAAICE2qLC9kgsI8Geyn3z4zasLtI-E10AAJUqgACbb7YS1dBbnAbJKrJPQQ",
    "seera_39": "CQACAgIAAxkBAAICFGqLC9noIyPRTcEssga3QoevyPWeAAJ5sQACuBjpS4Z8KUvzGNriPQQ",
    "seera_40": "CQACAgIAAxkBAAICFWqLC9k_jOyn2DtsY7TCPpEwbD17AAJnngACJ4f5S5XA1KBI-M-iPQQ"
}

# --- خادم الويب للإبقاء على البوت يعمل 24 ساعة ---
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

# 1. أمر البداية (يعرض أيقونتين رئيسيتين: تحفة الأطفال والسيرة النبوية)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📜 السيرة النبوية", callback_data="seera_menu")],
        [InlineKeyboardButton("📚 تحفة الأطفال", callback_data="tuhafa_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("أهلاً بكِ في مقرأة الشّاطبية 🌸\nيرجى اختيار القسم المطلوب من القائمة أدناه:", reply_markup=reply_markup)

# 2. معالج الأزرار والقوائم المتداخلة
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    chat_id = query.message.chat_id
    
    # --- القائمة الرئيسية للسيرة النبوية (تحتوي على خيارين: كتاب السيرة PDF والدروس الصوتية) ---
    if data == "seera_menu":
        keyboard = [
            [InlineKeyboardButton("📄 كتاب السيرة النبوية (PDF)", callback_data="seera_pdf")],
            [InlineKeyboardButton("🎧 الدروس الصوتية", callback_data="seera_audio_list")],
            [InlineKeyboardButton("⬅️ رجوع للقائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📜 **قسم السيرة النبوية:**\nاختر ما تحتاجه أدناه:", reply_markup=reply_markup, parse_mode="Markdown")

    # --- قائمة الدروس الصوتية للسيرة النبوية ---
    elif data == "seera_audio_list":
        keyboard = [
            [InlineKeyboardButton("🎧 الدرس 1", callback_data="seera_1")],
            [InlineKeyboardButton("🎧 الدرس 2", callback_data="seera_2")],
            [InlineKeyboardButton("🎧 الدرس 3", callback_data="seera_3")],
            [InlineKeyboardButton("🎧 الدرس 4", callback_data="seera_4")],
            [InlineKeyboardButton("🎧 الدرس 5", callback_data="seera_5")],
            [InlineKeyboardButton("🎧 الدرس 6", callback_data="seera_6")],
            [InlineKeyboardButton("🎧 الدرس 7", callback_data="seera_7")],
            [InlineKeyboardButton("🎧 الدرس 8", callback_data="seera_8")],
            [InlineKeyboardButton("🎧 الدرس 9", callback_data="seera_9")],
            [InlineKeyboardButton("🎧 الدرس 10", callback_data="seera_10")],
            [InlineKeyboardButton("🎧 الدرس 11", callback_data="seera_11")],
            [InlineKeyboardButton("🎧 الدرس 12", callback_data="seera_12")],
            [InlineKeyboardButton("🎧 الدرس 13", callback_data="seera_13")],
            [InlineKeyboardButton("🎧 الدرس 14", callback_data="seera_14")],
            [InlineKeyboardButton("🎧 الدرس 15", callback_data="seera_15")],
            [InlineKeyboardButton("🎧 الدرس 16", callback_data="seera_16")],
            [InlineKeyboardButton("🎧 الدرس 17", callback_data="seera_17")],
            [InlineKeyboardButton("🎧 الدرس 18", callback_data="seera_18")],
            [InlineKeyboardButton("🎧 الدرس 19", callback_data="seera_19")],
            [InlineKeyboardButton("🎧 الدرس 20", callback_data="seera_20")],
            [InlineKeyboardButton("🎧 الدرس 21", callback_data="seera_21"), InlineKeyboardButton("🎧 تكملة الدرس 21", callback_data="seera_21_takmela")],
            [InlineKeyboardButton("🎧 الدرس 22", callback_data="seera_22")],
            [InlineKeyboardButton("🎧 الدرس 23", callback_data="seera_23")],
            [InlineKeyboardButton("🎧 الدرس 24", callback_data="seera_24")],
            [InlineKeyboardButton("🎧 الدرس 26", callback_data="seera_26")],
            [InlineKeyboardButton("🎧 الدرس 27", callback_data="seera_27")],
            [InlineKeyboardButton("🎧 الدرس 28", callback_data="seera_28"), InlineKeyboardButton("🎧 تكملة الدرس 28", callback_data="seera_28_takmela")],
            [InlineKeyboardButton("🎧 الدرس 29", callback_data="seera_29")],
            [InlineKeyboardButton("🎧 الدرس 30", callback_data="seera_30")],
            [InlineKeyboardButton("🎧 الدرس 31", callback_data="seera_31")],
            [InlineKeyboardButton("🎧 الدرس 32", callback_data="seera_32")],
            [InlineKeyboardButton("🎧 الدرس 33", callback_data="seera_33")],
            [InlineKeyboardButton("🎧 الدرس 34", callback_data="seera_34")],
            [InlineKeyboardButton("🎧 الدرس 35", callback_data="seera_35")],
            [InlineKeyboardButton("🎧 الدرس 36", callback_data="seera_36")],
            [InlineKeyboardButton("🎧 الدرس 37", callback_data="seera_37"), InlineKeyboardButton("🎧 تكملة الدرس 37", callback_data="seera_37_takmela")],
            [InlineKeyboardButton("🎧 الدرس 38", callback_data="seera_38")],
            [InlineKeyboardButton("🎧 الدرس 39", callback_data="seera_39")],
            [InlineKeyboardButton("🎧 الدرس 40", callback_data="seera_40")],
            [InlineKeyboardButton("⬅️ رجوع لقائمة السيرة", callback_data="seera_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="🎧 **قائمة دروس السيرة النبوية الصوتية:**\nاختاري الدرس المطلوب للاستماع إليه:", reply_markup=reply_markup, parse_mode="Markdown")

    # --- القائمة الرئيسية العامة ---
    elif data == "main_menu":
        keyboard = [
            [InlineKeyboardButton("📜 السيرة النبوية", callback_data="seera_menu")],
            [InlineKeyboardButton("📚 تحفة الأطفال", callback_data="tuhafa_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="أهلاً بكِ مجدداً في مقرأة الشّاطبية 🌸\nيرجى اختيار القسم المطلوب من القائمة أدناه:", reply_markup=reply_markup)

    # --- قائمة تحفة الأطفال ---
    elif data == "tuhafa_menu":
        keyboard = [
            [InlineKeyboardButton("📖 فتح الأقفال", callback_data="book_1")],
            [InlineKeyboardButton("📖 منحة ذي الجلال", callback_data="book_2")],
            [InlineKeyboardButton("📖 فتح الملك المتعال", callback_data="book_3")],
            [InlineKeyboardButton("⬅️ رجوع للقائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="اختر الكتاب المطلوب من تحفة الأطفال:", reply_markup=reply_markup)
        
    # محتويات الكتاب الأول
    elif data == "book_1":
        keyboard = [[InlineKeyboardButton("📄 كتاب فتح الأقفال (PDF)", callback_data="book_1_pdf")]]
        for i in range(1, 20):
            keyboard.append([InlineKeyboardButton(f"🎧 التسجيل الصوتي {i}", callback_data=f"b1_lesson_{i}")])
        keyboard.append([InlineKeyboardButton("⬅️ رجوع للكتب", callback_data="tuhafa_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="محتويات كتاب فتح الأقفال:", reply_markup=reply_markup)

    # محتويات الكتاب الثاني
    elif data == "book_2":
        keyboard = [[InlineKeyboardButton("📄 كتاب منحة ذي الجلال (PDF)", callback_data="book_2_pdf")]]
        for i in range(1, 36):
            keyboard.append([InlineKeyboardButton(f"🎧 التسجيل الصوتي {i}", callback_data=f"b2_lesson_{i}")])
        keyboard.append([InlineKeyboardButton("⬅️ رجوع للكتب", callback_data="tuhafa_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="محتويات كتاب منحة ذي الجلال:", reply_markup=reply_markup)

    # محتويات الكتاب الثالث
    elif data == "book_3":
        keyboard = [[InlineKeyboardButton("📄 كتاب فتح الملك المتعال (PDF)", callback_data="book_3_pdf")]]
        for i in range(1, 13):
            keyboard.append([InlineKeyboardButton(f"🎧 التسجيل الصوتي {i}", callback_data=f"b3_lesson_{i}")])
        keyboard.append([InlineKeyboardButton("⬅️ رجوع للكتب", callback_data="tuhafa_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="محتويات كتاب فتح الملك المتعال:", reply_markup=reply_markup)
        
    # معالجة إرسال الملفات أو التسجيلات بناءً على مطابقتها لـ FILE_IDS
    elif data in FILE_IDS:
        file_id = FILE_IDS[data]
        
        # إذا كان ملف PDF (سواء كتاب السيرة أو كتب تحفة الأطفال)
        if "pdf" in data:
            if data == "seera_pdf":
                await context.bot.send_document(chat_id=chat_id, document=file_id, caption="📖 تفضلي كتاب السيرة النبوية (PDF)")
            else:
                book_names = {
                    "book_1_pdf": "كتاب فتح الأقفال",
                    "book_2_pdf": "كتاب منحة ذي الجلال",
                    "book_3_pdf": "كتاب فتح الملك المتعال"
                }
                await context.bot.send_document(chat_id=chat_id, document=file_id, caption=f"📖 تفضلي {book_names.get(data, 'الكتاب')}")
        
        # إذا كان من دروس السيرة النبوية (يبدأ بـ seera_)
        elif data.startswith("seera_"):
            if "takmela" in data:
                d_num = data.replace("seera_", "").replace("_takmela", "")
                caption_text = f"📜 السيرة النبوية - تكملة الدرس {d_num}"
            else:
                d_num = data.replace("seera_", "")
                caption_text = f"📜 السيرة النبوية - الدرس {d_num}"
            await context.bot.send_voice(chat_id=chat_id, voice=file_id, caption=caption_text)
        
        # إذا كان من دروس تحفة الأطفال (الكتب الثلاثة)
        else:
            parts = data.split("_")
            book_num = parts[0].replace("b", "")
            lesson_num = parts[2]
            await context.bot.send_voice(chat_id=chat_id, voice=file_id, caption=f"🎧 التسجيل الصوتي {lesson_num} (الكتاب {book_num})")

if __name__ == '__main__':
    keep_alive()
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("البوت يعمل الآن بالهيكل الجديد للسيرة النبوية وتحفة الأطفال على مدار 24 ساعة...")
    application.run_polling()
