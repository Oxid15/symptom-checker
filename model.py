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
        diab = self._diabetes_model.symptoms(user)

        if hyper:
            return self._hypertension_model.recommendations(user)
        elif diab:
            return self._diabetes_model.recommendations(user)
        else:
            return 'The system was not able to diagnose you with anything'  # We need to come up with some answer for this case also
