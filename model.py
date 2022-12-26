from user_model import UserModel
from diabetes_model import DiabetesModel
from hypertension_model import HypertensionModel


class SymptomChecker:
    def __init__(self):
        self._hypertension_model = HypertensionModel()
        self._diabetes_model = DiabetesModel()

    def _report(self, disease: str, score: float) -> str:
        return (
                f'Based on your Symptoms, Our Diagnosis suggests that you might be sufferring'
                f'from {disease} as you have a, {score * 100}% match to the criterias required'
                f'to have {disease}'
                f'\nPlease note this is a Diagnosis and not an Actual Pracitioners report, hence'
                f'If you feel the need, please consult a General Practitioner or Seek Emergency'
                f'help As soon as possible.\n Here are a few recommendations on How to deal'
                'with {disease}\n')

    def check(self, user: UserModel) -> str:
        if user.age < 18:
            return "Unfortunately, This Symptom Checker is Specifically Designed for Adults above the age of 18. We recommend visiting a General Practitioner or A Pediatrician if its Urgent."

        hyper = self._hypertension_model.analysis(user)

        diab = 0
        # diab = self._diabetes_model.symptoms(user)

        if hyper > diab:
            return self._report('Hypertension', hyper)
        elif diab < hyper:
            return self._report('Diabetes type 2', diab)
        elif diab > 0.80 and hyper > 0.80:
            return self._report('Diabetes type 2 and Hypertension', (diab + hyper) / 2)
        else:
            return (
                'Hmmm.... From the Symptoms you provided, it Seems though you might not be'
                'sufferring from either Hypertension or Diabetes. In case, your Symptoms '
                'start to get aggrevated over time, It is best to seek Medical Attenton'
                'as soon as possible.'
            )
