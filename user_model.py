from typing import Literal


class UserModel:
    def __init__(self):
        # todo blood pressure measures?

        self.name: str = None

        self.age: int = None
        self.gender: str = None
        self.is_pregnant: bool = None

        self.weight: int = None
        self.height: int = None
        self.bmi: float = self.weight / (self.height / 100) ** 2  # kg/m
        self.activity_level: Literal['mild', 'moderate', 'active'] = None

        # if user quit this year but was a strong smoker they're in risk too
        self.has_smoking_habit: Literal['every hour', 'no', 'quit', 'from time to time'] = None
        self.alcohol: Literal['every day', 'once a week', 'on holidays', 'no', 'quit'] = None

        self.has_art_hypertension: bool = None
        self.has_parents_hypertension: bool = None
        self.heart_beat_per_sec: int = None
        self.has_burning_sensation: bool = None
        self.has_lose_weight: bool = None
        self.has_appetite_increase: bool = None
        self.has_freq_urination: bool = None
        self.has_nausea: bool = None
        self.has_faintness: bool = None
        self.has_thirst_morning_night: bool = None
        self.has_poor_wound_healing: bool = None

        self.has_diabetes: bool = None
        self.has_parents_diabetes: bool = None
        self.has_high_blood_pressure: bool = None
        self.has_furunculosis: bool = None
        self.has_candidiasis: bool = None
        self.has_exc_physical_activity: bool = None

        self.has_impaired_vision: bool = None
        self.impaired_vision_duration: Literal = None  # options?

        self.has_pain_in_leg: bool = None
        self.pain_in_leg_intensity: Literal = None

        self.has_headache: bool = None
        self.headache_location: Literal = None  # options?
        self.headache_duration: Literal = None  # options?
        self.headache_intensity: Literal['mild', 'moderate', 'severe'] = None

        self.has_dizziness: bool = None
        self.dizziness_duration: Literal = None  # options?
        self.dizziness_intensity: Literal['mild', 'moderate', 'severe'] = None
        self.dizziness_interferes: bool = None


