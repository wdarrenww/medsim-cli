#!/usr/bin/env python3
"""
comprehensive example demonstrating realistic information discovery in medical simulation

this example shows how the enhanced system makes information discovery more realistic:
- patient information is hidden until discovered through appropriate methods
- symptoms progress over time and must be discovered through examination
- bmi and other calculated values must be explicitly calculated
- lab and imaging results are only available after being ordered
- physical exam findings are only known after performing the exam
"""

import sys
import os
from datetime import datetime, timedelta
import time
import json

# add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from medsim.core.physiology import EnhancedPhysiologicalEngine, DiscoveryMethod
from medsim.core.symptoms import ComprehensiveSymptomLibrary
from medsim.core.diagnostics import ComprehensiveLabLibrary, ComprehensiveImagingLibrary
from medsim.core.treatments import TreatmentEngine
from medsim.core.dialogue import DialogueSystem
from medsim.core.session import SimulationSession

def print_section(title: str):
    """print a section header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_subsection(title: str):
    """print a subsection header"""
    print(f"\n{'-'*40}")
    print(f" {title}")
    print(f"{'-'*40}")

def main():
    """demonstrate realistic information discovery"""
    print_section("REALISTIC INFORMATION DISCOVERY DEMONSTRATION")
    
    # initialize systems
    physiology_engine = EnhancedPhysiologicalEngine()
    symptom_library = ComprehensiveSymptomLibrary()
    lab_library = ComprehensiveLabLibrary()
    imaging_library = ComprehensiveImagingLibrary()
    treatment_engine = TreatmentEngine()
    dialogue_system = DialogueSystem()
    session = SimulationSession()
    
    print_subsection("1. Creating a Patient")
    
    # create a patient - basic info is available immediately
    patient_id = "P001"
    result = physiology_engine.create_patient(
        patient_id, "Sarah Johnson", 45, "female", 165.0, 70.0
    )
    print(f"✓ {result}")
    
    # show initial patient summary - notice no discovered information yet
    summary = physiology_engine.get_patient_summary(patient_id, include_undiscovered=True)
    print(f"\nPatient: {summary['name']}")
    print(f"Age: {summary['age']}, Gender: {summary['gender']}")
    print(f"Height: {summary['height_cm']} cm, Weight: {summary['weight_kg']} kg")
    print(f"Discovered Information: {len(summary['discovered_info'])} items")
    
    if 'undiscovered_info' in summary:
        print("Undiscovered Information:")
        for info_type in summary['undiscovered_info']:
            print(f"  • {info_type.replace('_', ' ').title()}")
    
    print_subsection("2. Discovering Basic Patient Information")
    
    # discover medical history through patient interview
    medical_history = ["hypertension", "diabetes type 2", "hyperlipidemia"]
    result = physiology_engine.discover_patient_information(
        patient_id, "medical_history", DiscoveryMethod.PATIENT_REPORTED, medical_history
    )
    print(f"✓ {result}")
    
    # discover medications through patient interview
    medications = ["metformin 500mg twice daily", "lisinopril 10mg daily", "atorvastatin 20mg daily"]
    result = physiology_engine.discover_patient_information(
        patient_id, "medications", DiscoveryMethod.PATIENT_REPORTED, medications
    )
    print(f"✓ {result}")
    
    # discover allergies through patient interview
    allergies = ["penicillin", "sulfa drugs"]
    result = physiology_engine.discover_patient_information(
        patient_id, "allergies", DiscoveryMethod.PATIENT_REPORTED, allergies
    )
    print(f"✓ {result}")
    
    print_subsection("3. Calculating Patient Metrics")
    
    # calculate and discover BMI
    result = physiology_engine.discover_patient_information(
        patient_id, "bmi", DiscoveryMethod.CALCULATION
    )
    print(f"✓ {result}")
    
    # calculate and discover body surface area
    result = physiology_engine.discover_patient_information(
        patient_id, "body_surface_area", DiscoveryMethod.CALCULATION
    )
    print(f"✓ {result}")
    
    # calculate and discover ideal body weight
    result = physiology_engine.discover_patient_information(
        patient_id, "ideal_body_weight", DiscoveryMethod.CALCULATION
    )
    print(f"✓ {result}")
    
    print_subsection("4. Adding Symptom Progressions")
    
    # add symptom progressions for the patient
    symptoms_to_add = ["chest_pain", "shortness_of_breath", "palpitations"]
    
    for symptom in symptoms_to_add:
        result = symptom_library.add_symptom_progression(symptom, patient_id)
        print(f"✓ {result}")
    
    print_subsection("5. Discovering Symptoms Through Different Methods")
    
    # discover chest pain through patient report
    result = symptom_library.discover_symptom(
        "chest_pain", patient_id, symptom_library.DiscoveryMethod.PATIENT_REPORTED
    )
    print(f"✓ {result}")
    
    # discover shortness of breath through observation
    result = symptom_library.discover_symptom(
        "shortness_of_breath", patient_id, symptom_library.DiscoveryMethod.OBSERVATION
    )
    print(f"✓ {result}")
    
    # discover palpitations through vital signs
    result = symptom_library.discover_symptom(
        "palpitations", patient_id, symptom_library.DiscoveryMethod.VITAL_SIGNS
    )
    print(f"✓ {result}")
    
    print_subsection("6. Updating Symptom Progressions")
    
    # update symptoms to show progression over time
    print("Updating symptom progressions...")
    updates = symptom_library.update_symptom_progressions()
    for update in updates:
        print(f"  {update}")
    
    print_subsection("7. Showing Discovered vs Undiscovered Information")
    
    # show discovered symptoms
    discovered_symptoms = symptom_library.get_discovered_symptoms(patient_id)
    print(f"Discovered Symptoms ({len(discovered_symptoms)}):")
    for symptom in discovered_symptoms:
        print(f"  • {symptom['name']} ({symptom['severity']}) - via {', '.join(symptom['discovery_methods'])}")
    
    # show undiscovered symptoms
    undiscovered_symptoms = symptom_library.get_undiscovered_symptoms(patient_id)
    print(f"\nUndiscovered Symptoms ({len(undiscovered_symptoms)}):")
    for symptom in undiscovered_symptoms:
        print(f"  • {symptom['name']} (difficulty: {symptom['discovery_difficulty']:.2f})")
    
    print_subsection("8. Physical Examination Findings")
    
    # discover physical exam findings
    physical_exam = {
        "chest_tenderness": "mild tenderness on palpation",
        "heart_sounds": "normal S1, S2, no murmurs",
        "lung_sounds": "clear bilaterally",
        "pulses": "2+ radial and pedal pulses"
    }
    
    result = physiology_engine.discover_patient_information(
        patient_id, "physical_exam", DiscoveryMethod.PHYSICAL_EXAM, physical_exam
    )
    print(f"✓ {result}")
    
    print_subsection("9. Ordering and Receiving Lab Results")
    
    # order lab tests
    lab_results = {
        "troponin": {"value": 0.02, "unit": "ng/mL", "normal_range": "0.00-0.04"},
        "ck_mb": {"value": 2.1, "unit": "ng/mL", "normal_range": "0.0-5.0"},
        "bnp": {"value": 150, "unit": "pg/mL", "normal_range": "0-100"},
        "cbc": {"value": {"wbc": 8.2, "hgb": 13.5, "plt": 250}, "unit": "K/uL", "normal_range": "4.5-11.0"}
    }
    
    result = physiology_engine.discover_patient_information(
        patient_id, "lab_results", DiscoveryMethod.LAB_RESULTS, lab_results
    )
    print(f"✓ {result}")
    
    print_subsection("10. Ordering and Receiving Imaging Results")
    
    # order imaging studies
    imaging_results = {
        "chest_xray": {"finding": "normal cardiac silhouette, clear lung fields", "impression": "normal"},
        "ecg": {"finding": "normal sinus rhythm, no ST changes", "impression": "normal"},
        "echo": {"finding": "normal ejection fraction 65%, no wall motion abnormalities", "impression": "normal"}
    }
    
    result = physiology_engine.discover_patient_information(
        patient_id, "imaging_results", DiscoveryMethod.IMAGING, imaging_results
    )
    print(f"✓ {result}")
    
    print_subsection("11. Comprehensive Patient Summary")
    
    # show final patient summary with all discovered information
    summary = physiology_engine.get_patient_summary(patient_id, include_undiscovered=True)
    
    print(f"Patient: {summary['name']}")
    print(f"Age: {summary['age']}, Gender: {summary['gender']}")
    print(f"Height: {summary['height_cm']} cm, Weight: {summary['weight_kg']} kg")
    
    print(f"\nVital Signs:")
    for key, value in summary['vitals'].items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print(f"\nSymptoms: {', '.join(summary['symptoms']) if summary['symptoms'] else 'None'}")
    
    print(f"\nDiscovered Information ({len(summary['discovered_info'])} items):")
    for info_type, info in summary['discovered_info'].items():
        print(f"  • {info_type.replace('_', ' ').title()}: {info['value']}")
    
    if 'undiscovered_info' in summary and summary['undiscovered_info']:
        print(f"\nUndiscovered Information:")
        for info_type in summary['undiscovered_info']:
            print(f"  • {info_type.replace('_', ' ').title()}")
    
    print_subsection("12. Discovery History")
    
    # show discovery history
    history = physiology_engine.get_discovery_history(patient_id)
    print(f"Discovery History ({len(history)} entries):")
    for entry in history:
        timestamp = entry['timestamp'].strftime("%H:%M:%S")
        success = "✓" if entry['success'] else "✗"
        print(f"  {timestamp} - {entry['info_type'].replace('_', ' ').title()} via {entry['method']} {success}")
    
    print_subsection("13. Realistic Clinical Scenario")
    
    print("""
Realistic Clinical Scenario:
The doctor doesn't know everything about the patient immediately.
Information must be discovered through:
• Patient interview (medical history, medications, allergies)
• Physical examination (findings, vital signs)
• Laboratory testing (results only after ordering)
• Imaging studies (results only after ordering)
• Calculation (BMI, BSA, IBW must be calculated)
• Observation (symptoms that are visible)

This creates a more realistic simulation where the doctor must:
1. Take a thorough history
2. Perform a complete physical examination
3. Order appropriate diagnostic tests
4. Interpret results as they become available
5. Make clinical decisions based on discovered information
""")
    
    print_subsection("14. Symptom Progression Over Time")
    
    # demonstrate symptom progression
    print("Simulating symptom progression over time...")
    
    for i in range(3):
        print(f"\nTime step {i+1}:")
        updates = symptom_library.update_symptom_progressions()
        if updates:
            for update in updates:
                print(f"  {update}")
        else:
            print("  No symptom changes")
        
        # show current symptom status
        discovered = symptom_library.get_discovered_symptoms(patient_id)
        for symptom in discovered:
            print(f"  {symptom['name']}: {symptom['severity']}")
    
    print_section("DEMONSTRATION COMPLETE")
    
    print("""
Key Features Demonstrated:
✓ Realistic information discovery through appropriate methods
✓ Progressive symptom development over time
✓ Hidden information until discovered
✓ Calculated values must be explicitly calculated
✓ Lab and imaging results only available after ordering
✓ Physical exam findings only known after examination
✓ Discovery history tracking
✓ Confidence levels in discovered information
✓ Difficulty levels for symptom discovery
✓ Temporal progression of symptoms

This enhanced system provides a much more realistic medical simulation
where the doctor must actively discover information rather than having
omniscient knowledge of the patient's condition.
""")

if __name__ == "__main__":
    main() 