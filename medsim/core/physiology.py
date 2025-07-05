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
    LYMPHATIC = "lymphatic"
    INTEGUMENTARY = "integumentary"

class DiseaseState(Enum):
    """disease progression states"""
    NORMAL = "normal"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"
    TERMINAL = "terminal"

class DiscoveryMethod(Enum):
    """how patient information is discovered"""
    PATIENT_REPORTED = "patient_reported"
    PHYSICAL_EXAM = "physical_exam"
    VITAL_SIGNS = "vital_signs"
    LAB_RESULTS = "lab_results"
    IMAGING = "imaging"
    OBSERVATION = "observation"
    CALCULATION = "calculation"
    MEDICAL_HISTORY = "medical_history"
    SPECIALIZED_TEST = "specialized_test"

@dataclass
class DiscoveredInformation:
    """information that has been discovered about a patient"""
    value: Any
    discovery_method: DiscoveryMethod
    discovery_time: datetime
    discovered_by: str = "doctor"  # who discovered it
    confidence: float = 1.0  # confidence in the value (0.0 to 1.0)
    notes: List[str] = field(default_factory=list)

@dataclass
class PhysiologicalParameter:
    """enhanced physiological parameter with real-time tracking"""
    name: str
    current_value: float
    normal_range: Tuple[float, float]
    unit: str
    system: OrganSystem
    trend_data: List[Tuple[datetime, float]] = field(default_factory=list)
    last_update: datetime = field(default_factory=datetime.now)
    is_critical: bool = False
    critical_threshold: Optional[float] = None
    alert_level: str = "normal"  # normal, warning, critical, emergency

@dataclass
class DiseaseProcess:
    """enhanced disease process with progression modeling"""
    name: str
    system: OrganSystem
    current_state: DiseaseState
    severity: float  # 0.0 to 1.0
    onset_time: datetime
    progression_rate: float  # severity change per hour
    affecting_systems: List[OrganSystem] = field(default_factory=list)
    symptoms: List[str] = field(default_factory=list)
    complications: List[str] = field(default_factory=list)
    treatments: List[str] = field(default_factory=list)
    prognosis: str = "unknown"
    mortality_risk: float = 0.0

@dataclass
class PatientProfile:
    """enhanced patient profile with sophisticated physiological modeling"""
    patient_id: str
    name: str
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    
    # discovered information
    discovered_info: Dict[str, DiscoveredInformation] = field(default_factory=dict)
    
    # enhanced vitals with real-time tracking
    vitals: Dict[str, PhysiologicalParameter] = field(default_factory=dict)
    
    # medical history (hidden until discovered)
    medical_history: List[str] = field(default_factory=list)
    medications: List[str] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    family_history: List[str] = field(default_factory=list)
    social_history: Dict[str, Any] = field(default_factory=dict)
    
    # physical exam findings (hidden until discovered)
    physical_exam: Dict[str, Any] = field(default_factory=dict)
    
    # lab results (hidden until ordered and received)
    lab_results: Dict[str, Any] = field(default_factory=dict)
    
    # imaging results (hidden until ordered and received)
    imaging_results: Dict[str, Any] = field(default_factory=dict)
    
    # calculated values (hidden until calculated)
    bmi: Optional[float] = None
    body_surface_area: Optional[float] = None
    ideal_body_weight: Optional[float] = None
    
    # symptoms (managed by symptom library)
    symptoms: List[str] = field(default_factory=list)
    
    # enhanced disease processes
    active_diseases: List[DiseaseProcess] = field(default_factory=list)
    
    # treatment history
    treatments: List[Dict[str, Any]] = field(default_factory=list)
    
    # assessment and notes
    assessment: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    
    # physiological state
    stress_level: float = 0.0  # 0.0 to 1.0
    pain_level: float = 0.0  # 0.0 to 10.0
    consciousness_level: str = "alert"  # alert, confused, drowsy, unresponsive
    mobility_status: str = "ambulatory"  # ambulatory, wheelchair, bedbound
    
    def __post_init__(self):
        """initialize calculated values and physiological parameters"""
        self._calculate_bmi()
        self._calculate_body_surface_area()
        self._calculate_ideal_body_weight()
        self._initialize_vitals()
    
    def _calculate_bmi(self):
        """calculate bmi but don't reveal it"""
        if self.height_cm > 0 and self.weight_kg > 0:
            height_m = self.height_cm / 100
            self.bmi = self.weight_kg / (height_m * height_m)
    
    def _calculate_body_surface_area(self):
        """calculate body surface area using dubois formula"""
        if self.height_cm > 0 and self.weight_kg > 0:
            self.body_surface_area = 0.007184 * (self.weight_kg ** 0.425) * (self.height_cm ** 0.725)
    
    def _calculate_ideal_body_weight(self):
        """calculate ideal body weight using devine formula"""
        if self.height_cm > 0:
            height_inches = self.height_cm / 2.54
            if self.gender.lower() == 'male':
                self.ideal_body_weight = 50 + 2.3 * (height_inches - 60)
            else:
                self.ideal_body_weight = 45.5 + 2.3 * (height_inches - 60)
    
    def _initialize_vitals(self):
        """initialize vital signs with normal ranges"""
        self.vitals = {
            'heart_rate': PhysiologicalParameter(
                name="Heart Rate",
                current_value=80.0,
                normal_range=(60.0, 100.0),
                unit="bpm",
                system=OrganSystem.CARDIOVASCULAR,
                critical_threshold=150.0
            ),
            'systolic_bp': PhysiologicalParameter(
                name="Systolic Blood Pressure",
                current_value=120.0,
                normal_range=(90.0, 140.0),
                unit="mmHg",
                system=OrganSystem.CARDIOVASCULAR,
                critical_threshold=180.0
            ),
            'diastolic_bp': PhysiologicalParameter(
                name="Diastolic Blood Pressure",
                current_value=80.0,
                normal_range=(60.0, 90.0),
                unit="mmHg",
                system=OrganSystem.CARDIOVASCULAR,
                critical_threshold=110.0
            ),
            'respiratory_rate': PhysiologicalParameter(
                name="Respiratory Rate",
                current_value=16.0,
                normal_range=(12.0, 20.0),
                unit="/min",
                system=OrganSystem.RESPIRATORY,
                critical_threshold=30.0
            ),
            'temperature': PhysiologicalParameter(
                name="Temperature",
                current_value=37.0,
                normal_range=(36.5, 37.5),
                unit="°C",
                system=OrganSystem.INTEGUMENTARY,
                critical_threshold=40.0
            ),
            'oxygen_saturation': PhysiologicalParameter(
                name="Oxygen Saturation",
                current_value=98.0,
                normal_range=(95.0, 100.0),
                unit="%",
                system=OrganSystem.RESPIRATORY,
                critical_threshold=90.0
            ),
            'blood_glucose': PhysiologicalParameter(
                name="Blood Glucose",
                current_value=100.0,
                normal_range=(70.0, 140.0),
                unit="mg/dL",
                system=OrganSystem.ENDOCRINE,
                critical_threshold=400.0
            ),
            'creatinine': PhysiologicalParameter(
                name="Creatinine",
                current_value=1.0,
                normal_range=(0.6, 1.2),
                unit="mg/dL",
                system=OrganSystem.RENAL,
                critical_threshold=5.0
            ),
            'sodium': PhysiologicalParameter(
                name="Sodium",
                current_value=140.0,
                normal_range=(135.0, 145.0),
                unit="mEq/L",
                system=OrganSystem.RENAL,
                critical_threshold=160.0
            ),
            'potassium': PhysiologicalParameter(
                name="Potassium",
                current_value=4.0,
                normal_range=(3.5, 5.0),
                unit="mEq/L",
                system=OrganSystem.RENAL,
                critical_threshold=6.5
            )
        }
    
    def update_vital(self, vital_name: str, new_value: float, timestamp: datetime = None):
        """update a vital sign with trend tracking"""
        if vital_name in self.vitals:
            vital = self.vitals[vital_name]
            vital.current_value = new_value
            vital.last_update = timestamp or datetime.now()
            
            # add to trend data
            vital.trend_data.append((vital.last_update, new_value))
            
            # keep only last 100 data points
            if len(vital.trend_data) > 100:
                vital.trend_data = vital.trend_data[-100:]
            
            # update alert level
            self._update_alert_level(vital)
    
    def _update_alert_level(self, vital: PhysiologicalParameter):
        """update alert level based on current value"""
        if vital.critical_threshold and vital.current_value >= vital.critical_threshold:
            vital.alert_level = "emergency"
        elif vital.current_value > vital.normal_range[1] or vital.current_value < vital.normal_range[0]:
            vital.alert_level = "warning"
        else:
            vital.alert_level = "normal"
    
    def discover_information(self, info_type: str, method: DiscoveryMethod, 
                           value: Any = None, confidence: float = 1.0) -> str:
        """discover information about the patient"""
        discovery_time = datetime.now()
        
        # handle different types of information
        if info_type == "bmi":
            if self.bmi is not None:
                self.discovered_info["bmi"] = DiscoveredInformation(
                    value=self.bmi,
                    discovery_method=method,
                    discovery_time=discovery_time,
                    confidence=confidence
                )
                return f"✓ BMI discovered: {self.bmi:.1f} kg/m²"
            else:
                return "Error: BMI not available"
        
        elif info_type == "body_surface_area":
            if self.body_surface_area is not None:
                self.discovered_info["body_surface_area"] = DiscoveredInformation(
                    value=self.body_surface_area,
                    discovery_method=method,
                    discovery_time=discovery_time,
                    confidence=confidence
                )
                return f"✓ Body surface area discovered: {self.body_surface_area:.2f} m²"
            else:
                return "Error: Body surface area not available"
        
        elif info_type == "ideal_body_weight":
            if self.ideal_body_weight is not None:
                self.discovered_info["ideal_body_weight"] = DiscoveredInformation(
                    value=self.ideal_body_weight,
                    discovery_method=method,
                    discovery_time=discovery_time,
                    confidence=confidence
                )
                return f"✓ Ideal body weight discovered: {self.ideal_body_weight:.1f} kg"
            else:
                return "Error: Ideal body weight not available"
        
        elif info_type == "medical_history":
            if value is not None:
                self.discovered_info["medical_history"] = DiscoveredInformation(
                    value=value,
                    discovery_method=method,
                    discovery_time=discovery_time,
                    confidence=confidence
                )
                self.medical_history = value
                return f"✓ Medical history discovered: {len(value)} conditions"
            else:
                return "Error: No medical history provided"
        
        elif info_type == "medications":
            if value is not None:
                self.discovered_info["medications"] = DiscoveredInformation(
                    value=value,
                    discovery_method=method,
                    discovery_time=discovery_time,
                    confidence=confidence
                )
                self.medications = value
                return f"✓ Medications discovered: {len(value)} medications"
            else:
                return "Error: No medications provided"
        
        elif info_type == "allergies":
            if value is not None:
                self.discovered_info["allergies"] = DiscoveredInformation(
                    value=value,
                    discovery_method=method,
                    discovery_time=discovery_time,
                    confidence=confidence
                )
                self.allergies = value
                return f"✓ Allergies discovered: {len(value)} allergies"
            else:
                return "Error: No allergies provided"
        
        elif info_type == "physical_exam":
            if value is not None:
                self.discovered_info["physical_exam"] = DiscoveredInformation(
                    value=value,
                    discovery_method=method,
                    discovery_time=discovery_time,
                    confidence=confidence
                )
                self.physical_exam.update(value)
                return f"✓ Physical exam findings discovered: {len(value)} findings"
            else:
                return "Error: No physical exam findings provided"
        
        elif info_type == "lab_results":
            if value is not None:
                self.discovered_info["lab_results"] = DiscoveredInformation(
                    value=value,
                    discovery_method=method,
                    discovery_time=discovery_time,
                    confidence=confidence
                )
                self.lab_results.update(value)
                return f"✓ Lab results discovered: {len(value)} results"
            else:
                return "Error: No lab results provided"
        
        elif info_type == "imaging_results":
            if value is not None:
                self.discovered_info["imaging_results"] = DiscoveredInformation(
                    value=value,
                    discovery_method=method,
                    discovery_time=discovery_time,
                    confidence=confidence
                )
                self.imaging_results.update(value)
                return f"✓ Imaging results discovered: {len(value)} results"
            else:
                return "Error: No imaging results provided"
        
        else:
            return f"Error: Unknown information type '{info_type}'"
    
    def get_discovered_information(self, info_type: str = None) -> Dict[str, Any]:
        """get all discovered information or specific type"""
        if info_type:
            if info_type in self.discovered_info:
                info = self.discovered_info[info_type]
                return {
                    'value': info.value,
                    'discovery_method': info.discovery_method.value,
                    'discovery_time': info.discovery_time,
                    'confidence': info.confidence
                }
            else:
                return {}
        else:
            return {
                key: {
                    'value': info.value,
                    'discovery_method': info.discovery_method.value,
                    'discovery_time': info.discovery_time,
                    'confidence': info.confidence
                }
                for key, info in self.discovered_info.items()
            }
    
    def get_undiscovered_information(self) -> List[str]:
        """get list of information types that haven't been discovered"""
        all_info_types = [
            "bmi", "body_surface_area", "ideal_body_weight",
            "medical_history", "medications", "allergies",
            "physical_exam", "lab_results", "imaging_results"
        ]
        
        discovered_types = set(self.discovered_info.keys())
        return [info_type for info_type in all_info_types if info_type not in discovered_types]
    
    def get_available_vitals(self) -> Dict[str, Any]:
        """get current vital signs with alert levels"""
        return {
            name: {
                'value': vital.current_value,
                'unit': vital.unit,
                'normal_range': vital.normal_range,
                'alert_level': vital.alert_level,
                'last_update': vital.last_update
            }
            for name, vital in self.vitals.items()
        }
    
    def get_critical_vitals(self) -> List[Dict[str, Any]]:
        """get vitals that are in critical or emergency state"""
        critical = []
        for name, vital in self.vitals.items():
            if vital.alert_level in ["critical", "emergency"]:
                critical.append({
                    'name': vital.name,
                    'value': vital.current_value,
                    'unit': vital.unit,
                    'alert_level': vital.alert_level,
                    'normal_range': vital.normal_range
                })
        return critical
    
    def get_vital_trends(self, vital_name: str, hours: int = 24) -> List[Tuple[datetime, float]]:
        """get trend data for a vital sign"""
        if vital_name in self.vitals:
            vital = self.vitals[vital_name]
            cutoff_time = datetime.now() - timedelta(hours=hours)
            return [(timestamp, value) for timestamp, value in vital.trend_data 
                   if timestamp >= cutoff_time]
        return []
    
    def add_disease(self, disease_name: str, system: OrganSystem, severity: float = 0.5) -> str:
        """add a disease process to the patient"""
        disease = DiseaseProcess(
            name=disease_name,
            system=system,
            current_state=DiseaseState.MILD if severity < 0.3 else DiseaseState.MODERATE if severity < 0.7 else DiseaseState.SEVERE,
            severity=severity,
            onset_time=datetime.now(),
            progression_rate=random.uniform(0.01, 0.1)
        )
        self.active_diseases.append(disease)
        return f"✓ Added disease: {disease_name} (severity: {severity:.2f})"
    
    def update_diseases(self) -> List[str]:
        """update all active disease processes"""
        updates = []
        
        for disease in self.active_diseases:
            # calculate time elapsed
            time_elapsed = (datetime.now() - disease.onset_time).total_seconds() / 3600  # hours
            
            # update severity based on progression rate
            severity_change = disease.progression_rate * time_elapsed
            new_severity = min(1.0, disease.severity + severity_change)
            
            if new_severity != disease.severity:
                old_state = disease.current_state
                disease.severity = new_severity
                
                # update disease state based on severity
                if new_severity < 0.3:
                    disease.current_state = DiseaseState.MILD
                elif new_severity < 0.7:
                    disease.current_state = DiseaseState.MODERATE
                else:
                    disease.current_state = DiseaseState.SEVERE
                
                if disease.current_state != old_state:
                    updates.append(f"Disease {disease.name} progressed from {old_state.value} to {disease.current_state.value}")
        
        return updates
    
    def add_symptom(self, symptom: str) -> str:
        """add a symptom to the patient"""
        if symptom not in self.symptoms:
            self.symptoms.append(symptom)
            return f"✓ Added symptom: {symptom}"
        else:
            return f"Symptom '{symptom}' already present"
    
    def remove_symptom(self, symptom: str) -> str:
        """remove a symptom from the patient"""
        if symptom in self.symptoms:
            self.symptoms.remove(symptom)
            return f"✓ Removed symptom: {symptom}"
        else:
            return f"Symptom '{symptom}' not found"
    
    def add_treatment(self, treatment: Dict[str, Any]) -> str:
        """add a treatment to the patient's history"""
        treatment['timestamp'] = datetime.now()
        self.treatments.append(treatment)
        return f"✓ Added treatment: {treatment.get('name', 'Unknown')}"
    
    def add_assessment(self, assessment: str) -> str:
        """add an assessment note"""
        self.assessment.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: {assessment}")
        return f"✓ Added assessment: {assessment}"
    
    def add_note(self, note: str) -> str:
        """add a general note"""
        self.notes.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: {note}")
        return f"✓ Added note: {note}"
    
    def get_summary(self, include_undiscovered: bool = False) -> Dict[str, Any]:
        """get a comprehensive patient summary"""
        summary = {
            'patient_id': self.patient_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'height_cm': self.height_cm,
            'weight_kg': self.weight_kg,
            'vitals': self.get_available_vitals(),
            'critical_vitals': self.get_critical_vitals(),
            'symptoms': self.symptoms,
            'active_diseases': [d.name for d in self.active_diseases],
            'discovered_info': self.get_discovered_information(),
            'treatments': len(self.treatments),
            'assessment_notes': len(self.assessment),
            'general_notes': len(self.notes),
            'stress_level': self.stress_level,
            'pain_level': self.pain_level,
            'consciousness_level': self.consciousness_level,
            'mobility_status': self.mobility_status
        }
        
        if include_undiscovered:
            summary['undiscovered_info'] = self.get_undiscovered_information()
        
        return summary

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
        
        self.patients: Dict[str, PatientProfile] = {}
        self.discovery_history: List[Dict[str, Any]] = []
        
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

    def create_patient(self, patient_id: str, name: str, age: int, gender: str, 
                      height_cm: float, weight_kg: float) -> str:
        """create a new patient profile"""
        if patient_id in self.patients:
            return f"Error: Patient {patient_id} already exists"
        
        self.patients[patient_id] = PatientProfile(
            patient_id=patient_id,
            name=name,
            age=age,
            gender=gender,
            height_cm=height_cm,
            weight_kg=weight_kg
        )
        
        return f"✓ Created patient {patient_id}: {name}"
    
    def get_patient(self, patient_id: str) -> Optional[PatientProfile]:
        """get a patient profile"""
        return self.patients.get(patient_id)
    
    def discover_patient_information(self, patient_id: str, info_type: str, 
                                   method: DiscoveryMethod, value: Any = None) -> str:
        """discover information about a patient"""
        patient = self.get_patient(patient_id)
        if not patient:
            return f"Error: Patient {patient_id} not found"
        
        result = patient.discover_information(info_type, method, value)
        
        # record discovery
        self.discovery_history.append({
            'patient_id': patient_id,
            'info_type': info_type,
            'method': method.value,
            'timestamp': datetime.now(),
            'success': '✓' in result
        })
        
        return result
    
    def update_patient_vitals(self, patient_id: str, vitals: Dict[str, Any]) -> str:
        """update a patient's vital signs"""
        patient = self.get_patient(patient_id)
        if not patient:
            return f"Error: Patient {patient_id} not found"
        
        return patient.update_vitals(vitals)
    
    def add_patient_symptom(self, patient_id: str, symptom: str) -> str:
        """add a symptom to a patient"""
        patient = self.get_patient(patient_id)
        if not patient:
            return f"Error: Patient {patient_id} not found"
        
        return patient.add_symptom(symptom)
    
    def add_patient_treatment(self, patient_id: str, treatment: Dict[str, Any]) -> str:
        """add a treatment to a patient's history"""
        patient = self.get_patient(patient_id)
        if not patient:
            return f"Error: Patient {patient_id} not found"
        
        return patient.add_treatment(treatment)
    
    def add_patient_assessment(self, patient_id: str, assessment: str) -> str:
        """add an assessment note to a patient"""
        patient = self.get_patient(patient_id)
        if not patient:
            return f"Error: Patient {patient_id} not found"
        
        return patient.add_assessment(assessment)
    
    def get_patient_summary(self, patient_id: str, include_undiscovered: bool = False) -> Dict[str, Any]:
        """get a summary of a patient's information"""
        patient = self.get_patient(patient_id)
        if not patient:
            return {"error": f"Patient {patient_id} not found"}
        
        return patient.get_summary(include_undiscovered)
    
    def get_all_patients(self) -> List[Dict[str, Any]]:
        """get summaries of all patients"""
        return [patient.get_summary() for patient in self.patients.values()]
    
    def get_discovery_history(self, patient_id: str = None) -> List[Dict[str, Any]]:
        """get discovery history for a patient or all patients"""
        if patient_id:
            return [entry for entry in self.discovery_history if entry['patient_id'] == patient_id]
        else:
            return self.discovery_history.copy()

# --- organ system class stubs for modular physiological modeling ---

class CardiovascularSystem:
    """models basic cardiovascular parameters; extend as needed"""
    def __init__(self):
        # initialize key hemodynamic variables
        self.heart_rate = 80.0
        self.blood_pressure_systolic = 120.0
        self.blood_pressure_diastolic = 80.0
        self.mean_arterial_pressure = 93.0
        self.cardiac_output = 5.0
        self.stroke_volume = 70.0
        self.ejection_fraction = 0.65
        self.systemic_vascular_resistance = 1200.0
        self.rhythm = "sinus"
        self.conditions = []
        self.disease_state = DiseaseState.NORMAL
    def update_from_stress(self, stress_level: float):
        # simple stress response; extend for realism
        self.heart_rate += stress_level * 10
        self.blood_pressure_systolic += stress_level * 5
        self.blood_pressure_diastolic += stress_level * 3

class RespiratorySystem:
    """models basic respiratory parameters; extend as needed"""
    def __init__(self):
        self.respiratory_rate = 16.0
        self.oxygen_saturation = 98.0
        self.tidal_volume = 500.0
        self.minute_ventilation = 8.0
        self.vital_capacity = 4000.0
        self.fev1 = 3500.0
        self.pao2 = 95.0
        self.paco2 = 40.0
        self.ph = 7.4
        self.conditions = []
        self.disease_state = DiseaseState.NORMAL
    def update_from_stress(self, stress_level: float):
        self.respiratory_rate += stress_level * 2

class RenalSystem:
    """models basic renal parameters; extend as needed"""
    def __init__(self):
        self.urine_output = 50.0
        self.glomerular_filtration_rate = 100.0
        self.creatinine = 1.0
        self.sodium = 140.0
        self.potassium = 4.0
        self.chloride = 100.0
        self.bicarbonate = 24.0
        self.bun = 14.0
        self.ph = 7.4
        self.base_excess = 0.0
        self.conditions = []
        self.disease_state = DiseaseState.NORMAL
    def update_from_stress(self, stress_level: float):
        pass

class EndocrineSystem:
    def __init__(self):
        self.blood_glucose = 100.0
        self.cortisol = 10.0
        self.hba1c = 5.0
        self.insulin_level = 10.0
        self.glucagon_level = 60.0
        self.tsh = 2.0
        self.free_t4 = 1.2
        self.free_t3 = 3.0
        self.aldosterone = 10.0
        self.conditions = []
        self.disease_state = DiseaseState.NORMAL
    def update_from_stress(self, stress_level: float):
        pass

class NeurologicalSystem:
    def __init__(self):
        self.glasgow_coma_scale = 15
        self.consciousness_level = "alert"
        self.motor_strength = {"right_arm": 5, "right_leg": 5, "left_arm": 5, "left_leg": 5}
        self.attention = "normal"
        self.hearing = "normal"
        self.conditions = []
        self.disease_state = DiseaseState.NORMAL
    def update_from_stress(self, stress_level: float):
        pass

class GastrointestinalSystem:
    def __init__(self):
        self.nausea = False
        self.abdominal_pain = False
        self.amylase = 40.0
        self.lipase = 30.0
        self.conditions = []
        self.disease_state = DiseaseState.NORMAL
    def update_from_stress(self, stress_level: float):
        pass

class HematologicalSystem:
    def __init__(self):
        self.hemoglobin = 14.0
        self.hematocrit = 42.0
        self.red_blood_cell_count = 5.0
        self.mcv = 90.0
        self.mch = 30.0
        self.mchc = 34.0
        self.white_blood_cell_count = 7.0
        self.neutrophils = 4.0
        self.lymphocytes = 2.0
        self.monocytes = 0.5
        self.eosinophils = 0.2
        self.basophils = 0.1
        self.platelet_count = 250.0
        self.pt = 12.0
        self.inr = 1.0
        self.ptt = 30.0
        self.fibrinogen = 300.0
        self.conditions = []
        self.disease_state = DiseaseState.NORMAL
    def update_from_stress(self, stress_level: float):
        pass

class ImmuneSystem:
    def __init__(self):
        self.crp = 1.0
        self.esr = 10.0
        self.ferritin = 100.0
        self.il6 = 2.0
        self.tnf_alpha = 2.0
        self.cd4_count = 800.0
        self.cd8_count = 400.0
        self.nk_cells = 200.0
        self.conditions = []
        self.disease_state = DiseaseState.NORMAL
    def update_from_stress(self, stress_level: float):
        pass

class HepaticSystem:
    def __init__(self):
        self.alt = 25.0
        self.ast = 25.0
        self.alkaline_phosphatase = 60.0
        self.ggt = 20.0
        self.total_bilirubin = 0.8
        self.direct_bilirubin = 0.2
        self.indirect_bilirubin = 0.6
        self.albumin = 4.0
        self.total_protein = 7.0
        self.conditions = []
        self.disease_state = DiseaseState.NORMAL
    def update_from_stress(self, stress_level: float):
        pass

class MusculoskeletalSystem:
    def __init__(self):
        self.pain = {"general": 0}
        self.calcium = 9.5
        self.vitamin_d = 50.0
        self.conditions = []
        self.disease_state = DiseaseState.NORMAL
    def update_from_stress(self, stress_level: float):
        pass

class DermatologicalSystem:
    def __init__(self):
        self.wounds = []
        self.rashes = []
        self.burns = []
        self.turgor = "normal"
        self.hydration = "normal"
        self.conditions = []
    def update_from_stress(self, stress_level: float):
        pass

class ReproductiveSystem:
    def __init__(self):
        self.pregnancy_status = "not_pregnant"
        self.menstrual_cycle_day = 0
        self.hormone_levels = {}
        self.sexual_health = "normal"
        self.conditions = []
    def update_from_stress(self, stress_level: float):
        pass

class OphthalmologicSystem:
    def __init__(self):
        self.vision = "normal"
        self.eye_trauma = False
        self.infection = False
        self.conditions = []
    def update_from_stress(self, stress_level: float):
        pass

class OtolaryngologicSystem:
    def __init__(self):
        self.hearing = "normal"
        self.balance = "normal"
        self.airway = "patent"
        self.infection = False
        self.conditions = []
    def update_from_stress(self, stress_level: float):
        pass

class PediatricSystem:
    def __init__(self):
        self.growth_percentile = 50.0
        self.congenital_conditions = []
        self.vaccination_status = "up_to_date"
        self.conditions = []
    def update_from_stress(self, stress_level: float):
        pass

class GeriatricSystem:
    def __init__(self):
        self.frailty_index = 0.0
        self.polypharmacy = False
        self.cognitive_decline = False
        self.conditions = []
    def update_from_stress(self, stress_level: float):
        pass

class PsychiatricSystem:
    def __init__(self):
        self.mood = "normal"
        self.cognition = "normal"
        self.substance_use = False
        self.conditions = []
    def update_from_stress(self, stress_level: float):
        pass 