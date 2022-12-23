from typing import List
import logging
from user_model import UserModel
from model import SymptomChecker

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


def kb2regex(kb: List[List[str]]) -> filters.Regex:
    terms = []
    for row in kb:
        for term in row:
            terms.append(term)

    return filters.Regex(f'[{"|".join(terms)}]')


BINARY_KB = [['yes', 'no']]
GENDER_KB = [['male', 'female']]
ACTIVITY_KB = [['mild', 'moderate', 'active']]
INTENSITY_KB = [['mild', 'moderate', 'intense']]
DURATION_KB = [['<1 day', '1 day to 1 week', '1 week to 1 month', '1 month to 1 year']]
HEADACHE_LOCATION_KB = [['left', 'right', 'both', 'center']]

INTEGER_REGEX = filters.Regex('^[0-9]')
BINARY_REGEX = kb2regex(BINARY_KB)
GENDER_REGEX = kb2regex(GENDER_KB)
ACTIVITY_REGEX = kb2regex(ACTIVITY_KB)
INTENSITY_REGEX = kb2regex(INTENSITY_KB)
DURATION_REGEX = kb2regex(DURATION_KB)
HEADACHE_LOCATION_REGEX = kb2regex(HEADACHE_LOCATION_KB)

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

users = {}
model = SymptomChecker()

with open('token', 'r') as f:
    TOKEN = f.readline()


async def ask_optional(update: Update, text: str, kb: List[List[str]]):
    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            kb, one_time_keyboard=True,
            input_field_placeholder=text
        )
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Entry point into the dialogue.
    Creates the model of the user that is stored while dialogue runs and is destroyed at the exit.
    """
    user = update.message.from_user
    users[user.id] = UserModel()
    users[user.id].name = user.first_name
    logger.info(f'User {user.id} started')

    await update.message.reply_text(f'Hi {user.first_name}! This is symptom checker, what is your age?')
    return AGE


async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].age = int(update.message.text)
    logger.info(f'User {user.id} selected {users[user.id].age}')

    await ask_optional(update, f'{users[user.id].name}, what is your gender?', GENDER_KB)
    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].gender = update.message.text
    logger.info(f'User {user.id} selected {users[user.id].gender}')

    if users[user.id].gender == 'male':
        await update.message.reply_text(f'{users[user.id].name}, what is your weight in kg? Please write integer number')
        return WEIGHT
    elif users[user.id].gender == 'female':
        await ask_optional(update, 'Are you pregnant?', BINARY_KB)
        return IS_PREGNANT
    else:
        raise ValueError(f'User selected: {users[user.id].gender}')


async def is_pregnant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].is_pregnant = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].is_pregnant}')

    await update.message.reply_text(f'{users[user.id].name},  what is your weight in kg? Please write integer number')
    return WEIGHT


async def weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].weight = int(update.message.text)
    logger.info(f'User {user.id} selected {users[user.id].weight}')

    await update.message.reply_text('What is your height in cm? Please write integer number')
    return HEIGHT


async def height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].height = int(update.message.text)
    logger.info(f'User {user.id} selected {users[user.id].height}')

    await ask_optional(update, 'What is your physical activity level?', ACTIVITY_KB)
    return ACTIVITY_LEVEL


async def activity_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].activity_level = update.message.text
    logger.info(f'User {user.id} selected {users[user.id].activity_level}')

    await ask_optional(update, 'Do you smoke?', BINARY_KB)
    return HAS_SMOKING_HABIT


async def has_smoking_habit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_smoking_habit = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].height}')

    await ask_optional(update, 'Do you drink alcohol frequently?', BINARY_KB)
    return HAS_ALCOHOL_HABIT


async def has_alcohol_habit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_alcohol_habit = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_alcohol_habit}')

    await ask_optional(update, 'Have you been diagnosed with arterial hypertension?', BINARY_KB)
    return HAS_ART_HYPERTENSION


async def has_art_hypertension(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_art_hypertension = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_art_hypertension}')

    await ask_optional(update, 'Have your parents been diagnosed with arterial hypertension?', BINARY_KB)
    return HAS_PARENTS_HYPERTENSION


async def has_parents_hypertension(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_parents_hypertension = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_parents_hypertension}')

    await ask_optional(update, 'Do you have burning sensation?', BINARY_KB)
    return HAS_BURNING_SENSATION


async def has_burning_sensation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_burning_sensation = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_burning_sensation}')

    await ask_optional(update, 'Did you recently lose weight?', BINARY_KB)
    return HAS_LOSE_WEIGHT


async def has_lose_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_lose_weight = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_lose_weight}')

    await ask_optional(update, 'Did you have your appetite increase recently?', BINARY_KB)
    return HAS_APPETITE_INCREASE


async def has_appetite_increase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_appetite_increase = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_appetite_increase}')

    await ask_optional(update, 'Do you urinate frequently?', BINARY_KB)
    return HAS_FREQUENT_URINATION


async def has_freq_urination(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_freq_urination = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_freq_urination}')

    await ask_optional(update, 'Do you have nausea?', BINARY_KB)
    return HAS_NAUSEA


async def has_nausea(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_nausea = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_nausea}')

    await ask_optional(update, 'Do you feel faintness?', BINARY_KB)
    return HAS_FAINTNESS


async def has_faintness(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_faintness = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_faintness}')

    await ask_optional(update, 'Do you feel strong thirst at the morning or during the night?', BINARY_KB)
    return HAS_THIRST_MORNING_NIGHT


async def has_thirst_morning_night(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_thirst_morning_night = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_thirst_morning_night}')

    await ask_optional(update, 'Do you have your wounds heal poorly?', BINARY_KB)
    return HAS_POOR_WOUND_HEALING


async def has_poor_wound_healing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_poor_wound_healing = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_poor_wound_healing}')

    await ask_optional(update, 'Have you been diagnosed diabetes before?', BINARY_KB)
    return HAS_DIABETES


async def has_diabetes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_diabetes = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_diabetes}')

    await ask_optional(update, 'Have your parents been diagnosed with diabetes?', BINARY_KB)
    return HAS_PARENTS_DIABETES


async def has_parents_diabetes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_parents_diabetes = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_parents_diabetes}')

    await ask_optional(update, 'Do you have high blood pressure?', BINARY_KB)
    return HAS_HIGH_BLOOD_PRESSURE


async def has_high_blood_pressure(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_high_blood_pressure = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_high_blood_pressure}')

    await ask_optional(update, 'Do you have furunculosis?', BINARY_KB)
    return HAS_FURUNCULOSIS


async def has_furunculosis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_furunculosis = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_furunculosis}')

    await ask_optional(update, 'Do you have candiasis?', BINARY_KB)
    return HAS_CANDIASIS


async def has_candidiasis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_candidiasis = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_candidiasis}')

    await ask_optional(update, 'Did you have excessive physical activity recently?', BINARY_KB)
    return HAS_EXC_PHYSICAL_ACTIVITY


async def has_exc_physical_activity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_exc_physical_activity = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_exc_physical_activity}')

    await ask_optional(update, 'Do you have impaired vision?', BINARY_KB)
    return HAS_IMPAIRED_VISION


async def has_impaired_vision(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_impaired_vision = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_impaired_vision}')

    if users[user.id].has_impaired_vision:
        await ask_optional(update, 'How long do you have it?', DURATION_KB)
        return IMPAIRED_VISION_DURATION
    else:
        await ask_optional(update, 'Do you have pain in the leg?', BINARY_KB)
        return HAS_PAIN_IN_LEG


async def impaired_vision_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].impaired_vision_duration = update.message.text
    logger.info(f'User {user.id} selected {users[user.id].impaired_vision_duration}')

    await ask_optional(update, 'Do you have pain in the leg?', BINARY_KB)
    return HAS_PAIN_IN_LEG


async def has_pain_in_leg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_pain_in_leg = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_pain_in_leg}')

    if users[user.id].has_pain_in_leg:
        await ask_optional(update, 'How intense is the pain?', INTENSITY_KB)
        return PAIN_IN_LEG_INTENSITY
    else:
        await ask_optional(update, 'Do you have a headache?', BINARY_KB)
        return HAS_HEADACHE


async def pain_in_leg_intensity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].pain_in_leg_intensity = update.message.text
    logger.info(f'User {user.id} selected {users[user.id].pain_in_leg_intensity}')

    await ask_optional(update, 'Do you have a headache?', BINARY_KB)
    return HAS_HEADACHE


async def has_headache(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_headache = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_headache}')

    if users[user.id].has_headache:
        await ask_optional(update, 'Where?', HEADACHE_LOCATION_KB)
        return HEADACHE_LOCATION
    else:
        await ask_optional(update, 'Do you feel dizzy?', BINARY_KB)
        return HAS_DIZZINESS


async def headache_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].headache_location = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].headache_location}')

    await ask_optional(update, 'For how long?', DURATION_KB)
    return HEADACHE_DURATION


async def headache_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].headache_duration = update.message.text == 'yes'

    logger.info(f'User {user.id} selected {users[user.id].headache_duration}')

    await ask_optional(update,'How intense is the pain?', INTENSITY_KB)
    return HEADACHE_INTENSITY


async def headache_intensity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].headache_intensity = update.message.text
    logger.info(f'User {user.id} selected {users[user.id].headache_intensity}')

    await ask_optional(update, 'Do you feel dizzy?', BINARY_KB)
    return HAS_DIZZINESS


async def has_dizziness(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].has_dizziness = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].has_dizziness}')

    if users[user.id].has_dizziness:
        await ask_optional(update, 'For how long?', DURATION_KB)
        return DIZZINESS_DURATION
    else:
        # INFERENCE
        response = model.check(users[user.id])

        await update.message.reply_text(response)
        return ConversationHandler.END


async def dizziness_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].dizziness_duration = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].dizziness_duration}')

    await ask_optional(update, 'How intense?', INTENSITY_KB)
    return DIZZINESS_INTENSITY


async def dizziness_intensity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].dizziness_intensity = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].dizziness_intensity}')

    await ask_optional(update, 'Dizziness inteferes in your daily activities?', BINARY_KB)
    return DIZZINESS_INTERFERES


async def dizziness_interferes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    users[user.id].dizziness_interferes = update.message.text == 'yes'
    logger.info(f'User {user.id} selected {users[user.id].dizziness_interferes}')

    # INFERENCE
    response = model.check(users[user.id])

    await update.message.reply_text(response)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info(f"User {user.id} canceled the conversation")
    del users[user.id]
    logger.info(f"User {user.id} was deleted")

    await update.message.reply_text("Bye!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()
    handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGE: [MessageHandler(INTEGER_REGEX, age)],
            GENDER: [MessageHandler(GENDER_REGEX, gender)],
            IS_PREGNANT: [MessageHandler(BINARY_REGEX, is_pregnant)],
            WEIGHT: [MessageHandler(INTEGER_REGEX, weight)],
            HEIGHT: [MessageHandler(INTEGER_REGEX, height)],
            ACTIVITY_LEVEL: [MessageHandler(ACTIVITY_REGEX, activity_level)],
            HAS_SMOKING_HABIT: [MessageHandler(BINARY_REGEX, has_smoking_habit)],
            HAS_ALCOHOL_HABIT: [MessageHandler(BINARY_REGEX, has_alcohol_habit)],
            HAS_ART_HYPERTENSION: [MessageHandler(BINARY_REGEX, has_art_hypertension)],
            HAS_PARENTS_HYPERTENSION: [MessageHandler(BINARY_REGEX, has_parents_hypertension)],
            HAS_BURNING_SENSATION: [MessageHandler(BINARY_REGEX, has_burning_sensation)],
            HAS_LOSE_WEIGHT: [MessageHandler(BINARY_REGEX, has_lose_weight)],
            HAS_APPETITE_INCREASE: [MessageHandler(BINARY_REGEX, has_appetite_increase)],
            HAS_FREQUENT_URINATION: [MessageHandler(BINARY_REGEX, has_freq_urination)],
            HAS_NAUSEA: [MessageHandler(BINARY_REGEX, has_nausea)],
            HAS_FAINTNESS: [MessageHandler(BINARY_REGEX, has_faintness)],
            HAS_THIRST_MORNING_NIGHT: [MessageHandler(BINARY_REGEX, has_poor_wound_healing)],
            HAS_POOR_WOUND_HEALING: [MessageHandler(BINARY_REGEX, has_poor_wound_healing)],
            HAS_DIABETES: [MessageHandler(BINARY_REGEX, has_diabetes)],
            HAS_PARENTS_DIABETES: [MessageHandler(BINARY_REGEX, has_parents_diabetes)],
            HAS_HIGH_BLOOD_PRESSURE: [MessageHandler(BINARY_REGEX, has_high_blood_pressure)],
            HAS_FURUNCULOSIS: [MessageHandler(BINARY_REGEX, has_furunculosis)],
            HAS_CANDIASIS: [MessageHandler(BINARY_REGEX, has_candidiasis)],
            HAS_EXC_PHYSICAL_ACTIVITY: [MessageHandler(BINARY_REGEX, has_exc_physical_activity)],
            HAS_IMPAIRED_VISION: [MessageHandler(BINARY_REGEX, has_impaired_vision)],
            IMPAIRED_VISION_DURATION: [MessageHandler(DURATION_REGEX, impaired_vision_duration)],
            HAS_PAIN_IN_LEG: [MessageHandler(BINARY_REGEX, has_pain_in_leg)],
            PAIN_IN_LEG_INTENSITY: [MessageHandler(INTENSITY_REGEX, pain_in_leg_intensity)],
            HAS_HEADACHE: [MessageHandler(BINARY_REGEX, has_headache)],
            HEADACHE_LOCATION: [MessageHandler(HEADACHE_LOCATION_REGEX, headache_location)],
            HEADACHE_DURATION: [MessageHandler(DURATION_REGEX, headache_duration)],
            HEADACHE_INTENSITY: [MessageHandler(INTENSITY_REGEX, headache_intensity)],
            HAS_DIZZINESS: [MessageHandler(BINARY_REGEX, has_dizziness)],
            DIZZINESS_DURATION: [MessageHandler(DURATION_REGEX, dizziness_duration)],
            DIZZINESS_INTENSITY: [MessageHandler(INTENSITY_REGEX, dizziness_intensity)],
            DIZZINESS_INTERFERES: [MessageHandler(BINARY_REGEX, dizziness_interferes)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(handler)

    application.run_polling()
