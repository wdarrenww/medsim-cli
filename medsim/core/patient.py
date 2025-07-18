"""
Enhanced Patient Simulation
provides rich patient profiles with personality, emotions, and social determinants
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import random
import json
from datetime import datetime, date

class EmotionalState(Enum):
    """patient emotional states"""
    CALM = "calm"
    ANXIOUS = "anxious"
    FEARFUL = "fearful"
    ANGRY = "angry"
    DEPRESSED = "depressed"
    CONFUSED = "confused"
    COOPERATIVE = "cooperative"
    UNCOOPERATIVE = "uncooperative"

class PersonalityType(Enum):
    """patient personality types"""
    TYPE_A = "type_a"  # competitive, time-conscious
    TYPE_B = "type_b"  # relaxed, patient
    INTROVERT = "introvert"
    EXTROVERT = "extrovert"
    ANALYTICAL = "analytical"
    EMOTIONAL = "emotional"

class SocialDeterminant(Enum):
    """social determinants of health"""
    POVERTY = "poverty"
    FOOD_INSECURITY = "food_insecurity"
    HOUSING_INSECURITY = "housing_insecurity"
    TRANSPORTATION_BARRIERS = "transportation_barriers"
    HEALTH_LITERACY = "health_literacy"
    LANGUAGE_BARRIERS = "language_barriers"
    DISCRIMINATION = "discrimination"
    SOCIAL_ISOLATION = "social_isolation"

@dataclass
class FamilyHistory:
    """family medical history"""
    conditions: List[str] = field(default_factory=list)
    age_of_onset: Dict[str, int] = field(default_factory=dict)
    deceased_relatives: List[str] = field(default_factory=list)
    cause_of_death: Dict[str, str] = field(default_factory=dict)

@dataclass
class SocialHistory:
    """social history and determinants"""
    occupation: Optional[str] = None
    education_level: Optional[str] = None
    marital_status: Optional[str] = None
    living_situation: Optional[str] = None
    insurance_status: Optional[str] = None
    primary_language: str = "English"
    social_determinants: List[SocialDeterminant] = field(default_factory=list)
    support_system: List[str] = field(default_factory=list)
    barriers_to_care: List[str] = field(default_factory=list)

@dataclass
class LifestyleFactors:
    """lifestyle and behavioral factors"""
    smoking_status: str = "never"
    alcohol_use: str = "none"
    drug_use: str = "none"
    exercise_frequency: str = "moderate"
    diet_quality: str = "balanced"
    sleep_quality: str = "good"
    stress_level: str = "low"

@dataclass
class PatientPersonality:
    """patient personality and communication style"""
    personality_type: PersonalityType = PersonalityType.TYPE_B
    communication_style: str = "direct"
    health_literacy: str = "adequate"
    trust_in_healthcare: str = "moderate"
    decision_making_style: str = "collaborative"
    coping_mechanisms: List[str] = field(default_factory=list)
    cultural_background: str = "general"
    religious_preferences: Optional[str] = None

@dataclass
class EnhancedPatientProfile:
    """enhanced patient profile with rich data"""
    # basic demographics
    patient_id: str
    name: str
    age: int
    gender: str
    race_ethnicity: str
    date_of_birth: date
    
    # physical characteristics
    height: float  # cm
    weight: float  # kg
    bmi: float
    
    # medical information
    allergies: List[str] = field(default_factory=list)
    medications: List[Dict[str, Any]] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)
    surgeries: List[Dict[str, Any]] = field(default_factory=list)
    symptoms: List[str] = field(default_factory=list)
    lab_results: Dict[str, Any] = field(default_factory=dict)
    imaging_results: Dict[str, Any] = field(default_factory=dict)
    
    # enhanced components
    family_history: FamilyHistory = field(default_factory=FamilyHistory)
    social_history: SocialHistory = field(default_factory=SocialHistory)
    lifestyle_factors: LifestyleFactors = field(default_factory=LifestyleFactors)
    personality: PatientPersonality = field(default_factory=PatientPersonality)
    
    # emotional and cognitive state
    emotional_state: EmotionalState = EmotionalState.CALM
    cognitive_status: str = "alert"
    pain_level: int = 0  # 0-10 scale
    anxiety_level: int = 0  # 0-10 scale
    
    # communication preferences
    preferred_communication: str = "verbal"
    interpreter_needed: bool = False
    hearing_impairment: bool = False
    vision_impairment: bool = False
    
    def __post_init__(self):
        """calculate bmi and validate data"""
        if self.height > 0:
            self.bmi = self.weight / ((self.height / 100) ** 2)
    
    def get_age(self) -> int:
        """calculate current age"""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def update_emotional_state(self, new_state: EmotionalState):
        """update emotional state"""
        self.emotional_state = new_state
    
    def update_pain_level(self, level: int):
        """update pain level (0-10)"""
        self.pain_level = max(0, min(10, level))
    
    def update_anxiety_level(self, level: int):
        """update anxiety level (0-10)"""
        self.anxiety_level = max(0, min(10, level))
    
    def has_social_determinant(self, determinant: SocialDeterminant) -> bool:
        """check if patient has specific social determinant"""
        return determinant in self.social_history.social_determinants
    
    def get_risk_factors(self) -> List[str]:
        """get list of patient risk factors"""
        risk_factors = []
        
        # age-related risks
        if self.age > 65:
            risk_factors.append("elderly")
        elif self.age < 18:
            risk_factors.append("pediatric")
        
        # bmi-related risks
        if self.bmi >= 30:
            risk_factors.append("obesity")
        elif self.bmi < 18.5:
            risk_factors.append("underweight")
        
        # lifestyle risks
        if self.lifestyle_factors.smoking_status != "never":
            risk_factors.append("smoking")
        if self.lifestyle_factors.alcohol_use != "none":
            risk_factors.append("alcohol_use")
        
        # social determinant risks
        for determinant in self.social_history.social_determinants:
            risk_factors.append(determinant.value)
        
        return risk_factors
    
    def to_dict(self) -> Dict[str, Any]:
        """convert to dictionary for serialization"""
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "race_ethnicity": self.race_ethnicity,
            "date_of_birth": self.date_of_birth.isoformat(),
            "height": self.height,
            "weight": self.weight,
            "bmi": self.bmi,
            "allergies": self.allergies,
            "medications": self.medications,
            "conditions": self.conditions,
            "surgeries": self.surgeries,
            "family_history": {
                "conditions": self.family_history.conditions,
                "age_of_onset": self.family_history.age_of_onset,
                "deceased_relatives": self.family_history.deceased_relatives,
                "cause_of_death": self.family_history.cause_of_death
            },
            "social_history": {
                "occupation": self.social_history.occupation,
                "education_level": self.social_history.education_level,
                "marital_status": self.social_history.marital_status,
                "living_situation": self.social_history.living_situation,
                "insurance_status": self.social_history.insurance_status,
                "primary_language": self.social_history.primary_language,
                "social_determinants": [d.value for d in self.social_history.social_determinants],
                "support_system": self.social_history.support_system,
                "barriers_to_care": self.social_history.barriers_to_care
            },
            "lifestyle_factors": {
                "smoking_status": self.lifestyle_factors.smoking_status,
                "alcohol_use": self.lifestyle_factors.alcohol_use,
                "drug_use": self.lifestyle_factors.drug_use,
                "exercise_frequency": self.lifestyle_factors.exercise_frequency,
                "diet_quality": self.lifestyle_factors.diet_quality,
                "sleep_quality": self.lifestyle_factors.sleep_quality,
                "stress_level": self.lifestyle_factors.stress_level
            },
            "personality": {
                "personality_type": self.personality.personality_type.value,
                "communication_style": self.personality.communication_style,
                "health_literacy": self.personality.health_literacy,
                "trust_in_healthcare": self.personality.trust_in_healthcare,
                "decision_making_style": self.personality.decision_making_style,
                "coping_mechanisms": self.personality.coping_mechanisms,
                "cultural_background": self.personality.cultural_background,
                "religious_preferences": self.personality.religious_preferences
            },
            "emotional_state": self.emotional_state.value,
            "cognitive_status": self.cognitive_status,
            "pain_level": self.pain_level,
            "anxiety_level": self.anxiety_level,
            "preferred_communication": self.preferred_communication,
            "interpreter_needed": self.interpreter_needed,
            "hearing_impairment": self.hearing_impairment,
            "vision_impairment": self.vision_impairment
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedPatientProfile':
        """create from dictionary"""
        # convert date string back to date object
        if isinstance(data.get("date_of_birth"), str):
            data["date_of_birth"] = date.fromisoformat(data["date_of_birth"])
        
        # reconstruct nested objects
        if "family_history" in data:
            data["family_history"] = FamilyHistory(**data["family_history"])
        if "social_history" in data:
            social_data = data["social_history"]
            social_data["social_determinants"] = [
                SocialDeterminant(d) for d in social_data.get("social_determinants", [])
            ]
            data["social_history"] = SocialHistory(**social_data)
        if "lifestyle_factors" in data:
            data["lifestyle_factors"] = LifestyleFactors(**data["lifestyle_factors"])
        if "personality" in data:
            personality_data = data["personality"]
            personality_data["personality_type"] = PersonalityType(personality_data["personality_type"])
            data["personality"] = PatientPersonality(**personality_data)
        
        # convert emotional state
        if "emotional_state" in data:
            data["emotional_state"] = EmotionalState(data["emotional_state"])
        
        return cls(**data)

    @property
    def vitals(self) -> dict:
        # provide default vitals for simulation
        return {
            "blood_pressure_systolic": 120,
            "blood_pressure_diastolic": 80,
            "heart_rate": 80,
            "respiratory_rate": 16,
            "temperature": 98.6,
            "oxygen_saturation": 98
        }

class PatientProfileGenerator:
    """generates realistic patient profiles with pattern-driven logic"""
    
    def __init__(self):
        self.names = {
            "male": ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Christopher"],
            "female": ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"]
        }
        
        self.occupations = [
            "Teacher", "Nurse", "Engineer", "Salesperson", "Manager", "Technician", 
            "Administrative Assistant", "Retail Worker", "Driver", "Construction Worker"
        ]
        
        self.education_levels = [
            "High School", "Some College", "Bachelor's Degree", "Master's Degree", "Doctorate"
        ]
        
        self.marital_statuses = [
            "Single", "Married", "Divorced", "Widowed", "Separated"
        ]
        
        # specialty-specific demographics distributions
        self.specialty_demographics = {
            "emergency_medicine": {
                "age_ranges": [(18, 45), (45, 65), (65, 85)],
                "age_weights": [0.4, 0.4, 0.2],
                "gender_distribution": {"male": 0.52, "female": 0.48},
                "common_conditions": ["trauma", "cardiac", "respiratory", "neurological"]
            },
            "cardiology": {
                "age_ranges": [(45, 65), (65, 85), (85, 95)],
                "age_weights": [0.3, 0.5, 0.2],
                "gender_distribution": {"male": 0.55, "female": 0.45},
                "common_conditions": ["hypertension", "diabetes", "hyperlipidemia", "heart_disease"]
            },
            "pediatrics": {
                "age_ranges": [(0, 2), (2, 12), (12, 18)],
                "age_weights": [0.3, 0.5, 0.2],
                "gender_distribution": {"male": 0.51, "female": 0.49},
                "common_conditions": ["respiratory", "fever", "gastroenteritis", "trauma"]
            },
            "geriatrics": {
                "age_ranges": [(65, 75), (75, 85), (85, 95)],
                "age_weights": [0.4, 0.4, 0.2],
                "gender_distribution": {"male": 0.45, "female": 0.55},
                "common_conditions": ["dementia", "falls", "polypharmacy", "frailty"]
            }
        }
        
        # difficulty-based characteristics
        self.difficulty_characteristics = {
            "easy": {
                "symptom_clarity": 0.9,
                "diagnostic_obviousness": 0.8,
                "comorbidity_complexity": 0.3,
                "social_factors": 0.2
            },
            "medium": {
                "symptom_clarity": 0.7,
                "diagnostic_obviousness": 0.6,
                "comorbidity_complexity": 0.5,
                "social_factors": 0.4
            },
            "hard": {
                "symptom_clarity": 0.4,
                "diagnostic_obviousness": 0.3,
                "comorbidity_complexity": 0.8,
                "social_factors": 0.7
            }
        }
    
    def generate_patient(self, age: Optional[int] = None, gender: Optional[str] = None) -> EnhancedPatientProfile:
        """generate a realistic patient profile"""
        if age is None:
            age = random.randint(18, 85)
        if gender is None:
            gender = random.choice(["male", "female"])
        gender = gender.lower()  # normalize to lowercase
        
        # generate basic demographics
        name = random.choice(self.names[gender])
        race_ethnicity = random.choice(["White", "Black", "Hispanic", "Asian", "Other"])
        
        # calculate birth date
        today = date.today()
        birth_year = today.year - age
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # simplified
        date_of_birth = date(birth_year, birth_month, birth_day)
        
        # physical characteristics
        if gender == "male":
            height = random.uniform(165, 185)  # cm
        else:
            height = random.uniform(155, 175)  # cm
        
        weight = random.uniform(50, 120)  # kg
        bmi = weight / ((height / 100) ** 2)
        
        # create patient profile
        patient = EnhancedPatientProfile(
            patient_id=f"P{random.randint(1000, 9999)}",
            name=name,
            age=age,
            gender=gender,
            race_ethnicity=race_ethnicity,
            date_of_birth=date_of_birth,
            height=height,
            weight=weight,
            bmi=bmi
        )
        
        # add social history
        patient.social_history.occupation = random.choice(self.occupations)
        patient.social_history.education_level = random.choice(self.education_levels)
        patient.social_history.marital_status = random.choice(self.marital_statuses)
        patient.social_history.insurance_status = random.choice(["Private", "Medicare", "Medicaid", "Uninsured"])
        patient.social_history.primary_language = random.choice(["English", "Spanish", "French", "German"])
        
        # add social determinants
        if random.random() < 0.3:
            patient.social_history.social_determinants.append(SocialDeterminant.POVERTY)
        if random.random() < 0.2:
            patient.social_history.social_determinants.append(SocialDeterminant.FOOD_INSECURITY)
        if random.random() < 0.15:
            patient.social_history.social_determinants.append(SocialDeterminant.TRANSPORTATION_BARRIERS)
        
        # add personality
        patient.personality.personality_type = random.choice(list(PersonalityType))
        patient.personality.communication_style = random.choice(["direct", "indirect", "detailed", "brief"])
        patient.personality.health_literacy = random.choice(["low", "adequate", "high"])
        
        # add lifestyle factors
        patient.lifestyle_factors.smoking_status = random.choice(["never", "former", "current"])
        patient.lifestyle_factors.alcohol_use = random.choice(["none", "moderate", "heavy"])
        patient.lifestyle_factors.exercise_frequency = random.choice(["none", "low", "moderate", "high"])
        
        # add family history
        if random.random() < 0.4:
            patient.family_history.conditions.append("Hypertension")
        if random.random() < 0.3:
            patient.family_history.conditions.append("Diabetes")
        if random.random() < 0.2:
            patient.family_history.conditions.append("Heart Disease")
        
        return patient
    
    def generate_patient_from_pattern(self, pattern: Dict[str, Any], difficulty: str = "medium") -> EnhancedPatientProfile:
        """generate patient profile based on clinical pattern"""
        pattern_data = pattern.get('pattern_data', {})
        demographics = pattern_data.get('demographics', {})
        
        # determine age from pattern
        age_range = demographics.get('age_range', (30, 70))
        age = random.randint(age_range[0], age_range[1])
        
        # determine gender from pattern
        gender_dist = demographics.get('gender_distribution', {'male': 0.5, 'female': 0.5})
        gender = random.choices(list(gender_dist.keys()), weights=list(gender_dist.values()))[0]
        
        # generate base patient
        patient = self.generate_patient(age, gender)
        
        # apply pattern-specific characteristics
        self._apply_pattern_characteristics(patient, pattern_data, difficulty)
        
        return patient
    
    def generate_patient_by_specialty(self, specialty: str, difficulty: str = "medium") -> EnhancedPatientProfile:
        """generate patient profile optimized for specific specialty"""
        if specialty not in self.specialty_demographics:
            # fallback to general patient generation
            return self.generate_patient()
        
        specialty_demo = self.specialty_demographics[specialty]
        
        # select age range based on specialty
        age_range_idx = random.choices(
            range(len(specialty_demo['age_ranges'])), 
            weights=specialty_demo['age_weights']
        )[0]
        age_range = specialty_demo['age_ranges'][age_range_idx]
        age = random.randint(age_range[0], age_range[1])
        
        # select gender based on specialty distribution
        gender = random.choices(
            list(specialty_demo['gender_distribution'].keys()),
            weights=list(specialty_demo['gender_distribution'].values())
        )[0]
        
        # generate base patient
        patient = self.generate_patient(age, gender)
        
        # apply specialty-specific characteristics
        self._apply_specialty_characteristics(patient, specialty, difficulty)
        
        return patient
    
    def generate_patient_by_difficulty(self, difficulty: str, specialty: Optional[str] = None) -> EnhancedPatientProfile:
        """generate patient profile with difficulty-appropriate characteristics"""
        if specialty:
            patient = self.generate_patient_by_specialty(specialty, difficulty)
        else:
            patient = self.generate_patient()
        
        # apply difficulty-specific characteristics
        self._apply_difficulty_characteristics(patient, difficulty)
        
        return patient
    
    def _apply_pattern_characteristics(self, patient: EnhancedPatientProfile, pattern_data: Dict[str, Any], difficulty: str):
        """apply pattern-specific characteristics to patient"""
        # add risk factors from pattern
        risk_factors = pattern_data.get('risk_factors', [])
        for risk in risk_factors:
            if risk == "hypertension":
                patient.conditions.append("Hypertension")
            elif risk == "diabetes":
                patient.conditions.append("Diabetes")
            elif risk == "smoking":
                patient.lifestyle_factors.smoking_status = "current"
            elif risk == "hyperlipidemia":
                patient.conditions.append("Hyperlipidemia")
        
        # adjust symptoms based on pattern
        symptom_clusters = pattern_data.get('symptom_clusters', [])
        if symptom_clusters:
            selected_cluster = random.choice(symptom_clusters)
            patient.symptoms = selected_cluster.get('symptoms', [])
        
        # adjust personality based on difficulty
        if difficulty == "hard":
            # make communication more challenging
            patient.personality.communication_style = random.choice(["indirect", "confused", "uncooperative"])
            patient.personality.health_literacy = "low"
        elif difficulty == "easy":
            # make communication clear
            patient.personality.communication_style = "direct"
            patient.personality.health_literacy = "high"
    
    def _apply_specialty_characteristics(self, patient: EnhancedPatientProfile, specialty: str, difficulty: str):
        """apply specialty-specific characteristics to patient"""
        specialty_demo = self.specialty_demographics[specialty]
        
        # add specialty-specific conditions
        common_conditions = specialty_demo.get('common_conditions', [])
        for condition in common_conditions:
            if random.random() < 0.3:  # 30% chance per condition
                patient.conditions.append(condition)
        
        # adjust social factors based on specialty
        if specialty == "geriatrics":
            patient.social_history.occupation = "Retired"
            patient.social_history.marital_status = random.choice(["Widowed", "Married", "Single"])
            if random.random() < 0.4:
                patient.social_history.social_determinants.append(SocialDeterminant.SOCIAL_ISOLATION)
        
        elif specialty == "pediatrics":
            patient.social_history.occupation = "Student" if patient.age > 5 else "Preschool"
            patient.social_history.marital_status = "Single"
            patient.personality.personality_type = random.choice([PersonalityType.EXTROVERT, PersonalityType.INTROVERT])
        
        elif specialty == "cardiology":
            # add cardiac risk factors
            if random.random() < 0.6:
                patient.family_history.conditions.append("Heart Disease")
            if random.random() < 0.5:
                patient.lifestyle_factors.smoking_status = "former"
    
    def _apply_difficulty_characteristics(self, patient: EnhancedPatientProfile, difficulty: str):
        """apply difficulty-specific characteristics to patient"""
        if difficulty not in self.difficulty_characteristics:
            return
        
        diff_chars = self.difficulty_characteristics[difficulty]
        
        # adjust symptom clarity
        if diff_chars['symptom_clarity'] < 0.5:
            # make symptoms less clear
            patient.symptoms = [f"vague {symptom}" for symptom in patient.symptoms]
            patient.personality.communication_style = "indirect"
        
        # adjust diagnostic obviousness
        if diff_chars['diagnostic_obviousness'] < 0.5:
            # add confounding symptoms
            confounding_symptoms = ["fatigue", "nausea", "dizziness", "anxiety"]
            patient.symptoms.extend(random.sample(confounding_symptoms, 2))
        
        # adjust comorbidity complexity
        if diff_chars['comorbidity_complexity'] > 0.6:
            # add multiple comorbidities
            comorbidities = ["Hypertension", "Diabetes", "COPD", "Depression", "Obesity"]
            for comorbidity in random.sample(comorbidities, 2):
                if comorbidity not in patient.conditions:
                    patient.conditions.append(comorbidity)
        
        # adjust social factors
        if diff_chars['social_factors'] > 0.5:
            # add challenging social determinants
            challenging_determinants = [
                SocialDeterminant.POVERTY,
                SocialDeterminant.LANGUAGE_BARRIERS,
                SocialDeterminant.TRANSPORTATION_BARRIERS,
                SocialDeterminant.SOCIAL_ISOLATION
            ]
            for determinant in random.sample(challenging_determinants, 2):
                if determinant not in patient.social_history.social_determinants:
                    patient.social_history.social_determinants.append(determinant)
    
    def generate_pediatric_patient(self, age: Optional[int] = None) -> EnhancedPatientProfile:
        """generate a pediatric patient profile"""
        if age is None:
            age = random.randint(1, 17)
        
        patient = self.generate_patient(age, random.choice(["male", "female"]))
        
        # adjust for pediatric characteristics
        patient.social_history.occupation = "Student" if age > 5 else "Preschool"
        patient.social_history.education_level = "Elementary" if age < 12 else "High School"
        patient.social_history.marital_status = "Single"
        patient.personality.personality_type = random.choice([PersonalityType.EXTROVERT, PersonalityType.INTROVERT])
        
        return patient
    
    def generate_geriatric_patient(self, age: Optional[int] = None) -> EnhancedPatientProfile:
        """generate a geriatric patient profile"""
        if age is None:
            age = random.randint(65, 95)
        
        patient = self.generate_patient(age, random.choice(["male", "female"]))
        
        # adjust for geriatric characteristics
        patient.social_history.occupation = "Retired"
        patient.social_history.education_level = random.choice(["High School", "Some College", "Bachelor's Degree"])
        patient.personality.personality_type = random.choice([PersonalityType.TYPE_A, PersonalityType.TYPE_B])
        
        # add geriatric risk factors
        if random.random() < 0.6:
            patient.family_history.conditions.append("Hypertension")
        if random.random() < 0.4:
            patient.family_history.conditions.append("Diabetes")
        if random.random() < 0.3:
            patient.family_history.conditions.append("Dementia")
        
        return patient 