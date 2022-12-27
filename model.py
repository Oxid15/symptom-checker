from typing import List
from user_model import UserModel
from diabetes_model import DiabetesModel
from hypertension_model import HypertensionModel


THRESHOLD = 0.60


class SymptomChecker:
    def __init__(self):
        self._hypertension_model = HypertensionModel()
        self._diabetes_model = DiabetesModel()

    def _report(self, diseases: List[str], scores: List[float]) -> str:
        name = ', '.join(diseases[:-1]) + ' and ' + diseases[-1]
        score = sum(scores) / len(scores)
        return (
                f'Based on your Symptoms, Our Diagnosis suggests that you might be sufferring '
                f'from {name} as you have a {score * 100: 0.2f}% match to the '
                f'criterias required '
                f'to have {name}'
                f'\nPlease note this is a Diagnosis and not an Actual Pracitioners report, hence '
                f'If you feel the need, please consult a General Practitioner or Seek Emergency '
                f'help As soon as possible.\nHere are a few recommendations on How to deal '
                f'with {name}\n\n')

    def check(self, user: UserModel) -> List[str]:
        if user.age < 18:
            return [
                'Unfortunately, This Symptom Checker is Specifically Designed for Adults above '
                'the age of 18. We recommend visiting a General Practitioner or A Pediatrician '
                'if its Urgent.']

        hyper = self._hypertension_model.analysis(user)
        diab_type_1 = self._diabetes_model.symptoms_type1(user)
        diab_type_2 = self._diabetes_model.symptoms_type2(user)

        if diab_type_1 > diab_type_2:
            diab = diab_type_1
            diab_disease = 'Diabetes type 1'
        else:
            diab = diab_type_2
            diab_disease = 'Diabetes type 2'

        print("Hyper = ", hyper)
        print("diab 1 = ", diab_type_1)
        print("diab 2 = ", diab_type_2)

        diseases = []
        scores = []
        recs = []

        if hyper > THRESHOLD:
            r = self._hypertension_model.recommendations(user)
            diseases.append('Hypertension')
            scores.append(hyper)
            recs.append(r)
        if diab > THRESHOLD:
            r = self._diabetes_model.recommendations(user)
            diseases.append(diab_disease)
            scores.append(diab)
            recs.append(r)
        if len(diseases) == 0:
            return [
                'Hmmm.... From the Symptoms you provided, it Seems though you might not be '
                'sufferring from either Hypertension or Diabetes. In case, your Symptoms '
                'start to get aggrevated over time, It is best to seek Medical Attenton '
                'as soon as possible.'
            ]
        else:
            return [self._report(diseases, scores)] + recs
