"""
disease progression system for realistic medical simulation
models disease development, complications, and treatment responses
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import random
import math
import json


class DiseaseStage(Enum):
    """disease progression stages"""
    LATENT = "latent"
    EARLY = "early"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"
    RESOLVING = "resolving"
    RESOLVED = "resolved"


class ComplicationType(Enum):
    """types of disease complications"""
    INFECTIOUS = "infectious"
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    RENAL = "renal"
    NEUROLOGICAL = "neurological"
    METABOLIC = "metabolic"
    HEMATOLOGICAL = "hematological"
    IMMUNOLOGICAL = "immunological"


class TreatmentResponse(Enum):
    """treatment response types"""
    EXCELLENT = "excellent"
    GOOD = "good"
    MODERATE = "moderate"
    POOR = "poor"
    RESISTANT = "resistant"
    ADVERSE = "adverse"


@dataclass
class DiseaseState:
    """represents current state of a disease"""
    disease_name: str
    stage: DiseaseStage
    severity_score: float  # 0.0 to 1.0
    onset_time: datetime
    progression_rate: float  # rate of progression
    complications: List[str] = field(default_factory=list)
    treatment_history: List[Dict[str, Any]] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    comorbidities: List[str] = field(default_factory=list)
    prognosis: str = "unknown"
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class Complication:
    """represents a disease complication"""
    complication_type: ComplicationType
    name: str
    severity: float  # 0.0 to 1.0
    onset_time: datetime
    risk_factors: List[str]
    symptoms: List[str]
    treatments: List[str]
    prognosis: str


@dataclass
class TreatmentEffect:
    """represents effect of a treatment"""
    treatment_name: str
    response_type: TreatmentResponse
    effectiveness: float  # 0.0 to 1.0
    side_effects: List[str]
    duration: timedelta
    administered_time: datetime
    dosage: str
    route: str


class DiseaseProgressionEngine:
    """engine for realistic disease progression modeling"""
    
    def __init__(self):
        self.disease_definitions = self._initialize_disease_definitions()
        self.complication_definitions = self._initialize_complication_definitions()
        self.treatment_definitions = self._initialize_treatment_definitions()
        self.patient_diseases: Dict[str, List[DiseaseState]] = {}
        self.patient_complications: Dict[str, List[Complication]] = {}
        self.patient_treatments: Dict[str, List[TreatmentEffect]] = {}
        
    def _initialize_disease_definitions(self) -> Dict[str, Dict[str, Any]]:
        """initialize disease definitions with progression patterns"""
        diseases = super()._initialize_disease_definitions() if hasattr(super(), '_initialize_disease_definitions') else {}
        diseases.update({
            "autoimmune_encephalitis": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 24, "symptoms": ["headache", "fever"], "severity": 0.2},
                    "moderate": {"duration_hours": 48, "symptoms": ["confusion", "seizures"], "severity": 0.6},
                    "severe": {"duration_hours": 72, "symptoms": ["psychosis", "coma"], "severity": 0.9},
                    "critical": {"duration_hours": 96, "symptoms": ["respiratory failure"], "severity": 1.0}
                },
                "complications": ["status_epilepticus", "respiratory_failure"],
                "risk_factors": ["autoimmune_disorder", "young_adult"],
                "progression_rate": 0.1,
                "treatment_responses": {
                    "steroids": {"effectiveness": 0.7, "response_time": 1.0},
                    "ivig": {"effectiveness": 0.8, "response_time": 2.0},
                    "plasmapheresis": {"effectiveness": 0.6, "response_time": 2.5}
                }
            },
            "sickle_cell_crisis": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 6, "symptoms": ["pain"], "severity": 0.3},
                    "moderate": {"duration_hours": 12, "symptoms": ["severe pain", "tachycardia"], "severity": 0.6},
                    "severe": {"duration_hours": 24, "symptoms": ["acute chest syndrome", "splenic sequestration"], "severity": 0.9},
                    "critical": {"duration_hours": 36, "symptoms": ["multi-organ failure"], "severity": 1.0}
                },
                "complications": ["acute_chest_syndrome", "stroke", "renal_failure"],
                "risk_factors": ["sickle_cell_trait", "infection", "dehydration"],
                "progression_rate": 0.2,
                "treatment_responses": {
                    "opioids": {"effectiveness": 0.8, "response_time": 0.5},
                    "oxygen": {"effectiveness": 0.7, "response_time": 0.3},
                    "exchange_transfusion": {"effectiveness": 0.9, "response_time": 1.5}
                }
            },
            "acute_coronary_syndrome": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 1, "symptoms": ["chest discomfort"], "severity": 0.3},
                    "moderate": {"duration_hours": 2, "symptoms": ["chest pain", "shortness of breath"], "severity": 0.6},
                    "severe": {"duration_hours": 4, "symptoms": ["severe chest pain", "sweating", "nausea"], "severity": 0.8},
                    "critical": {"duration_hours": 6, "symptoms": ["crushing chest pain", "cardiac arrest"], "severity": 1.0}
                },
                "complications": ["arrhythmia", "cardiogenic_shock", "heart_failure"],
                "risk_factors": ["hypertension", "diabetes", "smoking", "hyperlipidemia"],
                "progression_rate": 0.15,  # hours per stage
                "treatment_responses": {
                    "aspirin": {"effectiveness": 0.8, "response_time": 0.5},
                    "nitroglycerin": {"effectiveness": 0.7, "response_time": 0.3},
                    "thrombolytics": {"effectiveness": 0.9, "response_time": 1.0}
                }
            },
            "pneumonia": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 12, "symptoms": ["cough", "fever"], "severity": 0.3},
                    "moderate": {"duration_hours": 24, "symptoms": ["cough", "fever", "shortness of breath"], "severity": 0.6},
                    "severe": {"duration_hours": 48, "symptoms": ["severe cough", "high fever", "respiratory distress"], "severity": 0.8},
                    "critical": {"duration_hours": 72, "symptoms": ["respiratory failure", "sepsis"], "severity": 1.0}
                },
                "complications": ["pleural_effusion", "empyema", "sepsis", "respiratory_failure"],
                "risk_factors": ["smoking", "copd", "immunocompromised", "age"],
                "progression_rate": 0.08,
                "treatment_responses": {
                    "antibiotics": {"effectiveness": 0.85, "response_time": 2.0},
                    "oxygen_therapy": {"effectiveness": 0.9, "response_time": 0.5},
                    "steroids": {"effectiveness": 0.7, "response_time": 1.5}
                }
            },
            "diabetic_ketoacidosis": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 6, "symptoms": ["polyuria", "polydipsia"], "severity": 0.3},
                    "moderate": {"duration_hours": 12, "symptoms": ["nausea", "vomiting", "abdominal pain"], "severity": 0.6},
                    "severe": {"duration_hours": 18, "symptoms": ["dehydration", "confusion", "kussmaul_breathing"], "severity": 0.8},
                    "critical": {"duration_hours": 24, "symptoms": ["coma", "shock"], "severity": 1.0}
                },
                "complications": ["cerebral_edema", "hypokalemia", "acute_renal_failure"],
                "risk_factors": ["type_1_diabetes", "infection", "noncompliance"],
                "progression_rate": 0.12,
                "treatment_responses": {
                    "insulin": {"effectiveness": 0.95, "response_time": 1.0},
                    "fluids": {"effectiveness": 0.9, "response_time": 0.5},
                    "electrolytes": {"effectiveness": 0.8, "response_time": 1.5}
                }
            },
            "sepsis": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 2, "symptoms": ["fever", "tachycardia"], "severity": 0.4},
                    "moderate": {"duration_hours": 4, "symptoms": ["fever", "tachycardia", "tachypnea"], "severity": 0.6},
                    "severe": {"duration_hours": 6, "symptoms": ["hypotension", "organ_dysfunction"], "severity": 0.8},
                    "critical": {"duration_hours": 8, "symptoms": ["shock", "multiple_organ_failure"], "severity": 1.0}
                },
                "complications": ["acute_respiratory_distress_syndrome", "acute_kidney_injury", "disseminated_intravascular_coagulation"],
                "risk_factors": ["immunocompromised", "elderly", "chronic_disease"],
                "progression_rate": 0.25,
                "treatment_responses": {
                    "antibiotics": {"effectiveness": 0.8, "response_time": 1.5},
                    "fluids": {"effectiveness": 0.9, "response_time": 0.5},
                    "vasopressors": {"effectiveness": 0.7, "response_time": 1.0}
                }
            },
            "stroke": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 0.5, "symptoms": ["sudden_weakness", "speech_difficulty"], "severity": 0.5},
                    "moderate": {"duration_hours": 1, "symptoms": ["hemiparesis", "aphasia"], "severity": 0.7},
                    "severe": {"duration_hours": 2, "symptoms": ["severe_hemiparesis", "coma"], "severity": 0.9},
                    "critical": {"duration_hours": 4, "symptoms": ["brain_herniation", "death"], "severity": 1.0}
                },
                "complications": ["cerebral_edema", "hemorrhagic_transformation", "seizures"],
                "risk_factors": ["hypertension", "atrial_fibrillation", "diabetes", "smoking"],
                "progression_rate": 0.5,
                "treatment_responses": {
                    "tpa": {"effectiveness": 0.9, "response_time": 0.5},
                    "mechanical_thrombectomy": {"effectiveness": 0.95, "response_time": 1.0},
                    "blood_pressure_control": {"effectiveness": 0.8, "response_time": 0.5}
                }
            },
            # musculoskeletal: rheumatoid arthritis
            "rheumatoid_arthritis": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 48, "symptoms": ["joint_pain", "fatigue"], "severity": 0.2},
                    "moderate": {"duration_hours": 168, "symptoms": ["joint_pain", "swelling", "morning_stiffness"], "severity": 0.5},
                    "severe": {"duration_hours": 720, "symptoms": ["joint_pain", "deformity", "fatigue"], "severity": 0.8},
                    "critical": {"duration_hours": 1440, "symptoms": ["joint_pain", "loss_of_function", "systemic_symptoms"], "severity": 1.0}
                },
                "complications": ["joint_destruction", "vasculitis", "anemia"],
                "risk_factors": ["female", "family_history", "smoking"],
                "progression_rate": 0.01,
                "treatment_responses": {
                    "nsaids": {"effectiveness": 0.5, "response_time": 1.0},
                    "dmards": {"effectiveness": 0.8, "response_time": 2.0},
                    "steroids": {"effectiveness": 0.7, "response_time": 1.0}
                }
            },
            # dermatological: psoriasis
            "psoriasis": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 72, "symptoms": ["rash", "itching"], "severity": 0.2},
                    "moderate": {"duration_hours": 336, "symptoms": ["rash", "scaling", "joint_pain"], "severity": 0.5},
                    "severe": {"duration_hours": 720, "symptoms": ["rash", "erythroderma", "arthropathy"], "severity": 0.8},
                    "critical": {"duration_hours": 1440, "symptoms": ["rash", "systemic_symptoms"], "severity": 1.0}
                },
                "complications": ["psoriatic_arthritis", "infection"],
                "risk_factors": ["family_history", "stress", "obesity"],
                "progression_rate": 0.01,
                "treatment_responses": {
                    "topical_steroids": {"effectiveness": 0.7, "response_time": 1.0},
                    "phototherapy": {"effectiveness": 0.6, "response_time": 2.0},
                    "biologics": {"effectiveness": 0.8, "response_time": 3.0}
                }
            },
            # genitourinary: pyelonephritis
            "pyelonephritis": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 12, "symptoms": ["dysuria", "fever"], "severity": 0.3},
                    "moderate": {"duration_hours": 24, "symptoms": ["dysuria", "flank_pain", "nausea"], "severity": 0.6},
                    "severe": {"duration_hours": 48, "symptoms": ["dysuria", "vomiting", "sepsis"], "severity": 0.8},
                    "critical": {"duration_hours": 72, "symptoms": ["shock", "multi_organ_failure"], "severity": 1.0}
                },
                "complications": ["renal_abscess", "sepsis", "acute_kidney_injury"],
                "risk_factors": ["female", "urinary_tract_abnormality", "diabetes"],
                "progression_rate": 0.1,
                "treatment_responses": {
                    "antibiotics": {"effectiveness": 0.9, "response_time": 1.0},
                    "fluids": {"effectiveness": 0.8, "response_time": 0.5}
                }
            },
            # endocrine: diabetes insipidus
            "diabetes_insipidus": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 24, "symptoms": ["polyuria", "polydipsia"], "severity": 0.3},
                    "moderate": {"duration_hours": 48, "symptoms": ["polyuria", "dehydration", "fatigue"], "severity": 0.6},
                    "severe": {"duration_hours": 72, "symptoms": ["polyuria", "confusion", "electrolyte_imbalance"], "severity": 0.8},
                    "critical": {"duration_hours": 96, "symptoms": ["coma", "shock"], "severity": 1.0}
                },
                "complications": ["severe_dehydration", "seizures"],
                "risk_factors": ["head_trauma", "pituitary_tumor", "genetic"],
                "progression_rate": 0.1,
                "treatment_responses": {
                    "desmopressin": {"effectiveness": 0.95, "response_time": 1.0},
                    "fluids": {"effectiveness": 0.8, "response_time": 0.5}
                }
            },
            # hematological: immune thrombocytopenia
            "immune_thrombocytopenia": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 24, "symptoms": ["easy_bruising", "petechiae"], "severity": 0.3},
                    "moderate": {"duration_hours": 48, "symptoms": ["easy_bruising", "mucosal_bleeding"], "severity": 0.6},
                    "severe": {"duration_hours": 72, "symptoms": ["easy_bruising", "severe_bleeding"], "severity": 0.9},
                    "critical": {"duration_hours": 96, "symptoms": ["life_threatening_bleed"], "severity": 1.0}
                },
                "complications": ["intracranial_hemorrhage", "severe_anemia"],
                "risk_factors": ["autoimmune_disease", "recent_infection", "medications"],
                "progression_rate": 0.1,
                "treatment_responses": {
                    "steroids": {"effectiveness": 0.7, "response_time": 1.0},
                    "ivig": {"effectiveness": 0.8, "response_time": 1.5}
                }
            },
            # psychiatric: schizophrenia
            "schizophrenia": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 168, "symptoms": ["hallucinations", "delusions"], "severity": 0.3},
                    "moderate": {"duration_hours": 720, "symptoms": ["hallucinations", "disorganized_thoughts", "social_withdrawal"], "severity": 0.6},
                    "severe": {"duration_hours": 1440, "symptoms": ["hallucinations", "catatonia", "aggression"], "severity": 0.9},
                    "critical": {"duration_hours": 2880, "symptoms": ["suicidal_behavior", "violent_behavior"], "severity": 1.0}
                },
                "complications": ["self_harm", "substance_abuse", "homelessness"],
                "risk_factors": ["family_history", "urban_environment", "cannabis_use"],
                "progression_rate": 0.005,
                "treatment_responses": {
                    "antipsychotics": {"effectiveness": 0.8, "response_time": 2.0},
                    "psychotherapy": {"effectiveness": 0.5, "response_time": 4.0}
                }
            },
            # rare multi-system: erythromelalgia
            "erythromelalgia": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 12, "symptoms": ["erythromelalgia", "burning_pain"], "severity": 0.3},
                    "moderate": {"duration_hours": 24, "symptoms": ["erythromelalgia", "swelling"], "severity": 0.6},
                    "severe": {"duration_hours": 48, "symptoms": ["erythromelalgia", "ulceration"], "severity": 0.8},
                    "critical": {"duration_hours": 72, "symptoms": ["erythromelalgia", "gangrene"], "severity": 1.0}
                },
                "complications": ["ulceration", "infection", "gangrene"],
                "risk_factors": ["myeloproliferative_disorder", "autoimmune_disease"],
                "progression_rate": 0.05,
                "treatment_responses": {
                    "aspirin": {"effectiveness": 0.7, "response_time": 1.0},
                    "cooling": {"effectiveness": 0.6, "response_time": 0.5}
                }
            },
            # extend complications to allow diseases as side effects
            "pneumonia": {
                "complications": ["sepsis"],
            },
            "influenza": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 24, "symptoms": ["fever", "cough", "fatigue"], "severity": 0.2},
                    "moderate": {"duration_hours": 48, "symptoms": ["fever", "cough", "myalgia", "headache"], "severity": 0.5},
                    "severe": {"duration_hours": 96, "symptoms": ["fever", "shortness_of_breath", "chest_pain"], "severity": 0.8},
                    "critical": {"duration_hours": 168, "symptoms": ["respiratory_failure", "shock"], "severity": 1.0}
                },
                "complications": ["pneumonia", "myocarditis", "encephalitis"],
                "risk_factors": ["elderly", "immunocompromised", "chronic_disease"],
                "progression_rate": 0.08,
                "treatment_responses": {
                    "antivirals": {"effectiveness": 0.7, "response_time": 1.0},
                    "supportive_care": {"effectiveness": 0.6, "response_time": 0.5}
                }
            },
            "diabetes_mellitus": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 720, "symptoms": ["polyuria", "polydipsia", "fatigue"], "severity": 0.2},
                    "moderate": {"duration_hours": 8760, "symptoms": ["polyuria", "blurred_vision", "weight_loss"], "severity": 0.5},
                    "severe": {"duration_hours": 17520, "symptoms": ["polyuria", "neuropathy", "retinopathy"], "severity": 0.8},
                    "critical": {"duration_hours": 26280, "symptoms": ["coma", "multi_organ_failure"], "severity": 1.0}
                },
                "complications": ["diabetic_ketoacidosis", "chronic_kidney_disease", "coronary_artery_disease"],
                "risk_factors": ["obesity", "family_history", "sedentary_lifestyle"],
                "progression_rate": 0.001,
                "treatment_responses": {
                    "insulin": {"effectiveness": 0.95, "response_time": 1.0},
                    "oral_hypoglycemics": {"effectiveness": 0.8, "response_time": 2.0},
                    "lifestyle_modification": {"effectiveness": 0.7, "response_time": 6.0}
                }
            },
            # add more disease-to-disease relationships
            "hypertension": {
                "complications": ["stroke", "heart_failure", "chronic_kidney_disease"],
            },
            "atrial_fibrillation": {
                "complications": ["stroke", "heart_failure"],
            },
            "chronic_kidney_disease": {
                "complications": ["anemia", "bone_disease", "pericarditis"],
            },
            "cirrhosis": {
                "complications": ["hepatic_encephalopathy", "spontaneous_bacterial_peritonitis", "hepatorenal_syndrome"],
            },
            # drug-induced diseases
            "drug_induced_lupus": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 168, "symptoms": ["rash", "joint_pain", "fatigue"], "severity": 0.3},
                    "moderate": {"duration_hours": 720, "symptoms": ["rash", "joint_pain", "fever", "photosensitivity"], "severity": 0.6},
                    "severe": {"duration_hours": 1440, "symptoms": ["rash", "pleuritis", "pericarditis"], "severity": 0.8},
                    "critical": {"duration_hours": 2880, "symptoms": ["nephritis", "central_nervous_system_involvement"], "severity": 1.0}
                },
                "complications": ["nephritis", "pericarditis", "pleuritis"],
                "risk_factors": ["procainamide", "hydralazine", "isoniazid", "minocycline"],
                "progression_rate": 0.01,
                "treatment_responses": {
                    "discontinue_offending_drug": {"effectiveness": 0.9, "response_time": 2.0},
                    "steroids": {"effectiveness": 0.7, "response_time": 1.0}
                }
            },
            "drug_induced_diabetes": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 720, "symptoms": ["polyuria", "polydipsia"], "severity": 0.3},
                    "moderate": {"duration_hours": 1440, "symptoms": ["polyuria", "fatigue", "weight_loss"], "severity": 0.6},
                    "severe": {"duration_hours": 2880, "symptoms": ["polyuria", "blurred_vision", "neuropathy"], "severity": 0.8},
                    "critical": {"duration_hours": 4320, "symptoms": ["diabetic_ketoacidosis", "coma"], "severity": 1.0}
                },
                "complications": ["diabetic_ketoacidosis", "chronic_kidney_disease"],
                "risk_factors": ["steroids", "thiazide_diuretics", "atypical_antipsychotics"],
                "progression_rate": 0.002,
                "treatment_responses": {
                    "discontinue_offending_drug": {"effectiveness": 0.8, "response_time": 3.0},
                    "insulin": {"effectiveness": 0.95, "response_time": 1.0}
                }
            },
            "drug_induced_pneumonitis": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 48, "symptoms": ["cough", "shortness_of_breath"], "severity": 0.3},
                    "moderate": {"duration_hours": 96, "symptoms": ["cough", "shortness_of_breath", "fever"], "severity": 0.6},
                    "severe": {"duration_hours": 168, "symptoms": ["respiratory_distress", "hypoxemia"], "severity": 0.8},
                    "critical": {"duration_hours": 240, "symptoms": ["respiratory_failure", "shock"], "severity": 1.0}
                },
                "complications": ["respiratory_failure", "pulmonary_fibrosis"],
                "risk_factors": ["amiodarone", "nitrofurantoin", "bleomycin", "methotrexate"],
                "progression_rate": 0.05,
                "treatment_responses": {
                    "discontinue_offending_drug": {"effectiveness": 0.8, "response_time": 2.0},
                    "steroids": {"effectiveness": 0.7, "response_time": 1.0}
                }
            },
            "drug_induced_liver_disease": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 168, "symptoms": ["fatigue", "nausea", "abdominal_pain"], "severity": 0.3},
                    "moderate": {"duration_hours": 336, "symptoms": ["jaundice", "easy_bruising", "ascites"], "severity": 0.6},
                    "severe": {"duration_hours": 720, "symptoms": ["hepatic_encephalopathy", "coagulopathy"], "severity": 0.8},
                    "critical": {"duration_hours": 1440, "symptoms": ["liver_failure", "coma"], "severity": 1.0}
                },
                "complications": ["liver_failure", "hepatic_encephalopathy", "coagulopathy"],
                "risk_factors": ["acetaminophen", "statins", "isoniazid", "valproate"],
                "progression_rate": 0.03,
                "treatment_responses": {
                    "discontinue_offending_drug": {"effectiveness": 0.9, "response_time": 1.0},
                    "n_acetylcysteine": {"effectiveness": 0.8, "response_time": 0.5}
                }
            },
            "drug_induced_kidney_disease": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 168, "symptoms": ["fatigue", "nausea"], "severity": 0.3},
                    "moderate": {"duration_hours": 336, "symptoms": ["oliguria", "edema", "hypertension"], "severity": 0.6},
                    "severe": {"duration_hours": 720, "symptoms": ["uremia", "anemia", "bone_disease"], "severity": 0.8},
                    "critical": {"duration_hours": 1440, "symptoms": ["dialysis_dependent", "death"], "severity": 1.0}
                },
                "complications": ["chronic_kidney_disease", "anemia", "bone_disease"],
                "risk_factors": ["nsaids", "aminoglycosides", "contrast_dye", "ace_inhibitors"],
                "progression_rate": 0.02,
                "treatment_responses": {
                    "discontinue_offending_drug": {"effectiveness": 0.8, "response_time": 2.0},
                    "dialysis": {"effectiveness": 0.9, "response_time": 0.5}
                }
            },
            # add more cascading relationships
            "sepsis": {
                "complications": ["acute_respiratory_distress_syndrome", "disseminated_intravascular_coagulation", "acute_kidney_injury"],
            },
            "acute_coronary_syndrome": {
                "complications": ["heart_failure", "cardiogenic_shock", "arrhythmia"],
            },
            "stroke": {
                "complications": ["dysphagia", "aspiration_pneumonia", "deep_vein_thrombosis"],
            },
            "diabetic_ketoacidosis": {
                "complications": ["cerebral_edema", "acute_kidney_injury", "electrolyte_imbalance"],
            },
            # time-sensitive diseases requiring immediate intervention
            "aortic_dissection": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 0.5, "symptoms": ["chest_pain", "syncope"], "severity": 0.4},
                    "moderate": {"duration_hours": 1, "symptoms": ["chest_pain", "hypertension", "pulse_deficit"], "severity": 0.7},
                    "severe": {"duration_hours": 2, "symptoms": ["shock", "organ_malperfusion"], "severity": 0.9},
                    "critical": {"duration_hours": 4, "symptoms": ["death"], "severity": 1.0}
                },
                "complications": ["cardiac_tamponade", "stroke", "mesenteric_ischemia"],
                "risk_factors": ["hypertension", "marfan_syndrome", "trauma"],
                "progression_rate": 0.8,  # very rapid progression
                "treatment_responses": {
                    "surgery": {"effectiveness": 0.9, "response_time": 0.5},
                    "blood_pressure_control": {"effectiveness": 0.7, "response_time": 0.2}
                }
            },
            "tension_pneumothorax": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 0.1, "symptoms": ["chest_pain", "shortness_of_breath"], "severity": 0.5},
                    "moderate": {"duration_hours": 0.2, "symptoms": ["respiratory_distress", "tachycardia"], "severity": 0.8},
                    "severe": {"duration_hours": 0.5, "symptoms": ["shock", "cardiac_arrest"], "severity": 1.0},
                    "critical": {"duration_hours": 1, "symptoms": ["death"], "severity": 1.0}
                },
                "complications": ["cardiac_arrest", "death"],
                "risk_factors": ["trauma", "copd", "mechanical_ventilation"],
                "progression_rate": 2.0,  # extremely rapid
                "treatment_responses": {
                    "needle_decompression": {"effectiveness": 0.95, "response_time": 0.1},
                    "chest_tube": {"effectiveness": 0.9, "response_time": 0.5}
                }
            },
            "cardiac_tamponade": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 0.5, "symptoms": ["chest_pain", "dyspnea"], "severity": 0.4},
                    "moderate": {"duration_hours": 1, "symptoms": ["pulsus_paradoxus", "hypotension"], "severity": 0.7},
                    "severe": {"duration_hours": 2, "symptoms": ["shock", "cardiac_arrest"], "severity": 1.0},
                    "critical": {"duration_hours": 4, "symptoms": ["death"], "severity": 1.0}
                },
                "complications": ["cardiac_arrest", "death"],
                "risk_factors": ["trauma", "pericarditis", "malignancy"],
                "progression_rate": 1.0,
                "treatment_responses": {
                    "pericardiocentesis": {"effectiveness": 0.9, "response_time": 0.3},
                    "surgery": {"effectiveness": 0.95, "response_time": 1.0}
                }
            },
            # more drug-induced diseases
            "drug_induced_stevens_johnson": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 24, "symptoms": ["rash", "fever", "malaise"], "severity": 0.3},
                    "moderate": {"duration_hours": 48, "symptoms": ["rash", "mucosal_involvement", "blistering"], "severity": 0.7},
                    "severe": {"duration_hours": 72, "symptoms": ["extensive_blistering", "sepsis"], "severity": 0.9},
                    "critical": {"duration_hours": 96, "symptoms": ["death"], "severity": 1.0}
                },
                "complications": ["sepsis", "blindness", "death"],
                "risk_factors": ["sulfa_drugs", "anticonvulsants", "allopurinol", "nsaids"],
                "progression_rate": 0.1,
                "treatment_responses": {
                    "discontinue_offending_drug": {"effectiveness": 0.8, "response_time": 1.0},
                    "steroids": {"effectiveness": 0.6, "response_time": 2.0},
                    "burn_unit_care": {"effectiveness": 0.9, "response_time": 0.5}
                }
            },
            "drug_induced_serotonin_syndrome": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 2, "symptoms": ["agitation", "tachycardia", "diaphoresis"], "severity": 0.4},
                    "moderate": {"duration_hours": 4, "symptoms": ["hyperthermia", "rigidity", "tremor"], "severity": 0.7},
                    "severe": {"duration_hours": 6, "symptoms": ["seizures", "rhabdomyolysis"], "severity": 0.9},
                    "critical": {"duration_hours": 8, "symptoms": ["death"], "severity": 1.0}
                },
                "complications": ["rhabdomyolysis", "renal_failure", "death"],
                "risk_factors": ["ssris", "snris", "maois", "triptans"],
                "progression_rate": 0.3,
                "treatment_responses": {
                    "discontinue_offending_drug": {"effectiveness": 0.9, "response_time": 0.5},
                    "cyproheptadine": {"effectiveness": 0.8, "response_time": 1.0},
                    "supportive_care": {"effectiveness": 0.7, "response_time": 0.5}
                }
            },
            "drug_induced_neutropenia": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 168, "symptoms": ["fatigue", "fever"], "severity": 0.3},
                    "moderate": {"duration_hours": 336, "symptoms": ["fever", "infection", "mucosal_ulcers"], "severity": 0.6},
                    "severe": {"duration_hours": 504, "symptoms": ["severe_infection", "sepsis"], "severity": 0.9},
                    "critical": {"duration_hours": 672, "symptoms": ["death"], "severity": 1.0}
                },
                "complications": ["sepsis", "death"],
                "risk_factors": ["chemotherapy", "clozapine", "sulfa_drugs", "antithyroid_medications"],
                "progression_rate": 0.02,
                "treatment_responses": {
                    "discontinue_offending_drug": {"effectiveness": 0.8, "response_time": 2.0},
                    "g_csf": {"effectiveness": 0.9, "response_time": 1.0},
                    "antibiotics": {"effectiveness": 0.8, "response_time": 0.5}
                }
            },
            "drug_induced_qt_prolongation": {
                "stages": {
                    "latent": {"duration_hours": 0, "symptoms": [], "severity": 0.0},
                    "early": {"duration_hours": 24, "symptoms": ["palpitations", "dizziness"], "severity": 0.3},
                    "moderate": {"duration_hours": 48, "symptoms": ["syncope", "arrhythmia"], "severity": 0.7},
                    "severe": {"duration_hours": 72, "symptoms": ["torsades_de_pointes", "cardiac_arrest"], "severity": 0.9},
                    "critical": {"duration_hours": 96, "symptoms": ["death"], "severity": 1.0}
                },
                "complications": ["torsades_de_pointes", "cardiac_arrest", "death"],
                "risk_factors": ["quinidine", "amiodarone", "erythromycin", "antipsychotics"],
                "progression_rate": 0.05,
                "treatment_responses": {
                    "discontinue_offending_drug": {"effectiveness": 0.9, "response_time": 1.0},
                    "magnesium": {"effectiveness": 0.8, "response_time": 0.5},
                    "defibrillation": {"effectiveness": 0.9, "response_time": 0.1}
                }
            },
            # add time-sensitive complications to existing diseases
            "acute_coronary_syndrome": {
                "complications": ["ventricular_fibrillation", "cardiac_rupture"],
            },
            "stroke": {
                "complications": ["herniation", "hydrocephalus"],
            },
            "diabetic_ketoacidosis": {
                "complications": ["cerebral_edema", "cardiac_arrest"],
            }
        })
        return diseases
    
    def _initialize_complication_definitions(self) -> Dict[str, Dict[str, Any]]:
        """initialize complication definitions"""
        complications = super()._initialize_complication_definitions() if hasattr(super(), '_initialize_complication_definitions') else {}
        complications.update({
            "status_epilepticus": {
                "type": ComplicationType.NEUROLOGICAL,
                "risk_factors": ["epilepsy", "encephalitis"],
                "symptoms": ["continuous seizures", "unresponsiveness"],
                "treatments": ["benzodiazepines", "antiepileptics"],
                "severity_range": (0.8, 1.0)
            },
            "acute_chest_syndrome": {
                "type": ComplicationType.RESPIRATORY,
                "risk_factors": ["sickle_cell_disease", "infection"],
                "symptoms": ["chest pain", "hypoxemia", "infiltrates on xray"],
                "treatments": ["oxygen", "antibiotics", "exchange_transfusion"],
                "severity_range": (0.7, 1.0)
            },
            "arrhythmia": {
                "type": ComplicationType.CARDIOVASCULAR,
                "risk_factors": ["myocardial_infarction", "electrolyte_imbalance"],
                "symptoms": ["palpitations", "dizziness", "syncope"],
                "treatments": ["antiarrhythmics", "cardioversion", "pacemaker"],
                "severity_range": (0.4, 0.8)
            },
            "cardiogenic_shock": {
                "type": ComplicationType.CARDIOVASCULAR,
                "risk_factors": ["extensive_mi", "heart_failure"],
                "symptoms": ["hypotension", "cold_extremities", "altered_mental_status"],
                "treatments": ["inotropes", "intra_aortic_balloon_pump", "mechanical_support"],
                "severity_range": (0.8, 1.0)
            },
            "pleural_effusion": {
                "type": ComplicationType.RESPIRATORY,
                "risk_factors": ["pneumonia", "heart_failure", "malignancy"],
                "symptoms": ["shortness_of_breath", "chest_pain", "cough"],
                "treatments": ["thoracentesis", "chest_tube", "diuretics"],
                "severity_range": (0.3, 0.7)
            },
            "cerebral_edema": {
                "type": ComplicationType.NEUROLOGICAL,
                "risk_factors": ["stroke", "trauma", "metabolic_disorder"],
                "symptoms": ["headache", "nausea", "altered_mental_status"],
                "treatments": ["mannitol", "hypertonic_saline", "decompressive_craniectomy"],
                "severity_range": (0.7, 1.0)
            },
            "acute_kidney_injury": {
                "type": ComplicationType.RENAL,
                "risk_factors": ["sepsis", "hypotension", "nephrotoxins"],
                "symptoms": ["oliguria", "edema", "confusion"],
                "treatments": ["fluid_resuscitation", "dialysis", "nephroprotective_measures"],
                "severity_range": (0.5, 0.9)
            }
        })
        return complications
    
    def _initialize_treatment_definitions(self) -> Dict[str, Dict[str, Any]]:
        """initialize treatment definitions"""
        treatments = super()._initialize_treatment_definitions() if hasattr(super(), '_initialize_treatment_definitions') else {}
        treatments.update({
            "ivig": {
                "category": "immunotherapy",
                "effectiveness": 0.8,
                "side_effects": ["headache", "renal_dysfunction"],
                "contraindications": ["selective_iga_deficiency"],
                "dosage": "2g/kg",
                "route": "iv"
            },
            "plasmapheresis": {
                "category": "immunotherapy",
                "effectiveness": 0.6,
                "side_effects": ["hypotension", "bleeding"],
                "contraindications": ["coagulopathy"],
                "dosage": "variable",
                "route": "iv"
            },
            "exchange_transfusion": {
                "category": "hematology",
                "effectiveness": 0.9,
                "side_effects": ["transfusion_reaction", "volume_overload"],
                "contraindications": ["heart_failure"],
                "dosage": "variable",
                "route": "iv"
            },
            "aspirin": {
                "category": "antiplatelet",
                "effectiveness": 0.8,
                "side_effects": ["gastrointestinal_bleeding", "allergic_reaction"],
                "contraindications": ["active_bleeding", "allergy"],
                "dosage": "325mg",
                "route": "oral"
            },
            "nitroglycerin": {
                "category": "vasodilator",
                "effectiveness": 0.7,
                "side_effects": ["headache", "hypotension"],
                "contraindications": ["severe_hypotension", "viagra_use"],
                "dosage": "0.4mg",
                "route": "sublingual"
            },
            "antibiotics": {
                "category": "antimicrobial",
                "effectiveness": 0.85,
                "side_effects": ["diarrhea", "allergic_reaction", "resistance"],
                "contraindications": ["allergy", "pregnancy"],
                "dosage": "variable",
                "route": "iv/oral"
            },
            "insulin": {
                "category": "hormone",
                "effectiveness": 0.95,
                "side_effects": ["hypoglycemia", "weight_gain"],
                "contraindications": ["hypoglycemia"],
                "dosage": "variable",
                "route": "subcutaneous"
            },
            "tpa": {
                "category": "thrombolytic",
                "effectiveness": 0.9,
                "side_effects": ["intracranial_hemorrhage", "systemic_bleeding"],
                "contraindications": ["recent_surgery", "bleeding_disorder"],
                "dosage": "0.9mg/kg",
                "route": "iv"
            }
        })
        return treatments
    
    def initialize_patient_disease(self, patient_id: str, disease_name: str, 
                                 onset_time: Optional[datetime] = None) -> DiseaseState:
        """initialize a disease for a patient"""
        if disease_name not in self.disease_definitions:
            raise ValueError(f"Unknown disease: {disease_name}")
        
        if onset_time is None:
            onset_time = datetime.now()
        
        disease_def = self.disease_definitions[disease_name]
        
        # determine initial stage based on time since onset
        current_time = datetime.now()
        hours_since_onset = (current_time - onset_time).total_seconds() / 3600
        
        # calculate current stage
        stage = self._calculate_disease_stage(disease_def, hours_since_onset)
        
        # calculate severity
        severity = self._calculate_severity(disease_def, stage, hours_since_onset)
        
        disease_state = DiseaseState(
            disease_name=disease_name,
            stage=stage,
            severity_score=severity,
            onset_time=onset_time,
            progression_rate=disease_def["progression_rate"],
            risk_factors=disease_def["risk_factors"],
            prognosis=self._calculate_prognosis(disease_name, stage, severity)
        )
        
        if patient_id not in self.patient_diseases:
            self.patient_diseases[patient_id] = []
        
        self.patient_diseases[patient_id].append(disease_state)
        
        return disease_state
    
    def _calculate_disease_stage(self, disease_def: Dict[str, Any], hours_since_onset: float) -> DiseaseStage:
        """calculate current disease stage based on time"""
        # safety check for diseases without stages
        if "stages" not in disease_def:
            # default staging for diseases without explicit stages
            if hours_since_onset <= 0:
                return DiseaseStage.LATENT
            elif hours_since_onset <= 2:
                return DiseaseStage.EARLY
            elif hours_since_onset <= 6:
                return DiseaseStage.MODERATE
            elif hours_since_onset <= 12:
                return DiseaseStage.SEVERE
            else:
                return DiseaseStage.CRITICAL
        
        stages = disease_def["stages"]
        total_duration = sum(stage["duration_hours"] for stage in stages.values())
        
        if hours_since_onset <= 0:
            return DiseaseStage.LATENT
        elif hours_since_onset <= stages["early"]["duration_hours"]:
            return DiseaseStage.EARLY
        elif hours_since_onset <= stages["moderate"]["duration_hours"]:
            return DiseaseStage.MODERATE
        elif hours_since_onset <= stages["severe"]["duration_hours"]:
            return DiseaseStage.SEVERE
        else:
            return DiseaseStage.CRITICAL
    
    def _calculate_severity(self, disease_def: Dict[str, Any], stage: DiseaseStage, 
                           hours_since_onset: float) -> float:
        """calculate disease severity score"""
        # safety check for diseases without stages
        if "stages" not in disease_def:
            # default severity based on stage
            stage_severity = {
                DiseaseStage.LATENT: 0.1,
                DiseaseStage.EARLY: 0.3,
                DiseaseStage.MODERATE: 0.6,
                DiseaseStage.SEVERE: 0.8,
                DiseaseStage.CRITICAL: 0.95
            }
            base_severity = stage_severity.get(stage, 0.5)
        else:
            stages = disease_def["stages"]
            base_severity = stages[stage.value]["severity"]
        
        # add time-based progression
        time_factor = min(1.0, hours_since_onset / 24.0)  # normalize to 24 hours
        progression_factor = time_factor * 0.3  # max 30% additional severity from time
        
        return min(1.0, base_severity + progression_factor)
    
    def _calculate_prognosis(self, disease_name: str, stage: DiseaseStage, severity: float) -> str:
        """calculate prognosis based on disease state"""
        if stage in [DiseaseStage.LATENT, DiseaseStage.EARLY]:
            return "good"
        elif stage == DiseaseStage.MODERATE:
            return "fair"
        elif stage == DiseaseStage.SEVERE:
            return "poor"
        else:
            return "critical"
    
    def progress_disease(self, patient_id: str, disease_name: str, 
                        time_elapsed: timedelta) -> DiseaseState:
        """progress disease over time"""
        if patient_id not in self.patient_diseases:
            return None
        
        disease_state = None
        for disease in self.patient_diseases[patient_id]:
            if disease.disease_name == disease_name:
                disease_state = disease
                break
        
        if not disease_state:
            return None
        
        # update time and recalculate stage/severity
        hours_elapsed = time_elapsed.total_seconds() / 3600
        disease_def = self.disease_definitions[disease_name]
        
        # update stage
        new_stage = self._calculate_disease_stage(disease_def, hours_elapsed)
        disease_state.stage = new_stage
        
        # update severity
        new_severity = self._calculate_severity(disease_def, new_stage, hours_elapsed)
        disease_state.severity_score = new_severity
        
        # update prognosis
        disease_state.prognosis = self._calculate_prognosis(disease_name, new_stage, new_severity)
        disease_state.last_updated = datetime.now()
        
        # check for complications
        self._check_for_complications(patient_id, disease_state)
        
        return disease_state
    
    def _check_for_complications(self, patient_id: str, disease_state: DiseaseState):
        """check for development of complications"""
        disease_def = self.disease_definitions[disease_state.disease_name]
        complications = disease_def["complications"]
        
        # higher severity increases complication risk
        complication_risk = disease_state.severity_score * 0.3
        
        for complication_name in complications:
            if random.random() < complication_risk:
                self._develop_complication(patient_id, complication_name, disease_state)
    
    def _develop_complication(self, patient_id: str, complication_name: str, 
                            disease_state: DiseaseState):
        """develop a specific complication"""
        if complication_name not in self.complication_definitions:
            return
        
        comp_def = self.complication_definitions[complication_name]
        
        # check if complication already exists
        if patient_id in self.patient_complications:
            for comp in self.patient_complications[patient_id]:
                if comp.name == complication_name:
                    return  # already exists
        
        severity = random.uniform(*comp_def["severity_range"])
        
        complication = Complication(
            complication_type=comp_def["type"],
            name=complication_name,
            severity=severity,
            onset_time=datetime.now(),
            risk_factors=comp_def["risk_factors"],
            symptoms=comp_def["symptoms"],
            treatments=comp_def["treatments"],
            prognosis="variable"
        )
        
        if patient_id not in self.patient_complications:
            self.patient_complications[patient_id] = []
        
        self.patient_complications[patient_id].append(complication)
        disease_state.complications.append(complication_name)
    
    def administer_treatment(self, patient_id: str, treatment_name: str, 
                           dosage: str = None, route: str = None) -> TreatmentEffect:
        """administer a treatment and calculate its effect"""
        if treatment_name not in self.treatment_definitions:
            return None
        
        treatment_def = self.treatment_definitions[treatment_name]
        
        # calculate treatment response
        base_effectiveness = treatment_def["effectiveness"]
        
        # modify based on disease state
        disease_modifier = self._calculate_disease_treatment_modifier(patient_id)
        effectiveness = min(1.0, base_effectiveness * disease_modifier)
        
        # determine response type
        if effectiveness >= 0.8:
            response_type = TreatmentResponse.EXCELLENT
        elif effectiveness >= 0.6:
            response_type = TreatmentResponse.GOOD
        elif effectiveness >= 0.4:
            response_type = TreatmentResponse.MODERATE
        elif effectiveness >= 0.2:
            response_type = TreatmentResponse.POOR
        else:
            response_type = TreatmentResponse.RESISTANT
        
        # generate side effects
        side_effects = self._generate_side_effects(treatment_def, effectiveness)
        
        treatment_effect = TreatmentEffect(
            treatment_name=treatment_name,
            response_type=response_type,
            effectiveness=effectiveness,
            side_effects=side_effects,
            duration=timedelta(hours=4),  # default duration
            administered_time=datetime.now(),
            dosage=dosage or treatment_def["dosage"],
            route=route or treatment_def["route"]
        )
        
        if patient_id not in self.patient_treatments:
            self.patient_treatments[patient_id] = []
        
        self.patient_treatments[patient_id].append(treatment_effect)
        
        # update disease state based on treatment
        self._apply_treatment_effect(patient_id, treatment_effect)
        
        return treatment_effect
    
    def _calculate_disease_treatment_modifier(self, patient_id: str) -> float:
        """calculate modifier for treatment effectiveness based on disease state"""
        if patient_id not in self.patient_diseases:
            return 1.0
        
        # more severe disease may reduce treatment effectiveness
        max_severity = max(d.severity_score for d in self.patient_diseases[patient_id])
        modifier = 1.0 - (max_severity * 0.3)  # max 30% reduction
        
        return max(0.1, modifier)  # minimum 10% effectiveness
    
    def _generate_side_effects(self, treatment_def: Dict[str, Any], effectiveness: float) -> List[str]:
        """generate side effects for a treatment"""
        side_effects = []
        base_side_effects = treatment_def["side_effects"]
        
        # higher effectiveness may reduce side effects
        side_effect_probability = 0.3 * (1.0 - effectiveness)
        
        for side_effect in base_side_effects:
            if random.random() < side_effect_probability:
                side_effects.append(side_effect)
        
        return side_effects
    
    def _apply_treatment_effect(self, patient_id: str, treatment_effect: TreatmentEffect):
        """apply treatment effect to disease state"""
        if patient_id not in self.patient_diseases:
            return
        
        # find appropriate disease to treat
        for disease_state in self.patient_diseases[patient_id]:
            disease_def = self.disease_definitions[disease_state.disease_name]
            
            if treatment_effect.treatment_name in disease_def["treatment_responses"]:
                # apply treatment effect
                treatment_response = disease_def["treatment_responses"][treatment_effect.treatment_name]
                
                # reduce severity based on treatment effectiveness
                severity_reduction = treatment_effect.effectiveness * 0.3
                disease_state.severity_score = max(0.0, disease_state.severity_score - severity_reduction)
                
                # update prognosis
                disease_state.prognosis = self._calculate_prognosis(
                    disease_state.disease_name, 
                    disease_state.stage, 
                    disease_state.severity_score
                )
                
                # record treatment
                disease_state.treatment_history.append({
                    "treatment": treatment_effect.treatment_name,
                    "effectiveness": treatment_effect.effectiveness,
                    "administered": treatment_effect.administered_time,
                    "response": treatment_effect.response_type.value
                })
                
                break
    
    def get_patient_disease_summary(self, patient_id: str) -> Dict[str, Any]:
        """get comprehensive disease summary for a patient"""
        diseases = self.patient_diseases.get(patient_id, [])
        complications = self.patient_complications.get(patient_id, [])
        treatments = self.patient_treatments.get(patient_id, [])
        
        return {
            "active_diseases": [
                {
                    "name": d.disease_name,
                    "stage": d.stage.value,
                    "severity": d.severity_score,
                    "prognosis": d.prognosis,
                    "complications": d.complications,
                    "risk_factors": d.risk_factors
                }
                for d in diseases
            ],
            "complications": [
                {
                    "name": c.name,
                    "type": c.complication_type.value,
                    "severity": c.severity,
                    "symptoms": c.symptoms,
                    "treatments": c.treatments
                }
                for c in complications
            ],
            "recent_treatments": [
                {
                    "name": t.treatment_name,
                    "response": t.response_type.value,
                    "effectiveness": t.effectiveness,
                    "side_effects": t.side_effects,
                    "administered": t.administered_time.isoformat()
                }
                for t in treatments[-5:]  # last 5 treatments
            ],
            "overall_prognosis": self._calculate_overall_prognosis(diseases, complications)
        }
    
    def _calculate_overall_prognosis(self, diseases: List[DiseaseState], 
                                   complications: List[Complication]) -> str:
        """calculate overall prognosis for patient"""
        if not diseases:
            return "healthy"
        
        # consider disease severity and complications
        max_severity = max(d.severity_score for d in diseases)
        complication_count = len(complications)
        
        if max_severity >= 0.8 or complication_count >= 3:
            return "critical"
        elif max_severity >= 0.6 or complication_count >= 2:
            return "poor"
        elif max_severity >= 0.4 or complication_count >= 1:
            return "fair"
        else:
            return "good"
    
    def get_available_diseases(self) -> List[str]:
        """get list of available diseases"""
        return list(self.disease_definitions.keys())
    
    def get_available_complications(self) -> List[str]:
        """get list of available complications"""
        return list(self.complication_definitions.keys())
    
    def get_available_treatments(self) -> List[str]:
        """get list of available treatments"""
        return list(self.treatment_definitions.keys()) 