"""
Emergency Medicine Specialty Plugin
demonstrates plugin system functionality
"""

from typing import Dict, List, Any
from ...core.plugins import SpecialtyPlugin, PluginMetadata

class EmergencyMedicinePlugin(SpecialtyPlugin):
    """emergency medicine specialty plugin"""
    
    def __init__(self):
        metadata = PluginMetadata(
            name="Emergency Medicine",
            version="1.0.0",
            description="Emergency Medicine specialty with trauma, cardiac, and critical care scenarios",
            author="Medical Simulator Team",
            category="specialty",
            tags=["emergency", "trauma", "cardiac", "critical_care"],
            config_schema={
                "trauma_enabled": {"type": bool},
                "cardiac_enabled": {"type": bool},
                "pediatric_enabled": {"type": bool}
            }
        )
        
        config = {
            "trauma_enabled": True,
            "cardiac_enabled": True,
            "pediatric_enabled": True
        }
        
        super().__init__(metadata, config)
    
    def _load_specialty_content(self):
        """load emergency medicine content"""
        
        # emergency medicine scenarios
        self.scenarios = [
            {
                "id": "em_trauma_01",
                "title": "Motor Vehicle Accident - Multiple Trauma",
                "description": "25-year-old male involved in high-speed MVA with multiple injuries",
                "difficulty": "advanced",
                "learning_objectives": [
                    "Primary and secondary trauma assessment",
                    "Airway management in trauma",
                    "Hemorrhage control",
                    "Shock management"
                ],
                "patient_profile": {
                    "age": 25,
                    "gender": "male",
                    "chief_complaint": "Multiple injuries from MVA",
                    "vitals": {
                        "blood_pressure_systolic": 90,
                        "blood_pressure_diastolic": 60,
                        "heart_rate": 120,
                        "respiratory_rate": 24,
                        "temperature": 36.8,
                        "oxygen_saturation": 92
                    }
                }
            },
            {
                "id": "em_cardiac_01",
                "title": "Acute Myocardial Infarction",
                "description": "58-year-old male with chest pain and ST elevation",
                "difficulty": "intermediate",
                "learning_objectives": [
                    "ECG interpretation",
                    "STEMI recognition and management",
                    "Cardiac catheterization activation",
                    "Medication administration"
                ],
                "patient_profile": {
                    "age": 58,
                    "gender": "male",
                    "chief_complaint": "Chest pain for 2 hours",
                    "vitals": {
                        "blood_pressure_systolic": 140,
                        "blood_pressure_diastolic": 90,
                        "heart_rate": 85,
                        "respiratory_rate": 18,
                        "temperature": 37.0,
                        "oxygen_saturation": 98
                    }
                }
            },
            {
                "id": "em_pediatric_01",
                "title": "Pediatric Respiratory Distress",
                "description": "3-year-old child with severe respiratory distress",
                "difficulty": "intermediate",
                "learning_objectives": [
                    "Pediatric assessment",
                    "Respiratory distress management",
                    "Pediatric medication dosing",
                    "Family communication"
                ],
                "patient_profile": {
                    "age": 3,
                    "gender": "female",
                    "chief_complaint": "Difficulty breathing",
                    "vitals": {
                        "blood_pressure_systolic": 95,
                        "blood_pressure_diastolic": 65,
                        "heart_rate": 140,
                        "respiratory_rate": 35,
                        "temperature": 38.5,
                        "oxygen_saturation": 88
                    }
                }
            }
        ]
        
        # emergency medicine procedures
        self.procedures = [
            {
                "name": "Endotracheal Intubation",
                "category": "Airway",
                "description": "Orotracheal intubation for airway management",
                "indications": ["Respiratory failure", "Airway protection", "General anesthesia"],
                "contraindications": ["Facial trauma", "Cervical spine injury"],
                "equipment": ["Laryngoscope", "Endotracheal tube", "Stylet", "Syringe"],
                "steps": [
                    "Pre-oxygenate patient",
                    "Position patient",
                    "Insert laryngoscope",
                    "Visualize vocal cords",
                    "Insert endotracheal tube",
                    "Confirm placement"
                ],
                "complications": ["Esophageal intubation", "Dental trauma", "Vocal cord injury"],
                "success_rate": 0.95
            },
            {
                "name": "Central Line Insertion",
                "category": "Vascular",
                "description": "Central venous catheter insertion",
                "indications": ["Hemodynamic monitoring", "Vasopressor administration", "Dialysis access"],
                "contraindications": ["Infection at site", "Coagulopathy"],
                "equipment": ["Central line kit", "Ultrasound", "Sterile drapes"],
                "steps": [
                    "Sterile preparation",
                    "Ultrasound guidance",
                    "Needle insertion",
                    "Guidewire placement",
                    "Catheter insertion",
                    "Confirm placement"
                ],
                "complications": ["Pneumothorax", "Hemorrhage", "Infection"],
                "success_rate": 0.90
            },
            {
                "name": "Chest Tube Insertion",
                "category": "Thoracic",
                "description": "Tube thoracostomy for pneumothorax or hemothorax",
                "indications": ["Pneumothorax", "Hemothorax", "Pleural effusion"],
                "contraindications": ["Coagulopathy", "Infection at site"],
                "equipment": ["Chest tube kit", "Sterile drapes", "Suction"],
                "steps": [
                    "Sterile preparation",
                    "Identify insertion site",
                    "Local anesthesia",
                    "Make incision",
                    "Insert chest tube",
                    "Connect to drainage"
                ],
                "complications": ["Infection", "Hemorrhage", "Lung injury"],
                "success_rate": 0.85
            }
        ]
        
        # emergency medicine protocols
        self.protocols = [
            {
                "name": "ACLS Protocol",
                "category": "Resuscitation",
                "description": "Advanced Cardiac Life Support protocol",
                "indications": ["Cardiac arrest", "Ventricular fibrillation", "Pulseless VT"],
                "steps": [
                    "Check responsiveness",
                    "Activate emergency response",
                    "Begin chest compressions",
                    "Apply AED/defibrillator",
                    "Administer epinephrine",
                    "Advanced airway management"
                ],
                "medications": ["Epinephrine", "Amiodarone", "Lidocaine"],
                "equipment": ["Defibrillator", "AED", "Airway equipment"]
            },
            {
                "name": "Trauma Protocol",
                "category": "Trauma",
                "description": "Primary and secondary trauma assessment",
                "indications": ["Major trauma", "Multiple injuries", "Hemodynamic instability"],
                "steps": [
                    "Primary survey (ABCDE)",
                    "Airway management",
                    "Breathing assessment",
                    "Circulation control",
                    "Disability assessment",
                    "Exposure and environment"
                ],
                "medications": ["Crystalloids", "Blood products", "Analgesics"],
                "equipment": ["Cervical collar", "Backboard", "Tourniquet"]
            },
            {
                "name": "Sepsis Protocol",
                "category": "Critical Care",
                "description": "Sepsis recognition and management",
                "indications": ["Suspected infection", "Organ dysfunction", "Hemodynamic instability"],
                "steps": [
                    "Recognize sepsis",
                    "Obtain cultures",
                    "Administer antibiotics",
                    "Fluid resuscitation",
                    "Vasopressor support",
                    "Source control"
                ],
                "medications": ["Broad-spectrum antibiotics", "Vasopressors", "Corticosteroids"],
                "equipment": ["IV access", "Monitoring equipment", "Ventilator"]
            }
        ]
        
        # emergency medicine drugs
        self.drugs = [
            {
                "name": "Epinephrine",
                "class": "Catecholamine",
                "indications": ["Cardiac arrest", "Anaphylaxis", "Severe hypotension"],
                "dosing": "1mg IV every 3-5 minutes",
                "contraindications": ["Hypersensitivity"],
                "side_effects": ["Tachycardia", "Hypertension", "Arrhythmias"]
            },
            {
                "name": "Amiodarone",
                "class": "Antiarrhythmic",
                "indications": ["Ventricular fibrillation", "Ventricular tachycardia"],
                "dosing": "300mg IV bolus, then 150mg",
                "contraindications": ["Thyroid disease", "Pulmonary fibrosis"],
                "side_effects": ["Bradycardia", "Hypotension", "Pulmonary toxicity"]
            },
            {
                "name": "Fentanyl",
                "class": "Opioid",
                "indications": ["Pain management", "Sedation"],
                "dosing": "1-2mcg/kg IV",
                "contraindications": ["Respiratory depression", "Hypersensitivity"],
                "side_effects": ["Respiratory depression", "Sedation", "Nausea"]
            }
        ]
        
        # emergency medicine lab tests
        self.lab_tests = [
            {
                "name": "Troponin",
                "category": "Cardiac",
                "description": "Cardiac biomarker for myocardial injury",
                "normal_range": (0, 0.04),
                "critical_value": 0.5,
                "turnaround_time": 60
            },
            {
                "name": "Lactate",
                "category": "Metabolic",
                "description": "Marker for tissue hypoperfusion",
                "normal_range": (0.5, 2.2),
                "critical_value": 4.0,
                "turnaround_time": 30
            },
            {
                "name": "D-dimer",
                "category": "Coagulation",
                "description": "Fibrin degradation product",
                "normal_range": (0, 0.5),
                "critical_value": 2.0,
                "turnaround_time": 60
            }
        ]
        
        # emergency medicine imaging studies
        self.imaging_studies = [
            {
                "name": "Chest X-Ray",
                "modality": "X-Ray",
                "description": "Chest radiograph for trauma and respiratory assessment",
                "indications": ["Trauma", "Respiratory distress", "Chest pain"],
                "turnaround_time": 30,
                "cost": 150
            },
            {
                "name": "CT Head",
                "modality": "CT",
                "description": "Computed tomography of head",
                "indications": ["Head trauma", "Altered mental status", "Stroke"],
                "turnaround_time": 30,
                "cost": 600
            },
            {
                "name": "FAST Exam",
                "modality": "Ultrasound",
                "description": "Focused Assessment with Sonography for Trauma",
                "indications": ["Trauma", "Abdominal pain", "Hypotension"],
                "turnaround_time": 10,
                "cost": 200
            }
        ]

# plugin instance for registration
emergency_medicine_plugin = EmergencyMedicinePlugin() 