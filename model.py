from user_model import UserModel
from diabetes_model import Diabetes
from hypertension_model import Hypertension


class SymptomChecker:
    def __init__(self):
        self.user = UserModel()
        self.hypertension = Hypertension()
        self.diabetes = Diabetes()

    def model(self):
        if self.user.age < 18:
            print('not suitable for children')

        hyper = self.hypertension.symptoms()
        diab = self.diabetes.symptoms()

        if hyper:
            self.hypertension.recommendations()
        elif diab:
            self.diabetes.recommendations()
        else:
            print("there's nothing wrong with you")
