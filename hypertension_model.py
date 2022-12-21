from user_model import UserModel
from utils import bmi as bmi_func


class HypertensionModel:
    def symptoms(self, user: UserModel):
        bmi = bmi_func(user)
        if user.gender == 'male':
            if (user.age > 55 or
                    user.has_smoking_habit in ['every hour', 'quit'] or
                    user.alcohol == 'every day' or
                    user.activity_level == 'mild' or
                    user.has_parents_hypertension or
                    bmi > 25 or
                    user.heart_beat_per_sec > 80 or
                    user.has_high_blood_pressure or
                    user.has_diabetes):
                return True
        else:
            if (user.age > 65 or
                    user.has_smoking_habit in ['every hour', 'quit'] or
                    user.alcohol == 'every day' or
                    user.activity_level == 'mild' or
                    user.has_parents_hypertension or
                    bmi > 25 or
                    user.heart_beat_per_sec > 80 or
                    user.has_high_blood_pressure or
                    user.has_diabetes):
                return True

    def score(self, user: UserModel):
        bmi = bmi_func(user)

        scoring = {
            'gender': {'male>55': 6, 'female>65': 3, 'female': 0, 'male': 0},
            'alcohol': {'every day': 8, 'once a week': 2, 'on holidays': 0, 'quit': 0, 'no': 0},  # todo
            'smoker': {'a lot': 5, 'quit': 0, 'no': 0},  # todo
            'activity': {'mild': 5, 'moderate': 1, 'severe': 0},
            'parents hypertension': 8,
            'bmi': {'<25': 0, '25-30': 5, '30>': 10},
            'heart beat': {'<80': 0, '80>': 4},
            'diabetes': 5,
            'high bp': 8
        }
        score = 0
        if user.gender == 'male' and user.age > 55:
            score += scoring['gender']['male>55']
        elif user.gender == 'female' and user.age > 65:
            score += scoring['gender']['female>65']
        elif user.activity_level:
            score += scoring['activity'][user.activity_level]
        elif user.has_smoking_habit:
            score += scoring['smoker'][user.has_smoking_habit]
        elif user.alcohol:
            score += scoring['alcohol'][user.alcohol]
        elif user.has_parents_hypertension:
            score += scoring['parents hypertension']
        elif bmi > 30:
            score += scoring['bmi']['30>']
        elif 25 < bmi < 30:
            score += scoring['bmi']['25-30']
        elif user.heart_beat_per_sec > 80:
            score += scoring['heart beat']['80>']
        elif user.has_diabetes:
            score += scoring['diabetes']
        elif user.has_high_blood_pressure:
            score += scoring['high bp']
        # highest score is 59
        return score

    def recommendations(self, user: UserModel) -> str:
        score = self.score(user)
        if score > 30:
            return 'bad'
        if user.activity_level != 'active':
            return 'run'
        return 'all good'
