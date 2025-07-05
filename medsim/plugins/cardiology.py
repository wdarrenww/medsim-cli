"""
Cardiology Specialty Plugin
example for plugin system
"""

from typing import Dict, List, Any
from ...core.plugins import SpecialtyPlugin, PluginMetadata

class CardiologyPlugin(SpecialtyPlugin):
    """cardiology specialty plugin"""
    def __init__(self):
        metadata = PluginMetadata(
            name="Cardiology",
            version="1.0.0",
            description="Cardiology specialty with ACS, arrhythmia, and heart failure cases",
            author="Medical Simulator Team",
            category="specialty",
            tags=["cardiology", "acs", "arrhythmia", "heart_failure"],
            config_schema={}
        )
        super().__init__(metadata, {})
    def _load_specialty_content(self):
        self.scenarios = [
            {
                "id": "card_acs_01",
                "title": "Acute Coronary Syndrome",
                "description": "62-year-old male with chest pain and STEMI",
                "difficulty": "advanced",
                "learning_objectives": [
                    "STEMI recognition",
                    "Reperfusion therapy",
                    "Antiplatelet and anticoagulant use"
                ],
                "patient_profile": {
                    "age": 62,
                    "gender": "male",
                    "chief_complaint": "Chest pain",
                    "vitals": {
                        "blood_pressure_systolic": 130,
                        "blood_pressure_diastolic": 85,
                        "heart_rate": 95,
                        "respiratory_rate": 20,
                        "temperature": 36.9,
                        "oxygen_saturation": 97
                    }
                }
            },
            {
                "id": "card_arrhythmia_01",
                "title": "Atrial Fibrillation with RVR",
                "description": "70-year-old female with palpitations and rapid heart rate",
                "difficulty": "intermediate",
                "learning_objectives": [
                    "Arrhythmia recognition",
                    "Rate vs rhythm control",
                    "Stroke risk assessment"
                ],
                "patient_profile": {
                    "age": 70,
                    "gender": "female",
                    "chief_complaint": "Palpitations",
                    "vitals": {
                        "blood_pressure_systolic": 110,
                        "blood_pressure_diastolic": 70,
                        "heart_rate": 150,
                        "respiratory_rate": 22,
                        "temperature": 37.1,
                        "oxygen_saturation": 96
                    }
                }
            }
        ]
        self.procedures = [
            {
                "name": "Cardioversion",
                "category": "Arrhythmia",
                "description": "Synchronized electrical cardioversion for unstable arrhythmias",
                "indications": ["Atrial fibrillation", "SVT", "VT with pulse"],
                "contraindications": ["Digitalis toxicity", "Hypokalemia"],
                "equipment": ["Defibrillator", "Sedation meds"],
                "steps": [
                    "Sedate patient",
                    "Apply pads",
                    "Select energy",
                    "Synchronize",
                    "Deliver shock"
                ],
                "complications": ["Skin burns", "Arrhythmia", "Embolism"],
                "success_rate": 0.92
            }
        ]
        self.protocols = [
            {
                "name": "ACS Protocol",
                "category": "Acute Coronary Syndrome",
                "description": "Management of STEMI/NSTEMI",
                "indications": ["Chest pain", "ECG changes", "Elevated troponin"],
                "steps": [
                    "Aspirin",
                    "Nitroglycerin",
                    "Heparin",
                    "Cardiology consult",
                    "Cath lab activation"
                ],
                "medications": ["Aspirin", "Nitroglycerin", "Heparin"],
                "equipment": ["ECG", "IV access"]
            }
        ]
        self.drugs = [
            {
                "name": "Aspirin",
                "class": "Antiplatelet",
                "indications": ["ACS", "Stroke prevention"],
                "dosing": "325mg oral",
                "contraindications": ["Allergy", "Active bleeding"],
                "side_effects": ["GI upset", "Bleeding"]
            },
            {
                "name": "Metoprolol",
                "class": "Beta-blocker",
                "indications": ["Hypertension", "AFib", "Heart failure"],
                "dosing": "5mg IV q5min x3",
                "contraindications": ["Bradycardia", "Asthma"],
                "side_effects": ["Bradycardia", "Hypotension"]
            }
        ]
        self.lab_tests = [
            {
                "name": "Troponin",
                "category": "Cardiac",
                "description": "Cardiac biomarker",
                "normal_range": (0, 0.04),
                "critical_value": 0.5,
                "turnaround_time": 60
            }
        ]
        self.imaging_studies = [
            {
                "name": "ECG",
                "modality": "ECG",
                "description": "Electrocardiogram",
                "indications": ["Chest pain", "Arrhythmia"],
                "turnaround_time": 10,
                "cost": 100
            }
        ]

cardiology_plugin = CardiologyPlugin() 