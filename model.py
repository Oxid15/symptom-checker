from user_model import UserModel
from diabetes_model import Diabetes
from hypertension_model import Hypertension


class SymptomChecker:
    def __init__(self):
        self._hypertension_model = Hypertension()
        self._diabetes_model = Diabetes()

    def check(self, user: UserModel) -> str:
        if user.age < 18:
            return 'no children'

        hyper = self._hypertension_model.symptoms()
        diab = self._diabetes_model.symptoms()

        if hyper:
            return self._hypertension_model.recommendations()
        elif diab:
            return self._diabetes_model.recommendations()
        else:
            return "there's nothing wrong with you"
