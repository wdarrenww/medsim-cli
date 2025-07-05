# **Python CLI Medical Simulator**

A professional-grade, CLI-based medical simulation platform designed to provide a high-fidelity training experience for medical students, residents, and healthcare professionals. This simulator leverages dynamic physiological modeling and an advanced, text-based interface to create realistic and challenging clinical encounters.

## **Vision**

Our vision is to revolutionize medical education by providing an accessible, scalable, and deeply realistic simulation tool. We aim to bridge the gap between theoretical knowledge and practical application, allowing learners to develop critical thinking, diagnostic reasoning, and clinical decision-making skills in a safe, repeatable, and measurable environment.

## **Key Features**

This platform is being built with a comprehensive feature set designed to simulate the complete clinical experience.

### **1\. Core Engine & Architecture**

* **Discrete-Event Simulation Engine:** Manages the progression of time and complex patient state changes with high fidelity.  
* **Modular & Extensible Architecture:** A plugin-based system allows for the easy addition of new medical specialties, patient cases, and interventions.  
* **Cross-Platform Compatibility:** Fully compatible with Windows, macOS, and Linux.  
* **Headless Operation & API:** Enables remote access, automated testing, and seamless integration with other educational systems.

### **2\. Patient Simulation**

* **Comprehensive Patient Profiles:** Includes rich demographics, detailed medical/family history, and social determinants of health.  
* **Dynamic Physiological Engine:** A multi-organ system model (Cardiovascular, Respiratory, Renal, Endocrine, Neurological) that responds realistically to diseases and treatments.  
* **Advanced Pharmacology Model:** Simulates pharmacokinetics and pharmacodynamics for a vast library of medications, including drug-drug and drug-disease interactions.  
* **AI-Powered Patient Dialogue:** A Natural Language Processing (NLP) module allows for open-ended, realistic conversations with virtual patients.

### **3\. Clinical Activities & Interventions**

* **Comprehensive Diagnostics:** Order and interpret a wide array of laboratory tests, medical imaging (with text-based reports and ASCII-art visuals), and microbiology.  
* **Realistic Physical Examinations:** Perform virtual physical exams with detailed findings based on the patient's underlying condition.  
* **Treatments & Procedures:** Administer medications, perform procedures, and request specialty consultations.

### **4\. Educational & Assessment Tools**

* **Extensive Case Library:** A large, peer-reviewed library of cases covering numerous specialties and difficulty levels.  
* **Powerful Case Authoring Tool:** Allows educators to create, modify, and script new clinical scenarios with custom learning objectives.  
* **Data-Driven** Scenario **Generation:** Programmatically generates new, unique patient cases from anonymized clinical data models.  
* **Comprehensive Performance Analytics:** Tracks and scores user performance on diagnostic accuracy, clinical reasoning, patient safety, and resource utilization.  
* **AI-Powered Tutoring:** An intelligent tutor provides adaptive hints and uses Socratic questioning to guide learners.

### **5\. Commercial & Enterprise Features**

* **Institutional Dashboards:** Web-based dashboards for faculty to manage cohorts, assign cases, and track longitudinal student performance.  
* **LMS Integration:** LTI compliance for seamless integration with Canvas, Moodle, Blackboard, and other Learning Management Systems.  
* **Role-Based Access Control:** Granular permissions for students, faculty, and administrators.  
* **Security & Compliance:** Designed with data security and the principles of HIPAA in mind to ensure institutional trust.

## **Development Roadmap**

This project is being developed in three major phases, each designed to build upon the last and deliver incremental value.

### **Phase 1: The Core Clinical Encounter (MVP)** ✅ **COMPLETED**

* **Goal:** Deliver a stable, engaging simulation of a single patient encounter to validate the core learning experience.  
* **Status:** ✅ **COMPLETED**  
* **Key Deliverables:**  
  * ✅ Functional Discrete-Event Simulation Core using SimPy.
  * ✅ Basic CLI for user interaction with rich interface.
  * ✅ Ability to save/load a simulation session.
  * ✅ Simplified physiological model (Cardiovascular, Respiratory).
  * ✅ Scripted patient dialogue system.
  * ✅ A limited set of core diagnostic tests and medications.
  * ✅ A curated library of 5-10 high-quality scenarios in a single specialty.
  * ✅ A basic end-of-case performance summary.

### **Phase 2: The Educational Platform (Commercial Viability)**

* **Goal:** Build the essential tools for educators to create, manage, and assess learning, making the platform ready for institutional adoption.  
* **Status:** Not Started  
* **Key Deliverables:**  
  * **Scenario Authoring Tool:** The cornerstone feature, allowing faculty to create and customize cases.  
  * **Comprehensive Scoring & Debriefing:** Implement detailed performance metrics and in-depth feedback reports.  
  * **Expanded Physiological & Pharmacology Engines:** Model all major organ systems and complex drug interactions.  
  * **Modular, Plugin-Based Architecture:** Refactor for easy extensibility.  
  * **Institutional Dashboards (v1):** Web-based tools for faculty to manage students and assignments.  
  * **Role-Based Access Control.**  
  * **Greatly Expanded Case and Diagnostics Library.**

### **Phase 3: The Intelligent Health System Simulator (Market Leadership)**

* **Goal:** Evolve the product into an intelligent, adaptive learning ecosystem that provides personalized learning and deep integration capabilities.  
* **Status:** Not Started  
* **Key Deliverables:**  
  * **AI-Powered Tutoring System:** An intelligent agent to guide learners with adaptive hints and Socratic questioning.  
  * **AI-Powered Patient Dialogue (NLP):** Enable dynamic, unscripted patient conversations.  
  * **Data-Driven Scenario Generation:** Automatically create novel cases from data models.  
  * **LMS Integration (LTI Compliance).**  
  * **Cloud-Native Architecture:** Ensure high availability and scalability for large institutions.  
  * **Longitudinal Performance Analytics:** Track user growth and competency development over time.

## **Installation & Usage**

### **Prerequisites**

* Python 3.9+  
* Pip

### **Installation**

```bash
# Clone the repository
git clone <repository-url>
cd medsimcli

# Install in development mode
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

### **Running the Simulator**

```bash
# Run the medical simulator
python -m medsim

# Or if installed with entry point
medsim
```

### **Available Commands**

Once the simulator is running, you'll have access to the following commands:

* **help** - Show available commands
* **start** - Start a new simulation session
* **patient** - View patient information
* **vitals** - View or update patient vital signs
* **symptoms** - View or add patient symptoms
* **medications** - View or add patient medications
* **status** - Show simulation status
* **step** - Advance simulation by one time step
* **pause** - Pause simulation
* **reset** - Reset simulation
* **quit** - Exit simulator

### **Example Session**

```
Welcome to the Medical Simulator CLI
Professional-grade medical simulation platform

medsim: start
✓ Simulation started with patient: John Smith
✓ Patient ID: P001

medsim: patient
┌─────────────────────────────────────┐
│ Patient Information - John Smith    │
├─────────────────┬───────────────────┤
│ ID              │ P001              │
│ Name            │ John Smith        │
│ Age             │ 58                │
│ Gender          │ Male              │
│ Timestamp       │ 2024-01-15 10:30 │
└─────────────────┴───────────────────┘

medsim: vitals
View or Update vitals?: update
Update Vital Signs
Enter new values (press Enter to skip):
Blood Pressure (Systolic): 140
Blood Pressure (Diastolic): 90
Heart Rate (bpm): 85
Respiratory Rate (breaths/min): 18
Temperature (°F): 98.6
Oxygen Saturation (%): 98
✓ Vital signs updated successfully
```

### **Testing**

```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=medsim tests/
```

## **Architecture**

The Phase 1 implementation includes:

### **Core Simulation Engine (`medsim/core/simulation.py`)**
- **MedicalSimulation**: Main simulation engine using SimPy for discrete-event simulation
- **PatientState**: Data class representing patient state with vital signs, symptoms, medications, etc.
- Event scheduling and processing system
- Time management and simulation control

### **CLI Interface (`medsim/cli/interface.py`)**
- **SimulatorCLI**: Rich command-line interface using Typer and Rich
- Interactive command system with validation
- Beautiful table and panel displays
- Comprehensive help system

### **Key Features Implemented**

#### **Core Engine & Architecture**
- ✅ **Discrete-Event Simulation Engine**: Complete SimPy-based simulation with time management and event scheduling
- ✅ **Functional CLI**: Rich command-line interface with comprehensive commands and beautiful displays
- ✅ **Session Management**: Save and load simulation states with JSON serialization
- ✅ **Modular Architecture**: Well-organized codebase ready for Phase 2 expansion

#### **Patient Simulation**
- ✅ **Hardcoded Patient Profiles**: Rich patient data with demographics, medical history, and social determinants
- ✅ **Simplified Physiological Model**: Cardiovascular, Respiratory, and Renal systems with realistic parameter responses
- ✅ **Scripted Dialogue System**: Pre-written patient responses based on question types and context

#### **Clinical Activities & Interventions**
- ✅ **Limited Core Diagnostics**: 30+ laboratory tests (CBC, BMP, Cardiac Enzymes, etc.) with realistic results
- ✅ **Imaging Modalities**: 15+ imaging studies (CXR, CT, MRI, Ultrasound, ECG) with text-based reports
- ✅ **Physical Examination**: Basic exam commands with context-sensitive findings
- ✅ **Curated Formulary**: 20+ essential medications with dosing, effects, and contraindications

#### **Educational & Assessment Features**
- ✅ **High-Quality Scenarios**: 10 meticulously crafted Emergency Medicine scenarios with learning objectives
- ✅ **Performance Assessment**: Comprehensive end-of-case summary with pass/fail and optimal/suboptimal outcomes
- ✅ **Action Tracking**: Records user actions and compares against optimal clinical pathways
- ✅ **Time Management**: Tracks scenario completion time and efficiency

#### **Additional Features**
- ✅ **Rich CLI Interface**: Tabular displays, color-coded output, and intuitive command structure
- ✅ **Comprehensive Testing**: Unit tests for core simulation functionality
- ✅ **Documentation**: Complete implementation with clear architecture and usage examples

This Phase 1 implementation provides a solid foundation for the medical simulator with a functional simulation engine and user-friendly CLI interface, ready for the next phase of development.  