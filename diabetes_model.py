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
                     "The most important element of diabetes therapy is changing eating habits and lifestyle. "
                     "In some people diagnosed with prediabetes, changes in diet and sports can reduce blood glucose "
                     "levels and prevent the development of the disease.", ]

        if bmi > 25:
            recommend.append("It is recommended to limit the caloric content of the diet to all overweight patients "
                             "with diabetes in order to moderate weight loss. Maximum restriction of fats "
                             "(primarily of animal origin) and sugars is necessary; "
                             "\nmoderate restriction - products consisting mainly of complex carbohydrates (starches) and proteins; "
                             "\nunlimited consumption – products with minimal calories (mainly vegetables rich in water and fiber).")

        recommend.append("It is recommended to consume carbohydrates in vegetables, whole grains, dairy products, "
                         "as opposed to other sources of carbohydrates containing additionally saturated fats or "
                         "trans fats, sugars or salt. It is also important to include foods rich in mono- and "
                         "polyunsaturated fatty acids (fish, vegetable oils) in the diet."
                         "\nAlcohol drinking should be limited to 1 unit for women and 2 units for men per day to prevent "
                         "hypoglycemia. One unit corresponds to 15 g of ethanol, or about 40 g of spirits, or 140 g of wine, or 300 g of beer. ")

        if user.gender == 'female' and user.is_pregnant:
            recommend.append('Gestational diabetes is a condition in which a woman without diabetes develops high blood '
                            'sugar levels during pregnancy. The child and the mother who has undergone gestational '
                            'diabetes should monitor the level of sugar to prevent type 2 diabetes. Long term, children'
                            ' are at higher risk of being overweight and of developing type 2 diabetes.')

        return '\n'.join(recommend)
