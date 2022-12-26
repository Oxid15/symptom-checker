from user_model import UserModel
from utils import bmi as bmi_func
from scipy.spatial import distance


class HypertensionModel:
    def analysis(self, user: UserModel):
        #  Array to hold state
        FINAL = []

        # [ 1, 2, 3 & 4, 5, 6, 7 & 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

        # The Ideal Scenario for Hypertension
        HYPER_VECTOR = [ 2, 0,     2, 1, 2,     2, 2,  2,  1,  0,  1,  0,  1,  1,  0,  3,  3]  # Symptom Vector
        # [ 1,        1,  , 1,     1, 1,  1,                              2,  2] - # op 2
        # [                                                               1,  1] - # op 3

        # 1
        # Age Based
        if user.age >= 55 and user.age <= 64:
            FINAL.append(1)
        elif user.age >= 65:
            FINAL.append(2)
        else:
            FINAL.append(0)

        # 2
        # Gender, regardless of Men or Women, both are prone to HP & Diabetes
        # When Pregnant, the Blood pressure of Women is lower. hence the risk to HP is variable
        if user.gender == 'Female' and user.is_pregnant:
            FINAL.append(1)

        # 3 & 4
        # Weight & Height

        w = user.weight
        h = user.height

        # underweight = 2
        # overweight = 1
        # normal = 0

        # Underweight Conditions
        if (h < 160 and w < 45 or
            h > 161 and h < 170 and w > 46 and w < 52 or
            h > 171 and h < 180 and w > 53 and w < 60 or
            h > 181 and h < 190 and w > 61 and w < 65 or
            h > 191 and w > 72):
            FINAL.append(2)

        # Overweight Conditions
        elif (h < 160 and w < 70 or
              h > 161 and h < 170 and w > 71 and w < 81 or
              h > 171 and h < 180 and w > 82 and w < 95 or
              h > 181 and h < 190 and w > 96 and w < 110 or
              h > 191 and w > 111):
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 5
        # BMI

        # low = 0
        # high = 1

        bmi = bmi_func(user)

        if bmi >= 25.1:
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 6
        # Activity Level

        act = user.activity_level

        if act == 'Occasional (<30 mins a week)':
            FINAL.append(2)

        if act == 'Light Exercise (30 - 90 mins a Week)':
            FINAL.append(1)

        if act == 'Active (> 120 mins a Week)':
            FINAL.append(0)

        # 7 & 8
        # Smoking & Alcohol

        if user.has_smoking_habit and user.has_alcohol_habit:
            FINAL.append(2)
        elif user.has_smoking_habit or user.has_alcohol_habit: 
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 9 Diabetes & Hypertension

        if user.has_art_hypertension:
            FINAL.append(2)
        elif user.has_diabetes:
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 10 Diabetes & Hypertension of parents

        if user.has_parents_hypertension:
            FINAL.append(2)
        elif user.has_parents_diabetes:
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 11

        if user.has_burning_sensation:
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 12

        if user.has_lose_weight:
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 13

        if user.has_thirst_morning_night:
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 14

        if user.has_freq_urination:
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 15

        if user.has_nausea:
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 16

        if user.has_faintness:
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 17

        if user.has_poor_wound_healing:
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 18

        if user.has_impaired_vision:
            if user.impaired_vision_duration == 'Less than 1 Day':
                FINAL.append(2)
            elif user.impaired_vision_duration == '1 Day to 1 Week':
                FINAL.append(3)
            elif user.impaired_vision_duration == '1 Week to 1 Month' :
                FINAL.append(1)
            else:
                FINAL.append(0)
        else:
            FINAL.append(0)

        # 19

        if user.has_pain_in_leg:
            if user.pain_in_leg_intensiy == 'Mild':
                FINAL.append(1)
            elif user.pain_in_leg_intensiy == 'Moderate':
                FINAL.append(2)
            elif user.pain_in_leg_intensiy == 'Severe':
                FINAL.append(3)
        else:
            FINAL.append(0)

        # Calculating the Spatial Difference between the User Vector & Symptom Vector
        SS = distance.hamming(HYPER_VECTOR, FINAL)
        ANS = 1.0 - SS

        return ANS

    def recommendations(self, user: UserModel) -> str:
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

        if user.gender == 'Female' and user.is_pregnant:
            recommend.append("Hypertension and its associated complications still remain one of the main causes "
                             "of morbidity and mortality of the mother, fetus and newborn."
                             "Consult your doctor as soon as possible, as it may be vital for your "
                             "and your child's health.")

        recommend.append("However, the crucial effects of hypertension can be reduced with simple recommendations:"
                         "\nAdd more vegetables to your diet, and decrease the amount of animal fats. "
                         "Food rich in potassium and calcium (vegetables, fruits, cereals), and magnesium "
                         "(dairy products) should be added to your daily ration. "
                         "\nReduce the consumption of table salt to 5 g/day. "
                         "\nLimit consumption of coffee and other caffeine-rich products, "
                         "as caffeine increases blood pressure .")

        if user.activity_level != 'active':
            recommend.append("Add aerobic physical activity for 30-40 minutes at least 4 times a week."
                             "Regular exercise can reduce blood pressure.")

        if user.has_smoking_habit:
            recommend.append("Smoking has a negative impact on your condition; "
                             "however, quitting will help you feel better.")

        if bmi > 25:
            recommend.append("Maintain a healthy body mass index (BMI < 25 kg/m2)."
                             "Remember that a small amount of weight loss may still be beneficial, and a larger "
                             "amount will have advantageous metabolic impact in the long term.")

        if user.has_alcohol_habit:
            recommend.append("Limit alcohol consumption. This can reduce blood pressure and has broader health benefits.")
            if user.gender == 'Male':
                recommend.append("14 units per week is okay (1 unit is about 125 ml of wine or 230 ml of beer)")
            else:
                recommend.append("7 units per week is okay (1 unit is about 125 ml of wine or 230 ml of beer)")

        if user.has_diabetes:
            recommend.append("Increase physical activity and opt for a low-calorie diet with limiting the consumption "
                             "of table salt. Reducing body weight for patients with hypertension and diabetes helps to "
                             "reduce blood pressure and increase tissue sensitivity to insulin.")

        if user.age < 55 and user.gender == 'female':
            recommend.append("Young women who take oral contraceptives should also monitor their "
                             "blood pressure even when they feel well.")

        recommend.append("Hypertension may occur even with a healthy lifestyle. The cause may be heredity. "
                         "But sometimes secondary hypertension develops due to the pathology of the "
                         "endocrine system or kidneys, which are involved in pressure control."
                         "\nWe recommend you to visit the doctor, as hypertension is usually diagnosed by accident. "
                         "The earlier the therapy starts, the higher the probability that drugs would not be necessary "
                         "for you. Before your visit to the cardiologist, you can track your blood pressure for a week. "
                         "For that measure your blood pressure at rest every morning and evening and when you feel bad. "
                         "Do not measure the pressure immediately after eating or exercising. "
                         "\nThe main purpose of hypertension therapy is not only to reduce pressure, but to protect the "
                         "heart, kidneys, blood vessels, brain – target organs that can suffer from untreated high pressure.")

        return '\n\n'.join(recommend)
