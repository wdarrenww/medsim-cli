# Enhanced Patient & Physiological Systems

## Overview

The Medical Simulator now includes advanced patient simulation and physiological modeling systems that provide realistic, comprehensive patient encounters. These systems work together to create dynamic, responsive patient experiences that reflect real-world clinical complexity.

## Enhanced Patient System

### Patient Profile Components

#### 1. Demographics & Physical Characteristics
- **Basic Demographics**: Age, gender, race/ethnicity, date of birth
- **Physical Measurements**: Height, weight, BMI calculation
- **Communication Preferences**: Language, hearing/vision impairments, interpreter needs

#### 2. Personality & Communication Style
- **Personality Types**: Type A (competitive, time-conscious), Type B (relaxed, patient), Introvert, Extrovert, Analytical, Emotional
- **Communication Style**: Direct, indirect, detailed, brief
- **Health Literacy**: Low, adequate, high
- **Trust in Healthcare**: Low, moderate, high
- **Decision-Making Style**: Collaborative, autonomous, dependent

#### 3. Social History & Determinants
- **Occupation & Education**: Job type, education level
- **Living Situation**: Marital status, living arrangement, insurance status
- **Social Determinants**: Poverty, food insecurity, housing insecurity, transportation barriers, health literacy, language barriers, discrimination, social isolation
- **Support System**: Family, friends, community resources
- **Barriers to Care**: Financial, transportation, cultural, language

#### 4. Lifestyle Factors
- **Substance Use**: Smoking status, alcohol use, drug use
- **Health Behaviors**: Exercise frequency, diet quality, sleep quality, stress level
- **Risk Factors**: Automatically calculated based on demographics and behaviors

#### 5. Medical History
- **Allergies**: Medication and environmental allergies
- **Current Medications**: Active prescriptions with dosing
- **Medical Conditions**: Chronic and acute conditions
- **Surgical History**: Previous procedures and dates
- **Family History**: Conditions, age of onset, deceased relatives

#### 6. Emotional & Cognitive State
- **Emotional States**: Calm, anxious, fearful, angry, depressed, confused, cooperative, uncooperative
- **Pain Level**: 0-10 scale
- **Anxiety Level**: 0-10 scale
- **Cognitive Status**: Alert, confused, lethargic, unresponsive

### Patient Generation

The system includes a `PatientProfileGenerator` that creates realistic patient profiles:

```python
from medsim.core.patient import PatientProfileGenerator

generator = PatientProfileGenerator()

# Generate adult patient
patient = generator.generate_patient(age=45, gender="female")

# Generate pediatric patient
pediatric_patient = generator.generate_pediatric_patient(age=8)

# Generate geriatric patient
geriatric_patient = generator.generate_geriatric_patient(age=75)
```

### Patient Interaction Methods

```python
# Update emotional state
patient.update_emotional_state(EmotionalState.ANXIOUS)

# Update pain level
patient.update_pain_level(7)  # 0-10 scale

# Update anxiety level
patient.update_anxiety_level(5)  # 0-10 scale

# Check for social determinants
if patient.has_social_determinant(SocialDeterminant.POVERTY):
    print("Patient has poverty-related barriers")

# Get risk factors
risk_factors = patient.get_risk_factors()
```

## Enhanced Physiological Engine

### Multi-Organ System Modeling

The physiological engine models 10 major organ systems:

#### 1. Cardiovascular System
- **Hemodynamics**: Cardiac output, stroke volume, heart rate, blood pressure
- **Cardiac Function**: Ejection fraction, cardiac index, systemic vascular resistance
- **Rhythm**: Normal sinus, conduction abnormalities
- **Stress Response**: Increased heart rate, blood pressure, cardiac output

#### 2. Respiratory System
- **Ventilation**: Respiratory rate, tidal volume, minute ventilation, vital capacity
- **Gas Exchange**: Oxygen saturation, PaO2, PaCO2, pH
- **Mechanics**: Peak inspiratory pressure, PEEP
- **Stress Response**: Increased respiratory rate and minute ventilation

#### 3. Renal System
- **Function**: Glomerular filtration rate, creatinine, BUN, urine output
- **Electrolytes**: Sodium, potassium, chloride, bicarbonate
- **Acid-Base**: pH, base excess
- **Stress Response**: Reduced urine output and GFR

#### 4. Endocrine System
- **Glucose Metabolism**: Blood glucose, HbA1c, insulin, glucagon
- **Thyroid Function**: TSH, free T4, free T3
- **Adrenal Function**: Cortisol, aldosterone
- **Stress Response**: Increased cortisol and glucose

#### 5. Neurological System
- **Consciousness**: Glasgow Coma Scale, consciousness level, orientation
- **Cognitive Function**: Memory, attention, language
- **Motor Function**: Muscle strength, reflexes
- **Sensory Function**: Sensation, vision, hearing
- **Stress Response**: Anxiety, attention changes

#### 6. Gastrointestinal System
- **Motility**: Bowel sounds, bowel movements
- **Liver Function**: ALT, AST, alkaline phosphatase, bilirubin, albumin
- **Pancreas**: Amylase, lipase
- **Symptoms**: Nausea, vomiting, abdominal pain, diarrhea
- **Stress Response**: Nausea, abdominal pain

#### 7. Hematological System
- **Red Blood Cells**: Hemoglobin, hematocrit, RBC count, MCV, MCH, MCHC
- **White Blood Cells**: WBC count, neutrophils, lymphocytes, monocytes, eosinophils, basophils
- **Platelets**: Platelet count
- **Coagulation**: PT, INR, PTT, fibrinogen
- **Stress Response**: Increased WBC count and neutrophils

#### 8. Immune System
- **Inflammatory Markers**: CRP, ESR, ferritin
- **Cytokines**: IL-6, TNF-alpha
- **Immune Function**: CD4 count, CD8 count, NK cells
- **Stress Response**: Increased CRP and IL-6

#### 9. Hepatic System
- **Liver Function Tests**: ALT, AST, alkaline phosphatase, GGT, bilirubin, albumin
- **Synthetic Function**: PT, INR, factor VII
- **Stress Response**: Elevated liver enzymes

#### 10. Musculoskeletal System
- **Muscle Function**: Strength in upper/lower extremities, grip
- **Joint Function**: Range of motion assessment
- **Bone Health**: Bone density, calcium, vitamin D
- **Symptoms**: Pain, stiffness, weakness
- **Stress Response**: Generalized pain

### Disease Modeling

The system supports dynamic disease progression:

```python
# Add diseases with severity
engine.add_disease("Hypertension", severity=0.8)
engine.add_disease("Diabetes", severity=0.6)
engine.add_disease("Pneumonia", severity=0.9)

# Remove diseases
engine.remove_disease("Hypertension")

# Get disease effects
diseases = engine.diseases
```

### Medication Interactions

The system models realistic medication effects:

```python
# Beta blockers
if "propranolol" in med_name:
    heart_rate -= 10
    blood_pressure_systolic -= 10

# ACE inhibitors
elif "lisinopril" in med_name:
    blood_pressure_systolic -= 15
    blood_pressure_diastolic -= 8

# Diuretics
elif "furosemide" in med_name:
    urine_output += 0.5
    sodium -= 2
    potassium -= 0.3
```

### Cross-System Interactions

The engine models realistic physiological interactions:

```python
# Cardiovascular-respiratory coupling
if cardiac_output < 3.0:
    oxygen_saturation -= 2

# Renal-cardiovascular coupling
if mean_arterial_pressure < 60:
    glomerular_filtration_rate -= 20
    urine_output -= 0.5

# Endocrine-cardiovascular coupling
if cortisol > 25:
    blood_pressure_systolic += 5
    heart_rate += 5
```

## CLI Integration

### New Commands

#### Enhanced Patient Commands
```bash
medsim> patient_enhanced
# View comprehensive patient profile including personality, social determinants, and emotional state
```

#### Physiological System Commands
```bash
medsim> physiology
# View detailed status of all organ systems

medsim> labs
# View current laboratory values with normal ranges and abnormal flags

medsim> diseases
# View active diseases and their severity

medsim> add_disease
# Add a disease to the patient with specified severity

medsim> remove_disease
# Remove a disease from the patient
```

### Example Session

```bash
medsim> start
✓ Simulation started with enhanced patient: Sarah Johnson
✓ Patient ID: P1234

medsim> patient_enhanced
┌─────────────────────────────────────┐
│ Enhanced Patient Profile - Sarah    │
├─────────────────┬───────────────────┤
│ Demographics    │ Age: 45, Female   │
│ Personality     │ Type: type_b      │
│ Social History  │ Teacher, College  │
│ Emotional State │ Calm, Pain: 2/10  │
│ Risk Factors    │ obesity, smoking  │
└─────────────────┴───────────────────┘

medsim> physiology
┌─────────────────────────────────────┐
│ Physiological System Status         │
├─────────────────┬─────────┬────────┤
│ Cardiovascular  │ normal  │ HR: 80 │
│ Respiratory     │ normal  │ RR: 16 │
│ Renal           │ normal  │ GFR: 100│
│ Endocrine       │ normal  │ Glu: 100│
└─────────────────┴─────────┴────────┘

medsim> add_disease
Available diseases:
1. Hypertension
2. Diabetes
3. Heart Failure
...
Select disease (1-9): 1
Enter severity (0.1-1.0): 0.7
✅ Added Hypertension with severity 0.70

medsim> physiology
┌─────────────────────────────────────┐
│ Physiological System Status         │
├─────────────────┬─────────┬────────┤
│ Cardiovascular  │ moderate│ HR: 95 │
│ Respiratory     │ normal  │ RR: 16 │
│ Renal           │ normal  │ GFR: 100│
└─────────────────┴─────────┴────────┘

medsim> labs
┌─────────────────────────────────────┐
│ Laboratory Values                   │
├─────────────────┬─────────┬────────┤
│ SODIUM          │ 140.0   │ normal │
│ POTASSIUM       │ 4.0     │ normal │
│ GLUCOSE         │ 100.0   │ normal │
│ HEMOGLOBIN      │ 14.0    │ normal │
└─────────────────┴─────────┴────────┘
```

## API Integration

### Enhanced Patient API

```python
from medsim.api import MedicalSimulatorAPI

api = MedicalSimulatorAPI()

# Get enhanced patient profile
patient = api.get_patient()
print(f"Patient: {patient.name}, Age: {patient.age}")
print(f"Personality: {patient.personality.personality_type.value}")
print(f"Emotional State: {patient.emotional_state.value}")

# Update patient state
api.update_patient_emotional_state("anxious")
api.update_patient_pain_level(8)
```

### Physiological API

```python
# Get physiological status
status = api.get_physiological_status()
print(f"Cardiovascular: {status['system_status']['cardiovascular']['disease_state']}")

# Add disease
api.add_disease("Diabetes", severity=0.6)

# Get lab values
labs = api.get_lab_values()
abnormal = api.get_abnormal_lab_values()
```

## Configuration

### Patient Generation Settings

```python
# Configure patient generator
generator = PatientProfileGenerator()

# Generate with specific characteristics
patient = generator.generate_patient(
    age=45,
    gender="female",
    personality_type=PersonalityType.TYPE_A,
    social_determinants=[SocialDeterminant.POVERTY]
)
```

### Physiological Engine Settings

```python
# Configure physiological engine
engine = EnhancedPhysiologicalEngine()

# Set baseline parameters
engine.cardiovascular.heart_rate = 75
engine.respiratory.respiratory_rate = 14

# Add baseline conditions
engine.add_disease("Hypertension", severity=0.3)
```

## Best Practices

### 1. Realistic Patient Profiles
- Use appropriate age ranges for different scenarios
- Include relevant social determinants for the case
- Match personality type to scenario requirements

### 2. Disease Progression
- Start with mild severity and progress gradually
- Consider cross-system effects when adding diseases
- Monitor lab values for realistic changes

### 3. Medication Management
- Consider drug interactions when adding medications
- Monitor for side effects and complications
- Adjust dosing based on patient characteristics

### 4. Stress Management
- Use stress levels to drive physiological changes
- Consider patient personality in stress responses
- Monitor emotional state changes

## Troubleshooting

### Common Issues

1. **Patient Not Loading**: Ensure enhanced patient system is properly initialized
2. **Physiological Values Not Updating**: Check that physiological engine is running
3. **Diseases Not Taking Effect**: Verify disease severity is > 0.1
4. **Lab Values Not Changing**: Ensure cross-system interactions are enabled

### Debug Commands

```bash
# Check system status
medsim> physiology

# View all lab values
medsim> labs

# Check active diseases
medsim> diseases

# Reset simulation
medsim> reset
```

## Future Enhancements

### Planned Features

1. **Advanced Disease Progression**: Time-based disease evolution
2. **Medication Pharmacokinetics**: Detailed drug metabolism modeling
3. **Patient Response Modeling**: Individualized treatment responses
4. **Advanced Lab Interpretation**: Clinical correlation and recommendations
5. **Real-time Monitoring**: Continuous vital sign trending
6. **Predictive Analytics**: Outcome prediction based on interventions

### Integration Opportunities

1. **AI-Powered Dialogue**: Natural language patient interactions
2. **Virtual Reality**: 3D patient visualization
3. **Remote Monitoring**: Real-time data transmission
4. **Clinical Decision Support**: Evidence-based recommendations
5. **Performance Analytics**: Detailed learning assessment 