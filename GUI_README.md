# Medsim GUI - Medical Simulation Interface

A comprehensive, modern GUI for the Medsim medical simulation platform. This interface provides an intuitive way to manage multiple patients, monitor vitals, order tests, administer treatments, and communicate with patients with advanced medical realism.

## Features

### 🏥 Multi-Patient Management
- **Patient Sidebar**: View all active patients with their status
- **Add New Patients**: Create patients with detailed demographic information
- **Patient Switching**: Seamlessly switch between patients
- **Session Statistics**: Track total patients in current session

### 📊 Real-Time Patient Monitoring
- **Vital Signs Dashboard**: Real-time display of heart rate, blood pressure, respiratory rate, temperature, oxygen saturation, and blood glucose
- **Critical Alerts**: Immediate notification of abnormal vitals
- **Patient Summary**: Comprehensive patient information including demographics, symptoms, and treatment status

### 🫀 Enhanced Monitoring
- **Real-Time ECG**: Live ECG waveform with multiple rhythm patterns (normal, atrial fibrillation, ventricular tachycardia, bradycardia, tachycardia, asystole)
- **Pulse Oximetry**: Realistic SpO2 monitoring with waveform display
- **Drug Interactions**: Comprehensive drug interaction checking and display
- **Patient Timeline**: Complete medical event timeline with color-coded categories

### 🔬 Advanced Diagnostic Tools
- **Laboratory Tests**: Order comprehensive lab panels with detailed test information
- **Advanced Imaging**: Realistic medical imaging with multiple modalities
  - **X-Ray Viewer**: Interactive X-ray images with contrast/brightness controls and radiological findings
  - **CT Scan Viewer**: Multi-slice CT imaging with realistic anatomical representations
  - **Ultrasound Simulator**: Realistic ultrasound images for cardiac, abdominal, and obstetric studies
- **Test Results**: View and track all ordered tests and their results

### 💊 Treatment Management
- **Drug Administration**: Administer medications with proper dosing and route selection
- **Active Treatments**: Monitor ongoing treatments and drug levels
- **Treatment History**: Track all administered treatments
- **Ventilator Management**: Mechanical ventilator settings and waveform monitoring

### 🚨 Emergency Medicine
- **Code Blue Simulation**: Complete cardiac arrest simulation with:
  - Real-time CPR quality monitoring
  - Defibrillator with energy selection
  - Emergency medication administration
  - Code timer and protocol adherence
- **Trauma Protocols**: ABCDE assessment with trauma interventions
- **Critical Care**: Hemodynamic monitoring and vasopressor management
- **Emergency Scenarios**: Pre-built emergency scenarios for training

### 💬 Patient Communication
- **Interactive Dialogue**: Realistic patient conversations with emotional responses
- **Question Types**: Different conversation modes (general, emotional assessment, symptom inquiry, treatment discussion, medical history)
- **Conversation History**: Maintain complete conversation logs

### 📋 Medical Procedures
- **Procedure Simulation**: Step-by-step medical procedures including:
  - Central line insertion
  - Intubation
  - Chest tube insertion
  - Lumbar puncture
  - Paracentesis
  - Thoracentesis
- **Progress Tracking**: Real-time procedure progress monitoring

### 📝 Comprehensive Documentation
- **Progress Notes**: SOAP note documentation with templates
- **Discharge Summaries**: Complete discharge documentation
- **Medication Reconciliation**: Comprehensive medication management
- **Clinical Decision Support**: Evidence-based guidelines and recommendations

### 🎨 Modern UI/UX
- **Minimalist Design**: Clean, professional interface with medical color coding
- **Responsive Layout**: Adapts to different screen sizes
- **Tabbed Interface**: Organized sections for different aspects of patient care
- **Real-Time Updates**: Automatic data refresh every 5 seconds

## Installation

### Prerequisites
- Python 3.8 or higher
- Conda environment (recommended)

### Setup
1. **Activate your conda environment**:
   ```bash
   conda activate medsim
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the GUI**:
   ```bash
   python run_gui.py
   ```

## Usage Guide

### Getting Started

1. **Launch the Application**
   - Run `python run_gui.py`
   - The main window will open with a sidebar and dashboard

2. **Add Your First Patient**
   - Click the "+ Add Patient" button in the sidebar
   - Fill in patient details (ID, name, age, gender, height, weight)
   - Click "Add Patient" to create the patient

3. **Select a Patient**
   - Click on any patient in the sidebar to view their details
   - The dashboard will update with patient-specific information

### Enhanced Monitoring

#### ECG Monitoring
- **Real-Time Waveform**: View live ECG with realistic patterns
- **Rhythm Recognition**: Automatic rhythm detection based on heart rate
- **Multiple Patterns**: Normal sinus rhythm, atrial fibrillation, ventricular tachycardia, bradycardia, tachycardia, asystole
- **Grid Display**: Standard ECG grid for measurements

#### Pulse Oximetry
- **SpO2 Monitoring**: Real-time oxygen saturation display
- **Pulse Rate**: Concurrent heart rate monitoring
- **Waveform Display**: Realistic pulse waveform
- **Color Coding**: Visual alerts for low oxygen levels

### Advanced Imaging

#### X-Ray Viewer
- **Multiple Studies**: Chest, abdominal, and spine X-rays
- **Pathological Findings**: Pneumonia, pneumothorax, CHF, COPD, bowel obstruction, free air, fractures
- **Image Controls**: Contrast and brightness adjustment
- **Radiological Findings**: Detailed interpretation for each study

#### CT Scan Viewer
- **Multi-Slice Imaging**: Navigate through CT slices
- **Multiple Studies**: Head, chest, and abdominal CT
- **Pathological Findings**: Hemorrhage, masses, pulmonary embolism, pneumonia, appendicitis
- **Realistic Rendering**: Anatomically accurate representations

#### Ultrasound Simulator
- **Multiple Modalities**: Cardiac echo, abdominal, obstetric ultrasound
- **Realistic Images**: Anatomically correct ultrasound patterns
- **Depth Control**: Adjustable imaging depth
- **Pathological Findings**: CHF, gallstones, aortic aneurysm, normal pregnancy, ectopic pregnancy

### Emergency Medicine

#### Code Blue Simulation
1. **Start Code Blue**: Click "Start Code Blue" to begin simulation
2. **CPR Quality**: Monitor compression rate, depth, and ventilation rate
3. **Defibrillation**: Charge and deliver shocks with energy selection
4. **Medications**: Administer emergency medications (epinephrine, amiodarone, etc.)
5. **Timer**: Track elapsed time during resuscitation

#### Trauma Protocols
1. **Primary Survey**: Complete ABCDE assessment
2. **Interventions**: Perform trauma interventions (chest tube, IV access, etc.)
3. **Trauma Score**: Calculate and interpret trauma scores
4. **Documentation**: Record all interventions and findings

#### Critical Care
1. **Hemodynamic Monitoring**: Monitor CVP, PAP, cardiac output
2. **Vasopressor Management**: Start and titrate vasopressors
3. **Sedation**: Manage sedation and analgesia
4. **Ventilator Settings**: Adjust mechanical ventilation parameters

### Medical Procedures

#### Procedure Simulation
1. **Select Procedure**: Choose from available procedures
2. **Step-by-Step**: Follow procedure steps in order
3. **Progress Tracking**: Monitor completion progress
4. **Documentation**: Record procedure details

### Documentation

#### Progress Notes
1. **SOAP Format**: Document in Subjective, Objective, Assessment, Plan format
2. **Templates**: Load pre-built templates for common scenarios
3. **Save Notes**: Save progress notes to patient record
4. **Timestamps**: Automatic date and time stamping

#### Discharge Summary
1. **Admission Information**: Document admission diagnosis and dates
2. **Hospital Course**: Summarize hospital stay and interventions
3. **Discharge Planning**: Document discharge medications and follow-up
4. **Generate Summary**: Create comprehensive discharge summary

#### Medication Reconciliation
1. **Medication List**: View all patient medications
2. **Status Tracking**: Track medication continuation, discontinuation, or changes
3. **Reconciliation**: Complete medication reconciliation process
4. **Documentation**: Record all medication decisions

#### Clinical Decision Support
1. **Condition Selection**: Choose medical condition for guidance
2. **Guidelines**: View evidence-based clinical guidelines
3. **Recommendations**: Get specific clinical recommendations
4. **Case Analysis**: Analyze patient case against guidelines

### Real-Time Monitoring

#### Vital Signs
- **Heart Rate**: Normal range 60-100 bpm
- **Blood Pressure**: Normal <120/80 mmHg
- **Respiratory Rate**: Normal 12-20/min
- **Temperature**: Normal 36.5-37.5°C
- **Oxygen Saturation**: Normal >95%
- **Blood Glucose**: Normal 70-140 mg/dL

#### Alerts
- Critical vitals are highlighted in red
- Warning levels shown in orange
- Normal values displayed in green

### Quick Actions

The dashboard provides quick access to common tasks:
- **Update Vitals**: Manually refresh patient data
- **Talk to Patient**: Open communication dialog
- **Order Lab Test**: Quick lab ordering
- **Order Imaging**: Quick imaging ordering
- **Administer Drug**: Quick medication administration
- **Add Symptom**: Add new symptoms to patient

## Technical Details

### Architecture
- **PySide6**: Modern Qt-based GUI framework
- **Modular Design**: Separate widgets for different functions
- **Real-Time Updates**: Timer-based data refresh
- **Session Management**: Integrated with core session manager

### Data Integration
- **Physiological Engine**: Real-time vital signs and disease progression
- **Diagnostic System**: Lab tests and imaging studies
- **Treatment Engine**: Drug administration and monitoring
- **Dialogue Engine**: Patient communication and responses

### Enhanced Features
- **ECG Simulation**: Realistic cardiac rhythm generation
- **Imaging Rendering**: Anatomically accurate medical images
- **Emergency Protocols**: Evidence-based emergency medicine
- **Documentation System**: Comprehensive medical documentation

### Color Coding
- **Blue (#4f8cff)**: Primary actions and information
- **Green (#66bb6a)**: Success and communication
- **Orange (#ffa726)**: Warnings and medications
- **Red (#ff4f4f)**: Critical alerts and symptoms
- **Yellow (#ffff00)**: ECG and monitoring displays

## Troubleshooting

### Common Issues

1. **GUI won't start**
   - Ensure PySide6 is installed: `pip install PySide6`
   - Check Python version (3.8+ required)
   - Verify conda environment is activated

2. **No patients showing**
   - Sample patients are automatically added on startup
   - Use "Add Patient" to create new patients
   - Check console for error messages

3. **Actions not working**
   - Ensure a patient is selected first
   - Check that all engines are properly initialized
   - Verify patient ID exists in session manager

4. **Performance issues**
   - Reduce update frequency in the timer
   - Close unnecessary tabs
   - Restart the application if needed

### Error Messages
- **"Please select a patient first"**: Click on a patient in the sidebar
- **"Import error"**: Install missing dependencies
- **"Engine not found"**: Ensure all core modules are available

## Development

### Adding New Features
1. Create new widget classes in appropriate files
2. Add widgets to the main dashboard in `medsim/gui/app.py`
3. Connect signals and slots for interactivity
4. Update the color palette for consistency

### Customization
- Modify colors in the color palette constants
- Adjust update frequency in the timer
- Add new patient fields in the add dialog
- Extend conversation types in the dialogue system

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the console output for error messages
3. Ensure all dependencies are properly installed
4. Verify the conda environment is activated

The GUI provides a comprehensive, professional-grade interface for medical simulation training, combining real-time patient monitoring with interactive diagnostic and treatment capabilities, advanced emergency medicine protocols, and comprehensive documentation systems. 