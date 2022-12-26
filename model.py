from user_model import UserModel
from diabetes_model import DiabetesModel
from hypertension_model import HypertensionModel


class SymptomChecker:
    def __init__(self):
        self._hypertension_model = HypertensionModel()
        self._diabetes_model = DiabetesModel()

    def check(self, user: UserModel) -> str:
        if user.age < 18:
            return "Unfortunately, This Symptom Checker is Specifically Designed for Adults above the age of 18. We recommend visiting a General Practitioner or A Pediatrician if its Urgent."

        hyper = self._hypertension_model.symptoms(user)
        diab_type1 = self._diabetes_model.symptoms_type1(user)
        diab_type2 = self._diabetes_model.symptoms_type2(user)
        
        
        if hyper <0.3:
            return "Based on your Symptoms, Our Diagnosis suggests that you might be sufferring from Hypertension as you have a ", hyper,"% match to the criterias required to have Hypertension", "Please note this is a Diagnosis and not an Actual Pracitioners report, hence, If you feel the need, please consult a General Practitioner or Seek Emergency help As soon as possible.", "Here are a few recommendations on How to deal with Hypertension" , self._hypertension_model.recommendations(user)
        elif diab_type2 < 0.3:
            return "Based on your Symptoms, Our Diagnosis suggests that you might be sufferring from Diabetes Type 2 as you have a ", hyper,"% match to the criterias required to have Type 2 Diabetes", "Please note this is a Diagnosis and not an Actual Pracitioners report, hence, If you feel the need, please consult a General Practitioner or Seek Emergency help As soon as possible.", "Here are a few recommendations on How to deal with Hypertension", self._diabetes_model.recommendations(user)
        elif diab_type2 < 0.3 and hyper <0.3:
            return "Based on your Symptoms, Our Diganosis suggests that you might be sufferrring from Both hypertension & Diabetes Type 2 as you had a ", hyper,"% & ",diab, "% match to the criterias required to have Hypertension & Diabetes type 2 Respectively" 
        elif diab_type1 < 0.3:
            return "Diabetes type1" 
        elif diab_type1 < 0.3 and hyper <0.3:
            return "Diabetes type1 and hypertension"
        else:
            return "Hmmm.... From the Symptoms you provided, it Seems though you might not be sufferring from either Hypertension or Diabetes. In case, your Symptoms start to get aggrevated over time, It is best to seek Medical Attenton as soon as possible."  # We need to come up with some answer for this case also
