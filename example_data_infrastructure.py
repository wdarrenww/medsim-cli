#!/usr/bin/env python3
"""
example demonstrating the comprehensive data infrastructure for clinical datasets
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
import logging

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# import our data infrastructure components
from medsim.data.dataset_loader import ClinicalDatasetLoader, ClinicalRecord
from medsim.data.pattern_analyzer import PatternAnalyzer
from medsim.data.clinical_patterns import ClinicalPatterns
from medsim.data.data_validator import DataValidator
from medsim.data.anonymizer import DataAnonymizer, AnonymizationConfig


def create_sample_dataset():
    """create a sample clinical dataset for demonstration"""
    sample_data = {
        "patient_records": [
            {
                "demographics": {
                    "patient_id": "P001",
                    "name": "John Smith",
                    "age": 58,
                    "gender": "male",
                    "race": "white",
                    "ethnicity": "non-hispanic",
                    "insurance": "private",
                    "address": "123 Main St, Anytown, CA 90210",
                    "phone": "555-123-4567"
                },
                "presentation": {
                    "chief_complaint": "chest pain for 1 hour",
                    "symptoms": ["chest pain", "shortness of breath", "sweating"],
                    "vital_signs": {
                        "heart_rate": 95,
                        "bp_systolic": 160,
                        "bp_diastolic": 100,
                        "respiratory_rate": 20,
                        "oxygen_saturation": 96,
                        "temperature": 98.6
                    },
                    "arrival_time": "2024-01-15T10:30:00"
                },
                "diagnosis": {
                    "primary": "STEMI",
                    "secondary": ["hypertension", "diabetes"],
                    "icd_codes": ["I21.9"]
                },
                "treatment": {
                    "medications": ["aspirin", "nitroglycerin", "heparin"],
                    "procedures": ["cardiac catheterization"],
                    "sequence": ["aspirin", "nitroglycerin", "cardiac catheterization"]
                },
                "outcome": {
                    "disposition": "admitted",
                    "length_of_stay": 3,
                    "mortality": False,
                    "readmission": False
                },
                "temporal_data": {
                    "arrival_to_diagnosis": 30,
                    "diagnosis_to_treatment": 15,
                    "treatment_to_discharge": 180
                }
            },
            {
                "demographics": {
                    "patient_id": "P002",
                    "name": "Mary Johnson",
                    "age": 65,
                    "gender": "female",
                    "race": "black",
                    "ethnicity": "non-hispanic",
                    "insurance": "medicare",
                    "address": "456 Oak Ave, Somewhere, CA 90211",
                    "phone": "555-987-6543"
                },
                "presentation": {
                    "chief_complaint": "shortness of breath for 2 days",
                    "symptoms": ["shortness of breath", "cough", "wheezing"],
                    "vital_signs": {
                        "heart_rate": 110,
                        "bp_systolic": 140,
                        "bp_diastolic": 85,
                        "respiratory_rate": 28,
                        "oxygen_saturation": 88,
                        "temperature": 99.2
                    },
                    "arrival_time": "2024-01-15T14:20:00"
                },
                "diagnosis": {
                    "primary": "COPD exacerbation",
                    "secondary": ["hypertension"],
                    "icd_codes": ["J44.1"]
                },
                "treatment": {
                    "medications": ["albuterol", "prednisone"],
                    "procedures": ["nebulizer treatment"],
                    "sequence": ["oxygen therapy", "albuterol", "prednisone"]
                },
                "outcome": {
                    "disposition": "admitted",
                    "length_of_stay": 2,
                    "mortality": False,
                    "readmission": False
                },
                "temporal_data": {
                    "arrival_to_diagnosis": 45,
                    "diagnosis_to_treatment": 20,
                    "treatment_to_discharge": 120
                }
            },
            {
                "demographics": {
                    "patient_id": "P003",
                    "name": "David Wilson",
                    "age": 22,
                    "gender": "male",
                    "race": "hispanic",
                    "ethnicity": "hispanic",
                    "insurance": "medicaid",
                    "address": "789 Pine St, Elsewhere, CA 90212",
                    "phone": "555-456-7890"
                },
                "presentation": {
                    "chief_complaint": "right lower quadrant pain for 12 hours",
                    "symptoms": ["abdominal pain", "nausea", "decreased appetite"],
                    "vital_signs": {
                        "heart_rate": 100,
                        "bp_systolic": 130,
                        "bp_diastolic": 80,
                        "respiratory_rate": 18,
                        "oxygen_saturation": 98,
                        "temperature": 100.8
                    },
                    "arrival_time": "2024-01-15T16:45:00"
                },
                "diagnosis": {
                    "primary": "appendicitis",
                    "secondary": [],
                    "icd_codes": ["K35.90"]
                },
                "treatment": {
                    "medications": ["morphine", "ceftriaxone"],
                    "procedures": ["appendectomy"],
                    "sequence": ["pain medication", "antibiotics", "appendectomy"]
                },
                "outcome": {
                    "disposition": "admitted",
                    "length_of_stay": 1,
                    "mortality": False,
                    "readmission": False
                },
                "temporal_data": {
                    "arrival_to_diagnosis": 60,
                    "diagnosis_to_treatment": 30,
                    "treatment_to_discharge": 90
                }
            }
        ]
    }
    
    return sample_data


def demonstrate_data_infrastructure():
    """demonstrate all data infrastructure components"""
    print("=== Medical Simulation Data Infrastructure Demo ===\n")
    
    # 1. create sample dataset
    print("1. Creating sample clinical dataset...")
    sample_data = create_sample_dataset()
    
    # save sample dataset
    with open("sample_clinical_data.json", "w") as f:
        json.dump(sample_data, f, indent=2)
    print("   ✓ Sample dataset saved to sample_clinical_data.json")
    
    # 2. demonstrate dataset loader
    print("\n2. Testing dataset loader...")
    loader = ClinicalDatasetLoader(".")
    
    # load the sample dataset
    success = loader.load_dataset("sample_clinical_data.json", "sample_dataset")
    if success:
        print("   ✓ Dataset loaded successfully")
        
        # get dataset summary
        summary = loader.get_dataset_summary("sample_dataset")
        print(f"   ✓ Dataset contains {summary['metadata'].record_count} records")
        print(f"   ✓ Quality score: {summary['metadata'].quality_score:.2f}")
        print(f"   ✓ Specialties: {summary['metadata'].specialties}")
    else:
        print("   ✗ Failed to load dataset")
        return
    
    # 3. demonstrate data validation
    print("\n3. Testing data validation...")
    validator = DataValidator()
    records = loader.get_dataset("sample_dataset")
    
    validation_result = validator.validate_dataset(records)
    print(f"   ✓ Validation completed")
    print(f"   ✓ Is valid: {validation_result.is_valid}")
    print(f"   ✓ Quality score: {validation_result.quality_score:.2f}")
    print(f"   ✓ Completeness score: {validation_result.completeness_score:.2f}")
    print(f"   ✓ Consistency score: {validation_result.consistency_score:.2f}")
    
    if validation_result.errors:
        print(f"   ⚠ Errors: {len(validation_result.errors)}")
        for error in validation_result.errors[:3]:  # show first 3
            print(f"      - {error}")
    
    if validation_result.warnings:
        print(f"   ⚠ Warnings: {len(validation_result.warnings)}")
        for warning in validation_result.warnings[:3]:  # show first 3
            print(f"      - {warning}")
    
    # 4. demonstrate data anonymization
    print("\n4. Testing data anonymization...")
    anonymizer = DataAnonymizer()
    
    # anonymize the dataset
    original_records = []
    for record in records:
        record_dict = {
            'demographics': record.demographics,
            'presentation': record.presentation,
            'diagnosis': record.diagnosis,
            'treatment': record.treatment,
            'outcome': record.outcome,
            'temporal_data': record.temporal_data,
            'metadata': record.metadata
        }
        original_records.append(record_dict)
    
    anonymized_records = anonymizer.anonymize_dataset(original_records, "sample_dataset")
    
    print(f"   ✓ Anonymized {len(anonymized_records)} records")
    
    # validate anonymization
    validation = anonymizer.validate_anonymization(original_records, anonymized_records)
    print(f"   ✓ Anonymization score: {validation['anonymization_score']:.2f}")
    print(f"   ✓ Medical info preserved: {validation['medical_info_preserved']}")
    
    if validation['pii_remaining']:
        print(f"   ⚠ Remaining PII: {len(validation['pii_remaining'])} records")
    
    # save anonymized dataset
    with open("anonymized_clinical_data.json", "w") as f:
        json.dump({"patient_records": anonymized_records}, f, indent=2)
    print("   ✓ Anonymized dataset saved to anonymized_clinical_data.json")
    
    # 5. demonstrate pattern analysis
    print("\n5. Testing pattern analysis...")
    analyzer = PatternAnalyzer()
    
    # analyze the original dataset
    analysis_results = analyzer.analyze_dataset(records)
    print(f"   ✓ Pattern analysis completed")
    
    # show pattern counts
    for pattern_type, patterns in analysis_results.items():
        if patterns:
            print(f"   ✓ {pattern_type}: {len(patterns)} patterns found")
    
    # show some example patterns
    if analysis_results['symptom_patterns']:
        pattern = analysis_results['symptom_patterns'][0]
        print(f"   ✓ Example symptom pattern: {pattern.characteristics['symptoms']}")
    
    if analysis_results['diagnosis_patterns']:
        pattern = analysis_results['diagnosis_patterns'][0]
        print(f"   ✓ Example diagnosis pattern: {pattern.characteristics['diagnosis']}")
    
    # 6. demonstrate clinical patterns
    print("\n6. Testing clinical pattern generation...")
    patterns = ClinicalPatterns()
    
    # get patterns by specialty
    emergency_patterns = patterns.get_patterns_by_specialty("emergency_medicine")
    print(f"   ✓ Emergency medicine patterns: {len(emergency_patterns)}")
    
    # get random pattern
    random_pattern = patterns.get_random_pattern(specialty="emergency_medicine", difficulty="medium")
    if random_pattern:
        print(f"   ✓ Random pattern: {random_pattern['pattern_name']}")
        print(f"   ✓ Specialty: {random_pattern['specialty']}")
    
    # generate scenario from pattern
    if random_pattern:
        scenario = patterns.generate_scenario_from_pattern(random_pattern)
        print(f"   ✓ Generated scenario with diagnosis: {scenario['diagnosis']['primary']}")
        print(f"   ✓ Patient age: {scenario['demographics']['age']}")
        print(f"   ✓ Symptoms: {scenario['presentation']['symptoms']}")
    
    # 7. demonstrate comprehensive workflow
    print("\n7. Testing comprehensive workflow...")
    
    # load anonymized data
    loader2 = ClinicalDatasetLoader(".")
    loader2.load_dataset("anonymized_clinical_data.json", "anonymized_dataset")
    
    # validate anonymized data
    anonymized_records = loader2.get_dataset("anonymized_dataset")
    validation_result2 = validator.validate_dataset(anonymized_records)
    
    print(f"   ✓ Anonymized data validation: {validation_result2.is_valid}")
    print(f"   ✓ Anonymized data quality: {validation_result2.quality_score:.2f}")
    
    # analyze anonymized patterns
    analysis_results2 = analyzer.analyze_dataset(anonymized_records)
    print(f"   ✓ Anonymized pattern analysis completed")
    
    # export patterns
    analyzer.export_patterns("clinical_patterns.json")
    print("   ✓ Patterns exported to clinical_patterns.json")
    
    print("\n=== Data Infrastructure Demo Complete ===")
    print("\nGenerated files:")
    print("  - sample_clinical_data.json (original dataset)")
    print("  - anonymized_clinical_data.json (anonymized dataset)")
    print("  - clinical_patterns.json (extracted patterns)")
    
    print("\nKey features demonstrated:")
    print("  ✓ Multi-format dataset loading (JSON, CSV, Parquet, Excel)")
    print("  ✓ Comprehensive data validation and quality assessment")
    print("  ✓ PII detection and anonymization with medical info preservation")
    print("  ✓ Clinical pattern recognition and analysis")
    print("  ✓ Scenario generation from real clinical patterns")
    print("  ✓ Specialty-specific pattern libraries")
    print("  ✓ Difficulty-adaptive scenario generation")


if __name__ == "__main__":
    demonstrate_data_infrastructure() 