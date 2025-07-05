"""
discrete-event simulation engine for medical scenarios
"""

import simpy
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging
import json
from .patient import EnhancedPatientProfile, PatientProfileGenerator, EmotionalState
from .physiology import EnhancedPhysiologicalEngine
from .pharmacology import PKPDEngine
from .drug_db import drug_db
from .monitoring import MonitoringSystem, DrugLevelMonitor, DrugLevel

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


@dataclass
class SimulationState:
    """current state of the simulation"""
    patient_id: str
    current_time: datetime
    vital_signs: Dict[str, float] = field(default_factory=dict)
    lab_values: Dict[str, float] = field(default_factory=dict)
    active_drugs: Dict[str, DrugLevel] = field(default_factory=dict)
    symptoms: List[str] = field(default_factory=list)
    procedures_performed: List[str] = field(default_factory=list)
    monitoring_active: bool = False


class MedicalSimulation:
    """main medical simulation engine"""
    
    def __init__(self):
        self.env = simpy.Environment()
        self.patient_state = None
        self.physiological_engine = EnhancedPhysiologicalEngine()
        self.patient_generator = PatientProfileGenerator()
        self.is_running = False
        self.current_time = 0
        self.events = []
        
        # enhanced systems
        self.enhanced_patient = None
        self.stress_level = 0.0
        
        # pk/pd engine
        self.pkpd_engine = PKPDEngine(drug_db)
        self.patient_weight = 70.0  # default, can be set from patient profile
        
        self.monitoring = MonitoringSystem()
        self.drug_monitor = DrugLevelMonitor(self.monitoring)
        
        self.current_state = SimulationState(
            patient_id="default",
            current_time=datetime.now()
        )
        
        # new: track all patients
        self.patients = {}
        
        # initialize monitoring callbacks
        self.monitoring.add_alert_callback(self._on_alert)
        
    def start_simulation(self, patient_profile: Optional[Dict[str, Any]] = None):
        """start a new simulation session"""
        if patient_profile is None:
            # generate a new patient
            self.enhanced_patient = self.patient_generator.generate_patient()
        else:
            # use provided patient profile
            self.enhanced_patient = EnhancedPatientProfile.from_dict(patient_profile)
        
        # initialize patient state with enhanced data
        self.patient_state = PatientState(
            patient_id=self.enhanced_patient.patient_id,
            name=self.enhanced_patient.name,
            age=self.enhanced_patient.age,
            gender=self.enhanced_patient.gender,
            vital_signs={
                "blood_pressure_systolic": self.enhanced_patient.vitals.get("blood_pressure_systolic", 120),
                "blood_pressure_diastolic": self.enhanced_patient.vitals.get("blood_pressure_diastolic", 80),
                "heart_rate": self.enhanced_patient.vitals.get("heart_rate", 80),
                "respiratory_rate": self.enhanced_patient.vitals.get("respiratory_rate", 16),
                "temperature": self.enhanced_patient.vitals.get("temperature", 98.6),
                "oxygen_saturation": self.enhanced_patient.vitals.get("oxygen_saturation", 98)
            },
            symptoms=self.enhanced_patient.symptoms.copy(),
            medications=self.enhanced_patient.medications.copy(),
            lab_results=self.enhanced_patient.lab_results.copy()
        )
        
        # initialize physiological engine
        self.physiological_engine = EnhancedPhysiologicalEngine()
        
        # add any existing conditions to physiological engine
        for condition in self.enhanced_patient.conditions:
            self.physiological_engine.add_disease(condition, severity=0.5)
        
        self.is_running = True
        self.current_time = 0
        self.events = []
        
        # schedule initial events
        self._schedule_physiological_updates()
        
        self.current_state.monitoring_active = True
        self.monitoring.start_monitoring()
        
        return self.enhanced_patient
    
    def _schedule_physiological_updates(self):
        """schedule regular physiological updates"""
        def update_physiology():
            while self.is_running:
                # update physiological systems
                self.physiological_engine.update_systems(
                    stress_level=self.stress_level,
                    medications=self.patient_state.medications
                )
                
                # update patient state with new vital signs
                new_vitals = self.physiological_engine.get_vital_signs()
                self.patient_state.vital_signs.update(new_vitals)
                
                # update enhanced patient emotional state based on stress
                if self.stress_level > 0.7:
                    self.enhanced_patient.update_emotional_state(EmotionalState.ANXIOUS)
                elif self.stress_level > 0.3:
                    self.enhanced_patient.update_emotional_state(EmotionalState.CALM)
                
                yield self.env.timeout(1)  # update every time step
        
        self.env.process(update_physiology())
    
    def get_patient(self, patient_id: Optional[str] = None) -> EnhancedPatientProfile:
        """get the enhanced patient profile"""
        if patient_id:
            return self.patients.get(patient_id)
        return self.enhanced_patient
    
    def update_stress_level(self, new_stress: float):
        """update patient stress level (0.0-1.0)"""
        self.stress_level = max(0.0, min(1.0, new_stress))
        
        # update patient anxiety level
        anxiety_level = int(self.stress_level * 10)
        self.enhanced_patient.update_anxiety_level(anxiety_level)
    
    def add_disease(self, disease_name: str, severity: float = 1.0):
        """add a disease to the patient"""
        self.physiological_engine.add_disease(disease_name, severity)
    
    def remove_disease(self, disease_name: str):
        """remove a disease from the patient"""
        self.physiological_engine.remove_disease(disease_name)
    
    def get_physiological_status(self) -> Dict[str, Any]:
        """get detailed physiological status"""
        return {
            "system_status": self.physiological_engine.get_system_status(),
            "lab_values": self.physiological_engine.get_lab_values(),
            "abnormal_values": self.physiological_engine.get_abnormal_values(),
            "diseases": self.physiological_engine.diseases
        }
    
    def step_simulation(self):
        """advance simulation by one time step"""
        if not self.is_running:
            return False
        
        self.env.step()
        self.current_time += 1
        
        # update pk/pd engine and physiological engine
        self.update_pkpd(dt=1.0)
        
        # update patient state with latest physiological data
        if self.physiological_engine:
            new_vitals = self.physiological_engine.get_vital_signs()
            self.patient_state.vital_signs.update(new_vitals)
        
        return True
    
    def pause_simulation(self):
        """pause the simulation"""
        self.is_running = False
    
    def resume_simulation(self):
        """resume the simulation"""
        self.is_running = True
    
    def reset_simulation(self):
        """reset the simulation to initial state"""
        self.is_running = False
        self.current_time = 0
        self.events = []
        self.stress_level = 0.0
        
        # reset physiological engine
        self.physiological_engine = EnhancedPhysiologicalEngine()
        
        # reset enhanced patient
        if self.enhanced_patient:
            self.enhanced_patient.update_emotional_state(EmotionalState.CALM)
            self.enhanced_patient.update_pain_level(0)
            self.enhanced_patient.update_anxiety_level(0)
        
        self.current_state.monitoring_active = False
        self.monitoring.stop_monitoring()
    
    def save_session(self, filename: str):
        """save current simulation session"""
        session_data = {
            "patient": self.enhanced_patient.to_dict() if self.enhanced_patient else None,
            "patient_state": self.patient_state.to_dict() if self.patient_state else None,
            "physiological_status": self.get_physiological_status(),
            "current_time": self.current_time,
            "stress_level": self.stress_level,
            "is_running": self.is_running,
            "monitoring_active": self.current_state.monitoring_active
        }
        
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
    
    def load_session(self, filename: str):
        """load a saved simulation session"""
        with open(filename, 'r') as f:
            session_data = json.load(f)
        
        # restore enhanced patient
        if session_data.get("patient"):
            self.enhanced_patient = EnhancedPatientProfile.from_dict(session_data["patient"])
        
        # restore patient state
        if session_data.get("patient_state"):
            self.patient_state = PatientState.from_dict(session_data["patient_state"])
        
        # restore physiological status
        if session_data.get("physiological_status"):
            # recreate physiological engine with saved data
            self.physiological_engine = EnhancedPhysiologicalEngine()
            
            # restore diseases
            for disease in session_data["physiological_status"].get("diseases", []):
                self.physiological_engine.add_disease(disease["name"], disease["severity"])
        
        self.current_time = session_data.get("current_time", 0)
        self.stress_level = session_data.get("stress_level", 0.0)
        self.is_running = session_data.get("is_running", False)
        
        self.current_state.monitoring_active = session_data.get("monitoring_active", False)
        if self.current_state.monitoring_active:
            self.monitoring.start_monitoring()
    
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
    
    def get_simulation_state(self) -> Dict[str, Any]:
        """get current simulation state"""
        return {
            'current_time': self.current_time,
            'is_running': self.is_running,
            'patient_count': len(self.patients),
            'pending_events': len(self.events),
            'monitoring_active': self.current_state.monitoring_active
        }
    
    def reset_simulation(self) -> None:
        """reset the simulation to initial state"""
        self.env = simpy.Environment()
        self.current_time = 0
        self.events.clear()
        self.is_running = False
        logger.info("simulation reset")

    def administer_drug(self, name: str, dose: float, route: str):
        """administer a drug to the patient"""
        admin = self.pkpd_engine.administer_drug(name, dose, route, self.patient_weight)
        
        # add to monitoring system
        drug_level = DrugLevel(
            drug_name=name,
            concentration=admin.concentration,
            therapeutic_min=0.1,  # default values - in real system would come from drug database
            therapeutic_max=10.0,
            toxic_threshold=20.0,
            status="therapeutic"
        )
        self.current_state.active_drugs[name] = drug_level
        self.drug_monitor.add_drug_level(name, drug_level)
        
        return admin

    def get_active_drugs(self):
        return self.pkpd_engine.get_active_drugs()

    def get_adverse_events(self):
        return self.pkpd_engine.get_adverse_events()

    def update_pkpd(self, dt: float = 1.0):
        self.pkpd_engine.update(dt, self.physiological_engine)

    def _on_alert(self, alert):
        """handle new alerts"""
        print(f"🚨 ALERT: {alert.level.value.upper()} - {alert.message}")
    
    def _update_vital_signs(self):
        """update vital signs from physiological engine"""
        vitals = self.physiological_engine.get_vital_signs()
        self.current_state.vital_signs = vitals
        
        # add to monitoring
        for param, value in vitals.items():
            self.monitoring.add_trend_data(param, value, self._get_unit(param))
    
    def _get_unit(self, parameter: str) -> str:
        """get unit for parameter"""
        units = {
            "heart_rate": "bpm",
            "blood_pressure_systolic": "mmHg",
            "blood_pressure_diastolic": "mmHg",
            "temperature": "°C",
            "oxygen_saturation": "%",
            "respiratory_rate": "breaths/min",
            "glucose": "mg/dL",
            "potassium": "mEq/L",
            "sodium": "mEq/L",
            "creatinine": "mg/dL",
        }
        return units.get(parameter, "units")
    
    def get_monitoring_summary(self) -> Dict[str, Any]:
        """get monitoring system summary"""
        return self.monitoring.get_monitoring_summary()
    
    def get_drug_monitoring_summary(self) -> Dict[str, Dict[str, Any]]:
        """get drug monitoring summaries"""
        return self.drug_monitor.get_all_drug_summaries()
    
    def get_active_alerts(self):
        """get active alerts"""
        return self.monitoring.get_active_alerts()
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str):
        """acknowledge an alert"""
        self.monitoring.acknowledge_alert(alert_id, acknowledged_by)
    
    def get_trend_data(self, parameter: str):
        """get trend data for parameter"""
        return self.monitoring.get_trend_data(parameter)
    
    def get_all_trends(self):
        """get all trend data"""
        return self.monitoring.get_all_trends()
    
    def update_simulation(self):
        """update simulation state"""
        if not self.is_running:
            return
        
        # update PKPD engine
        self.update_pkpd(1.0)  # 1 minute time step
        
        # update physiological systems
        self.physiological_engine.update_systems(
            stress_level=self.stress_level,
            medications=self.patient_state.medications
        )
        
        # update vital signs
        self._update_vital_signs()
        
        # update drug levels
        self._update_drug_levels()
    
    def _update_drug_levels(self):
        """update drug levels over time"""
        current_time = datetime.now()
        
        # sync with PKPD engine active drugs
        active_pkpd_drugs = self.pkpd_engine.get_active_drugs()
        
        for admin in active_pkpd_drugs:
            drug_name = admin.drug.name.lower()
            
            # update concentration from PKPD engine
            concentration = admin.update_concentration(self.pkpd_engine.current_time)
            
            # get or create drug level for monitoring
            if drug_name not in self.current_state.active_drugs:
                drug_level = DrugLevel(
                    drug_name=drug_name,
                    concentration=concentration,
                    therapeutic_min=0.1,  # default values
                    therapeutic_max=10.0,
                    toxic_threshold=20.0,
                    status="therapeutic"
                )
                self.current_state.active_drugs[drug_name] = drug_level
            else:
                drug_level = self.current_state.active_drugs[drug_name]
                drug_level.concentration = concentration
                drug_level.timestamp = current_time
            
            # update status based on concentration
            if concentration < drug_level.therapeutic_min * 0.5:
                drug_level.status = "subtherapeutic"
            elif concentration > drug_level.toxic_threshold:
                drug_level.status = "toxic"
            else:
                drug_level.status = "therapeutic"
            
            # add to monitoring
            self.drug_monitor.add_drug_level(drug_name, drug_level)
        
        # remove completed drugs from monitoring
        completed_drugs = [name for name in self.current_state.active_drugs.keys() 
                          if name not in [admin.drug.name.lower() for admin in active_pkpd_drugs]]
        for drug_name in completed_drugs:
            del self.current_state.active_drugs[drug_name]
    
    def set_patient_profile(self, profile: Dict[str, Any]):
        """set patient profile for simulation"""
        # update physiological engine with patient characteristics
        if "age" in profile:
            self.physiological_engine.set_age(profile["age"])
        if "weight" in profile:
            self.physiological_engine.set_weight(profile["weight"])
        if "height" in profile:
            self.physiological_engine.set_height(profile["height"])
        if "gender" in profile:
            self.physiological_engine.set_gender(profile["gender"])
        
        # update monitoring thresholds based on patient characteristics
        self._update_monitoring_thresholds(profile)
    
    def _update_monitoring_thresholds(self, profile: Dict[str, Any]):
        """update monitoring thresholds based on patient characteristics"""
        age = profile.get("age", 30)
        
        # adjust thresholds for age
        if age < 18:  # pediatric
            self.monitoring.alert_thresholds["heart_rate"]["high"] = 140
            self.monitoring.alert_thresholds["blood_pressure_systolic"]["low"] = 80
        elif age > 65:  # geriatric
            self.monitoring.alert_thresholds["heart_rate"]["high"] = 100
            self.monitoring.alert_thresholds["blood_pressure_systolic"]["high"] = 160
        
        # adjust for comorbidities
        if "diabetes" in profile.get("comorbidities", []):
            self.monitoring.alert_thresholds["glucose"]["high"] = 250
        if "hypertension" in profile.get("comorbidities", []):
            self.monitoring.alert_thresholds["blood_pressure_systolic"]["high"] = 160

    def add_patient(self, patient_id: str, name: str, age: int, gender: str) -> EnhancedPatientProfile:
        # create and store a new patient
        patient = self.patient_generator.generate_patient(age=age, gender=gender)
        patient.patient_id = patient_id
        patient.name = name
        patient.age = age
        patient.gender = gender
        self.patients[patient_id] = patient
        return patient 