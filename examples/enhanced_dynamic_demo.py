#!/usr/bin/env python3
"""
enhanced dynamic generation demonstration
shows disease progression, temporal events, and realistic patient scenarios
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from medsim.core.dynamic_patient_loader import DynamicPatientLoader, PatientLoadConfig
from medsim.core.disease_progression import DiseaseProgressionEngine
from medsim.generation.enhanced_scenario_generator import EnhancedScenarioGenerator, EnhancedScenarioConfig
from medsim.data.clinical_patterns import ClinicalPatterns
import json
import time
from datetime import datetime, timedelta


def demo_disease_progression():
    """demonstrate disease progression system"""
    print("=== Disease Progression Demo ===")
    
    engine = DiseaseProgressionEngine()
    
    # initialize a patient with acute coronary syndrome
    patient_id = "P001"
    disease_name = "acute_coronary_syndrome"
    
    print(f"Initializing {disease_name} for patient {patient_id}...")
    disease_state = engine.initialize_patient_disease(patient_id, disease_name)
    
    print(f"Initial stage: {disease_state.stage.value}")
    print(f"Initial severity: {disease_state.severity_score:.2f}")
    print(f"Prognosis: {disease_state.prognosis}")
    
    # simulate disease progression over time
    print("\nSimulating disease progression:")
    for hours in [1, 2, 4, 6]:
        progressed_state = engine.progress_disease(
            patient_id, disease_name, timedelta(hours=hours)
        )
        
        if progressed_state:
            print(f"  {hours}h: Stage={progressed_state.stage.value}, "
                  f"Severity={progressed_state.severity_score:.2f}, "
                  f"Prognosis={progressed_state.prognosis}")
    
    # administer treatments
    print("\nAdministering treatments:")
    treatments = ["aspirin", "nitroglycerin", "morphine"]
    
    for treatment in treatments:
        effect = engine.administer_treatment(patient_id, treatment)
        if effect:
            print(f"  {treatment}: {effect.response_type.value} response "
                  f"(effectiveness: {effect.effectiveness:.2f})")
            if effect.side_effects:
                print(f"    Side effects: {', '.join(effect.side_effects)}")
    
    # get patient summary
    summary = engine.get_patient_disease_summary(patient_id)
    print(f"\nPatient summary: {len(summary['active_diseases'])} active diseases, "
          f"{len(summary['complications'])} complications")


def demo_dynamic_patient_loading():
    """demonstrate dynamic patient loading with complexity"""
    print("\n=== Dynamic Patient Loading Demo ===")
    
    loader = DynamicPatientLoader()
    
    # test different complexity levels
    complexity_levels = ["simple", "moderate", "complex"]
    specialties = ["emergency_medicine", "cardiology", "neurology"]
    
    for specialty in specialties:
        print(f"\nLoading {specialty} patients:")
        
        for complexity in complexity_levels:
            config = PatientLoadConfig(
                specialty=specialty,
                difficulty="medium",
                complexity_level=complexity,
                social_determinants=True,
                comorbidities=True,
                disease_progression=True,
                realistic_vitals=True,
                medication_history=True
            )
            
            result = loader.load_patient(config)
            patient = result.patient
            
            print(f"  {complexity}: {patient.name}, {patient.age}y, {patient.gender}")
            print(f"    Conditions: {len(patient.conditions)}")
            print(f"    Symptoms: {len(patient.symptoms)}")
            print(f"    Medications: {len(patient.medications)}")
            print(f"    Social determinants: {len(patient.social_history.social_determinants)}")
            print(f"    Social determinants: {[d.value for d in patient.social_history.social_determinants]}")
            print(f"    Medical complexity: {result.medical_complexity:.2f}")
            print(f"    Risk score: {result.risk_score:.2f}")


def demo_enhanced_scenario_generation():
    """demonstrate enhanced scenario generation with temporal events and realism features"""
    print("\n=== Enhanced Scenario Generation Demo ===")
    
    generator = EnhancedScenarioGenerator()
    
    # test different configurations
    configs = [
        EnhancedScenarioConfig(
            specialty="emergency_medicine",
            difficulty="medium",
            complexity_level="moderate",
            temporal_progression=True,
            disease_progression=True,
            social_determinants=True,
            realistic_outcomes=True,
            include_underlying_cause=True,
            include_misleading_clues=True,
            include_incomplete_history=True,
            include_system_barriers=True
        ),
        EnhancedScenarioConfig(
            specialty="cardiology",
            difficulty="hard",
            complexity_level="complex",
            temporal_progression=True,
            disease_progression=True,
            social_determinants=True,
            realistic_outcomes=True,
            include_underlying_cause=True,
            include_misleading_clues=True,
            include_incomplete_history=True,
            include_system_barriers=True
        )
    ]
    
    for i, config in enumerate(configs, 1):
        print(f"\nGenerating enhanced scenario {i}:")
        print(f"  Specialty: {config.specialty}")
        print(f"  Difficulty: {config.difficulty}")
        print(f"  Complexity: {config.complexity_level}")
        
        scenario = generator.generate_enhanced_scenario(config)
        
        print(f"  Title: {scenario.title}")
        print(f"  Patient: {scenario.patient_load_result.patient.name}, "
              f"{scenario.patient_load_result.patient.age}y")
        print(f"  Diseases: {len(scenario.patient_load_result.disease_states)}")
        print(f"  Temporal events: {len(scenario.temporal_events)}")
        print(f"  Decision points: {len(scenario.key_decision_points)}")
        print(f"  Learning objectives: {len(scenario.learning_objectives)}")
        
        # show realism features
        print(f"  Underlying cause: {scenario.underlying_cause}")
        print(f"  Rationale: {scenario.underlying_cause_rationale}")
        print(f"  Misleading clues: {scenario.misleading_clues}")
        print(f"  Incomplete history: {scenario.incomplete_history}")
        print(f"  System barriers: {scenario.system_barriers}")
        print(f"  Differential diagnosis: {scenario.differential_diagnosis}")
        print(f"  Final diagnosis: {scenario.final_diagnosis}")
        
        # show temporal events
        if scenario.temporal_events:
            print("  Temporal events:")
            for event in scenario.temporal_events[:3]:  # show first 3
                time_str = event.timestamp.strftime("%H:%M")
                print(f"    {time_str}: {event.description}")
        
        # show outcome probabilities
        print("  Outcome probabilities:")
        for outcome, prob in scenario.outcome_probabilities.items():
            print(f"    {outcome}: {prob:.2f}")


def demo_realistic_patient_scenarios():
    """demonstrate realistic patient scenarios with social determinants"""
    print("\n=== Realistic Patient Scenarios Demo ===")
    
    loader = DynamicPatientLoader()
    
    # create scenarios with different social contexts
    social_scenarios = [
        {
            "name": "Elderly patient with limited resources",
            "config": PatientLoadConfig(
                specialty="geriatrics",
                difficulty="medium",
                complexity_level="complex",
                social_determinants=True
            )
        },
        {
            "name": "Young patient with substance abuse",
            "config": PatientLoadConfig(
                specialty="emergency_medicine",
                difficulty="hard",
                complexity_level="moderate",
                social_determinants=True
            )
        },
        {
            "name": "Middle-aged patient with chronic conditions",
            "config": PatientLoadConfig(
                specialty="cardiology",
                difficulty="medium",
                complexity_level="moderate",
                social_determinants=True
            )
        }
    ]
    
    for scenario in social_scenarios:
        print(f"\n{scenario['name']}:")
        
        result = loader.load_patient(scenario['config'])
        patient = result.patient
        
        print(f"  Patient: {patient.name}, {patient.age}y, {patient.gender}")
        print(f"  Occupation: {patient.social_history.occupation}")
        print(f"  Insurance: {patient.social_history.insurance_status}")
        print(f"  Social determinants: {[d.value for d in patient.social_history.social_determinants]}")
        print(f"  Conditions: {patient.conditions}")
        print(f"  Medications: {patient.medications}")
        print(f"  Communication style: {patient.personality.communication_style}")
        print(f"  Health literacy: {patient.personality.health_literacy}")
        print(f"  Medical complexity: {result.medical_complexity:.2f}")
        print(f"  Risk score: {result.risk_score:.2f}")
        
        # show realistic factors
        realistic = result.realistic_factors
        print(f"  Presentation delay: {realistic['presentation_delay']:.1f} hours")
        print(f"  Medication compliance: {realistic['medication_compliance']:.2f}")
        print(f"  Follow-up likelihood: {realistic['follow_up_likelihood']:.2f}")


def demo_temporal_progression():
    """demonstrate temporal progression in medical scenarios"""
    print("\n=== Temporal Progression Demo ===")
    
    generator = EnhancedScenarioGenerator()
    
    # create a scenario with temporal progression
    config = EnhancedScenarioConfig(
        specialty="emergency_medicine",
        difficulty="hard",
        complexity_level="complex",
        temporal_progression=True,
        disease_progression=True,
        scenario_duration_hours=6.0
    )
    
    scenario = generator.generate_enhanced_scenario(config)
    
    print(f"Scenario: {scenario.title}")
    print(f"Duration: {config.scenario_duration_hours} hours")
    print(f"Temporal events: {len(scenario.temporal_events)}")
    
    # show timeline
    print("\nTimeline:")
    current_time = datetime.now()
    
    for event in scenario.temporal_events:
        time_offset = event.timestamp - current_time
        hours = time_offset.total_seconds() / 3600
        print(f"  +{hours:.1f}h: {event.description}")
        print(f"    Severity change: {event.severity_change:+.2f}")
        print(f"    Required actions: {', '.join(event.required_actions)}")
    
    # show disease progression
    print(f"\nDisease progression timeline: {len(scenario.disease_progression_timeline)} entries")
    if scenario.disease_progression_timeline:
        initial = scenario.disease_progression_timeline[0]
        final = scenario.disease_progression_timeline[-1]
        print(f"  Initial severity: {initial['severity']:.2f}")
        print(f"  Final severity: {final['severity']:.2f}")
    
    # show treatment timeline
    print(f"\nTreatment timeline: {len(scenario.treatment_timeline)} treatments")
    for treatment in scenario.treatment_timeline:
        time_offset = treatment['timestamp'] - current_time
        hours = time_offset.total_seconds() / 3600
        print(f"  +{hours:.1f}h: {treatment['treatment']} - {treatment['response_type']} response")


def demo_integrated_workflow():
    """demonstrate complete integrated workflow"""
    print("\n=== Integrated Workflow Demo ===")
    
    # initialize all components
    print("Initializing enhanced system components...")
    
    patient_loader = DynamicPatientLoader()
    disease_engine = DiseaseProgressionEngine()
    scenario_generator = EnhancedScenarioGenerator()
    patterns = ClinicalPatterns()
    
    # 1. load complex patient
    print("1. Loading complex patient...")
    patient_config = PatientLoadConfig(
        specialty="emergency_medicine",
        difficulty="hard",
        complexity_level="complex",
        social_determinants=True,
        disease_progression=True
    )
    
    patient_result = patient_loader.load_patient(patient_config)
    patient = patient_result.patient
    
    print(f"   Patient: {patient.name}, {patient.age}y, {patient.gender}")
    print(f"   Conditions: {patient.conditions}")
    print(f"   Social determinants: {[d.value for d in patient.social_history.social_determinants]}")
    print(f"   Medical complexity: {patient_result.medical_complexity:.2f}")
    
    # 2. simulate disease progression
    print("2. Simulating disease progression...")
    for disease_state in patient_result.disease_states:
        print(f"   Disease: {disease_state.disease_name}")
        print(f"   Stage: {disease_state.stage.value}")
        print(f"   Severity: {disease_state.severity_score:.2f}")
        print(f"   Complications: {disease_state.complications}")
    
    # 3. generate enhanced scenario
    print("3. Generating enhanced scenario...")
    scenario_config = EnhancedScenarioConfig(
        specialty="emergency_medicine",
        difficulty="hard",
        complexity_level="complex",
        temporal_progression=True,
        disease_progression=True
    )
    
    scenario = scenario_generator.generate_enhanced_scenario(scenario_config)
    
    print(f"   Scenario: {scenario.title}")
    print(f"   Temporal events: {len(scenario.temporal_events)}")
    print(f"   Decision points: {len(scenario.key_decision_points)}")
    print(f"   Outcome probabilities: {scenario.outcome_probabilities}")
    
    # 4. get comprehensive summary
    print("4. Generating comprehensive summary...")
    summary = scenario_generator.get_enhanced_scenario_summary(scenario)
    
    print(f"   Patient summary: {summary['patient_summary']}")
    print(f"   Disease states: {len(summary['disease_states'])}")
    print(f"   Temporal events: {len(summary['temporal_events'])}")
    print(f"   Medical complexity: {summary['medical_complexity']:.2f}")
    print(f"   Risk score: {summary['risk_score']:.2f}")
    
    print("Integrated workflow completed successfully!")


def main():
    """run all enhanced demonstrations"""
    print("Medsim Enhanced Dynamic Generation System Demo")
    print("=" * 60)
    
    try:
        # run all enhanced demos
        demo_disease_progression()
        demo_dynamic_patient_loading()
        demo_enhanced_scenario_generation()
        demo_realistic_patient_scenarios()
        demo_temporal_progression()
        demo_integrated_workflow()
        
        print("\n" + "=" * 60)
        print("All enhanced demonstrations completed successfully!")
        print("\nEnhanced Features Demonstrated:")
        print("- Realistic disease progression modeling")
        print("- Dynamic patient loading with social determinants")
        print("- Temporal event generation and progression")
        print("- Complex medical scenarios with comorbidities")
        print("- Treatment response variability and side effects")
        print("- Realistic outcome probability modeling")
        print("- Enhanced scenario generation with decision points")
        print("- Integrated workflow with multiple components")
        
    except Exception as e:
        print(f"Error during enhanced demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 