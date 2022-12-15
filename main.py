import logging

from user_model import UserModel

from telegram import __version__ as TG_VER
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, 'alpha', 5):
    raise RuntimeError(
        f'This example is not compatible with your current PTB version {TG_VER}. To view the '
        f'{TG_VER} version of this example, '
        f'visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html'
    )

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

GENDER, AGE = range(2)

user_model = UserModel()

with open('token', 'r') as f:
    TOKEN = f.readline()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['Male', 'Female']]
    user = update.message.from_user

    logger.info(f'User {user.first_name} started')

    await update.message.reply_text(
        f'Hi {user.first_name}! This is symptom checker, what is your gender?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Male of female?'
        ),
    )
    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.name = user.first_name
    if update.message.text == 'Male':
        user_model.gender = False
    elif update.message.text == 'Female':
        user_model.gender = True

    logger.info(f'User {user.first_name} selected {user_model.gender}')

    await update.message.reply_text(
        f'{user_model.name}, what is your age?',
        reply_markup=ReplyKeyboardRemove(),
    )

    return AGE


async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        'Okay'
    )
    user_model.age = int(update.message.text)

    logger.info(f'Total: {user_model.name}, {user_model.age}, {user_model.gender}')
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info(f"User {user.first_name} canceled the conversation")
    await update.message.reply_text(
        "Bye!",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()
    handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GENDER: [MessageHandler(filters.Regex('^(Male|Female)$'), gender)],
            AGE: [MessageHandler(filters.Regex('^[0-9]'), age)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(handler)

    application.run_polling()
