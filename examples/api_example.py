#!/usr/bin/env python3
"""
Medical Simulator API Example
demonstrates programmatic access to simulator functionality
"""

import json
from datetime import datetime
from medsim.api import MedicalSimulatorAPI

def main():
    """demonstrate API functionality"""
    print("Medical Simulator API Example")
    print("=" * 40)
    
    # initialize API
    api = MedicalSimulatorAPI()
    
    # start simulation
    print("\n1. Starting simulation...")
    response = api.start_simulation()
    if response.success:
        print(f"✓ Simulation started: {response.data['session_id']}")
    else:
        print(f"✗ Failed to start simulation: {response.error}")
        return
    
    # get initial state
    print("\n2. Getting simulation state...")
    state_response = api.get_simulation_state()
    if state_response.success:
        state = state_response.data
        print(f"✓ Patient: {state.patient.name} ({state.patient.age} years old)")
        print(f"✓ Vitals: BP {state.vitals.blood_pressure_systolic}/{state.vitals.blood_pressure_diastolic}, HR {state.vitals.heart_rate}")
    else:
        print(f"✗ Failed to get state: {state_response.error}")
    
    # order lab tests
    print("\n3. Ordering lab tests...")
    lab_tests = ["troponin", "glucose", "potassium"]
    for test in lab_tests:
        response = api.order_lab_test(test)
        if response.success:
            print(f"✓ Ordered {test}")
        else:
            print(f"✗ Failed to order {test}: {response.error}")
    
    # order imaging
    print("\n4. Ordering imaging studies...")
    imaging_studies = ["chest_xray", "ecg"]
    for study in imaging_studies:
        response = api.order_imaging_study(study)
        if response.success:
            print(f"✓ Ordered {study}")
        else:
            print(f"✗ Failed to order {study}: {response.error}")
    
    # advance simulation to get results
    print("\n5. Advancing simulation...")
    response = api.step_simulation(10)
    if response.success:
        print(f"✓ Advanced simulation by {response.data['steps_completed']} steps")
    else:
        print(f"✗ Failed to advance simulation: {response.error}")
    
    # get updated state with results
    print("\n6. Getting updated state...")
    state_response = api.get_simulation_state()
    if state_response.success:
        state = state_response.data
        print(f"✓ Lab results: {len(state.lab_results)} tests")
        print(f"✓ Imaging results: {len(state.imaging_results)} studies")
        
        # show some results
        for lab in state.lab_results[:3]:  # show first 3 lab results
            print(f"  • {lab.test_name}: {lab.value} {lab.unit} ({lab.status})")
        
        for imaging in state.imaging_results[:2]:  # show first 2 imaging results
            print(f"  • {imaging.study_name}: {imaging.clinical_impression}")
    else:
        print(f"✗ Failed to get updated state: {state_response.error}")
    
    # administer medication
    print("\n7. Administering medication...")
    medication_data = {
        "name": "Aspirin",
        "dose": "325mg",
        "route": "oral"
    }
    response = api.administer_medication(medication_data)
    if response.success:
        print(f"✓ Administered {medication_data['name']}")
    else:
        print(f"✗ Failed to administer medication: {response.error}")
    
    # perform procedure
    print("\n8. Performing procedure...")
    procedure_data = {
        "name": "Intubation",
        "parameters": {
            "tube_size": "7.5",
            "depth": "23cm"
        }
    }
    response = api.perform_procedure(procedure_data)
    if response.success:
        print(f"✓ Performed {procedure_data['name']}")
    else:
        print(f"✗ Failed to perform procedure: {response.error}")
    
    # start dialogue
    print("\n9. Starting patient dialogue...")
    response = api.start_dialogue("How are you feeling?")
    if response.success:
        print(f"✓ Patient response: {response.data['response']}")
    else:
        print(f"✗ Failed to start dialogue: {response.error}")
    
    # get assessment
    print("\n10. Getting assessment...")
    response = api.get_assessment()
    if response.success:
        assessment = response.data
        print(f"✓ Actions performed: {len(assessment.actions)}")
        print(f"✓ Score: {assessment.score}")
        print(f"✓ Passed: {assessment.passed}")
    else:
        print(f"✗ Failed to get assessment: {response.error}")
    
    # get plugin information
    print("\n11. Getting plugin information...")
    response = api.get_plugins()
    if response.success:
        plugins = response.data
        print(f"✓ Loaded plugins: {len(plugins)}")
        for plugin in plugins:
            print(f"  • {plugin['name']} v{plugin['version']} ({plugin['category']})")
    else:
        print(f"✗ Failed to get plugins: {response.error}")
    
    # save session
    print("\n12. Saving session...")
    filename = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    response = api.save_session(filename)
    if response.success:
        print(f"✓ Session saved to {filename}")
    else:
        print(f"✗ Failed to save session: {response.error}")
    
    # stop simulation
    print("\n13. Stopping simulation...")
    response = api.stop_simulation()
    if response.success:
        print("✓ Simulation stopped")
    else:
        print(f"✗ Failed to stop simulation: {response.error}")
    
    print("\n" + "=" * 40)
    print("API Example completed successfully!")

if __name__ == "__main__":
    main() 