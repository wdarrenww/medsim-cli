"""
Enhanced Physiological Engine
provides comprehensive multi-organ system modeling with disease progression
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import math
import random
from enum import Enum

class OrganSystem(Enum):
    """organ systems"""
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    RENAL = "renal"
    ENDOCRINE = "endocrine"
    NEUROLOGICAL = "neurological"
    GASTROINTESTINAL = "gastrointestinal"
    HEMATOLOGICAL = "hematological"
    IMMUNE = "immune"
    HEPATIC = "hepatic"
    MUSCULOSKELETAL = "musculoskeletal"

class DiseaseState(Enum):
    """disease progression states"""
    NORMAL = "normal"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"

@dataclass
class CardiovascularSystem:
    """cardiovascular system parameters"""
    # hemodynamics
    cardiac_output: float = 5.0  # L/min
    stroke_volume: float = 70.0  # mL
    heart_rate: int = 80  # bpm
    blood_pressure_systolic: int = 120  # mmHg
    blood_pressure_diastolic: int = 80  # mmHg
    mean_arterial_pressure: float = 93.3  # mmHg
    
    # cardiac function
    ejection_fraction: float = 0.65  # 65%
    cardiac_index: float = 3.0  # L/min/m²
    systemic_vascular_resistance: float = 1200  # dyn·s/cm⁵
    
    # rhythm
    rhythm: str = "normal sinus"
    conduction_abnormalities: List[str] = field(default_factory=list)
    
    # disease states
    disease_state: DiseaseState = DiseaseState.NORMAL
    conditions: List[str] = field(default_factory=list)
    
    def update_from_stress(self, stress_level: float):
        """update cv parameters based on stress"""
        if stress_level > 0.7:  # high stress
            self.heart_rate = min(150, self.heart_rate + 20)
            self.blood_pressure_systolic = min(180, self.blood_pressure_systolic + 15)
            self.cardiac_output = min(8.0, self.cardiac_output + 1.5)
        elif stress_level > 0.3:  # moderate stress
            self.heart_rate = min(120, self.heart_rate + 10)
            self.blood_pressure_systolic = min(160, self.blood_pressure_systolic + 8)
            self.cardiac_output = min(6.5, self.cardiac_output + 0.8)
        
        self.mean_arterial_pressure = self.blood_pressure_diastolic + (self.blood_pressure_systolic - self.blood_pressure_diastolic) / 3

@dataclass
class RespiratorySystem:
    """respiratory system parameters"""
    # ventilation
    respiratory_rate: int = 16  # breaths/min
    tidal_volume: float = 500.0  # mL
    minute_ventilation: float = 8.0  # L/min
    vital_capacity: float = 4.5  # L
    fev1: float = 3.6  # L (forced expiratory volume in 1 second)
    
    # gas exchange
    oxygen_saturation: float = 98.0  # %
    pao2: float = 95.0  # mmHg (arterial oxygen pressure)
    paco2: float = 40.0  # mmHg (arterial carbon dioxide pressure)
    ph: float = 7.40
    
    # mechanics
    peak_inspiratory_pressure: float = 20.0  # cmH2O
    positive_end_expiratory_pressure: float = 5.0  # cmH2O
    
    # disease states
    disease_state: DiseaseState = DiseaseState.NORMAL
    conditions: List[str] = field(default_factory=list)
    
    def update_from_stress(self, stress_level: float):
        """update respiratory parameters based on stress"""
        if stress_level > 0.7:  # high stress
            self.respiratory_rate = min(30, self.respiratory_rate + 8)
            self.minute_ventilation = min(15.0, self.minute_ventilation + 2.0)
        elif stress_level > 0.3:  # moderate stress
            self.respiratory_rate = min(24, self.respiratory_rate + 4)
            self.minute_ventilation = min(12.0, self.minute_ventilation + 1.0)

@dataclass
class RenalSystem:
    """renal system parameters"""
    # function
    glomerular_filtration_rate: float = 100.0  # mL/min
    creatinine: float = 1.0  # mg/dL
    bun: float = 15.0  # mg/dL
    urine_output: float = 1.0  # mL/kg/hr
    
    # electrolytes
    sodium: float = 140.0  # mEq/L
    potassium: float = 4.0  # mEq/L
    chloride: float = 102.0  # mEq/L
    bicarbonate: float = 24.0  # mEq/L
    
    # acid-base
    ph: float = 7.40
    base_excess: float = 0.0  # mEq/L
    
    # disease states
    disease_state: DiseaseState = DiseaseState.NORMAL
    conditions: List[str] = field(default_factory=list)
    
    def update_from_stress(self, stress_level: float):
        """update renal parameters based on stress"""
        if stress_level > 0.7:  # high stress - reduced perfusion
            self.urine_output = max(0.3, self.urine_output - 0.3)
            self.glomerular_filtration_rate = max(60.0, self.glomerular_filtration_rate - 10.0)

@dataclass
class EndocrineSystem:
    """endocrine system parameters"""
    # glucose metabolism
    blood_glucose: float = 100.0  # mg/dL
    hba1c: float = 5.7  # %
    insulin_level: float = 10.0  # μU/mL
    glucagon_level: float = 50.0  # pg/mL
    
    # thyroid function
    tsh: float = 2.5  # μIU/mL
    free_t4: float = 1.2  # ng/dL
    free_t3: float = 3.2  # pg/mL
    
    # adrenal function
    cortisol: float = 15.0  # μg/dL
    aldosterone: float = 10.0  # ng/dL
    
    # disease states
    disease_state: DiseaseState = DiseaseState.NORMAL
    conditions: List[str] = field(default_factory=list)
    
    def update_from_stress(self, stress_level: float):
        """update endocrine parameters based on stress"""
        if stress_level > 0.7:  # high stress
            self.cortisol = min(30.0, self.cortisol + 8.0)
            self.blood_glucose = min(200.0, self.blood_glucose + 20.0)
        elif stress_level > 0.3:  # moderate stress
            self.cortisol = min(25.0, self.cortisol + 5.0)
            self.blood_glucose = min(150.0, self.blood_glucose + 10.0)

@dataclass
class NeurologicalSystem:
    """neurological system parameters"""
    # consciousness
    glasgow_coma_scale: int = 15
    consciousness_level: str = "alert"
    orientation: str = "oriented"
    
    # cognitive function
    memory: str = "intact"
    attention: str = "normal"
    language: str = "normal"
    
    # motor function
    motor_strength: Dict[str, int] = field(default_factory=lambda: {
        "right_arm": 5, "left_arm": 5, "right_leg": 5, "left_leg": 5
    })
    reflexes: Dict[str, str] = field(default_factory=lambda: {
        "biceps": "2+", "triceps": "2+", "patellar": "2+", "achilles": "2+"
    })
    
    # sensory function
    sensation: str = "intact"
    vision: str = "normal"
    hearing: str = "normal"
    
    # disease states
    disease_state: DiseaseState = DiseaseState.NORMAL
    conditions: List[str] = field(default_factory=list)
    
    def update_from_stress(self, stress_level: float):
        """update neurological parameters based on stress"""
        if stress_level > 0.8:  # very high stress
            self.consciousness_level = "anxious"
            self.attention = "distracted"

@dataclass
class GastrointestinalSystem:
    """gastrointestinal system parameters"""
    # motility
    bowel_sounds: str = "normal"
    bowel_movements: str = "normal"
    
    # liver function
    alt: float = 25.0  # U/L
    ast: float = 25.0  # U/L
    alkaline_phosphatase: float = 70.0  # U/L
    total_bilirubin: float = 1.0  # mg/dL
    albumin: float = 4.0  # g/dL
    
    # pancreas
    amylase: float = 60.0  # U/L
    lipase: float = 30.0  # U/L
    
    # symptoms
    nausea: bool = False
    vomiting: bool = False
    abdominal_pain: bool = False
    diarrhea: bool = False
    
    # disease states
    disease_state: DiseaseState = DiseaseState.NORMAL
    conditions: List[str] = field(default_factory=list)
    
    def update_from_stress(self, stress_level: float):
        """update gi parameters based on stress"""
        if stress_level > 0.7:  # high stress
            if random.random() < 0.3:
                self.nausea = True
            if random.random() < 0.2:
                self.abdominal_pain = True

@dataclass
class HematologicalSystem:
    """hematological system parameters"""
    # red blood cells
    hemoglobin: float = 14.0  # g/dL
    hematocrit: float = 42.0  # %
    red_blood_cell_count: float = 4.8  # million/μL
    mcv: float = 90.0  # fL (mean corpuscular volume)
    mch: float = 30.0  # pg (mean corpuscular hemoglobin)
    mchc: float = 34.0  # g/dL (mean corpuscular hemoglobin concentration)
    
    # white blood cells
    white_blood_cell_count: float = 7.5  # thousand/μL
    neutrophils: float = 4.5  # thousand/μL
    lymphocytes: float = 2.0  # thousand/μL
    monocytes: float = 0.5  # thousand/μL
    eosinophils: float = 0.2  # thousand/μL
    basophils: float = 0.1  # thousand/μL
    
    # platelets
    platelet_count: float = 250.0  # thousand/μL
    
    # coagulation
    pt: float = 12.0  # seconds
    inr: float = 1.0
    ptt: float = 30.0  # seconds
    fibrinogen: float = 300.0  # mg/dL
    
    # disease states
    disease_state: DiseaseState = DiseaseState.NORMAL
    conditions: List[str] = field(default_factory=list)
    
    def update_from_stress(self, stress_level: float):
        """update hematological parameters based on stress"""
        if stress_level > 0.7:  # high stress
            self.white_blood_cell_count = min(15.0, self.white_blood_cell_count + 2.0)
            self.neutrophils = min(8.0, self.neutrophils + 1.5)

@dataclass
class ImmuneSystem:
    """immune system parameters"""
    # inflammatory markers
    crp: float = 3.0  # mg/L
    esr: float = 15.0  # mm/hr
    ferritin: float = 100.0  # ng/mL
    
    # cytokines
    il6: float = 2.0  # pg/mL
    tnf_alpha: float = 5.0  # pg/mL
    
    # immune function
    cd4_count: float = 800.0  # cells/μL
    cd8_count: float = 500.0  # cells/μL
    nk_cells: float = 200.0  # cells/μL
    
    # disease states
    disease_state: DiseaseState = DiseaseState.NORMAL
    conditions: List[str] = field(default_factory=list)
    
    def update_from_stress(self, stress_level: float):
        """update immune parameters based on stress"""
        if stress_level > 0.7:  # high stress
            self.crp = min(20.0, self.crp + 5.0)
            self.il6 = min(15.0, self.il6 + 3.0)

@dataclass
class HepaticSystem:
    """hepatic system parameters"""
    # liver function tests
    alt: float = 25.0  # U/L
    ast: float = 25.0  # U/L
    alkaline_phosphatase: float = 70.0  # U/L
    ggt: float = 30.0  # U/L
    total_bilirubin: float = 1.0  # mg/dL
    direct_bilirubin: float = 0.3  # mg/dL
    indirect_bilirubin: float = 0.7  # mg/dL
    albumin: float = 4.0  # g/dL
    total_protein: float = 7.0  # g/dL
    
    # synthetic function
    pt: float = 12.0  # seconds
    inr: float = 1.0
    factor_vii: float = 100.0  # %
    
    # disease states
    disease_state: DiseaseState = DiseaseState.NORMAL
    conditions: List[str] = field(default_factory=list)
    
    def update_from_stress(self, stress_level: float):
        """update hepatic parameters based on stress"""
        if stress_level > 0.8:  # very high stress
            self.alt = min(50.0, self.alt + 5.0)
            self.ast = min(50.0, self.ast + 5.0)

@dataclass
class MusculoskeletalSystem:
    """musculoskeletal system parameters"""
    # muscle function
    muscle_strength: Dict[str, int] = field(default_factory=lambda: {
        "upper_extremities": 5, "lower_extremities": 5, "grip": 5
    })
    
    # joint function
    joint_range_of_motion: Dict[str, str] = field(default_factory=lambda: {
        "shoulders": "normal", "elbows": "normal", "wrists": "normal",
        "hips": "normal", "knees": "normal", "ankles": "normal"
    })
    
    # bone health
    bone_density: str = "normal"
    calcium: float = 9.5  # mg/dL
    vitamin_d: float = 30.0  # ng/mL
    
    # symptoms
    pain: Dict[str, int] = field(default_factory=dict)  # 0-10 scale
    stiffness: Dict[str, bool] = field(default_factory=dict)
    weakness: Dict[str, bool] = field(default_factory=dict)
    
    # disease states
    disease_state: DiseaseState = DiseaseState.NORMAL
    conditions: List[str] = field(default_factory=list)
    
    def update_from_stress(self, stress_level: float):
        """update musculoskeletal parameters based on stress"""
        if stress_level > 0.7:  # high stress
            if random.random() < 0.4:
                self.pain["general"] = min(5, random.randint(1, 3))

@dataclass
class DermatologicalSystem:
    wounds: list = field(default_factory=list)
    rashes: list = field(default_factory=list)
    burns: list = field(default_factory=list)
    turgor: str = 'normal'
    hydration: str = 'normal'
    def update_from_stress(self, stress_level: float):
        if stress_level > 0.7 and random.random() < 0.1:
            self.turgor = 'decreased'

@dataclass
class ReproductiveSystem:
    pregnancy_status: str = 'not_pregnant'
    menstrual_cycle_day: int = 0
    hormone_levels: dict = field(default_factory=lambda: {'estrogen': 0, 'progesterone': 0, 'testosterone': 0})
    sexual_health: str = 'normal'
    def update_from_stress(self, stress_level: float):
        if self.pregnancy_status == 'pregnant' and stress_level > 0.8:
            self.hormone_levels['progesterone'] = max(0, self.hormone_levels['progesterone'] - 1)

@dataclass
class OphthalmologicSystem:
    vision: str = 'normal'
    eye_trauma: bool = False
    infection: bool = False
    def update_from_stress(self, stress_level: float):
        if stress_level > 0.9 and random.random() < 0.05:
            self.vision = 'blurred'

@dataclass
class OtolaryngologicSystem:
    hearing: str = 'normal'
    balance: str = 'normal'
    airway: str = 'patent'
    infection: bool = False
    def update_from_stress(self, stress_level: float):
        if stress_level > 0.8 and random.random() < 0.05:
            self.hearing = 'decreased'

@dataclass
class PediatricSystem:
    growth_percentile: float = 50.0
    congenital_conditions: list = field(default_factory=list)
    vaccination_status: str = 'up_to_date'
    def update_from_stress(self, stress_level: float):
        if stress_level > 0.7 and random.random() < 0.1:
            self.growth_percentile = max(0, self.growth_percentile - 1)

@dataclass
class GeriatricSystem:
    frailty_index: float = 0.0
    polypharmacy: int = 0
    cognitive_decline: bool = False
    def update_from_stress(self, stress_level: float):
        if stress_level > 0.6:
            self.frailty_index = min(1.0, self.frailty_index + 0.01)

@dataclass
class PsychiatricSystem:
    mood: str = 'stable'
    cognition: str = 'intact'
    substance_use: str = 'none'
    def update_from_stress(self, stress_level: float):
        if stress_level > 0.7:
            self.mood = 'anxious'

class EnhancedPhysiologicalEngine:
    """enhanced physiological engine with multi-organ system modeling"""
    
    def __init__(self):
        self.cardiovascular = CardiovascularSystem()
        self.respiratory = RespiratorySystem()
        self.renal = RenalSystem()
        self.endocrine = EndocrineSystem()
        self.neurological = NeurologicalSystem()
        self.gastrointestinal = GastrointestinalSystem()
        self.hematological = HematologicalSystem()
        self.immune = ImmuneSystem()
        self.hepatic = HepaticSystem()
        self.musculoskeletal = MusculoskeletalSystem()
        self.dermatological = DermatologicalSystem()
        self.reproductive = ReproductiveSystem()
        self.ophthalmologic = OphthalmologicSystem()
        self.otolaryngologic = OtolaryngologicSystem()
        self.pediatric = PediatricSystem()
        self.geriatric = GeriatricSystem()
        self.psychiatric = PsychiatricSystem()
        
        self.medications: List[Dict[str, Any]] = []
        self.diseases: List[Dict[str, Any]] = []
        self.time_step: int = 0
        
    def update_systems(self, stress_level: float = 0.0, medications: List[Dict[str, Any]] = None):
        """update all physiological systems"""
        if medications is None:
            medications = []
        
        self.medications = medications
        self.time_step += 1
        
        # update each system
        self.cardiovascular.update_from_stress(stress_level)
        self.respiratory.update_from_stress(stress_level)
        self.renal.update_from_stress(stress_level)
        self.endocrine.update_from_stress(stress_level)
        self.neurological.update_from_stress(stress_level)
        self.gastrointestinal.update_from_stress(stress_level)
        self.hematological.update_from_stress(stress_level)
        self.immune.update_from_stress(stress_level)
        self.hepatic.update_from_stress(stress_level)
        self.musculoskeletal.update_from_stress(stress_level)
        self.dermatological.update_from_stress(stress_level)
        self.reproductive.update_from_stress(stress_level)
        self.ophthalmologic.update_from_stress(stress_level)
        self.otolaryngologic.update_from_stress(stress_level)
        self.pediatric.update_from_stress(stress_level)
        self.geriatric.update_from_stress(stress_level)
        self.psychiatric.update_from_stress(stress_level)
        
        # apply medication effects
        self._apply_medication_effects()
        
        # apply disease effects
        self._apply_disease_effects()
        
        # cross-system interactions
        self._update_cross_system_interactions()
    
    def _apply_medication_effects(self):
        """apply effects of current medications"""
        for med in self.medications:
            med_name = med.get("name", "").lower()
            dose = med.get("dose", 0)
            
            # cardiovascular medications
            if "propranolol" in med_name or "metoprolol" in med_name:
                self.cardiovascular.heart_rate = max(50, self.cardiovascular.heart_rate - 10)
                self.cardiovascular.blood_pressure_systolic = max(90, self.cardiovascular.blood_pressure_systolic - 10)
            
            elif "lisinopril" in med_name or "enalapril" in med_name:
                self.cardiovascular.blood_pressure_systolic = max(90, self.cardiovascular.blood_pressure_systolic - 15)
                self.cardiovascular.blood_pressure_diastolic = max(60, self.cardiovascular.blood_pressure_diastolic - 8)
                self.renal.potassium = min(6.0, self.renal.potassium + 0.5)
            
            elif "amlodipine" in med_name:
                self.cardiovascular.blood_pressure_systolic = max(90, self.cardiovascular.blood_pressure_systolic - 12)
                self.cardiovascular.blood_pressure_diastolic = max(60, self.cardiovascular.blood_pressure_diastolic - 6)
            
            elif "digoxin" in med_name:
                self.cardiovascular.heart_rate = max(50, self.cardiovascular.heart_rate - 15)
                if dose > 2.0:  # toxicity
                    self.neurological.consciousness_level = "confused"
                    self.gastrointestinal.nausea = True
            
            elif "nitroglycerin" in med_name:
                self.cardiovascular.blood_pressure_systolic = max(80, self.cardiovascular.blood_pressure_systolic - 20)
                self.cardiovascular.blood_pressure_diastolic = max(50, self.cardiovascular.blood_pressure_diastolic - 10)
            
            # diuretics
            elif "furosemide" in med_name:
                self.renal.urine_output = min(3.0, self.renal.urine_output + 0.5)
                self.renal.sodium = max(130, self.renal.sodium - 2)
                self.renal.potassium = max(3.0, self.renal.potassium - 0.3)
                self.renal.chloride = max(95, self.renal.chloride - 3)
            
            elif "hydrochlorothiazide" in med_name:
                self.renal.urine_output = min(2.5, self.renal.urine_output + 0.3)
                self.renal.sodium = max(130, self.renal.sodium - 1)
                self.renal.potassium = max(3.0, self.renal.potassium - 0.2)
            
            # endocrine medications
            elif "insulin" in med_name:
                self.endocrine.blood_glucose = max(70, self.endocrine.blood_glucose - 30)
                if dose > 10:  # hypoglycemia
                    self.neurological.consciousness_level = "confused"
                    self.cardiovascular.heart_rate = min(120, self.cardiovascular.heart_rate + 10)
            
            elif "metformin" in med_name:
                self.endocrine.blood_glucose = max(70, self.endocrine.blood_glucose - 20)
                if self.renal.creatinine > 1.5:  # contraindicated
                    self.gastrointestinal.nausea = True
            
            elif "glipizide" in med_name:
                self.endocrine.blood_glucose = max(70, self.endocrine.blood_glucose - 25)
            
            # antibiotics
            elif "penicillin" in med_name or "amoxicillin" in med_name:
                self.immune.crp = max(3.0, self.immune.crp - 2.0)
                self.immune.il6 = max(2.0, self.immune.il6 - 1.0)
            
            elif "vancomycin" in med_name:
                self.immune.crp = max(3.0, self.immune.crp - 3.0)
                if dose > 15:  # nephrotoxicity
                    self.renal.creatinine = min(3.0, self.renal.creatinine + 0.5)
            
            elif "gentamicin" in med_name:
                self.immune.crp = max(3.0, self.immune.crp - 2.5)
                if dose > 5:  # nephrotoxicity
                    self.renal.creatinine = min(3.0, self.renal.creatinine + 0.3)
                    self.neurological.hearing = "decreased"
            
            # anticoagulants
            elif "warfarin" in med_name:
                self.hematological.pt = min(25, self.hematological.pt + 5)
                self.hematological.inr = min(3.5, self.hematological.inr + 0.8)
            
            elif "heparin" in med_name:
                self.hematological.ptt = min(60, self.hematological.ptt + 15)
            
            elif "apixaban" in med_name or "rivaroxaban" in med_name:
                self.hematological.pt = min(20, self.hematological.pt + 2)
                self.hematological.inr = min(2.5, self.hematological.inr + 0.3)
            
            # antiplatelets
            elif "aspirin" in med_name:
                self.hematological.platelet_count = max(150, self.hematological.platelet_count - 20)
                if dose > 325:  # GI bleeding risk
                    self.gastrointestinal.abdominal_pain = True
            
            elif "clopidogrel" in med_name:
                self.hematological.platelet_count = max(150, self.hematological.platelet_count - 15)
            
            # pain medications
            elif "morphine" in med_name or "fentanyl" in med_name:
                self.respiratory.respiratory_rate = max(8, self.respiratory.respiratory_rate - 4)
                self.neurological.consciousness_level = "sedated"
                if dose > 10:  # respiratory depression
                    self.respiratory.oxygen_saturation = max(85, self.respiratory.oxygen_saturation - 5)
            
            elif "acetaminophen" in med_name:
                if dose > 4000:  # hepatotoxicity
                    self.hepatic.alt = min(200.0, self.hepatic.alt + 50.0)
                    self.hepatic.ast = min(200.0, self.hepatic.ast + 50.0)
            
            elif "ibuprofen" in med_name:
                if dose > 2400:  # GI irritation
                    self.gastrointestinal.abdominal_pain = True
                    self.renal.creatinine = min(2.0, self.renal.creatinine + 0.2)
            
            # psychiatric medications
            elif "sertraline" in med_name or "fluoxetine" in med_name:
                self.psychiatric.mood = "improved"
                if dose > 100:  # serotonin syndrome
                    self.cardiovascular.heart_rate = min(150, self.cardiovascular.heart_rate + 15)
                    self.neurological.consciousness_level = "agitated"
            
            elif "alprazolam" in med_name or "lorazepam" in med_name:
                self.neurological.consciousness_level = "sedated"
                self.respiratory.respiratory_rate = max(10, self.respiratory.respiratory_rate - 2)
            
            # steroids
            elif "prednisone" in med_name or "methylprednisolone" in med_name:
                self.endocrine.cortisol = min(40.0, self.endocrine.cortisol + 10.0)
                self.endocrine.blood_glucose = min(200, self.endocrine.blood_glucose + 15)
                self.immune.white_blood_cell_count = min(20.0, self.immune.white_blood_cell_count + 3.0)
            
            # vasopressors
            elif "epinephrine" in med_name:
                self.cardiovascular.heart_rate = min(150, self.cardiovascular.heart_rate + 30)
                self.cardiovascular.blood_pressure_systolic = min(200, self.cardiovascular.blood_pressure_systolic + 30)
                self.respiratory.respiratory_rate = min(35, self.respiratory.respiratory_rate + 8)
            
            elif "norepinephrine" in med_name:
                self.cardiovascular.blood_pressure_systolic = min(200, self.cardiovascular.blood_pressure_systolic + 25)
                self.cardiovascular.blood_pressure_diastolic = min(120, self.cardiovascular.blood_pressure_diastolic + 15)
            
            # inotropes
            elif "dobutamine" in med_name:
                self.cardiovascular.heart_rate = min(150, self.cardiovascular.heart_rate + 20)
                self.cardiovascular.cardiac_output = min(8.0, self.cardiovascular.cardiac_output + 1.5)
            
            # antiarrhythmics
            elif "amiodarone" in med_name:
                self.cardiovascular.heart_rate = max(50, self.cardiovascular.heart_rate - 15)
                if dose > 400:  # pulmonary toxicity
                    self.respiratory.oxygen_saturation = max(90, self.respiratory.oxygen_saturation - 3)
            
            # statins
            elif "atorvastatin" in med_name or "simvastatin" in med_name:
                if dose > 80:  # myopathy
                    self.musculoskeletal.pain["general"] = min(5, self.musculoskeletal.pain.get("general", 0) + 2)
                    self.hepatic.alt = min(100.0, self.hepatic.alt + 20.0)
    
    def _apply_disease_effects(self):
        """apply effects of current diseases"""
        for disease in self.diseases:
            disease_name = disease.get("name", "").lower()
            severity = disease.get("severity", 1.0)
            
            # cardiovascular diseases
            if "hypertension" in disease_name:
                self.cardiovascular.blood_pressure_systolic = min(200, self.cardiovascular.blood_pressure_systolic + int(20 * severity))
                self.cardiovascular.blood_pressure_diastolic = min(120, self.cardiovascular.blood_pressure_diastolic + int(10 * severity))
            
            elif "heart failure" in disease_name:
                self.cardiovascular.ejection_fraction = max(0.2, self.cardiovascular.ejection_fraction - 0.1 * severity)
                self.cardiovascular.cardiac_output = max(2.0, self.cardiovascular.cardiac_output - 1.0 * severity)
                self.renal.sodium = max(130, self.renal.sodium - 2 * severity)
            
            elif "atrial fibrillation" in disease_name:
                self.cardiovascular.rhythm = "atrial fibrillation"
                self.cardiovascular.heart_rate = min(150, self.cardiovascular.heart_rate + int(20 * severity))
            
            elif "myocardial infarction" in disease_name:
                self.cardiovascular.ejection_fraction = max(0.2, self.cardiovascular.ejection_fraction - 0.2 * severity)
                self.cardiovascular.heart_rate = min(150, self.cardiovascular.heart_rate + int(15 * severity))
                self.cardiovascular.blood_pressure_systolic = max(80, self.cardiovascular.blood_pressure_systolic - int(10 * severity))
            
            # respiratory diseases
            elif "pneumonia" in disease_name:
                self.respiratory.oxygen_saturation = max(85, self.respiratory.oxygen_saturation - int(5 * severity))
                self.respiratory.respiratory_rate = min(35, self.respiratory.respiratory_rate + int(5 * severity))
                self.immune.white_blood_cell_count = min(20.0, self.immune.white_blood_cell_count + 3.0 * severity)
            
            elif "asthma" in disease_name:
                self.respiratory.fev1 = max(1.0, self.respiratory.fev1 - 1.0 * severity)
                self.respiratory.respiratory_rate = min(35, self.respiratory.respiratory_rate + int(8 * severity))
            
            elif "copd" in disease_name:
                self.respiratory.fev1 = max(0.8, self.respiratory.fev1 - 1.5 * severity)
                self.respiratory.oxygen_saturation = max(90, self.respiratory.oxygen_saturation - int(3 * severity))
            
            # endocrine diseases
            elif "diabetes" in disease_name:
                self.endocrine.blood_glucose = min(300, self.endocrine.blood_glucose + int(50 * severity))
                self.endocrine.hba1c = min(12.0, self.endocrine.hba1c + severity)
                if severity > 0.7:
                    self.renal.creatinine = min(3.0, self.renal.creatinine + 0.5)
            
            elif "hyperthyroidism" in disease_name:
                self.cardiovascular.heart_rate = min(150, self.cardiovascular.heart_rate + int(20 * severity))
                self.endocrine.free_t4 = min(4.0, self.endocrine.free_t4 + 1.0 * severity)
                self.endocrine.tsh = max(0.1, self.endocrine.tsh - 1.0 * severity)
            
            elif "hypothyroidism" in disease_name:
                self.cardiovascular.heart_rate = max(50, self.cardiovascular.heart_rate - int(10 * severity))
                self.endocrine.free_t4 = max(0.5, self.endocrine.free_t4 - 0.5 * severity)
                self.endocrine.tsh = min(20.0, self.endocrine.tsh + 5.0 * severity)
            
            # renal diseases
            elif "kidney disease" in disease_name or "renal failure" in disease_name:
                self.renal.glomerular_filtration_rate = max(10.0, self.renal.glomerular_filtration_rate - 30.0 * severity)
                self.renal.creatinine = min(8.0, self.renal.creatinine + 2.0 * severity)
                self.renal.potassium = min(7.0, self.renal.potassium + 1.0 * severity)
                self.hematological.hemoglobin = max(8.0, self.hematological.hemoglobin - 2.0 * severity)
            
            # hepatic diseases
            elif "liver disease" in disease_name or "cirrhosis" in disease_name:
                self.hepatic.alt = min(200.0, self.hepatic.alt + 50.0 * severity)
                self.hepatic.ast = min(200.0, self.hepatic.ast + 50.0 * severity)
                self.hepatic.albumin = max(2.0, self.hepatic.albumin - 1.0 * severity)
                self.hematological.pt = min(25, self.hematological.pt + 5 * severity)
                self.hematological.inr = min(3.0, self.hematological.inr + 0.5 * severity)
            
            # neurological diseases
            elif "stroke" in disease_name:
                self.neurological.glasgow_coma_scale = max(3, self.neurological.glasgow_coma_scale - int(5 * severity))
                self.neurological.consciousness_level = "confused" if severity > 0.5 else "lethargic"
                if severity > 0.7:
                    self.neurological.motor_strength["right_arm"] = max(0, self.neurological.motor_strength["right_arm"] - 3)
                    self.neurological.motor_strength["right_leg"] = max(0, self.neurological.motor_strength["right_leg"] - 3)
            
            elif "seizure" in disease_name:
                self.neurological.consciousness_level = "postictal" if severity > 0.5 else "confused"
                self.cardiovascular.heart_rate = min(150, self.cardiovascular.heart_rate + int(15 * severity))
            
            # infectious diseases
            elif "sepsis" in disease_name:
                self.cardiovascular.heart_rate = min(150, self.cardiovascular.heart_rate + int(20 * severity))
                self.respiratory.respiratory_rate = min(35, self.respiratory.respiratory_rate + int(8 * severity))
                self.immune.crp = min(100.0, self.immune.crp + 20.0 * severity)
                self.immune.il6 = min(50.0, self.immune.il6 + 10.0 * severity)
                self.hematological.white_blood_cell_count = min(25.0, self.hematological.white_blood_cell_count + 5.0 * severity)
            
            elif "uti" in disease_name or "urinary tract infection" in disease_name:
                self.immune.white_blood_cell_count = min(20.0, self.immune.white_blood_cell_count + 2.0 * severity)
                self.gastrointestinal.abdominal_pain = True if severity > 0.5 else False
            
            # hematological diseases
            elif "anemia" in disease_name:
                self.hematological.hemoglobin = max(6.0, self.hematological.hemoglobin - 4.0 * severity)
                self.hematological.hematocrit = max(20.0, self.hematological.hematocrit - 10.0 * severity)
                self.cardiovascular.heart_rate = min(120, self.cardiovascular.heart_rate + int(10 * severity))
            
            elif "thrombocytopenia" in disease_name:
                self.hematological.platelet_count = max(50.0, self.hematological.platelet_count - 100.0 * severity)
            
            # psychiatric diseases
            elif "depression" in disease_name:
                self.psychiatric.mood = "depressed"
                self.neurological.attention = "poor"
            
            elif "anxiety" in disease_name:
                self.psychiatric.mood = "anxious"
                self.cardiovascular.heart_rate = min(120, self.cardiovascular.heart_rate + int(10 * severity))
                self.respiratory.respiratory_rate = min(30, self.respiratory.respiratory_rate + int(5 * severity))
            
            # gastrointestinal diseases
            elif "peptic ulcer" in disease_name:
                self.gastrointestinal.abdominal_pain = True
                self.gastrointestinal.nausea = True if severity > 0.5 else False
            
            elif "pancreatitis" in disease_name:
                self.gastrointestinal.abdominal_pain = True
                self.gastrointestinal.amylase = min(500.0, self.gastrointestinal.amylase + 200.0 * severity)
                self.gastrointestinal.lipase = min(300.0, self.gastrointestinal.lipase + 150.0 * severity)
            
            # trauma
            elif "trauma" in disease_name:
                self.cardiovascular.heart_rate = min(150, self.cardiovascular.heart_rate + int(20 * severity))
                self.respiratory.oxygen_saturation = max(85, self.respiratory.oxygen_saturation - int(5 * severity))
                self.hematological.hemoglobin = max(8.0, self.hematological.hemoglobin - 2.0 * severity)
                if severity > 0.7:
                    self.neurological.glasgow_coma_scale = max(3, self.neurological.glasgow_coma_scale - int(5 * severity))
    
    def _update_cross_system_interactions(self):
        """update cross-system physiological interactions"""
        
        # cardiovascular-respiratory coupling
        if self.cardiovascular.cardiac_output < 3.0:
            self.respiratory.oxygen_saturation = max(90, self.respiratory.oxygen_saturation - 2)
        
        # renal-cardiovascular coupling
        if self.cardiovascular.mean_arterial_pressure < 60:
            self.renal.glomerular_filtration_rate = max(30, self.renal.glomerular_filtration_rate - 20)
            self.renal.urine_output = max(0.1, self.renal.urine_output - 0.5)
        
        # endocrine-cardiovascular coupling
        if self.endocrine.cortisol > 25:
            self.cardiovascular.blood_pressure_systolic = min(180, self.cardiovascular.blood_pressure_systolic + 5)
            self.cardiovascular.heart_rate = min(120, self.cardiovascular.heart_rate + 5)
        
        # hepatic-hematological coupling
        if self.hepatic.alt > 50 or self.hepatic.ast > 50:
            self.hematological.pt = min(20, self.hematological.pt + 2)
            self.hematological.inr = min(2.0, self.hematological.inr + 0.2)
        
        # pregnancy increases blood volume and cardiac output, decreases SVR
        if self.reproductive.pregnancy_status == 'pregnant':
            self.cardiovascular.cardiac_output = min(9.0, self.cardiovascular.cardiac_output + 1.0)
            self.cardiovascular.stroke_volume = min(100.0, self.cardiovascular.stroke_volume + 10.0)
            self.cardiovascular.systemic_vascular_resistance = max(900, self.cardiovascular.systemic_vascular_resistance - 100)
            self.renal.glomerular_filtration_rate = min(150.0, self.renal.glomerular_filtration_rate + 20.0)
        # frailty increases risk of all system decompensation
        if self.geriatric.frailty_index > 0.5:
            self.cardiovascular.ejection_fraction = max(0.2, self.cardiovascular.ejection_fraction - 0.05)
            self.neurological.glasgow_coma_scale = max(3, self.neurological.glasgow_coma_scale - 1)
            self.hematological.hemoglobin = max(8.0, self.hematological.hemoglobin - 0.5)
        # psychiatric mood affects neuro/endocrine
        if self.psychiatric.mood == 'anxious':
            self.neurological.attention = 'distracted'
            self.endocrine.cortisol = min(40.0, self.endocrine.cortisol + 5.0)
        # severe dermatological burns increase fluid loss, risk of infection
        if len(self.dermatological.burns) > 0:
            self.renal.urine_output = max(0.1, self.renal.urine_output - 0.2)
            self.immune.crp = min(100.0, self.immune.crp + 10.0)
        # pediatric: low percentile increases risk for infection, poor healing
        if self.pediatric.growth_percentile < 5:
            self.immune.crp = min(100.0, self.immune.crp + 5.0)
            self.dermatological.wounds.append('delayed healing')
        # otolaryngologic airway compromise affects respiratory
        if self.otolaryngologic.airway != 'patent':
            self.respiratory.oxygen_saturation = max(80, self.respiratory.oxygen_saturation - 10)
        # ophthalmologic severe infection can cause fever
        if self.ophthalmologic.infection:
            self.cardiovascular.heart_rate = min(150, self.cardiovascular.heart_rate + 10)
    
    def add_disease(self, disease_name: str, severity: float = 1.0):
        """add a disease to the patient"""
        self.diseases.append({
            "name": disease_name,
            "severity": severity,
            "onset_time": self.time_step
        })
    
    def remove_disease(self, disease_name: str):
        """remove a disease from the patient"""
        self.diseases = [d for d in self.diseases if d["name"] != disease_name]
    
    def get_vital_signs(self) -> Dict[str, Any]:
        """get current vital signs"""
        return {
            "heart_rate": self.cardiovascular.heart_rate,
            "blood_pressure_systolic": self.cardiovascular.blood_pressure_systolic,
            "blood_pressure_diastolic": self.cardiovascular.blood_pressure_diastolic,
            "respiratory_rate": self.respiratory.respiratory_rate,
            "oxygen_saturation": self.respiratory.oxygen_saturation,
            "temperature": 37.0,  # simplified
            "mean_arterial_pressure": self.cardiovascular.mean_arterial_pressure,
            "cardiac_output": self.cardiovascular.cardiac_output,
            "stroke_volume": self.cardiovascular.stroke_volume,
            "ejection_fraction": self.cardiovascular.ejection_fraction,
            "rhythm": self.cardiovascular.rhythm,
            "tidal_volume": self.respiratory.tidal_volume,
            "minute_ventilation": self.respiratory.minute_ventilation,
            "vital_capacity": self.respiratory.vital_capacity,
            "fev1": self.respiratory.fev1,
            "pao2": self.respiratory.pao2,
            "paco2": self.respiratory.paco2,
            "ph": self.respiratory.ph,
            "glasgow_coma_scale": self.neurological.glasgow_coma_scale,
            "consciousness_level": self.neurological.consciousness_level,
            "urine_output": self.renal.urine_output,
            "glomerular_filtration_rate": self.renal.glomerular_filtration_rate
        }
    
    def get_lab_values(self) -> Dict[str, Any]:
        """get current lab values"""
        return {
            # electrolytes
            "sodium": self.renal.sodium,
            "potassium": self.renal.potassium,
            "chloride": self.renal.chloride,
            "bicarbonate": self.renal.bicarbonate,
            "calcium": self.musculoskeletal.calcium,
            "magnesium": 2.0,  # simplified
            "phosphate": 3.5,  # simplified
            
            # renal function
            "creatinine": self.renal.creatinine,
            "bun": self.renal.bun,
            "egfr": self.renal.glomerular_filtration_rate,
            
            # glucose metabolism
            "glucose": self.endocrine.blood_glucose,
            "hba1c": self.endocrine.hba1c,
            "insulin": self.endocrine.insulin_level,
            "glucagon": self.endocrine.glucagon_level,
            
            # thyroid function
            "tsh": self.endocrine.tsh,
            "free_t4": self.endocrine.free_t4,
            "free_t3": self.endocrine.free_t3,
            
            # adrenal function
            "cortisol": self.endocrine.cortisol,
            "aldosterone": self.endocrine.aldosterone,
            
            # hematology
            "hemoglobin": self.hematological.hemoglobin,
            "hematocrit": self.hematological.hematocrit,
            "red_blood_cell_count": self.hematological.red_blood_cell_count,
            "mcv": self.hematological.mcv,
            "mch": self.hematological.mch,
            "mchc": self.hematological.mchc,
            "white_blood_cell_count": self.hematological.white_blood_cell_count,
            "neutrophils": self.hematological.neutrophils,
            "lymphocytes": self.hematological.lymphocytes,
            "monocytes": self.hematological.monocytes,
            "eosinophils": self.hematological.eosinophils,
            "basophils": self.hematological.basophils,
            "platelet_count": self.hematological.platelet_count,
            
            # coagulation
            "pt": self.hematological.pt,
            "inr": self.hematological.inr,
            "ptt": self.hematological.ptt,
            "fibrinogen": self.hematological.fibrinogen,
            
            # liver function
            "alt": self.hepatic.alt,
            "ast": self.hepatic.ast,
            "alkaline_phosphatase": self.hepatic.alkaline_phosphatase,
            "ggt": self.hepatic.ggt,
            "total_bilirubin": self.hepatic.total_bilirubin,
            "direct_bilirubin": self.hepatic.direct_bilirubin,
            "indirect_bilirubin": self.hepatic.indirect_bilirubin,
            "albumin": self.hepatic.albumin,
            "total_protein": self.hepatic.total_protein,
            
            # pancreas
            "amylase": self.gastrointestinal.amylase,
            "lipase": self.gastrointestinal.lipase,
            
            # inflammatory markers
            "crp": self.immune.crp,
            "esr": self.immune.esr,
            "ferritin": self.immune.ferritin,
            "il6": self.immune.il6,
            "tnf_alpha": self.immune.tnf_alpha,
            
            # immune function
            "cd4_count": self.immune.cd4_count,
            "cd8_count": self.immune.cd8_count,
            "nk_cells": self.immune.nk_cells,
            
            # bone health
            "vitamin_d": self.musculoskeletal.vitamin_d,
            
            # acid-base
            "ph": self.renal.ph,
            "base_excess": self.renal.base_excess,
            
            # cardiac enzymes (simplified)
            "troponin_i": 0.01,  # normal
            "ck_mb": 2.0,  # normal
            "bnp": 50.0,  # normal
            "nt_probnp": 100.0  # normal
        }
    
    def get_abnormal_values(self) -> List[Dict[str, Any]]:
        """get list of abnormal lab values"""
        abnormal = []
        lab_values = self.get_lab_values()
        
        # define normal ranges
        normal_ranges = {
            # electrolytes
            "sodium": (135, 145),
            "potassium": (3.5, 5.0),
            "chloride": (98, 106),
            "bicarbonate": (22, 28),
            "calcium": (8.5, 10.5),
            "magnesium": (1.5, 2.5),
            "phosphate": (2.5, 4.5),
            
            # renal function
            "creatinine": (0.6, 1.2),
            "bun": (7, 20),
            "egfr": (90, 120),
            
            # glucose metabolism
            "glucose": (70, 100),
            "hba1c": (4.0, 5.6),
            "insulin": (3, 25),
            "glucagon": (50, 100),
            
            # thyroid function
            "tsh": (0.4, 4.0),
            "free_t4": (0.8, 1.8),
            "free_t3": (2.3, 4.2),
            
            # adrenal function
            "cortisol": (6, 23),
            "aldosterone": (4, 31),
            
            # hematology
            "hemoglobin": (12, 16),
            "hematocrit": (36, 46),
            "red_blood_cell_count": (4.2, 5.8),
            "mcv": (80, 100),
            "mch": (27, 33),
            "mchc": (32, 36),
            "white_blood_cell_count": (4.5, 11.0),
            "neutrophils": (2.0, 7.5),
            "lymphocytes": (1.0, 4.0),
            "monocytes": (0.2, 0.8),
            "eosinophils": (0.0, 0.5),
            "basophils": (0.0, 0.2),
            "platelet_count": (150, 450),
            
            # coagulation
            "pt": (11, 13),
            "inr": (0.8, 1.2),
            "ptt": (25, 35),
            "fibrinogen": (200, 400),
            
            # liver function
            "alt": (7, 55),
            "ast": (8, 48),
            "alkaline_phosphatase": (44, 147),
            "ggt": (9, 48),
            "total_bilirubin": (0.3, 1.2),
            "direct_bilirubin": (0.0, 0.3),
            "indirect_bilirubin": (0.2, 0.9),
            "albumin": (3.4, 5.4),
            "total_protein": (6.0, 8.3),
            
            # pancreas
            "amylase": (30, 110),
            "lipase": (7, 60),
            
            # inflammatory markers
            "crp": (0, 3),
            "esr": (0, 20),
            "ferritin": (20, 250),
            "il6": (0, 5),
            "tnf_alpha": (0, 8.1),
            
            # immune function
            "cd4_count": (500, 1500),
            "cd8_count": (200, 800),
            "nk_cells": (100, 400),
            
            # bone health
            "vitamin_d": (30, 100),
            
            # acid-base
            "ph": (7.35, 7.45),
            "base_excess": (-2, 2),
            
            # cardiac enzymes
            "troponin_i": (0, 0.04),
            "ck_mb": (0, 5),
            "bnp": (0, 100),
            "nt_probnp": (0, 125)
        }
        
        for test, value in lab_values.items():
            if test in normal_ranges:
                min_val, max_val = normal_ranges[test]
                if value < min_val or value > max_val:
                    abnormal.append({
                        "test": test,
                        "value": value,
                        "normal_range": f"{min_val}-{max_val}",
                        "status": "low" if value < min_val else "high"
                    })
        
        return abnormal
    
    def get_system_status(self) -> Dict[str, Any]:
        """get status of all organ systems"""
        status = {
            "cardiovascular": {
                "disease_state": self.cardiovascular.disease_state.value,
                "conditions": self.cardiovascular.conditions,
                "cardiac_output": self.cardiovascular.cardiac_output,
                "ejection_fraction": self.cardiovascular.ejection_fraction
            },
            "respiratory": {
                "disease_state": self.respiratory.disease_state.value,
                "conditions": self.respiratory.conditions,
                "oxygen_saturation": self.respiratory.oxygen_saturation,
                "minute_ventilation": self.respiratory.minute_ventilation
            },
            "renal": {
                "disease_state": self.renal.disease_state.value,
                "conditions": self.renal.conditions,
                "glomerular_filtration_rate": self.renal.glomerular_filtration_rate,
                "urine_output": self.renal.urine_output
            },
            "endocrine": {
                "disease_state": self.endocrine.disease_state.value,
                "conditions": self.endocrine.conditions,
                "blood_glucose": self.endocrine.blood_glucose,
                "cortisol": self.endocrine.cortisol
            },
            "neurological": {
                "disease_state": self.neurological.disease_state.value,
                "conditions": self.neurological.conditions,
                "glasgow_coma_scale": self.neurological.glasgow_coma_scale,
                "consciousness_level": self.neurological.consciousness_level
            },
            "gastrointestinal": {
                "disease_state": self.gastrointestinal.disease_state.value,
                "conditions": self.gastrointestinal.conditions,
                "nausea": self.gastrointestinal.nausea,
                "abdominal_pain": self.gastrointestinal.abdominal_pain
            },
            "hematological": {
                "disease_state": self.hematological.disease_state.value,
                "conditions": self.hematological.conditions,
                "hemoglobin": self.hematological.hemoglobin,
                "white_blood_cell_count": self.hematological.white_blood_cell_count
            },
            "immune": {
                "disease_state": self.immune.disease_state.value,
                "conditions": self.immune.conditions,
                "crp": self.immune.crp,
                "il6": self.immune.il6
            },
            "hepatic": {
                "disease_state": self.hepatic.disease_state.value,
                "conditions": self.hepatic.conditions,
                "alt": self.hepatic.alt,
                "ast": self.hepatic.ast
            },
            "musculoskeletal": {
                "disease_state": self.musculoskeletal.disease_state.value,
                "conditions": self.musculoskeletal.conditions,
                "pain": self.musculoskeletal.pain
            },
            "dermatological": {
                "wounds": self.dermatological.wounds,
                "rashes": self.dermatological.rashes,
                "burns": self.dermatological.burns,
                "turgor": self.dermatological.turgor,
                "hydration": self.dermatological.hydration
            },
            "reproductive": {
                "pregnancy_status": self.reproductive.pregnancy_status,
                "menstrual_cycle_day": self.reproductive.menstrual_cycle_day,
                "hormone_levels": self.reproductive.hormone_levels,
                "sexual_health": self.reproductive.sexual_health
            },
            "ophthalmologic": {
                "vision": self.ophthalmologic.vision,
                "eye_trauma": self.ophthalmologic.eye_trauma,
                "infection": self.ophthalmologic.infection
            },
            "otolaryngologic": {
                "hearing": self.otolaryngologic.hearing,
                "balance": self.otolaryngologic.balance,
                "airway": self.otolaryngologic.airway,
                "infection": self.otolaryngologic.infection
            },
            "pediatric": {
                "growth_percentile": self.pediatric.growth_percentile,
                "congenital_conditions": self.pediatric.congenital_conditions,
                "vaccination_status": self.pediatric.vaccination_status
            },
            "geriatric": {
                "frailty_index": self.geriatric.frailty_index,
                "polypharmacy": self.geriatric.polypharmacy,
                "cognitive_decline": self.geriatric.cognitive_decline
            },
            "psychiatric": {
                "mood": self.psychiatric.mood,
                "cognition": self.psychiatric.cognition,
                "substance_use": self.psychiatric.substance_use
            }
        }
        return status 