# Medical Simulation Data Infrastructure

This document describes the comprehensive data infrastructure for the medical simulation platform, enabling data-driven scenario generation and continuous looped experiences.

## Overview

The data infrastructure provides a complete pipeline for:
- Loading and validating clinical datasets
- Anonymizing patient data while preserving medical relevance
- Analyzing clinical patterns from real data
- Generating realistic scenarios based on identified patterns
- Supporting continuous simulation loops

## Architecture

```
medsim/data/
├── __init__.py              # Module initialization
├── dataset_loader.py        # Multi-format dataset loading
├── pattern_analyzer.py      # Clinical pattern recognition
├── clinical_patterns.py     # Pattern templates and generation
├── data_validator.py        # Data quality validation
└── anonymizer.py           # PII removal and anonymization
```

## Components

### 1. Dataset Loader (`dataset_loader.py`)

**Purpose**: Load clinical datasets from multiple formats and validate structure.

**Key Features**:
- Supports JSON, CSV, Parquet, and Excel formats
- Automatic data structure validation
- Metadata generation and quality scoring
- Flexible field mapping for different data sources

**Usage**:
```python
from medsim.data.dataset_loader import ClinicalDatasetLoader

# Initialize loader
loader = ClinicalDatasetLoader("data_directory")

# Load dataset
success = loader.load_dataset("clinical_data.json", "emergency_dataset")

# Get dataset summary
summary = loader.get_dataset_summary("emergency_dataset")
print(f"Quality score: {summary['metadata'].quality_score}")
```

**Supported Formats**:
- **JSON**: Structured clinical records
- **CSV**: Tabular data with column mapping
- **Parquet**: High-performance columnar format
- **Excel**: Spreadsheet data with multiple sheets

### 2. Pattern Analyzer (`pattern_analyzer.py`)

**Purpose**: Identify clinical patterns from datasets for scenario generation.

**Key Features**:
- Symptom cluster analysis
- Diagnosis-treatment pattern recognition
- Temporal pattern analysis
- Demographic pattern identification
- Statistical clustering of similar patterns

**Usage**:
```python
from medsim.data.pattern_analyzer import PatternAnalyzer

# Initialize analyzer
analyzer = PatternAnalyzer()

# Analyze dataset
records = loader.get_dataset("emergency_dataset")
analysis_results = analyzer.analyze_dataset(records)

# Get patterns by type
symptom_patterns = analyzer.get_patterns_by_type("symptom_cluster")
diagnosis_patterns = analyzer.get_patterns_by_type("diagnosis_pattern")

# Export patterns
analyzer.export_patterns("clinical_patterns.json")
```

**Pattern Types**:
- **Symptom Clusters**: Common symptom combinations
- **Diagnosis Patterns**: Disease presentations and characteristics
- **Treatment Sequences**: Standard treatment protocols
- **Temporal Patterns**: Time-based clinical events
- **Demographic Patterns**: Age/gender-specific presentations
- **Outcome Patterns**: Disposition and mortality patterns

### 3. Clinical Patterns (`clinical_patterns.py`)

**Purpose**: Define clinical pattern templates and generate scenarios.

**Key Features**:
- Specialty-specific pattern libraries
- Difficulty-adaptive scenario generation
- Realistic patient trajectory modeling
- Performance-based difficulty adjustment

**Usage**:
```python
from medsim.data.clinical_patterns import ClinicalPatterns

# Initialize patterns
patterns = ClinicalPatterns()

# Get patterns by specialty
emergency_patterns = patterns.get_patterns_by_specialty("emergency_medicine")

# Generate scenario from pattern
random_pattern = patterns.get_random_pattern(specialty="emergency_medicine")
scenario = patterns.generate_scenario_from_pattern(random_pattern, user_performance)

print(f"Generated scenario: {scenario['diagnosis']['primary']}")
```

**Specialties Supported**:
- Emergency Medicine
- Cardiology
- Neurology
- Respiratory Medicine
- Surgery
- Pediatrics
- Obstetrics

### 4. Data Validator (`data_validator.py`)

**Purpose**: Ensure data quality and validate clinical dataset structure.

**Key Features**:
- Comprehensive data validation
- Quality scoring and metrics
- Anomaly detection
- Consistency checking
- Completeness assessment

**Usage**:
```python
from medsim.data.data_validator import DataValidator

# Initialize validator
validator = DataValidator()

# Validate dataset
validation_result = validator.validate_dataset(records)

print(f"Valid: {validation_result.is_valid}")
print(f"Quality Score: {validation_result.quality_score}")
print(f"Completeness: {validation_result.completeness_score}")

# Get detailed metrics
metrics = validator.get_quality_metrics(records)
print(f"Anomaly rate: {metrics.anomaly_rate}")
```

**Validation Checks**:
- Required field completeness
- Data type validation
- Logical consistency (e.g., BP relationships)
- Anomaly detection (statistical outliers)
- Duplicate record detection
- PII presence validation

### 5. Data Anonymizer (`anonymizer.py`)

**Purpose**: Remove PII while preserving medical relevance.

**Key Features**:
- Comprehensive PII detection
- Medical information preservation
- Configurable anonymization levels
- Validation of anonymization quality

**Usage**:
```python
from medsim.data.anonymizer import DataAnonymizer, AnonymizationConfig

# Configure anonymization
config = AnonymizationConfig(
    preserve_medical_info=True,
    add_noise_to_ages=True,
    hash_identifiers=True
)

# Initialize anonymizer
anonymizer = DataAnonymizer(config)

# Anonymize dataset
original_records = [record.__dict__ for record in records]
anonymized_records = anonymizer.anonymize_dataset(original_records)

# Validate anonymization
validation = anonymizer.validate_anonymization(original_records, anonymized_records)
print(f"Anonymization score: {validation['anonymization_score']}")
```

**PII Detection**:
- Phone numbers
- Social Security Numbers
- Email addresses
- Credit card numbers
- Medical record numbers
- Patient identifiers
- Addresses
- Zip codes

## Data Formats

### Clinical Record Structure

```json
{
  "patient_records": [
    {
      "demographics": {
        "patient_id": "P001",
        "name": "John Smith",
        "age": 58,
        "gender": "male",
        "race": "white",
        "ethnicity": "non-hispanic",
        "insurance": "private"
      },
      "presentation": {
        "chief_complaint": "chest pain for 1 hour",
        "symptoms": ["chest pain", "shortness of breath"],
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
        "secondary": ["hypertension"],
        "icd_codes": ["I21.9"]
      },
      "treatment": {
        "medications": ["aspirin", "nitroglycerin"],
        "procedures": ["cardiac catheterization"],
        "sequence": ["aspirin", "nitroglycerin", "cardiac catheterization"]
      },
      "outcome": {
        "disposition": "admitted",
        "length_of_stay": 3,
        "mortality": false,
        "readmission": false
      },
      "temporal_data": {
        "arrival_to_diagnosis": 30,
        "diagnosis_to_treatment": 15,
        "treatment_to_discharge": 180
      }
    }
  ]
}
```

### Pattern Definition Format

```json
{
  "pattern_type": "symptom_cluster",
  "frequency": 0.15,
  "demographics": {
    "age_range": [40, 80],
    "gender_distribution": {"male": 0.6, "female": 0.4},
    "risk_factors": ["hypertension", "diabetes"]
  },
  "symptom_clusters": [
    {
      "symptoms": ["chest pain", "shortness of breath"],
      "frequency": 0.4,
      "severity": "high"
    }
  ],
  "diagnoses": [
    {
      "diagnosis": "STEMI",
      "frequency": 0.3,
      "difficulty": "hard"
    }
  ],
  "treatments": [
    {
      "treatment": "aspirin",
      "frequency": 0.9,
      "timing": "immediate"
    }
  ]
}
```

## Usage Examples

### Complete Workflow

```python
from medsim.data import (
    ClinicalDatasetLoader, PatternAnalyzer, ClinicalPatterns,
    DataValidator, DataAnonymizer
)

# 1. Load and validate dataset
loader = ClinicalDatasetLoader("data")
loader.load_dataset("clinical_data.json", "emergency_data")

validator = DataValidator()
records = loader.get_dataset("emergency_data")
validation = validator.validate_dataset(records)

if not validation.is_valid:
    print("Dataset validation failed")
    exit(1)

# 2. Anonymize data
anonymizer = DataAnonymizer()
original_records = [r.__dict__ for r in records]
anonymized_records = anonymizer.anonymize_dataset(original_records)

# 3. Analyze patterns
analyzer = PatternAnalyzer()
analysis_results = analyzer.analyze_dataset(records)

# 4. Generate scenarios
patterns = ClinicalPatterns()
scenario = patterns.generate_scenario_from_pattern(
    patterns.get_random_pattern(specialty="emergency_medicine")
)

print(f"Generated scenario: {scenario['diagnosis']['primary']}")
```

### Performance-Based Difficulty

```python
# Track user performance
user_performance = {
    'diagnosis_accuracy': 0.85,
    'treatment_appropriateness': 0.78,
    'response_time': 0.92
}

# Generate scenario with adaptive difficulty
scenario = patterns.generate_scenario_from_pattern(
    pattern, 
    user_performance=user_performance
)
```

### Continuous Loop Integration

```python
# For continuous simulation loops
def generate_next_patient():
    """Generate next patient for continuous simulation"""
    pattern = patterns.get_random_pattern()
    return patterns.generate_scenario_from_pattern(pattern)

# Use in simulation loop
for shift_hour in range(8):
    patient = generate_next_patient()
    # Process patient in simulation
    # Track performance
    # Adjust difficulty based on performance
```

## Configuration

### Anonymization Configuration

```python
config = AnonymizationConfig(
    preserve_medical_info=True,      # Keep medical details
    preserve_demographics=True,      # Keep age/gender
    preserve_temporal_data=True,     # Keep timing info
    hash_identifiers=True,           # Hash patient IDs
    add_noise_to_ages=True,         # Add age noise
    age_noise_range=2,              # ±2 years
    preserve_geographic_region=False, # Remove location
    preserve_zip_code_prefix=False   # Remove zip codes
)
```

### Validation Configuration

```python
# Custom validation rules
validator = DataValidator()
validator.required_fields = {
    'demographics': ['age', 'gender'],
    'presentation': ['chief_complaint'],
    'diagnosis': ['primary'],
    'treatment': ['medications']
}
```

## Quality Metrics

### Data Quality Score
- **Completeness**: Percentage of required fields filled
- **Consistency**: Logical relationship validation
- **Anomaly Rate**: Statistical outlier detection
- **Duplicate Rate**: Duplicate record identification

### Anonymization Score
- **PII Removal**: Percentage of PII successfully removed
- **Medical Preservation**: Medical information retention
- **Privacy Level**: Degree of anonymization achieved

### Pattern Quality
- **Frequency**: How common the pattern is
- **Confidence**: Statistical confidence in pattern
- **Representativeness**: How well it represents real data

## Best Practices

### Data Preparation
1. **Standardize Formats**: Use consistent field names and data types
2. **Validate Early**: Check data quality before processing
3. **Preserve Context**: Keep medical relevance during anonymization
4. **Document Changes**: Track all data transformations

### Pattern Analysis
1. **Sufficient Data**: Ensure adequate sample sizes for patterns
2. **Cross-Validation**: Validate patterns across different datasets
3. **Medical Review**: Have clinicians review generated patterns
4. **Regular Updates**: Refresh patterns with new data

### Privacy Protection
1. **Comprehensive PII Detection**: Use multiple detection methods
2. **Medical Preservation**: Balance privacy with medical utility
3. **Validation**: Always validate anonymization results
4. **Audit Trail**: Track all anonymization changes

## Troubleshooting

### Common Issues

**Dataset Loading Errors**:
- Check file format compatibility
- Verify required fields are present
- Ensure proper encoding (UTF-8)

**Validation Failures**:
- Review data completeness
- Check for logical inconsistencies
- Verify data types match expectations

**Anonymization Issues**:
- Check PII detection patterns
- Verify medical information preservation
- Review anonymization configuration

**Pattern Analysis Problems**:
- Ensure sufficient data volume
- Check for data quality issues
- Verify pattern detection parameters

### Performance Optimization

**Large Datasets**:
- Use Parquet format for better performance
- Implement batch processing
- Consider data sampling for initial analysis

**Memory Usage**:
- Process data in chunks
- Use generators for large datasets
- Implement data streaming where possible

## Integration with Simulation

The data infrastructure integrates seamlessly with the medical simulation platform:

```python
from medsim.core.simulation import MedicalSimulation
from medsim.data import ClinicalPatterns

# Generate scenario from data patterns
patterns = ClinicalPatterns()
scenario = patterns.generate_scenario_from_pattern(
    patterns.get_random_pattern()
)

# Create simulation with generated scenario
simulation = MedicalSimulation()
simulation.start_simulation(scenario)

# Use in continuous loop
for patient in continuous_patient_generator():
    simulation.start_simulation(patient)
    # Process patient care
    # Track performance
    # Generate next patient
```

This data infrastructure provides the foundation for realistic, data-driven medical simulation scenarios while ensuring privacy and data quality. 