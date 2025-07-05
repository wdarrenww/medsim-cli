"""
session management for saving and loading simulation states
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from .simulation import MedicalSimulation, PatientState


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