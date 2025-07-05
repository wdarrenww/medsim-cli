"""
comprehensive symptoms library for medical simulation with realistic discovery patterns
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import random


class SymptomSeverity(Enum):
    """symptom severity levels"""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


class SymptomCategory(Enum):
    """symptom categories"""
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    GASTROINTESTINAL = "gastrointestinal"
    NEUROLOGICAL = "neurological"
    MUSCULOSKELETAL = "musculoskeletal"
    DERMATOLOGICAL = "dermatological"
    GENITOURINARY = "genitourinary"
    ENDOCRINE = "endocrine"
    HEMATOLOGICAL = "hematological"
    PSYCHIATRIC = "psychiatric"
    GENERAL = "general"
    CONSTITUTIONAL = "constitutional"


class DiscoveryMethod(Enum):
    """how symptoms are discovered"""
    PATIENT_REPORTED = "patient_reported"
    PHYSICAL_EXAM = "physical_exam"
    VITAL_SIGNS = "vital_signs"
    LAB_RESULTS = "lab_results"
    IMAGING = "imaging"
    OBSERVATION = "observation"
    SPECIALIZED_TEST = "specialized_test"


@dataclass
class SymptomProgression:
    """symptom progression over time"""
    onset_time: datetime
    initial_severity: SymptomSeverity
    current_severity: SymptomSeverity
    progression_rate: float  # severity change per hour
    triggers: List[str] = field(default_factory=list)
    relieving_factors: List[str] = field(default_factory=list)
    associated_symptoms: List[str] = field(default_factory=list)
    discovered_by: List[DiscoveryMethod] = field(default_factory=list)
    discovery_time: Optional[datetime] = None
    notes: List[str] = field(default_factory=list)


@dataclass
class Symptom:
    """symptom definition with realistic discovery patterns"""
    name: str
    category: SymptomCategory
    description: str
    severity: SymptomSeverity
    associated_conditions: List[str] = field(default_factory=list)
    differential_diagnosis: List[str] = field(default_factory=list)
    red_flags: List[str] = field(default_factory=list)
    common_causes: List[str] = field(default_factory=list)
    typical_duration: str = ""
    aggravating_factors: List[str] = field(default_factory=list)
    relieving_factors: List[str] = field(default_factory=list)
    associated_symptoms: List[str] = field(default_factory=list)
    
    # discovery patterns
    discovery_methods: List[DiscoveryMethod] = field(default_factory=list)
    discovery_difficulty: float = 1.0  # 0.0 = obvious, 1.0 = very subtle
    requires_specific_exam: bool = False
    requires_lab_confirmation: bool = False
    requires_imaging: bool = False
    
    # temporal patterns
    typical_onset: str = "variable"  # sudden, gradual, intermittent
    progression_pattern: str = "variable"  # worsening, improving, fluctuating
    time_to_peak: Optional[int] = None  # hours to peak severity
    
    # physical exam findings
    exam_findings: Dict[str, str] = field(default_factory=dict)
    vital_sign_changes: Dict[str, Tuple[float, float]] = field(default_factory=dict)
    
    # lab/imaging correlates
    lab_correlates: List[str] = field(default_factory=list)
    imaging_correlates: List[str] = field(default_factory=list)


class ComprehensiveSymptomLibrary:
    """comprehensive library of medical symptoms with realistic discovery patterns"""
    
    def __init__(self):
        self.symptoms = self._initialize_symptoms()
        self.active_symptoms: Dict[str, SymptomProgression] = {}
        self.discovery_history: List[Dict[str, Any]] = []
    
    def _initialize_symptoms(self) -> Dict[str, Symptom]:
        """initialize comprehensive symptom library with realistic discovery patterns"""
        symptoms = {}
        
        # cardiovascular symptoms
        symptoms["chest_pain"] = Symptom(
            name="Chest Pain",
            category=SymptomCategory.CARDIOVASCULAR,
            description="Pain or discomfort in the chest area",
            severity=SymptomSeverity.SEVERE,
            associated_conditions=["myocardial infarction", "angina", "aortic dissection", "pulmonary embolism"],
            differential_diagnosis=["GERD", "costochondritis", "pneumonia", "anxiety"],
            red_flags=["crushing pain", "radiation to arm/jaw", "sweating", "shortness of breath"],
            common_causes=["coronary artery disease", "musculoskeletal", "gastrointestinal"],
            typical_duration="variable",
            aggravating_factors=["exertion", "stress", "cold weather"],
            relieving_factors=["rest", "nitroglycerin", "antacids"],
            associated_symptoms=["shortness of breath", "nausea", "sweating", "dizziness"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.PHYSICAL_EXAM],
            discovery_difficulty=0.2,  # usually obvious
            requires_specific_exam=True,
            typical_onset="sudden",
            progression_pattern="worsening",
            time_to_peak=2,
            exam_findings={
                "chest_tenderness": "may be present in costochondritis",
                "heart_sounds": "may have S3, S4, or murmurs",
                "pulses": "may be diminished in dissection"
            },
            vital_sign_changes={
                "heart_rate": (10, 30),
                "blood_pressure": (10, 40),
                "respiratory_rate": (5, 15)
            },
            lab_correlates=["troponin", "ck_mb", "bnp"],
            imaging_correlates=["chest_xray", "chest_ct", "coronary_angiogram"]
        )
        
        symptoms["shortness_of_breath"] = Symptom(
            name="Shortness of Breath",
            category=SymptomCategory.RESPIRATORY,
            description="Difficulty breathing or feeling of breathlessness",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["heart failure", "pneumonia", "COPD", "pulmonary embolism"],
            differential_diagnosis=["anxiety", "anemia", "obesity", "deconditioning"],
            red_flags=["sudden onset", "chest pain", "cyanosis", "altered mental status"],
            common_causes=["cardiac", "pulmonary", "anxiety"],
            typical_duration="variable",
            aggravating_factors=["exertion", "lying flat", "exposure to triggers"],
            relieving_factors=["rest", "upright position", "bronchodilators"],
            associated_symptoms=["chest pain", "cough", "fatigue", "anxiety"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.OBSERVATION, DiscoveryMethod.VITAL_SIGNS],
            discovery_difficulty=0.3,
            requires_specific_exam=True,
            typical_onset="variable",
            progression_pattern="worsening",
            exam_findings={
                "respiratory_rate": "tachypnea",
                "oxygen_saturation": "may be decreased",
                "lung_sounds": "may have crackles, wheezes, or diminished breath sounds",
                "accessory_muscle_use": "may be present"
            },
            vital_sign_changes={
                "respiratory_rate": (5, 20),
                "oxygen_saturation": (-5, -15),
                "heart_rate": (10, 25)
            },
            lab_correlates=["abg", "bicarbonate"],
            imaging_correlates=["chest_xray", "chest_ct", "vq_scan"]
        )
        
        symptoms["palpitations"] = Symptom(
            name="Palpitations",
            category=SymptomCategory.CARDIOVASCULAR,
            description="Sensation of rapid, irregular, or forceful heartbeat",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["atrial fibrillation", "ventricular tachycardia", "anxiety"],
            differential_diagnosis=["normal sinus rhythm", "premature beats", "anxiety"],
            red_flags=["syncope", "chest pain", "shortness of breath"],
            common_causes=["anxiety", "caffeine", "medications", "arrhythmias"],
            typical_duration="minutes to hours",
            aggravating_factors=["stress", "caffeine", "alcohol"],
            relieving_factors=["rest", "vagal maneuvers"],
            associated_symptoms=["anxiety", "chest pain", "dizziness"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.VITAL_SIGNS],
            discovery_difficulty=0.4,
            requires_specific_exam=True,
            typical_onset="sudden",
            progression_pattern="fluctuating",
            exam_findings={
                "heart_rate": "may be irregular or rapid",
                "pulse": "may be irregular",
                "blood_pressure": "may be variable"
            },
            vital_sign_changes={
                "heart_rate": (20, 60),
                "blood_pressure": (5, 20)
            },
            lab_correlates=["electrolytes", "thyroid_function"],
            imaging_correlates=["ecg", "holter_monitor"]
        )
        
        symptoms["syncope"] = Symptom(
            name="Syncope",
            category=SymptomCategory.NEUROLOGICAL,
            description="Temporary loss of consciousness due to decreased blood flow to brain",
            severity=SymptomSeverity.SEVERE,
            associated_conditions=["cardiac arrhythmia", "orthostatic hypotension", "seizure"],
            differential_diagnosis=["vasovagal", "cardiac", "neurological", "psychogenic"],
            red_flags=["chest pain", "palpitations", "head injury", "focal neurological signs"],
            common_causes=["vasovagal", "orthostatic", "cardiac", "neurological"],
            typical_duration="seconds to minutes",
            aggravating_factors=["prolonged standing", "dehydration", "pain"],
            relieving_factors=["lying down", "hydration"],
            associated_symptoms=["dizziness", "nausea", "sweating", "palpitations"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.OBSERVATION],
            discovery_difficulty=0.1,  # very obvious
            requires_specific_exam=True,
            typical_onset="sudden",
            progression_pattern="sudden",
            exam_findings={
                "orthostatic_vitals": "may show significant drop",
                "neurological_exam": "should be normal after recovery",
                "cardiac_exam": "may reveal arrhythmia"
            },
            vital_sign_changes={
                "blood_pressure": (20, 50),
                "heart_rate": (10, 40)
            },
            lab_correlates=["electrolytes", "glucose", "cardiac_enzymes"],
            imaging_correlates=["ecg", "head_ct", "carotid_doppler"]
        )
        
        # respiratory symptoms
        symptoms["cough"] = Symptom(
            name="Cough",
            category=SymptomCategory.RESPIRATORY,
            description="Sudden expulsion of air from lungs",
            severity=SymptomSeverity.MILD,
            associated_conditions=["upper respiratory infection", "pneumonia", "COPD", "asthma"],
            differential_diagnosis=["post-nasal drip", "GERD", "medication side effect"],
            red_flags=["blood in sputum", "weight loss", "fever", "chest pain"],
            common_causes=["viral infection", "allergies", "smoking", "medications"],
            typical_duration="days to weeks",
            aggravating_factors=["cold air", "allergens", "lying down"],
            relieving_factors=["humidifier", "cough suppressants", "treating underlying cause"],
            associated_symptoms=["sore throat", "runny nose", "fever", "fatigue"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.OBSERVATION],
            discovery_difficulty=0.1,
            requires_specific_exam=False,
            typical_onset="gradual",
            progression_pattern="variable",
            exam_findings={
                "lung_sounds": "may have crackles, wheezes, or normal",
                "throat": "may be erythematous",
                "lymph_nodes": "may be enlarged"
            },
            vital_sign_changes={
                "respiratory_rate": (2, 8)
            },
            lab_correlates=["cbc", "sputum_culture"],
            imaging_correlates=["chest_xray"]
        )
        
        symptoms["wheezing"] = Symptom(
            name="Wheezing",
            category=SymptomCategory.RESPIRATORY,
            description="High-pitched whistling sound during breathing",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["asthma", "COPD", "bronchitis", "heart failure"],
            differential_diagnosis=["foreign body", "tumor", "vocal cord dysfunction"],
            red_flags=["severe respiratory distress", "cyanosis", "altered mental status"],
            common_causes=["asthma", "COPD", "bronchitis", "allergies"],
            typical_duration="variable",
            aggravating_factors=["allergens", "exercise", "cold air", "respiratory infections"],
            relieving_factors=["bronchodilators", "steroids", "avoiding triggers"],
            associated_symptoms=["shortness of breath", "cough", "chest tightness"],
            discovery_methods=[DiscoveryMethod.PHYSICAL_EXAM, DiscoveryMethod.PATIENT_REPORTED],
            discovery_difficulty=0.3,
            requires_specific_exam=True,
            typical_onset="variable",
            progression_pattern="worsening",
            exam_findings={
                "lung_sounds": "wheezes on auscultation",
                "respiratory_rate": "may be increased",
                "accessory_muscle_use": "may be present",
                "oxygen_saturation": "may be decreased"
            },
            vital_sign_changes={
                "respiratory_rate": (5, 15),
                "oxygen_saturation": (-3, -10)
            },
            lab_correlates=["peak_flow", "pulmonary_function"],
            imaging_correlates=["chest_xray"]
        )
        
        # gastrointestinal symptoms
        symptoms["abdominal_pain"] = Symptom(
            name="Abdominal Pain",
            category=SymptomCategory.GASTROINTESTINAL,
            description="Pain or discomfort in the abdomen",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["appendicitis", "cholecystitis", "diverticulitis", "peptic ulcer"],
            differential_diagnosis=["irritable bowel syndrome", "constipation", "gas", "anxiety"],
            red_flags=["severe pain", "rigid abdomen", "fever", "vomiting"],
            common_causes=["gas", "constipation", "infection", "inflammation"],
            typical_duration="variable",
            aggravating_factors=["eating", "movement", "stress"],
            relieving_factors=["rest", "heat", "antacids"],
            associated_symptoms=["nausea", "vomiting", "diarrhea", "constipation"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.PHYSICAL_EXAM],
            discovery_difficulty=0.2,
            requires_specific_exam=True,
            typical_onset="variable",
            progression_pattern="worsening",
            exam_findings={
                "tenderness": "localized or diffuse",
                "guarding": "may be present",
                "rebound": "may be present",
                "bowel_sounds": "may be increased or decreased"
            },
            vital_sign_changes={
                "heart_rate": (5, 20),
                "blood_pressure": (5, 15)
            },
            lab_correlates=["cbc", "amylase", "lipase", "liver_function"],
            imaging_correlates=["abdominal_ct", "abdominal_ultrasound"]
        )
        
        symptoms["nausea"] = Symptom(
            name="Nausea",
            category=SymptomCategory.GASTROINTESTINAL,
            description="Sensation of wanting to vomit",
            severity=SymptomSeverity.MILD,
            associated_conditions=["gastroenteritis", "pregnancy", "migraine", "medication side effect"],
            differential_diagnosis=["anxiety", "motion sickness", "food poisoning"],
            red_flags=["severe abdominal pain", "headache", "fever", "dehydration"],
            common_causes=["viral infection", "pregnancy", "medications", "anxiety"],
            typical_duration="hours to days",
            aggravating_factors=["strong odors", "certain foods", "motion"],
            relieving_factors=["rest", "small meals", "antiemetics"],
            associated_symptoms=["vomiting", "abdominal pain", "dizziness", "sweating"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED],
            discovery_difficulty=0.1,
            requires_specific_exam=False,
            typical_onset="variable",
            progression_pattern="variable",
            exam_findings={
                "abdomen": "may be tender",
                "dehydration": "may be present"
            },
            vital_sign_changes={
                "heart_rate": (5, 15)
            },
            lab_correlates=["electrolytes", "pregnancy_test"],
            imaging_correlates=[]
        )
        
        symptoms["vomiting"] = Symptom(
            name="Vomiting",
            category=SymptomCategory.GASTROINTESTINAL,
            description="Forceful expulsion of stomach contents",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["gastroenteritis", "pregnancy", "migraine", "food poisoning"],
            differential_diagnosis=["anxiety", "motion sickness", "medication side effect"],
            red_flags=["blood in vomit", "severe abdominal pain", "headache", "dehydration"],
            common_causes=["viral infection", "food poisoning", "pregnancy", "medications"],
            typical_duration="hours to days",
            aggravating_factors=["certain foods", "motion", "strong odors"],
            relieving_factors=["rest", "hydration", "antiemetics"],
            associated_symptoms=["nausea", "abdominal pain", "dehydration", "weakness"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.OBSERVATION],
            discovery_difficulty=0.1,
            requires_specific_exam=False,
            typical_onset="variable",
            progression_pattern="variable",
            exam_findings={
                "dehydration": "may be present",
                "abdomen": "may be tender"
            },
            vital_sign_changes={
                "heart_rate": (10, 25),
                "blood_pressure": (5, 20)
            },
            lab_correlates=["electrolytes", "pregnancy_test"],
            imaging_correlates=[]
        )
        
        symptoms["diarrhea"] = Symptom(
            name="Diarrhea",
            category=SymptomCategory.GASTROINTESTINAL,
            description="Loose, watery stools occurring more frequently than normal",
            severity=SymptomSeverity.MILD,
            associated_conditions=["gastroenteritis", "food poisoning", "irritable bowel syndrome"],
            differential_diagnosis=["medication side effect", "anxiety", "dietary changes"],
            red_flags=["blood in stool", "severe abdominal pain", "dehydration", "fever"],
            common_causes=["viral infection", "food poisoning", "medications", "dietary changes"],
            typical_duration="days",
            aggravating_factors=["certain foods", "stress", "medications"],
            relieving_factors=["hydration", "bland diet", "antidiarrheals"],
            associated_symptoms=["abdominal pain", "nausea", "dehydration", "weakness"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED],
            discovery_difficulty=0.1,
            requires_specific_exam=False,
            typical_onset="variable",
            progression_pattern="variable",
            exam_findings={
                "abdomen": "may be tender",
                "dehydration": "may be present"
            },
            vital_sign_changes={
                "heart_rate": (5, 15)
            },
            lab_correlates=["stool_culture", "electrolytes"],
            imaging_correlates=[]
        )
        
        symptoms["constipation"] = Symptom(
            name="Constipation",
            category=SymptomCategory.GASTROINTESTINAL,
            description="Infrequent or difficult bowel movements",
            severity=SymptomSeverity.MILD,
            associated_conditions=["irritable bowel syndrome", "hypothyroidism", "medication side effect"],
            differential_diagnosis=["dehydration", "low fiber diet", "lack of exercise"],
            red_flags=["severe abdominal pain", "blood in stool", "weight loss"],
            common_causes=["low fiber diet", "dehydration", "lack of exercise", "medications"],
            typical_duration="days to weeks",
            aggravating_factors=["low fiber diet", "dehydration", "sedentary lifestyle"],
            relieving_factors=["high fiber diet", "hydration", "exercise", "laxatives"],
            associated_symptoms=["abdominal pain", "bloating", "straining", "hard stools"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED],
            discovery_difficulty=0.2,
            requires_specific_exam=False,
            typical_onset="gradual",
            progression_pattern="variable",
            exam_findings={
                "abdomen": "may be distended",
                "rectal_exam": "may reveal impaction"
            },
            vital_sign_changes={},
            lab_correlates=["thyroid_function"],
            imaging_correlates=[]
        )
        
        # neurological symptoms
        symptoms["headache"] = Symptom(
            name="Headache",
            category=SymptomCategory.NEUROLOGICAL,
            description="Pain in the head or upper neck",
            severity=SymptomSeverity.MILD,
            associated_conditions=["migraine", "tension headache", "cluster headache", "meningitis"],
            differential_diagnosis=["sinusitis", "eye strain", "dehydration", "anxiety"],
            red_flags=["sudden severe pain", "fever", "altered mental status", "focal neurological signs"],
            common_causes=["tension", "dehydration", "lack of sleep", "stress"],
            typical_duration="hours to days",
            aggravating_factors=["stress", "lack of sleep", "certain foods", "bright lights"],
            relieving_factors=["rest", "pain medications", "hydration", "dark room"],
            associated_symptoms=["nausea", "sensitivity to light", "sensitivity to sound"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED],
            discovery_difficulty=0.1,
            requires_specific_exam=False,
            typical_onset="variable",
            progression_pattern="variable",
            exam_findings={
                "neurological_exam": "should be normal",
                "meningeal_signs": "may be present in meningitis"
            },
            vital_sign_changes={
                "blood_pressure": (5, 15)
            },
            lab_correlates=["cbc", "lumbar_puncture"],
            imaging_correlates=["head_ct", "head_mri"]
        )
        
        symptoms["dizziness"] = Symptom(
            name="Dizziness",
            category=SymptomCategory.NEUROLOGICAL,
            description="Sensation of spinning or lightheadedness",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["vertigo", "orthostatic hypotension", "anxiety", "inner ear problems"],
            differential_diagnosis=["dehydration", "medication side effect", "anemia"],
            red_flags=["focal neurological signs", "chest pain", "palpitations", "syncope"],
            common_causes=["inner ear problems", "dehydration", "anxiety", "medications"],
            typical_duration="minutes to hours",
            aggravating_factors=["sudden movement", "standing up quickly", "stress"],
            relieving_factors=["rest", "hydration", "avoiding triggers"],
            associated_symptoms=["nausea", "sweating", "palpitations", "anxiety"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.VITAL_SIGNS],
            discovery_difficulty=0.3,
            requires_specific_exam=True,
            typical_onset="variable",
            progression_pattern="variable",
            exam_findings={
                "orthostatic_vitals": "may show drop",
                "neurological_exam": "should be normal",
                "nystagmus": "may be present in vertigo"
            },
            vital_sign_changes={
                "blood_pressure": (10, 30),
                "heart_rate": (5, 15)
            },
            lab_correlates=["electrolytes", "glucose"],
            imaging_correlates=["head_ct", "head_mri"]
        )
        
        symptoms["numbness"] = Symptom(
            name="Numbness",
            category=SymptomCategory.NEUROLOGICAL,
            description="Loss of sensation in a part of the body",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["peripheral neuropathy", "stroke", "carpal tunnel syndrome"],
            differential_diagnosis=["anxiety", "medication side effect", "compression"],
            red_flags=["sudden onset", "focal distribution", "weakness", "speech problems"],
            common_causes=["nerve compression", "diabetes", "vitamin deficiency", "medications"],
            typical_duration="variable",
            aggravating_factors=["prolonged pressure", "repetitive motion", "cold"],
            relieving_factors=["changing position", "treating underlying cause"],
            associated_symptoms=["tingling", "weakness", "pain", "burning"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.PHYSICAL_EXAM],
            discovery_difficulty=0.4,
            requires_specific_exam=True,
            typical_onset="variable",
            progression_pattern="variable",
            exam_findings={
                "sensation": "may be decreased",
                "motor_strength": "may be decreased",
                "reflexes": "may be decreased"
            },
            vital_sign_changes={},
            lab_correlates=["glucose", "vitamin_b12", "thyroid_function"],
            imaging_correlates=["mri_spine", "nerve_conduction"]
        )
        
        symptoms["weakness"] = Symptom(
            name="Weakness",
            category=SymptomCategory.NEUROLOGICAL,
            description="Reduced strength in muscles",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["stroke", "multiple sclerosis", "myasthenia gravis", "muscle disease"],
            differential_diagnosis=["fatigue", "deconditioning", "anxiety", "depression"],
            red_flags=["sudden onset", "focal distribution", "speech problems", "vision changes"],
            common_causes=["deconditioning", "fatigue", "anxiety", "medications"],
            typical_duration="variable",
            aggravating_factors=["exertion", "stress", "lack of sleep"],
            relieving_factors=["rest", "exercise", "treating underlying cause"],
            associated_symptoms=["fatigue", "numbness", "pain", "difficulty with activities"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.PHYSICAL_EXAM],
            discovery_difficulty=0.3,
            requires_specific_exam=True,
            typical_onset="variable",
            progression_pattern="variable",
            exam_findings={
                "motor_strength": "may be decreased",
                "coordination": "may be impaired",
                "gait": "may be abnormal"
            },
            vital_sign_changes={},
            lab_correlates=["ck", "electrolytes", "thyroid_function"],
            imaging_correlates=["head_mri", "spine_mri"]
        )
        
        # musculoskeletal symptoms
        symptoms["joint_pain"] = Symptom(
            name="Joint Pain",
            category=SymptomCategory.MUSCULOSKELETAL,
            description="Pain, stiffness, or discomfort in one or more joints",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["osteoarthritis", "rheumatoid arthritis", "gout", "lupus"],
            differential_diagnosis=["bursitis", "tendinitis", "infection", "trauma"],
            red_flags=["red, hot, swollen joint", "fever", "inability to move joint"],
            common_causes=["degeneration", "inflammation", "injury"],
            typical_duration="variable",
            aggravating_factors=["movement", "weight-bearing"],
            relieving_factors=["rest", "ice", "NSAIDs"],
            associated_symptoms=["swelling", "stiffness", "warmth"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.PHYSICAL_EXAM],
            discovery_difficulty=0.3,
            requires_specific_exam=True,
            typical_onset="gradual",
            progression_pattern="worsening",
            exam_findings={
                "swelling": "may be present",
                "warmth": "may be present",
                "range_of_motion": "may be decreased"
            },
            vital_sign_changes={},
            lab_correlates=["cbc", "esr", "crp", "rheumatoid_factor"],
            imaging_correlates=["joint_xray", "mri"]
        )

        # dermatological symptoms
        symptoms["rash"] = Symptom(
            name="Rash",
            category=SymptomCategory.DERMATOLOGICAL,
            description="Change in skin color, texture, or appearance",
            severity=SymptomSeverity.MILD,
            associated_conditions=["allergic reaction", "infection", "autoimmune disease", "drug reaction"],
            differential_diagnosis=["eczema", "psoriasis", "urticaria", "contact dermatitis"],
            red_flags=["rapidly spreading", "blistering", "mucosal involvement", "systemic symptoms"],
            common_causes=["allergy", "infection", "irritant"],
            typical_duration="days to weeks",
            aggravating_factors=["heat", "friction", "allergens"],
            relieving_factors=["antihistamines", "topical steroids", "avoiding triggers"],
            associated_symptoms=["itching", "swelling", "pain"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.PHYSICAL_EXAM],
            discovery_difficulty=0.2,
            requires_specific_exam=True,
            typical_onset="variable",
            progression_pattern="fluctuating",
            exam_findings={
                "distribution": "may be localized or generalized",
                "morphology": "macular, papular, vesicular, etc.",
                "blanching": "may or may not blanch"
            },
            vital_sign_changes={},
            lab_correlates=["cbc", "skin_biopsy"],
            imaging_correlates=[]
        )

        # genitourinary symptoms
        symptoms["dysuria"] = Symptom(
            name="Dysuria",
            category=SymptomCategory.GENITOURINARY,
            description="Pain or burning sensation during urination",
            severity=SymptomSeverity.MILD,
            associated_conditions=["urinary tract infection", "sexually transmitted infection", "bladder stones"],
            differential_diagnosis=["vaginitis", "prostatitis", "urethritis"],
            red_flags=["fever", "flank pain", "hematuria", "urinary retention"],
            common_causes=["infection", "irritation", "trauma"],
            typical_duration="days",
            aggravating_factors=["urination"],
            relieving_factors=["hydration", "antibiotics"],
            associated_symptoms=["frequency", "urgency", "hematuria"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.PHYSICAL_EXAM],
            discovery_difficulty=0.1,
            requires_specific_exam=False,
            typical_onset="sudden",
            progression_pattern="worsening",
            exam_findings={
                "suprapubic_tenderness": "may be present",
                "urethral_discharge": "may be present"
            },
            vital_sign_changes={},
            lab_correlates=["urinalysis", "urine_culture"],
            imaging_correlates=["renal_ultrasound"]
        )

        # endocrine symptoms
        symptoms["polyuria"] = Symptom(
            name="Polyuria",
            category=SymptomCategory.ENDOCRINE,
            description="Excessive urination, usually more than 3 liters per day",
            severity=SymptomSeverity.MILD,
            associated_conditions=["diabetes mellitus", "diabetes insipidus", "hypercalcemia"],
            differential_diagnosis=["psychogenic polydipsia", "diuretic use"],
            red_flags=["dehydration", "electrolyte imbalance", "altered mental status"],
            common_causes=["diabetes", "excess fluid intake", "medications"],
            typical_duration="variable",
            aggravating_factors=["high fluid intake"],
            relieving_factors=["treating underlying cause"],
            associated_symptoms=["polydipsia", "nocturia", "dehydration"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.LAB_RESULTS],
            discovery_difficulty=0.2,
            requires_specific_exam=False,
            typical_onset="gradual",
            progression_pattern="worsening",
            exam_findings={
                "hydration_status": "may show signs of dehydration"
            },
            vital_sign_changes={},
            lab_correlates=["glucose", "serum_osmolality", "urine_osmolality"],
            imaging_correlates=[]
        )

        # hematological symptoms
        symptoms["easy_bruising"] = Symptom(
            name="Easy Bruising",
            category=SymptomCategory.HEMATOLOGICAL,
            description="Bruising with minimal or no trauma",
            severity=SymptomSeverity.MILD,
            associated_conditions=["thrombocytopenia", "hemophilia", "liver disease", "vitamin K deficiency"],
            differential_diagnosis=["medication effect", "vasculitis", "aging"],
            red_flags=["spontaneous bleeding", "large hematomas", "prolonged bleeding"],
            common_causes=["low platelets", "clotting disorder", "medications"],
            typical_duration="variable",
            aggravating_factors=["trauma", "anticoagulants"],
            relieving_factors=["treating underlying cause"],
            associated_symptoms=["bleeding gums", "petechiae", "fatigue"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.PHYSICAL_EXAM],
            discovery_difficulty=0.2,
            requires_specific_exam=True,
            typical_onset="variable",
            progression_pattern="fluctuating",
            exam_findings={
                "skin": "ecchymoses, petechiae, purpura",
                "mucosa": "may show bleeding"
            },
            vital_sign_changes={},
            lab_correlates=["cbc", "pt", "inr", "liver_function"],
            imaging_correlates=[]
        )

        # psychiatric symptoms
        symptoms["hallucinations"] = Symptom(
            name="Hallucinations",
            category=SymptomCategory.PSYCHIATRIC,
            description="Perception of something that is not present (auditory, visual, tactile, etc.)",
            severity=SymptomSeverity.SEVERE,
            associated_conditions=["schizophrenia", "delirium", "substance intoxication", "dementia"],
            differential_diagnosis=["mood disorder", "sleep deprivation", "neurological disease"],
            red_flags=["command hallucinations", "suicidal ideation", "violent behavior"],
            common_causes=["psychiatric illness", "drugs", "sleep deprivation"],
            typical_duration="variable",
            aggravating_factors=["stress", "substance use"],
            relieving_factors=["antipsychotics", "sleep"],
            associated_symptoms=["delusions", "paranoia", "disorganized thinking"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.OBSERVATION],
            discovery_difficulty=0.4,
            requires_specific_exam=True,
            typical_onset="variable",
            progression_pattern="fluctuating",
            exam_findings={
                "mental_status": "disorganized, distracted, responding to internal stimuli"
            },
            vital_sign_changes={},
            lab_correlates=["toxicology_screen", "cbc", "metabolic_panel"],
            imaging_correlates=["head_ct", "mri"]
        )

        # constitutional symptoms
        symptoms["night_sweats"] = Symptom(
            name="Night Sweats",
            category=SymptomCategory.CONSTITUTIONAL,
            description="Excessive sweating during sleep, often soaking clothes or sheets",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["tuberculosis", "lymphoma", "menopause", "infection"],
            differential_diagnosis=["hyperthyroidism", "anxiety", "medication side effect"],
            red_flags=["weight loss", "fever", "lymphadenopathy"],
            common_causes=["infection", "malignancy", "hormonal changes"],
            typical_duration="weeks to months",
            aggravating_factors=["warm environment", "stress"],
            relieving_factors=["cool environment", "treating underlying cause"],
            associated_symptoms=["fever", "weight loss", "fatigue"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.OBSERVATION],
            discovery_difficulty=0.2,
            requires_specific_exam=False,
            typical_onset="gradual",
            progression_pattern="worsening",
            exam_findings={
                "skin": "may be clammy or moist after episode"
            },
            vital_sign_changes={},
            lab_correlates=["cbc", "esr", "hiv_test"],
            imaging_correlates=[]
        )

        # rare multi-system symptom
        symptoms["erythromelalgia"] = Symptom(
            name="Erythromelalgia",
            category=SymptomCategory.GENERAL,
            description="Episodes of burning pain, redness, and warmth in extremities, often triggered by heat or exercise",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["myeloproliferative disorders", "autoimmune disease", "neuropathy"],
            differential_diagnosis=["cellulitis", "gout", "complex regional pain syndrome"],
            red_flags=["ulceration", "severe pain", "loss of function"],
            common_causes=["idiopathic", "secondary to hematologic disease"],
            typical_duration="minutes to hours",
            aggravating_factors=["heat", "exercise", "stress"],
            relieving_factors=["cooling", "rest", "aspirin"],
            associated_symptoms=["swelling", "numbness", "tingling"],
            discovery_methods=[DiscoveryMethod.PATIENT_REPORTED, DiscoveryMethod.PHYSICAL_EXAM],
            discovery_difficulty=0.5,
            requires_specific_exam=True,
            typical_onset="sudden",
            progression_pattern="fluctuating",
            exam_findings={
                "skin": "red, warm, swollen extremity during episode"
            },
            vital_sign_changes={},
            lab_correlates=["cbc", "platelet_count"],
            imaging_correlates=[]
        )
        
        return symptoms
    
    def add_symptom_progression(self, symptom_name: str, patient_id: str, onset_time: datetime = None) -> str:
        """add a symptom progression for a patient"""
        if symptom_name not in self.symptoms:
            return f"Error: Symptom '{symptom_name}' not found."
        
        symptom = self.symptoms[symptom_name]
        if onset_time is None:
            onset_time = datetime.now()
        
        progression_id = f"{patient_id}_{symptom_name}_{len(self.active_symptoms)}"
        
        self.active_symptoms[progression_id] = SymptomProgression(
            onset_time=onset_time,
            initial_severity=symptom.severity,
            current_severity=symptom.severity,
            progression_rate=random.uniform(0.1, 0.5),  # severity change per hour
            triggers=symptom.aggravating_factors.copy(),
            relieving_factors=symptom.relieving_factors.copy(),
            associated_symptoms=symptom.associated_symptoms.copy(),
            discovered_by=[]
        )
        
        return f"✓ Symptom '{symptom.name}' progression started for patient {patient_id}"
    
    def discover_symptom(self, symptom_name: str, patient_id: str, method: DiscoveryMethod, 
                        discovery_time: datetime = None) -> str:
        """discover a symptom through a specific method"""
        if symptom_name not in self.symptoms:
            return f"Error: Symptom '{symptom_name}' not found."
        
        symptom = self.symptoms[symptom_name]
        
        # find active progression for this patient and symptom
        progression_id = None
        for pid, progression in self.active_symptoms.items():
            if patient_id in pid and symptom_name in pid:
                progression_id = pid
                break
        
        if not progression_id:
            return f"Error: No active progression found for symptom '{symptom_name}' in patient {patient_id}"
        
        progression = self.active_symptoms[progression_id]
        
        # check if this method can discover this symptom
        if method not in symptom.discovery_methods:
            return f"Error: Method '{method.value}' cannot discover symptom '{symptom_name}'"
        
        # check discovery difficulty
        if random.random() < symptom.discovery_difficulty:
            return f"Note: Symptom '{symptom_name}' not discovered by {method.value} (difficulty: {symptom.discovery_difficulty})"
        
        # add discovery method
        if method not in progression.discovered_by:
            progression.discovered_by.append(method)
        
        # set discovery time
        if discovery_time is None:
            discovery_time = datetime.now()
        progression.discovery_time = discovery_time
        
        # record discovery
        self.discovery_history.append({
            'symptom_name': symptom_name,
            'patient_id': patient_id,
            'method': method.value,
            'discovery_time': discovery_time,
            'difficulty': symptom.discovery_difficulty
        })
        
        return f"✓ Symptom '{symptom.name}' discovered via {method.value}"
    
    def update_symptom_progressions(self, current_time: datetime = None) -> List[str]:
        """update all active symptom progressions"""
        if current_time is None:
            current_time = datetime.now()
        
        updates = []
        
        for progression_id, progression in self.active_symptoms.items():
            # calculate time elapsed
            time_elapsed = (current_time - progression.onset_time).total_seconds() / 3600  # hours
            
            # update severity based on progression rate
            severity_change = progression.progression_rate * time_elapsed
            
            # convert severity to numeric for calculation
            severity_map = {
                SymptomSeverity.MILD: 1,
                SymptomSeverity.MODERATE: 2,
                SymptomSeverity.SEVERE: 3,
                SymptomSeverity.CRITICAL: 4
            }
            
            current_severity_num = severity_map.get(progression.current_severity, 2)
            new_severity_num = min(4, max(1, current_severity_num + severity_change))
            
            # convert back to severity enum
            reverse_severity_map = {v: k for k, v in severity_map.items()}
            new_severity = reverse_severity_map.get(int(new_severity_num), SymptomSeverity.MODERATE)
            
            if new_severity != progression.current_severity:
                progression.current_severity = new_severity
                updates.append(f"Symptom {progression_id} severity changed to {new_severity.value}")
        
        return updates
    
    def get_discovered_symptoms(self, patient_id: str) -> List[Dict[str, Any]]:
        """get all discovered symptoms for a patient"""
        discovered = []
        
        for progression_id, progression in self.active_symptoms.items():
            if patient_id in progression_id and progression.discovered_by:
                symptom_name = progression_id.split('_')[1]
                symptom = self.symptoms.get(symptom_name)
                
                if symptom:
                    discovered.append({
                        'name': symptom.name,
                        'category': symptom.category.value,
                        'severity': progression.current_severity.value,
                        'discovery_methods': [m.value for m in progression.discovered_by],
                        'discovery_time': progression.discovery_time,
                        'description': symptom.description,
                        'red_flags': symptom.red_flags
                    })
        
        return discovered
    
    def get_undiscovered_symptoms(self, patient_id: str) -> List[Dict[str, Any]]:
        """get all undiscovered symptoms for a patient"""
        undiscovered = []
        
        for progression_id, progression in self.active_symptoms.items():
            if patient_id in progression_id and not progression.discovered_by:
                symptom_name = progression_id.split('_')[1]
                symptom = self.symptoms.get(symptom_name)
                
                if symptom:
                    undiscovered.append({
                        'name': symptom.name,
                        'category': symptom.category.value,
                        'discovery_difficulty': symptom.discovery_difficulty,
                        'discovery_methods': [m.value for m in symptom.discovery_methods],
                        'requires_specific_exam': symptom.requires_specific_exam
                    })
        
        return undiscovered
    
    def get_symptom(self, name: str) -> Optional[Symptom]:
        """get a specific symptom by name"""
        return self.symptoms.get(name.lower().replace(" ", "_"))
    
    def get_symptoms_by_category(self, category: SymptomCategory) -> List[Symptom]:
        """get all symptoms in a category"""
        return [symptom for symptom in self.symptoms.values() if symptom.category == category]
    
    def get_symptoms_by_severity(self, severity: SymptomSeverity) -> List[Symptom]:
        """get all symptoms of a specific severity"""
        return [symptom for symptom in self.symptoms.values() if symptom.severity == severity]
    
    def search_symptoms(self, query: str) -> List[Symptom]:
        """search symptoms by name or description"""
        query = query.lower()
        results = []
        for symptom in self.symptoms.values():
            if (query in symptom.name.lower() or 
                query in symptom.description.lower() or
                any(query in condition.lower() for condition in symptom.associated_conditions)):
                results.append(symptom)
        return results
    
    def get_red_flag_symptoms(self) -> List[Symptom]:
        """get symptoms with red flags"""
        return [symptom for symptom in self.symptoms.values() if symptom.red_flags]
    
    def get_critical_symptoms(self) -> List[Symptom]:
        """get symptoms with critical severity"""
        return [symptom for symptom in self.symptoms.values() if symptom.severity == SymptomSeverity.CRITICAL]
    
    def get_all_symptoms(self) -> Dict[str, Symptom]:
        """get all symptoms"""
        return self.symptoms.copy() 