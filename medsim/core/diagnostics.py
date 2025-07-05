"""
enhanced diagnostic system with sophisticated lab interpretation and imaging analysis
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import random
import json


class TestCategory(Enum):
    """enhanced lab test categories"""
    HEMATOLOGY = "hematology"
    CHEMISTRY = "chemistry"
    CARDIAC = "cardiac"
    THYROID = "thyroid"
    LIPID = "lipid"
    COAGULATION = "coagulation"
    INFLAMMATORY = "inflammatory"
    MICROBIOLOGY = "microbiology"
    RAPID_TESTS = "rapid_tests"
    DRUG_LEVELS = "drug_levels"
    ARTERIAL_BLOOD_GAS = "arterial_blood_gas"
    SPECIALIZED = "specialized"


class ImagingModality(Enum):
    """enhanced imaging modalities"""
    XRAY = "xray"
    CT = "ct"
    MRI = "mri"
    ULTRASOUND = "ultrasound"
    NUCLEAR_MEDICINE = "nuclear_medicine"
    FLUOROSCOPY = "fluoroscopy"
    ANGIOGRAPHY = "angiography"
    ENDOSCOPY = "endoscopy"


class CriticalLevel(Enum):
    """critical value levels"""
    NORMAL = "normal"
    LOW = "low"
    HIGH = "high"
    CRITICAL_LOW = "critical_low"
    CRITICAL_HIGH = "critical_high"


@dataclass
class LabTestResult:
    """enhanced lab test result with interpretation"""
    test_name: str
    value: float
    unit: str
    normal_range: Tuple[float, float]
    critical_level: CriticalLevel
    interpretation: str
    clinical_significance: str
    timestamp: datetime
    is_abnormal: bool = False
    requires_action: bool = False
    trending: str = "stable"  # improving, worsening, stable


@dataclass
class ImagingResult:
    """enhanced imaging result with detailed findings"""
    study_name: str
    modality: ImagingModality
    body_part: str
    findings: Dict[str, Any]
    impression: str
    recommendations: List[str]
    urgency: str = "routine"  # routine, urgent, emergent
    timestamp: datetime = field(default_factory=datetime.now)
    requires_followup: bool = False


@dataclass
class LabTest:
    """enhanced lab test definition"""
    name: str
    category: TestCategory
    normal_range: Tuple[float, float]
    unit: str
    turnaround_time: int  # minutes
    cost: float
    critical_low: Optional[float] = None
    critical_high: Optional[float] = None
    clinical_significance: str = ""
    interpretation_guide: Dict[str, str] = field(default_factory=dict)
    related_tests: List[str] = field(default_factory=list)


@dataclass
class ImagingStudy:
    """enhanced imaging study definition"""
    name: str
    modality: ImagingModality
    body_part: str
    description: str
    indications: List[str] = field(default_factory=list)
    contraindications: List[str] = field(default_factory=list)
    preparation: str = ""
    duration: int = 30  # minutes
    cost: float = 0.0
    radiation_dose: Optional[str] = None
    contrast_required: bool = False
    sedation_required: bool = False


class EnhancedDiagnosticSystem:
    """enhanced diagnostic system with sophisticated interpretation"""
    
    def __init__(self):
        self.lab_tests = self._initialize_lab_tests()
        self.imaging_studies = self._initialize_imaging_studies()
        self.pending_orders: Dict[str, List[Dict[str, Any]]] = {}
        self.completed_results: Dict[str, List[Any]] = {}
        self.critical_alerts: List[Dict[str, Any]] = []
    
    def _initialize_lab_tests(self) -> Dict[str, LabTest]:
        """initialize comprehensive lab test library"""
        tests = {}
        
        # hematology tests
        tests["cbc"] = LabTest(
            name="Complete Blood Count",
            category=TestCategory.HEMATOLOGY,
            normal_range=(4.5, 11.0),
            unit="K/uL",
            turnaround_time=30,
            cost=25.0,
            critical_low=2.0,
            critical_high=50.0,
            clinical_significance="Measures white blood cell count, red blood cell count, hemoglobin, hematocrit, and platelets",
            interpretation_guide={
                "high": "May indicate infection, inflammation, or blood disorder",
                "low": "May indicate bone marrow suppression, blood loss, or nutritional deficiency"
            }
        )
        
        tests["hemoglobin"] = LabTest(
            name="Hemoglobin",
            category=TestCategory.HEMATOLOGY,
            normal_range=(12.0, 16.0),
            unit="g/dL",
            turnaround_time=30,
            cost=15.0,
            critical_low=7.0,
            critical_high=20.0,
            clinical_significance="Measures oxygen-carrying capacity of blood",
            interpretation_guide={
                "high": "May indicate polycythemia, dehydration, or high altitude",
                "low": "May indicate anemia, blood loss, or nutritional deficiency"
            }
        )
        
        tests["platelets"] = LabTest(
            name="Platelet Count",
            category=TestCategory.HEMATOLOGY,
            normal_range=(150, 450),
            unit="K/uL",
            turnaround_time=30,
            cost=15.0,
            critical_low=50,
            critical_high=1000,
            clinical_significance="Measures clotting ability",
            interpretation_guide={
                "high": "May indicate inflammation, infection, or myeloproliferative disorder",
                "low": "May indicate bleeding risk, bone marrow suppression, or immune disorder"
            }
        )
        
        # chemistry tests
        tests["sodium"] = LabTest(
            name="Sodium",
            category=TestCategory.CHEMISTRY,
            normal_range=(135, 145),
            unit="mEq/L",
            turnaround_time=45,
            cost=20.0,
            critical_low=120,
            critical_high=160,
            clinical_significance="Measures electrolyte balance and hydration status",
            interpretation_guide={
                "high": "May indicate dehydration, diabetes insipidus, or excess salt intake",
                "low": "May indicate fluid overload, SIADH, or diuretic use"
            }
        )
        
        tests["potassium"] = LabTest(
            name="Potassium",
            category=TestCategory.CHEMISTRY,
            normal_range=(3.5, 5.0),
            unit="mEq/L",
            turnaround_time=45,
            cost=20.0,
            critical_low=2.5,
            critical_high=6.5,
            clinical_significance="Critical for cardiac function and muscle contraction",
            interpretation_guide={
                "high": "May cause cardiac arrhythmias, renal failure, or medication effect",
                "low": "May cause muscle weakness, arrhythmias, or diuretic use"
            }
        )
        
        tests["creatinine"] = LabTest(
            name="Creatinine",
            category=TestCategory.CHEMISTRY,
            normal_range=(0.6, 1.2),
            unit="mg/dL",
            turnaround_time=45,
            cost=20.0,
            critical_high=5.0,
            clinical_significance="Measures kidney function",
            interpretation_guide={
                "high": "May indicate acute or chronic kidney injury",
                "low": "May indicate muscle wasting or pregnancy"
            }
        )
        
        tests["glucose"] = LabTest(
            name="Glucose",
            category=TestCategory.CHEMISTRY,
            normal_range=(70, 140),
            unit="mg/dL",
            turnaround_time=30,
            cost=15.0,
            critical_low=40,
            critical_high=400,
            clinical_significance="Measures blood sugar levels",
            interpretation_guide={
                "high": "May indicate diabetes, stress, or medication effect",
                "low": "May indicate hypoglycemia, insulin overdose, or fasting"
            }
        )
        
        # cardiac markers
        tests["troponin"] = LabTest(
            name="Troponin I",
            category=TestCategory.CARDIAC,
            normal_range=(0.0, 0.04),
            unit="ng/mL",
            turnaround_time=60,
            cost=50.0,
            critical_high=0.5,
            clinical_significance="Specific marker for myocardial injury",
            interpretation_guide={
                "high": "Indicates myocardial infarction or cardiac injury",
                "normal": "Suggests no acute cardiac injury"
            }
        )
        
        tests["bnp"] = LabTest(
            name="B-type Natriuretic Peptide",
            category=TestCategory.CARDIAC,
            normal_range=(0, 100),
            unit="pg/mL",
            turnaround_time=90,
            cost=75.0,
            critical_high=500,
            clinical_significance="Measures heart failure severity",
            interpretation_guide={
                "high": "Indicates heart failure or volume overload",
                "normal": "Suggests no significant heart failure"
            }
        )
        
        # thyroid function
        tests["tsh"] = LabTest(
            name="Thyroid Stimulating Hormone",
            category=TestCategory.THYROID,
            normal_range=(0.4, 4.0),
            unit="mIU/L",
            turnaround_time=120,
            cost=40.0,
            clinical_significance="Measures thyroid function",
            interpretation_guide={
                "high": "May indicate hypothyroidism",
                "low": "May indicate hyperthyroidism"
            }
        )
        
        # inflammatory markers
        tests["crp"] = LabTest(
            name="C-Reactive Protein",
            category=TestCategory.INFLAMMATORY,
            normal_range=(0, 3),
            unit="mg/L",
            turnaround_time=60,
            cost=35.0,
            critical_high=100,
            clinical_significance="Measures inflammation",
            interpretation_guide={
                "high": "Indicates active inflammation or infection",
                "normal": "Suggests no significant inflammation"
            }
        )
        
        return tests
    
    def _initialize_imaging_studies(self) -> Dict[str, ImagingStudy]:
        """initialize comprehensive imaging studies library"""
        studies = {}
        
        # chest imaging
        studies["chest_xray"] = ImagingStudy(
            name="Chest X-Ray",
            modality=ImagingModality.XRAY,
            body_part="Chest",
            description="Standard chest radiograph",
            indications=["chest pain", "shortness of breath", "cough", "fever"],
            contraindications=["pregnancy (first trimester)"],
            duration=15,
            cost=150.0,
            radiation_dose="0.1 mSv"
        )
        
        studies["chest_ct"] = ImagingStudy(
            name="Chest CT",
            modality=ImagingModality.CT,
            body_part="Chest",
            description="Computed tomography of the chest",
            indications=["suspected pulmonary embolism", "lung cancer screening", "complex chest pathology"],
            contraindications=["pregnancy", "contrast allergy"],
            preparation="IV contrast may be required",
            duration=30,
            cost=800.0,
            radiation_dose="7 mSv",
            contrast_required=True
        )
        
        studies["ecg"] = ImagingStudy(
            name="Electrocardiogram",
            modality=ImagingModality.XRAY,
            body_part="Heart",
            description="Electrical activity of the heart",
            indications=["chest pain", "palpitations", "syncope", "arrhythmia"],
            contraindications=[],
            duration=10,
            cost=100.0
        )
        
        studies["echo"] = ImagingStudy(
            name="Echocardiogram",
            modality=ImagingModality.ULTRASOUND,
            body_part="Heart",
            description="Ultrasound of the heart",
            indications=["heart failure", "valvular disease", "cardiac function assessment"],
            contraindications=[],
            duration=45,
            cost=600.0
        )
        
        studies["head_ct"] = ImagingStudy(
            name="Head CT",
            modality=ImagingModality.CT,
            body_part="Head",
            description="Computed tomography of the head",
            indications=["head trauma", "stroke", "headache", "altered mental status"],
            contraindications=["pregnancy", "contrast allergy"],
            preparation="IV contrast may be required",
            duration=20,
            cost=500.0,
            radiation_dose="2 mSv",
            contrast_required=True
        )
        
        studies["abdominal_ct"] = ImagingStudy(
            name="Abdominal CT",
            modality=ImagingModality.CT,
            body_part="Abdomen",
            description="Computed tomography of the abdomen",
            indications=["abdominal pain", "trauma", "suspected appendicitis"],
            contraindications=["pregnancy", "contrast allergy"],
            preparation="Oral and IV contrast may be required",
            duration=30,
            cost=800.0,
            radiation_dose="8 mSv",
            contrast_required=True
        )
        
        studies["abdominal_ultrasound"] = ImagingStudy(
            name="Abdominal Ultrasound",
            modality=ImagingModality.ULTRASOUND,
            body_part="Abdomen",
            description="Ultrasound of the abdomen",
            indications=["abdominal pain", "gallbladder disease", "liver disease"],
            contraindications=[],
            preparation="Fasting may be required",
            duration=30,
            cost=300.0
        )
        
        return studies
    
    def order_lab_test(self, patient_id: str, test_name: str) -> str:
        """order a lab test for a patient"""
        if test_name not in self.lab_tests:
            return f"Error: Lab test '{test_name}' not found"
        
        test = self.lab_tests[test_name]
        
        if patient_id not in self.pending_orders:
            self.pending_orders[patient_id] = []
        
        order = {
            'test_name': test_name,
            'order_time': datetime.now(),
            'expected_completion': datetime.now() + timedelta(minutes=test.turnaround_time),
            'status': 'ordered'
        }
        
        self.pending_orders[patient_id].append(order)
        return f"✓ Ordered {test_name} for patient {patient_id} (ETA: {test.turnaround_time} minutes)"
    
    def order_imaging_study(self, patient_id: str, study_name: str) -> str:
        """order an imaging study for a patient"""
        if study_name not in self.imaging_studies:
            return f"Error: Imaging study '{study_name}' not found"
        
        study = self.imaging_studies[study_name]
        
        if patient_id not in self.pending_orders:
            self.pending_orders[patient_id] = []
        
        order = {
            'study_name': study_name,
            'order_time': datetime.now(),
            'expected_completion': datetime.now() + timedelta(minutes=study.duration),
            'status': 'ordered'
        }
        
        self.pending_orders[patient_id].append(order)
        return f"✓ Ordered {study_name} for patient {patient_id} (ETA: {study.duration} minutes)"
    
    def get_pending_orders(self, patient_id: str) -> List[Dict[str, Any]]:
        """get pending orders for a patient"""
        return self.pending_orders.get(patient_id, [])
    
    def complete_lab_test(self, patient_id: str, test_name: str, value: float) -> LabTestResult:
        """complete a lab test with result"""
        if test_name not in self.lab_tests:
            raise ValueError(f"Lab test '{test_name}' not found")
        
        test = self.lab_tests[test_name]
        
        # determine critical level
        if test.critical_low and value <= test.critical_low:
            critical_level = CriticalLevel.CRITICAL_LOW
        elif test.critical_high and value >= test.critical_high:
            critical_level = CriticalLevel.CRITICAL_HIGH
        elif value < test.normal_range[0]:
            critical_level = CriticalLevel.LOW
        elif value > test.normal_range[1]:
            critical_level = CriticalLevel.HIGH
        else:
            critical_level = CriticalLevel.NORMAL
        
        # generate interpretation
        interpretation = self._interpret_lab_result(test, value, critical_level)
        
        result = LabTestResult(
            test_name=test_name,
            value=value,
            unit=test.unit,
            normal_range=test.normal_range,
            critical_level=critical_level,
            interpretation=interpretation,
            clinical_significance=test.clinical_significance,
            timestamp=datetime.now(),
            is_abnormal=critical_level != CriticalLevel.NORMAL,
            requires_action=critical_level in [CriticalLevel.CRITICAL_LOW, CriticalLevel.CRITICAL_HIGH]
        )
        
        # store result
        if patient_id not in self.completed_results:
            self.completed_results[patient_id] = []
        self.completed_results[patient_id].append(result)
        
        # check for critical alerts
        if result.requires_action:
            self.critical_alerts.append({
                'patient_id': patient_id,
                'test_name': test_name,
                'value': value,
                'unit': test.unit,
                'critical_level': critical_level.value,
                'timestamp': datetime.now()
            })
        
        return result
    
    def _interpret_lab_result(self, test: LabTest, value: float, critical_level: CriticalLevel) -> str:
        """generate interpretation for lab result"""
        if critical_level == CriticalLevel.NORMAL:
            return f"Normal {test.name} level"
        
        interpretation = test.interpretation_guide.get(critical_level.value, "")
        if not interpretation:
            if critical_level in [CriticalLevel.LOW, CriticalLevel.CRITICAL_LOW]:
                interpretation = f"Low {test.name} level"
            else:
                interpretation = f"High {test.name} level"
        
        return interpretation
    
    def complete_imaging_study(self, patient_id: str, study_name: str, findings: Dict[str, Any]) -> ImagingResult:
        """complete an imaging study with results"""
        if study_name not in self.imaging_studies:
            raise ValueError(f"Imaging study '{study_name}' not found")
        
        study = self.imaging_studies[study_name]
        
        # generate impression and recommendations
        impression = self._generate_imaging_impression(study, findings)
        recommendations = self._generate_imaging_recommendations(study, findings)
        
        result = ImagingResult(
            study_name=study_name,
            modality=study.modality,
            body_part=study.body_part,
            findings=findings,
            impression=impression,
            recommendations=recommendations,
            urgency="routine"  # could be determined by findings
        )
        
        # store result
        if patient_id not in self.completed_results:
            self.completed_results[patient_id] = []
        self.completed_results[patient_id].append(result)
        
        return result
    
    def _generate_imaging_impression(self, study: ImagingStudy, findings: Dict[str, Any]) -> str:
        """generate impression for imaging study"""
        if "normal" in findings.get("impression", "").lower():
            return f"Normal {study.body_part} study"
        elif "abnormal" in findings.get("impression", "").lower():
            return f"Abnormal {study.body_part} study - {findings.get('impression', 'Clinical correlation recommended')}"
        else:
            return f"{study.body_part} study - {findings.get('impression', 'Clinical correlation recommended')}"
    
    def _generate_imaging_recommendations(self, study: ImagingStudy, findings: Dict[str, Any]) -> List[str]:
        """generate recommendations for imaging study"""
        recommendations = []
        
        if "abnormal" in findings.get("impression", "").lower():
            recommendations.append("Clinical correlation recommended")
            recommendations.append("Consider follow-up imaging if clinically indicated")
        
        if study.modality == ImagingModality.CT:
            recommendations.append("Radiation exposure noted")
        
        return recommendations
    
    def get_lab_results(self, patient_id: str) -> List[LabTestResult]:
        """get lab results for a patient"""
        results = []
        for result in self.completed_results.get(patient_id, []):
            if isinstance(result, LabTestResult):
                results.append(result)
        return results
    
    def get_imaging_results(self, patient_id: str) -> List[ImagingResult]:
        """get imaging results for a patient"""
        results = []
        for result in self.completed_results.get(patient_id, []):
            if isinstance(result, ImagingResult):
                results.append(result)
        return results
    
    def get_critical_alerts(self) -> List[Dict[str, Any]]:
        """get critical lab alerts"""
        return self.critical_alerts.copy()
    
    def acknowledge_critical_alert(self, alert_index: int) -> str:
        """acknowledge a critical alert"""
        if 0 <= alert_index < len(self.critical_alerts):
            alert = self.critical_alerts.pop(alert_index)
            return f"✓ Acknowledged critical alert: {alert['test_name']} = {alert['value']} {alert['unit']}"
        else:
            return "Error: Invalid alert index"
    
    def get_available_lab_tests(self) -> Dict[str, LabTest]:
        """get all available lab tests"""
        return self.lab_tests.copy()
    
    def get_available_imaging_studies(self) -> Dict[str, ImagingStudy]:
        """get all available imaging studies"""
        return self.imaging_studies.copy()
    
    def search_lab_tests(self, query: str) -> Dict[str, LabTest]:
        """search lab tests by name or category"""
        query = query.lower()
        results = {}
        for name, test in self.lab_tests.items():
            if (query in name.lower() or 
                query in test.category.value.lower() or
                query in test.clinical_significance.lower()):
                results[name] = test
        return results
    
    def search_imaging_studies(self, query: str) -> Dict[str, ImagingStudy]:
        """search imaging studies by name or modality"""
        query = query.lower()
        results = {}
        for name, study in self.imaging_studies.items():
            if (query in name.lower() or 
                query in study.modality.value.lower() or
                query in study.body_part.lower()):
                results[name] = study
        return results