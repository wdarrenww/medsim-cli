"""
advanced treatment system with comprehensive medication management and dosing
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import random
import math


@dataclass
class Medication:
    """medication definition with comprehensive properties"""
    name: str
    category: str
    mechanism: str
    indications: List[str]
    contraindications: List[str]
    side_effects: List[str]
    drug_interactions: List[str]
    dosing_adult: Dict[str, Any]
    dosing_pediatric: Dict[str, Any]
    dosage_forms: List[str] = field(default_factory=list)
    renal_adjustment: bool = False
    hepatic_adjustment: bool = False
    pregnancy_category: str = "C"
    cost_per_dose: float = 10.0
    description: str = ""
    onset_time: int = 5  # minutes
    duration: int = 240  # minutes
    monitoring_required: List[str] = field(default_factory=list)


@dataclass
class TreatmentOrder:
    """treatment order with dosing and administration details"""
    medication: str
    dose: float
    unit: str
    route: str
    frequency: str
    duration: str
    patient_weight: float
    patient_age: int
    renal_function: float
    hepatic_function: str
    allergies: List[str]
    current_medications: List[str]
    order_time: datetime
    status: str = "ordered"  # ordered, administered, completed, discontinued
    administration_time: Optional[datetime] = None
    effects: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Procedure:
    """clinical procedure definition"""
    name: str
    steps: list
    indications: list
    contraindications: list
    complications: list
    required_equipment: list
    success_rate: float = 0.98
    time_required: int = 10  # minutes
    documentation: str = ""


@dataclass
class Protocol:
    """clinical protocol or order set"""
    name: str
    steps: list
    indications: list
    contraindications: list
    bundled_orders: list
    documentation: str = ""


class ProcedureSystem:
    """system for managing clinical procedures and protocols"""
    def __init__(self):
        self.procedures = self._initialize_procedures()
        self.protocols = self._initialize_protocols()
        self.active_procedures = {}
        self.procedure_history = []
        self.protocol_history = []

    def _initialize_procedures(self):
        procedures = {}
        # Airway
        procedures["cricothyrotomy"] = Procedure(
            name="Surgical Cricothyrotomy",
            steps=[
                "Identify cricothyroid membrane",
                "Prep and anesthetize",
                "Incise skin and membrane",
                "Insert tracheostomy tube",
                "Secure tube and confirm placement"
            ],
            indications=["cannot intubate/cannot oxygenate", "upper airway obstruction"],
            contraindications=["children <10 years (relative)", "laryngeal fracture"],
            complications=["bleeding", "misplacement", "subcutaneous emphysema", "infection"],
            required_equipment=["scalpel", "tracheostomy tube", "suction", "syringe"],
            success_rate=0.90,
            time_required=8,
            documentation="Cricothyrotomy performed for failed airway. Tube secured. Placement confirmed."
        )
        procedures["bag_valve_mask"] = Procedure(
            name="Bag-Valve-Mask Ventilation",
            steps=[
                "Position patient",
                "Open airway (head tilt/chin lift or jaw thrust)",
                "Seal mask",
                "Deliver breaths, observe chest rise"
            ],
            indications=["apnea", "respiratory failure", "pre-oxygenation"],
            contraindications=["complete upper airway obstruction"],
            complications=["gastric insufflation", "aspiration", "hypoventilation"],
            required_equipment=["BVM", "mask", "oxygen source"],
            success_rate=0.98,
            time_required=3,
            documentation="BVM ventilation provided with good chest rise."
        )
        # Vascular
        procedures["arterial_line"] = Procedure(
            name="Arterial Line Placement",
            steps=[
                "Prepare and drape site",
                "Anesthetize",
                "Insert needle/catheter",
                "Confirm placement (waveform)",
                "Secure line"
            ],
            indications=["hemodynamic monitoring", "frequent ABGs", "vasopressor use"],
            contraindications=["infection at site", "poor collateral flow"],
            complications=["thrombosis", "bleeding", "infection", "arterial spasm"],
            required_equipment=["arterial line kit", "pressure bag", "transducer"],
            success_rate=0.93,
            time_required=12,
            documentation="Radial arterial line placed, waveform confirmed."
        )
        procedures["intraosseous_access"] = Procedure(
            name="Intraosseous Access",
            steps=[
                "Identify site (proximal tibia/humerus)",
                "Prep and anesthetize",
                "Insert IO needle",
                "Confirm placement (aspirate, flush)",
                "Secure needle"
            ],
            indications=["emergent access", "failed IV access"],
            contraindications=["fracture at site", "infection at site"],
            complications=["extravasation", "osteomyelitis", "growth plate injury"],
            required_equipment=["IO needle", "drill", "flush", "dressing"],
            success_rate=0.97,
            time_required=2,
            documentation="IO access obtained in left proximal tibia. Good flow."
        )
        # Resuscitation
        procedures["defibrillation"] = Procedure(
            name="Defibrillation",
            steps=[
                "Apply pads",
                "Charge defibrillator",
                "Clear patient",
                "Deliver shock",
                "Resume CPR"
            ],
            indications=["VF/VT arrest"],
            contraindications=["asystole", "PEA"],
            complications=["skin burns", "arrhythmia", "equipment failure"],
            required_equipment=["defibrillator", "pads", "gel"],
            success_rate=0.99,
            time_required=1,
            documentation="Defibrillation delivered for VF. Immediate CPR resumed."
        )
        procedures["cardioversion"] = Procedure(
            name="Synchronized Cardioversion",
            steps=[
                "Apply pads",
                "Set to sync mode",
                "Select energy",
                "Clear patient",
                "Deliver shock"
            ],
            indications=["unstable tachyarrhythmia"],
            contraindications=["sinus rhythm", "asystole"],
            complications=["skin burns", "arrhythmia", "embolism"],
            required_equipment=["defibrillator", "pads", "sedation"],
            success_rate=0.97,
            time_required=2,
            documentation="Synchronized cardioversion performed for unstable SVT."
        )
        procedures["external_pacing"] = Procedure(
            name="Transcutaneous Pacing",
            steps=[
                "Apply pads",
                "Set pacing rate and output",
                "Confirm capture",
                "Monitor patient"
            ],
            indications=["unstable bradycardia"],
            contraindications=["asystole", "VF"],
            complications=["discomfort", "skin burns", "failure to capture"],
            required_equipment=["pacer/defibrillator", "pads"],
            success_rate=0.95,
            time_required=3,
            documentation="Transcutaneous pacing initiated for bradycardia. Capture confirmed."
        )
        # Trauma
        procedures["fast_exam"] = Procedure(
            name="Focused Assessment with Sonography for Trauma (FAST)",
            steps=[
                "Apply ultrasound gel",
                "Scan RUQ, LUQ, pelvis, pericardium",
                "Interpret findings"
            ],
            indications=["blunt trauma", "hypotension"],
            contraindications=[],
            complications=["missed injury", "false positive/negative"],
            required_equipment=["ultrasound machine", "gel"],
            success_rate=0.98,
            time_required=5,
            documentation="FAST exam performed, no free fluid identified."
        )
        procedures["pelvic_binder"] = Procedure(
            name="Pelvic Binder Placement",
            steps=[
                "Position binder at greater trochanters",
                "Tighten and secure binder"
            ],
            indications=["pelvic fracture", "unstable pelvis"],
            contraindications=["open pelvic wound"],
            complications=["skin breakdown", "nerve injury"],
            required_equipment=["pelvic binder"],
            success_rate=0.99,
            time_required=1,
            documentation="Pelvic binder placed for unstable pelvic fracture."
        )
        # Neuro
        procedures["lumbar_puncture"] = Procedure(
            name="Lumbar Puncture",
            steps=[
                "Position patient",
                "Prep and drape",
                "Identify L3-L4/L4-L5 space",
                "Insert spinal needle",
                "Collect CSF",
                "Remove needle and apply dressing"
            ],
            indications=["meningitis workup", "subarachnoid hemorrhage"],
            contraindications=["increased ICP", "coagulopathy", "infection at site"],
            complications=["headache", "bleeding", "infection", "herniation"],
            required_equipment=["spinal needle", "sterile kit", "manometer"],
            success_rate=0.95,
            time_required=15,
            documentation="LP performed, clear CSF obtained."
        )
        # GI
        procedures["ng_tube"] = Procedure(
            name="Nasogastric Tube Placement",
            steps=[
                "Measure and mark tube",
                "Lubricate",
                "Insert via nostril",
                "Advance to oropharynx",
                "Have patient swallow",
                "Advance to stomach",
                "Confirm placement (aspirate, CXR)"
            ],
            indications=["bowel obstruction", "GI bleed", "decompression"],
            contraindications=["basilar skull fracture", "esophageal varices"],
            complications=["epistaxis", "misplacement", "aspiration"],
            required_equipment=["NG tube", "lubricant", "syringe", "CXR"],
            success_rate=0.96,
            time_required=6,
            documentation="NG tube placed, placement confirmed by aspirate and CXR."
        )
        procedures["paracentesis"] = Procedure(
            name="Paracentesis",
            steps=[
                "Prep and drape",
                "Identify site (US guidance preferred)",
                "Anesthetize",
                "Insert needle/catheter",
                "Aspirate fluid",
                "Remove needle, apply dressing"
            ],
            indications=["ascites", "diagnostic workup"],
            contraindications=["infection at site", "coagulopathy"],
            complications=["bleeding", "infection", "bowel perforation"],
            required_equipment=["paracentesis kit", "ultrasound", "dressing"],
            success_rate=0.97,
            time_required=10,
            documentation="Paracentesis performed, clear fluid obtained."
        )
        # OB/GYN
        procedures["vaginal_delivery"] = Procedure(
            name="Vaginal Delivery",
            steps=[
                "Prepare delivery area",
                "Support perineum",
                "Deliver head, check for nuchal cord",
                "Deliver shoulders and body",
                "Clamp and cut cord",
                "Deliver placenta"
            ],
            indications=["term pregnancy, labor"],
            contraindications=["malpresentation", "placenta previa"],
            complications=["postpartum hemorrhage", "shoulder dystocia", "perineal tear"],
            required_equipment=["delivery kit", "clamps", "suction", "warm blankets"],
            success_rate=0.99,
            time_required=30,
            documentation="Vaginal delivery performed, healthy infant delivered."
        )
        # Pediatrics
        procedures["broselow_tape"] = Procedure(
            name="Broselow Tape Assessment",
            steps=[
                "Lay child on tape",
                "Read weight/medication zone",
                "Select equipment/doses accordingly"
            ],
            indications=["pediatric resuscitation"],
            contraindications=[],
            complications=["incorrect zone selection"],
            required_equipment=["Broselow tape"],
            success_rate=0.99,
            time_required=1,
            documentation="Broselow tape used for pediatric dosing/equipment selection."
        )
        return procedures

    def _initialize_protocols(self):
        protocols = {}
        protocols["acls"] = Protocol(
            name="ACLS/Cardiac Arrest Algorithm",
            steps=[
                "Start CPR",
                "Attach monitor/defibrillator",
                "Identify rhythm",
                "Defibrillate if indicated",
                "Administer epinephrine/amiodarone",
                "Airway management",
                "Reversible causes",
                "Post-arrest care"
            ],
            indications=["cardiac arrest"],
            contraindications=[],
            bundled_orders=["defibrillation", "intubation", "epinephrine", "amiodarone"],
            documentation="ACLS protocol followed for cardiac arrest."
        )
        protocols["sepsis"] = Protocol(
            name="Sepsis Bundle",
            steps=[
                "Obtain cultures",
                "Administer broad-spectrum antibiotics",
                "Administer IV fluids",
                "Check lactate",
                "Start vasopressors if needed",
                "Monitor urine output"
            ],
            indications=["suspected sepsis", "septic shock"],
            contraindications=[],
            bundled_orders=["blood_cultures", "ceftriaxone", "normal_saline", "norepinephrine"],
            documentation="Sepsis bundle initiated per protocol."
        )
        protocols["stroke"] = Protocol(
            name="Acute Stroke Protocol",
            steps=[
                "Activate stroke team",
                "Obtain CT head",
                "Check glucose",
                "Assess tPA eligibility",
                "Administer tPA if indicated",
                "Monitor neuro status"
            ],
            indications=["acute stroke symptoms"],
            contraindications=["bleeding", "recent surgery"],
            bundled_orders=["ct_head", "glucose", "tpa"],
            documentation="Stroke protocol followed, tPA administered as indicated."
        )
        protocols["trauma"] = Protocol(
            name="Trauma/ATLS Protocol",
            steps=[
                "Primary survey (ABCDE)",
                "Resuscitation",
                "Secondary survey",
                "Imaging",
                "Definitive care"
            ],
            indications=["major trauma"],
            contraindications=[],
            bundled_orders=["fast_exam", "pelvic_binder", "blood_transfusion"],
            documentation="ATLS protocol followed for trauma patient."
        )
        protocols["dka"] = Protocol(
            name="DKA/HHS Protocol",
            steps=[
                "Start IV fluids",
                "Check glucose, electrolytes",
                "Start insulin infusion",
                "Monitor potassium",
                "Monitor for complications"
            ],
            indications=["DKA", "HHS"],
            contraindications=[],
            bundled_orders=["normal_saline", "insulin_regular", "potassium"],
            documentation="DKA protocol initiated. Insulin and fluids started."
        )
        protocols["massive_transfusion"] = Protocol(
            name="Massive Transfusion Protocol",
            steps=[
                "Activate protocol",
                "Order blood products (PRBC, FFP, platelets)",
                "Monitor calcium",
                "Monitor for complications"
            ],
            indications=["hemorrhagic shock", "major trauma"],
            contraindications=[],
            bundled_orders=["prbc", "ffp", "platelets", "calcium"],
            documentation="Massive transfusion protocol activated."
        )
        return protocols

    def perform_procedure(self, patient_id: str, procedure_name: str) -> dict:
        if procedure_name not in self.procedures:
            return {"success": False, "error": "procedure not found"}
        procedure = self.procedures[procedure_name]
        # Simulate success/failure
        success = random.random() < procedure.success_rate
        complications = []
        if not success:
            complications = [random.choice(procedure.complications)]
        # Record procedure
        record = {
            "patient_id": patient_id,
            "procedure": procedure_name,
            "success": success,
            "complications": complications,
            "timestamp": datetime.now().isoformat(),
            "documentation": procedure.documentation
        }
        self.procedure_history.append(record)
        return record


class AdvancedTreatmentSystem:
    """advanced treatment system with comprehensive medication management"""
    
    def __init__(self):
        self.medications = self._initialize_medications()
        self.active_orders = {}
        self.administration_history = []
        self.monitoring_alerts = []
        self.procedures = ProcedureSystem()  # Integrate procedure system
        
    def _initialize_medications(self) -> Dict[str, Medication]:
        """initialize comprehensive medication formulary"""
        medications = {}
        
        # antiplatelet agents
        medications["aspirin"] = Medication(
            name="Aspirin",
            category="Antiplatelet",
            mechanism="Irreversible COX-1 inhibition",
            indications=["ACS", "MI prevention", "stroke prevention"],
            contraindications=["active bleeding", "aspirin allergy", "severe liver disease"],
            side_effects=["gastrointestinal bleeding", "nausea", "dyspepsia"],
            drug_interactions=["warfarin", "clopidogrel", "ibuprofen"],
            dosing_adult={
                "loading": {"dose": 325, "unit": "mg", "route": "PO"},
                "maintenance": {"dose": 81, "unit": "mg", "route": "PO", "frequency": "daily"}
            },
            dosing_pediatric={
                "fever": {"dose": 10, "unit": "mg/kg", "route": "PO", "frequency": "q4-6h"}
            },
            description="Irreversible platelet inhibitor",
            onset_time=30,
            duration=1440,  # 24 hours
            monitoring_required=["bleeding", "platelet_count"]
        )
            
        # anticoagulants
        medications["heparin"] = Medication(
            name="Heparin",
            category="Anticoagulant",
            mechanism="Antithrombin III activation",
            indications=["DVT", "PE", "ACS", "atrial fibrillation"],
            contraindications=["active bleeding", "heparin allergy", "HIT"],
            side_effects=["bleeding", "thrombocytopenia", "osteoporosis"],
            drug_interactions=["aspirin", "clopidogrel", "warfarin"],
            dosing_adult={
                "loading": {"dose": 80, "unit": "units/kg", "route": "IV"},
                "maintenance": {"dose": 18, "unit": "units/kg/hr", "route": "IV"}
            },
            dosing_pediatric={
                "loading": {"dose": 75, "unit": "units/kg", "route": "IV"},
                "maintenance": {"dose": 20, "unit": "units/kg/hr", "route": "IV"}
            },
            description="Unfractionated heparin for anticoagulation",
            onset_time=5,
            duration=60,
            monitoring_required=["aPTT", "platelet_count", "HIT_antibodies"]
        )
        
        medications["warfarin"] = Medication(
            name="Warfarin",
            category="Anticoagulant",
            mechanism="Vitamin K antagonist",
            indications=["DVT", "PE", "atrial fibrillation", "mechanical valves"],
            contraindications=["active bleeding", "pregnancy", "severe liver disease"],
            side_effects=["bleeding", "skin necrosis", "teratogenicity"],
            drug_interactions=["aspirin", "amiodarone", "rifampin", "many_others"],
            dosing_adult={
                "loading": {"dose": 5, "unit": "mg", "route": "PO", "frequency": "daily"},
                "maintenance": {"dose": 2.5, "unit": "mg", "route": "PO", "frequency": "daily"}
            },
            dosing_pediatric={
                "loading": {"dose": 0.1, "unit": "mg/kg", "route": "PO", "frequency": "daily"},
                "maintenance": {"dose": 0.05, "unit": "mg/kg", "route": "PO", "frequency": "daily"}
            },
            description="Oral anticoagulant requiring INR monitoring",
            onset_time=1440,  # 24 hours
            duration=4320,  # 72 hours
            monitoring_required=["INR", "bleeding_signs"]
        )
        
        # antiarrhythmics
        medications["amiodarone"] = Medication(
            name="Amiodarone",
            category="Antiarrhythmic",
            mechanism="Class III antiarrhythmic",
            indications=["atrial fibrillation", "ventricular tachycardia", "cardiac arrest"],
            contraindications=["severe bradycardia", "second/third degree heart block", "thyroid disease"],
            side_effects=["pulmonary fibrosis", "thyroid dysfunction", "hepatotoxicity", "corneal deposits"],
            drug_interactions=["warfarin", "digoxin", "many_others"],
            dosing_adult={
                "loading": {"dose": 150, "unit": "mg", "route": "IV", "frequency": "over 10 min"},
                "maintenance": {"dose": 1, "unit": "mg/min", "route": "IV", "frequency": "for 6 hours"}
            },
            dosing_pediatric={
                "loading": {"dose": 5, "unit": "mg/kg", "route": "IV", "frequency": "over 10 min"}
            },
            description="Potent antiarrhythmic with multiple organ toxicities",
            onset_time=10,
            duration=480,
            monitoring_required=["ECG", "thyroid_function", "liver_function", "pulmonary_function"]
        )
        
        # beta blockers
        medications["metoprolol"] = Medication(
            name="Metoprolol",
            category="Beta Blocker",
            mechanism="Selective beta-1 adrenergic blockade",
            indications=["hypertension", "angina", "heart failure", "MI"],
            contraindications=["severe bradycardia", "heart block", "cardiogenic shock", "asthma"],
            side_effects=["bradycardia", "hypotension", "fatigue", "bronchospasm"],
            drug_interactions=["amiodarone", "digoxin", "verapamil"],
            dosing_adult={
                "loading": {"dose": 5, "unit": "mg", "route": "IV", "frequency": "q5min x3"},
                "maintenance": {"dose": 25, "unit": "mg", "route": "PO", "frequency": "bid"}
            },
            dosing_pediatric={
                "loading": {"dose": 0.1, "unit": "mg/kg", "route": "IV", "frequency": "q5min x3"}
            },
            description="Cardioselective beta blocker",
            onset_time=5,
            duration=360,
            monitoring_required=["heart_rate", "blood_pressure", "ECG"]
        )
        
        # calcium channel blockers
        medications["diltiazem"] = Medication(
            name="Diltiazem",
            category="Calcium Channel Blocker",
            mechanism="Calcium channel blockade",
            indications=["atrial fibrillation", "hypertension", "angina"],
            contraindications=["severe bradycardia", "heart block", "cardiogenic shock"],
            side_effects=["bradycardia", "hypotension", "constipation", "headache"],
            drug_interactions=["amiodarone", "digoxin", "beta_blockers"],
            dosing_adult={
                "loading": {"dose": 0.25, "unit": "mg/kg", "route": "IV", "frequency": "over 2 min"},
                "maintenance": {"dose": 5, "unit": "mg/hr", "route": "IV"}
            },
            dosing_pediatric={
                "loading": {"dose": 0.25, "unit": "mg/kg", "route": "IV", "frequency": "over 2 min"}
            },
            description="Calcium channel blocker for rate control",
            onset_time=3,
            duration=240,
            monitoring_required=["heart_rate", "blood_pressure", "ECG"]
        )
        
        # vasodilators
        medications["nitroglycerin"] = Medication(
            name="Nitroglycerin",
            category="Vasodilator",
            mechanism="Nitric oxide donor",
            indications=["angina", "hypertension", "heart failure"],
            contraindications=["severe hypotension", "right ventricular infarction", "viagra_use"],
            side_effects=["headache", "hypotension", "reflex tachycardia"],
            drug_interactions=["sildenafil", "tadalafil", "vardenafil"],
            dosing_adult={
                "sublingual": {"dose": 0.4, "unit": "mg", "route": "SL", "frequency": "q5min x3"},
                "iv": {"dose": 10, "unit": "mcg/min", "route": "IV", "frequency": "titrate"}
            },
            dosing_pediatric={
                "iv": {"dose": 0.5, "unit": "mcg/kg/min", "route": "IV", "frequency": "titrate"}
            },
            description="Potent vasodilator for acute coronary syndrome",
            onset_time=1,
            duration=30,
            monitoring_required=["blood_pressure", "heart_rate", "chest_pain"]
        )
        
        # diuretics
        medications["furosemide"] = Medication(
            name="Furosemide",
            category="Diuretic",
            mechanism="Loop diuretic",
            indications=["heart failure", "pulmonary edema", "hypertension"],
            contraindications=["anuria", "severe electrolyte depletion"],
            side_effects=["hypokalemia", "dehydration", "ototoxicity"],
            drug_interactions=["digoxin", "lithium", "aminoglycosides"],
            dosing_adult={
                "loading": {"dose": 40, "unit": "mg", "route": "IV", "frequency": "once"},
                "maintenance": {"dose": 20, "unit": "mg", "route": "PO", "frequency": "daily"}
            },
            dosing_pediatric={
                "loading": {"dose": 1, "unit": "mg/kg", "route": "IV", "frequency": "once"}
            },
            description="Loop diuretic for fluid overload",
            onset_time=5,
            duration=120,
            monitoring_required=["electrolytes", "renal_function", "weight"]
        )
        
        # analgesics
        medications["morphine"] = Medication(
            name="Morphine",
            category="Opioid Analgesic",
            mechanism="Mu-opioid receptor agonist",
            indications=["severe pain", "pulmonary edema", "end-of-life care"],
            contraindications=["respiratory depression", "acute bronchial asthma", "paralytic ileus"],
            side_effects=["respiratory depression", "sedation", "constipation", "nausea"],
            drug_interactions=["benzodiazepines", "alcohol", "other_opioids"],
            dosing_adult={
                "loading": {"dose": 2, "unit": "mg", "route": "IV", "frequency": "q5-15min"},
                "maintenance": {"dose": 0.1, "unit": "mg/kg", "route": "PO", "frequency": "q4h"}
            },
            dosing_pediatric={
                "loading": {"dose": 0.05, "unit": "mg/kg", "route": "IV", "frequency": "q5-15min"}
            },
            description="Potent opioid for severe pain",
            onset_time=5,
            duration=240,
            monitoring_required=["respiratory_rate", "sedation_level", "pain_score"]
        )
        
        # antibiotics
        medications["ceftriaxone"] = Medication(
            name="Ceftriaxone",
            category="Antibiotic",
            mechanism="Third-generation cephalosporin",
            indications=["pneumonia", "meningitis", "sepsis", "UTI"],
            contraindications=["ceftriaxone allergy", "severe penicillin allergy"],
            side_effects=["diarrhea", "allergic reactions", "gallbladder sludge"],
            drug_interactions=["calcium_containing_solutions", "warfarin"],
            dosing_adult={
                "loading": {"dose": 1, "unit": "g", "route": "IV", "frequency": "daily"},
                "maintenance": {"dose": 1, "unit": "g", "route": "IV", "frequency": "daily"}
            },
            dosing_pediatric={
                "loading": {"dose": 50, "unit": "mg/kg", "route": "IV", "frequency": "daily"}
            },
            description="Broad-spectrum cephalosporin antibiotic",
            onset_time=30,
            duration=1440,
            monitoring_required=["allergic_reactions", "renal_function"]
        )
        
        # bronchodilators
        medications["albuterol"] = Medication(
            name="Albuterol",
            category="Bronchodilator",
            mechanism="Beta-2 adrenergic agonist",
            indications=["asthma", "COPD", "bronchospasm"],
            contraindications=["hypersensitivity", "uncontrolled arrhythmia"],
            side_effects=["tachycardia", "tremor", "hypokalemia"],
            drug_interactions=["beta_blockers", "diuretics"],
            dosing_adult={
                "nebulized": {"dose": 2.5, "unit": "mg", "route": "nebulizer", "frequency": "q20min x3"},
                "inhaler": {"dose": 2, "unit": "puffs", "route": "inhaler", "frequency": "q4-6h"}
            },
            dosing_pediatric={
                "nebulized": {"dose": 0.15, "unit": "mg/kg", "route": "nebulizer", "frequency": "q20min x3"}
            },
            description="Short-acting beta-2 agonist for bronchospasm",
            onset_time=5,
            duration=240,
            monitoring_required=["respiratory_rate", "oxygen_saturation", "heart_rate"]
        )
        
        # antiemetics
        medications["ondansetron"] = Medication(
            name="Ondansetron",
            category="Antiemetic",
            mechanism="5-HT3 receptor antagonist",
            indications=["nausea", "vomiting", "chemotherapy-induced emesis"],
            contraindications=["ondansetron allergy", "concurrent apomorphine"],
            side_effects=["headache", "constipation", "QT prolongation"],
            drug_interactions=["apomorphine", "tramadol"],
            dosing_adult={
                "loading": {"dose": 4, "unit": "mg", "route": "IV", "frequency": "once"},
                "maintenance": {"dose": 8, "unit": "mg", "route": "PO", "frequency": "q8h"}
            },
            dosing_pediatric={
                "loading": {"dose": 0.15, "unit": "mg/kg", "route": "IV", "frequency": "once"}
            },
            description="Serotonin antagonist for nausea and vomiting",
            onset_time=15,
            duration=480,
            monitoring_required=["QT_interval", "nausea_vomiting"]
        )
        
        # antiplatelet agents
        medications["clopidogrel"] = Medication(
            name="Clopidogrel",
            category="Antiplatelet",
            mechanism="P2Y12 receptor antagonist",
            indications=["ACS", "PCI", "stroke prevention"],
            contraindications=["active bleeding", "clopidogrel allergy"],
            side_effects=["bleeding", "thrombotic thrombocytopenic purpura"],
            drug_interactions=["aspirin", "warfarin", "omeprazole"],
            dosing_adult={
                "loading": {"dose": 600, "unit": "mg", "route": "PO", "frequency": "once"},
                "maintenance": {"dose": 75, "unit": "mg", "route": "PO", "frequency": "daily"}
            },
            dosing_pediatric={
                "loading": {"dose": 1, "unit": "mg/kg", "route": "PO", "frequency": "once"}
            },
            description="P2Y12 inhibitor for antiplatelet therapy",
            onset_time=60,
            duration=1440,
            monitoring_required=["bleeding", "platelet_function"]
        )
        
        # ACE inhibitors
        medications["lisinopril"] = Medication(
            name="Lisinopril",
            category="ACE Inhibitor",
            mechanism="Angiotensin-converting enzyme inhibition",
            indications=["hypertension", "heart failure", "MI", "diabetic nephropathy"],
            contraindications=["angioedema", "pregnancy", "bilateral renal artery stenosis"],
            side_effects=["cough", "hyperkalemia", "angioedema", "renal dysfunction"],
            drug_interactions=["lithium", "potassium_sparing_diuretics", "NSAIDs"],
            dosing_adult={
                "loading": {"dose": 5, "unit": "mg", "route": "PO", "frequency": "daily"},
                "maintenance": {"dose": 10, "unit": "mg", "route": "PO", "frequency": "daily"}
            },
            dosing_pediatric={
                "loading": {"dose": 0.07, "unit": "mg/kg", "route": "PO", "frequency": "daily"}
            },
            description="ACE inhibitor for cardiovascular protection",
            onset_time=60,
            duration=1440,
            monitoring_required=["blood_pressure", "renal_function", "potassium"]
        )
        
        # statins
        medications["atorvastatin"] = Medication(
            name="Atorvastatin",
            category="Statin",
            mechanism="HMG-CoA reductase inhibition",
            indications=["hyperlipidemia", "cardiovascular risk reduction"],
            contraindications=["active liver disease", "pregnancy", "lactation"],
            side_effects=["myalgia", "hepatotoxicity", "rhabdomyolysis"],
            drug_interactions=["amiodarone", "verapamil", "gemfibrozil"],
            dosing_adult={
                "loading": {"dose": 10, "unit": "mg", "route": "PO", "frequency": "daily"},
                "maintenance": {"dose": 20, "unit": "mg", "route": "PO", "frequency": "daily"}
            },
            dosing_pediatric={
                "loading": {"dose": 10, "unit": "mg", "route": "PO", "frequency": "daily"}
            },
            description="HMG-CoA reductase inhibitor for lipid management",
            onset_time=1440,
            duration=1440,
            monitoring_required=["liver_function", "creatine_kinase", "lipid_panel"]
        )
        
        # Additional medications for comprehensive formulary
        medications["acetaminophen"] = Medication(
            name="Acetaminophen",
            category="Analgesic",
            mechanism="COX-2 inhibition",
            indications=["pain", "fever"],
            contraindications=["severe liver disease", "acetaminophen allergy"],
            side_effects=["hepatotoxicity", "allergic reaction", "overdose risk"],
            drug_interactions=["warfarin", "alcohol"],
            dosing_adult={
                "loading": {"dose": 650, "unit": "mg", "route": "PO", "frequency": "q4-6h"},
                "maintenance": {"dose": 1000, "unit": "mg", "route": "PO", "frequency": "q6h"}
            },
            dosing_pediatric={
                "loading": {"dose": 15, "unit": "mg/kg", "route": "PO", "frequency": "q4-6h"}
            },
            dosage_forms=["PO"],
            description="Non-opioid analgesic and antipyretic",
            onset_time=30,
            duration=240,
            monitoring_required=["liver_function", "overdose_signs"]
        )
        
        medications["ibuprofen"] = Medication(
            name="Ibuprofen",
            category="NSAID",
            mechanism="COX-1 and COX-2 inhibition",
            indications=["pain", "inflammation", "fever"],
            contraindications=["active peptic ulcer", "severe renal disease", "aspirin allergy"],
            side_effects=["gastrointestinal bleeding", "renal dysfunction", "hypertension"],
            drug_interactions=["aspirin", "warfarin", "ace_inhibitors"],
            dosing_adult={
                "loading": {"dose": 400, "unit": "mg", "route": "PO", "frequency": "q6-8h"},
                "maintenance": {"dose": 600, "unit": "mg", "route": "PO", "frequency": "q6-8h"}
            },
            dosing_pediatric={
                "loading": {"dose": 10, "unit": "mg/kg", "route": "PO", "frequency": "q6-8h"}
            },
            dosage_forms=["PO"],
            description="Non-steroidal anti-inflammatory drug",
            onset_time=30,
            duration=360,
            monitoring_required=["renal_function", "gastrointestinal_symptoms"]
        )
        
        medications["digoxin"] = Medication(
            name="Digoxin",
            category="Cardiac Glycoside",
            mechanism="Na+/K+ ATPase inhibition",
            indications=["heart failure", "atrial fibrillation"],
            contraindications=["severe bradycardia", "heart block", "digitalis toxicity"],
            side_effects=["bradycardia", "arrhythmias", "nausea", "visual changes"],
            drug_interactions=["amiodarone", "verapamil", "diuretics"],
            dosing_adult={
                "loading": {"dose": 0.5, "unit": "mg", "route": "PO", "frequency": "q8h x3"},
                "maintenance": {"dose": 0.125, "unit": "mg", "route": "PO", "frequency": "daily"}
            },
            dosing_pediatric={
                "loading": {"dose": 0.01, "unit": "mg/kg", "route": "PO", "frequency": "q8h x3"}
            },
            dosage_forms=["PO"],
            description="Cardiac glycoside for heart failure and rate control",
            onset_time=60,
            duration=1440,
            monitoring_required=["digoxin_level", "ECG", "renal_function"]
        )
        
        medications["insulin_regular"] = Medication(
            name="Insulin Regular",
            category="Insulin",
            mechanism="Glucose transport and metabolism",
            indications=["diabetes", "hyperglycemia", "diabetic ketoacidosis"],
            contraindications=["hypoglycemia", "insulin allergy"],
            side_effects=["hypoglycemia", "weight gain", "injection site reactions"],
            drug_interactions=["corticosteroids", "beta_blockers", "thiazide_diuretics"],
            dosing_adult={
                "loading": {"dose": 10, "unit": "units", "route": "SC", "frequency": "as needed"},
                "maintenance": {"dose": 0.5, "unit": "units/kg/day", "route": "SC", "frequency": "divided doses"}
            },
            dosing_pediatric={
                "loading": {"dose": 0.5, "unit": "units/kg", "route": "SC", "frequency": "as needed"}
            },
            dosage_forms=["SC"],
            description="Short-acting human insulin",
            onset_time=30,
            duration=360,
            monitoring_required=["blood_glucose", "hypoglycemia_signs"]
        )
        # End of medication definitions
        return medications
    
    def get_available_medications(self) -> List[str]:
        """get list of available medications"""
        return list(self.medications.keys())
    
    def get_medication_info(self, medication_name: str) -> Optional[Medication]:
        """get detailed information about a medication"""
        return self.medications.get(medication_name)
    
    def administer_medication(self, patient_id: str, medication_name: str, dose: str, route: str) -> Dict[str, Any]:
        """administer a medication to a patient"""
        if medication_name not in self.medications:
            return {"success": False, "error": "medication not found"}
        
        medication = self.medications[medication_name]
        
        # check if route is available
        if route not in medication.dosage_forms:
            return {"success": False, "error": f"route {route} not available for {medication_name}"}
        
        # create treatment record
        treatment = {
            'medication_name': medication_name,
            'dose': dose,
            'route': route,
            'administered_at': datetime.now().isoformat(),
            'effects': medication.effects.copy(),
            'side_effects': medication.side_effects.copy()
        }
        
        # add to active treatments
        if patient_id not in self.active_treatments:
            self.active_treatments[patient_id] = []
        
        self.active_treatments[patient_id].append(treatment)
        
        return {
            "success": True,
            "medication": medication_name,
            "dose": dose,
            "route": route,
            "cost": medication.cost,
            "effects": medication.effects,
            "side_effects": medication.side_effects
        }
    
    def get_active_treatments(self, patient_id: str) -> List[Dict[str, Any]]:
        """get active treatments for a patient"""
        return self.active_treatments.get(patient_id, [])
    
    def get_medication_effects(self, patient_id: str) -> Dict[str, Any]:
        """get cumulative medication effects for a patient"""
        if patient_id not in self.active_treatments:
            return {}
        
        cumulative_effects = {}
        for treatment in self.active_treatments[patient_id]:
            for effect, value in treatment['effects'].items():
                if effect in cumulative_effects:
                    # combine effects (simplified logic)
                    if isinstance(value, bool):
                        cumulative_effects[effect] = cumulative_effects[effect] or value
                    elif isinstance(value, (int, float)):
                        cumulative_effects[effect] = cumulative_effects[effect] + value
                else:
                    cumulative_effects[effect] = value
        
        return cumulative_effects
    
    def search_medications(self, category: str = None, route: str = None) -> List[str]:
        """search medications by category or route"""
        results = []
        
        for name, medication in self.medications.items():
            if category and medication.category.lower() != category.lower():
                continue
            if route and route not in medication.dosage_forms:
                continue
            results.append(name)
        
        return results
    
    def get_medication_categories(self) -> List[str]:
        """get all medication categories"""
        categories = set()
        for medication in self.medications.values():
            categories.add(medication.category)
        return list(categories)
    
    def get_medication_by_category(self, category: str) -> List[str]:
        """get medications by category"""
        return [name for name, med in self.medications.items() 
                if med.category.lower() == category.lower()]
    
    def check_contraindications(self, medication_name: str, patient_conditions: List[str]) -> List[str]:
        """check for contraindications"""
        if medication_name not in self.medications:
            return ["medication not found"]
        
        medication = self.medications[medication_name]
        contraindications = []
        
        for condition in patient_conditions:
            if condition.lower() in [c.lower() for c in medication.contraindications]:
                contraindications.append(condition)
        
        return contraindications 