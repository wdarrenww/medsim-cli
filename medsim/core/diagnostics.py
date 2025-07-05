"""
advanced diagnostic system with comprehensive lab tests and imaging studies
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import random
import math


@dataclass
class LabTest:
    """laboratory test definition"""
    name: str
    category: str
    normal_range: Tuple[float, float]
    unit: str
    critical_low: Optional[float] = None
    critical_high: Optional[float] = None
    turnaround_time: int = 30  # minutes
    cost: float = 50.0
    description: str = ""
    clinical_significance: str = ""


@dataclass
class ImagingStudy:
    """imaging study definition"""
    name: str
    modality: str
    body_part: str
    turnaround_time: int = 60  # minutes
    cost: float = 200.0
    description: str = ""
    findings_template: str = ""
    contraindications: List[str] = field(default_factory=list)


class AdvancedDiagnosticSystem:
    """advanced diagnostic system with comprehensive testing capabilities"""
    
    def __init__(self):
        self.lab_tests = self._initialize_lab_tests()
        self.imaging_studies = self._initialize_imaging_studies()
        self.test_results = {}
        self.pending_tests = {}
        self.test_history = []
        
    def _initialize_lab_tests(self) -> Dict[str, LabTest]:
        """initialize comprehensive lab test library"""
        tests = {}
        
        # complete blood count (cbc)
        tests["wbc"] = LabTest(
            name="White Blood Cell Count",
            category="CBC",
            normal_range=(4.0, 11.0),
            unit="K/μL",
            critical_low=1.0,
            critical_high=30.0,
            turnaround_time=45,
            description="Measures total white blood cell count",
            clinical_significance="Elevated in infection, inflammation; decreased in bone marrow suppression"
        )
        
        tests["rbc"] = LabTest(
            name="Red Blood Cell Count",
            category="CBC",
            normal_range=(4.5, 5.9),
            unit="M/μL",
            critical_low=2.0,
            critical_high=8.0,
            description="Measures red blood cell count",
            clinical_significance="Decreased in anemia; increased in polycythemia"
        )
        
        tests["hemoglobin"] = LabTest(
            name="Hemoglobin",
            category="CBC",
            normal_range=(13.0, 17.0),
            unit="g/dL",
            critical_low=7.0,
            critical_high=20.0,
            description="Measures hemoglobin concentration",
            clinical_significance="Decreased in anemia, blood loss; increased in polycythemia"
        )
        
        tests["hematocrit"] = LabTest(
            name="Hematocrit",
            category="CBC",
            normal_range=(40.0, 50.0),
            unit="%",
            critical_low=20.0,
            critical_high=60.0,
            description="Measures percentage of blood volume occupied by red cells",
            clinical_significance="Decreased in anemia; increased in dehydration, polycythemia"
        )
        
        tests["platelets"] = LabTest(
            name="Platelet Count",
            category="CBC",
            normal_range=(150, 450),
            unit="K/μL",
            critical_low=50,
            critical_high=1000,
            description="Measures platelet count",
            clinical_significance="Decreased in thrombocytopenia; increased in reactive thrombocytosis"
        )
        
        # basic metabolic panel (bmp)
        tests["sodium"] = LabTest(
            name="Sodium",
            category="BMP",
            normal_range=(135, 145),
            unit="mEq/L",
            critical_low=120,
            critical_high=160,
            description="Measures serum sodium concentration",
            clinical_significance="Decreased in hyponatremia; increased in hypernatremia"
        )
        
        tests["potassium"] = LabTest(
            name="Potassium",
            category="BMP",
            normal_range=(3.5, 5.0),
            unit="mEq/L",
            critical_low=2.5,
            critical_high=6.5,
            description="Measures serum potassium concentration",
            clinical_significance="Decreased in hypokalemia; increased in hyperkalemia"
        )
        
        tests["chloride"] = LabTest(
            name="Chloride",
            category="BMP",
            normal_range=(96, 106),
            unit="mEq/L",
            description="Measures serum chloride concentration",
            clinical_significance="Usually follows sodium changes"
        )
        
        tests["bicarbonate"] = LabTest(
            name="Bicarbonate",
            category="BMP",
            normal_range=(22, 28),
            unit="mEq/L",
            critical_low=15,
            critical_high=35,
            description="Measures serum bicarbonate concentration",
            clinical_significance="Decreased in metabolic acidosis; increased in metabolic alkalosis"
        )
        
        tests["bun"] = LabTest(
            name="Blood Urea Nitrogen",
            category="BMP",
            normal_range=(7, 20),
            unit="mg/dL",
            description="Measures blood urea nitrogen",
            clinical_significance="Elevated in renal failure, dehydration, high protein diet"
        )
        
        tests["creatinine"] = LabTest(
            name="Creatinine",
            category="BMP",
            normal_range=(0.7, 1.3),
            unit="mg/dL",
            critical_high=5.0,
            description="Measures serum creatinine",
            clinical_significance="Elevated in renal failure, muscle breakdown"
        )
        
        tests["glucose"] = LabTest(
            name="Glucose",
            category="BMP",
            normal_range=(70, 100),
            unit="mg/dL",
            critical_low=40,
            critical_high=400,
            description="Measures blood glucose",
            clinical_significance="Elevated in diabetes; decreased in hypoglycemia"
        )
        
        # cardiac enzymes
        tests["troponin"] = LabTest(
            name="Troponin I",
            category="Cardiac",
            normal_range=(0.0, 0.04),
            unit="ng/mL",
            critical_high=0.5,
            turnaround_time=60,
            description="Cardiac-specific marker for myocardial injury",
            clinical_significance="Elevated in myocardial infarction, myocarditis"
        )
        
        tests["ck_mb"] = LabTest(
            name="CK-MB",
            category="Cardiac",
            normal_range=(0.0, 5.0),
            unit="ng/mL",
            critical_high=25.0,
            turnaround_time=60,
            description="Creatine kinase myocardial band",
            clinical_significance="Elevated in myocardial infarction"
        )
        
        tests["bnp"] = LabTest(
            name="B-Type Natriuretic Peptide",
            category="Cardiac",
            normal_range=(0, 100),
            unit="pg/mL",
            critical_high=500,
            turnaround_time=90,
            description="Marker for heart failure",
            clinical_significance="Elevated in heart failure, volume overload"
        )
        
        # liver function tests
        tests["alt"] = LabTest(
            name="Alanine Aminotransferase",
            category="Liver",
            normal_range=(7, 55),
            unit="U/L",
            critical_high=300,
            description="Liver enzyme",
            clinical_significance="Elevated in liver injury, hepatitis"
        )
        
        tests["ast"] = LabTest(
            name="Aspartate Aminotransferase",
            category="Liver",
            normal_range=(8, 48),
            unit="U/L",
            critical_high=300,
            description="Liver enzyme",
            clinical_significance="Elevated in liver injury, muscle damage"
        )
        
        tests["alkaline_phosphatase"] = LabTest(
            name="Alkaline Phosphatase",
            category="Liver",
            normal_range=(44, 147),
            unit="U/L",
            description="Liver enzyme",
            clinical_significance="Elevated in cholestasis, bone disease"
        )
        
        tests["bilirubin_total"] = LabTest(
            name="Total Bilirubin",
            category="Liver",
            normal_range=(0.3, 1.2),
            unit="mg/dL",
            critical_high=5.0,
            description="Total bilirubin",
            clinical_significance="Elevated in liver disease, hemolysis"
        )
        
        # inflammatory markers
        tests["c_reactive_protein"] = LabTest(
            name="C-Reactive Protein",
            category="Inflammatory",
            normal_range=(0, 3),
            unit="mg/L",
            critical_high=50,
            turnaround_time=60,
            description="Acute phase reactant",
            clinical_significance="Elevated in inflammation, infection"
        )
        
        tests["esr"] = LabTest(
            name="Erythrocyte Sedimentation Rate",
            category="Inflammatory",
            normal_range=(0, 20),
            unit="mm/hr",
            critical_high=100,
            turnaround_time=60,
            description="Non-specific inflammatory marker",
            clinical_significance="Elevated in inflammation, infection, malignancy"
        )
        
        tests["procalcitonin"] = LabTest(
            name="Procalcitonin",
            category="Inflammatory",
            normal_range=(0, 0.1),
            unit="ng/mL",
            critical_high=2.0,
            turnaround_time=90,
            description="Marker for bacterial infection",
            clinical_significance="Elevated in bacterial infection, sepsis"
        )
        
        # coagulation studies
        tests["pt"] = LabTest(
            name="Prothrombin Time",
            category="Coagulation",
            normal_range=(11, 13.5),
            unit="seconds",
            critical_high=20,
            turnaround_time=45,
            description="Measures extrinsic coagulation pathway",
            clinical_significance="Prolonged in warfarin use, liver disease"
        )
        
        tests["inr"] = LabTest(
            name="International Normalized Ratio",
            category="Coagulation",
            normal_range=(0.9, 1.1),
            unit="ratio",
            critical_high=5.0,
            description="Standardized prothrombin time",
            clinical_significance="Target 2-3 for warfarin therapy"
        )
        
        tests["aptt"] = LabTest(
            name="Activated Partial Thromboplastin Time",
            category="Coagulation",
            normal_range=(25, 35),
            unit="seconds",
            critical_high=60,
            turnaround_time=45,
            description="Measures intrinsic coagulation pathway",
            clinical_significance="Prolonged in heparin use, hemophilia"
        )
        
        # arterial blood gas
        tests["ph"] = LabTest(
            name="pH",
            category="ABG",
            normal_range=(7.35, 7.45),
            unit="",
            critical_low=7.20,
            critical_high=7.60,
            turnaround_time=15,
            description="Blood pH",
            clinical_significance="Decreased in acidosis; increased in alkalosis"
        )
        
        tests["pco2"] = LabTest(
            name="PCO2",
            category="ABG",
            normal_range=(35, 45),
            unit="mmHg",
            critical_low=20,
            critical_high=60,
            turnaround_time=15,
            description="Partial pressure of carbon dioxide",
            clinical_significance="Elevated in respiratory acidosis; decreased in respiratory alkalosis"
        )
        
        tests["po2"] = LabTest(
            name="PO2",
            category="ABG",
            normal_range=(80, 100),
            unit="mmHg",
            critical_low=60,
            turnaround_time=15,
            description="Partial pressure of oxygen",
            clinical_significance="Decreased in hypoxemia, respiratory failure"
        )
        
        tests["hco3"] = LabTest(
            name="Bicarbonate",
            category="ABG",
            normal_range=(22, 28),
            unit="mEq/L",
            critical_low=15,
            critical_high=35,
            turnaround_time=15,
            description="Bicarbonate from blood gas",
            clinical_significance="Decreased in metabolic acidosis; increased in metabolic alkalosis"
        )
        
        # additional specialized tests
        tests["d_dimer"] = LabTest(
            name="D-Dimer",
            category="Coagulation",
            normal_range=(0, 0.5),
            unit="μg/mL",
            critical_high=2.0,
            turnaround_time=60,
            description="Fibrin degradation product",
            clinical_significance="Elevated in DVT, PE, DIC"
        )
        
        tests["troponin_high_sensitivity"] = LabTest(
            name="High-Sensitivity Troponin",
            category="Cardiac",
            normal_range=(0, 14),
            unit="ng/L",
            critical_high=50,
            turnaround_time=60,
            description="High-sensitivity cardiac troponin",
            clinical_significance="More sensitive marker for myocardial injury"
        )
        
        tests["nt_probnp"] = LabTest(
            name="NT-proBNP",
            category="Cardiac",
            normal_range=(0, 125),
            unit="pg/mL",
            critical_high=450,
            turnaround_time=90,
            description="N-terminal pro-BNP",
            clinical_significance="Elevated in heart failure"
        )
        
        return tests
    
    def _initialize_imaging_studies(self) -> Dict[str, ImagingStudy]:
        """initialize comprehensive imaging study library"""
        studies = {}
        
        # chest imaging
        studies["chest_xray"] = ImagingStudy(
            name="Chest X-Ray",
            modality="X-Ray",
            body_part="Chest",
            turnaround_time=30,
            cost=150.0,
            description="Standard chest radiograph",
            findings_template="Chest X-ray shows {findings}. {additional_findings}",
            contraindications=["pregnancy"]
        )
        
        studies["chest_ct"] = ImagingStudy(
            name="Chest CT",
            modality="CT",
            body_part="Chest",
            turnaround_time=60,
            cost=800.0,
            description="Computed tomography of the chest",
            findings_template="Chest CT demonstrates {findings}. {additional_findings}",
            contraindications=["pregnancy", "contrast_allergy"]
        )
        
        studies["chest_ct_angiogram"] = ImagingStudy(
            name="Chest CT Angiogram",
            modality="CT",
            body_part="Chest",
            turnaround_time=90,
            cost=1200.0,
            description="CT angiogram for pulmonary embolism evaluation",
            findings_template="CT angiogram shows {findings}. {additional_findings}",
            contraindications=["pregnancy", "contrast_allergy", "renal_insufficiency"]
        )
        
        # cardiac imaging
        studies["ecg"] = ImagingStudy(
            name="Electrocardiogram",
            modality="ECG",
            body_part="Heart",
            turnaround_time=15,
            cost=100.0,
            description="12-lead electrocardiogram",
            findings_template="ECG shows {findings}. {additional_findings}",
            contraindications=[]
        )
        
        studies["echocardiogram"] = ImagingStudy(
            name="Echocardiogram",
            modality="Ultrasound",
            body_part="Heart",
            turnaround_time=120,
            cost=600.0,
            description="Transthoracic echocardiogram",
            findings_template="Echocardiogram demonstrates {findings}. {additional_findings}",
            contraindications=[]
        )
        
        studies["stress_test"] = ImagingStudy(
            name="Stress Test",
            modality="Nuclear",
            body_part="Heart",
            turnaround_time=180,
            cost=1500.0,
            description="Nuclear stress test",
            findings_template="Stress test shows {findings}. {additional_findings}",
            contraindications=["acute_coronary_syndrome", "unstable_angina"]
        )
        
        # abdominal imaging
        studies["abdominal_xray"] = ImagingStudy(
            name="Abdominal X-Ray",
            modality="X-Ray",
            body_part="Abdomen",
            turnaround_time=30,
            cost=150.0,
            description="Abdominal radiograph",
            findings_template="Abdominal X-ray shows {findings}. {additional_findings}",
            contraindications=["pregnancy"]
        )
        
        studies["abdominal_ct"] = ImagingStudy(
            name="Abdominal CT",
            modality="CT",
            body_part="Abdomen",
            turnaround_time=60,
            cost=800.0,
            description="Computed tomography of the abdomen",
            findings_template="Abdominal CT demonstrates {findings}. {additional_findings}",
            contraindications=["pregnancy", "contrast_allergy"]
        )
        
        studies["abdominal_ultrasound"] = ImagingStudy(
            name="Abdominal Ultrasound",
            modality="Ultrasound",
            body_part="Abdomen",
            turnaround_time=45,
            cost=400.0,
            description="Abdominal ultrasound",
            findings_template="Abdominal ultrasound shows {findings}. {additional_findings}",
            contraindications=[]
        )
        
        # neurological imaging
        studies["head_ct"] = ImagingStudy(
            name="Head CT",
            modality="CT",
            body_part="Head",
            turnaround_time=45,
            cost=600.0,
            description="Computed tomography of the head",
            findings_template="Head CT shows {findings}. {additional_findings}",
            contraindications=["pregnancy"]
        )
        
        studies["brain_mri"] = ImagingStudy(
            name="Brain MRI",
            modality="MRI",
            body_part="Brain",
            turnaround_time=120,
            cost=1500.0,
            description="Magnetic resonance imaging of the brain",
            findings_template="Brain MRI demonstrates {findings}. {additional_findings}",
            contraindications=["metallic_implants", "claustrophobia"]
        )
        
        # vascular imaging
        studies["carotid_ultrasound"] = ImagingStudy(
            name="Carotid Ultrasound",
            modality="Ultrasound",
            body_part="Neck",
            turnaround_time=60,
            cost=500.0,
            description="Carotid artery ultrasound",
            findings_template="Carotid ultrasound shows {findings}. {additional_findings}",
            contraindications=[]
        )
        
        studies["venous_ultrasound"] = ImagingStudy(
            name="Venous Ultrasound",
            modality="Ultrasound",
            body_part="Extremities",
            turnaround_time=45,
            cost=400.0,
            description="Venous ultrasound for DVT evaluation",
            findings_template="Venous ultrasound shows {findings}. {additional_findings}",
            contraindications=[]
        )
        
        # musculoskeletal imaging
        studies["bone_xray"] = ImagingStudy(
            name="Bone X-Ray",
            modality="X-Ray",
            body_part="Extremities",
            turnaround_time=30,
            cost=150.0,
            description="Bone radiograph",
            findings_template="Bone X-ray shows {findings}. {additional_findings}",
            contraindications=["pregnancy"]
        )
        
        studies["joint_mri"] = ImagingStudy(
            name="Joint MRI",
            modality="MRI",
            body_part="Joints",
            turnaround_time=90,
            cost=1200.0,
            description="Magnetic resonance imaging of joints",
            findings_template="Joint MRI demonstrates {findings}. {additional_findings}",
            contraindications=["metallic_implants", "claustrophobia"]
        )
        
        return studies
    
    def order_lab_test(self, test_name: str, patient_condition: Dict[str, Any]) -> str:
        """order a laboratory test"""
        if test_name not in self.lab_tests:
            return f"Error: Test '{test_name}' not available."
        
        test = self.lab_tests[test_name]
        test_id = f"LAB_{test_name}_{len(self.pending_tests) + 1}"
        
        self.pending_tests[test_id] = {
            'test_name': test_name,
            'test_type': 'lab',
            'ordered_time': datetime.now(),
            'turnaround_time': test.turnaround_time,
            'patient_condition': patient_condition.copy()
        }
        
        return f"✓ Lab test '{test.name}' ordered. Expected turnaround: {test.turnaround_time} minutes."
    
    def order_imaging_study(self, study_name: str, patient_condition: Dict[str, Any]) -> str:
        """order an imaging study"""
        if study_name not in self.imaging_studies:
            return f"Error: Imaging study '{study_name}' not available."
        
        study = self.imaging_studies[study_name]
        study_id = f"IMG_{study_name}_{len(self.pending_tests) + 1}"
        
        # check contraindications
        contraindications = self._check_imaging_contraindications(study, patient_condition)
        if contraindications:
            return f"⚠️ Warning: {study.name} may be contraindicated due to {', '.join(contraindications)}."
        
        self.pending_tests[study_id] = {
            'test_name': study_name,
            'test_type': 'imaging',
            'ordered_time': datetime.now(),
            'turnaround_time': study.turnaround_time,
            'patient_condition': patient_condition.copy()
        }
        
        return f"✓ Imaging study '{study.name}' ordered. Expected turnaround: {study.turnaround_time} minutes."
    
    def _check_imaging_contraindications(self, study: ImagingStudy, 
                                       patient_condition: Dict[str, Any]) -> List[str]:
        """check for imaging study contraindications"""
        contraindications = []
        
        for contraindication in study.contraindications:
            if contraindication == "pregnancy" and patient_condition.get('pregnant', False):
                contraindications.append("pregnancy")
            elif contraindication == "contrast_allergy" and patient_condition.get('contrast_allergy', False):
                contraindications.append("contrast allergy")
            elif contraindication == "renal_insufficiency" and patient_condition.get('creatinine', 1.0) > 2.0:
                contraindications.append("renal insufficiency")
            elif contraindication == "metallic_implants" and patient_condition.get('metallic_implants', False):
                contraindications.append("metallic implants")
            elif contraindication == "claustrophobia" and patient_condition.get('claustrophobia', False):
                contraindications.append("claustrophobia")
            elif contraindication == "acute_coronary_syndrome" and patient_condition.get('acute_coronary_syndrome', False):
                contraindications.append("acute coronary syndrome")
            elif contraindication == "unstable_angina" and patient_condition.get('unstable_angina', False):
                contraindications.append("unstable angina")
        
        return contraindications
    
    def get_pending_tests(self) -> Dict[str, Any]:
        """get list of pending tests"""
        return self.pending_tests.copy()
    
    def get_available_lab_tests(self) -> Dict[str, LabTest]:
        """get available laboratory tests"""
        return self.lab_tests.copy()
    
    def get_available_imaging_studies(self) -> Dict[str, ImagingStudy]:
        """get available imaging studies"""
        return self.imaging_studies.copy()
    
    def generate_test_result(self, test_id: str, time_elapsed: float) -> Optional[Dict[str, Any]]:
        """generate test result based on patient condition and time elapsed"""
        if test_id not in self.pending_tests:
            return None
        
        test_info = self.pending_tests[test_id]
        test_name = test_info['test_name']
        test_type = test_info['test_type']
        ordered_time = test_info['ordered_time']
        turnaround_time = test_info['turnaround_time']
        patient_condition = test_info['patient_condition']
        
        # check if enough time has passed
        if time_elapsed < turnaround_time:
            return None
        
        # generate result based on test type
        if test_type == 'lab':
            result = self._generate_lab_result(test_name, patient_condition)
        else:  # imaging
            result = self._generate_imaging_result(test_name, patient_condition)
        
        # move from pending to results
        del self.pending_tests[test_id]
        self.test_results[test_id] = result
        self.test_history.append({
            'test_id': test_id,
            'test_name': test_name,
            'test_type': test_type,
            'result': result,
            'completion_time': datetime.now()
        })
        
        return result
    
    def _generate_lab_result(self, test_name: str, patient_condition: Dict[str, Any]) -> Dict[str, Any]:
        """generate realistic lab test result based on patient condition"""
        test = self.lab_tests[test_name]
        base_value = (test.normal_range[0] + test.normal_range[1]) / 2
        
        # apply disease effects
        modified_value = self._apply_disease_effects_to_lab(test_name, base_value, patient_condition)
        
        # add some random variation
        variation = random.uniform(-0.1, 0.1) * modified_value
        final_value = modified_value + variation
        
        # determine result status
        if final_value < test.normal_range[0]:
            status = "LOW"
        elif final_value > test.normal_range[1]:
            status = "HIGH"
        else:
            status = "NORMAL"
        
        # check for critical values
        critical = False
        if test.critical_low and final_value <= test.critical_low:
            critical = True
            status = "CRITICAL LOW"
        elif test.critical_high and final_value >= test.critical_high:
            critical = True
            status = "CRITICAL HIGH"
        
        return {
            'test_name': test.name,
            'value': round(final_value, 2),
            'unit': test.unit,
            'normal_range': test.normal_range,
            'status': status,
            'critical': critical,
            'clinical_significance': test.clinical_significance,
            'timestamp': datetime.now()
        }
    
    def _apply_disease_effects_to_lab(self, test_name: str, base_value: float, 
                                     patient_condition: Dict[str, Any]) -> float:
        """apply disease effects to lab values"""
        modified_value = base_value
        
        # cardiovascular effects
        if test_name == "troponin" and patient_condition.get('myocardial_infarction', False):
            modified_value = random.uniform(2.0, 15.0)  # significantly elevated
        elif test_name == "ck_mb" and patient_condition.get('myocardial_infarction', False):
            modified_value = random.uniform(15.0, 50.0)  # elevated
        elif test_name == "bnp" and patient_condition.get('heart_failure', False):
            modified_value = random.uniform(200.0, 800.0)  # elevated
        elif test_name == "nt_probnp" and patient_condition.get('heart_failure', False):
            modified_value = random.uniform(500.0, 2000.0)  # elevated
        
        # respiratory effects
        elif test_name == "po2" and patient_condition.get('pneumonia', False):
            modified_value = random.uniform(60.0, 85.0)  # decreased
        elif test_name == "pco2" and patient_condition.get('copd', False):
            modified_value = random.uniform(45.0, 60.0)  # elevated
        
        # renal effects
        elif test_name == "creatinine" and patient_condition.get('acute_kidney_injury', False):
            modified_value = random.uniform(2.0, 5.0)  # elevated
        elif test_name == "bun" and patient_condition.get('acute_kidney_injury', False):
            modified_value = random.uniform(25.0, 60.0)  # elevated
        elif test_name == "potassium" and patient_condition.get('acute_kidney_injury', False):
            modified_value = random.uniform(5.5, 7.0)  # elevated
        
        # infectious effects
        elif test_name == "wbc" and patient_condition.get('infection', False):
            modified_value = random.uniform(12.0, 25.0)  # elevated
        elif test_name == "c_reactive_protein" and patient_condition.get('infection', False):
            modified_value = random.uniform(10.0, 50.0)  # elevated
        elif test_name == "procalcitonin" and patient_condition.get('bacterial_infection', False):
            modified_value = random.uniform(0.5, 5.0)  # elevated
        
        # hepatic effects
        elif test_name == "alt" and patient_condition.get('liver_disease', False):
            modified_value = random.uniform(100.0, 500.0)  # elevated
        elif test_name == "ast" and patient_condition.get('liver_disease', False):
            modified_value = random.uniform(80.0, 400.0)  # elevated
        elif test_name == "bilirubin_total" and patient_condition.get('liver_disease', False):
            modified_value = random.uniform(2.0, 8.0)  # elevated
        
        # coagulation effects
        elif test_name == "pt" and patient_condition.get('liver_disease', False):
            modified_value = random.uniform(14.0, 25.0)  # prolonged
        elif test_name == "inr" and patient_condition.get('anticoagulation', False):
            modified_value = random.uniform(2.0, 3.5)  # therapeutic range
        elif test_name == "d_dimer" and patient_condition.get('pulmonary_embolism', False):
            modified_value = random.uniform(1.0, 5.0)  # elevated
        
        # metabolic effects
        elif test_name == "glucose" and patient_condition.get('diabetes', False):
            modified_value = random.uniform(150.0, 400.0)  # elevated
        elif test_name == "sodium" and patient_condition.get('hyponatremia', False):
            modified_value = random.uniform(120.0, 135.0)  # decreased
        
        return modified_value
    
    def _generate_imaging_result(self, study_name: str, patient_condition: Dict[str, Any]) -> Dict[str, Any]:
        """generate realistic imaging study result"""
        study = self.imaging_studies[study_name]
        
        # generate findings based on patient condition
        findings = self._generate_imaging_findings(study_name, patient_condition)
        
        return {
            'study_name': study.name,
            'modality': study.modality,
            'body_part': study.body_part,
            'findings': findings,
            'impression': self._generate_impression(study_name, findings),
            'recommendations': self._generate_recommendations(study_name, findings),
            'timestamp': datetime.now()
        }
    
    def _generate_imaging_findings(self, study_name: str, patient_condition: Dict[str, Any]) -> str:
        """generate imaging findings based on patient condition"""
        if study_name == "chest_xray":
            if patient_condition.get('pneumonia', False):
                return "Bilateral infiltrates consistent with pneumonia. No pneumothorax or pleural effusion."
            elif patient_condition.get('pulmonary_embolism', False):
                return "Normal cardiac silhouette. No obvious infiltrates. Subtle atelectasis in right lower lobe."
            elif patient_condition.get('heart_failure', False):
                return "Cardiomegaly with pulmonary vascular congestion. Bilateral pleural effusions."
            else:
                return "Normal cardiac silhouette and clear lung fields. No acute cardiopulmonary process."
        
        elif study_name == "chest_ct":
            if patient_condition.get('pneumonia', False):
                return "Bilateral ground glass opacities and consolidations consistent with pneumonia. No pulmonary embolism."
            elif patient_condition.get('pulmonary_embolism', False):
                return "Filling defects in segmental pulmonary arteries bilaterally consistent with pulmonary embolism."
            else:
                return "Normal lung parenchyma. No pulmonary embolism or infiltrates."
        
        elif study_name == "ecg":
            if patient_condition.get('myocardial_infarction', False):
                return "ST elevation in leads II, III, aVF consistent with inferior MI. Q waves present."
            elif patient_condition.get('atrial_fibrillation', False):
                return "Irregularly irregular rhythm with absent P waves consistent with atrial fibrillation."
            else:
                return "Normal sinus rhythm at 80 bpm. Normal axis and intervals."
        
        elif study_name == "head_ct":
            if patient_condition.get('stroke', False):
                return "Hypodense area in left middle cerebral artery territory consistent with acute ischemic stroke."
            elif patient_condition.get('intracranial_hemorrhage', False):
                return "Hyperdense area in right parietal lobe consistent with intraparenchymal hemorrhage."
            else:
                return "Normal brain parenchyma. No mass effect or hemorrhage."
        
        else:
            return "Normal study. No acute abnormalities detected."
    
    def _generate_impression(self, study_name: str, findings: str) -> str:
        """generate clinical impression based on findings"""
        if "pneumonia" in findings.lower():
            return "Bilateral pneumonia requiring antibiotic therapy."
        elif "pulmonary embolism" in findings.lower():
            return "Acute pulmonary embolism requiring anticoagulation."
        elif "myocardial infarction" in findings.lower():
            return "Acute inferior myocardial infarction requiring emergent intervention."
        elif "stroke" in findings.lower():
            return "Acute ischemic stroke requiring evaluation for thrombolysis."
        elif "hemorrhage" in findings.lower():
            return "Intracranial hemorrhage requiring neurosurgical evaluation."
        else:
            return "No acute findings requiring immediate intervention."
    
    def _generate_recommendations(self, study_name: str, findings: str) -> str:
        """generate clinical recommendations based on findings"""
        if "pneumonia" in findings.lower():
            return "Recommend broad-spectrum antibiotics and follow-up chest X-ray."
        elif "pulmonary embolism" in findings.lower():
            return "Recommend therapeutic anticoagulation and cardiology consultation."
        elif "myocardial infarction" in findings.lower():
            return "Recommend emergent cardiac catheterization and cardiology consultation."
        elif "stroke" in findings.lower():
            return "Recommend neurology consultation and evaluation for thrombolysis."
        elif "hemorrhage" in findings.lower():
            return "Recommend neurosurgery consultation and blood pressure control."
        else:
            return "Continue current management plan."
    
    def get_test_results(self) -> Dict[str, Any]:
        """get all completed test results"""
        return self.test_results.copy()
    
    def get_test_history(self) -> List[Dict[str, Any]]:
        """get test history"""
        return self.test_history.copy() 