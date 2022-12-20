from user_model import UserModel


class Hypertension:
    def __init__(self):
        self.user = UserModel()

    def symptoms(self):
        if self.user.gender == 'male':
            if (self.user.age > 55 or
                    self.user.has_smoking_habit in ['every hour', 'quit'] or
                    self.user.alcohol == 'every day' or
                    self.user.activity_level == 'mild' or
                    self.user.has_parents_hypertension or
                    self.user.bmi > 25 or
                    self.user.heart_beat_per_sec > 80 or
                    self.user.has_high_blood_pressure or
                    self.user.has_diabetes):
                return True
        else:
            if (self.user.age > 65 or
                    self.user.has_smoking_habit in ['every hour', 'quit'] or
                    self.user.alcohol == 'every day' or
                    self.user.activity_level == 'mild' or
                    self.user.has_parents_hypertension or
                    self.user.bmi > 25 or
                    self.user.heart_beat_per_sec > 80 or
                    self.user.has_high_blood_pressure or
                    self.user.has_diabetes):
                return True

    def score(self):
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
        if self.user.gender == 'male' and self.user.age > 55:
            score += scoring['gender']['male>55']
        elif self.user.gender == 'female' and self.user.age > 65:
            score += scoring['gender']['female>65']
        elif self.user.activity_level:
            score += scoring['activity'][self.user.activity_level]
        elif self.user.has_smoking_habit:
            score += scoring['smoker'][self.user.has_smoking_habit]
        elif self.user.alcohol:
            score += scoring['alcohol'][self.user.alcohol]
        elif self.user.has_parents_hypertension:
            score += scoring['parents hypertension']
        elif self.user.bmi > 30:
            score += scoring['bmi']['30>']
        elif 25 < self.user.bmi < 30:
            score += scoring['bmi']['25-30']
        elif self.user.heart_beat_per_sec > 80:
            score += scoring['heart beat']['80>']
        elif self.user.has_diabetes:
            score += scoring['diabetes']
        elif self.user.has_high_blood_pressure:
            score += scoring['high bp']
        # highest score is 59
        return score

    def recommendations(self):
        score = self.score()
        if score > 30:
            print('bad')
        if self.user.activity_level != 'severe':
            print('run')

