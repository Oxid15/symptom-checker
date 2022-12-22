from user_model import UserModel
from utils import bmi as bmi_func


class Diabetes1:
    def symptoms(self, user: UserModel):
        pass

# do we need different classes for different types


class DiabetesModel:
    def symptoms(self, user: UserModel):
        bmi = bmi_func(user)
        if (
            user.age >= 45 or
            bmi > 25 or
            user.has_parents_diabetes or
            user.has_art_hypertension or
            user.has_smoking_habit or
            user.has_alcohol_habit or
            user.has_appetite_increase or
            user.has_burning_sensation or
            user.has_lose_weight or
            user.has_freq_urination or
            user.has_nausea or
            user.has_faintness or
            user.has_thirst_morning_night or
            user.has_poor_wound_healing or
            user.has_high_blood_pressure or
            user.has_furunculosis or
            user.has_candidiasis or
            user.has_exc_physical_activity or
            user.has_impaired_vision or
            user.has_pain_in_leg or
            user.has_headache or
            user.has_dizziness
        ):
            return True

    def recommendations(self, user) -> str:
        return 'all good'
