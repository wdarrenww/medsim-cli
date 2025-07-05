"""
dynamic patient loader for generating realistic patient profiles
with disease progression, social determinants, and complex medical histories
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import random
import json
import math

from .patient import EnhancedPatientProfile, PatientProfileGenerator
from .disease_progression import DiseaseProgressionEngine, DiseaseState, Complication
from ..data.clinical_patterns import ClinicalPatterns


@dataclass
class PatientLoadConfig:
    """configuration for dynamic patient loading"""
    specialty: Optional[str] = None
    difficulty: str = "medium"
    age_range: Optional[Tuple[int, int]] = None
    gender: Optional[str] = None
    complexity_level: str = "moderate"  # simple, moderate, complex
    social_determinants: bool = True
    comorbidities: bool = True
    disease_progression: bool = True
    realistic_vitals: bool = True
    medication_history: bool = True


@dataclass
class PatientLoadResult:
    """result of dynamic patient loading"""
    patient: EnhancedPatientProfile
    disease_states: List[DiseaseState]
    complications: List[Complication]
    social_context: Dict[str, Any]
    medical_complexity: float
    risk_score: float
    realistic_factors: Dict[str, Any]


class DynamicPatientLoader:
    """dynamic patient loader with realistic medical complexity"""
    
    def __init__(self):
        self.patient_generator = PatientProfileGenerator()
        self.disease_engine = DiseaseProgressionEngine()
        self.patterns = ClinicalPatterns()
        
        # social determinant templates
        self.social_determinants = {
            "poverty": {
                "frequency": 0.15,
                "effects": ["limited_access_to_care", "medication_noncompliance", "delayed_presentation"],
                "risk_multiplier": 1.5
            },
            "homelessness": {
                "frequency": 0.05,
                "effects": ["poor_hygiene", "exposure", "substance_abuse"],
                "risk_multiplier": 2.0
            },
            "language_barriers": {
                "frequency": 0.12,
                "effects": ["communication_difficulty", "misunderstanding_instructions"],
                "risk_multiplier": 1.3
            },
            "transportation_barriers": {
                "frequency": 0.08,
                "effects": ["missed_appointments", "delayed_care"],
                "risk_multiplier": 1.4
            },
            "food_insecurity": {
                "frequency": 0.10,
                "effects": ["malnutrition", "diabetes_control_issues"],
                "risk_multiplier": 1.6
            },
            "social_isolation": {
                "frequency": 0.07,
                "effects": ["depression", "lack_of_support"],
                "risk_multiplier": 1.2
            },
            "discrimination": {
                "frequency": 0.05,
                "effects": ["mistrust_in_healthcare", "delayed_care"],
                "risk_multiplier": 1.3
            },
            "health_literacy": {
                "frequency": 0.10,
                "effects": ["misunderstanding_instructions", "poor_compliance"],
                "risk_multiplier": 1.2
            },
            "housing_insecurity": {
                "frequency": 0.07,
                "effects": ["unstable_housing", "missed_appointments"],
                "risk_multiplier": 1.4
            }
        }
        
        # mapping from string keys to enum values
        self.social_determinant_mapping = {
            "poverty": "POVERTY",
            "homelessness": "HOUSING_INSECURITY",  # closest match
            "language_barriers": "LANGUAGE_BARRIERS",
            "transportation_barriers": "TRANSPORTATION_BARRIERS",
            "food_insecurity": "FOOD_INSECURITY",
            "social_isolation": "SOCIAL_ISOLATION",
            "discrimination": "DISCRIMINATION",
            "health_literacy": "HEALTH_LITERACY",
            "housing_insecurity": "HOUSING_INSECURITY"
        }
        
        # comorbidity patterns
        self.comorbidity_patterns = {
            "diabetes": {
                "common_comorbidities": ["hypertension", "hyperlipidemia", "diabetic_retinopathy"],
                "risk_factors": ["obesity", "family_history", "sedentary_lifestyle"]
            },
            "hypertension": {
                "common_comorbidities": ["diabetes", "heart_disease", "chronic_kidney_disease"],
                "risk_factors": ["age", "obesity", "high_salt_diet"]
            },
            "copd": {
                "common_comorbidities": ["heart_failure", "pneumonia", "depression"],
                "risk_factors": ["smoking", "environmental_exposure", "age"]
            },
            "heart_failure": {
                "common_comorbidities": ["hypertension", "diabetes", "atrial_fibrillation"],
                "risk_factors": ["previous_mi", "valvular_disease", "age"]
            },
            "systemic lupus erythematosus": {
                "common_comorbidities": ["renal_failure", "anemia", "vasculitis"],
                "risk_factors": ["female", "african_ancestry", "autoimmune_disorder"]
            },
            "hiv/aids": {
                "common_comorbidities": ["opportunistic_infection", "lymphoma", "neuropathy"],
                "risk_factors": ["unprotected_sex", "iv_drug_use"]
            }
        }
        
        # medication interaction patterns
        self.medication_interactions = {
            "warfarin": {
                "interactions": ["aspirin", "nsaids", "antibiotics"],
                "monitoring": ["inr", "bleeding_signs"]
            },
            "insulin": {
                "interactions": ["steroids", "beta_blockers"],
                "monitoring": ["blood_glucose", "hypoglycemia_signs"]
            },
            "digoxin": {
                "interactions": ["diuretics", "amiodarone"],
                "monitoring": ["digoxin_level", "cardiac_signs"]
            },
            "methotrexate": {
                "interactions": ["trimethoprim", "NSAIDs"],
                "monitoring": ["liver_function", "cbc"]
            },
            "warfarin": {
                "interactions": ["amiodarone", "antibiotics", "antifungals"],
                "monitoring": ["inr", "bleeding_signs"]
            }
        }
    
    def load_patient(self, config: PatientLoadConfig) -> PatientLoadResult:
        """load a dynamic patient with realistic complexity"""
        # generate base patient
        patient = self._generate_base_patient(config)
        
        # add social determinants
        social_context = self._add_social_determinants(patient, config)
        
        # add disease progression
        disease_states = self._add_disease_progression(patient, config)
        
        # add complications
        complications = self._add_complications(patient, disease_states, config)
        
        # add comorbidities
        if config.comorbidities:
            self._add_comorbidities(patient, config)
        
        # add medication history
        if config.medication_history:
            self._add_medication_history(patient, config)
        
        # adjust vitals for realism
        if config.realistic_vitals:
            self._adjust_vitals_for_realism(patient, disease_states)
        
        # calculate complexity and risk
        medical_complexity = self._calculate_medical_complexity(patient, disease_states, complications)
        risk_score = self._calculate_risk_score(patient, disease_states, social_context)
        
        # add realistic factors
        realistic_factors = self._add_realistic_factors(patient, disease_states, social_context)
        
        return PatientLoadResult(
            patient=patient,
            disease_states=disease_states,
            complications=complications,
            social_context=social_context,
            medical_complexity=medical_complexity,
            risk_score=risk_score,
            realistic_factors=realistic_factors
        )
    
    def _generate_base_patient(self, config: PatientLoadConfig) -> EnhancedPatientProfile:
        """generate base patient profile"""
        if config.specialty:
            patient = self.patient_generator.generate_patient_by_specialty(
                config.specialty, config.difficulty
            )
        else:
            patient = self.patient_generator.generate_patient_by_difficulty(config.difficulty)
        
        # override age/gender if specified
        if config.age_range:
            patient.age = random.randint(*config.age_range)
            # recalculate birth date
            from datetime import date
            today = date.today()
            birth_year = today.year - patient.age
            patient.date_of_birth = date(birth_year, random.randint(1, 12), random.randint(1, 28))
        
        if config.gender:
            patient.gender = config.gender
        
        return patient
    
    def _add_social_determinants(self, patient: EnhancedPatientProfile, 
                                config: PatientLoadConfig) -> Dict[str, Any]:
        """add social determinants of health"""
        if not config.social_determinants:
            return {}
        
        social_context = {
            "determinants": [],
            "effects": [],
            "risk_multiplier": 1.0
        }
        
        # add social determinants based on frequency
        for determinant, data in self.social_determinants.items():
            if random.random() < data["frequency"]:
                # convert string to SocialDeterminant enum using mapping
                from ..core.patient import SocialDeterminant
                enum_key = self.social_determinant_mapping.get(determinant, determinant.upper())
                try:
                    determinant_enum = SocialDeterminant[enum_key]
                    patient.social_history.social_determinants.append(determinant_enum)
                    social_context["determinants"].append(determinant)
                    social_context["effects"].extend(data["effects"])
                    social_context["risk_multiplier"] *= data["risk_multiplier"]
                except KeyError:
                    # skip invalid determinants
                    continue
        
        # add specific social context based on determinants
        if "poverty" in social_context["determinants"]:
            patient.social_history.insurance_status = "Medicaid"
            patient.social_history.occupation = random.choice(["Unemployed", "Part-time", "Service Worker"])
        
        if "homelessness" in social_context["determinants"]:
            patient.social_history.occupation = "Unemployed"
            patient.social_history.marital_status = "Single"
        
        if "language_barriers" in social_context["determinants"]:
            patient.social_history.primary_language = random.choice(["Spanish", "French", "Mandarin"])
            patient.personality.health_literacy = "low"
        
        return social_context
    
    def _add_disease_progression(self, patient: EnhancedPatientProfile, 
                                config: PatientLoadConfig) -> List[DiseaseState]:
        """add disease progression based on specialty and complexity"""
        disease_states = []
        
        if not config.disease_progression:
            return disease_states
        
        # determine number of diseases based on complexity
        if config.complexity_level == "simple":
            num_diseases = random.randint(0, 1)
        elif config.complexity_level == "moderate":
            num_diseases = random.randint(1, 2)
        else:  # complex
            num_diseases = random.randint(2, 4)
        
        # get appropriate diseases for specialty
        if config.specialty:
            specialty_patterns = self.patterns.get_patterns_by_specialty(config.specialty)
            available_diseases = []
            
            for pattern_name, pattern_data in specialty_patterns.items():
                if isinstance(pattern_data, dict) and 'diagnoses' in pattern_data:
                    diagnoses = pattern_data['diagnoses']
                    for diagnosis in diagnoses:
                        if isinstance(diagnosis, dict) and 'diagnosis' in diagnosis:
                            disease_name = self._map_diagnosis_to_disease(diagnosis['diagnosis'])
                            if disease_name:
                                available_diseases.append(disease_name)
        else:
            available_diseases = self.disease_engine.get_available_diseases()
        
        # select diseases
        selected_diseases = random.sample(available_diseases, min(num_diseases, len(available_diseases)))
        
        for disease_name in selected_diseases:
            # determine onset time (more recent for acute conditions)
            if disease_name in ["acute_coronary_syndrome", "stroke", "sepsis"]:
                onset_hours_ago = random.uniform(0.5, 6.0)
            else:
                onset_hours_ago = random.uniform(1.0, 72.0)
            
            onset_time = datetime.now() - timedelta(hours=onset_hours_ago)
            
            # initialize disease
            disease_state = self.disease_engine.initialize_patient_disease(
                patient.patient_id, disease_name, onset_time
            )
            
            # progress disease to current time
            self.disease_engine.progress_disease(
                patient.patient_id, disease_name, timedelta(hours=onset_hours_ago)
            )
            
            disease_states.append(disease_state)
            
            # add symptoms to patient
            disease_def = self.disease_engine.disease_definitions[disease_name]
            current_stage = disease_state.stage.value
            if current_stage in disease_def["stages"]:
                symptoms = disease_def["stages"][current_stage]["symptoms"]
                patient.symptoms.extend(symptoms)
            
            # add conditions to patient
            patient.conditions.append(disease_name.replace("_", " ").title())
        
        return disease_states
    
    def _add_complications(self, patient: EnhancedPatientProfile, 
                          disease_states: List[DiseaseState], 
                          config: PatientLoadConfig) -> List[Complication]:
        """add complications based on disease states"""
        complications = []
        
        for disease_state in disease_states:
            # check for complications based on disease severity
            if disease_state.severity_score > 0.7:
                # high risk for complications
                complication_risk = 0.4
            elif disease_state.severity_score > 0.4:
                # moderate risk
                complication_risk = 0.2
            else:
                # low risk
                complication_risk = 0.05
            
            if random.random() < complication_risk:
                # select appropriate complication
                available_complications = self.disease_engine.get_available_complications()
                if available_complications:
                    complication_name = random.choice(available_complications)
                    
                    # check if complication is appropriate for this disease
                    disease_def = self.disease_engine.disease_definitions[disease_state.disease_name]
                    if complication_name in disease_def.get("complications", []):
                        # develop complication
                        self.disease_engine._develop_complication(
                            patient.patient_id, complication_name, disease_state
                        )
                        
                        # get the complication object
                        if patient.patient_id in self.disease_engine.patient_complications:
                            for comp in self.disease_engine.patient_complications[patient.patient_id]:
                                if comp.name == complication_name:
                                    complications.append(comp)
                                    break
        
        return complications
    
    def _add_comorbidities(self, patient: EnhancedPatientProfile, config: PatientLoadConfig):
        """add comorbidities based on existing conditions"""
        for condition in patient.conditions:
            condition_lower = condition.lower()
            
            for comorbidity_condition, pattern in self.comorbidity_patterns.items():
                if comorbidity_condition in condition_lower:
                    # add common comorbidities
                    for comorbidity in pattern["common_comorbidities"]:
                        if random.random() < 0.3:  # 30% chance per comorbidity
                            if comorbidity not in patient.conditions:
                                patient.conditions.append(comorbidity)
                    
                    # add risk factors
                    for risk_factor in pattern["risk_factors"]:
                        if random.random() < 0.4:  # 40% chance per risk factor
                            if risk_factor not in patient.conditions:
                                patient.conditions.append(risk_factor)
    
    def _add_medication_history(self, patient: EnhancedPatientProfile, config: PatientLoadConfig):
        """add realistic medication history"""
        medications = []
        
        # add medications based on conditions
        for condition in patient.conditions:
            condition_lower = condition.lower()
            
            if "diabetes" in condition_lower:
                medications.extend(["metformin", "insulin", "glipizide"])
            elif "hypertension" in condition_lower:
                medications.extend(["lisinopril", "amlodipine", "hydrochlorothiazide"])
            elif "copd" in condition_lower:
                medications.extend(["albuterol", "tiotropium", "prednisone"])
            elif "heart_failure" in condition_lower:
                medications.extend(["furosemide", "carvedilol", "lisinopril"])
            elif "depression" in condition_lower:
                medications.extend(["sertraline", "fluoxetine", "bupropion"])
        
        # add common medications based on age
        if patient.age > 65:
            medications.extend(["aspirin", "vitamin_d", "calcium"])
        
        # add medications based on social determinants
        if any("poverty" in d.value for d in patient.social_history.social_determinants):
            # may have limited access to medications
            medications = medications[:2]  # fewer medications
        
        # add to patient
        patient.medications = list(set(medications))  # remove duplicates
    
    def _adjust_vitals_for_realism(self, patient: EnhancedPatientProfile, 
                                  disease_states: List[DiseaseState]):
        """adjust vital signs for disease states"""
        # start with baseline vitals
        vitals = {
            "heart_rate": 70,
            "bp_systolic": 120,
            "bp_diastolic": 80,
            "respiratory_rate": 16,
            "oxygen_saturation": 98,
            "temperature": 98.6
        }
        
        # adjust based on disease states
        for disease_state in disease_states:
            disease_name = disease_state.disease_name
            severity = disease_state.severity_score
            
            if "coronary" in disease_name:
                vitals["heart_rate"] += int(severity * 30)
                vitals["bp_systolic"] += int(severity * 40)
                vitals["bp_diastolic"] += int(severity * 20)
            
            elif "pneumonia" in disease_name:
                vitals["respiratory_rate"] += int(severity * 10)
                vitals["oxygen_saturation"] -= int(severity * 8)
                vitals["temperature"] += severity * 3
            
            elif "sepsis" in disease_name:
                vitals["heart_rate"] += int(severity * 40)
                vitals["respiratory_rate"] += int(severity * 15)
                vitals["temperature"] += severity * 4
                vitals["bp_systolic"] -= int(severity * 20)
            
            elif "stroke" in disease_name:
                vitals["bp_systolic"] += int(severity * 30)
                vitals["heart_rate"] += int(severity * 15)
        
        # add random variation
        vitals["heart_rate"] += random.randint(-5, 5)
        vitals["bp_systolic"] += random.randint(-10, 10)
        vitals["bp_diastolic"] += random.randint(-5, 5)
        vitals["respiratory_rate"] += random.randint(-2, 2)
        vitals["oxygen_saturation"] += random.randint(-2, 2)
        vitals["temperature"] += random.uniform(-0.5, 0.5)
        
        # ensure realistic ranges
        vitals["heart_rate"] = max(40, min(180, vitals["heart_rate"]))
        vitals["bp_systolic"] = max(80, min(200, vitals["bp_systolic"]))
        vitals["bp_diastolic"] = max(50, min(120, vitals["bp_diastolic"]))
        vitals["respiratory_rate"] = max(8, min(40, vitals["respiratory_rate"]))
        vitals["oxygen_saturation"] = max(85, min(100, vitals["oxygen_saturation"]))
        vitals["temperature"] = max(95, min(105, vitals["temperature"]))
        
        # update patient vitals
        patient.vital_signs = vitals
    
    def _calculate_medical_complexity(self, patient: EnhancedPatientProfile, 
                                    disease_states: List[DiseaseState], 
                                    complications: List[Complication]) -> float:
        """calculate medical complexity score"""
        complexity = 0.0
        
        # base complexity from age
        if patient.age > 80:
            complexity += 0.3
        elif patient.age > 65:
            complexity += 0.2
        elif patient.age < 18:
            complexity += 0.1
        
        # complexity from number of conditions
        complexity += len(patient.conditions) * 0.1
        
        # complexity from disease severity
        for disease_state in disease_states:
            complexity += disease_state.severity_score * 0.2
        
        # complexity from complications
        complexity += len(complications) * 0.15
        
        # complexity from social determinants
        social_determinants = len(patient.social_history.social_determinants)
        complexity += social_determinants * 0.1
        
        # complexity from medications
        complexity += len(patient.medications) * 0.05
        
        return min(1.0, complexity)
    
    def _calculate_risk_score(self, patient: EnhancedPatientProfile, 
                            disease_states: List[DiseaseState], 
                            social_context: Dict[str, Any]) -> float:
        """calculate overall risk score"""
        risk = 0.0
        
        # age risk
        if patient.age > 80:
            risk += 0.4
        elif patient.age > 65:
            risk += 0.2
        
        # disease severity risk
        for disease_state in disease_states:
            risk += disease_state.severity_score * 0.3
        
        # social determinant risk
        risk *= social_context.get("risk_multiplier", 1.0)
        
        # condition risk
        high_risk_conditions = ["diabetes", "hypertension", "heart_failure", "copd"]
        for condition in patient.conditions:
            if any(hrc in condition.lower() for hrc in high_risk_conditions):
                risk += 0.1
        
        return min(1.0, risk)
    
    def _add_realistic_factors(self, patient: EnhancedPatientProfile, 
                              disease_states: List[DiseaseState], 
                              social_context: Dict[str, Any]) -> Dict[str, Any]:
        """add realistic factors to patient"""
        realistic_factors = {
            "presentation_delay": self._calculate_presentation_delay(social_context),
            "medication_compliance": self._calculate_medication_compliance(social_context),
            "follow_up_likelihood": self._calculate_follow_up_likelihood(social_context),
            "health_literacy": patient.personality.health_literacy,
            "communication_barriers": len([d for d in social_context.get("determinants", []) 
                                        if "language" in d or "barrier" in d])
        }
        
        return realistic_factors
    
    def _calculate_presentation_delay(self, social_context: Dict[str, Any]) -> float:
        """calculate delay in seeking care"""
        delay = 0.0
        
        determinants = social_context.get("determinants", [])
        
        if "poverty" in determinants:
            delay += 2.0  # hours
        if "homelessness" in determinants:
            delay += 4.0
        if "transportation_barriers" in determinants:
            delay += 1.5
        if "language_barriers" in determinants:
            delay += 1.0
        
        return delay
    
    def _calculate_medication_compliance(self, social_context: Dict[str, Any]) -> float:
        """calculate medication compliance rate"""
        compliance = 0.8  # baseline
        
        determinants = social_context.get("determinants", [])
        
        if "poverty" in determinants:
            compliance -= 0.2
        if "homelessness" in determinants:
            compliance -= 0.4
        if "language_barriers" in determinants:
            compliance -= 0.1
        
        return max(0.1, compliance)
    
    def _calculate_follow_up_likelihood(self, social_context: Dict[str, Any]) -> float:
        """calculate likelihood of follow-up care"""
        likelihood = 0.7  # baseline
        
        determinants = social_context.get("determinants", [])
        
        if "poverty" in determinants:
            likelihood -= 0.2
        if "transportation_barriers" in determinants:
            likelihood -= 0.3
        if "homelessness" in determinants:
            likelihood -= 0.4
        
        return max(0.1, likelihood)
    
    def _map_diagnosis_to_disease(self, diagnosis: str) -> Optional[str]:
        """map diagnosis to disease name"""
        diagnosis_lower = diagnosis.lower()
        
        mapping = {
            "stemi": "acute_coronary_syndrome",
            "nstemi": "acute_coronary_syndrome",
            "pneumonia": "pneumonia",
            "copd exacerbation": "pneumonia",  # treat as similar
            "diabetic ketoacidosis": "diabetic_ketoacidosis",
            "sepsis": "sepsis",
            "stroke": "stroke",
            "ischemic stroke": "stroke"
        }
        
        for key, disease in mapping.items():
            if key in diagnosis_lower:
                return disease
        
        return None
    
    def get_patient_summary(self, patient_id: str) -> Dict[str, Any]:
        """get comprehensive patient summary"""
        disease_summary = self.disease_engine.get_patient_disease_summary(patient_id)
        
        return {
            "patient_id": patient_id,
            "disease_summary": disease_summary,
            "social_context": disease_summary.get("social_context", {}),
            "medical_complexity": disease_summary.get("medical_complexity", 0.0),
            "risk_score": disease_summary.get("risk_score", 0.0)
        } 