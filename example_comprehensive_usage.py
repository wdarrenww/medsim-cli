#!/usr/bin/env python3
"""
comprehensive example usage of the enhanced medical simulator
demonstrating all features including comprehensive libraries
"""

from medsim.core.simulation import MedicalSimulation, PatientState
from medsim.core.symptoms import ComprehensiveSymptomLibrary, SymptomCategory
from medsim.core.procedures import ComprehensiveProcedureLibrary, ProcedureCategory
from medsim.core.diagnostics import AdvancedDiagnosticSystem
from medsim.core.treatments import AdvancedTreatmentSystem
from medsim.core.dialogue import AdvancedDialogueSystem
from medsim.core.assessment import AdvancedAssessmentSystem
from medsim.core.session import SessionManager
from medsim.scenarios.scenario_manager import ScenarioManager
from medsim.core.monitoring import MonitoringSystem
from medsim.core.pharmacology import PKPDEngine
from medsim.core.physiology import EnhancedPhysiologicalEngine
from medsim.core.session import PatientState
from medsim.cli.interface import SimulatorCLI

import time
import json
from datetime import datetime, timedelta


def demonstrate_comprehensive_libraries():
    """demonstrate the comprehensive libraries"""
    print("\n" + "="*60)
    print("COMPREHENSIVE LIBRARIES DEMONSTRATION")
    print("="*60)
    
    # symptoms library
    print("\n📋 SYMPTOMS LIBRARY")
    print("-" * 30)
    symptoms_lib = ComprehensiveSymptomLibrary()
    
    # search for chest-related symptoms
    chest_symptoms = symptoms_lib.search_symptoms("chest")
    print(f"Found {len(chest_symptoms)} chest-related symptoms:")
    for symptom in chest_symptoms[:5]:
        print(f"  • {symptom.name} ({symptom.severity.value}) - {symptom.description[:60]}...")
    
    # get cardiovascular symptoms
    cv_symptoms = symptoms_lib.get_symptoms_by_category(SymptomCategory.CARDIOVASCULAR)
    print(f"\nFound {len(cv_symptoms)} cardiovascular symptoms")
    
    # get critical symptoms
    critical_symptoms = symptoms_lib.get_critical_symptoms()
    print(f"Found {len(critical_symptoms)} critical symptoms")
    
    # procedures library
    print("\n🔬 PROCEDURES LIBRARY")
    print("-" * 30)
    procedures_lib = ComprehensiveProcedureLibrary()
    
    # search for emergency procedures
    emergency_procedures = procedures_lib.get_procedures_by_category(ProcedureCategory.EMERGENCY)
    print(f"Found {len(emergency_procedures)} emergency procedures:")
    for procedure in emergency_procedures[:3]:
        print(f"  • {procedure.name} ({procedure.complexity.value}) - {procedure.duration_minutes} min")
    
    # get critical procedures
    critical_procedures = procedures_lib.get_critical_procedures()
    print(f"\nFound {len(critical_procedures)} critical procedures")
    
    # diagnostic system
    print("\n🔬 DIAGNOSTIC SYSTEM")
    print("-" * 30)
    diagnostic_system = AdvancedDiagnosticSystem()
    
    # get available lab tests
    lab_tests = diagnostic_system.get_available_lab_tests()
    print(f"Available lab tests: {len(lab_tests)}")
    
    # get available imaging studies
    imaging_studies = diagnostic_system.get_available_imaging_studies()
    print(f"Available imaging studies: {len(imaging_studies)}")
    
    # show some examples
    print("\nLab test examples:")
    for test_id, test in list(lab_tests.items())[:5]:
        print(f"  • {test.name} ({test.category}) - {test.normal_range[0]}-{test.normal_range[1]} {test.unit}")
    
    print("\nImaging study examples:")
    for study_id, study in list(imaging_studies.items())[:5]:
        print(f"  • {study.name} ({study.modality}) - {study.body_part}")


def demonstrate_advanced_simulation():
    """demonstrate advanced simulation features"""
    print("\n" + "="*60)
    print("ADVANCED SIMULATION DEMONSTRATION")
    print("="*60)
    
    # create simulation
    sim = MedicalSimulation()
    
    # add patient
    patient = sim.add_patient("P001", "Sarah Johnson", 45, "Female")
    
    # start simulation
    sim.start_simulation()
    
    print(f"\nPatient: {patient.name} (ID: {patient.patient_id})")
    print(f"Age: {patient.age}, Gender: {patient.gender}")
    
    # demonstrate physiological systems
    print("\n🧬 PHYSIOLOGICAL SYSTEMS")
    print("-" * 30)
    
    # get system status
    system_status = sim.get_system_status()
    print("System status:")
    for system, status in system_status.items():
        if isinstance(status, dict) and 'disease_state' in status:
            print(f"  • {system}: {status['disease_state']}")
    
    # demonstrate drug administration and monitoring
    print("\n💊 DRUG ADMINISTRATION & MONITORING")
    print("-" * 30)
    
    # administer a drug
    result = sim.administer_drug("aspirin", 325, "PO")
    print(f"Drug administration: {result}")
    
    # step simulation
    sim.update_simulation()
    
    # get drug monitoring
    drug_summary = sim.get_drug_monitoring_summary()
    if drug_summary:
        print("Drug monitoring data:")
        for drug, data in drug_summary.items():
            print(f"  • {drug}: {data['current_level']:.2f} mg/L ({data['status']})")
    
    # demonstrate diagnostics
    print("\n🔬 DIAGNOSTICS")
    print("-" * 30)
    
    # order lab tests
    patient_condition = {"age": patient.age, "gender": patient.gender}
    lab_result = sim.diagnostic_system.order_lab_test("troponin", patient_condition)
    print(f"Lab test ordered: {lab_result}")
    
    # order imaging
    imaging_result = sim.diagnostic_system.order_imaging_study("chest_xray", patient_condition)
    print(f"Imaging ordered: {imaging_result}")
    
    # demonstrate dialogue system
    print("\n💬 DIALOGUE SYSTEM")
    print("-" * 30)
    
    dialogue_system = AdvancedDialogueSystem()
    
    # simulate patient interaction
    response = dialogue_system.generate_response(
        "How are you feeling today?",
        patient_state=patient,
        context="initial_assessment"
    )
    print(f"Patient response: {response}")
    
    # demonstrate assessment system
    print("\n📊 ASSESSMENT SYSTEM")
    print("-" * 30)
    
    assessment_system = AdvancedAssessmentSystem()
    
    # record some actions
    assessment_system.record_action("ordered_troponin", "lab_test", 10)
    assessment_system.record_action("ordered_chest_xray", "imaging", 15)
    assessment_system.record_action("administered_aspirin", "medication", 5)
    
    # get assessment
    assessment = assessment_system.get_assessment()
    print(f"Assessment score: {assessment['total_score']}/{assessment['max_score']}")
    print(f"Actions taken: {len(assessment['actions'])}")
    print(f"Time efficiency: {assessment['time_efficiency']:.1%}")


def demonstrate_cli_features():
    """demonstrate CLI features"""
    print("\n" + "="*60)
    print("CLI FEATURES DEMONSTRATION")
    print("="*60)
    
    # create CLI instance
    cli = SimulatorCLI()
    
    print("\nAvailable CLI commands:")
    print("  • symptoms_library - Access comprehensive symptoms library")
    print("  • procedures_library - Access comprehensive procedures library")
    print("  • labs_library - Access comprehensive lab tests library")
    print("  • imaging_library - Access comprehensive imaging studies library")
    print("  • monitor - Real-time monitoring dashboard")
    print("  • trends - Parameter trending analysis")
    print("  • drugs_monitor - Drug level monitoring")
    print("  • alerts_manage - Clinical alert management")
    
    print("\nExample CLI usage:")
    print("  python -m medsim symptoms_library cardiovascular")
    print("  python -m medsim procedures_library emergency")
    print("  python -m medsim labs_library cardiac")
    print("  python -m medsim imaging_library CT")


def demonstrate_scenario_management():
    """demonstrate scenario management"""
    print("\n" + "="*60)
    print("SCENARIO MANAGEMENT DEMONSTRATION")
    print("="*60)
    
    scenario_manager = ScenarioManager()
    
    # get available scenarios
    scenarios = scenario_manager.get_available_scenarios()
    print(f"Available scenarios: {len(scenarios)}")
    
    for scenario_id, scenario in scenarios.items():
        print(f"\nScenario: {scenario.name}")
        print(f"  Difficulty: {scenario.difficulty}")
        print(f"  Time limit: {scenario.time_limit} minutes")
        print(f"  Points possible: {scenario.points_possible}")
        print(f"  Correct diagnosis: {scenario.correct_diagnosis}")
        print(f"  Optimal actions: {len(scenario.optimal_actions)}")


def demonstrate_monitoring_and_trends():
    """demonstrate monitoring and trending features"""
    print("\n" + "="*60)
    print("MONITORING & TRENDING DEMONSTRATION")
    print("="*60)
    
    # create simulation
    sim = MedicalSimulation()
    sim.start_simulation()
    
    # add some monitoring data
    monitoring_system = sim.monitoring_system
    
    # simulate some parameter changes
    for i in range(10):
        monitoring_system.record_parameter("heart_rate", 80 + i, datetime.now())
        monitoring_system.record_parameter("blood_pressure_systolic", 120 + i*2, datetime.now())
        monitoring_system.record_parameter("temperature", 98.6 + i*0.1, datetime.now())
        time.sleep(0.1)
    
    # get trends
    heart_rate_trend = monitoring_system.get_parameter_trend("heart_rate", minutes=60)
    if heart_rate_trend:
        stats = heart_rate_trend.get_statistics()
        print(f"Heart rate trend: {stats['trend']} (strength: {stats['trend_strength']:.2f})")
    
    # get alerts
    alerts = sim.get_active_alerts()
    print(f"Active alerts: {len(alerts)}")
    
    for alert in alerts[:3]:
        print(f"  • {alert.level.value}: {alert.message}")


def demonstrate_plugin_system():
    """demonstrate plugin system"""
    print("\n" + "="*60)
    print("PLUGIN SYSTEM DEMONSTRATION")
    print("="*60)
    
    # create simulation with plugins
    sim = MedicalSimulation()
    
    # demonstrate plugin loading
    print("Plugin system supports:")
    print("  • Custom physiological models")
    print("  • Additional drug databases")
    print("  • Specialized diagnostic algorithms")
    print("  • Custom assessment criteria")
    print("  • Extended monitoring capabilities")
    
    # show plugin API
    print("\nPlugin API features:")
    print("  • Version 1.0 API compliance")
    print("  • Modular architecture")
    print("  • Hot-swappable components")
    print("  • Standardized interfaces")


def main():
    """main demonstration function"""
    print("🏥 MEDICAL SIMULATOR - COMPREHENSIVE DEMONSTRATION")
    print("=" * 60)
    print("This demonstration showcases all enhanced features including:")
    print("  • Comprehensive medical libraries")
    print("  • Advanced physiological modeling")
    print("  • Real-time monitoring and trending")
    print("  • Drug administration and monitoring")
    print("  • Advanced diagnostic capabilities")
    print("  • Interactive patient dialogue")
    print("  • Performance assessment")
    print("  • Scenario management")
    print("  • Plugin architecture")
    print("  • Enhanced CLI interface")
    
    # run demonstrations
    demonstrate_comprehensive_libraries()
    demonstrate_advanced_simulation()
    demonstrate_cli_features()
    demonstrate_scenario_management()
    demonstrate_monitoring_and_trends()
    demonstrate_plugin_system()
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    print("\nTo run the simulator:")
    print("  python -m medsim")
    print("\nTo access libraries:")
    print("  python -m medsim symptoms_library")
    print("  python -m medsim procedures_library")
    print("  python -m medsim labs_library")
    print("  python -m medsim imaging_library")
    print("\nFor help:")
    print("  python -m medsim --help")


if __name__ == "__main__":
    main() 