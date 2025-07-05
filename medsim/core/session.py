"""
session management for saving and loading simulation states
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List, Set
from pathlib import Path
from dataclasses import dataclass, field
import uuid

from .simulation import MedicalSimulation, PatientState


@dataclass
class PatientSession:
    """enhanced patient session with comprehensive tracking"""
    patient_id: str
    name: str
    created_time: datetime
    last_accessed: datetime
    active_diseases: List[str] = field(default_factory=list)
    active_treatments: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    tags: Set[str] = field(default_factory=set)
    priority: str = "normal"  # low, normal, high, critical
    status: str = "active"  # active, discharged, transferred, deceased
    assigned_provider: str = ""
    room_number: str = ""
    admission_date: Optional[datetime] = None
    discharge_date: Optional[datetime] = None


class MultiPatientSessionManager:
    """enhanced session manager for multiple patients"""
    
    def __init__(self):
        self.patients: Dict[str, PatientSession] = {}
        self.current_patient_id: Optional[str] = None
        self.patient_order: List[str] = []
        self.session_start_time = datetime.now()
        self.auto_save_interval = 300  # 5 minutes
        self.last_auto_save = datetime.now()
    
    def create_patient_session(self, patient_id: str, name: str, **kwargs) -> str:
        """create a new patient session"""
        if patient_id in self.patients:
            return f"Error: Patient {patient_id} already exists"
        
        session = PatientSession(
            patient_id=patient_id,
            name=name,
            created_time=datetime.now(),
            last_accessed=datetime.now(),
            **kwargs
        )
        
        self.patients[patient_id] = session
        self.patient_order.append(patient_id)
        
        # set as current if no current patient
        if self.current_patient_id is None:
            self.current_patient_id = patient_id
        
        return f"✓ Created patient session for {name} (ID: {patient_id})"
    
    def set_current_patient(self, patient_id: str) -> str:
        """set the current active patient"""
        if patient_id not in self.patients:
            return f"Error: Patient {patient_id} not found"
        
        self.current_patient_id = patient_id
        self.patients[patient_id].last_accessed = datetime.now()
        
        return f"✓ Switched to patient {patient_id}"
    
    def get_current_patient(self) -> Optional[str]:
        """get the current patient ID"""
        return self.current_patient_id
    
    def get_current_patient_session(self) -> Optional[PatientSession]:
        """get the current patient session"""
        if self.current_patient_id:
            return self.patients.get(self.current_patient_id)
        return None
    
    def get_all_patients(self) -> List[PatientSession]:
        """get all patient sessions"""
        return list(self.patients.values())
    
    def get_active_patients(self) -> List[PatientSession]:
        """get all active patient sessions"""
        return [p for p in self.patients.values() if p.status == "active"]
    
    def get_patient_by_id(self, patient_id: str) -> Optional[PatientSession]:
        """get a specific patient session"""
        return self.patients.get(patient_id)
    
    def update_patient_status(self, patient_id: str, status: str) -> str:
        """update patient status"""
        if patient_id not in self.patients:
            return f"Error: Patient {patient_id} not found"
        
        self.patients[patient_id].status = status
        if status == "discharged":
            self.patients[patient_id].discharge_date = datetime.now()
        
        return f"✓ Updated patient {patient_id} status to {status}"
    
    def add_patient_note(self, patient_id: str, note: str) -> str:
        """add a note to a patient"""
        if patient_id not in self.patients:
            return f"Error: Patient {patient_id} not found"
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.patients[patient_id].notes.append(f"{timestamp}: {note}")
        
        return f"✓ Added note to patient {patient_id}"
    
    def add_patient_tag(self, patient_id: str, tag: str) -> str:
        """add a tag to a patient"""
        if patient_id not in self.patients:
            return f"Error: Patient {patient_id} not found"
        
        self.patients[patient_id].tags.add(tag)
        
        return f"✓ Added tag '{tag}' to patient {patient_id}"
    
    def remove_patient_tag(self, patient_id: str, tag: str) -> str:
        """remove a tag from a patient"""
        if patient_id not in self.patients:
            return f"Error: Patient {patient_id} not found"
        
        if tag in self.patients[patient_id].tags:
            self.patients[patient_id].tags.remove(tag)
            return f"✓ Removed tag '{tag}' from patient {patient_id}"
        else:
            return f"Tag '{tag}' not found on patient {patient_id}"
    
    def set_patient_priority(self, patient_id: str, priority: str) -> str:
        """set patient priority"""
        if patient_id not in self.patients:
            return f"Error: Patient {patient_id} not found"
        
        valid_priorities = ["low", "normal", "high", "critical"]
        if priority not in valid_priorities:
            return f"Error: Invalid priority. Must be one of {valid_priorities}"
        
        self.patients[patient_id].priority = priority
        
        return f"✓ Set patient {patient_id} priority to {priority}"
    
    def assign_provider(self, patient_id: str, provider: str) -> str:
        """assign a provider to a patient"""
        if patient_id not in self.patients:
            return f"Error: Patient {patient_id} not found"
        
        self.patients[patient_id].assigned_provider = provider
        
        return f"✓ Assigned {provider} to patient {patient_id}"
    
    def set_room_number(self, patient_id: str, room: str) -> str:
        """set patient room number"""
        if patient_id not in self.patients:
            return f"Error: Patient {patient_id} not found"
        
        self.patients[patient_id].room_number = room
        
        return f"✓ Set patient {patient_id} room to {room}"
    
    def get_patients_by_tag(self, tag: str) -> List[PatientSession]:
        """get patients with a specific tag"""
        return [p for p in self.patients.values() if tag in p.tags]
    
    def get_patients_by_priority(self, priority: str) -> List[PatientSession]:
        """get patients with a specific priority"""
        return [p for p in self.patients.values() if p.priority == priority]
    
    def get_patients_by_provider(self, provider: str) -> List[PatientSession]:
        """get patients assigned to a specific provider"""
        return [p for p in self.patients.values() if p.assigned_provider == provider]
    
    def get_critical_patients(self) -> List[PatientSession]:
        """get patients with critical priority or critical alerts"""
        critical = []
        for patient in self.patients.values():
            if (patient.priority == "critical" or 
                len(patient.critical_alerts) > 0 or
                patient.status == "critical"):
                critical.append(patient)
        return critical
    
    def search_patients(self, query: str) -> List[PatientSession]:
        """search patients by name, ID, or tags"""
        query = query.lower()
        results = []
        
        for patient in self.patients.values():
            if (query in patient.name.lower() or
                query in patient.patient_id.lower() or
                any(query in tag.lower() for tag in patient.tags)):
                results.append(patient)
        
        return results
    
    def get_patient_summary(self, patient_id: str) -> Dict[str, Any]:
        """get comprehensive patient summary"""
        if patient_id not in self.patients:
            return {"error": f"Patient {patient_id} not found"}
        
        patient = self.patients[patient_id]
        
        # calculate session duration
        session_duration = datetime.now() - patient.created_time
        
        return {
            'patient_id': patient.patient_id,
            'name': patient.name,
            'status': patient.status,
            'priority': patient.priority,
            'assigned_provider': patient.assigned_provider,
            'room_number': patient.room_number,
            'created_time': patient.created_time,
            'last_accessed': patient.last_accessed,
            'session_duration': str(session_duration).split('.')[0],  # remove microseconds
            'active_diseases': len(patient.active_diseases),
            'active_treatments': len(patient.active_treatments),
            'critical_alerts': len(patient.critical_alerts),
            'notes_count': len(patient.notes),
            'tags': list(patient.tags),
            'admission_date': patient.admission_date,
            'discharge_date': patient.discharge_date
        }
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """get overall session statistics"""
        total_patients = len(self.patients)
        active_patients = len([p for p in self.patients.values() if p.status == "active"])
        critical_patients = len(self.get_critical_patients())
        
        # priority breakdown
        priority_counts = {}
        for priority in ["low", "normal", "high", "critical"]:
            priority_counts[priority] = len(self.get_patients_by_priority(priority))
        
        # status breakdown
        status_counts = {}
        for status in ["active", "discharged", "transferred", "deceased"]:
            status_counts[status] = len([p for p in self.patients.values() if p.status == status])
        
        return {
            'total_patients': total_patients,
            'active_patients': active_patients,
            'critical_patients': critical_patients,
            'priority_breakdown': priority_counts,
            'status_breakdown': status_counts,
            'session_duration': str(datetime.now() - self.session_start_time).split('.')[0]
        }
    
    def export_session_data(self, filepath: str) -> str:
        """export session data to JSON file"""
        try:
            data = {
                'session_start_time': self.session_start_time.isoformat(),
                'current_patient_id': self.current_patient_id,
                'patients': {}
            }
            
            for patient_id, patient in self.patients.items():
                data['patients'][patient_id] = {
                    'patient_id': patient.patient_id,
                    'name': patient.name,
                    'created_time': patient.created_time.isoformat(),
                    'last_accessed': patient.last_accessed.isoformat(),
                    'active_diseases': patient.active_diseases,
                    'active_treatments': patient.active_treatments,
                    'critical_alerts': patient.critical_alerts,
                    'notes': patient.notes,
                    'tags': list(patient.tags),
                    'priority': patient.priority,
                    'status': patient.status,
                    'assigned_provider': patient.assigned_provider,
                    'room_number': patient.room_number,
                    'admission_date': patient.admission_date.isoformat() if patient.admission_date else None,
                    'discharge_date': patient.discharge_date.isoformat() if patient.discharge_date else None
                }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            return f"✓ Exported session data to {filepath}"
        
        except Exception as e:
            return f"Error exporting session data: {str(e)}"
    
    def import_session_data(self, filepath: str) -> str:
        """import session data from JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # clear current session
            self.patients.clear()
            self.patient_order.clear()
            
            # import patients
            for patient_id, patient_data in data['patients'].items():
                session = PatientSession(
                    patient_id=patient_data['patient_id'],
                    name=patient_data['name'],
                    created_time=datetime.fromisoformat(patient_data['created_time']),
                    last_accessed=datetime.fromisoformat(patient_data['last_accessed']),
                    active_diseases=patient_data['active_diseases'],
                    active_treatments=patient_data['active_treatments'],
                    critical_alerts=patient_data['critical_alerts'],
                    notes=patient_data['notes'],
                    tags=set(patient_data['tags']),
                    priority=patient_data['priority'],
                    status=patient_data['status'],
                    assigned_provider=patient_data['assigned_provider'],
                    room_number=patient_data['room_number'],
                    admission_date=datetime.fromisoformat(patient_data['admission_date']) if patient_data['admission_date'] else None,
                    discharge_date=datetime.fromisoformat(patient_data['discharge_date']) if patient_data['discharge_date'] else None
                )
                
                self.patients[patient_id] = session
                self.patient_order.append(patient_id)
            
            # set current patient
            self.current_patient_id = data.get('current_patient_id')
            
            return f"✓ Imported session data from {filepath}"
        
        except Exception as e:
            return f"Error importing session data: {str(e)}"
    
    def auto_save(self) -> bool:
        """perform auto-save if interval has elapsed"""
        if (datetime.now() - self.last_auto_save).total_seconds() >= self.auto_save_interval:
            self.last_auto_save = datetime.now()
            return True
        return False


# Global session manager instance
session_manager = MultiPatientSessionManager()


class SessionManager:
    """manages saving and loading simulation sessions"""
    
    def __init__(self, save_directory: str = "sessions"):
        self.save_directory = Path(save_directory)
        self.save_directory.mkdir(exist_ok=True)
    
    def save_session(self, simulation: MedicalSimulation, session_name: str) -> bool:
        """save current simulation state to file"""
        try:
            session_data = self._serialize_simulation(simulation)
            session_data['metadata'] = {
                'session_name': session_name,
                'saved_at': datetime.now().isoformat(),
                'version': '1.0'
            }
            
            filename = f"{session_name}.json"
            filepath = self.save_directory / filename
            
            with open(filepath, 'w') as f:
                json.dump(session_data, f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"error saving session: {e}")
            return False
    
    def load_session(self, session_name: str) -> Optional[MedicalSimulation]:
        """load simulation state from file"""
        try:
            filename = f"{session_name}.json"
            filepath = self.save_directory / filename
            
            if not filepath.exists():
                print(f"session file not found: {filename}")
                return None
            
            with open(filepath, 'r') as f:
                session_data = json.load(f)
            
            simulation = self._deserialize_simulation(session_data)
            return simulation
            
        except Exception as e:
            print(f"error loading session: {e}")
            return None
    
    def list_sessions(self) -> list:
        """list all available saved sessions"""
        sessions = []
        for filepath in self.save_directory.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    sessions.append({
                        'name': filepath.stem,
                        'saved_at': data.get('metadata', {}).get('saved_at', 'unknown'),
                        'patient_count': len(data.get('patients', {}))
                    })
            except Exception:
                continue
        return sessions
    
    def delete_session(self, session_name: str) -> bool:
        """delete a saved session"""
        try:
            filename = f"{session_name}.json"
            filepath = self.save_directory / filename
            
            if filepath.exists():
                filepath.unlink()
                return True
            return False
        except Exception as e:
            print(f"error deleting session: {e}")
            return False
    
    def _serialize_simulation(self, simulation: MedicalSimulation) -> Dict[str, Any]:
        """convert simulation state to serializable format"""
        patients_data = {}
        for patient_id, patient in simulation.patients.items():
            patients_data[patient_id] = {
                'patient_id': patient.patient_id,
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender,
                'vital_signs': patient.vital_signs,
                'symptoms': patient.symptoms,
                'medications': patient.medications,
                'lab_results': patient.lab_results,
                'procedures': patient.procedures,
                'timestamp': patient.timestamp.isoformat()
            }
        
        return {
            'patients': patients_data,
            'current_time': simulation.current_time,
            'is_running': simulation.is_running,
            'events': simulation.events
        }
    
    def _deserialize_simulation(self, session_data: Dict[str, Any]) -> MedicalSimulation:
        """create simulation from serialized data"""
        simulation = MedicalSimulation()
        
        # restore patients
        for patient_id, patient_data in session_data.get('patients', {}).items():
            patient = PatientState(
                patient_id=patient_data['patient_id'],
                name=patient_data['name'],
                age=patient_data['age'],
                gender=patient_data['gender']
            )
            patient.vital_signs = patient_data.get('vital_signs', {})
            patient.symptoms = patient_data.get('symptoms', [])
            patient.medications = patient_data.get('medications', [])
            patient.lab_results = patient_data.get('lab_results', {})
            patient.procedures = patient_data.get('procedures', [])
            patient.timestamp = datetime.fromisoformat(patient_data['timestamp'])
            
            simulation.patients[patient_id] = patient
        
        # restore simulation state
        simulation.current_time = session_data.get('current_time', 0)
        simulation.is_running = session_data.get('is_running', False)
        simulation.events = session_data.get('events', [])
        
        return simulation 