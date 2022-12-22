from typing import Literal, Union


Duration = Literal['<1 day', '1 day to 1 week', '1 week to 1 month', '1 month to 1 year', None]
Intensity = Literal['mild', 'moderate', 'severe', None]


class UserModel:
    def __init__(self):
        self.name: str

        self.age: int
        self.gender: str
        self.is_pregnant: bool

        self.weight: int
        self.height: int
        self.activity_level: Literal['mild', 'moderate', 'active']

        self.has_smoking_habit: bool
        self.has_alcohol_habit: bool

        self.has_art_hypertension: bool
        self.has_parents_hypertension: bool
        self.has_burning_sensation: bool
        self.has_lose_weight: bool
        self.has_appetite_increase: bool
        self.has_freq_urination: bool
        self.has_nausea: bool
        self.has_faintness: bool
        self.has_thirst_morning_night: bool
        self.has_poor_wound_healing: bool

        self.has_diabetes: bool
        self.has_parents_diabetes: bool
        self.has_high_blood_pressure: bool
        self.has_furunculosis: bool
        self.has_candidiasis: bool
        self.has_exc_physical_activity: bool

        self.has_impaired_vision: bool
        self.impaired_vision_duration: Duration

        self.has_pain_in_leg: bool
        self.pain_in_leg_intensity: Intensity

        self.has_headache: bool
        self.headache_location: Literal['left', 'right', 'both', 'center', None]
        self.headache_duration: Duration
        self.headache_intensity: Intensity

        self.has_dizziness: bool
        self.dizziness_duration: Duration
        self.dizziness_intensity: Intensity
        self.dizziness_interferes: bool

    def __str__(self) -> str:
        return str(self.__dict__)
