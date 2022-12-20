from typing import Literal


class UserModel:
    name: str
    age: int
    gender: Literal['male', 'female']
    has_pregnancy: bool
    height: int  # cm
    weight: int  # kg
    activity_level: Literal['mild', 'moderate', 'active']
    has_smoking_habit: bool

    has_art_hypertension: bool
    has_burning_sensation: bool
    has_lose_weight: bool
    has_appetite_increase: bool
    has_freq_urination: bool
    has_nausea: bool
    has_faintness: bool
    has_thirst_morning_night: bool
    has_poor_wound_healing: bool

    has_diabetes: bool
    has_parents_diabetes: bool
    has_high_blood_pressure: bool
    has_furunculosis: bool
    has_candidiasis: bool
    has_exc_physical_activity: bool

    has_impaired_vision: bool
    impaired_vision_duration: Literal  # options?

    has_pain_in_leg: bool
    pain_in_leg_intensity: Literal['mild', 'moderate', 'severe']

    has_headache: bool
    headache_location: Literal  # options?
    headache_duration: Literal  # options?
    headache_intensity:  Literal['mild', 'moderate', 'severe']

    has_dizziness: bool
    dizziness_duration: Literal  # options?
    dizziness_intensity:  Literal['mild', 'moderate', 'severe']
    dizziness_interferes: bool
