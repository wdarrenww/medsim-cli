"""
scenario manager for medical simulations with dynamic generation support
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import random

from ..core.simulation import PatientState
from ..core.physiology import EnhancedPhysiologicalEngine
from ..core.dialogue import EnhancedDialogueEngine
from ..generation.scenario_generator import DynamicScenarioGenerator, DynamicScenarioConfig


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
    """manages medical scenarios with dynamic generation support"""
    
    def __init__(self):
        self.scenarios = self._initialize_scenarios()
        self.current_scenario: Optional[Scenario] = None
        self.scenario_start_time: Optional[datetime] = None
        
        # dynamic generation components
        self.dynamic_generator = DynamicScenarioGenerator()
        self.dynamic_config = DynamicScenarioConfig()
        
        # continuous simulation state
        self.continuous_mode = False
        self.scenario_sequence = []
        self.current_sequence_index = 0
        self.user_performance_history = []
        
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
                    "symptoms": ["thunderclap headache", "nausea", "photophobia"],
                    "medical_history": ["hypertension"],
                    "medications": ["lisinopril"],
                    "allergies": ["none"],
                    "social_history": {"smoking": "former", "alcohol": "moderate"},
                    "family_history": ["father had stroke at age 60"]
                },
                correct_diagnosis="Subarachnoid Hemorrhage",
                optimal_actions=[
                    "obtain head ct immediately",
                    "assess neurological status",
                    "control blood pressure",
                    "consult neurosurgery",
                    "prepare for angiography",
                    "monitor for complications"
                ],
                time_limit=35,
                points_possible=100
            )
        }
        
        return scenarios
    
    # Dynamic Generation Methods
    
    def generate_dynamic_scenario(self, specialty: Optional[str] = None, 
                                difficulty: Optional[str] = None,
                                variety: float = 1.0) -> Optional[Dict[str, Any]]:
        """generate a dynamic scenario based on parameters"""
        config = DynamicScenarioConfig(
            specialty=specialty,
            difficulty=difficulty,
            variety=variety,
            adaptive=True,
            user_performance=self._get_average_performance()
        )
        
        scenario_data = self.dynamic_generator.generate_scenario(config)
        
        # convert to scenario format
        scenario = self._convert_dynamic_to_scenario(scenario_data)
        
        return scenario
    
    def start_continuous_mode(self, specialty: Optional[str] = None, 
                            difficulty: Optional[str] = None,
                            scenario_count: int = 10) -> bool:
        """start continuous scenario generation mode"""
        config = DynamicScenarioConfig(
            specialty=specialty,
            difficulty=difficulty,
            adaptive=True,
            user_performance=self._get_average_performance()
        )
        
        self.scenario_sequence = self.dynamic_generator.generate_looped_scenarios(
            n=scenario_count, 
            config=config
        )
        
        self.continuous_mode = True
        self.current_sequence_index = 0
        
        return True
    
    def get_next_continuous_scenario(self) -> Optional[Dict[str, Any]]:
        """get the next scenario in continuous mode"""
        if not self.continuous_mode or self.current_sequence_index >= len(self.scenario_sequence):
            return None
        
        scenario_data = self.scenario_sequence[self.current_sequence_index]
        scenario = self._convert_dynamic_to_scenario(scenario_data)
        
        self.current_sequence_index += 1
        return scenario
    
    def update_user_performance(self, performance_metrics: Dict[str, float]):
        """update user performance for adaptive difficulty"""
        self.user_performance_history.append(performance_metrics)
        
        # keep only last 10 performances
        if len(self.user_performance_history) > 10:
            self.user_performance_history = self.user_performance_history[-10:]
        
        # update dynamic generator
        avg_performance = self._get_average_performance()
        if avg_performance:
            self.dynamic_generator.update_user_performance(avg_performance)
    
    def _get_average_performance(self) -> Optional[Dict[str, float]]:
        """calculate average performance from history"""
        if not self.user_performance_history:
            return None
        
        # calculate average for each metric
        avg_performance = {}
        metrics = self.user_performance_history[0].keys()
        
        for metric in metrics:
            values = [perf.get(metric, 0.0) for perf in self.user_performance_history]
            avg_performance[metric] = sum(values) / len(values)
        
        return avg_performance
    
    def _convert_dynamic_to_scenario(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """convert dynamic scenario data to scenario format"""
        # extract patient state
        patient_state = {
            "patient_id": scenario_data.get('demographics', {}).get('patient_id', 'P001'),
            "name": f"Patient {scenario_data.get('demographics', {}).get('age', 50)}",
            "age": scenario_data.get('demographics', {}).get('age', 50),
            "gender": scenario_data.get('demographics', {}).get('gender', 'unknown'),
            "vital_signs": scenario_data.get('presentation', {}).get('vital_signs', {}),
            "symptoms": scenario_data.get('presentation', {}).get('symptoms', []),
            "medical_history": scenario_data.get('diagnosis', {}).get('secondary', []),
            "medications": scenario_data.get('treatment', {}).get('medications', []),
            "allergies": [],
            "social_history": {},
            "family_history": []
        }
        
        # create scenario structure
        scenario = {
            "id": f"dynamic_{scenario_data.get('pattern_id', 'unknown')}",
            "title": f"Dynamic {scenario_data.get('diagnosis', {}).get('primary', 'Case')}",
            "description": f"Dynamic scenario generated for {scenario_data.get('specialty', 'Emergency Medicine')}",
            "difficulty": scenario_data.get('difficulty', 'medium'),
            "specialty": scenario_data.get('specialty', 'Emergency Medicine'),
            "learning_objectives": scenario_data.get('learning_objectives', []),
            "initial_patient_state": patient_state,
            "correct_diagnosis": scenario_data.get('diagnosis', {}).get('primary', 'Unknown'),
            "optimal_actions": scenario_data.get('key_actions', []),
            "time_limit": 30,
            "points_possible": 100,
            "generated_at": scenario_data.get('generated_at'),
            "generation_config": scenario_data.get('generation_config', {})
        }
        
        return scenario
    
    def get_available_specialties(self) -> List[str]:
        """get available specialties for dynamic generation"""
        return self.dynamic_generator.get_available_specialties()
    
    def get_available_difficulties(self) -> List[str]:
        """get available difficulties for dynamic generation"""
        return self.dynamic_generator.get_available_difficulties()
    
    def set_dynamic_config(self, config: DynamicScenarioConfig):
        """set dynamic generation configuration"""
        self.dynamic_config = config
        self.dynamic_generator.set_config(config)
    
    # Original ScenarioManager Methods (unchanged)
    
    def get_available_scenarios(self) -> List[Dict[str, Any]]:
        """get list of available scenarios"""
        available = []
        for scenario_id, scenario in self.scenarios.items():
            available.append({
                "id": scenario_id,
                "title": scenario.title,
                "description": scenario.description,
                "difficulty": scenario.difficulty,
                "specialty": scenario.specialty,
                "time_limit": scenario.time_limit,
                "points_possible": scenario.points_possible
            })
        return available
    
    def get_scenario(self, scenario_id: str) -> Optional[Scenario]:
        """get a specific scenario by ID"""
        return self.scenarios.get(scenario_id)
    
    def start_scenario(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        """start a scenario"""
        scenario = self.get_scenario(scenario_id)
        if not scenario:
            return None
        
        self.current_scenario = scenario
        self.scenario_start_time = datetime.now()
        
        return {
            "scenario_id": scenario_id,
            "title": scenario.title,
            "description": scenario.description,
            "difficulty": scenario.difficulty,
            "specialty": scenario.specialty,
            "learning_objectives": scenario.learning_objectives,
            "initial_patient_state": scenario.initial_patient_state,
            "correct_diagnosis": scenario.correct_diagnosis,
            "optimal_actions": scenario.optimal_actions,
            "time_limit": scenario.time_limit,
            "points_possible": scenario.points_possible,
            "start_time": self.scenario_start_time.isoformat()
        }
    
    def get_scenario_progress(self) -> Optional[Dict[str, Any]]:
        """get current scenario progress"""
        if not self.current_scenario or not self.scenario_start_time:
            return None
        
        elapsed_time = (datetime.now() - self.scenario_start_time).total_seconds() / 60
        
        return {
            "scenario_id": self.current_scenario.id,
            "elapsed_time": elapsed_time,
            "time_limit": self.current_scenario.time_limit,
            "time_remaining": max(0, self.current_scenario.time_limit - elapsed_time)
        }
    
    def end_scenario(self) -> Optional[Dict[str, Any]]:
        """end current scenario"""
        if not self.current_scenario or not self.scenario_start_time:
            return None
        
        elapsed_time = (datetime.now() - self.scenario_start_time).total_seconds() / 60
        
        result = {
            "scenario_id": self.current_scenario.id,
            "elapsed_time": elapsed_time,
            "time_limit": self.current_scenario.time_limit,
            "completed": elapsed_time <= self.current_scenario.time_limit
        }
        
        self.current_scenario = None
        self.scenario_start_time = None
        
        return result
    
    def get_scenarios_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """get scenarios by difficulty level"""
        filtered = []
        for scenario_id, scenario in self.scenarios.items():
            if scenario.difficulty.lower() == difficulty.lower():
                filtered.append({
                    "id": scenario_id,
                    "title": scenario.title,
                    "description": scenario.description,
                    "difficulty": scenario.difficulty,
                    "specialty": scenario.specialty
                })
        return filtered
    
    def get_scenarios_by_specialty(self, specialty: str) -> List[Dict[str, Any]]:
        """get scenarios by specialty"""
        filtered = []
        for scenario_id, scenario in self.scenarios.items():
            if scenario.specialty.lower() == specialty.lower():
                filtered.append({
                    "id": scenario_id,
                    "title": scenario.title,
                    "description": scenario.description,
                    "difficulty": scenario.difficulty,
                    "specialty": scenario.specialty
                })
        return filtered 