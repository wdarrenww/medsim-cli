"""
Infectious Disease Specialty Plugin
example for plugin system
"""

from typing import Dict, List, Any
from ...core.plugins import SpecialtyPlugin, PluginMetadata

class InfectiousDiseasePlugin(SpecialtyPlugin):
    """infectious disease specialty plugin"""
    def __init__(self):
        metadata = PluginMetadata(
            name="Infectious Disease",
            version="1.0.0",
            description="Infectious Disease specialty with sepsis, pneumonia, and meningitis cases",
            author="Medical Simulator Team",
            category="specialty",
            tags=["infectious", "sepsis", "pneumonia", "meningitis"],
            config_schema={}
        )
        super().__init__(metadata, {})
    def _load_specialty_content(self):
        self.scenarios = [
            {
                "id": "id_sepsis_01",
                "title": "Septic Shock",
                "description": "68-year-old female with fever, hypotension, and altered mental status",
                "difficulty": "advanced",
                "learning_objectives": [
                    "Sepsis recognition",
                    "Early antibiotics",
                    "Fluid resuscitation"
                ],
                "patient_profile": {
                    "age": 68,
                    "gender": "female",
                    "chief_complaint": "Fever and confusion",
                    "vitals": {
                        "blood_pressure_systolic": 80,
                        "blood_pressure_diastolic": 50,
                        "heart_rate": 120,
                        "respiratory_rate": 28,
                        "temperature": 39.2,
                        "oxygen_saturation": 90
                    }
                }
            },
            {
                "id": "id_pneumonia_01",
                "title": "Community-Acquired Pneumonia",
                "description": "55-year-old male with cough, fever, and hypoxia",
                "difficulty": "intermediate",
                "learning_objectives": [
                    "Pneumonia diagnosis",
                    "Antibiotic selection",
                    "Oxygen therapy"
                ],
                "patient_profile": {
                    "age": 55,
                    "gender": "male",
                    "chief_complaint": "Cough and fever",
                    "vitals": {
                        "blood_pressure_systolic": 115,
                        "blood_pressure_diastolic": 70,
                        "heart_rate": 105,
                        "respiratory_rate": 24,
                        "temperature": 38.7,
                        "oxygen_saturation": 91
                    }
                }
            }
        ]
        self.procedures = [
            {
                "name": "Lumbar Puncture",
                "category": "Diagnostic",
                "description": "CSF sampling for meningitis diagnosis",
                "indications": ["Suspected meningitis", "Subarachnoid hemorrhage"],
                "contraindications": ["Increased ICP", "Coagulopathy"],
                "equipment": ["LP kit", "Sterile gloves"],
                "steps": [
                    "Position patient",
                    "Sterile prep",
                    "Insert needle",
                    "Collect CSF",
                    "Send for analysis"
                ],
                "complications": ["Headache", "Bleeding", "Infection"],
                "success_rate": 0.97
            }
        ]
        self.protocols = [
            {
                "name": "Sepsis Protocol",
                "category": "Sepsis",
                "description": "Early goal-directed therapy for sepsis",
                "indications": ["Suspected sepsis", "Hypotension", "Lactate >2.0"],
                "steps": [
                    "Blood cultures",
                    "Broad-spectrum antibiotics",
                    "IV fluids",
                    "Vasopressors if needed"
                ],
                "medications": ["Vancomycin", "Piperacillin-tazobactam", "Norepinephrine"],
                "equipment": ["IV access", "Monitoring"]
            }
        ]
        self.drugs = [
            {
                "name": "Vancomycin",
                "class": "Glycopeptide antibiotic",
                "indications": ["MRSA", "Sepsis"],
                "dosing": "15mg/kg IV q12h",
                "contraindications": ["Allergy"],
                "side_effects": ["Nephrotoxicity", "Red man syndrome"]
            },
            {
                "name": "Piperacillin-tazobactam",
                "class": "Beta-lactam/beta-lactamase inhibitor",
                "indications": ["Sepsis", "Pneumonia"],
                "dosing": "4.5g IV q6h",
                "contraindications": ["Allergy"],
                "side_effects": ["Rash", "Diarrhea"]
            }
        ]
        self.lab_tests = [
            {
                "name": "Blood Culture",
                "category": "Microbiology",
                "description": "Detects bacteremia",
                "normal_range": (0, 0),
                "critical_value": 1,
                "turnaround_time": 1440
            }
        ]
        self.imaging_studies = [
            {
                "name": "Chest X-Ray",
                "modality": "X-Ray",
                "description": "Detects pneumonia, effusion, or infiltrate",
                "indications": ["Cough", "Fever", "Hypoxia"],
                "turnaround_time": 30,
                "cost": 150
            }
        ]

infectious_disease_plugin = InfectiousDiseasePlugin() 