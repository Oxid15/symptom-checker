from user_model import UserModel


class Diabetes1:
    def __init__(self):
        self.user = UserModel()

    def symptoms(self):
        pass

# do we need different classes for different types


class Diabetes:
    def __init__(self):
        self.user = UserModel()

    def symptoms(self):
        if (self.user.age >= 45 or
                self.user.bmi > 25 or
                self.user.has_parents_diabetes or
                self.user.has_art_hypertension or
                self.user.has_smoking_habit or
                self.user.has_appetite_increase or
                self.user.has_burning_sensation or
                self.user.has_lose_weight or
                self.user.has_freq_urination or
                self.user.has_nausea or
                self.user.has_faintness or
                self.user.has_thirst_morning_night or
                self.user.has_poor_wound_healing or
                self.user.has_high_blood_pressure or
                self.user.has_furunculosis or
                self.user.has_candidiasis or
                self.user.has_exc_physical_activity or
                self.user.has_impaired_vision or
                self.user.has_pain_in_leg or
                self.user.has_headache or
                self.user.has_dizziness):
            return True

    def recommendations(self):

        if self.user.is_pregnant:
            return ''
        else:
            return ''

