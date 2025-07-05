"""
continuous simulation engine for managing full loop logic
handles multiple patients simultaneously with dynamic generation and realistic flow
"""

from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import random
import time
import threading
from enum import Enum

from .patient_queue_manager import PatientQueueManager, PatientQueueItem, QueueMetrics
from .dynamic_patient_loader import DynamicPatientLoader, PatientLoadConfig
from .disease_progression import DiseaseProgressionEngine
from ..generation.enhanced_scenario_generator import EnhancedScenarioGenerator, EnhancedScenarioConfig


class SimulationState(Enum):
    """simulation states"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


@dataclass
class SimulationEvent:
    """represents a simulation event"""
    timestamp: datetime
    event_type: str  # patient_arrival, patient_activation, patient_completion, patient_transfer
    patient_id: str
    description: str
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SimulationMetrics:
    """comprehensive simulation metrics"""
    total_patients_processed: int = 0
    total_simulation_time: timedelta = timedelta(0)
    average_patients_per_hour: float = 0.0
    average_wait_time: timedelta = timedelta(0)
    average_completion_time: timedelta = timedelta(0)
    specialty_distribution: Dict[str, int] = field(default_factory=dict)
    complexity_distribution: Dict[str, int] = field(default_factory=dict)
    difficulty_distribution: Dict[str, int] = field(default_factory=dict)
    provider_performance: Dict[str, Dict[str, Any]] = field(default_factory=dict)


class ContinuousSimulationEngine:
    """continuous simulation engine with full loop logic"""
    
    def __init__(self, max_simultaneous_patients: int = 3, 
                 arrival_rate_per_hour: float = 2.5):
        self.max_simultaneous_patients = max_simultaneous_patients
        self.arrival_rate_per_hour = arrival_rate_per_hour
        
        # core components
        self.queue_manager = PatientQueueManager(max_simultaneous_patients)
        self.disease_engine = DiseaseProgressionEngine()
        self.scenario_generator = EnhancedScenarioGenerator()
        
        # simulation state
        self.state = SimulationState.IDLE
        self.current_time = datetime.now()
        self.simulation_start_time = None
        self.simulation_end_time = None
        
        # events and metrics
        self.events: List[SimulationEvent] = []
        self.metrics = SimulationMetrics()
        
        # callbacks for external monitoring
        self.event_callbacks: List[Callable[[SimulationEvent], None]] = []
        self.metrics_callbacks: List[Callable[[SimulationMetrics], None]] = []
        
        # simulation settings
        self.time_acceleration = 1.0  # 1.0 = real time, 2.0 = 2x speed
        self.event_interval_seconds = 30  # check for events every 30 seconds
        self.max_simulation_hours = 24  # maximum simulation duration
        
        # providers (simulated healthcare workers)
        self.providers = ["Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Brown"]
        self.available_providers = self.providers.copy()
        
        # threading for continuous operation
        self.simulation_thread = None
        self.stop_simulation = False
    
    def start_simulation(self, duration_hours: Optional[float] = None):
        """start continuous simulation"""
        if self.state == SimulationState.RUNNING:
            return
        
        self.state = SimulationState.RUNNING
        self.simulation_start_time = datetime.now()
        self.current_time = self.simulation_start_time
        self.stop_simulation = False
        
        # start simulation thread
        self.simulation_thread = threading.Thread(
            target=self._run_simulation_loop,
            args=(duration_hours,)
        )
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
    
    def pause_simulation(self):
        """pause simulation"""
        if self.state == SimulationState.RUNNING:
            self.state = SimulationState.PAUSED
    
    def resume_simulation(self):
        """resume simulation"""
        if self.state == SimulationState.PAUSED:
            self.state = SimulationState.RUNNING
    
    def stop_simulation_engine(self):
        """stop simulation"""
        self.state = SimulationState.STOPPED
        self.stop_simulation = True
        if self.simulation_thread and self.simulation_thread.is_alive():
            self.simulation_thread.join(timeout=5)
    
    def _run_simulation_loop(self, duration_hours: Optional[float] = None):
        """main simulation loop"""
        end_time = None
        if duration_hours:
            end_time = self.simulation_start_time + timedelta(hours=duration_hours)
        else:
            end_time = self.simulation_start_time + timedelta(hours=self.max_simulation_hours)
        
        while (self.state == SimulationState.RUNNING and 
               not self.stop_simulation and 
               self.current_time < end_time):
            
            # process simulation step
            self._process_simulation_step()
            
            # advance time
            self.current_time += timedelta(seconds=self.event_interval_seconds * self.time_acceleration)
            
            # update metrics
            self._update_simulation_metrics()
            
            # small delay to prevent excessive CPU usage
            time.sleep(0.1)
        
        self.simulation_end_time = self.current_time
        self.state = SimulationState.STOPPED
    
    def _process_simulation_step(self):
        """process one simulation step"""
        # check for new patient arrivals
        if self._should_generate_new_patient():
            self._generate_and_add_patient()
        
        # check for patient completions
        self._check_patient_completions()
        
        # activate waiting patients if slots available
        self._activate_waiting_patients()
        
        # progress disease states for active patients
        self._progress_active_patient_diseases()
    
    def _should_generate_new_patient(self) -> bool:
        """determine if should generate new patient"""
        # check if can accept new patient
        if not self.queue_manager.can_accept_new_patient():
            return False
        
        # calculate arrival probability based on rate
        arrival_probability = (self.arrival_rate_per_hour * 
                             (self.event_interval_seconds / 3600))
        
        return random.random() < arrival_probability
    
    def _generate_and_add_patient(self):
        """generate and add new patient to queue"""
        # generate new patient
        patient = self.queue_manager.generate_new_patient(self.current_time)
        
        # add to queue
        self.queue_manager.add_patient_to_queue(patient)
        
        # create event
        event = SimulationEvent(
            timestamp=self.current_time,
            event_type="patient_arrival",
            patient_id=patient.patient_id,
            description=f"Patient {patient.patient_id} arrived with {patient.complexity_level} {patient.specialty_needed} case",
            data={
                "priority_score": patient.priority_score,
                "complexity": patient.complexity_level,
                "specialty": patient.specialty_needed,
                "conditions": patient.patient_result.patient.conditions
            }
        )
        
        self.events.append(event)
        self._notify_event_callbacks(event)
    
    def _check_patient_completions(self):
        """check for patient completions"""
        for patient_id in self.queue_manager.active_patients[:]:  # copy to avoid modification during iteration
            patient = self.queue_manager.patients[patient_id]
            
            if (patient.estimated_completion_time and 
                self.current_time >= patient.estimated_completion_time):
                
                # complete patient
                self.queue_manager.complete_patient(patient_id, self.current_time)
                
                # free up provider
                if patient.assigned_provider in self.providers:
                    self.available_providers.append(patient.assigned_provider)
                
                # create event
                event = SimulationEvent(
                    timestamp=self.current_time,
                    event_type="patient_completion",
                    patient_id=patient_id,
                    description=f"Patient {patient_id} completed treatment",
                    data={
                        "provider": patient.assigned_provider,
                        "actual_completion_time": patient.actual_completion_time.isoformat(),
                        "estimated_completion_time": patient.estimated_completion_time.isoformat()
                    }
                )
                
                self.events.append(event)
                self._notify_event_callbacks(event)
    
    def _activate_waiting_patients(self):
        """activate waiting patients if slots and providers available"""
        while (self.queue_manager.get_available_slots() > 0 and 
               self.available_providers and 
               self.queue_manager.waiting_queue):
            
            # get next patient by priority
            next_patient_id = self.queue_manager.get_next_patient()
            if not next_patient_id:
                break
            
            # assign provider
            provider = random.choice(self.available_providers)
            self.available_providers.remove(provider)
            
            # activate patient
            self.queue_manager.activate_patient(next_patient_id, provider, self.current_time)
            
            # create event
            event = SimulationEvent(
                timestamp=self.current_time,
                event_type="patient_activation",
                patient_id=next_patient_id,
                description=f"Patient {next_patient_id} activated by {provider}",
                data={
                    "provider": provider,
                    "priority_score": self.queue_manager.patients[next_patient_id].priority_score
                }
            )
            
            self.events.append(event)
            self._notify_event_callbacks(event)
    
    def _progress_active_patient_diseases(self):
        """progress disease states for active patients"""
        for patient_id in self.queue_manager.active_patients:
            patient = self.queue_manager.patients[patient_id]
            
            # progress each disease state
            for disease_state in patient.patient_result.disease_states:
                # progress disease by time interval
                progressed_state = self.disease_engine.progress_disease(
                    patient.patient_result.patient.patient_id,
                    disease_state.disease_name,
                    timedelta(seconds=self.event_interval_seconds * self.time_acceleration)
                )
                
                if progressed_state and progressed_state.severity_score > 0.9:
                    # critical condition - may need transfer
                    if random.random() < 0.1:  # 10% chance of transfer
                        destination = random.choice(["ICU", "OR", "Specialist"])
                        self.queue_manager.transfer_patient(patient_id, destination, self.current_time)
                        
                        event = SimulationEvent(
                            timestamp=self.current_time,
                            event_type="patient_transfer",
                            patient_id=patient_id,
                            description=f"Patient {patient_id} transferred to {destination} due to critical condition",
                            data={
                                "destination": destination,
                                "reason": "critical_condition",
                                "disease": disease_state.disease_name,
                                "severity": disease_state.severity_score
                            }
                        )
                        
                        self.events.append(event)
                        self._notify_event_callbacks(event)
    
    def _update_simulation_metrics(self):
        """update simulation metrics"""
        # update queue metrics
        self.queue_manager.update_metrics(self.current_time)
        
        # update simulation metrics
        if self.simulation_start_time:
            self.metrics.total_simulation_time = self.current_time - self.simulation_start_time
        
        self.metrics.total_patients_processed = len(self.queue_manager.completed_patients)
        self.metrics.average_wait_time = self.queue_manager.metrics.average_wait_time
        self.metrics.average_patients_per_hour = self.queue_manager.metrics.patients_per_hour
        
        # update distributions
        self.metrics.specialty_distribution = self.queue_manager.metrics.specialty_distribution.copy()
        self.metrics.complexity_distribution = self.queue_manager.metrics.complexity_distribution.copy()
        
        # notify metrics callbacks
        self._notify_metrics_callbacks()
    
    def add_event_callback(self, callback: Callable[[SimulationEvent], None]):
        """add event callback for external monitoring"""
        self.event_callbacks.append(callback)
    
    def add_metrics_callback(self, callback: Callable[[SimulationMetrics], None]):
        """add metrics callback for external monitoring"""
        self.metrics_callbacks.append(callback)
    
    def _notify_event_callbacks(self, event: SimulationEvent):
        """notify event callbacks"""
        for callback in self.event_callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in event callback: {e}")
    
    def _notify_metrics_callbacks(self):
        """notify metrics callbacks"""
        for callback in self.metrics_callbacks:
            try:
                callback(self.metrics)
            except Exception as e:
                print(f"Error in metrics callback: {e}")
    
    def get_simulation_status(self) -> Dict[str, Any]:
        """get current simulation status"""
        return {
            "state": self.state.value,
            "current_time": self.current_time,
            "simulation_start_time": self.simulation_start_time,
            "simulation_end_time": self.simulation_end_time,
            "total_events": len(self.events),
            "queue_status": self.queue_manager.get_queue_status(),
            "metrics": {
                "total_patients_processed": self.metrics.total_patients_processed,
                "total_simulation_time": str(self.metrics.total_simulation_time),
                "average_patients_per_hour": self.metrics.average_patients_per_hour,
                "average_wait_time": str(self.metrics.average_wait_time)
            }
        }
    
    def get_recent_events(self, count: int = 10) -> List[SimulationEvent]:
        """get recent simulation events"""
        return self.events[-count:] if self.events else []
    
    def get_patient_details(self, patient_id: str) -> Dict[str, Any]:
        """get detailed patient information"""
        return self.queue_manager.get_patient_summary(patient_id)
    
    def get_simulation_metrics(self) -> SimulationMetrics:
        """get current simulation metrics"""
        return self.metrics
    
    def set_time_acceleration(self, acceleration: float):
        """set simulation time acceleration"""
        self.time_acceleration = max(0.1, min(10.0, acceleration))
    
    def set_arrival_rate(self, rate_per_hour: float):
        """set patient arrival rate"""
        self.arrival_rate_per_hour = max(0.1, min(10.0, rate_per_hour))
        self.queue_manager.arrival_rate_per_hour = rate_per_hour 