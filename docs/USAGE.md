# Medical Simulation CLI (medsimcli) - Comprehensive Usage Guide

## Table of Contents
1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Basic Usage](#basic-usage)
4. [Patient Management](#patient-management)
5. [Physiological Monitoring](#physiological-monitoring)
6. [Diagnostics](#diagnostics)
7. [Treatment](#treatment)
8. [Disease Progression](#disease-progression)
9. [Drug-Induced Diseases](#drug-induced-diseases)
10. [Time-Sensitive Scenarios](#time-sensitive-scenarios)
11. [Advanced Features](#advanced-features)
12. [Examples](#examples)
13. [Troubleshooting](#troubleshooting)

## Overview

The Medical Simulation CLI (medsimcli) is a comprehensive medical simulation platform that models realistic patient scenarios, disease progression, drug interactions, and clinical decision-making. The system includes:

- **Extensive Symptom Library**: 50+ symptoms across all organ systems
- **Disease Progression Engine**: 30+ diseases with realistic progression patterns
- **Drug Database**: 40+ medications with PK/PD modeling
- **Time-Sensitive Scenarios**: Rapidly progressing conditions requiring immediate intervention
- **Drug-Induced Diseases**: Realistic medication side effects and complications
- **Multi-System Integration**: Cardiovascular, respiratory, neurological, and more

## Installation & Setup

### Prerequisites
- Python 3.13+
- Conda environment manager

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd medsimcli

# Create and activate conda environment
conda create -n medsim python=3.13
conda activate medsim

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation
```bash
# Test basic functionality
python -m medsim --help
```

## Basic Usage

### Starting the CLI
```bash
# Activate environment
conda activate medsim

# Start the CLI
python -m medsim
```

### Getting Help
```bash
# General help
python -m medsim --help

# Command-specific help
python -m medsim create-patient --help
python -m medsim administer-drug --help
```

## Patient Management

### Creating a Patient
```bash
python -m medsim create-patient \
  --id P001 \
  --name "John Doe" \
  --age 45 \
  --gender male \
  --height 175 \
  --weight 80
```

### Discovering Patient Information
```bash
# Calculate BMI
python -m medsim discover-info --type bmi --method calculation

# Add medical history
python -m medsim discover-info --type medical_history --method patient_reported --value "hypertension,diabetes,smoking"

# Add medications
python -m medsim discover-info --type medications --method patient_reported --value "lisinopril,metformin,aspirin"

# Add allergies
python -m medsim discover-info --type allergies --method patient_reported --value "penicillin,sulfa"
```

### Viewing Patient Summary
```bash
python -m medsim show-patient-summary
```

## Physiological Monitoring

### Updating Vital Signs
```bash
# Update multiple vitals
python -m medsim update-vitals \
  --hr 85 \
  --sbp 140 \
  --dbp 90 \
  --rr 16 \
  --temp 37.2 \
  --o2 98

# Update single vital
python -m medsim update-vitals --glucose 120
```

### Viewing Current Vitals
```bash
python -m medsim show-vitals
```

### Adding Symptoms
```bash
# Add a symptom
python -m medsim add-symptom --symptom chest_pain

# Add multiple symptoms
python -m medsim add-symptom --symptom shortness_of_breath
python -m medsim add-symptom --symptom palpitations
```

### Adding Diseases
```bash
# Add acute coronary syndrome
python -m medsim add-disease --disease acute_coronary_syndrome --system cardiovascular --severity 0.7

# Add diabetes mellitus
python -m medsim add-disease --disease diabetes_mellitus --system endocrine --severity 0.5
```

## Diagnostics

### Ordering Lab Tests
```bash
# Order CBC
python -m medsim order-lab --test cbc

# Order comprehensive metabolic panel
python -m medsim order-lab --test cmp

# Order cardiac enzymes
python -m medsim order-lab --test troponin
```

### Completing Lab Tests
```bash
# Complete CBC with results
python -m medsim complete-lab --test cbc --value 12.5

# Complete troponin
python -m medsim complete-lab --test troponin --value 0.8
```

### Ordering Imaging
```bash
# Order chest X-ray
python -m medsim order-imaging --study chest_xray

# Order CT scan
python -m medsim order-imaging --study chest_ct
```

### Completing Imaging
```bash
# Complete chest X-ray with findings
python -m medsim complete-imaging --study chest_xray --findings '{"findings": "pulmonary edema", "impression": "cardiogenic pulmonary edema"}'
```

## Treatment

### Administering Medications
```bash
# Administer aspirin
python -m medsim administer-drug --drug aspirin --dose 325 --route oral

# Administer nitroglycerin
python -m medsim administer-drug --drug nitroglycerin --dose 0.4 --route sublingual

# Administer epinephrine
python -m medsim administer-drug --drug epinephrine --dose 1.0 --route iv
```

### Starting Treatment Protocols
```bash
# Start ACLS protocol
python -m medsim start-protocol --protocol acls

# Start sepsis protocol
python -m medsim start-protocol --protocol sepsis
```

### Monitoring Drug Effects
```bash
# Update simulation to process drug effects
python -m medsim update-simulation

# Check for critical alerts
python -m medsim show-critical-alerts
```

## Disease Progression

### Time-Sensitive Diseases

The system includes several time-sensitive diseases that progress rapidly and require immediate intervention:

#### Aortic Dissection
- **Progression**: Hours to death
- **Symptoms**: Chest pain, syncope, pulse deficit
- **Treatment**: Immediate surgery, blood pressure control

```bash
# Add aortic dissection
python -m medsim add-disease --disease aortic_dissection --system cardiovascular --severity 0.8

# Monitor progression
python -m medsim update-simulation
python -m medsim show-critical-alerts
```

#### Tension Pneumothorax
- **Progression**: Minutes to death
- **Symptoms**: Chest pain, respiratory distress, shock
- **Treatment**: Immediate needle decompression

```bash
# Add tension pneumothorax
python -m medsim add-disease --disease tension_pneumothorax --system respiratory --severity 0.9

# Immediate intervention required
python -m medsim update-simulation
```

#### Cardiac Tamponade
- **Progression**: Hours to death
- **Symptoms**: Chest pain, dyspnea, pulsus paradoxus
- **Treatment**: Immediate pericardiocentesis

### Chronic Disease Progression

#### Diabetes Mellitus
```bash
# Add diabetes
python -m medsim add-disease --disease diabetes_mellitus --system endocrine --severity 0.6

# Monitor for complications
python -m medsim update-simulation
```

#### Rheumatoid Arthritis
```bash
# Add rheumatoid arthritis
python -m medsim add-disease --disease rheumatoid_arthritis --system musculoskeletal --severity 0.5
```

## Drug-Induced Diseases

The system models realistic drug-induced diseases that can occur as medication side effects:

### Drug-Induced Lupus
**Causative Drugs**: Procainamide, Hydralazine, Isoniazid
```bash
# Administer procainamide
python -m medsim administer-drug --drug procainamide --dose 1000 --route iv

# Monitor for lupus symptoms
python -m medsim update-simulation
python -m medsim add-symptom --symptom rash
python -m medsim add-symptom --symptom joint_pain
```

### Stevens-Johnson Syndrome
**Causative Drugs**: Sulfamethoxazole, Phenytoin, Allopurinol
```bash
# Administer sulfamethoxazole
python -m medsim administer-drug --drug sulfamethoxazole --dose 800 --route oral

# Monitor for skin reactions
python -m medsim update-simulation
python -m medsim add-symptom --symptom rash
```

### Serotonin Syndrome
**Causative Drugs**: Sertraline, Venlafaxine, MAOIs
```bash
# Administer sertraline
python -m medsim administer-drug --drug sertraline --dose 50 --route oral

# Monitor for serotonin syndrome
python -m medsim update-simulation
```

### Drug-Induced Liver Disease
**Causative Drugs**: Acetaminophen, Simvastatin, Isoniazid
```bash
# Administer acetaminophen
python -m medsim administer-drug --drug acetaminophen --dose 1000 --route oral

# Monitor liver function
python -m medsim update-simulation
```

### Drug-Induced Kidney Disease
**Causative Drugs**: Ibuprofen, Gentamicin, Lisinopril
```bash
# Administer ibuprofen
python -m medsim administer-drug --drug ibuprofen --dose 400 --route oral

# Monitor renal function
python -m medsim update-simulation
```

## Time-Sensitive Scenarios

### Acute Coronary Syndrome
```bash
# Create patient with chest pain
python -m medsim create-patient --id P002 --name "Jane Smith" --age 58 --gender female --height 165 --weight 70
python -m medsim add-symptom --symptom chest_pain
python -m medsim update-vitals --hr 110 --sbp 160 --dbp 95

# Add ACS
python -m medsim add-disease --disease acute_coronary_syndrome --system cardiovascular --severity 0.8

# Order diagnostics
python -m medsim order-lab --test troponin
python -m medsim order-imaging --study ecg

# Administer treatment
python -m medsim administer-drug --drug aspirin --dose 325 --route oral
python -m medsim administer-drug --drug nitroglycerin --dose 0.4 --route sublingual

# Monitor progression
python -m medsim update-simulation
python -m medsim show-critical-alerts
```

### Sepsis
```bash
# Create septic patient
python -m medsim create-patient --id P003 --name "Bob Johnson" --age 72 --gender male --height 180 --weight 85
python -m medsim add-symptom --symptom fever
python -m medsim add-symptom --symptom shortness_of_breath
python -m medsim update-vitals --hr 120 --sbp 90 --dbp 60 --temp 39.5

# Add sepsis
python -m medsim add-disease --disease sepsis --system infectious --severity 0.7

# Administer antibiotics
python -m medsim administer-drug --drug ceftriaxone --dose 1000 --route iv
python -m medsim administer-drug --drug vancomycin --dose 1000 --route iv

# Monitor for complications
python -m medsim update-simulation
```

## Advanced Features

### Disease Cascades
The system models realistic disease cascades where one disease can cause others:

```bash
# Pneumonia can cause sepsis
python -m medsim add-disease --disease pneumonia --system respiratory --severity 0.6
python -m medsim update-simulation
# System may automatically develop sepsis as complication

# Diabetes can cause diabetic ketoacidosis
python -m medsim add-disease --disease diabetes_mellitus --system endocrine --severity 0.8
python -m medsim update-simulation
# System may automatically develop DKA as complication
```

### Drug Interactions
The system models drug interactions and their effects:

```bash
# Administer warfarin
python -m medsim administer-drug --drug warfarin --dose 5 --route oral

# Administer interacting drug (aspirin)
python -m medsim administer-drug --drug aspirin --dose 325 --route oral

# Monitor for bleeding complications
python -m medsim update-simulation
python -m medsim add-symptom --symptom easy_bruising
```

### Library Searches
```bash
# Search for symptoms
python -m medsim search-library --query chest --type symptoms

# Search for drugs
python -m medsim search-library --query antibiotic --type drugs

# Search for lab tests
python -m medsim search-library --query cardiac --type labs
```

### Viewing Medical Libraries
```bash
# View symptom library
python -m medsim show-library --type symptoms

# View drug library
python -m medsim show-library --type drugs

# View lab tests
python -m medsim show-library --type labs

# View imaging studies
python -m medsim show-library --type imaging

# View treatment protocols
python -m medsim show-library --type protocols
```

## Examples

### Complete Cardiac Scenario
```bash
# 1. Create patient
python -m medsim create-patient --id P004 --name "Alice Brown" --age 65 --gender female --height 160 --weight 75

# 2. Add symptoms
python -m medsim add-symptom --symptom chest_pain
python -m medsim add-symptom --symptom shortness_of_breath
python -m medsim add-symptom --symptom palpitations

# 3. Update vitals
python -m medsim update-vitals --hr 95 --sbp 150 --dbp 90 --rr 20 --o2 94

# 4. Order diagnostics
python -m medsim order-lab --test troponin
python -m medsim order-lab --test cbc
python -m medsim order-imaging --study ecg

# 5. Complete tests
python -m medsim complete-lab --test troponin --value 2.5
python -m medsim complete-lab --test cbc --value 14.2

# 6. Add disease
python -m medsim add-disease --disease acute_coronary_syndrome --system cardiovascular --severity 0.8

# 7. Administer treatment
python -m medsim administer-drug --drug aspirin --dose 325 --route oral
python -m medsim administer-drug --drug nitroglycerin --dose 0.4 --route sublingual

# 8. Monitor progression
python -m medsim update-simulation
python -m medsim show-critical-alerts
python -m medsim show-patient-summary
```

### Drug-Induced Disease Scenario
```bash
# 1. Create patient
python -m medsim create-patient --id P005 --name "Charlie Wilson" --age 45 --gender male --height 175 --weight 80

# 2. Add medical history
python -m medsim discover-info --type medical_history --method patient_reported --value "hypertension,depression"

# 3. Administer medications
python -m medsim administer-drug --drug hydralazine --dose 25 --route oral
python -m medsim administer-drug --drug sertraline --dose 50 --route oral

# 4. Monitor for drug-induced diseases
python -m medsim update-simulation

# 5. Add symptoms of drug-induced lupus
python -m medsim add-symptom --symptom rash
python -m medsim add-symptom --symptom joint_pain
python -m medsim add-symptom --symptom fatigue

# 6. Add symptoms of serotonin syndrome
python -m medsim add-symptom --symptom agitation
python -m medsim add-symptom --symptom diaphoresis

# 7. Monitor progression
python -m medsim update-simulation
python -m medsim show-critical-alerts
```

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure conda environment is activated
conda activate medsim

# Reinstall dependencies
pip install -r requirements.txt
```

#### Command Not Found
```bash
# Check available commands
python -m medsim --help

# Verify installation
python -c "import medsim; print('Installation successful')"
```

#### Patient Not Found
```bash
# Create a patient first
python -m medsim create-patient --id P001 --name "Test Patient" --age 30 --gender male --height 170 --weight 70

# Set as current patient
python -m medsim show-patient-summary
```

#### Drug Not Found
```bash
# Check available drugs
python -m medsim show-library --type drugs

# Search for specific drug
python -m medsim search-library --query aspirin --type drugs
```

### Debug Mode
```bash
# Run with verbose output
python -m medsim --verbose create-patient --id P001 --name "Debug Patient" --age 30 --gender male --height 170 --weight 70
```

### Logging
The system logs all operations to help with debugging:
- Patient creation and updates
- Drug administrations and effects
- Disease progression
- Symptom development
- Critical alerts

## Best Practices

### 1. Patient Safety
- Always verify patient identity before administering medications
- Monitor for drug interactions and contraindications
- Check for allergies before administering medications
- Monitor vital signs after medication administration

### 2. Clinical Decision Making
- Order appropriate diagnostics before treatment
- Consider differential diagnoses
- Monitor for complications and side effects
- Document all interventions and patient responses

### 3. Time-Sensitive Conditions
- Recognize time-sensitive diseases early
- Administer appropriate interventions promptly
- Monitor for rapid progression
- Escalate care when necessary

### 4. Drug Safety
- Verify drug dosages and routes
- Check for drug interactions
- Monitor for adverse effects
- Discontinue offending medications when side effects occur

## Support

For additional support:
- Check the project documentation
- Review example scenarios
- Test with simple cases first
- Use the help system for command syntax

---

*This comprehensive usage guide covers all major features of the medsimcli system. The simulation provides realistic medical scenarios for training and education purposes.* 