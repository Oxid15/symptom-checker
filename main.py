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

BINARY_KB = [['yes', 'no']]
INTENSITY_KB = [['mild', 'moderate', 'active']]
DURATION_KB = [['<1 day', '1 day to 1 week', '1 week to 1 month', '1 month to 1 year']]

(
    GENDER, AGE, IS_PREGNANT, WEIGHT, HEIGHT,
    ACTIVITY_LEVEL, HAS_SMOKING_HABIT, HAS_ALCOHOL_HABIT,
    HAS_ART_HYPERTENSION, HAS_PARENTS_HYPERTENSION,
    HAS_BURNING_SENSATION, HAS_LOSE_WEIGHT,
    HAS_APPETITE_INCREASE, HAS_FREQUENT_URINATION,
    HAS_NAUSEA, HAS_FAINTNESS, HAS_THIRST_MORNING_NIGHT,
    HAS_POOR_WOUND_HEALING, HAS_DIABETES, HAS_PARENTS_DIABETES,
    HAS_HIGH_BLOOD_PRESSURE, HAS_FURUNCULOSIS,
    HAS_CANDIASIS, HAS_EXC_PHYSICAL_ACTIVITY,
    HAS_IMPAIRED_VISION, IMPAIRED_VISION_DURATION,
    HAS_PAIN_IN_LEG, PAIN_IN_LEG_INTENSITY,
    HAS_HEADACHE, HEADACHE_LOCATION, HEADACHE_DURATION,
    HEADACHE_INTENSITY, HAS_DIZZINESS, DIZZINESS_DURATION,
    DIZZINESS_INTENSITY, DIZZINESS_INTERFERES
) = range(36)

user_model = UserModel()

with open('token', 'r') as f:
    TOKEN = f.readline()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.name = user.first_name

    logger.info(f'User {user.first_name} started')

    await update.message.reply_text(
        f'Hi {user.first_name}! This is symptom checker, what is your age?',
    )
    return AGE


async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['male', 'female']]
    user = update.message.from_user
    user_model.age = int(update.message.text)

    logger.info(f'User {user.first_name} selected {user_model.age}')

    await update.message.reply_text(
        f'{user_model.name}, what is your gender?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Male or female?'
        ),
    )

    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.gender = update.message.text

    logger.info(f'User {user.first_name} selected {user_model.gender}')

    if user_model.gender == 'male':
        await update.message.reply_text(
            f'{user_model.name}, what is your weight in kg? Please write integer number'
        )
        return WEIGHT
    elif user_model.gender == 'female':

        await update.message.reply_text(
            f'{user_model.name}, are you pregnant?',
            reply_markup=ReplyKeyboardMarkup(
                BINARY_KB, one_time_keyboard=True,
                input_field_placeholder='Yes or no?'
            )
        )
        return IS_PREGNANT
    else:
        raise ValueError(f'User selected: {user_model.gender}')


async def is_pregnant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.is_pregnant = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.is_pregnant}')

    await update.message.reply_text(
        f'{user_model.name},  what is your weight in kg? Please write integer number'
    )

    return WEIGHT


async def weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.weight = int(update.message.text)

    logger.info(f'User {user.first_name} selected {user_model.weight}')

    await update.message.reply_text(
        'What is your height in cm? Please write integer number'
    )

    return HEIGHT


async def height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.height = int(update.message.text)

    logger.info(f'User {user.first_name} selected {user_model.height}')

    await update.message.reply_text(
        'What is your physical activity level?',
        reply_markup=ReplyKeyboardMarkup(
            INTENSITY_KB, one_time_keyboard=True,
            input_field_placeholder='How active are you?'
        )
    )

    return ACTIVITY_LEVEL


async def activity_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.activity_level = update.message.text

    logger.info(f'User {user.first_name} selected {user_model.activity_level}')

    await update.message.reply_text(
        'Do you smoke?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_SMOKING_HABIT


async def has_smoking_habit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_smoking_habit = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.height}')

    await update.message.reply_text(
        'Do you drink alcohol frequently?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_ALCOHOL_HABIT


async def has_alcohol_habit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_alcohol_habit = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_alcohol_habit}')

    await update.message.reply_text(
        'Have you been diagnosed with arterial hypertension?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_ART_HYPERTENSION


async def has_art_hypertension(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_art_hypertension = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_art_hypertension}')

    await update.message.reply_text(
        'Have your parents been diagnosed with arterial hypertension?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_PARENTS_HYPERTENSION


async def has_parents_hypertension(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_parents_hypertension = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_parents_hypertension}')

    await update.message.reply_text(
        'Do you have burning sensation?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_BURNING_SENSATION


async def has_burning_sensation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_burning_sensation = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_burning_sensation}')

    await update.message.reply_text(
        'Did you recently lose weight?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_LOSE_WEIGHT


async def has_lose_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_lose_weight = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_lose_weight}')

    await update.message.reply_text(
        'Did you have your appetite increase recently?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_APPETITE_INCREASE


async def has_appetite_increase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_appetite_increase = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_appetite_increase}')

    await update.message.reply_text(
        'Do you urinate frequently?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_FREQUENT_URINATION


async def has_freq_urination(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_freq_urination = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_freq_urination}')

    await update.message.reply_text(
        'Do you have nausea?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_NAUSEA


async def has_nausea(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_nausea = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_nausea}')

    await update.message.reply_text(
        'Do you feel faintness?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_FAINTNESS


async def has_faintness(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_faintness = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_faintness}')

    await update.message.reply_text(
        'Do you feel strong thirst at the morning or during the night?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_THIRST_MORNING_NIGHT


async def has_thirst_morning_night(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_thirst_morning_night = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_thirst_morning_night}')

    await update.message.reply_text(
        'Do you have your wounds heal poorly?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_POOR_WOUND_HEALING


async def has_poor_wound_healing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_poor_wound_healing = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_poor_wound_healing}')

    await update.message.reply_text(
        'Have you been diagnosed diabetes before?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_DIABETES


async def has_diabetes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_diabetes = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_diabetes}')

    await update.message.reply_text(
        'Have your parents been diagnosed with diabetes?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_PARENTS_DIABETES


async def has_parents_diabetes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_parents_diabetes = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_parents_diabetes}')

    await update.message.reply_text(
        'Do you have high blood pressure?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_HIGH_BLOOD_PRESSURE


async def has_high_blood_pressure(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_high_blood_pressure = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_high_blood_pressure}')

    await update.message.reply_text(
        'Do you have furunculosis?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_FURUNCULOSIS


async def has_furunculosis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_furunculosis = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_furunculosis}')

    await update.message.reply_text(
        'Do you have candiasis?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_CANDIASIS


async def has_candidiasis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_candidiasis = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_candidiasis}')

    await update.message.reply_text(
        'Did you have excessive physical activity recently?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_EXC_PHYSICAL_ACTIVITY


async def has_exc_physical_activity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_exc_physical_activity = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_exc_physical_activity}')

    await update.message.reply_text(
        'Do you have impaired vision?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_IMPAIRED_VISION


async def has_impaired_vision(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_impaired_vision = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_impaired_vision}')

    if user_model.has_impaired_vision:
        await update.message.reply_text(
            'How long do you have it?',
            reply_markup=ReplyKeyboardMarkup(
                DURATION_KB, one_time_keyboard=True,
                input_field_placeholder='Duration'
            )
        )

        return IMPAIRED_VISION_DURATION
    else:

        await update.message.reply_text(
            'Do you have pain in the leg?',
            reply_markup=ReplyKeyboardMarkup(
                BINARY_KB, one_time_keyboard=True,
                input_field_placeholder='Yes or no?'
            )
        )

        return HAS_PAIN_IN_LEG


async def impaired_vision_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.impaired_vision_duration = update.message.text

    logger.info(f'User {user.first_name} selected {user_model.impaired_vision_duration}')

    await update.message.reply_text(
        'Do you have pain in the leg?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_PAIN_IN_LEG


async def has_pain_in_leg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_pain_in_leg = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_pain_in_leg}')

    if user_model.has_pain_in_leg:
        reply_keyboard = [['mild', 'moderate', 'intense']]
        await update.message.reply_text(
            'How intense the pain?',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True,
                input_field_placeholder='How intense the pain?'
            )
        )

        return PAIN_IN_LEG_INTENSITY
    else:

        await update.message.reply_text(
            'Do you have a headache?',
            reply_markup=ReplyKeyboardMarkup(
                BINARY_KB, one_time_keyboard=True,
                input_field_placeholder='Yes or no?'
            )
        )

        return HAS_HEADACHE


async def pain_in_leg_intensity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.pain_in_leg_intensity = update.message.text
    logger.info(f'User {user.first_name} selected {user_model.pain_in_leg_intensity}')

    await update.message.reply_text(
        'Do you have a headache?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_HEADACHE


async def has_headache(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_headache = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_headache}')

    if user_model.has_headache:
        reply_keyboard = [['left', 'right', 'both', 'center']]
        await update.message.reply_text(
            'Where?',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True,
                input_field_placeholder='Where?'
            )
        )

        return HEADACHE_LOCATION
    else:

        if user_model.has_headache:
            await update.message.reply_text(
                'Do you feel dizzy?',
                reply_markup=ReplyKeyboardMarkup(
                    BINARY_KB, one_time_keyboard=True,
                    input_field_placeholder='Yes or no?'
                )
            )

        return HAS_DIZZINESS


async def headache_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.headache_location = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.headache_location}')

    await update.message.reply_text(
        'For how long?',
        reply_markup=ReplyKeyboardMarkup(
            DURATION_KB, one_time_keyboard=True,
            input_field_placeholder='Duration'
        )
    )

    return HEADACHE_DURATION


async def headache_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['mild', 'moderate', 'intense']]
    user = update.message.from_user
    user_model.headache_duration = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.headache_duration}')

    await update.message.reply_text(
        'How intense is the pain?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
            input_field_placeholder='Intensity'
        )
    )

    return HEADACHE_INTENSITY


async def headache_intensity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.headache_intensity = update.message.text

    logger.info(f'User {user.first_name} selected {user_model.headache_intensity}')

    await update.message.reply_text(
        'Do you feel dizzy?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return HAS_DIZZINESS


async def has_dizziness(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.has_dizziness = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.has_dizziness}')

    if user_model.has_dizziness:
        await update.message.reply_text(
            'For how long?',
            reply_markup=ReplyKeyboardMarkup(
                DURATION_KB, one_time_keyboard=True,
                input_field_placeholder='Duration'
            )
        )

        return DIZZINESS_DURATION
    else:
        await update.message.reply_text(
            str(user_model)
        )

        return ConversationHandler.END


async def dizziness_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.dizziness_duration = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.dizziness_duration}')

    await update.message.reply_text(
        'How intense?',
        reply_markup=ReplyKeyboardMarkup(
            INTENSITY_KB, one_time_keyboard=True,
            input_field_placeholder='Intensity'
        )
    )

    return DIZZINESS_INTENSITY


async def dizziness_intensity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.dizziness_intensity = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.dizziness_intensity}')

    await update.message.reply_text(
        'Dizziness inteferes in your daily activities?',
        reply_markup=ReplyKeyboardMarkup(
            BINARY_KB, one_time_keyboard=True,
            input_field_placeholder='Yes or no?'
        )
    )

    return DIZZINESS_INTERFERES


async def dizziness_interferes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_model.dizziness_interferes = update.message.text == 'yes'

    logger.info(f'User {user.first_name} selected {user_model.dizziness_interferes}')

    await update.message.reply_text(
        str(user_model)
    )

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
            AGE: [
                MessageHandler(filters.Regex('^[0-9]'), age)
            ],
            GENDER: [
                MessageHandler(filters.Regex('[male|female]'), gender)
            ],
            IS_PREGNANT: [
                MessageHandler(filters.Regex('[yes|no]'), is_pregnant)
            ],
            WEIGHT: [
                MessageHandler(filters.Regex('^[0-9]'), weight)
            ],
            HEIGHT: [
                MessageHandler(filters.Regex('^[0-9]'), height)
            ],
            ACTIVITY_LEVEL: [
                MessageHandler(filters.Regex('[mild|moderate|active]'), activity_level)
            ],
            HAS_SMOKING_HABIT: [
                MessageHandler(filters.Regex('[yes|no]'), has_smoking_habit)
            ],
            HAS_ALCOHOL_HABIT: [
                MessageHandler(filters.Regex('[yes|no]'), has_alcohol_habit)
            ],
            HAS_ART_HYPERTENSION: [
                MessageHandler(filters.Regex('[yes|no]'), has_art_hypertension)
            ],
            HAS_PARENTS_HYPERTENSION: [
                MessageHandler(filters.Regex('[yes|no]'), has_parents_hypertension)
            ],
            HAS_BURNING_SENSATION: [
                MessageHandler(filters.Regex('[yes|no]'), has_burning_sensation)
            ],
            HAS_LOSE_WEIGHT: [
                MessageHandler(filters.Regex('[yes|no]'), has_lose_weight)
            ],
            HAS_APPETITE_INCREASE: [
                MessageHandler(filters.Regex('[yes|no]'), has_appetite_increase)
            ],
            HAS_FREQUENT_URINATION: [
                MessageHandler(filters.Regex('[yes|no]'), has_freq_urination)
            ],
            HAS_NAUSEA: [
                MessageHandler(filters.Regex('[yes|no]'), has_nausea)
            ],
            HAS_FAINTNESS: [
                MessageHandler(filters.Regex('[yes|no]'), has_faintness)
            ],
            HAS_THIRST_MORNING_NIGHT: [
                MessageHandler(filters.Regex('[yes|no]'), has_poor_wound_healing)
            ],
            HAS_POOR_WOUND_HEALING: [
                MessageHandler(filters.Regex('[yes|no]'), has_poor_wound_healing)
            ],
            HAS_DIABETES: [
                MessageHandler(filters.Regex('[yes|no]'), has_diabetes)
            ],
            HAS_PARENTS_DIABETES: [
                MessageHandler(filters.Regex('[yes|no]'), has_parents_diabetes)
            ],
            HAS_HIGH_BLOOD_PRESSURE: [
                MessageHandler(filters.Regex('[yes|no]'), has_high_blood_pressure)
            ],
            HAS_FURUNCULOSIS: [
                MessageHandler(filters.Regex('[yes|no]'), has_furunculosis)
            ],
            HAS_CANDIASIS: [
                MessageHandler(filters.Regex('[yes|no]'), has_candidiasis)
            ],
            HAS_EXC_PHYSICAL_ACTIVITY: [
                MessageHandler(filters.Regex('[yes|no]'), has_exc_physical_activity)
            ],
            HAS_IMPAIRED_VISION: [
                MessageHandler(filters.Regex('[yes|no]'), has_impaired_vision)
            ],
            IMPAIRED_VISION_DURATION: [
                MessageHandler(filters.Regex('[<1 day|1 day to 1 week|1 week to 1 month|1 month to 1 year]'), impaired_vision_duration)
            ],
            HAS_PAIN_IN_LEG: [
                MessageHandler(filters.Regex('[yes|no]'), has_pain_in_leg)
            ],
            PAIN_IN_LEG_INTENSITY: [
                MessageHandler(filters.Regex('[mild|moderate|active]'), pain_in_leg_intensity)
            ],
            HAS_HEADACHE: [
                MessageHandler(filters.Regex('[yes|no]'), has_headache)
            ],
            HEADACHE_LOCATION: [
                MessageHandler(filters.Regex('left|right|both|center'), headache_location)
            ],
            HEADACHE_DURATION: [
                MessageHandler(filters.Regex('[<1 day|1 day to 1 week|1 week to 1 month|1 month to 1 year]'), headache_duration)
            ],
            HEADACHE_INTENSITY: [
                MessageHandler(filters.Regex('[mild|moderate|active]'), headache_intensity)
            ],
            HAS_DIZZINESS: [
                MessageHandler(filters.Regex('[yes|no]'), has_dizziness)
            ],
            DIZZINESS_DURATION: [
                MessageHandler(filters.Regex('[<1 day|1 day to 1 week|1 week to 1 month|1 month to 1 year]'), dizziness_duration)
            ],
            DIZZINESS_INTENSITY: [
                MessageHandler(filters.Regex('[mild|moderate|active]'), dizziness_intensity)
            ],
            DIZZINESS_INTERFERES: [
                MessageHandler(filters.Regex('[yes|no]'), dizziness_interferes)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(handler)

    application.run_polling()
