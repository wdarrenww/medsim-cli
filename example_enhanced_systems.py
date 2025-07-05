#!/usr/bin/env python3
"""
comprehensive example demonstrating enhanced medical simulation systems
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from medsim.core.physiology import EnhancedPhysiologicalEngine, DiscoveryMethod, OrganSystem, DiseaseState
from medsim.core.diagnostics import EnhancedDiagnosticSystem, TestCategory, ImagingModality
from medsim.core.treatments import EnhancedTreatmentEngine, DrugCategory, Route, InteractionSeverity
from medsim.core.dialogue import EnhancedDialogueEngine, EmotionalState, CommunicationStyle, PainLevel
from medsim.core.symptoms import SymptomLibrary
from datetime import datetime, timedelta
import json


def main():
    """demonstrate enhanced medical simulation systems"""
    print("🏥 Enhanced Medical Simulation - Comprehensive Example")
    print("=" * 60)
    
    # initialize all engines
    print("\n📋 Initializing simulation engines...")
    physio_engine = EnhancedPhysiologicalEngine()
    diagnostic_engine = EnhancedDiagnosticSystem()
    treatment_engine = EnhancedTreatmentEngine()
    dialogue_engine = EnhancedDialogueEngine()
    symptom_library = SymptomLibrary()
    
    # create a patient
    print("\n👤 Creating patient profile...")
    patient_id = "P001"
    result = physio_engine.create_patient(
        patient_id=patient_id,
        name="Sarah Johnson",
        age=58,
        gender="female",
        height_cm=165,
        weight_kg=75
    )
    print(f"✓ {result}")
    
    # initialize dialogue context
    dialogue_engine.initialize_patient_context(
        patient_id, 
        emotional_state=EmotionalState.ANXIOUS,
        communication_style=CommunicationStyle.DETAILED
    )
    
    # discover patient information
    print("\n🔍 Discovering patient information...")
    
    # discover BMI
    result = physio_engine.discover_patient_information(
        patient_id, "bmi", DiscoveryMethod.CALCULATION
    )
    print(f"✓ {result}")
    
    # discover medical history
    medical_history = ["hypertension", "diabetes type 2", "hyperlipidemia"]
    result = physio_engine.discover_patient_information(
        patient_id, "medical_history", DiscoveryMethod.MEDICAL_HISTORY, medical_history
    )
    print(f"✓ {result}")
    
    # discover medications
    medications = ["metoprolol 25mg twice daily", "metformin 500mg twice daily", "atorvastatin 20mg daily"]
    result = physio_engine.discover_patient_information(
        patient_id, "medications", DiscoveryMethod.MEDICAL_HISTORY, medications
    )
    print(f"✓ {result}")
    
    # update vitals with concerning values
    print("\n💓 Updating vital signs...")
    vitals = {
        'heart_rate': 110,
        'systolic_bp': 160,
        'diastolic_bp': 95,
        'respiratory_rate': 22,
        'temperature': 37.8,
        'oxygen_saturation': 94,
        'blood_glucose': 180,
        'creatinine': 1.4,
        'sodium': 142,
        'potassium': 4.2
    }
    result = physio_engine.update_patient_vitals(patient_id, vitals)
    print(f"✓ {result}")
    
    # add symptoms
    print("\n🤒 Adding symptoms...")
    symptoms = ["chest pain", "shortness of breath", "fatigue", "nausea"]
    for symptom in symptoms:
        result = physio_engine.add_patient_symptom(patient_id, symptom)
        print(f"✓ {result}")
    
    # add disease processes
    print("\n🦠 Adding disease processes...")
    result = physio_engine.add_patient_disease(
        patient_id, "acute coronary syndrome", OrganSystem.CARDIOVASCULAR, 0.7
    )
    print(f"✓ {result}")
    
    result = physio_engine.add_patient_disease(
        patient_id, "diabetic ketoacidosis", OrganSystem.ENDOCRINE, 0.6
    )
    print(f"✓ {result}")
    
    # order diagnostic tests
    print("\n🔬 Ordering diagnostic tests...")
    
    # order lab tests
    lab_tests = ["cbc", "creatinine", "glucose", "troponin", "bnp"]
    for test in lab_tests:
        result = diagnostic_engine.order_lab_test(patient_id, test)
        print(f"✓ {result}")
    
    # order imaging studies
    imaging_studies = ["chest_xray", "ecg", "echo"]
    for study in imaging_studies:
        result = diagnostic_engine.order_imaging_study(patient_id, study)
        print(f"✓ {result}")
    
    # complete lab tests with results
    print("\n📊 Completing lab tests...")
    lab_results = {
        "cbc": 12.5,  # elevated WBC
        "creatinine": 1.8,  # elevated
        "glucose": 320,  # very elevated
        "troponin": 0.15,  # elevated
        "bnp": 450  # elevated
    }
    
    for test_name, value in lab_results.items():
        result = diagnostic_engine.complete_lab_test(patient_id, test_name, value)
        print(f"✓ Completed {test_name}: {value}")
        if result.requires_action:
            print(f"⚠️ ACTION REQUIRED: {result.interpretation}")
    
    # complete imaging studies
    print("\n🖼️ Completing imaging studies...")
    
    # chest x-ray findings
    chest_findings = {
        "impression": "abnormal",
        "findings": {
            "cardiomegaly": "moderate",
            "pulmonary_edema": "mild",
            "pleural_effusion": "none"
        }
    }
    result = diagnostic_engine.complete_imaging_study(patient_id, "chest_xray", chest_findings)
    print(f"✓ Chest X-ray: {result.impression}")
    
    # ECG findings
    ecg_findings = {
        "impression": "abnormal",
        "findings": {
            "st_elevation": "anterior leads",
            "q_waves": "present",
            "t_wave_inversion": "diffuse"
        }
    }
    result = diagnostic_engine.complete_imaging_study(patient_id, "ecg", ecg_findings)
    print(f"✓ ECG: {result.impression}")
    
    # administer treatments
    print("\n💊 Administering treatments...")
    
    # start chest pain protocol
    result = treatment_engine.start_treatment_protocol(patient_id, "chest_pain")
    print(f"✓ {result}")
    
    # administer medications
    medications = [
        ("aspirin", 325, "oral"),
        ("nitroglycerin", 0.4, "sublingual"),
        ("morphine", 4, "iv"),
        ("heparin", 5000, "iv")
    ]
    
    for drug_name, dose, route in medications:
        result = treatment_engine.administer_drug(patient_id, drug_name, dose, route)
        print(f"✓ {result}")
    
    # patient communication
    print("\n💬 Patient communication...")
    
    # initial assessment
    response = dialogue_engine.get_patient_response(
        patient_id, 
        "Hello Mrs. Johnson, I'm Dr. Smith. How are you feeling today?",
        "emotional_assessment"
    )
    print(f"Patient: {response.text}")
    print(f"Emotion: {response.emotion.value}")
    
    # pain assessment
    response = dialogue_engine.get_patient_response(
        patient_id,
        "Can you tell me about your chest pain? When did it start?",
        "symptom_inquiry"
    )
    print(f"Patient: {response.text}")
    
    # treatment discussion
    response = dialogue_engine.get_patient_response(
        patient_id,
        "I'm going to start some medications to help with your chest pain and blood sugar.",
        "treatment_discussion"
    )
    print(f"Patient: {response.text}")
    
    # update simulation
    print("\n⏰ Updating simulation...")
    physio_updates = physio_engine.update_all_patients()
    drug_updates = treatment_engine.update_drug_levels(patient_id)
    disease_updates = physio_engine.update_patient_diseases(patient_id)
    
    all_updates = physio_updates + drug_updates + disease_updates
    if all_updates:
        print("Simulation updates:")
        for update in all_updates:
            print(f"• {update}")
    
    # show comprehensive summary
    print("\n📋 Patient Summary:")
    summary = physio_engine.get_patient_summary(patient_id)
    
    print(f"Patient: {summary['name']} (ID: {summary['patient_id']})")
    print(f"Age: {summary['age']} | Gender: {summary['gender']}")
    print(f"Height: {summary['height_cm']}cm | Weight: {summary['weight_kg']}kg")
    print(f"Symptoms: {', '.join(summary['symptoms'])}")
    print(f"Active Diseases: {', '.join(summary['active_diseases'])}")
    print(f"Treatments: {summary['treatments']}")
    print(f"Assessment Notes: {summary['assessment_notes']}")
    print(f"Stress Level: {summary['stress_level']:.2f}")
    print(f"Pain Level: {summary['pain_level']:.1f}")
    print(f"Consciousness: {summary['consciousness_level']}")
    print(f"Mobility: {summary['mobility_status']}")
    
    # show critical vitals
    critical_vitals = summary['critical_vitals']
    if critical_vitals:
        print(f"\n⚠️ Critical Vitals:")
        for vital in critical_vitals:
            print(f"• {vital['name']}: {vital['value']} {vital['unit']} ({vital['alert_level']})")
    
    # show discovered information
    discovered_info = summary['discovered_info']
    if discovered_info:
        print(f"\n🔍 Discovered Information:")
        for info_type, info in discovered_info.items():
            print(f"• {info_type}: {info['value']} (via {info['discovery_method']})")
    
    # show lab results
    lab_results = diagnostic_engine.get_lab_results(patient_id)
    if lab_results:
        print(f"\n🔬 Lab Results:")
        for result in lab_results:
            status = "⚠️" if result.is_abnormal else "✓"
            print(f"{status} {result.test_name}: {result.value} {result.unit} ({result.interpretation})")
    
    # show imaging results
    imaging_results = diagnostic_engine.get_imaging_results(patient_id)
    if imaging_results:
        print(f"\n🖼️ Imaging Results:")
        for result in imaging_results:
            print(f"• {result.study_name}: {result.impression}")
            if result.recommendations:
                print(f"  Recommendations: {', '.join(result.recommendations)}")
    
    # show active treatments
    active_treatments = treatment_engine.get_active_treatments(patient_id)
    if active_treatments:
        print(f"\n💊 Active Treatments:")
        for treatment in active_treatments:
            print(f"• {treatment['drug_name']} {treatment['dose']} via {treatment['route']}")
            if treatment['interactions']:
                print(f"  ⚠️ Drug interactions detected")
    
    # show drug levels
    drug_levels = treatment_engine.get_drug_levels(patient_id)
    if drug_levels:
        print(f"\n📊 Drug Levels:")
        for level in drug_levels:
            status = "⚠️" if level.is_toxic or not level.is_therapeutic else "✓"
            print(f"{status} {level.drug_name}: {level.current_level:.2f} {level.unit}")
    
    # show emotional summary
    emotional_summary = dialogue_engine.get_emotional_summary(patient_id)
    print(f"\n😊 Emotional Summary:")
    print(f"Current Emotion: {emotional_summary['current_emotion']}")
    print(f"Emotion Intensity: {emotional_summary['emotion_intensity']:.2f}")
    print(f"Communication Style: {emotional_summary['communication_style']}")
    print(f"Pain Level: {emotional_summary['pain_level']}")
    print(f"Trust Level: {emotional_summary['trust_level']:.2f}")
    print(f"Understanding Level: {emotional_summary['understanding_level']:.2f}")
    
    # show critical alerts
    print(f"\n🚨 Critical Alerts:")
    
    # physiological alerts
    physio_alerts = physio_engine.get_critical_alerts()
    if physio_alerts:
        print("Physiological Alerts:")
        for alert in physio_alerts:
            print(f"• {alert['patient_name']}: {alert['vital_name']} = {alert['value']} {alert['unit']}")
    
    # diagnostic alerts
    diagnostic_alerts = diagnostic_engine.get_critical_alerts()
    if diagnostic_alerts:
        print("Laboratory Alerts:")
        for alert in diagnostic_alerts:
            print(f"• {alert['test_name']}: {alert['value']} {alert['unit']} ({alert['critical_level']})")
    
    # treatment alerts
    treatment_alerts = treatment_engine.get_critical_alerts()
    if treatment_alerts:
        print("Treatment Alerts:")
        for alert in treatment_alerts:
            print(f"• {alert['drug_name']}: {alert['level']} {alert['unit']} ({alert['status']})")
    
    # demonstrate library features
    print(f"\n📚 Medical Library Features:")
    
    # search symptoms
    symptoms = symptom_library.search_symptoms("chest")
    print(f"Found {len(symptoms)} symptoms related to 'chest'")
    
    # search drugs
    drugs = treatment_engine.search_drugs("cardio")
    print(f"Found {len(drugs)} cardiovascular drugs")
    
    # search lab tests
    labs = diagnostic_engine.search_lab_tests("cardiac")
    print(f"Found {len(labs)} cardiac lab tests")
    
    # show conversation history
    conversation_history = dialogue_engine.get_conversation_history(patient_id)
    print(f"\n💬 Conversation History ({len(conversation_history)} exchanges):")
    for i, exchange in enumerate(conversation_history[-5:], 1):  # show last 5
        print(f"{i}. {exchange.speaker.title()}: {exchange.message[:50]}...")
    
    print(f"\n✅ Enhanced medical simulation demonstration completed!")
    print("This example showcases:")
    print("• Sophisticated physiological modeling with real-time tracking")
    print("• Comprehensive diagnostic system with lab and imaging")
    print("• Advanced treatment system with drug interactions and protocols")
    print("• Realistic patient communication with emotional modeling")
    print("• Information discovery and clinical decision support")
    print("• Critical alert monitoring and trending")


if __name__ == "__main__":
    main() 