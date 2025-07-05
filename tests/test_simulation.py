"""
unit tests for simulation engine
"""

import pytest
from medsim.core.simulation import MedicalSimulation, PatientState


class TestPatientState:
    """test patient state functionality"""
    
    def test_patient_creation(self):
        """test creating a new patient"""
        patient = PatientState(
            patient_id="P001",
            name="John Smith",
            age=58,
            gender="Male"
        )
        
        assert patient.patient_id == "P001"
        assert patient.name == "John Smith"
        assert patient.age == 58
        assert patient.gender == "Male"
        assert len(patient.vital_signs) == 0
        assert len(patient.symptoms) == 0
        assert len(patient.medications) == 0
    
    def test_update_vital_signs(self):
        """test updating patient vital signs"""
        patient = PatientState("P001", "John Smith", 58, "Male")
        
        vitals = {
            'bp_systolic': 140,
            'bp_diastolic': 90,
            'heart_rate': 80
        }
        
        patient.update_vital_signs(vitals)
        
        assert patient.vital_signs['bp_systolic'] == 140
        assert patient.vital_signs['bp_diastolic'] == 90
        assert patient.vital_signs['heart_rate'] == 80
    
    def test_add_symptom(self):
        """test adding symptoms to patient"""
        patient = PatientState("P001", "John Smith", 58, "Male")
        
        patient.add_symptom("chest pain")
        patient.add_symptom("shortness of breath")
        
        assert "chest pain" in patient.symptoms
        assert "shortness of breath" in patient.symptoms
        assert len(patient.symptoms) == 2
    
    def test_add_medication(self):
        """test adding medications to patient"""
        patient = PatientState("P001", "John Smith", 58, "Male")
        
        patient.add_medication("aspirin")
        patient.add_medication("nitroglycerin")
        
        assert "aspirin" in patient.medications
        assert "nitroglycerin" in patient.medications
        assert len(patient.medications) == 2
    
    def test_add_lab_result(self):
        """test adding lab results to patient"""
        patient = PatientState("P001", "John Smith", 58, "Male")
        
        patient.add_lab_result("troponin", 0.5)
        patient.add_lab_result("ck-mb", 25)
        
        assert patient.lab_results["troponin"] == 0.5
        assert patient.lab_results["ck-mb"] == 25
    
    def test_add_procedure(self):
        """test adding procedures to patient"""
        patient = PatientState("P001", "John Smith", 58, "Male")
        
        patient.add_procedure("ecg")
        patient.add_procedure("chest x-ray")
        
        assert "ecg" in patient.procedures
        assert "chest x-ray" in patient.procedures
        assert len(patient.procedures) == 2


class TestMedicalSimulation:
    """test medical simulation engine"""
    
    def test_simulation_creation(self):
        """test creating a new simulation"""
        sim = MedicalSimulation()
        
        assert len(sim.patients) == 0
        assert sim.current_time == 0
        assert len(sim.events) == 0
        assert not sim.is_running
    
    def test_add_patient(self):
        """test adding a patient to simulation"""
        sim = MedicalSimulation()
        
        patient = sim.add_patient("P001", "John Smith", 58, "Male")
        
        assert patient.patient_id == "P001"
        assert patient.name == "John Smith"
        assert len(sim.patients) == 1
        assert "P001" in sim.patients
    
    def test_get_patient(self):
        """test retrieving a patient from simulation"""
        sim = MedicalSimulation()
        sim.add_patient("P001", "John Smith", 58, "Male")
        
        patient = sim.get_patient("P001")
        
        assert patient is not None
        assert patient.name == "John Smith"
        
        # test getting non-existent patient
        patient = sim.get_patient("P999")
        assert patient is None
    
    def test_schedule_event(self):
        """test scheduling events in simulation"""
        sim = MedicalSimulation()
        sim.add_patient("P001", "John Smith", 58, "Male")
        
        event_data = {
            'patient_id': 'P001',
            'vital_signs': {'heart_rate': 100}
        }
        
        sim.schedule_event(5.0, 'vital_signs_change', event_data)
        
        assert len(sim.events) == 1
        assert sim.events[0]['type'] == 'vital_signs_change'
        assert sim.events[0]['data'] == event_data
    
    def test_simulation_control(self):
        """test simulation start/pause/reset"""
        sim = MedicalSimulation()
        
        # test start
        sim.start_simulation()
        assert sim.is_running
        
        # test pause
        sim.pause_simulation()
        assert not sim.is_running
        
        # test reset
        sim.reset_simulation()
        assert not sim.is_running
        assert sim.current_time == 0
        assert len(sim.events) == 0
    
    def test_step_simulation(self):
        """test advancing simulation by time steps"""
        sim = MedicalSimulation()
        sim.start_simulation()

        initial_time = sim.current_time
        sim.step_simulation()
        assert sim.current_time == initial_time + 1
    
    def test_get_simulation_state(self):
        """test getting simulation state"""
        sim = MedicalSimulation()
        sim.add_patient("P001", "John Smith", 58, "Male")
        sim.start_simulation()
        
        state = sim.get_simulation_state()
        
        assert 'current_time' in state
        assert 'is_running' in state
        assert 'patient_count' in state
        assert 'pending_events' in state
        assert state['patient_count'] == 1
        assert state['is_running'] is True 