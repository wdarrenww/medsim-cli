#!/usr/bin/env python3
"""
continuous simulation demonstration
shows full loop logic with up to 3 patients simultaneously
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from medsim.core.continuous_simulation_engine import ContinuousSimulationEngine, SimulationEvent, SimulationMetrics
from medsim.core.patient_queue_manager import PatientQueueManager
from medsim.core.dynamic_patient_loader import DynamicPatientLoader
from medsim.generation.enhanced_scenario_generator import EnhancedScenarioGenerator
import time
from datetime import datetime, timedelta


def demo_queue_manager():
    """demonstrate patient queue manager functionality"""
    print("=== Patient Queue Manager Demo ===")
    
    queue_manager = PatientQueueManager(max_simultaneous_patients=3)
    
    # generate several patients
    current_time = datetime.now()
    patients = []
    
    for i in range(5):
        patient = queue_manager.generate_new_patient(current_time)
        queue_manager.add_patient_to_queue(patient)
        patients.append(patient)
        
        print(f"Generated patient {patient.patient_id}:")
        print(f"  Name: {patient.patient_result.patient.name}")
        print(f"  Age: {patient.patient_result.patient.age}y")
        print(f"  Specialty: {patient.specialty_needed}")
        print(f"  Complexity: {patient.complexity_level}")
        print(f"  Priority: {patient.priority_score:.2f}")
        print(f"  Conditions: {patient.patient_result.patient.conditions}")
        print()
    
    # show queue status
    status = queue_manager.get_queue_status()
    print(f"Queue Status:")
    print(f"  Waiting: {status['waiting_count']}")
    print(f"  Active: {status['active_count']}")
    print(f"  Completed: {status['completed_count']}")
    print(f"  Available slots: {status['available_slots']}")
    
    # show waiting patients
    print("\nWaiting patients:")
    for patient_info in status['waiting_patients']:
        print(f"  {patient_info['id']}: Priority {patient_info['priority']:.2f}, "
              f"{patient_info['complexity']} {patient_info['specialty']}")
    
    # activate some patients
    print("\nActivating patients...")
    providers = ["Dr. Smith", "Dr. Johnson", "Dr. Williams"]
    
    for i, provider in enumerate(providers):
        next_patient = queue_manager.get_next_patient()
        if next_patient:
            queue_manager.activate_patient(next_patient, provider, current_time)
            print(f"  Activated {next_patient} with {provider}")
    
    # show updated status
    status = queue_manager.get_queue_status()
    print(f"\nUpdated Queue Status:")
    print(f"  Waiting: {status['waiting_count']}")
    print(f"  Active: {status['active_count']}")
    print(f"  Available slots: {status['available_slots']}")
    
    # show active patients
    print("\nActive patients:")
    for patient_info in status['active_patients']:
        print(f"  {patient_info['id']}: {patient_info['provider']}, "
              f"Est. completion: {patient_info['estimated_completion']}")


def demo_continuous_simulation():
    """demonstrate continuous simulation engine"""
    print("\n=== Continuous Simulation Demo ===")
    
    # create simulation engine
    engine = ContinuousSimulationEngine(
        max_simultaneous_patients=3,
        arrival_rate_per_hour=3.0
    )
    
    # set up event callback
    def event_callback(event: SimulationEvent):
        timestamp = event.timestamp.strftime("%H:%M:%S")
        print(f"[{timestamp}] {event.event_type}: {event.description}")
    
    engine.add_event_callback(event_callback)
    
    # set up metrics callback
    def metrics_callback(metrics: SimulationMetrics):
        print(f"\n--- Metrics Update ---")
        print(f"Total patients processed: {metrics.total_patients_processed}")
        print(f"Average patients per hour: {metrics.average_patients_per_hour:.1f}")
        print(f"Average wait time: {metrics.average_wait_time}")
        print(f"Specialty distribution: {metrics.specialty_distribution}")
        print(f"Complexity distribution: {metrics.complexity_distribution}")
    
    engine.add_metrics_callback(metrics_callback)
    
    # start simulation
    print("Starting continuous simulation...")
    print("Simulation will run for 2 hours with 3x time acceleration")
    
    engine.set_time_acceleration(3.0)  # 3x speed
    engine.start_simulation(duration_hours=2.0)
    
    # monitor simulation
    start_time = time.time()
    while engine.state.value == "running" and time.time() - start_time < 30:  # max 30 seconds demo
        time.sleep(2)
        
        # show current status
        status = engine.get_simulation_status()
        print(f"\n--- Simulation Status ---")
        print(f"State: {status['state']}")
        print(f"Current time: {status['current_time'].strftime('%H:%M:%S')}")
        print(f"Total events: {status['total_events']}")
        
        queue_status = status['queue_status']
        print(f"Queue: {queue_status['waiting_count']} waiting, "
              f"{queue_status['active_count']} active, "
              f"{queue_status['completed_count']} completed")
    
    # stop simulation
    engine.stop_simulation_engine()
    print("\nSimulation completed!")
    
    # show final metrics
    final_metrics = engine.get_simulation_metrics()
    print(f"\nFinal Metrics:")
    print(f"Total patients processed: {final_metrics.total_patients_processed}")
    print(f"Total simulation time: {final_metrics.total_simulation_time}")
    print(f"Average patients per hour: {final_metrics.average_patients_per_hour:.1f}")
    print(f"Average wait time: {final_metrics.average_wait_time}")
    
    # show recent events
    recent_events = engine.get_recent_events(10)
    print(f"\nRecent Events:")
    for event in recent_events:
        timestamp = event.timestamp.strftime("%H:%M:%S")
        print(f"  [{timestamp}] {event.event_type}: {event.description}")


def demo_dynamic_variation():
    """demonstrate dynamic variation in patient generation"""
    print("\n=== Dynamic Variation Demo ===")
    
    queue_manager = PatientQueueManager(max_simultaneous_patients=3)
    
    # generate patients with different settings
    current_time = datetime.now()
    
    print("Generating patients with dynamic variation...")
    
    for i in range(10):
        patient = queue_manager.generate_new_patient(current_time)
        queue_manager.add_patient_to_queue(patient)
        
        print(f"Patient {patient.patient_id}:")
        print(f"  Name: {patient.patient_result.patient.name}")
        print(f"  Age: {patient.patient_result.patient.age}y")
        print(f"  Gender: {patient.patient_result.patient.gender}")
        print(f"  Specialty: {patient.specialty_needed}")
        print(f"  Complexity: {patient.complexity_level}")
        print(f"  Priority: {patient.priority_score:.2f}")
        print(f"  Medical complexity: {patient.patient_result.medical_complexity:.2f}")
        print(f"  Risk score: {patient.patient_result.risk_score:.2f}")
        print(f"  Social determinants: {[d.value for d in patient.patient_result.patient.social_history.social_determinants]}")
        print(f"  Conditions: {patient.patient_result.patient.conditions}")
        print(f"  Symptoms: {patient.patient_result.patient.symptoms}")
        print()
    
    # show distribution statistics
    metrics = queue_manager.get_queue_metrics()
    print("Distribution Statistics:")
    print(f"  Specialty distribution: {metrics.specialty_distribution}")
    print(f"  Complexity distribution: {metrics.complexity_distribution}")
    
    # show patient details for one patient
    if queue_manager.patients:
        first_patient_id = list(queue_manager.patients.keys())[0]
        patient_details = queue_manager.get_patient_summary(first_patient_id)
        
        print(f"\nDetailed Patient Summary for {first_patient_id}:")
        for key, value in patient_details.items():
            if key not in ['disease_states', 'notes']:  # skip complex nested data
                print(f"  {key}: {value}")


def demo_realistic_flow():
    """demonstrate realistic patient flow with transfers and complications"""
    print("\n=== Realistic Patient Flow Demo ===")
    
    engine = ContinuousSimulationEngine(
        max_simultaneous_patients=3,
        arrival_rate_per_hour=4.0
    )
    
    # set up detailed event callback
    def detailed_event_callback(event: SimulationEvent):
        timestamp = event.timestamp.strftime("%H:%M:%S")
        event_type = event.event_type
        
        if event_type == "patient_arrival":
            print(f"[{timestamp}] 🚑 {event.description}")
        elif event_type == "patient_activation":
            print(f"[{timestamp}] 👨‍⚕️ {event.description}")
        elif event_type == "patient_completion":
            print(f"[{timestamp}] ✅ {event.description}")
        elif event_type == "patient_transfer":
            print(f"[{timestamp}] 🚨 {event.description}")
    
    engine.add_event_callback(detailed_event_callback)
    
    # start simulation with higher time acceleration
    print("Starting realistic flow simulation...")
    print("Simulation will run for 1 hour with 5x time acceleration")
    
    engine.set_time_acceleration(5.0)
    engine.start_simulation(duration_hours=1.0)
    
    # monitor for 20 seconds
    start_time = time.time()
    while engine.state.value == "running" and time.time() - start_time < 20:
        time.sleep(1)
        
        # show current queue status
        status = engine.get_simulation_status()
        queue_status = status['queue_status']
        
        print(f"\rQueue: {queue_status['waiting_count']} waiting, "
              f"{queue_status['active_count']} active, "
              f"{queue_status['completed_count']} completed", end="")
    
    # stop simulation
    engine.stop_simulation_engine()
    print("\n\nRealistic flow simulation completed!")
    
    # show final statistics
    final_metrics = engine.get_simulation_metrics()
    print(f"\nFinal Statistics:")
    print(f"Total patients processed: {final_metrics.total_patients_processed}")
    print(f"Average patients per hour: {final_metrics.average_patients_per_hour:.1f}")
    print(f"Specialty distribution: {final_metrics.specialty_distribution}")
    print(f"Complexity distribution: {final_metrics.complexity_distribution}")


def demo_integrated_workflow():
    """demonstrate complete integrated workflow"""
    print("\n=== Integrated Workflow Demo ===")
    
    # create all components
    print("Initializing integrated system components...")
    
    queue_manager = PatientQueueManager(max_simultaneous_patients=3)
    engine = ContinuousSimulationEngine(max_simultaneous_patients=3)
    patient_loader = DynamicPatientLoader()
    scenario_generator = EnhancedScenarioGenerator()
    
    # 1. demonstrate queue management
    print("1. Testing queue management...")
    current_time = datetime.now()
    
    for i in range(3):
        patient = queue_manager.generate_new_patient(current_time)
        queue_manager.add_patient_to_queue(patient)
        print(f"   Added patient {patient.patient_id} ({patient.specialty_needed})")
    
    status = queue_manager.get_queue_status()
    print(f"   Queue status: {status['waiting_count']} waiting, {status['active_count']} active")
    
    # 2. demonstrate patient activation
    print("2. Testing patient activation...")
    providers = ["Dr. Smith", "Dr. Johnson"]
    
    for provider in providers:
        next_patient = queue_manager.get_next_patient()
        if next_patient:
            queue_manager.activate_patient(next_patient, provider, current_time)
            print(f"   Activated {next_patient} with {provider}")
    
    # 3. demonstrate scenario generation
    print("3. Testing enhanced scenario generation...")
    config = EnhancedScenarioConfig(
        specialty="emergency_medicine",
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
    
    scenario = scenario_generator.generate_enhanced_scenario(config)
    print(f"   Generated scenario: {scenario.title}")
    print(f"   Underlying cause: {scenario.underlying_cause}")
    print(f"   Misleading clues: {len(scenario.misleading_clues)}")
    print(f"   System barriers: {len(scenario.system_barriers)}")
    
    # 4. demonstrate continuous simulation
    print("4. Testing continuous simulation...")
    
    def quick_event_callback(event: SimulationEvent):
        timestamp = event.timestamp.strftime("%H:%M:%S")
        print(f"   [{timestamp}] {event.event_type}: {event.patient_id}")
    
    engine.add_event_callback(quick_event_callback)
    
    # run simulation for 10 seconds
    engine.set_time_acceleration(10.0)
    engine.start_simulation(duration_hours=0.5)
    
    time.sleep(10)
    engine.stop_simulation_engine()
    
    # 5. show final results
    print("5. Final results...")
    final_status = engine.get_simulation_status()
    print(f"   Total events: {final_status['total_events']}")
    print(f"   Patients processed: {final_status['metrics']['total_patients_processed']}")
    print(f"   Average patients per hour: {final_status['metrics']['average_patients_per_hour']:.1f}")
    
    print("Integrated workflow completed successfully!")


def main():
    """run all continuous simulation demonstrations"""
    print("Medsim Continuous Simulation System Demo")
    print("=" * 60)
    
    try:
        # run all demos
        demo_queue_manager()
        demo_continuous_simulation()
        demo_dynamic_variation()
        demo_realistic_flow()
        demo_integrated_workflow()
        
        print("\n" + "=" * 60)
        print("All continuous simulation demonstrations completed successfully!")
        print("\nContinuous Simulation Features Demonstrated:")
        print("- Patient queue management with priority-based scheduling")
        print("- Dynamic patient generation with varied specialties and complexity")
        print("- Realistic patient flow with arrivals, activations, and completions")
        print("- Disease progression for active patients")
        print("- Patient transfers for critical conditions")
        print("- Comprehensive metrics and event tracking")
        print("- Time-accelerated simulation with configurable parameters")
        print("- Multi-threaded continuous operation")
        print("- Integrated workflow with all system components")
        
    except Exception as e:
        print(f"Error during continuous simulation demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 