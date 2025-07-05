#!/usr/bin/env python3
"""
dynamic generation demonstration script
shows integrated pattern-driven patient generation, scenario management, and continuous simulation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from medsim.data.dataset_loader import ClinicalDatasetLoader, ClinicalRecord
from medsim.data.pattern_analyzer import PatternAnalyzer
from medsim.data.clinical_patterns import ClinicalPatterns
from medsim.generation.scenario_generator import DynamicScenarioGenerator, DynamicScenarioConfig
from medsim.scenarios.scenario_manager import ScenarioManager
from medsim.core.patient import PatientProfileGenerator
from medsim.data.data_validator import DataValidator
import json
import time


def demo_data_infrastructure():
    """demonstrate data infrastructure components"""
    print("=== Data Infrastructure Demo ===")
    
    # initialize components
    loader = ClinicalDatasetLoader()
    analyzer = PatternAnalyzer()
    patterns = ClinicalPatterns()
    
    # load sample data
    print("Loading sample clinical data...")
    sample_data = [
        {
            "patient_id": "P001",
            "age": 65,
            "gender": "male",
            "presenting_symptoms": ["chest pain", "shortness of breath"],
            "diagnosis": "acute coronary syndrome",
            "risk_factors": ["hypertension", "diabetes", "smoking"],
            "vital_signs": {"hr": 95, "bp": 160/100, "rr": 20, "o2": 96},
            "treatments": ["aspirin", "nitroglycerin", "cardiac catheterization"]
        },
        {
            "patient_id": "P002", 
            "age": 45,
            "gender": "female",
            "presenting_symptoms": ["headache", "nausea", "photophobia"],
            "diagnosis": "migraine",
            "risk_factors": ["stress", "family history"],
            "vital_signs": {"hr": 85, "bp": 140/90, "rr": 16, "o2": 98},
            "treatments": ["sumatriptan", "hydration", "rest"]
        }
    ]
    
    # validate data
    print("Validating data structure...")
    # convert sample_data dicts to ClinicalRecord objects for validation
    records = []
    for d in sample_data:
        record = ClinicalRecord(
            patient_id=d.get('patient_id', 'unknown'),
            demographics={
                'age': d.get('age', 0),
                'gender': d.get('gender', 'unknown')
            },
            presentation={
                'symptoms': d.get('presenting_symptoms', []),
                'vital_signs': d.get('vital_signs', {})
            },
            diagnosis={'primary': d.get('diagnosis', '')},
            treatment={'medications': d.get('treatments', [])},
            outcome={},
            temporal_data={},
            metadata={}
        )
        records.append(record)
    validator = DataValidator()
    validation_result = validator.validate_dataset(records)
    print(f"Validation: {validation_result.is_valid}")
    if not validation_result.is_valid:
        print(f"Errors: {validation_result.errors}")
    
    # analyze patterns
    print("Analyzing clinical patterns...")
    pattern_results = analyzer.analyze_dataset(records)
    print(f"Found {len(pattern_results)} patterns")
    
    # fetch a random clinical pattern
    print("Fetching a random clinical pattern...")
    random_pattern = patterns.get_random_pattern()
    print(f"Random pattern: {random_pattern.get('pattern_name', 'N/A')}")
    return random_pattern


def demo_patient_generation():
    """demonstrate enhanced patient profile generation"""
    print("\n=== Enhanced Patient Generation Demo ===")
    
    generator = PatientProfileGenerator()
    
    # generate patients by specialty
    specialties = ["emergency_medicine", "cardiology", "pediatrics", "geriatrics"]
    difficulties = ["easy", "medium", "hard"]
    
    print("Generating specialty-specific patients:")
    for specialty in specialties:
        patient = generator.generate_patient_by_specialty(specialty, "medium")
        print(f"  {specialty}: {patient.name}, {patient.age}y, {patient.gender}")
        print(f"    Conditions: {patient.conditions[:3]}")
        print(f"    Symptoms: {patient.symptoms[:3]}")
    
    print("\nGenerating difficulty-specific patients:")
    for difficulty in difficulties:
        patient = generator.generate_patient_by_difficulty(difficulty)
        print(f"  {difficulty}: {patient.name}, {patient.age}y")
        print(f"    Communication: {patient.personality.communication_style}")
        print(f"    Health literacy: {patient.personality.health_literacy}")
        print(f"    Social determinants: {len(patient.social_history.social_determinants)}")


def demo_dynamic_scenario_generation():
    """demonstrate dynamic scenario generation"""
    print("\n=== Dynamic Scenario Generation Demo ===")
    
    generator = DynamicScenarioGenerator()
    
    # generate scenarios with different configurations
    configs = [
        DynamicScenarioConfig(specialty="emergency_medicine", difficulty="medium"),
        DynamicScenarioConfig(specialty="cardiology", difficulty="hard"),
        DynamicScenarioConfig(specialty="pediatrics", difficulty="easy"),
        DynamicScenarioConfig(specialty="geriatrics", difficulty="medium")
    ]
    
    for i, config in enumerate(configs, 1):
        print(f"\nGenerating scenario {i}:")
        print(f"  Specialty: {config.specialty}")
        print(f"  Difficulty: {config.difficulty}")
        
        scenario = generator.generate_scenario(config)
        
        if scenario:
            print(f"  Diagnosis: {scenario.get('diagnosis', {}).get('primary', 'Unknown')}")
            print(f"  Age: {scenario.get('demographics', {}).get('age', 'Unknown')}")
            print(f"  Gender: {scenario.get('demographics', {}).get('gender', 'Unknown')}")
            print(f"  Symptoms: {scenario.get('presentation', {}).get('symptoms', [])[:3]}")
            print(f"  Key Actions: {scenario.get('key_actions', [])[:3]}")


def demo_continuous_simulation():
    """demonstrate continuous simulation mode"""
    print("\n=== Continuous Simulation Demo ===")
    
    manager = ScenarioManager()
    
    # start continuous mode
    print("Starting continuous simulation mode...")
    success = manager.start_continuous_mode(
        specialty="emergency_medicine",
        difficulty="medium",
        scenario_count=5
    )
    
    if success:
        print("Continuous mode started successfully")
        
        # simulate user performance updates
        performance_metrics = {
            "diagnostic_accuracy": 0.8,
            "treatment_appropriateness": 0.7,
            "time_efficiency": 0.9,
            "patient_safety": 0.85
        }
        
        print("Updating user performance...")
        manager.update_user_performance(performance_metrics)
        
        # get scenarios from sequence
        print("Retrieving scenarios from sequence:")
        for i in range(5):
            scenario = manager.get_next_continuous_scenario()
            if scenario:
                print(f"  Scenario {i+1}: {scenario['title']}")
                print(f"    Diagnosis: {scenario['correct_diagnosis']}")
                print(f"    Difficulty: {scenario['difficulty']}")
                print(f"    Time Limit: {scenario['time_limit']} minutes")
            else:
                print(f"  No more scenarios available")
                break


def demo_integrated_workflow():
    """demonstrate complete integrated workflow"""
    print("\n=== Integrated Workflow Demo ===")
    
    # initialize all components
    print("Initializing integrated system...")
    
    # data infrastructure
    loader = ClinicalDatasetLoader()
    analyzer = PatternAnalyzer()
    patterns = ClinicalPatterns()
    
    # generation components
    scenario_generator = DynamicScenarioGenerator()
    patient_generator = PatientProfileGenerator()
    
    # management components
    scenario_manager = ScenarioManager()
    
    # simulate data-driven workflow
    print("Simulating data-driven workflow:")
    
    # 1. load and analyze clinical data
    print("1. Loading and analyzing clinical data...")
    sample_data = [
        {
            "patient_id": "P001",
            "age": 58,
            "gender": "male",
            "presenting_symptoms": ["chest pain", "shortness of breath", "sweating"],
            "diagnosis": "acute coronary syndrome",
            "risk_factors": ["hypertension", "diabetes", "smoking"],
            "vital_signs": {"hr": 95, "bp": 160/100, "rr": 20, "o2": 96},
            "treatments": ["aspirin", "nitroglycerin", "cardiac catheterization"]
        }
    ]
    
    # 2. generate patterns
    print("2. Generating clinical patterns...")
    random_pattern = patterns.get_random_pattern()
    
    # 3. create dynamic scenario
    print("3. Creating dynamic scenario...")
    config = DynamicScenarioConfig(
        specialty="emergency_medicine",
        difficulty="medium",
        variety=0.8,
        adaptive=True
    )
    
    scenario_data = scenario_generator.generate_scenario(config)
    
    # 4. generate patient profile
    print("4. Generating patient profile...")
    if scenario_data:
        patient = patient_generator.generate_patient_from_pattern(
            scenario_data, 
            difficulty="medium"
        )
        print(f"   Patient: {patient.name}, {patient.age}y, {patient.gender}")
        print(f"   Conditions: {patient.conditions}")
        print(f"   Symptoms: {patient.symptoms}")
    
    # 5. integrate with scenario manager
    print("5. Integrating with scenario manager...")
    scenario = scenario_manager.generate_dynamic_scenario(
        specialty="emergency_medicine",
        difficulty="medium"
    )
    
    if scenario:
        print(f"   Scenario: {scenario['title']}")
        print(f"   Diagnosis: {scenario['correct_diagnosis']}")
        print(f"   Actions: {scenario['optimal_actions'][:3]}")
    
    print("Integrated workflow completed successfully!")


def demo_performance_tracking():
    """demonstrate performance tracking and adaptive difficulty"""
    print("\n=== Performance Tracking Demo ===")
    
    manager = ScenarioManager()
    
    # simulate multiple scenario attempts with varying performance
    performance_scenarios = [
        {"diagnostic_accuracy": 0.9, "treatment_appropriateness": 0.8, "time_efficiency": 0.95},
        {"diagnostic_accuracy": 0.7, "treatment_appropriateness": 0.6, "time_efficiency": 0.8},
        {"diagnostic_accuracy": 0.5, "treatment_appropriateness": 0.4, "time_efficiency": 0.6},
        {"diagnostic_accuracy": 0.8, "treatment_appropriateness": 0.7, "time_efficiency": 0.85}
    ]
    
    print("Simulating performance tracking:")
    for i, performance in enumerate(performance_scenarios, 1):
        print(f"  Scenario {i} performance:")
        for metric, value in performance.items():
            print(f"    {metric}: {value:.2f}")
        
        manager.update_user_performance(performance)
        
        # generate next scenario with adaptive difficulty
        next_scenario = manager.generate_dynamic_scenario(
            specialty="emergency_medicine",
            variety=0.8
        )
        
        if next_scenario:
            print(f"    Next scenario difficulty: {next_scenario['difficulty']}")
    
    # show average performance
    avg_performance = manager._get_average_performance()
    if avg_performance:
        print(f"\nAverage performance:")
        for metric, value in avg_performance.items():
            print(f"  {metric}: {value:.2f}")


def main():
    """run all demonstrations"""
    print("Medsim Dynamic Generation System Demo")
    print("=" * 50)
    
    try:
        # run all demos
        demo_data_infrastructure()
        demo_patient_generation()
        demo_dynamic_scenario_generation()
        demo_continuous_simulation()
        demo_integrated_workflow()
        demo_performance_tracking()
        
        print("\n" + "=" * 50)
        print("All demonstrations completed successfully!")
        print("\nKey Features Demonstrated:")
        print("- Data-driven pattern analysis")
        print("- Specialty-specific patient generation")
        print("- Difficulty-adaptive scenarios")
        print("- Continuous simulation loops")
        print("- Performance tracking and adaptation")
        print("- Integrated workflow management")
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 