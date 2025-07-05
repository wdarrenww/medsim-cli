"""
scenario manager for medical simulations
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import random

from ..core.simulation import PatientState
from ..core.physiology import PhysiologicalEngine
from ..core.dialogue import AdvancedDialogueSystem


@dataclass
class Scenario:
    """represents a medical scenario"""
    id: str
    title: str
    description: str
    difficulty: str  # easy, medium, hard
    specialty: str
    learning_objectives: List[str]
    initial_patient_state: Dict[str, Any]
    correct_diagnosis: str
    optimal_actions: List[str]
    time_limit: int  # minutes
    points_possible: int


class ScenarioManager:
    """manages medical scenarios"""
    
    def __init__(self):
        self.scenarios = self._initialize_scenarios()
        self.current_scenario: Optional[Scenario] = None
        self.scenario_start_time: Optional[datetime] = None
        
    def _initialize_scenarios(self) -> Dict[str, Scenario]:
        """initialize high-quality emergency medicine scenarios"""
        scenarios = {
            "chest_pain_01": Scenario(
                id="chest_pain_01",
                title="Acute Coronary Syndrome",
                description="A 58-year-old male presents with crushing chest pain that started 1 hour ago. He has a history of hypertension and diabetes.",
                difficulty="medium",
                specialty="Emergency Medicine",
                learning_objectives=[
                    "Recognize symptoms of acute coronary syndrome",
                    "Order appropriate cardiac workup",
                    "Initiate timely treatment for STEMI",
                    "Manage complications of myocardial infarction"
                ],
                initial_patient_state={
                    "patient_id": "P001",
                    "name": "John Smith",
                    "age": 58,
                    "gender": "Male",
                    "vital_signs": {
                        "heart_rate": 95,
                        "bp_systolic": 160,
                        "bp_diastolic": 100,
                        "respiratory_rate": 20,
                        "oxygen_saturation": 96,
                        "temperature": 98.6
                    },
                    "symptoms": ["chest pain", "shortness of breath", "sweating"],
                    "medical_history": ["hypertension", "diabetes", "hyperlipidemia"],
                    "medications": ["metformin", "lisinopril", "atorvastatin"],
                    "allergies": ["penicillin"],
                    "social_history": {"smoking": "former", "alcohol": "moderate"},
                    "family_history": ["father had heart attack at age 55"]
                },
                correct_diagnosis="ST-Elevation Myocardial Infarction (STEMI)",
                optimal_actions=[
                    "obtain ecg immediately",
                    "order cardiac enzymes (troponin)",
                    "administer aspirin",
                    "administer nitroglycerin",
                    "order chest x-ray",
                    "consult cardiology",
                    "prepare for cardiac catheterization"
                ],
                time_limit=30,
                points_possible=100
            ),
            
            "shortness_breath_01": Scenario(
                id="shortness_breath_01",
                title="Acute Exacerbation of COPD",
                description="A 65-year-old female with COPD presents with worsening shortness of breath over the past 2 days. She has increased sputum production and is using her rescue inhaler more frequently.",
                difficulty="medium",
                specialty="Emergency Medicine",
                learning_objectives=[
                    "Recognize COPD exacerbation",
                    "Assess respiratory status",
                    "Initiate appropriate bronchodilator therapy",
                    "Manage hypoxemia and respiratory distress"
                ],
                initial_patient_state={
                    "patient_id": "P002",
                    "name": "Mary Johnson",
                    "age": 65,
                    "gender": "Female",
                    "vital_signs": {
                        "heart_rate": 110,
                        "bp_systolic": 140,
                        "bp_diastolic": 85,
                        "respiratory_rate": 28,
                        "oxygen_saturation": 88,
                        "temperature": 99.2
                    },
                    "symptoms": ["shortness of breath", "cough", "increased sputum"],
                    "medical_history": ["COPD", "hypertension"],
                    "medications": ["albuterol inhaler", "tiotropium", "lisinopril"],
                    "allergies": ["sulfa drugs"],
                    "social_history": {"smoking": "current", "alcohol": "none"},
                    "family_history": ["mother had emphysema"]
                },
                correct_diagnosis="Acute Exacerbation of COPD",
                optimal_actions=[
                    "assess oxygen saturation",
                    "administer albuterol nebulizer",
                    "order chest x-ray",
                    "administer oxygen therapy",
                    "consider steroids",
                    "assess for pneumonia"
                ],
                time_limit=25,
                points_possible=100
            ),
            
            "abdominal_pain_01": Scenario(
                id="abdominal_pain_01",
                title="Acute Appendicitis",
                description="A 22-year-old male presents with right lower quadrant abdominal pain that started 12 hours ago. The pain has been progressively worsening and is now severe.",
                difficulty="easy",
                specialty="Emergency Medicine",
                learning_objectives=[
                    "Recognize signs and symptoms of appendicitis",
                    "Perform appropriate abdominal examination",
                    "Order diagnostic imaging",
                    "Initiate surgical consultation"
                ],
                initial_patient_state={
                    "patient_id": "P003",
                    "name": "David Wilson",
                    "age": 22,
                    "gender": "Male",
                    "vital_signs": {
                        "heart_rate": 100,
                        "bp_systolic": 130,
                        "bp_diastolic": 80,
                        "respiratory_rate": 18,
                        "oxygen_saturation": 98,
                        "temperature": 100.8
                    },
                    "symptoms": ["right lower quadrant pain", "nausea", "decreased appetite"],
                    "medical_history": ["none"],
                    "medications": ["none"],
                    "allergies": ["none"],
                    "social_history": {"smoking": "none", "alcohol": "social"},
                    "family_history": ["none relevant"]
                },
                correct_diagnosis="Acute Appendicitis",
                optimal_actions=[
                    "perform abdominal examination",
                    "order cbc",
                    "order abdominal ct",
                    "consult surgery",
                    "administer pain medication",
                    "start iv fluids"
                ],
                time_limit=20,
                points_possible=100
            ),
            
            "headache_01": Scenario(
                id="headache_01",
                title="Subarachnoid Hemorrhage",
                description="A 45-year-old female presents with the worst headache of her life that started suddenly 2 hours ago. She describes it as a thunderclap headache.",
                difficulty="hard",
                specialty="Emergency Medicine",
                learning_objectives=[
                    "Recognize thunderclap headache",
                    "Identify red flags for subarachnoid hemorrhage",
                    "Order appropriate imaging",
                    "Initiate neurosurgical consultation"
                ],
                initial_patient_state={
                    "patient_id": "P004",
                    "name": "Sarah Davis",
                    "age": 45,
                    "gender": "Female",
                    "vital_signs": {
                        "heart_rate": 85,
                        "bp_systolic": 180,
                        "bp_diastolic": 110,
                        "respiratory_rate": 16,
                        "oxygen_saturation": 98,
                        "temperature": 98.6
                    },
                    "symptoms": ["severe headache", "nausea", "photophobia"],
                    "medical_history": ["hypertension"],
                    "medications": ["amlodipine"],
                    "allergies": ["none"],
                    "social_history": {"smoking": "none", "alcohol": "moderate"},
                    "family_history": ["father had stroke"]
                },
                correct_diagnosis="Subarachnoid Hemorrhage",
                optimal_actions=[
                    "obtain detailed headache history",
                    "perform neurological examination",
                    "order head ct",
                    "order lumbar puncture if ct negative",
                    "consult neurosurgery",
                    "control blood pressure"
                ],
                time_limit=30,
                points_possible=100
            ),
            
            "syncope_01": Scenario(
                id="syncope_01",
                title="Pulmonary Embolism",
                description="A 35-year-old female presents with syncope and chest pain. She recently had surgery and has been immobile. She also complains of shortness of breath.",
                difficulty="hard",
                specialty="Emergency Medicine",
                learning_objectives=[
                    "Recognize risk factors for pulmonary embolism",
                    "Assess for deep vein thrombosis",
                    "Order appropriate diagnostic studies",
                    "Initiate anticoagulation therapy"
                ],
                initial_patient_state={
                    "patient_id": "P005",
                    "name": "Jennifer Brown",
                    "age": 35,
                    "gender": "Female",
                    "vital_signs": {
                        "heart_rate": 120,
                        "bp_systolic": 110,
                        "bp_diastolic": 70,
                        "respiratory_rate": 24,
                        "oxygen_saturation": 92,
                        "temperature": 98.8
                    },
                    "symptoms": ["syncope", "chest pain", "shortness of breath", "leg swelling"],
                    "medical_history": ["recent surgery", "obesity"],
                    "medications": ["none"],
                    "allergies": ["none"],
                    "social_history": {"smoking": "none", "alcohol": "social"},
                    "family_history": ["mother had blood clots"]
                },
                correct_diagnosis="Pulmonary Embolism",
                optimal_actions=[
                    "assess for dvt",
                    "order d-dimer",
                    "order chest ct angiography",
                    "order ecg",
                    "start heparin",
                    "assess oxygen requirements"
                ],
                time_limit=25,
                points_possible=100
            ),
            
            "fever_01": Scenario(
                id="fever_01",
                title="Sepsis",
                description="A 70-year-old male presents with fever, confusion, and decreased urine output. He has a history of diabetes and recent urinary tract infection.",
                difficulty="medium",
                specialty="Emergency Medicine",
                learning_objectives=[
                    "Recognize signs of sepsis",
                    "Initiate sepsis protocol",
                    "Order appropriate cultures",
                    "Administer broad-spectrum antibiotics"
                ],
                initial_patient_state={
                    "patient_id": "P006",
                    "name": "Robert Miller",
                    "age": 70,
                    "gender": "Male",
                    "vital_signs": {
                        "heart_rate": 110,
                        "bp_systolic": 90,
                        "bp_diastolic": 60,
                        "respiratory_rate": 22,
                        "oxygen_saturation": 94,
                        "temperature": 101.5
                    },
                    "symptoms": ["fever", "confusion", "decreased urine output"],
                    "medical_history": ["diabetes", "hypertension", "recent uti"],
                    "medications": ["metformin", "lisinopril"],
                    "allergies": ["penicillin"],
                    "social_history": {"smoking": "former", "alcohol": "none"},
                    "family_history": ["none relevant"]
                },
                correct_diagnosis="Sepsis",
                optimal_actions=[
                    "obtain blood cultures",
                    "start broad-spectrum antibiotics",
                    "administer iv fluids",
                    "order cbc and chemistry",
                    "assess for source of infection",
                    "monitor vital signs closely"
                ],
                time_limit=20,
                points_possible=100
            ),
            
            "trauma_01": Scenario(
                id="trauma_01",
                title="Motor Vehicle Accident",
                description="A 28-year-old male is brought in by ambulance after a motor vehicle accident. He has multiple injuries and is complaining of chest and abdominal pain.",
                difficulty="hard",
                specialty="Emergency Medicine",
                learning_objectives=[
                    "Perform primary and secondary trauma assessment",
                    "Recognize life-threatening injuries",
                    "Order appropriate imaging",
                    "Coordinate with trauma team"
                ],
                initial_patient_state={
                    "patient_id": "P007",
                    "name": "Michael Taylor",
                    "age": 28,
                    "gender": "Male",
                    "vital_signs": {
                        "heart_rate": 115,
                        "bp_systolic": 100,
                        "bp_diastolic": 65,
                        "respiratory_rate": 26,
                        "oxygen_saturation": 95,
                        "temperature": 98.6
                    },
                    "symptoms": ["chest pain", "abdominal pain", "headache"],
                    "medical_history": ["none"],
                    "medications": ["none"],
                    "allergies": ["none"],
                    "social_history": {"smoking": "none", "alcohol": "unknown"},
                    "family_history": ["none relevant"]
                },
                correct_diagnosis="Multiple Trauma with Potential Internal Injuries",
                optimal_actions=[
                    "perform primary survey",
                    "stabilize airway and breathing",
                    "order trauma panel",
                    "order chest and abdominal ct",
                    "consult trauma surgery",
                    "assess for spinal injuries"
                ],
                time_limit=35,
                points_possible=100
            ),
            
            "pediatric_01": Scenario(
                id="pediatric_01",
                title="Pediatric Asthma Exacerbation",
                description="A 6-year-old child presents with wheezing and difficulty breathing. The child has a history of asthma and has been using albuterol more frequently.",
                difficulty="medium",
                specialty="Emergency Medicine",
                learning_objectives=[
                    "Recognize pediatric asthma exacerbation",
                    "Assess respiratory status in children",
                    "Initiate appropriate bronchodilator therapy",
                    "Monitor for respiratory failure"
                ],
                initial_patient_state={
                    "patient_id": "P008",
                    "name": "Emma Rodriguez",
                    "age": 6,
                    "gender": "Female",
                    "vital_signs": {
                        "heart_rate": 130,
                        "bp_systolic": 110,
                        "bp_diastolic": 70,
                        "respiratory_rate": 35,
                        "oxygen_saturation": 92,
                        "temperature": 98.8
                    },
                    "symptoms": ["wheezing", "difficulty breathing", "cough"],
                    "medical_history": ["asthma", "eczema"],
                    "medications": ["albuterol inhaler"],
                    "allergies": ["none"],
                    "social_history": {"smoking": "none", "alcohol": "none"},
                    "family_history": ["father has asthma"]
                },
                correct_diagnosis="Pediatric Asthma Exacerbation",
                optimal_actions=[
                    "assess respiratory status",
                    "administer albuterol nebulizer",
                    "administer oxygen",
                    "consider steroids",
                    "monitor for improvement",
                    "assess for pneumonia"
                ],
                time_limit=20,
                points_possible=100
            ),
            
            "geriatric_01": Scenario(
                id="geriatric_01",
                title="Geriatric Fall with Hip Fracture",
                description="An 82-year-old female presents after a fall at home. She has pain in her right hip and is unable to bear weight. She has a history of osteoporosis.",
                difficulty="easy",
                specialty="Emergency Medicine",
                learning_objectives=[
                    "Assess geriatric patients after falls",
                    "Recognize hip fracture",
                    "Order appropriate imaging",
                    "Coordinate with orthopedics"
                ],
                initial_patient_state={
                    "patient_id": "P009",
                    "name": "Helen Thompson",
                    "age": 82,
                    "gender": "Female",
                    "vital_signs": {
                        "heart_rate": 85,
                        "bp_systolic": 140,
                        "bp_diastolic": 80,
                        "respiratory_rate": 18,
                        "oxygen_saturation": 98,
                        "temperature": 98.6
                    },
                    "symptoms": ["right hip pain", "inability to bear weight"],
                    "medical_history": ["osteoporosis", "hypertension"],
                    "medications": ["calcium", "vitamin d", "lisinopril"],
                    "allergies": ["none"],
                    "social_history": {"smoking": "none", "alcohol": "none"},
                    "family_history": ["none relevant"]
                },
                correct_diagnosis="Right Hip Fracture",
                optimal_actions=[
                    "assess for other injuries",
                    "order hip x-ray",
                    "administer pain medication",
                    "consult orthopedics",
                    "assess for complications",
                    "plan for surgery"
                ],
                time_limit=25,
                points_possible=100
            )
        }
        return scenarios
    
    def get_available_scenarios(self) -> List[Dict[str, Any]]:
        """get list of available scenarios"""
        return [
            {
                'id': scenario.id,
                'title': scenario.title,
                'description': scenario.description,
                'difficulty': scenario.difficulty,
                'specialty': scenario.specialty,
                'time_limit': scenario.time_limit,
                'points_possible': scenario.points_possible
            }
            for scenario in self.scenarios.values()
        ]
    
    def get_scenario(self, scenario_id: str) -> Optional[Scenario]:
        """get a specific scenario"""
        return self.scenarios.get(scenario_id)
    
    def start_scenario(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        """start a specific scenario"""
        scenario = self.get_scenario(scenario_id)
        if not scenario:
            return None
        
        self.current_scenario = scenario
        self.scenario_start_time = datetime.now()
        
        return {
            'scenario_id': scenario.id,
            'title': scenario.title,
            'description': scenario.description,
            'learning_objectives': scenario.learning_objectives,
            'patient_state': scenario.initial_patient_state,
            'time_limit': scenario.time_limit,
            'points_possible': scenario.points_possible
        }
    
    def get_scenario_progress(self) -> Optional[Dict[str, Any]]:
        """get current scenario progress"""
        if not self.current_scenario or not self.scenario_start_time:
            return None
        
        elapsed_time = (datetime.now() - self.scenario_start_time).total_seconds() / 60
        
        return {
            'scenario_id': self.current_scenario.id,
            'title': self.current_scenario.title,
            'elapsed_time': elapsed_time,
            'time_limit': self.current_scenario.time_limit,
            'remaining_time': max(0, self.current_scenario.time_limit - elapsed_time)
        }
    
    def end_scenario(self) -> Optional[Dict[str, Any]]:
        """end the current scenario and calculate performance"""
        if not self.current_scenario or not self.scenario_start_time:
            return None
        
        elapsed_time = (datetime.now() - self.scenario_start_time).total_seconds() / 60
        
        return {
            'scenario_id': self.current_scenario.id,
            'title': self.current_scenario.title,
            'elapsed_time': elapsed_time,
            'correct_diagnosis': self.current_scenario.correct_diagnosis,
            'optimal_actions': self.current_scenario.optimal_actions,
            'time_limit': self.current_scenario.time_limit,
            'points_possible': self.current_scenario.points_possible
        }
    
    def get_scenarios_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """get scenarios by difficulty level"""
        return [
            {
                'id': scenario.id,
                'title': scenario.title,
                'description': scenario.description,
                'difficulty': scenario.difficulty,
                'specialty': scenario.specialty,
                'time_limit': scenario.time_limit
            }
            for scenario in self.scenarios.values()
            if scenario.difficulty.lower() == difficulty.lower()
        ]
    
    def get_scenarios_by_specialty(self, specialty: str) -> List[Dict[str, Any]]:
        """get scenarios by specialty"""
        return [
            {
                'id': scenario.id,
                'title': scenario.title,
                'description': scenario.description,
                'difficulty': scenario.difficulty,
                'specialty': scenario.specialty,
                'time_limit': scenario.time_limit
            }
            for scenario in self.scenarios.values()
            if scenario.specialty.lower() == specialty.lower()
        ] 