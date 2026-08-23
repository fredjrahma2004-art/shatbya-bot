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

# جدول معرفات الملفات الكامل للكتب الثلاثة وتسجيلات السيرة النبوية
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
    "b3_lesson_12": "CQACAgIAAxkBAAPzannDwW-8jd8IbotuOVYpsFzcmQ4AAjSQAAJpI9BKSiGa2-6lqN89BA",

    # 📜 دروس وسيرة النبوية (40 درساً مع التكملات)
    "seera_1": "CQACAgIAAxkBAAEh59Rqir0Bmnu3G6qcX_iF9Pb3Uu9uywACZpsAAvWayEoWTHbTvtE3Vj0E",
    "seera_2": "CQACAgIAAxkBAAEh59Vqir0BwGd8g2kmc7X6PUoB-aWjqAACW50AAnDr-UrC0n6JOf3uRj0E",
    "seera_3": "CQACAgIAAxkBAAEh59Zqir0BLe4JOdmmWTWvlrSrjSvXhQAC_JwAArTcAAFLg3vh_NJyuQo9BA",
    "seera_4": "CQACAgIAAxkBAAEh59dqir0BngJAB5ADwZMR21e-cU3xhQACaZkAArL9GUvRykMp01zJ0D0E",
    "seera_5": "CQACAgIAAxkBAAEh59hqir0Bisa2976fURtfQ9TDObS6TAACfKAAAviHQEsMPqfeEcfTqz0E",
    "seera_6": "CQACAgIAAxkBAAEh59lqir0B4mEigG3ayhIN1qBnHwOsBQACc4gAAl9fUUs7-mouCbm60D0E",
    "seera_7": "CQACAgIAAxkBAAEh59pqir0BDDkal48VlVqkYHn1KWTy6wACh6MAAq0WYUv2ScPYim1okT0E",
    "seera_8": "CQACAgIAAxkBAAEh59tqir0BiWmlMyVYsqdsxT0RzsyWYAACnKUAAnkiiEuho3wHvPAAARU9BA",
    "seera_9": "CQACAgIAAxkBAAEh59xqir0BcVHkZioBzQaLiG76_pYWKwAC6Z0AAsTmkEuq0NjDhIIm8T0E",
    "seera_10": "CQACAgIAAxkBAAEh591qir0Be6-Gvs5_hU1_6HEjA00ScwAC958AAkkeqUs78aQgwL4eSj0E",
    "seera_11": "CQACAgIAAxkBAAEh595qir0BhPBJZ685kLyJejtc6atDOQAC8ZkAAhQP8EuRf4Q2mWASvD0E",
    "seera_12": "CQACAgIAAxkBAAEh599qir0B8ih0tv0zYtZHpeIXVNO3sgACJakAAr3BIUhhX9FPhoQTYT0E",
    "seera_13": "CQACAgIAAxkBAAEh5-Bqir0BHxlR7h9kNTKaY9hUrBEtygAC_KYAAvHRKUjFc9pHrKZ4kD0E",
    "seera_14": "CQACAgIAAxkBAAEh5-Fqir0BHq7rpf2diBxoOICkk-C21wACmJkAAv_lQEjH174MEqodrT0E",
    "seera_15": "CQACAgIAAxkBAAEh5-Jqir0BJTMD-7b-oh_msGd5jGfFxgAC1Y8AAjIraUhg3TpYlDXhcT0E",
    "seera_16": "CQACAgIAAxkBAAEh5-Nqir0Bb4KhxEA0PrFTX8IsqtnFAAPYowACguuJSAQ9gI-Uj3HpPQQ",
    "seera_17": "CQACAgIAAxkBAAEh5-Rqir0B4EA3N9yvCBwxloiaZFYO8wACIJsAAi2LCEnPD460nc-Yiz0E",
    "seera_18": "CQACAgIAAxkBAAEh5-Vqir0Brj860YLrVbsUNK_STzCRHwAC1JoAAtMzIEliWjASBzq2az0E",
    "seera_19": "CQACAgIAAxkBAAEh5-Zqir0Bnj2IXGsOodzxeiaBSRUFygAC5aQAAtZFQUmEdTUbV5pZfz0E",
    "seera_20": "CQACAgIAAxkBAAEh5-dqir0BtL-1ZBWbqEiM4seZj3m1KgAC0J0AArRvUUnOuih7cH0VPj0E",
    "seera_21": "CQACAgIAAxkBAAEh5-hqir0BK2pHoLMu3-T12TYkRJ5nlwACy54AAof2aUkvHAyPbUS_rD0E",
    "seera_21_takmela": "CQACAgIAAxkBAAEh5-lqir0BHjMNWa5P8SjkpNcUbyr-pAACHqUAAqkJYUm4mJHsmDTdPD0E",
    "seera_22": "CQACAgIAAxkBAAEh5-pqir0BYJU8enXd_GlkirBVw6rtwgACPKoAAiftkElZGfjRhlTRCj0E",
    "seera_23": "CQACAgIAAxkBAAEh5-tqir0BzoyjWqvlvpWR9qFcW6tLAANxnwACyAAB0Elk2DQ6_oiUjj0E",
    "seera_24": "CQACAgIAAxkBAAEh5-xqir0Bf-2wAAE9oeClwgIo-En6EtAAAo6bAAJ_4PlJk-pMV6QNPUI9BA",
    "seera_25": "CQACAgIAAxkBAAEh5-1qir0Bric5o3waCb9wQAbBgiA_hwACU5oAArNeIUocBE5L4pbRgj0E",
    "seera_26": "CQACAgIAAxkBAAEh5-5qir0BNXGZBJAcvGET51of51OBwwAC25wAAs-EQEqzXQteWvClFj0E",
    "seera_27": "CQACAgIAAxkBAAEh6eZqiu2VRzEAAdbiZAi4F9Af-gRfqeIAAg2rAAIuK2FKysZAQqr-dSI9BA",
    "seera_28": "CQACAgIAAxkBAAEh5-9qir0BCnMWlUHWG0ZOmMRPGajBWQAC-6EAAn6scEpHfzRuvDJ43D0E",
    "seera_28_takmela": "CQACAgIAAxkBAAEh5_Bqir0BAAE-bZUPo1-FUAAB1A96bYxBAAKFoQAC48pxSl7juT31KqbcPQQ",
    "seera_29": "CQACAgIAAxkBAAEh5_Fqir0BySuUy0xcg5cXqZmwRId_iwACc54AAmIBuUq60vzpV3EMbz0E",
    "seera_30": "CQACAgIAAxkBAAEh5_Jqir0B633tWwrVM-HmIzmJXIMZUgAC7Z8AAp4UwUoodPbShIxRPj0E",
    "seera_31": "CQACAgIAAxkBAAEh5_Nqir0BXyU-XTml-j5WoXWXxbZEIgAC06EAArv40Upl0oQI3HxNOT0E",
    "seera_32": "CQACAgIAAxkBAAEh5_Rqir0BZNUt9vAf6luntl1Dsj2D5gACfqIAAl1f-UobL3x_KbjRgD0E",
    "seera_33": "CQACAgIAAxkBAAEh5_Vqir0BRIAiwt3MZl4l-AS5y47UYAACYKkAApyXIEtLsDKWsQLtvj0E",
    "seera_34": "CQACAgIAAxkBAAEh5_Zqir0BzaVRaNBc3lxvNZTRQHnIwAACVq4AAkfXSUvJ70xs9l9C8j0E",
    "seera_35": "CQACAgIAAxkBAAEh5_dqir0BVasZdQOHozGkhyqN5DKBUQAC-KYAAufRkUuCUUD-Ak-otj0E",
    "seera_36": "CQACAgIAAxkBAAEh5_hqir0BIDFU3pvtEbPJsZzYQ6emvgACMKYAAg6soEtMt0Ig-5cJUT0E",
    "seera_37": "CQACAgIAAxkBAAEh5_lqir0BBcq4NGmdWHq_OwIbs4X6PAACRqcAAlhqsUuOO6ahS47Lwz0E",
    "seera_37_takmela": "CQACAgIAAxkBAAEh5_pqir0BsSQLFVdA3GyWZODgTuTURQACDaoAAqOhsUv6kXPV78O2QD0E",
    "seera_38": "CQACAgIAAxkBAAEh6HZqir2Yxd2wkGftGP4JRKLf-SPosgACVKoAAm2-2EuDo6jXpZfxoj0E",
    "seera_39": "CQACAgIAAxkBAAEh6Hdqir2YHrwm0w4YoGSSIa5d8dsUPgACebEAArgY6UuVRF9MdzbOkT0E",
    "seera_40": "CQACAgIAAxkBAAEh6Hhqir2Y5NENYESWU6i-pB7IvezVLQACZ54AAieH-UsAAaumGMg1huQ9BA"
}

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

# 1. أمر البداية (القائمة الرئيسية: السيرة النبوية + تحفة الأطفال)
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
    
    # --- قسم السيرة النبوية (40 درساً مع التكملات) ---
    if data == "seera_menu":
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
            [InlineKeyboardButton("🎧 الدرس 25", callback_data="seera_25")],
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
            [InlineKeyboardButton("⬅️ رجوع للقائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📚 **قائمة دروس السيرة النبوية:**\nاختاري الدرس المطلوب للاستماع إليه:", reply_markup=reply_markup, parse_mode="Markdown")

    # --- القائمة الرئيسية العامة ---
    elif data == "main_menu":
        keyboard = [
            [InlineKeyboardButton("📜 السيرة النبوية", callback_data="seera_menu")],
            [InlineKeyboardButton("📚 تحفة الأطفال", callback_data="tuhafa_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="أهلاً بكِ مجدداً في مقرأة الشّاطبية 🌸\nيرجى اختيار القسم المطلوب من القائمة أدناه:", reply_markup=reply_markup)

    # --- القائمة الرئيسية لمتن تحفة الأطفال (الكتب الثلاثة) ---
    elif data == "tuhafa_menu":
        keyboard = [
            [InlineKeyboardButton("📖 فتح الأقفال", callback_data="book_1")],
            [InlineKeyboardButton("📖 منحة ذي الجلال", callback_data="book_2")],
            [InlineKeyboardButton("📖 فتح الملك المتعال", callback_data="book_3")],
            [InlineKeyboardButton("⬅️ رجوع للقائمة الرئيسية", callback_data="main_menu")]
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
        elif data.startswith("seera_"):
            if "takmela" in data:
                d_num = data.replace("seera_", "").replace("_takmela", "")
                caption_text = f"📜 السيرة النبوية - تكملة الدرس {d_num}"
            else:
                d_num = data.replace("seera_", "")
                caption_text = f"📜 السيرة النبوية - الدرس {d_num}"
            await context.bot.send_voice(chat_id=chat_id, voice=file_id, caption=caption_text)
        else:
            parts = data.split("_")
            book_num = parts[0].replace("b", "")
            lesson_num = parts[2]
            await context.bot.send_voice(chat_id=chat_id, voice=file_id, caption=f"🎧 التسجيل الصوتي {lesson_num} (الكتاب {book_num})")

if __name__ == '__main__':
    # تشغيل خادم الويب في الخلفية أولاً لضمان عدم توقف البوت
    keep_alive()
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("البوت يعمل الآن بكامل قوائم السيرة النبوية وتحفة الأطفال على مدار 24 ساعة...")
    application.run_polling()
