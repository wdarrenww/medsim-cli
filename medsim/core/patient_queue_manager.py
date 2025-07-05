"""
patient queue manager for handling multiple simultaneous patients
manages dynamic patient generation, queue logic, and realistic patient flow
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import random
import uuid

from .dynamic_patient_loader import DynamicPatientLoader, PatientLoadConfig, PatientLoadResult
from .disease_progression import DiseaseProgressionEngine
from ..generation.enhanced_scenario_generator import EnhancedScenarioGenerator, EnhancedScenarioConfig


@dataclass
class PatientQueueItem:
    """represents a patient in the queue"""
    patient_id: str
    patient_result: PatientLoadResult
    arrival_time: datetime
    priority_score: float  # 0.0 to 1.0, higher = more urgent
    status: str  # waiting, active, completed, transferred
    assigned_provider: Optional[str] = None
    estimated_completion_time: Optional[datetime] = None
    actual_completion_time: Optional[datetime] = None
    complexity_level: str = "moderate"
    specialty_needed: Optional[str] = None
    notes: List[str] = field(default_factory=list)


@dataclass
class QueueMetrics:
    """metrics for queue performance"""
    total_patients: int = 0
    active_patients: int = 0
    average_wait_time: timedelta = timedelta(0)
    average_completion_time: timedelta = timedelta(0)
    patients_per_hour: float = 0.0
    complexity_distribution: Dict[str, int] = field(default_factory=dict)
    specialty_distribution: Dict[str, int] = field(default_factory=dict)


class PatientQueueManager:
    """manages patient queue with dynamic generation and realistic flow"""
    
    def __init__(self, max_simultaneous_patients: int = 3):
        self.max_simultaneous_patients = max_simultaneous_patients
        self.patient_loader = DynamicPatientLoader()
        self.disease_engine = DiseaseProgressionEngine()
        self.scenario_generator = EnhancedScenarioGenerator()
        
        # queue state
        self.patients: Dict[str, PatientQueueItem] = {}
        self.waiting_queue: List[str] = []
        self.active_patients: List[str] = []
        self.completed_patients: List[str] = []
        
        # generation settings
        self.specialty_weights = {
            "emergency_medicine": 0.4,
            "cardiology": 0.2,
            "neurology": 0.15,
            "rheumatology": 0.1,
            "hematology": 0.1,
            "infectious_disease": 0.05
        }
        
        self.complexity_weights = {
            "simple": 0.3,
            "moderate": 0.5,
            "complex": 0.2
        }
        
        self.difficulty_weights = {
            "easy": 0.2,
            "medium": 0.5,
            "hard": 0.3
        }
        
        # timing settings
        self.arrival_rate_per_hour = 2.5  # patients per hour
        self.completion_time_ranges = {
            "simple": (15, 45),  # minutes
            "moderate": (30, 90),
            "complex": (60, 180)
        }
        
        # metrics
        self.metrics = QueueMetrics()
        self.start_time = datetime.now()
    
    def generate_new_patient(self, current_time: datetime) -> PatientQueueItem:
        """generate a new patient with dynamic variation"""
        # select specialty based on weights
        specialty = self._select_specialty()
        
        # select complexity and difficulty
        complexity = self._select_complexity()
        difficulty = self._select_difficulty()
        
        # create patient load config
        patient_config = PatientLoadConfig(
            specialty=specialty,
            difficulty=difficulty,
            complexity_level=complexity,
            social_determinants=True,
            comorbidities=True,
            disease_progression=True,
            realistic_vitals=True,
            medication_history=True
        )
        
        # load patient
        patient_result = self.patient_loader.load_patient(patient_config)
        
        # calculate priority score
        priority_score = self._calculate_priority_score(patient_result, complexity, difficulty)
        
        # estimate completion time
        completion_minutes = random.randint(*self.completion_time_ranges[complexity])
        estimated_completion = current_time + timedelta(minutes=completion_minutes)
        
        # create queue item
        patient_id = f"P{len(self.patients) + 1:03d}"
        queue_item = PatientQueueItem(
            patient_id=patient_id,
            patient_result=patient_result,
            arrival_time=current_time,
            priority_score=priority_score,
            status="waiting",
            complexity_level=complexity,
            specialty_needed=specialty,
            estimated_completion_time=estimated_completion
        )
        
        return queue_item
    
    def add_patient_to_queue(self, patient: PatientQueueItem):
        """add patient to queue"""
        self.patients[patient.patient_id] = patient
        self.waiting_queue.append(patient.patient_id)
        
        # update metrics
        self.metrics.total_patients += 1
        self.metrics.complexity_distribution[patient.complexity_level] = \
            self.metrics.complexity_distribution.get(patient.complexity_level, 0) + 1
        self.metrics.specialty_distribution[patient.specialty_needed] = \
            self.metrics.specialty_distribution.get(patient.specialty_needed, 0) + 1
    
    def activate_patient(self, patient_id: str, provider: str, current_time: datetime):
        """activate a patient (start treatment)"""
        if patient_id in self.patients and patient_id in self.waiting_queue:
            patient = self.patients[patient_id]
            patient.status = "active"
            patient.assigned_provider = provider
            
            # update estimated completion time based on activation time
            completion_minutes = random.randint(*self.completion_time_ranges[patient.complexity_level])
            patient.estimated_completion_time = current_time + timedelta(minutes=completion_minutes)
            
            # move from waiting to active
            self.waiting_queue.remove(patient_id)
            self.active_patients.append(patient_id)
            
            # update metrics
            self.metrics.active_patients = len(self.active_patients)
    
    def complete_patient(self, patient_id: str, current_time: datetime):
        """complete a patient's treatment"""
        if patient_id in self.patients and patient_id in self.active_patients:
            patient = self.patients[patient_id]
            patient.status = "completed"
            patient.actual_completion_time = current_time
            
            # move from active to completed
            self.active_patients.remove(patient_id)
            self.completed_patients.append(patient_id)
            
            # update metrics
            self.metrics.active_patients = len(self.active_patients)
    
    def transfer_patient(self, patient_id: str, destination: str, current_time: datetime):
        """transfer patient to another service"""
        if patient_id in self.patients:
            patient = self.patients[patient_id]
            patient.status = "transferred"
            patient.notes.append(f"Transferred to {destination} at {current_time}")
            
            # remove from active if present
            if patient_id in self.active_patients:
                self.active_patients.remove(patient_id)
                self.metrics.active_patients = len(self.active_patients)
    
    def get_next_patient(self) -> Optional[str]:
        """get next patient from waiting queue based on priority"""
        if not self.waiting_queue:
            return None
        
        # sort by priority score (highest first)
        sorted_queue = sorted(
            self.waiting_queue,
            key=lambda pid: self.patients[pid].priority_score,
            reverse=True
        )
        
        return sorted_queue[0] if sorted_queue else None
    
    def get_available_slots(self) -> int:
        """get number of available slots for new patients"""
        return self.max_simultaneous_patients - len(self.active_patients)
    
    def can_accept_new_patient(self) -> bool:
        """check if can accept new patient"""
        return len(self.active_patients) < self.max_simultaneous_patients
    
    def get_queue_status(self) -> Dict[str, Any]:
        """get current queue status"""
        return {
            "waiting_count": len(self.waiting_queue),
            "active_count": len(self.active_patients),
            "completed_count": len(self.completed_patients),
            "available_slots": self.get_available_slots(),
            "waiting_patients": [
                {
                    "id": pid,
                    "priority": self.patients[pid].priority_score,
                    "complexity": self.patients[pid].complexity_level,
                    "specialty": self.patients[pid].specialty_needed,
                    "wait_time": datetime.now() - self.patients[pid].arrival_time
                }
                for pid in self.waiting_queue
            ],
            "active_patients": [
                {
                    "id": pid,
                    "provider": self.patients[pid].assigned_provider,
                    "estimated_completion": self.patients[pid].estimated_completion_time
                }
                for pid in self.active_patients
            ]
        }
    
    def update_metrics(self, current_time: datetime):
        """update queue metrics"""
        # calculate average wait time
        if self.completed_patients:
            total_wait_time = timedelta(0)
            for pid in self.completed_patients:
                patient = self.patients[pid]
                if patient.actual_completion_time:
                    wait_time = patient.actual_completion_time - patient.arrival_time
                    total_wait_time += wait_time
            
            self.metrics.average_wait_time = total_wait_time / len(self.completed_patients)
        
        # calculate patients per hour
        elapsed_hours = (current_time - self.start_time).total_seconds() / 3600
        if elapsed_hours > 0:
            self.metrics.patients_per_hour = len(self.completed_patients) / elapsed_hours
    
    def _select_specialty(self) -> str:
        """select specialty based on weights"""
        specialties = list(self.specialty_weights.keys())
        weights = list(self.specialty_weights.values())
        return random.choices(specialties, weights=weights)[0]
    
    def _select_complexity(self) -> str:
        """select complexity based on weights"""
        complexities = list(self.complexity_weights.keys())
        weights = list(self.complexity_weights.values())
        return random.choices(complexities, weights=weights)[0]
    
    def _select_difficulty(self) -> str:
        """select difficulty based on weights"""
        difficulties = list(self.difficulty_weights.keys())
        weights = list(self.difficulty_weights.values())
        return random.choices(difficulties, weights=weights)[0]
    
    def _calculate_priority_score(self, patient_result: PatientLoadResult, 
                                complexity: str, difficulty: str) -> float:
        """calculate priority score based on multiple factors"""
        score = 0.0
        
        # medical urgency (disease severity)
        for disease_state in patient_result.disease_states:
            score += disease_state.severity_score * 0.4
        
        # social factors (higher risk = higher priority)
        score += patient_result.risk_score * 0.2
        
        # complexity factor
        complexity_scores = {"simple": 0.1, "moderate": 0.3, "complex": 0.5}
        score += complexity_scores.get(complexity, 0.3)
        
        # difficulty factor
        difficulty_scores = {"easy": 0.1, "medium": 0.3, "hard": 0.5}
        score += difficulty_scores.get(difficulty, 0.3)
        
        # random variation
        score += random.uniform(-0.1, 0.1)
        
        return max(0.0, min(1.0, score))
    
    def get_patient_summary(self, patient_id: str) -> Dict[str, Any]:
        """get detailed patient summary"""
        if patient_id not in self.patients:
            return {}
        
        patient = self.patients[patient_id]
        patient_result = patient.patient_result
        
        return {
            "patient_id": patient_id,
            "name": patient_result.patient.name,
            "age": patient_result.patient.age,
            "gender": patient_result.patient.gender,
            "arrival_time": patient.arrival_time,
            "priority_score": patient.priority_score,
            "status": patient.status,
            "complexity": patient.complexity_level,
            "specialty": patient.specialty_needed,
            "conditions": patient_result.patient.conditions,
            "symptoms": patient_result.patient.symptoms,
            "social_determinants": [d.value for d in patient_result.patient.social_history.social_determinants],
            "medical_complexity": patient_result.medical_complexity,
            "risk_score": patient_result.risk_score,
            "disease_states": [
                {
                    "name": d.disease_name,
                    "stage": d.stage.value,
                    "severity": d.severity_score
                }
                for d in patient_result.disease_states
            ],
            "estimated_completion": patient.estimated_completion_time,
            "actual_completion": patient.actual_completion_time,
            "notes": patient.notes
        }
    
    def get_queue_metrics(self) -> QueueMetrics:
        """get current queue metrics"""
        return self.metrics 