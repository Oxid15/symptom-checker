from user_model import UserModel
from diabetes_model import DiabetesModel
from hypertension_model import HypertensionModel


class SymptomChecker:
    def __init__(self):
        self._hypertension_model = HypertensionModel()
        self._diabetes_model = DiabetesModel()

    def check(self, user: UserModel) -> str:
        if user.age < 18:
            return 'no children'

        hyper = self._hypertension_model.symptoms(user)
        diab = self._diabetes_model.symptoms(user)

        if hyper:
            return self._hypertension_model.recommendations(user)
        elif diab:
            return self._diabetes_model.recommendations(user)
        else:
            return "there's nothing wrong with you"
