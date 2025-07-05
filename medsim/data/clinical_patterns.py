"""
clinical patterns and templates for scenario generation
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)


@dataclass
class ClinicalTemplate:
    """template for generating clinical scenarios"""
    template_id: str
    name: str
    specialty: str
    difficulty: str
    description: str
    demographics_range: Dict[str, Any]
    symptom_templates: List[Dict[str, Any]]
    diagnosis_templates: List[Dict[str, Any]]
    treatment_templates: List[Dict[str, Any]]
    outcome_templates: List[Dict[str, Any]]
    temporal_templates: List[Dict[str, Any]]
    learning_objectives: List[str]
    key_actions: List[str]
    complications: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)


class ClinicalPatterns:
    """manages clinical patterns and templates for scenario generation"""
    
    def __init__(self):
        self.templates: Dict[str, ClinicalTemplate] = {}
        self.pattern_library: Dict[str, Dict[str, Any]] = {}
        self._initialize_patterns()
    
    def _initialize_patterns(self):
        """initialize clinical pattern library"""
        self.pattern_library = {
            'emergency_medicine': {
                'chest_pain': {
                    'frequency': 0.15,
                    'demographics': {
                        'age_range': (40, 80),
                        'gender_distribution': {'male': 0.6, 'female': 0.4},
                        'risk_factors': ['hypertension', 'diabetes', 'smoking', 'hyperlipidemia']
                    },
                    'symptom_clusters': [
                        {
                            'symptoms': ['chest pain', 'shortness of breath', 'sweating'],
                            'frequency': 0.4,
                            'severity': 'high'
                        },
                        {
                            'symptoms': ['chest pain', 'nausea', 'vomiting'],
                            'frequency': 0.3,
                            'severity': 'medium'
                        }
                    ],
                    'diagnoses': [
                        {'diagnosis': 'STEMI', 'frequency': 0.3, 'difficulty': 'hard'},
                        {'diagnosis': 'NSTEMI', 'frequency': 0.4, 'difficulty': 'medium'},
                        {'diagnosis': 'stable angina', 'frequency': 0.2, 'difficulty': 'easy'},
                        {'diagnosis': 'aortic dissection', 'frequency': 0.1, 'difficulty': 'hard'}
                    ],
                    'treatments': [
                        {'treatment': 'aspirin', 'frequency': 0.9, 'timing': 'immediate'},
                        {'treatment': 'nitroglycerin', 'frequency': 0.7, 'timing': 'immediate'},
                        {'treatment': 'cardiac catheterization', 'frequency': 0.5, 'timing': 'urgent'},
                        {'treatment': 'thrombolytics', 'frequency': 0.3, 'timing': 'urgent'}
                    ]
                },
                'shortness_of_breath': {
                    'frequency': 0.12,
                    'demographics': {
                        'age_range': (50, 85),
                        'gender_distribution': {'male': 0.45, 'female': 0.55},
                        'risk_factors': ['copd', 'asthma', 'heart_failure', 'smoking']
                    },
                    'symptom_clusters': [
                        {
                            'symptoms': ['shortness of breath', 'cough', 'wheezing'],
                            'frequency': 0.5,
                            'severity': 'medium'
                        },
                        {
                            'symptoms': ['shortness of breath', 'chest pain', 'anxiety'],
                            'frequency': 0.3,
                            'severity': 'high'
                        }
                    ],
                    'diagnoses': [
                        {'diagnosis': 'copd exacerbation', 'frequency': 0.4, 'difficulty': 'medium'},
                        {'diagnosis': 'pneumonia', 'frequency': 0.3, 'difficulty': 'medium'},
                        {'diagnosis': 'pulmonary embolism', 'frequency': 0.2, 'difficulty': 'hard'},
                        {'diagnosis': 'heart failure', 'frequency': 0.1, 'difficulty': 'medium'}
                    ],
                    'treatments': [
                        {'treatment': 'oxygen therapy', 'frequency': 0.8, 'timing': 'immediate'},
                        {'treatment': 'albuterol nebulizer', 'frequency': 0.7, 'timing': 'immediate'},
                        {'treatment': 'steroids', 'frequency': 0.6, 'timing': 'urgent'},
                        {'treatment': 'antibiotics', 'frequency': 0.4, 'timing': 'urgent'}
                    ]
                },
                'abdominal_pain': {
                    'frequency': 0.10,
                    'demographics': {
                        'age_range': (20, 70),
                        'gender_distribution': {'male': 0.5, 'female': 0.5},
                        'risk_factors': ['previous_surgery', 'inflammatory_bowel_disease']
                    },
                    'symptom_clusters': [
                        {
                            'symptoms': ['abdominal pain', 'nausea', 'vomiting'],
                            'frequency': 0.6,
                            'severity': 'medium'
                        },
                        {
                            'symptoms': ['abdominal pain', 'fever', 'chills'],
                            'frequency': 0.3,
                            'severity': 'high'
                        }
                    ],
                    'diagnoses': [
                        {'diagnosis': 'appendicitis', 'frequency': 0.3, 'difficulty': 'easy'},
                        {'diagnosis': 'cholecystitis', 'frequency': 0.25, 'difficulty': 'medium'},
                        {'diagnosis': 'diverticulitis', 'frequency': 0.2, 'difficulty': 'medium'},
                        {'diagnosis': 'bowel obstruction', 'frequency': 0.15, 'difficulty': 'hard'},
                        {'diagnosis': 'peritonitis', 'frequency': 0.1, 'difficulty': 'hard'}
                    ],
                    'treatments': [
                        {'treatment': 'pain medication', 'frequency': 0.8, 'timing': 'immediate'},
                        {'treatment': 'antibiotics', 'frequency': 0.6, 'timing': 'urgent'},
                        {'treatment': 'surgical consultation', 'frequency': 0.5, 'timing': 'urgent'},
                        {'treatment': 'imaging studies', 'frequency': 0.9, 'timing': 'urgent'}
                    ]
                }
            },
            'cardiology': {
                'acute_coronary_syndrome': {
                    'frequency': 0.08,
                    'demographics': {
                        'age_range': (45, 85),
                        'gender_distribution': {'male': 0.65, 'female': 0.35},
                        'risk_factors': ['hypertension', 'diabetes', 'smoking', 'hyperlipidemia', 'family_history']
                    },
                    'symptom_clusters': [
                        {
                            'symptoms': ['chest pain', 'shortness of breath', 'sweating', 'nausea'],
                            'frequency': 0.6,
                            'severity': 'high'
                        },
                        {
                            'symptoms': ['chest pain', 'arm pain', 'jaw pain'],
                            'frequency': 0.3,
                            'severity': 'high'
                        }
                    ],
                    'diagnoses': [
                        {'diagnosis': 'STEMI', 'frequency': 0.4, 'difficulty': 'hard'},
                        {'diagnosis': 'NSTEMI', 'frequency': 0.4, 'difficulty': 'medium'},
                        {'diagnosis': 'unstable angina', 'frequency': 0.2, 'difficulty': 'medium'}
                    ],
                    'treatments': [
                        {'treatment': 'aspirin', 'frequency': 0.95, 'timing': 'immediate'},
                        {'treatment': 'nitroglycerin', 'frequency': 0.8, 'timing': 'immediate'},
                        {'treatment': 'cardiac catheterization', 'frequency': 0.7, 'timing': 'urgent'},
                        {'treatment': 'thrombolytics', 'frequency': 0.3, 'timing': 'urgent'},
                        {'treatment': 'beta blockers', 'frequency': 0.6, 'timing': 'urgent'}
                    ]
                },
                'heart_failure': {
                    'frequency': 0.06,
                    'demographics': {
                        'age_range': (60, 90),
                        'gender_distribution': {'male': 0.55, 'female': 0.45},
                        'risk_factors': ['hypertension', 'diabetes', 'previous_mi', 'valvular_disease']
                    },
                    'symptom_clusters': [
                        {
                            'symptoms': ['shortness of breath', 'fatigue', 'edema'],
                            'frequency': 0.7,
                            'severity': 'medium'
                        },
                        {
                            'symptoms': ['shortness of breath', 'orthopnea', 'paroxysmal_nocturnal_dyspnea'],
                            'frequency': 0.3,
                            'severity': 'high'
                        }
                    ],
                    'diagnoses': [
                        {'diagnosis': 'acute decompensated heart failure', 'frequency': 0.6, 'difficulty': 'medium'},
                        {'diagnosis': 'chronic heart failure', 'frequency': 0.4, 'difficulty': 'medium'}
                    ],
                    'treatments': [
                        {'treatment': 'diuretics', 'frequency': 0.9, 'timing': 'immediate'},
                        {'treatment': 'ace inhibitors', 'frequency': 0.7, 'timing': 'urgent'},
                        {'treatment': 'beta blockers', 'frequency': 0.6, 'timing': 'urgent'},
                        {'treatment': 'oxygen therapy', 'frequency': 0.8, 'timing': 'immediate'}
                    ]
                }
            },
            'neurology': {
                'acute_stroke': {
                    'frequency': 0.05,
                    'demographics': {
                        'age_range': (50, 85),
                        'gender_distribution': {'male': 0.52, 'female': 0.48},
                        'risk_factors': ['hypertension', 'diabetes', 'atrial_fibrillation', 'smoking']
                    },
                    'symptom_clusters': [
                        {
                            'symptoms': ['facial droop', 'arm weakness', 'speech difficulty'],
                            'frequency': 0.5,
                            'severity': 'high'
                        },
                        {
                            'symptoms': ['sudden headache', 'confusion', 'vision changes'],
                            'frequency': 0.3,
                            'severity': 'high'
                        }
                    ],
                    'diagnoses': [
                        {'diagnosis': 'ischemic stroke', 'frequency': 0.7, 'difficulty': 'hard'},
                        {'diagnosis': 'hemorrhagic stroke', 'frequency': 0.2, 'difficulty': 'hard'},
                        {'diagnosis': 'tia', 'frequency': 0.1, 'difficulty': 'medium'}
                    ],
                    'treatments': [
                        {'treatment': 'tpa', 'frequency': 0.3, 'timing': 'urgent'},
                        {'treatment': 'mechanical thrombectomy', 'frequency': 0.2, 'timing': 'urgent'},
                        {'treatment': 'antiplatelet therapy', 'frequency': 0.8, 'timing': 'urgent'},
                        {'treatment': 'blood pressure management', 'frequency': 0.9, 'timing': 'immediate'}
                    ]
                },
                'seizure': {
                    'frequency': 0.04,
                    'demographics': {
                        'age_range': (20, 80),
                        'gender_distribution': {'male': 0.48, 'female': 0.52},
                        'risk_factors': ['epilepsy', 'head_trauma', 'brain_tumor', 'metabolic_disorder']
                    },
                    'symptom_clusters': [
                        {
                            'symptoms': ['unconsciousness', 'convulsions', 'incontinence'],
                            'frequency': 0.6,
                            'severity': 'high'
                        },
                        {
                            'symptoms': ['confusion', 'memory loss', 'headache'],
                            'frequency': 0.4,
                            'severity': 'medium'
                        }
                    ],
                    'diagnoses': [
                        {'diagnosis': 'generalized tonic-clonic seizure', 'frequency': 0.5, 'difficulty': 'medium'},
                        {'diagnosis': 'complex partial seizure', 'frequency': 0.3, 'difficulty': 'medium'},
                        {'diagnosis': 'status epilepticus', 'frequency': 0.2, 'difficulty': 'hard'}
                    ],
                    'treatments': [
                        {'treatment': 'benzodiazepines', 'frequency': 0.8, 'timing': 'immediate'},
                        {'treatment': 'antiepileptic drugs', 'frequency': 0.6, 'timing': 'urgent'},
                        {'treatment': 'airway management', 'frequency': 0.9, 'timing': 'immediate'},
                        {'treatment': 'imaging studies', 'frequency': 0.7, 'timing': 'urgent'}
                    ]
                }
            },
            'respiratory': {
                'copd_exacerbation': {
                    'frequency': 0.07,
                    'demographics': {
                        'age_range': (55, 85),
                        'gender_distribution': {'male': 0.6, 'female': 0.4},
                        'risk_factors': ['smoking', 'environmental_exposure', 'previous_copd']
                    },
                    'symptom_clusters': [
                        {
                            'symptoms': ['shortness of breath', 'cough', 'increased sputum'],
                            'frequency': 0.7,
                            'severity': 'medium'
                        },
                        {
                            'symptoms': ['shortness of breath', 'wheezing', 'chest tightness'],
                            'frequency': 0.3,
                            'severity': 'medium'
                        }
                    ],
                    'diagnoses': [
                        {'diagnosis': 'copd exacerbation', 'frequency': 0.8, 'difficulty': 'medium'},
                        {'diagnosis': 'pneumonia', 'frequency': 0.2, 'difficulty': 'medium'}
                    ],
                    'treatments': [
                        {'treatment': 'bronchodilators', 'frequency': 0.9, 'timing': 'immediate'},
                        {'treatment': 'steroids', 'frequency': 0.8, 'timing': 'urgent'},
                        {'treatment': 'oxygen therapy', 'frequency': 0.7, 'timing': 'immediate'},
                        {'treatment': 'antibiotics', 'frequency': 0.5, 'timing': 'urgent'}
                    ]
                },
                'pneumonia': {
                    'frequency': 0.06,
                    'demographics': {
                        'age_range': (40, 85),
                        'gender_distribution': {'male': 0.48, 'female': 0.52},
                        'risk_factors': ['smoking', 'immunocompromised', 'chronic_lung_disease']
                    },
                    'symptom_clusters': [
                        {
                            'symptoms': ['fever', 'cough', 'shortness of breath', 'chest pain'],
                            'frequency': 0.6,
                            'severity': 'medium'
                        },
                        {
                            'symptoms': ['fever', 'chills', 'fatigue', 'cough'],
                            'frequency': 0.4,
                            'severity': 'medium'
                        }
                    ],
                    'diagnoses': [
                        {'diagnosis': 'community acquired pneumonia', 'frequency': 0.7, 'difficulty': 'medium'},
                        {'diagnosis': 'hospital acquired pneumonia', 'frequency': 0.2, 'difficulty': 'hard'},
                        {'diagnosis': 'aspiration pneumonia', 'frequency': 0.1, 'difficulty': 'medium'}
                    ],
                    'treatments': [
                        {'treatment': 'antibiotics', 'frequency': 0.9, 'timing': 'urgent'},
                        {'treatment': 'oxygen therapy', 'frequency': 0.6, 'timing': 'immediate'},
                        {'treatment': 'chest physiotherapy', 'frequency': 0.4, 'timing': 'routine'},
                        {'treatment': 'hydration', 'frequency': 0.8, 'timing': 'immediate'}
                    ]
                }
            },
            "rheumatology": {
                "diagnoses": [
                    {"diagnosis": "systemic lupus erythematosus", "prevalence": 0.02},
                    {"diagnosis": "rheumatoid arthritis", "prevalence": 0.03},
                    {"diagnosis": "vasculitis", "prevalence": 0.01}
                ],
                "symptoms": ["joint pain", "rash", "fatigue", "fever"],
                "labs": ["ANA", "RF", "ESR", "CRP"],
                "imaging": ["joint xray", "chest xray"]
            },
            "hematology": {
                "diagnoses": [
                    {"diagnosis": "sickle cell crisis", "prevalence": 0.01},
                    {"diagnosis": "thrombotic thrombocytopenic purpura", "prevalence": 0.005}
                ],
                "symptoms": ["pain", "anemia", "jaundice", "petechiae"],
                "labs": ["CBC", "LDH", "haptoglobin", "peripheral smear"],
                "imaging": ["abdominal ultrasound"]
            },
            "infectious_disease": {
                "diagnoses": [
                    {"diagnosis": "tuberculosis", "prevalence": 0.01},
                    {"diagnosis": "HIV/AIDS", "prevalence": 0.01},
                    {"diagnosis": "malaria", "prevalence": 0.005}
                ],
                "symptoms": ["fever", "night sweats", "weight loss", "cough"],
                "labs": ["HIV test", "TB quantiferon", "malaria smear"],
                "imaging": ["chest xray", "CT scan"]
            }
        }
        return self.pattern_library
    
    def get_patterns_by_specialty(self, specialty: str) -> Dict[str, Any]:
        """get patterns for specific specialty"""
        return self.pattern_library.get(specialty, {})
    
    def get_patterns_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """get patterns by difficulty level"""
        patterns = []
        for specialty, specialty_patterns in self.pattern_library.items():
            for pattern_name, pattern_data in specialty_patterns.items():
                for diagnosis in pattern_data.get('diagnoses', []):
                    if diagnosis.get('difficulty') == difficulty:
                        patterns.append({
                            'specialty': specialty,
                            'pattern_name': pattern_name,
                            'pattern_data': pattern_data,
                            'diagnosis': diagnosis
                        })
        return patterns
    
    def get_random_pattern(self, specialty: Optional[str] = None, difficulty: Optional[str] = None) -> Dict[str, Any]:
        """get a random pattern matching criteria"""
        available_patterns = []
        
        for spec, specialty_patterns in self.pattern_library.items():
            if specialty and spec != specialty:
                continue
                
            for pattern_name, pattern_data in specialty_patterns.items():
                if difficulty:
                    # check if any diagnosis matches difficulty
                    diagnoses = pattern_data.get('diagnoses', [])
                    if not any(d.get('difficulty') == difficulty for d in diagnoses):
                        continue
                
                available_patterns.append({
                    'specialty': spec,
                    'pattern_name': pattern_name,
                    'pattern_data': pattern_data
                })
        
        if available_patterns:
            return random.choice(available_patterns)
        else:
            return {}
    
    def generate_scenario_from_pattern(self, pattern: Dict[str, Any], 
                                     user_performance: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """generate a scenario from a clinical pattern"""
        if not pattern:
            return {}
        
        pattern_data = pattern['pattern_data']
        specialty = pattern['specialty']
        pattern_name = pattern['pattern_name']
        
        # adjust difficulty based on user performance
        difficulty_modifier = self._calculate_difficulty_modifier(user_performance)
        
        # generate demographics
        demographics = self._generate_demographics(pattern_data['demographics'])
        
        # select symptom cluster
        symptom_cluster = self._select_symptom_cluster(pattern_data['symptom_clusters'])
        
        # select diagnosis
        diagnosis = self._select_diagnosis(pattern_data['diagnoses'], difficulty_modifier)
        
        # select treatments
        treatments = self._select_treatments(pattern_data['treatments'])
        
        # generate temporal data
        temporal_data = self._generate_temporal_data(pattern_data)
        
        # generate outcome
        outcome = self._generate_outcome(diagnosis, treatments)
        
        scenario = {
            'pattern_id': f"{specialty}_{pattern_name}",
            'specialty': specialty,
            'difficulty': diagnosis.get('difficulty', 'medium'),
            'demographics': demographics,
            'presentation': {
                'chief_complaint': self._generate_chief_complaint(symptom_cluster),
                'symptoms': symptom_cluster['symptoms'],
                'vital_signs': self._generate_vital_signs(diagnosis['diagnosis']),
                'arrival_time': datetime.now()
            },
            'diagnosis': {
                'primary': diagnosis['diagnosis'],
                'secondary': self._generate_secondary_diagnoses(diagnosis['diagnosis']),
                'icd_codes': self._get_icd_codes(diagnosis['diagnosis'])
            },
            'treatment': {
                'medications': [t['treatment'] for t in treatments if 'medication' in t['treatment'].lower()],
                'procedures': [t['treatment'] for t in treatments if 'procedure' in t['treatment'].lower()],
                'sequence': [t['treatment'] for t in treatments]
            },
            'outcome': outcome,
            'temporal_data': temporal_data,
            'learning_objectives': self._generate_learning_objectives(diagnosis['diagnosis']),
            'key_actions': self._generate_key_actions(diagnosis['diagnosis'], treatments)
        }
        
        return scenario
    
    def _calculate_difficulty_modifier(self, user_performance: Optional[Dict[str, float]]) -> float:
        """calculate difficulty modifier based on user performance"""
        if not user_performance:
            return 1.0
        
        # calculate average performance across metrics
        avg_performance = sum(user_performance.values()) / len(user_performance)
        
        # adjust difficulty: better performance = harder scenarios
        if avg_performance > 0.8:
            return 1.2  # increase difficulty
        elif avg_performance < 0.4:
            return 0.8  # decrease difficulty
        else:
            return 1.0
    
    def _generate_demographics(self, demographics_template: Dict[str, Any]) -> Dict[str, Any]:
        """generate patient demographics from template"""
        age_range = demographics_template.get('age_range', (30, 70))
        age = random.randint(age_range[0], age_range[1])
        
        gender_dist = demographics_template.get('gender_distribution', {'male': 0.5, 'female': 0.5})
        gender = random.choices(list(gender_dist.keys()), weights=list(gender_dist.values()))[0]
        
        risk_factors = demographics_template.get('risk_factors', [])
        selected_risk_factors = random.sample(risk_factors, min(len(risk_factors), random.randint(1, 3)))
        
        return {
            'age': age,
            'gender': gender,
            'risk_factors': selected_risk_factors,
            'race': random.choice(['white', 'black', 'hispanic', 'asian', 'other']),
            'ethnicity': random.choice(['hispanic', 'non-hispanic']),
            'insurance': random.choice(['private', 'medicare', 'medicaid', 'uninsured'])
        }
    
    def _select_symptom_cluster(self, symptom_clusters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """select a symptom cluster based on frequency"""
        weights = [cluster['frequency'] for cluster in symptom_clusters]
        return random.choices(symptom_clusters, weights=weights)[0]
    
    def _select_diagnosis(self, diagnoses: List[Dict[str, Any]], difficulty_modifier: float) -> Dict[str, Any]:
        """select diagnosis based on frequency and difficulty"""
        # adjust frequencies based on difficulty modifier
        adjusted_diagnoses = []
        for diagnosis in diagnoses:
            adjusted_freq = diagnosis['frequency'] * difficulty_modifier
            adjusted_diagnoses.append({**diagnosis, 'frequency': adjusted_freq})
        
        weights = [d['frequency'] for d in adjusted_diagnoses]
        return random.choices(adjusted_diagnoses, weights=weights)[0]
    
    def _select_treatments(self, treatments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """select treatments based on frequency"""
        selected_treatments = []
        for treatment in treatments:
            if random.random() < treatment['frequency']:
                selected_treatments.append(treatment)
        
        # ensure at least one treatment is selected
        if not selected_treatments:
            selected_treatments = [random.choice(treatments)]
        
        return selected_treatments
    
    def _generate_temporal_data(self, pattern_data: Dict[str, Any]) -> Dict[str, float]:
        """generate temporal data for scenario"""
        base_times = {
            'arrival_to_diagnosis': 30,  # minutes
            'diagnosis_to_treatment': 15,  # minutes
            'treatment_to_discharge': 120   # minutes
        }
        
        # add some randomness
        temporal_data = {}
        for key, base_time in base_times.items():
            variation = random.uniform(0.7, 1.3)
            temporal_data[key] = base_time * variation
        
        return temporal_data
    
    def _generate_outcome(self, diagnosis: Dict[str, Any], treatments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """generate patient outcome based on diagnosis and treatments"""
        diagnosis_name = diagnosis['diagnosis']
        difficulty = diagnosis.get('difficulty', 'medium')
        
        # base outcomes by diagnosis
        outcome_templates = {
            'STEMI': {'disposition': 'admitted', 'length_of_stay': 3, 'mortality': 0.05},
            'NSTEMI': {'disposition': 'admitted', 'length_of_stay': 2, 'mortality': 0.03},
            'copd exacerbation': {'disposition': 'admitted', 'length_of_stay': 2, 'mortality': 0.02},
            'pneumonia': {'disposition': 'admitted', 'length_of_stay': 3, 'mortality': 0.04},
            'appendicitis': {'disposition': 'admitted', 'length_of_stay': 1, 'mortality': 0.01}
        }
        
        base_outcome = outcome_templates.get(diagnosis_name, {
            'disposition': 'discharged',
            'length_of_stay': 1,
            'mortality': 0.01
        })
        
        # adjust based on difficulty
        if difficulty == 'hard':
            base_outcome['mortality'] *= 1.5
            base_outcome['length_of_stay'] *= 1.2
        
        # add randomness
        outcome = {
            'disposition': base_outcome['disposition'],
            'length_of_stay': base_outcome['length_of_stay'] * random.uniform(0.8, 1.2),
            'mortality': random.random() < base_outcome['mortality'],
            'readmission': random.random() < 0.1
        }
        
        return outcome
    
    def _generate_chief_complaint(self, symptom_cluster: Dict[str, Any]) -> str:
        """generate chief complaint from symptom cluster"""
        symptoms = symptom_cluster['symptoms']
        primary_symptoms = ['chest pain', 'shortness of breath', 'abdominal pain', 'headache']
        
        for symptom in symptoms:
            if symptom in primary_symptoms:
                return f"patient complains of {symptom}"
        
        return f"patient complains of {symptoms[0]}"
    
    def _generate_vital_signs(self, diagnosis: str) -> Dict[str, float]:
        """generate vital signs based on diagnosis"""
        vital_templates = {
            'STEMI': {
                'heart_rate': (90, 120),
                'bp_systolic': (140, 180),
                'bp_diastolic': (90, 110),
                'respiratory_rate': (18, 24),
                'oxygen_saturation': (92, 98),
                'temperature': (98.0, 99.5)
            },
            'copd exacerbation': {
                'heart_rate': (100, 130),
                'bp_systolic': (130, 160),
                'bp_diastolic': (80, 100),
                'respiratory_rate': (24, 32),
                'oxygen_saturation': (85, 92),
                'temperature': (98.5, 100.5)
            }
        }
        
        template = vital_templates.get(diagnosis, {
            'heart_rate': (70, 100),
            'bp_systolic': (110, 140),
            'bp_diastolic': (70, 90),
            'respiratory_rate': (16, 20),
            'oxygen_saturation': (95, 99),
            'temperature': (97.5, 99.0)
        })
        
        vitals = {}
        for vital, (min_val, max_val) in template.items():
            vitals[vital] = random.uniform(min_val, max_val)
        
        return vitals
    
    def _generate_secondary_diagnoses(self, primary_diagnosis: str) -> List[str]:
        """generate secondary diagnoses"""
        secondary_map = {
            'STEMI': ['hypertension', 'diabetes', 'hyperlipidemia'],
            'copd exacerbation': ['hypertension', 'pneumonia'],
            'pneumonia': ['copd', 'diabetes'],
            'appendicitis': ['hypertension']
        }
        
        return secondary_map.get(primary_diagnosis, [])
    
    def _get_icd_codes(self, diagnosis: str) -> List[str]:
        """get icd codes for diagnosis"""
        icd_map = {
            'STEMI': ['I21.9'],
            'NSTEMI': ['I21.4'],
            'copd exacerbation': ['J44.1'],
            'pneumonia': ['J18.9'],
            'appendicitis': ['K35.90']
        }
        
        return icd_map.get(diagnosis, ['Z51.9'])
    
    def _generate_learning_objectives(self, diagnosis: str) -> List[str]:
        """generate learning objectives for diagnosis"""
        objectives_map = {
            'STEMI': [
                'recognize symptoms of acute coronary syndrome',
                'order appropriate cardiac workup',
                'initiate timely treatment for stemi',
                'manage complications of myocardial infarction'
            ],
            'copd exacerbation': [
                'recognize copd exacerbation',
                'assess respiratory status',
                'initiate appropriate bronchodilator therapy',
                'manage hypoxemia and respiratory distress'
            ]
        }
        
        return objectives_map.get(diagnosis, [
            'assess patient presentation',
            'formulate differential diagnosis',
            'initiate appropriate treatment',
            'monitor patient response'
        ])
    
    def _generate_key_actions(self, diagnosis: str, treatments: List[Dict[str, Any]]) -> List[str]:
        """generate key actions for scenario"""
        actions = []
        
        for treatment in treatments:
            treatment_name = treatment['treatment']
            timing = treatment.get('timing', 'routine')
            
            if timing == 'immediate':
                actions.append(f"administer {treatment_name} immediately")
            elif timing == 'urgent':
                actions.append(f"order {treatment_name} urgently")
            else:
                actions.append(f"consider {treatment_name}")
        
        return actions 