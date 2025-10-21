from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8297252247:AAFWCEp1Taa6wykfjzmO4nGC7w0PjTOVuCA'  # Токен вашего бота

# Функция для старта бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f'Привет, {user.first_name}! Нажми на кнопку ниже, чтобы посмотреть товары.',
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Смотреть товары", web_app=WebAppInfo(url='https://myonlineshop.loca.lt'))  # URL вашего мини-приложения
        ]])
    )

# Основная функция для запуска бота
def main():
    application = Application.builder().token(TOKEN).build()

    # Обрабатываем команду /start
    application.add_handler(CommandHandler("start", start))

    # Начинаем прослушивание
    application.run_polling()

if __name__ == '__main__':
    main()
