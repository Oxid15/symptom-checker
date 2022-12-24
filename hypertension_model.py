from user_model import UserModel
from utils import bmi as bmi_func


class HypertensionModel:
    def symptoms(self, user: UserModel):
        bmi = bmi_func(user)
        if user.gender == 'male':
            if (user.age > 55 or
                    user.has_smoking_habit or
                    user.has_alcohol_habit == 'every day' or
                    user.activity_level == 'mild' or
                    user.has_parents_hypertension or
                    bmi > 25 or
                    # user.heart_beat_per_sec > 80 or
                    user.has_high_blood_pressure or
                    user.has_diabetes):
                return True
        else:
            if (user.age > 65 or
                    user.has_smoking_habit or
                    user.has_alcohol_habit == 'every day' or
                    user.activity_level == 'mild' or
                    user.has_parents_hypertension or
                    bmi > 25 or
                    # user.heart_beat_per_sec > 80 or
                    user.has_high_blood_pressure or
                    user.has_diabetes):
                return True

    def score(self, user: UserModel):
        bmi = bmi_func(user)

        scoring = {
            'gender': {'male>55': 6, 'female>65': 3, 'female': 0, 'male': 0},
            'alcohol': {'every day': 8, 'once a week': 2, 'on holidays': 0, 'quit': 0, 'no': 0},  # todo
            'smoker': {'a lot': 5, 'quit': 0, 'no': 0},  # todo
            'activity': {'mild': 5, 'moderate': 1, 'active': 0},
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
        bmi = bmi_func(user)
        # print relevant symptoms before recommendations

        recommend = ["You may have hypertension. Hypertension is a condition in which a person's blood pressure becomes "
                     "higher than 140/90 mmHg. High blood pressure is the main risk factor for cardiovascular diseases "
                     "(such as heart attack), cerebrovascular diseases (ischemic stroke), kidney diseases. "
                     "High blood pressure is the cause of almost 10 million deaths and "
                     "more than 200 million cases of disability in the world.", ]

        # other recommendations are appended if there is such a symptom

        if user.age < 55:
            recommend.append("An increase in blood pressure in middle age is associated with the development of "
                             "cognitive impairment and dementia in old age. Intensive therapy of hypertension "
                             "reduces the risks of cognitive impairment and dementia.")

        if user.gender == 'female' and user.is_pregnant:
            recommend.append("Hypertension and its associated complications still remain one of the main causes "
                             "of morbidity and mortality of the mother, fetus and newborn.")

        recommend.append("However, the crucial effects of hypertension can be reduced with simple recommendations:"
                         "\nAdd more vegetables to your diet, and decrease the amount of animal fats. "
                         "Food rich in potassium and calcium (vegetables, fruits, cereals), and magnesium "
                         "(dairy products) should be added to your daily ration. "
                         "\nReduce the consumption of table salt to 5 g/day. ")

        if user.activity_level != 'active':
            recommend.append("Add regular aerobic physical activity for 30-40 minutes at least 4 times a week.")

        if user.has_smoking_habit:
            recommend.append("Quit smoking.")

        if bmi > 25:
            recommend.append("Normalize your body mass (BMI < 25 kg/m2)")

        if user.has_alcohol_habit:
            recommend.append("limit alcohol consumption:")
            if user.gender == 'male':
                recommend.append("14 units per week (1 unit is about 125 ml of wine or 230 ml of beer)")
            else:
                recommend.append("7 units per week (1 unit is about 125 ml of wine or 230 ml of beer)")

        if user.has_diabetes:
            recommend.append("Increase physical activity and opt for a low-calorie diet with limiting the consumption "
                             "of table salt. Reducing body weight for patients with hypertension and diabetes helps to "
                             "reduce blood pressure and increase tissue sensitivity to insulin.")

        if user.age < 55 and user.gender == 'female':
            recommend.append("Young women who take oral contraceptives should also monitor their "
                             "blood pressure even when they feel well.")

        recommend.append("Hypertension may occur even with a healthy lifestyle. The cause may be heredity. "
                         "But sometimes secondary hypertension develops – due to the pathology of the "
                         "endocrine system or kidneys, which are involved in pressure control."
                         "\nWe recommend you to visit the doctor, as hypertension is usually diagnosed by accident. "
                         "The earlier the therapy starts, the higher the probability that drugs would not be necessary "
                         "for you. Before your visit to the cardiologist, you can track your blood pressure for a week. "
                         "For that measure your blood pressure at rest every morning and evening and when you feel bad. "
                         "\nThe main purpose of hypertension therapy is not to reduce pressure, but to protect the "
                         "heart, kidneys, blood vessels, brain – target organs that can suffer from untreated high pressure.")

        return '\n\n'.join(recommend)
