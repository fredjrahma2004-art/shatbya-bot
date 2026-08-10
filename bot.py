from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

TOKEN = "8166656056:AAE8xNDpBcjUJ3D1II0twNyV7goQiyYKOhIo"


async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if update.message.audio:
    file_id = update.message.audio.file_id
    await update.message.reply_text(
        f"معرّف الصوت هو:\n`{file_id}`", parse_mode="Markdown"
    )


def main():
  application = Application.builder().token(TOKEN).build()
  application.add_handler(MessageHandler(filters.AUDIO, get_file_id))
  application.run_polling()


if __name__ == "__main__":
  main()
