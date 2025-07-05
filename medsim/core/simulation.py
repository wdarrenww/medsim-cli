"""
discrete-event simulation engine for medical scenarios
"""

import simpy
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@dataclass
class PatientState:
    """represents the current state of a patient"""
    patient_id: str
    name: str
    age: int
    gender: str
    vital_signs: Dict[str, float] = field(default_factory=dict)
    symptoms: List[str] = field(default_factory=list)
    medications: List[str] = field(default_factory=list)
    lab_results: Dict[str, Any] = field(default_factory=dict)
    procedures: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def update_vital_signs(self, vitals: Dict[str, float]) -> None:
        """update patient vital signs"""
        self.vital_signs.update(vitals)
        self.timestamp = datetime.now()
    
    def add_symptom(self, symptom: str) -> None:
        """add a symptom to the patient"""
        if symptom not in self.symptoms:
            self.symptoms.append(symptom)
    
    def add_medication(self, medication: str) -> None:
        """add a medication to the patient"""
        if medication not in self.medications:
            self.medications.append(medication)
    
    def add_lab_result(self, test_name: str, result: Any) -> None:
        """add a lab result"""
        self.lab_results[test_name] = result
    
    def add_procedure(self, procedure: str) -> None:
        """add a procedure to the patient"""
        if procedure not in self.procedures:
            self.procedures.append(procedure)


class MedicalSimulation:
    """main simulation engine for medical scenarios"""
    
    def __init__(self):
        self.env = simpy.Environment()
        self.patients: Dict[str, PatientState] = {}
        self.current_time = 0
        self.events: List[Dict[str, Any]] = []
        self.is_running = False
        
    def add_patient(self, patient_id: str, name: str, age: int, gender: str) -> PatientState:
        """add a new patient to the simulation"""
        patient = PatientState(
            patient_id=patient_id,
            name=name,
            age=age,
            gender=gender
        )
        self.patients[patient_id] = patient
        logger.info(f"added patient: {name} (id: {patient_id})")
        return patient
    
    def get_patient(self, patient_id: str) -> Optional[PatientState]:
        """get a patient by id"""
        return self.patients.get(patient_id)
    
    def schedule_event(self, delay: float, event_type: str, data: Dict[str, Any]) -> None:
        """schedule an event to occur after a delay"""
        event = {
            'type': event_type,
            'data': data,
            'scheduled_time': self.current_time + delay
        }
        self.events.append(event)
        self.env.process(self._execute_event(delay, event))
    
    def _execute_event(self, delay: float, event: Dict[str, Any]) -> None:
        """execute a scheduled event"""
        yield self.env.timeout(delay)
        self._process_event(event)
    
    def _process_event(self, event: Dict[str, Any]) -> None:
        """process an event and update simulation state"""
        event_type = event['type']
        data = event['data']
        
        if event_type == 'vital_signs_change':
            patient_id = data.get('patient_id')
            vitals = data.get('vital_signs', {})
            if patient_id in self.patients:
                self.patients[patient_id].update_vital_signs(vitals)
                logger.info(f"updated vitals for patient {patient_id}: {vitals}")
        
        elif event_type == 'symptom_onset':
            patient_id = data.get('patient_id')
            symptom = data.get('symptom')
            if patient_id in self.patients:
                self.patients[patient_id].add_symptom(symptom)
                logger.info(f"patient {patient_id} developed symptom: {symptom}")
        
        elif event_type == 'medication_effect':
            patient_id = data.get('patient_id')
            medication = data.get('medication')
            effect = data.get('effect')
            if patient_id in self.patients:
                # apply medication effect to patient state
                logger.info(f"medication {medication} effect on patient {patient_id}: {effect}")
    
    def start_simulation(self) -> None:
        """start the simulation"""
        self.is_running = True
        logger.info("simulation started")
    
    def pause_simulation(self) -> None:
        """pause the simulation"""
        self.is_running = False
        logger.info("simulation paused")
    
    def step_simulation(self, time_step: float = 1.0) -> None:
        """advance simulation by one time step"""
        if not self.is_running:
            return
        
        # advance simpy environment
        self.env.run(until=self.env.now + time_step)
        self.current_time = self.env.now
        
        # process any events that should occur at this time
        current_events = [e for e in self.events if e['scheduled_time'] <= self.current_time]
        for event in current_events:
            self._process_event(event)
            self.events.remove(event)
    
    def get_simulation_state(self) -> Dict[str, Any]:
        """get current simulation state"""
        return {
            'current_time': self.current_time,
            'is_running': self.is_running,
            'patient_count': len(self.patients),
            'pending_events': len(self.events)
        }
    
    def reset_simulation(self) -> None:
        """reset the simulation to initial state"""
        self.env = simpy.Environment()
        self.current_time = 0
        self.events.clear()
        self.is_running = False
        logger.info("simulation reset") 