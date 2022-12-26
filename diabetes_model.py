from user_model import UserModel
from utils import bmi as bmi_func
from scipy.spatial import distance


class DiabetesModel:
    def symptoms_type1(self, user: UserModel):
        #  Array to hold state
        FINAL = []

        # [ 1, 2, 3 & 4, 5, 6, 7 & 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

        # The Ideal Scenario for Diabetes
        DIA_VECTOR = [1, 0, 2, 1, 2, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 3, 3]  # Symptom Vector

        # 1
        # Age Based
        if user.age >= 18 and user.age <= 45:
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 2
        # Gender, regardless of Men or Women, both are prone to HP & Diabetes
        if user.gender == 'Female' and user.is_pregnant:
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 3 & 4
        # Weight & Height

        w = user.weight
        h = user.height

        # underweight = 1
        # overweight = 2
        # normal = 0

        # Underweight Conditions
        if (h < 160 and w < 45 or
            h > 161 and h < 170 and w > 46 and w < 52 or
            h > 171 and h < 180 and w > 53 and w < 60 or
            h > 181 and h < 190 and w > 61 and w < 65 or
            h > 191 and w > 72):
            FINAL.append(1)

        # Overweight Conditions
        elif (h < 160 and w < 70 or
              h > 161 and h < 170 and w > 71 and w < 81 or
              h > 171 and h < 180 and w > 82 and w < 95 or
              h > 181 and h < 190 and w > 96 and w < 110 or
              h > 191 and w > 111):
            FINAL.append(2)
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

        if act == 'Occasional (<30 mins a Week)':
            FINAL.append(2)
        elif act == 'Light Exercise (30 - 90 mins a Week)':
            FINAL.append(1)
        elif act == 'Active (> 120 mins a Week)':
            FINAL.append(0)
        else:
            RuntimeError(f'got {act}')

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
            FINAL.append(1)
        elif user.has_diabetes:
            FINAL.append(2)
        else:
            FINAL.append(0)

        # 10 Diabetes & Hypertension of parents

        if user.has_parents_hypertension:
            FINAL.append(1)
        elif user.has_parents_diabetes:
            FINAL.append(2)
        else:
            FINAL.append(0)

        # 11

        if user.has_burning_sensation:
            FINAL.append(0)
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
            FINAL.append(0)
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
        SS = distance.hamming(DIA_VECTOR, FINAL)
        ANS = 1.0 - SS

        return ANS

    def symptoms_type2(self, user: UserModel):
        #  Array to hold state
        FINAL = []

        # [ 1, 2, 3 & 4, 5, 6, 7 & 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

        # The Ideal Scenario for Diabetes
        DIA_VECTOR = [1, 0, 2, 1, 2, 2, 2, 2, 0, 0, 0, 1, 0, 1, 1, 3, 3]  # Symptom Vector

        # 1
        # Age Based
        if user.age >= 45:
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 2
        # Gender, regardless of Men or Women, both are prone to HP & Diabetes
        if user.is_pregnant:
            FINAL.append(1)
        else:
            FINAL.append(0)

        # 3 & 4
        # Weight & Height

        w = user.weight
        h = user.height

        # underweight = 1
        # overweight = 2
        # normal = 0

        # Underweight Conditions
        if (h < 160 and w < 45 or
            h > 161 and h < 170 and w > 46 and w < 52 or
            h > 171 and h < 180 and w > 53 and w < 60 or
            h > 181 and h < 190 and w > 61 and w < 65 or
            h > 191 and w > 72):
            FINAL.append(1)

        # Overweight Conditions
        elif (h < 160 and w < 70 or
              h > 161 and h < 170 and w > 71 and w < 81 or
              h > 171 and h < 180 and w > 82 and w < 95 or
              h > 181 and h < 190 and w > 96 and w < 110 or
              h > 191 and w > 111):
            FINAL.append(2)
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

        if act == 'Occasional (<30 mins a Week)':
            FINAL.append(2)
        elif act == 'Light Exercise (30 - 90 mins a Week)':
            FINAL.append(1)
        elif act == 'Active (> 120 mins a Week)':
            FINAL.append(0)
        else:
            raise RuntimeError(f'got {act}')

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
            FINAL.append(1)
        elif user.has_diabetes:
            FINAL.append(2)
        else:
            FINAL.append(0)

        # 10 Diabetes & Hypertension of parents

        if user.has_parents_hypertension:
            FINAL.append(1)
        elif user.has_parents_diabetes:
            FINAL.append(2)
        else:
            FINAL.append(0)

        # 11

        if user.has_burning_sensation:
            FINAL.append(0)
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
            FINAL.append(0)
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
        SS = distance.hamming(DIA_VECTOR, FINAL)
        ANS = 1.0-SS

        return ANS

    def recommendations(self, user: UserModel) -> str:

        bmi = bmi_func(user)

        recommend = ["You may have diabetes of type 2. This form of diabetes is characterized by high blood sugar, "
                     "insulin resistance, and relative lack of insulin. In this situation you should definitely visit "
                     "the doctor, as diabetes can be diagnosed only with laboratory tests."
                     "You may be facing prediabetes now, which is characterized by elevated blood sugar levels that "
                     "fall below the threshold to diagnose diabetes."
                     "\nUsually, diabetes is detected by accident while examining a patient with concomitant diseases "
                     "(obesity, coronary heart disease, arterial hypertension, gout, polycystic ovaries). "
                     "Abdominal obesity is the main risk factor for diabetes of type 2 and is largely the cause of "
                     "the observed insulin resistance. With insulin resistance, the body produces a lot of this hormone,"
                     " but the tissues have a reduced sensitivity to its effects. "
                     "\nThe most important element of diabetes therapy is changing eating habits and lifestyle. "
                     "In some people diagnosed with prediabetes, changes in diet and sports can reduce blood glucose "
                     "levels and prevent the development of the disease.", ]

        if bmi > 25:
            recommend.append("It is recommended to limit the caloric content of the diet to all overweight patients "
                             "with diabetes in order to moderate weight loss. Maximum restriction of fats "
                             "(primarily of animal origin) and sugars is necessary; "
                             "\nmoderate restriction - products consisting mainly of complex carbohydrates (starches) and proteins; "
                             "\nunlimited consumption – products with minimal calories (mainly vegetables rich in water and fiber)."
                             "Remember that a small amount of weight loss may still be beneficial, and a larger "
                             "amount will have advantageous metabolic impact in the long term.")

        recommend.append("It is recommended to consume carbohydrates in vegetables, whole grains, dairy products, "
                         "as opposed to other sources of carbohydrates containing additionally saturated fats or "
                         "trans fats, sugars or salt. It is also important to include foods rich in mono- and "
                         "polyunsaturated fatty acids (fish, vegetable oils) in the diet."
                         "\nAlcohol drinking should be limited to 1 unit for women and 2 units for men per day to prevent"
                         " hypoglycemia. One unit corresponds to 15 g of ethanol, or 125 ml of wine, or 230 ml of beer.")

        if user.gender == 'female' and user.is_pregnant:
            recommend.append('Gestational diabetes is a condition in which a woman without diabetes develops high blood '
                            'sugar levels during pregnancy. The child and the mother who has undergone gestational '
                            'diabetes should monitor the level of sugar to prevent type 2 diabetes. Long term, children'
                            ' are at higher risk of being overweight and of developing type 2 diabetes.')

        if user.has_high_blood_pressure:
            recommend.append("Try to track your blood pressure for a week. For that measure your blood pressure "
                             "at rest every morning and evening and when you feel bad. "
                             "Do not measure the pressure immediately after eating or exercising. "
                             "Share your observations with your doctor. ")

        recommend.append("Visit your doctor as fast as you can. It may be crucial for your health.")

        return '\n\n'.join(recommend)
