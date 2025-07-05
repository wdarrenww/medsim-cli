#!/usr/bin/env python3
"""
example usage of the medical simulator
"""

from medsim.core.simulation import MedicalSimulation, PatientState

def main():
    """demonstrate the medical simulator functionality"""
    
    # create a new simulation
    sim = MedicalSimulation()
    
    # add a patient
    patient = sim.add_patient("P001", "John Smith", 58, "Male")
    
    # start the simulation
    sim.start_simulation()
    
    print("=== Medical Simulator Example ===")
    print(f"Patient: {patient.name} (ID: {patient.patient_id})")
    print(f"Age: {patient.age}, Gender: {patient.gender}")
    print()
    
    # update patient vital signs
    vitals = {
        'bp_systolic': 140,
        'bp_diastolic': 90,
        'heart_rate': 85,
        'respiratory_rate': 18,
        'temperature': 98.6,
        'oxygen_saturation': 98
    }
    patient.update_vital_signs(vitals)
    
    print("=== Vital Signs ===")
    for key, value in patient.vital_signs.items():
        print(f"{key}: {value}")
    print()
    
    # add symptoms
    patient.add_symptom("chest pain")
    patient.add_symptom("shortness of breath")
    
    print("=== Symptoms ===")
    for symptom in patient.symptoms:
        print(f"- {symptom}")
    print()
    
    # add medications
    patient.add_medication("aspirin")
    patient.add_medication("nitroglycerin")
    
    print("=== Medications ===")
    for medication in patient.medications:
        print(f"- {medication}")
    print()
    
    # schedule some events
    sim.schedule_event(5.0, 'vital_signs_change', {
        'patient_id': 'P001',
        'vital_signs': {'heart_rate': 95}
    })
    
    sim.schedule_event(10.0, 'symptom_onset', {
        'patient_id': 'P001',
        'symptom': 'nausea'
    })
    
    # step through simulation
    print("=== Simulation Steps ===")
    for i in range(3):
        sim.step_simulation(5.0)
        state = sim.get_simulation_state()
        print(f"Time: {state['current_time']:.1f} minutes")
        print(f"Pending events: {state['pending_events']}")
        print()
    
    # show final patient state
    print("=== Final Patient State ===")
    print(f"Vital Signs: {patient.vital_signs}")
    print(f"Symptoms: {patient.symptoms}")
    print(f"Medications: {patient.medications}")
    print()
    
    print("=== Simulation Complete ===")

if __name__ == "__main__":
    main() 