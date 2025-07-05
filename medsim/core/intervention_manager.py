"""
comprehensive intervention manager for patient simulation
handles ordering, scheduling, execution, and tracking of interventions
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import random
import json

class InterventionType(Enum):
    """types of medical interventions"""
    MEDICATION = "medication"
    PROCEDURE = "procedure"
    LABORATORY = "laboratory"
    IMAGING = "imaging"
    SUPPORTIVE = "supportive"
    MONITORING = "monitoring"
    EMERGENCY = "emergency"

class OrganSystem(Enum):
    """organ systems that can be affected by interventions"""
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    RENAL = "renal"
    HEPATIC = "hepatic"
    NEUROLOGICAL = "neurological"
    HEMATOLOGICAL = "hematological"
    IMMUNE = "immune"
    ENDOCRINE = "endocrine"
    GASTROINTESTINAL = "gastrointestinal"
    MUSCULOSKELETAL = "musculoskeletal"
    INTEGUMENTARY = "integumentary"

class AdverseEventType(Enum):
    """types of adverse events"""
    ALLERGIC_REACTION = "allergic_reaction"
    ARRHYTHMIA = "arrhythmia"
    HYPOTENSION = "hypotension"
    HYPERTENSION = "hypertension"
    RESPIRATORY_DEPRESSION = "respiratory_depression"
    RENAL_INJURY = "renal_injury"
    HEPATIC_INJURY = "hepatic_injury"
    BLEEDING = "bleeding"
    INFECTION = "infection"
    THROMBOSIS = "thrombosis"
    EMBOLISM = "embolism"
    SEPSIS = "sepsis"
    SHOCK = "shock"
    CARDIAC_ARREST = "cardiac_arrest"
    STROKE = "stroke"
    SEIZURE = "seizure"
    COMA = "coma"
    ORGAN_FAILURE = "organ_failure"
    MEDICATION_ERROR = "medication_error"
    PROCEDURE_COMPLICATION = "procedure_complication"

@dataclass
class InterventionDefinition:
    """definition of an intervention with its properties"""
    name: str
    type: InterventionType
    target_organs: List[OrganSystem]
    duration_minutes: int
    success_rate: float
    adverse_event_risk: float
    contraindications: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    description: str = ""

@dataclass
class InterventionOrder:
    """an intervention order with comprehensive tracking"""
    order_id: str
    type: InterventionType
    name: str
    target_organs: List[OrganSystem]
    parameters: Dict[str, Any] = field(default_factory=dict)
    ordered_time: datetime = field(default_factory=datetime.now)
    scheduled_time: Optional[datetime] = None
    executed_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None
    status: str = "pending"  # pending, scheduled, executing, completed, cancelled, failed
    result: Optional[Dict[str, Any]] = None
    adverse_events: List[AdverseEventType] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    provider: Optional[str] = None
    priority: int = 1  # 1=low, 2=medium, 3=high, 4=urgent

class InterventionManager:
    """comprehensive intervention manager with extensive intervention library"""
    
    def __init__(self):
        self.orders: List[InterventionOrder] = []
        self.next_order_id = 1
        self.intervention_definitions = self._initialize_intervention_definitions()
        
    def _initialize_intervention_definitions(self) -> Dict[str, InterventionDefinition]:
        """initialize comprehensive intervention definitions"""
        definitions = {}
        
        # medications
        definitions.update({
            "antibiotic": InterventionDefinition(
                name="antibiotic",
                type=InterventionType.MEDICATION,
                target_organs=[OrganSystem.IMMUNE, OrganSystem.RENAL, OrganSystem.HEPATIC],
                duration_minutes=60,
                success_rate=0.85,
                adverse_event_risk=0.08,
                contraindications=["allergy", "renal_failure"],
                parameters={"route": "iv", "dose": "1g", "frequency": "q8h"}
            ),
            "vasopressor": InterventionDefinition(
                name="vasopressor",
                type=InterventionType.MEDICATION,
                target_organs=[OrganSystem.CARDIOVASCULAR, OrganSystem.RENAL],
                duration_minutes=30,
                success_rate=0.90,
                adverse_event_risk=0.12,
                contraindications=["arrhythmia", "severe_hypertension"],
                parameters={"agent": "norepinephrine", "dose": "0.1mcg/kg/min"}
            ),
            "anticoagulant": InterventionDefinition(
                name="anticoagulant",
                type=InterventionType.MEDICATION,
                target_organs=[OrganSystem.HEMATOLOGICAL, OrganSystem.CARDIOVASCULAR],
                duration_minutes=45,
                success_rate=0.88,
                adverse_event_risk=0.15,
                contraindications=["bleeding", "thrombocytopenia"],
                parameters={"agent": "heparin", "dose": "5000u"}
            ),
            "sedative": InterventionDefinition(
                name="sedative",
                type=InterventionType.MEDICATION,
                target_organs=[OrganSystem.NEUROLOGICAL, OrganSystem.RESPIRATORY],
                duration_minutes=20,
                success_rate=0.95,
                adverse_event_risk=0.10,
                contraindications=["respiratory_failure", "shock"],
                parameters={"agent": "midazolam", "dose": "2mg"}
            ),
            "insulin": InterventionDefinition(
                name="insulin",
                type=InterventionType.MEDICATION,
                target_organs=[OrganSystem.ENDOCRINE, OrganSystem.CARDIOVASCULAR],
                duration_minutes=120,
                success_rate=0.92,
                adverse_event_risk=0.05,
                contraindications=["hypoglycemia"],
                parameters={"type": "regular", "dose": "10u"}
            ),
            "diuretic": InterventionDefinition(
                name="diuretic",
                type=InterventionType.MEDICATION,
                target_organs=[OrganSystem.RENAL, OrganSystem.CARDIOVASCULAR],
                duration_minutes=90,
                success_rate=0.87,
                adverse_event_risk=0.08,
                contraindications=["hypovolemia", "renal_failure"],
                parameters={"agent": "furosemide", "dose": "40mg"}
            ),
            "bronchodilator": InterventionDefinition(
                name="bronchodilator",
                type=InterventionType.MEDICATION,
                target_organs=[OrganSystem.RESPIRATORY, OrganSystem.CARDIOVASCULAR],
                duration_minutes=30,
                success_rate=0.89,
                adverse_event_risk=0.06,
                contraindications=["arrhythmia"],
                parameters={"agent": "albuterol", "dose": "2.5mg"}
            ),
            "antiemetic": InterventionDefinition(
                name="antiemetic",
                type=InterventionType.MEDICATION,
                target_organs=[OrganSystem.GASTROINTESTINAL, OrganSystem.NEUROLOGICAL],
                duration_minutes=60,
                success_rate=0.90,
                adverse_event_risk=0.03,
                contraindications=["bowel_obstruction"],
                parameters={"agent": "ondansetron", "dose": "4mg"}
            )
        })
        
        # procedures
        definitions.update({
            "intubation": InterventionDefinition(
                name="intubation",
                type=InterventionType.PROCEDURE,
                target_organs=[OrganSystem.RESPIRATORY, OrganSystem.NEUROLOGICAL],
                duration_minutes=15,
                success_rate=0.95,
                adverse_event_risk=0.08,
                contraindications=["facial_trauma", "cervical_spine_injury"],
                parameters={"tube_size": "7.5", "depth": "22cm"}
            ),
            "central_line": InterventionDefinition(
                name="central_line",
                type=InterventionType.PROCEDURE,
                target_organs=[OrganSystem.CARDIOVASCULAR, OrganSystem.INTEGUMENTARY],
                duration_minutes=30,
                success_rate=0.90,
                adverse_event_risk=0.12,
                contraindications=["coagulopathy", "infection"],
                parameters={"site": "subclavian", "catheter_type": "triple_lumen"}
            ),
            "chest_tube": InterventionDefinition(
                name="chest_tube",
                type=InterventionType.PROCEDURE,
                target_organs=[OrganSystem.RESPIRATORY, OrganSystem.CARDIOVASCULAR],
                duration_minutes=25,
                success_rate=0.88,
                adverse_event_risk=0.15,
                contraindications=["coagulopathy"],
                parameters={"size": "28f", "site": "5th_ics"}
            ),
            "lumbar_puncture": InterventionDefinition(
                name="lumbar_puncture",
                type=InterventionType.PROCEDURE,
                target_organs=[OrganSystem.NEUROLOGICAL],
                duration_minutes=20,
                success_rate=0.85,
                adverse_event_risk=0.05,
                contraindications=["increased_icp", "coagulopathy"],
                parameters={"needle_size": "22g", "site": "l4-l5"}
            ),
            "paracentesis": InterventionDefinition(
                name="paracentesis",
                type=InterventionType.PROCEDURE,
                target_organs=[OrganSystem.GASTROINTESTINAL, OrganSystem.RENAL],
                duration_minutes=45,
                success_rate=0.92,
                adverse_event_risk=0.08,
                contraindications=["coagulopathy", "infection"],
                parameters={"site": "right_lower_quadrant", "volume": "2l"}
            ),
            "dialysis": InterventionDefinition(
                name="dialysis",
                type=InterventionType.PROCEDURE,
                target_organs=[OrganSystem.RENAL, OrganSystem.CARDIOVASCULAR],
                duration_minutes=240,
                success_rate=0.95,
                adverse_event_risk=0.10,
                contraindications=["hypotension", "bleeding"],
                parameters={"type": "hemodialysis", "duration": "4h"}
            ),
            "cardiac_catheterization": InterventionDefinition(
                name="cardiac_catheterization",
                type=InterventionType.PROCEDURE,
                target_organs=[OrganSystem.CARDIOVASCULAR],
                duration_minutes=120,
                success_rate=0.88,
                adverse_event_risk=0.18,
                contraindications=["coagulopathy", "renal_failure"],
                parameters={"access": "femoral", "contrast_volume": "100ml"}
            ),
            "endoscopy": InterventionDefinition(
                name="endoscopy",
                type=InterventionType.PROCEDURE,
                target_organs=[OrganSystem.GASTROINTESTINAL],
                duration_minutes=60,
                success_rate=0.90,
                adverse_event_risk=0.08,
                contraindications=["perforation", "obstruction"],
                parameters={"type": "upper_gi", "scope_size": "9.8mm"}
            )
        })
        
        # laboratory tests
        definitions.update({
            "cbc": InterventionDefinition(
                name="cbc",
                type=InterventionType.LABORATORY,
                target_organs=[OrganSystem.HEMATOLOGICAL],
                duration_minutes=30,
                success_rate=0.98,
                adverse_event_risk=0.01,
                parameters={"volume": "3ml", "tube": "lavender"}
            ),
            "chemistry": InterventionDefinition(
                name="chemistry",
                type=InterventionType.LABORATORY,
                target_organs=[OrganSystem.RENAL, OrganSystem.HEPATIC],
                duration_minutes=45,
                success_rate=0.97,
                adverse_event_risk=0.01,
                parameters={"volume": "5ml", "tube": "red"}
            ),
            "troponin": InterventionDefinition(
                name="troponin",
                type=InterventionType.LABORATORY,
                target_organs=[OrganSystem.CARDIOVASCULAR],
                duration_minutes=20,
                success_rate=0.96,
                adverse_event_risk=0.01,
                parameters={"volume": "2ml", "tube": "red"}
            ),
            "blood_culture": InterventionDefinition(
                name="blood_culture",
                type=InterventionType.LABORATORY,
                target_organs=[OrganSystem.IMMUNE],
                duration_minutes=15,
                success_rate=0.95,
                adverse_event_risk=0.02,
                parameters={"volume": "10ml", "bottles": 2}
            ),
            "arterial_blood_gas": InterventionDefinition(
                name="arterial_blood_gas",
                type=InterventionType.LABORATORY,
                target_organs=[OrganSystem.RESPIRATORY, OrganSystem.CARDIOVASCULAR],
                duration_minutes=10,
                success_rate=0.90,
                adverse_event_risk=0.05,
                parameters={"site": "radial", "volume": "1ml"}
            ),
            "coagulation_studies": InterventionDefinition(
                name="coagulation_studies",
                type=InterventionType.LABORATORY,
                target_organs=[OrganSystem.HEMATOLOGICAL],
                duration_minutes=40,
                success_rate=0.96,
                adverse_event_risk=0.01,
                parameters={"volume": "2ml", "tube": "blue"}
            )
        })
        
        # imaging
        definitions.update({
            "chest_xray": InterventionDefinition(
                name="chest_xray",
                type=InterventionType.IMAGING,
                target_organs=[OrganSystem.RESPIRATORY, OrganSystem.CARDIOVASCULAR],
                duration_minutes=15,
                success_rate=0.99,
                adverse_event_risk=0.001,
                parameters={"views": "pa_lateral", "radiation": "0.1msv"}
            ),
            "ct_chest": InterventionDefinition(
                name="ct_chest",
                type=InterventionType.IMAGING,
                target_organs=[OrganSystem.RESPIRATORY, OrganSystem.CARDIOVASCULAR],
                duration_minutes=30,
                success_rate=0.98,
                adverse_event_risk=0.005,
                parameters={"contrast": "iv", "radiation": "7msv"}
            ),
            "ct_head": InterventionDefinition(
                name="ct_head",
                type=InterventionType.IMAGING,
                target_organs=[OrganSystem.NEUROLOGICAL],
                duration_minutes=20,
                success_rate=0.98,
                adverse_event_risk=0.005,
                parameters={"contrast": "none", "radiation": "2msv"}
            ),
            "echocardiogram": InterventionDefinition(
                name="echocardiogram",
                type=InterventionType.IMAGING,
                target_organs=[OrganSystem.CARDIOVASCULAR],
                duration_minutes=45,
                success_rate=0.95,
                adverse_event_risk=0.001,
                parameters={"type": "transthoracic", "views": "standard"}
            ),
            "mri_brain": InterventionDefinition(
                name="mri_brain",
                type=InterventionType.IMAGING,
                target_organs=[OrganSystem.NEUROLOGICAL],
                duration_minutes=60,
                success_rate=0.97,
                adverse_event_risk=0.001,
                parameters={"sequences": "t1_t2_flair", "contrast": "gadolinium"}
            ),
            "ultrasound_abdomen": InterventionDefinition(
                name="ultrasound_abdomen",
                type=InterventionType.IMAGING,
                target_organs=[OrganSystem.GASTROINTESTINAL, OrganSystem.HEPATIC],
                duration_minutes=30,
                success_rate=0.94,
                adverse_event_risk=0.001,
                parameters={"probe": "3.5mhz", "views": "standard"}
            )
        })
        
        # supportive care
        definitions.update({
            "oxygen_therapy": InterventionDefinition(
                name="oxygen_therapy",
                type=InterventionType.SUPPORTIVE,
                target_organs=[OrganSystem.RESPIRATORY],
                duration_minutes=0,  # continuous
                success_rate=0.99,
                adverse_event_risk=0.01,
                parameters={"flow": "2lpm", "device": "nasal_cannula"}
            ),
            "mechanical_ventilation": InterventionDefinition(
                name="mechanical_ventilation",
                type=InterventionType.SUPPORTIVE,
                target_organs=[OrganSystem.RESPIRATORY, OrganSystem.CARDIOVASCULAR],
                duration_minutes=0,  # continuous
                success_rate=0.95,
                adverse_event_risk=0.15,
                parameters={"mode": "assist_control", "tidal_volume": "500ml"}
            ),
            "iv_fluids": InterventionDefinition(
                name="iv_fluids",
                type=InterventionType.SUPPORTIVE,
                target_organs=[OrganSystem.CARDIOVASCULAR, OrganSystem.RENAL],
                duration_minutes=0,  # continuous
                success_rate=0.98,
                adverse_event_risk=0.03,
                parameters={"type": "normal_saline", "rate": "100ml/hr"}
            ),
            "blood_transfusion": InterventionDefinition(
                name="blood_transfusion",
                type=InterventionType.SUPPORTIVE,
                target_organs=[OrganSystem.HEMATOLOGICAL, OrganSystem.CARDIOVASCULAR],
                duration_minutes=120,
                success_rate=0.99,
                adverse_event_risk=0.05,
                parameters={"type": "prbc", "units": 2}
            ),
            "temperature_control": InterventionDefinition(
                name="temperature_control",
                type=InterventionType.SUPPORTIVE,
                target_organs=[OrganSystem.INTEGUMENTARY, OrganSystem.NEUROLOGICAL],
                duration_minutes=0,  # continuous
                success_rate=0.97,
                adverse_event_risk=0.02,
                parameters={"method": "cooling_blanket", "target": "37c"}
            ),
            "nutrition": InterventionDefinition(
                name="nutrition",
                type=InterventionType.SUPPORTIVE,
                target_organs=[OrganSystem.GASTROINTESTINAL, OrganSystem.ENDOCRINE],
                duration_minutes=0,  # continuous
                success_rate=0.96,
                adverse_event_risk=0.03,
                parameters={"type": "enteral", "rate": "50ml/hr"}
            )
        })
        
        # monitoring
        definitions.update({
            "ecg_monitoring": InterventionDefinition(
                name="ecg_monitoring",
                type=InterventionType.MONITORING,
                target_organs=[OrganSystem.CARDIOVASCULAR],
                duration_minutes=0,  # continuous
                success_rate=0.99,
                adverse_event_risk=0.001,
                parameters={"leads": "5_lead", "alarms": "enabled"}
            ),
            "pulse_oximetry": InterventionDefinition(
                name="pulse_oximetry",
                type=InterventionType.MONITORING,
                target_organs=[OrganSystem.RESPIRATORY, OrganSystem.CARDIOVASCULAR],
                duration_minutes=0,  # continuous
                success_rate=0.99,
                adverse_event_risk=0.001,
                parameters={"site": "finger", "alarms": "enabled"}
            ),
            "arterial_line": InterventionDefinition(
                name="arterial_line",
                type=InterventionType.MONITORING,
                target_organs=[OrganSystem.CARDIOVASCULAR],
                duration_minutes=0,  # continuous
                success_rate=0.90,
                adverse_event_risk=0.08,
                parameters={"site": "radial", "calibration": "q4h"}
            ),
            "central_venous_pressure": InterventionDefinition(
                name="central_venous_pressure",
                type=InterventionType.MONITORING,
                target_organs=[OrganSystem.CARDIOVASCULAR],
                duration_minutes=0,  # continuous
                success_rate=0.92,
                adverse_event_risk=0.05,
                parameters={"site": "subclavian", "calibration": "q4h"}
            ),
            "intracranial_pressure": InterventionDefinition(
                name="intracranial_pressure",
                type=InterventionType.MONITORING,
                target_organs=[OrganSystem.NEUROLOGICAL],
                duration_minutes=0,  # continuous
                success_rate=0.85,
                adverse_event_risk=0.12,
                parameters={"type": "intraventricular", "calibration": "q8h"}
            )
        })
        
        # emergency interventions
        definitions.update({
            "cpr": InterventionDefinition(
                name="cpr",
                type=InterventionType.EMERGENCY,
                target_organs=[OrganSystem.CARDIOVASCULAR, OrganSystem.RESPIRATORY],
                duration_minutes=5,
                success_rate=0.40,
                adverse_event_risk=0.20,
                parameters={"compression_rate": "100/min", "depth": "2in"}
            ),
            "defibrillation": InterventionDefinition(
                name="defibrillation",
                type=InterventionType.EMERGENCY,
                target_organs=[OrganSystem.CARDIOVASCULAR],
                duration_minutes=1,
                success_rate=0.60,
                adverse_event_risk=0.05,
                parameters={"energy": "200j", "paddle_position": "sternal_apex"}
            ),
            "emergency_intubation": InterventionDefinition(
                name="emergency_intubation",
                type=InterventionType.EMERGENCY,
                target_organs=[OrganSystem.RESPIRATORY, OrganSystem.NEUROLOGICAL],
                duration_minutes=3,
                success_rate=0.85,
                adverse_event_risk=0.25,
                parameters={"tube_size": "7.5", "cricoid_pressure": "yes"}
            ),
            "emergency_thoracotomy": InterventionDefinition(
                name="emergency_thoracotomy",
                type=InterventionType.EMERGENCY,
                target_organs=[OrganSystem.CARDIOVASCULAR, OrganSystem.RESPIRATORY],
                duration_minutes=30,
                success_rate=0.30,
                adverse_event_risk=0.50,
                parameters={"approach": "left_anterolateral", "indication": "cardiac_arrest"}
            ),
            "emergency_laparotomy": InterventionDefinition(
                name="emergency_laparotomy",
                type=InterventionType.EMERGENCY,
                target_organs=[OrganSystem.GASTROINTESTINAL, OrganSystem.CARDIOVASCULAR],
                duration_minutes=60,
                success_rate=0.70,
                adverse_event_risk=0.40,
                parameters={"approach": "midline", "indication": "peritonitis"}
            )
        })
        
        return definitions
    
    def get_available_interventions(self, organ_system: Optional[OrganSystem] = None) -> List[str]:
        """get list of available interventions, optionally filtered by organ system"""
        if organ_system is None:
            return list(self.intervention_definitions.keys())
        return [name for name, defn in self.intervention_definitions.items() 
                if organ_system in defn.target_organs]
    
    def get_intervention_info(self, intervention_name: str) -> Optional[InterventionDefinition]:
        """get detailed information about an intervention"""
        return self.intervention_definitions.get(intervention_name)
    
    def order_intervention(self, intervention_name: str, parameters: Optional[Dict[str, Any]] = None,
                          delay_minutes: int = 0, priority: int = 2, provider: Optional[str] = None) -> InterventionOrder:
        """order an intervention with comprehensive parameters"""
        if intervention_name not in self.intervention_definitions:
            raise ValueError(f"unknown intervention: {intervention_name}")
        
        definition = self.intervention_definitions[intervention_name]
        
        # merge default parameters with provided ones
        final_parameters = definition.parameters.copy()
        if parameters:
            final_parameters.update(parameters)
        
        order = InterventionOrder(
            order_id=f"ORD{self.next_order_id:04d}",
            type=definition.type,
            name=intervention_name,
            target_organs=definition.target_organs,
            parameters=final_parameters,
            ordered_time=datetime.now(),
            scheduled_time=datetime.now() + timedelta(minutes=delay_minutes),
            status="scheduled" if delay_minutes > 0 else "pending",
            priority=priority,
            provider=provider
        )
        
        self.orders.append(order)
        self.next_order_id += 1
        return order
    
    def execute_due_interventions(self, current_time: datetime) -> List[InterventionOrder]:
        """execute all due interventions and return results"""
        executed = []
        for order in self.orders:
            if order.status in ["pending", "scheduled"] and order.scheduled_time and current_time >= order.scheduled_time:
                order.status = "executing"
                order.executed_time = current_time
                
                # simulate execution
                success = self._simulate_execution_success(order)
                if success:
                    order.status = "completed"
                    order.completed_time = current_time + timedelta(minutes=self.intervention_definitions[order.name].duration_minutes)
                    order.result = self._simulate_result(order)
                else:
                    order.status = "failed"
                    order.result = {"error": "execution_failed"}
                
                # simulate adverse events
                order.adverse_events = self._simulate_adverse_events(order)
                
                executed.append(order)
        
        return executed
    
    def _simulate_execution_success(self, order: InterventionOrder) -> bool:
        """simulate whether intervention execution succeeds"""
        definition = self.intervention_definitions[order.name]
        base_success_rate = definition.success_rate
        
        # modify based on priority
        if order.priority >= 4:  # urgent
            base_success_rate += 0.05
        elif order.priority <= 1:  # low
            base_success_rate -= 0.05
        
        return random.random() < base_success_rate
    
    def _simulate_result(self, order: InterventionOrder) -> Dict[str, Any]:
        """simulate detailed intervention results"""
        definition = self.intervention_definitions[order.name]
        
        if definition.type == InterventionType.LABORATORY:
            return self._simulate_lab_result(order)
        elif definition.type == InterventionType.IMAGING:
            return self._simulate_imaging_result(order)
        elif definition.type == InterventionType.MEDICATION:
            return self._simulate_medication_result(order)
        elif definition.type == InterventionType.PROCEDURE:
            return self._simulate_procedure_result(order)
        else:
            return {"status": "completed", "timestamp": order.executed_time.isoformat()}
    
    def _simulate_lab_result(self, order: InterventionOrder) -> Dict[str, Any]:
        """simulate laboratory test results"""
        lab_results = {
            "cbc": {
                "wbc": random.uniform(4.0, 12.0),
                "hgb": random.uniform(12.0, 16.0),
                "plt": random.uniform(150, 450),
                "units": {"wbc": "k/ul", "hgb": "g/dl", "plt": "k/ul"}
            },
            "chemistry": {
                "na": random.uniform(135, 145),
                "k": random.uniform(3.5, 5.0),
                "cl": random.uniform(95, 105),
                "co2": random.uniform(22, 28),
                "bun": random.uniform(7, 20),
                "creatinine": random.uniform(0.6, 1.2),
                "units": {"na": "meq/l", "k": "meq/l", "cl": "meq/l", "co2": "meq/l", "bun": "mg/dl", "creatinine": "mg/dl"}
            },
            "troponin": {
                "troponin_i": random.uniform(0.0, 0.04),
                "units": {"troponin_i": "ng/ml"}
            },
            "blood_culture": {
                "result": "no_growth" if random.random() > 0.3 else "positive",
                "organism": None if random.random() > 0.3 else random.choice(["staph_aureus", "e_coli", "pseudomonas"])
            },
            "arterial_blood_gas": {
                "ph": random.uniform(7.35, 7.45),
                "pco2": random.uniform(35, 45),
                "po2": random.uniform(80, 100),
                "hco3": random.uniform(22, 28),
                "units": {"ph": "", "pco2": "mmhg", "po2": "mmhg", "hco3": "meq/l"}
            },
            "coagulation_studies": {
                "pt": random.uniform(11, 13),
                "ptt": random.uniform(25, 35),
                "inr": random.uniform(0.9, 1.1),
                "units": {"pt": "seconds", "ptt": "seconds", "inr": ""}
            }
        }
        
        return lab_results.get(order.name, {"status": "completed"})
    
    def _simulate_imaging_result(self, order: InterventionOrder) -> Dict[str, Any]:
        """simulate imaging study results"""
        imaging_results = {
            "chest_xray": {
                "findings": random.choice(["normal", "pneumonia", "pulmonary_edema", "pneumothorax", "effusion"]),
                "impression": "clinical correlation recommended"
            },
            "ct_chest": {
                "findings": random.choice(["normal", "pneumonia", "pulmonary_embolism", "mass", "effusion"]),
                "impression": "clinical correlation recommended"
            },
            "ct_head": {
                "findings": random.choice(["normal", "hemorrhage", "infarct", "mass", "edema"]),
                "impression": "clinical correlation recommended"
            },
            "echocardiogram": {
                "ef": random.uniform(50, 70),
                "findings": random.choice(["normal", "systolic_dysfunction", "valvular_disease", "pericardial_effusion"]),
                "units": {"ef": "%"}
            },
            "mri_brain": {
                "findings": random.choice(["normal", "stroke", "tumor", "demyelination", "hemorrhage"]),
                "impression": "clinical correlation recommended"
            },
            "ultrasound_abdomen": {
                "findings": random.choice(["normal", "ascites", "gallstones", "mass", "free_fluid"]),
                "impression": "clinical correlation recommended"
            }
        }
        
        return imaging_results.get(order.name, {"status": "completed"})
    
    def _simulate_medication_result(self, order: InterventionOrder) -> Dict[str, Any]:
        """simulate medication administration results"""
        return {
            "status": "administered",
            "route": order.parameters.get("route", "iv"),
            "dose": order.parameters.get("dose", "standard"),
            "timestamp": order.executed_time.isoformat()
        }
    
    def _simulate_procedure_result(self, order: InterventionOrder) -> Dict[str, Any]:
        """simulate procedure completion results"""
        return {
            "status": "completed",
            "duration_minutes": self.intervention_definitions[order.name].duration_minutes,
            "technique": order.parameters.get("technique", "standard"),
            "timestamp": order.executed_time.isoformat()
        }
    
    def _simulate_adverse_events(self, order: InterventionOrder) -> List[AdverseEventType]:
        """simulate comprehensive adverse events"""
        events = []
        definition = self.intervention_definitions[order.name]
        base_risk = definition.adverse_event_risk
        
        # organ-specific adverse events
        for organ in order.target_organs:
            if organ == OrganSystem.CARDIOVASCULAR:
                if random.random() < base_risk * 0.3:
                    events.append(AdverseEventType.ARRHYTHMIA)
                if random.random() < base_risk * 0.2:
                    events.append(AdverseEventType.HYPOTENSION)
                if random.random() < base_risk * 0.1:
                    events.append(AdverseEventType.CARDIAC_ARREST)
            
            elif organ == OrganSystem.RESPIRATORY:
                if random.random() < base_risk * 0.4:
                    events.append(AdverseEventType.RESPIRATORY_DEPRESSION)
                if random.random() < base_risk * 0.2:
                    events.append(AdverseEventType.INFECTION)
            
            elif organ == OrganSystem.RENAL:
                if random.random() < base_risk * 0.5:
                    events.append(AdverseEventType.RENAL_INJURY)
            
            elif organ == OrganSystem.HEPATIC:
                if random.random() < base_risk * 0.4:
                    events.append(AdverseEventType.HEPATIC_INJURY)
            
            elif organ == OrganSystem.HEMATOLOGICAL:
                if random.random() < base_risk * 0.3:
                    events.append(AdverseEventType.BLEEDING)
                if random.random() < base_risk * 0.2:
                    events.append(AdverseEventType.THROMBOSIS)
            
            elif organ == OrganSystem.IMMUNE:
                if random.random() < base_risk * 0.3:
                    events.append(AdverseEventType.ALLERGIC_REACTION)
                if random.random() < base_risk * 0.2:
                    events.append(AdverseEventType.INFECTION)
        
        # intervention-specific adverse events
        if order.name == "antibiotic":
            if random.random() < base_risk * 0.4:
                events.append(AdverseEventType.ALLERGIC_REACTION)
        
        elif order.name == "vasopressor":
            if random.random() < base_risk * 0.5:
                events.append(AdverseEventType.ARRHYTHMIA)
            if random.random() < base_risk * 0.3:
                events.append(AdverseEventType.HYPERTENSION)
        
        elif order.name == "anticoagulant":
            if random.random() < base_risk * 0.6:
                events.append(AdverseEventType.BLEEDING)
        
        elif order.name == "sedative":
            if random.random() < base_risk * 0.5:
                events.append(AdverseEventType.RESPIRATORY_DEPRESSION)
        
        elif "intubation" in order.name:
            if random.random() < base_risk * 0.3:
                events.append(AdverseEventType.INFECTION)
        
        elif "catheterization" in order.name or "line" in order.name:
            if random.random() < base_risk * 0.4:
                events.append(AdverseEventType.INFECTION)
            if random.random() < base_risk * 0.2:
                events.append(AdverseEventType.BLEEDING)
        
        return list(set(events))  # remove duplicates
    
    def get_active_orders(self) -> List[InterventionOrder]:
        """get all active (pending/scheduled/executing) orders"""
        return [o for o in self.orders if o.status in ["pending", "scheduled", "executing"]]
    
    def get_completed_orders(self) -> List[InterventionOrder]:
        """get all completed orders"""
        return [o for o in self.orders if o.status == "completed"]
    
    def get_failed_orders(self) -> List[InterventionOrder]:
        """get all failed orders"""
        return [o for o in self.orders if o.status == "failed"]
    
    def get_all_orders(self) -> List[InterventionOrder]:
        """get all orders"""
        return self.orders.copy()
    
    def cancel_order(self, order_id: str) -> bool:
        """cancel an order if it's still pending or scheduled"""
        for order in self.orders:
            if order.order_id == order_id and order.status in ["pending", "scheduled"]:
                order.status = "cancelled"
                return True
        return False
    
    def get_orders_by_organ(self, organ_system: OrganSystem) -> List[InterventionOrder]:
        """get all orders targeting a specific organ system"""
        return [o for o in self.orders if organ_system in o.target_organs]
    
    def get_orders_by_type(self, intervention_type: InterventionType) -> List[InterventionOrder]:
        """get all orders of a specific type"""
        return [o for o in self.orders if o.type == intervention_type]
    
    def get_orders_by_priority(self, priority: int) -> List[InterventionOrder]:
        """get all orders with a specific priority level"""
        return [o for o in self.orders if o.priority == priority]
    
    def get_adverse_events_summary(self) -> Dict[AdverseEventType, int]:
        """get summary of all adverse events across all orders"""
        summary = {}
        for order in self.orders:
            for event in order.adverse_events:
                summary[event] = summary.get(event, 0) + 1
        return summary
    
    def export_orders_summary(self) -> Dict[str, Any]:
        """export comprehensive summary of all orders"""
        return {
            "total_orders": len(self.orders),
            "active_orders": len(self.get_active_orders()),
            "completed_orders": len(self.get_completed_orders()),
            "failed_orders": len(self.get_failed_orders()),
            "orders_by_type": {t.value: len(self.get_orders_by_type(t)) for t in InterventionType},
            "orders_by_priority": {p: len(self.get_orders_by_priority(p)) for p in range(1, 5)},
            "adverse_events": self.get_adverse_events_summary(),
            "recent_orders": [{"id": o.order_id, "name": o.name, "status": o.status, "timestamp": o.ordered_time.isoformat()} 
                             for o in sorted(self.orders, key=lambda x: x.ordered_time, reverse=True)[:10]]
        } 