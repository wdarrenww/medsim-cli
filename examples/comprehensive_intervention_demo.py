#!/usr/bin/env python3
"""
comprehensive intervention system demo
showcases all intervention types, organ systems, and adverse effects
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
import json
from typing import Dict, Any

from medsim.core.intervention_interface import InterventionInterface, InterventionRequest
from medsim.core.patient_state_evolution import PatientStateEvolutionEngine, PatientState
from medsim.core.disease_progression import DiseaseProgressionEngine, DiseaseState
from medsim.core.intervention_manager import InterventionType, OrganSystem, AdverseEventType

def print_header(title: str):
    """print a formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_subheader(title: str):
    """print a formatted subheader"""
    print(f"\n--- {title} ---")

def print_patient_state(state: PatientState):
    """print current patient state"""
    print_subheader("current patient state")
    print(f"consciousness: {state.consciousness}")
    print(f"mobility: {state.mobility}")
    print(f"nutrition: {state.nutrition_status}")
    print(f"skin integrity: {state.skin_integrity}")
    
    print("\nvital signs:")
    vitals = state.vitals
    print(f"  heart rate: {vitals.heart_rate:.1f} bpm")
    print(f"  bp: {vitals.bp_systolic:.0f}/{vitals.bp_diastolic:.0f} mmhg")
    print(f"  map: {vitals.mean_arterial_pressure:.1f} mmhg")
    print(f"  respiratory rate: {vitals.respiratory_rate:.1f} /min")
    print(f"  oxygen saturation: {vitals.oxygen_saturation:.1f}%")
    print(f"  temperature: {vitals.temperature:.1f}°f")
    print(f"  consciousness level: {vitals.consciousness_level}")
    print(f"  urine output: {vitals.urine_output:.1f} ml/hr")
    
    print("\norgan systems:")
    for system_name, organ in state.organ_systems.items():
        status = "normal" if organ.function_score > 0.8 else "mild" if organ.function_score > 0.6 else "moderate" if organ.function_score > 0.4 else "severe"
        print(f"  {system_name}: {status} ({organ.function_score:.2f})")
        if organ.dysfunctions:
            print(f"    dysfunctions: {', '.join(organ.dysfunctions)}")
    
    if state.symptoms:
        print(f"\nsymptoms: {', '.join(state.symptoms)}")
    
    if state.adverse_events:
        print(f"adverse events: {', '.join([event.value for event in state.adverse_events])}")

def print_intervention_menu(interface: InterventionInterface):
    """print the quick intervention menu"""
    print_subheader("quick intervention menu")
    menu = interface.get_quick_intervention_menu()
    
    for category, interventions in menu.items():
        print(f"\n{category.upper()}:")
        for intervention in interventions:
            priority_text = {1: "low", 2: "medium", 3: "high", 4: "urgent"}[intervention["priority"]]
            print(f"  {intervention['name']}: {intervention['description']} ({priority_text} priority)")

def print_available_interventions(interface: InterventionInterface):
    """print available interventions by category"""
    print_subheader("available interventions by category")
    categories = interface.get_intervention_categories()
    
    for category, interventions in categories.items():
        if interventions:
            print(f"\n{category.upper()}:")
            for intervention in interventions:
                print(f"  {intervention}")

def print_organ_system_interventions(interface: InterventionInterface):
    """print interventions by organ system"""
    print_subheader("interventions by organ system")
    organ_interventions = interface.get_organ_system_interventions()
    
    for organ, interventions in organ_interventions.items():
        if interventions:
            print(f"\n{organ.upper()}:")
            for intervention in interventions[:5]:  # show first 5
                print(f"  {intervention}")
            if len(interventions) > 5:
                print(f"  ... and {len(interventions) - 5} more")

def demonstrate_intervention_ordering(interface: InterventionInterface):
    """demonstrate ordering various types of interventions"""
    print_subheader("demonstrating intervention ordering")
    
    # emergency intervention
    print("\n1. ordering emergency intervention (vasopressor):")
    request = InterventionRequest(
        intervention_name="vasopressor",
        parameters={"agent": "norepinephrine", "dose": "0.1mcg/kg/min"},
        priority=4,
        provider="dr_smith",
        notes="patient hypotensive"
    )
    response = interface.request_intervention(request)
    print(f"   success: {response.success}")
    print(f"   message: {response.message}")
    if response.warnings:
        print(f"   warnings: {', '.join(response.warnings)}")
    
    # laboratory test
    print("\n2. ordering laboratory test (cbc):")
    request = InterventionRequest(
        intervention_name="cbc",
        priority=2,
        provider="dr_jones"
    )
    response = interface.request_intervention(request)
    print(f"   success: {response.success}")
    print(f"   message: {response.message}")
    
    # imaging study
    print("\n3. ordering imaging study (chest_xray):")
    request = InterventionRequest(
        intervention_name="chest_xray",
        parameters={"views": "pa_lateral"},
        priority=2,
        provider="dr_wilson"
    )
    response = interface.request_intervention(request)
    print(f"   success: {response.success}")
    print(f"   message: {response.message}")
    
    # supportive care
    print("\n4. ordering supportive care (oxygen_therapy):")
    request = InterventionRequest(
        intervention_name="oxygen_therapy",
        parameters={"flow": "2lpm", "device": "nasal_cannula"},
        priority=2,
        provider="nurse_brown"
    )
    response = interface.request_intervention(request)
    print(f"   success: {response.success}")
    print(f"   message: {response.message}")

def demonstrate_intervention_execution(interface: InterventionInterface, state_engine: PatientStateEvolutionEngine):
    """demonstrate intervention execution and effects"""
    print_subheader("demonstrating intervention execution")
    
    # execute due interventions
    current_time = datetime.now()
    executed_orders = interface.execute_interventions(current_time)
    
    print(f"\nexecuted {len(executed_orders)} interventions:")
    for order in executed_orders:
        print(f"  {order.name} ({order.type.value})")
        print(f"    status: {order.status}")
        if order.result:
            print(f"    result: {order.result}")
        if order.adverse_events:
            print(f"    adverse events: {[event.value for event in order.adverse_events]}")
    
    # evolve patient state
    if interface.current_patient_state:
        print("\nevolving patient state...")
        new_state = state_engine.evolve_state(
            interface.current_patient_state,
            timedelta(minutes=30)
        )
        interface.set_patient_state(new_state)
        print_patient_state(new_state)

def demonstrate_recommendations(interface: InterventionInterface):
    """demonstrate intervention recommendations"""
    print_subheader("intervention recommendations")
    
    recommendations = interface.get_patient_intervention_recommendations()
    
    if recommendations:
        print(f"\nfound {len(recommendations)} recommendations:")
        for i, rec in enumerate(recommendations, 1):
            priority_text = {1: "low", 2: "medium", 3: "high", 4: "urgent"}[rec["priority"]]
            print(f"  {i}. {rec['intervention']}")
            print(f"     reason: {rec['reason']}")
            print(f"     severity: {rec['severity']}")
            print(f"     priority: {priority_text}")
    else:
        print("no recommendations at this time")

def demonstrate_adverse_events(interface: InterventionInterface):
    """demonstrate adverse event tracking"""
    print_subheader("adverse event tracking")
    
    summary = interface.get_adverse_events_summary()
    
    if summary:
        print(f"\nfound {sum(summary.values())} adverse events:")
        for event_type, count in summary.items():
            print(f"  {event_type}: {count}")
    else:
        print("no adverse events recorded")

def demonstrate_effectiveness_report(interface: InterventionInterface):
    """demonstrate intervention effectiveness reporting"""
    print_subheader("intervention effectiveness report")
    
    report = interface.get_intervention_effectiveness_report()
    
    if report:
        print(f"\nanalyzing {len(report)} interventions:")
        for intervention, data in report.items():
            if data["total_orders"] > 0:
                success_rate = data["success_rate"] * 100
                adverse_rate = data["adverse_event_rate"] * 100
                print(f"  {intervention}:")
                print(f"    success rate: {success_rate:.1f}%")
                print(f"    adverse event rate: {adverse_rate:.1f}%")
                print(f"    average duration: {data['avg_duration']:.1f} minutes")
    else:
        print("no effectiveness data available")

def demonstrate_comprehensive_data_export(interface: InterventionInterface):
    """demonstrate comprehensive data export"""
    print_subheader("comprehensive data export")
    
    data = interface.export_intervention_data()
    
    print(f"\nexported data includes:")
    print(f"  - {len(data['orders_summary']['recent_orders'])} recent orders")
    print(f"  - {len(data['active_orders'])} active orders")
    print(f"  - {len(data['completed_orders'])} completed orders")
    print(f"  - {len(data['failed_orders'])} failed orders")
    print(f"  - {len(data['adverse_events'])} adverse event types")
    print(f"  - {len(data['effectiveness_report'])} interventions analyzed")
    print(f"  - {len(data['recommendations'])} recommendations")
    print(f"  - {len(data['available_interventions'])} available interventions")
    print(f"  - {len(data['organ_system_interventions'])} organ systems")
    print(f"  - {len(data['intervention_categories'])} intervention categories")

def main():
    """main demonstration function"""
    print_header("comprehensive intervention system demo")
    
    # initialize systems
    print("initializing intervention systems...")
    interface = InterventionInterface()
    state_engine = PatientStateEvolutionEngine()
    disease_engine = DiseaseProgressionEngine()
    
    # create a patient with multiple diseases
    print("creating patient with complex disease state...")
    disease_states = [
        DiseaseState("sepsis", "moderate", 0.7),
        DiseaseState("acute_respiratory_distress_syndrome", "mild", 0.4),
        DiseaseState("acute_kidney_injury", "mild", 0.3)
    ]
    
    patient_state = state_engine.initialize_patient_state(disease_states)
    interface.set_patient_state(patient_state)
    
    print_patient_state(patient_state)
    
    # demonstrate intervention menu
    print_intervention_menu(interface)
    
    # demonstrate available interventions
    print_available_interventions(interface)
    
    # demonstrate organ system interventions
    print_organ_system_interventions(interface)
    
    # demonstrate intervention ordering
    demonstrate_intervention_ordering(interface)
    
    # demonstrate intervention execution
    demonstrate_intervention_execution(interface, state_engine)
    
    # demonstrate recommendations
    demonstrate_recommendations(interface)
    
    # demonstrate adverse events
    demonstrate_adverse_events(interface)
    
    # demonstrate effectiveness reporting
    demonstrate_effectiveness_report(interface)
    
    # demonstrate comprehensive data export
    demonstrate_comprehensive_data_export(interface)
    
    print_header("demo completed")
    print("this demonstration showcased:")
    print("  ✓ comprehensive intervention types (medications, procedures, labs, imaging, supportive, monitoring, emergency)")
    print("  ✓ 11 organ systems with detailed function tracking")
    print("  ✓ 20+ types of adverse events")
    print("  ✓ user-friendly interface for intervention management")
    print("  ✓ real-time patient state evolution")
    print("  ✓ intervention recommendations based on patient state")
    print("  ✓ effectiveness reporting and analytics")
    print("  ✓ comprehensive data export capabilities")

if __name__ == "__main__":
    main() 