"""
advanced diagnostic system with comprehensive lab tests and imaging studies
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import random
import math
from ..core.session import PatientState


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
        
        # Complete blood count (cbc)
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
        
        # Basic metabolic panel (bmp)
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
        
        # Cardiac enzymes
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
            critical_high=10.0,
            description="Creatine kinase MB fraction",
            clinical_significance="Elevated in myocardial infarction"
        )
        
        tests["bnp"] = LabTest(
            name="B-type Natriuretic Peptide",
            category="Cardiac",
            normal_range=(0, 100),
            unit="pg/mL",
            critical_high=500,
            description="Marker for heart failure",
            clinical_significance="Elevated in heart failure, volume overload"
        )
        
        # Coagulation studies
        tests["pt"] = LabTest(
            name="Prothrombin Time",
            category="Coagulation",
            normal_range=(11.0, 13.5),
            unit="seconds",
            critical_high=20.0,
            description="Measures extrinsic coagulation pathway",
            clinical_significance="Prolonged in warfarin use, liver disease, DIC"
        )
        
        tests["inr"] = LabTest(
            name="International Normalized Ratio",
            category="Coagulation",
            normal_range=(0.9, 1.1),
            unit="",
            critical_high=5.0,
            description="Standardized measure of PT",
            clinical_significance="Target 2-3 for most anticoagulation"
        )
        
        tests["aptt"] = LabTest(
            name="Activated Partial Thromboplastin Time",
            category="Coagulation",
            normal_range=(25, 35),
            unit="seconds",
            critical_high=60,
            description="Measures intrinsic coagulation pathway",
            clinical_significance="Prolonged in heparin use, hemophilia, DIC"
        )
        
        tests["fibrinogen"] = LabTest(
            name="Fibrinogen",
            category="Coagulation",
            normal_range=(200, 400),
            unit="mg/dL",
            critical_low=100,
            description="Essential clotting factor",
            clinical_significance="Decreased in DIC, liver disease, congenital deficiency"
        )
        
        tests["d_dimer"] = LabTest(
            name="D-Dimer",
            category="Coagulation",
            normal_range=(0, 0.5),
            unit="μg/mL",
            critical_high=2.0,
            description="Fibrin degradation product",
            clinical_significance="Elevated in DVT, PE, DIC, inflammation"
        )
        
        # Arterial blood gas
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
            description="Partial pressure of CO2",
            clinical_significance="Elevated in respiratory acidosis; decreased in respiratory alkalosis"
        )
        
        tests["po2"] = LabTest(
            name="PO2",
            category="ABG",
            normal_range=(80, 100),
            unit="mmHg",
            critical_low=60,
            description="Partial pressure of O2",
            clinical_significance="Decreased in hypoxemia, respiratory failure"
        )
        
        tests["hco3"] = LabTest(
            name="Bicarbonate",
            category="ABG",
            normal_range=(22, 28),
            unit="mEq/L",
            critical_low=15,
            critical_high=35,
            description="Bicarbonate concentration",
            clinical_significance="Decreased in metabolic acidosis; increased in metabolic alkalosis"
        )
        
        tests["base_excess"] = LabTest(
            name="Base Excess",
            category="ABG",
            normal_range=(-2, 2),
            unit="mEq/L",
            description="Metabolic acid-base status",
            clinical_significance="Negative in metabolic acidosis; positive in metabolic alkalosis"
        )
        
        # Liver function tests
        tests["ast"] = LabTest(
            name="Aspartate Aminotransferase",
            category="Liver",
            normal_range=(10, 40),
            unit="U/L",
            critical_high=200,
            description="Liver enzyme",
            clinical_significance="Elevated in liver disease, muscle injury, heart failure"
        )
        
        tests["alt"] = LabTest(
            name="Alanine Aminotransferase",
            category="Liver",
            normal_range=(7, 56),
            unit="U/L",
            critical_high=200,
            description="Liver-specific enzyme",
            clinical_significance="Elevated in liver disease, hepatitis"
        )
        
        tests["alk_phos"] = LabTest(
            name="Alkaline Phosphatase",
            category="Liver",
            normal_range=(44, 147),
            unit="U/L",
            description="Bone and liver enzyme",
            clinical_significance="Elevated in cholestasis, bone disease, pregnancy"
        )
        
        tests["bilirubin_total"] = LabTest(
            name="Total Bilirubin",
            category="Liver",
            normal_range=(0.3, 1.2),
            unit="mg/dL",
            critical_high=5.0,
            description="Breakdown product of heme",
            clinical_significance="Elevated in liver disease, hemolysis, biliary obstruction"
        )
        
        tests["albumin"] = LabTest(
            name="Albumin",
            category="Liver",
            normal_range=(3.4, 5.4),
            unit="g/dL",
            critical_low=2.0,
            description="Major plasma protein",
            clinical_significance="Decreased in liver disease, malnutrition, inflammation"
        )
        
        # Toxicology
        tests["acetaminophen"] = LabTest(
            name="Acetaminophen Level",
            category="Toxicology",
            normal_range=(0, 10),
            unit="μg/mL",
            critical_high=150,
            turnaround_time=120,
            description="Acetaminophen concentration",
            clinical_significance="Elevated in overdose, risk of hepatotoxicity"
        )
        
        tests["salicylate"] = LabTest(
            name="Salicylate Level",
            category="Toxicology",
            normal_range=(0, 20),
            unit="mg/dL",
            critical_high=40,
            description="Aspirin/salicylate concentration",
            clinical_significance="Elevated in overdose, risk of toxicity"
        )
        
        tests["ethanol"] = LabTest(
            name="Ethanol Level",
            category="Toxicology",
            normal_range=(0, 80),
            unit="mg/dL",
            critical_high=300,
            description="Blood alcohol concentration",
            clinical_significance="Elevated in alcohol intoxication"
        )
        
        # Cultures
        tests["blood_culture"] = LabTest(
            name="Blood Culture",
            category="Microbiology",
            normal_range=(0, 0),
            unit="",
            turnaround_time=1440,  # 24 hours
            description="Bacterial culture of blood",
            clinical_significance="Positive in bacteremia, sepsis"
        )
        
        tests["urine_culture"] = LabTest(
            name="Urine Culture",
            category="Microbiology",
            normal_range=(0, 0),
            unit="",
            turnaround_time=1440,
            description="Bacterial culture of urine",
            clinical_significance="Positive in UTI"
        )
        
        tests["sputum_culture"] = LabTest(
            name="Sputum Culture",
            category="Microbiology",
            normal_range=(0, 0),
            unit="",
            turnaround_time=1440,
            description="Bacterial culture of sputum",
            clinical_significance="Positive in pneumonia"
        )
        
        # Point-of-care tests
        tests["bedside_glucose"] = LabTest(
            name="Bedside Glucose",
            category="POC",
            normal_range=(70, 140),
            unit="mg/dL",
            critical_low=40,
            critical_high=400,
            turnaround_time=2,
            description="Capillary glucose measurement",
            clinical_significance="Immediate glucose assessment"
        )
        
        tests["troponin_poc"] = LabTest(
            name="Point-of-Care Troponin",
            category="POC",
            normal_range=(0, 0.04),
            unit="ng/mL",
            critical_high=0.5,
            turnaround_time=15,
            description="Rapid troponin assay",
            clinical_significance="Quick assessment for myocardial injury"
        )
        
        tests["urine_dip"] = LabTest(
            name="Urine Dipstick",
            category="POC",
            normal_range=(0, 0),
            unit="",
            turnaround_time=5,
            description="Urine analysis",
            clinical_significance="Screening for UTI, proteinuria, hematuria"
        )
        
        # Specialty panels
        tests["thyroid_panel"] = LabTest(
            name="Thyroid Function Panel",
            category="Endocrine",
            normal_range=(0, 0),
            unit="",
            turnaround_time=180,
            description="TSH, T4, T3",
            clinical_significance="Assessment of thyroid function"
        )
        
        tests["lipid_panel"] = LabTest(
            name="Lipid Panel",
            category="Cardiovascular",
            normal_range=(0, 0),
            unit="",
            turnaround_time=240,
            description="Total cholesterol, HDL, LDL, triglycerides",
            clinical_significance="Cardiovascular risk assessment"
        )
        
        tests["cardiac_panel"] = LabTest(
            name="Cardiac Panel",
            category="Cardiac",
            normal_range=(0, 0),
            unit="",
            turnaround_time=60,
            description="Troponin, CK-MB, BNP",
            clinical_significance="Comprehensive cardiac assessment"
        )
        
        return tests
    
    def _initialize_imaging_studies(self) -> Dict[str, ImagingStudy]:
        """initialize comprehensive imaging studies"""
        studies = {}
        
        # Chest imaging
        studies["chest_xray"] = ImagingStudy(
            name="Chest X-Ray",
            modality="X-Ray",
            body_part="Chest",
            turnaround_time=30,
            cost=150.0,
            description="Standard chest radiograph",
            findings_template="Lungs: {lung_findings}. Heart: {heart_findings}. Mediastinum: {mediastinal_findings}. Bones: {bone_findings}.",
            contraindications=["pregnancy (relative)"]
        )
        
        studies["chest_ct"] = ImagingStudy(
            name="Chest CT",
            modality="CT",
            body_part="Chest",
            turnaround_time=60,
            cost=800.0,
            description="Computed tomography of chest",
            findings_template="Lungs: {lung_findings}. Mediastinum: {mediastinal_findings}. Pulmonary vessels: {vessel_findings}. Pleura: {pleural_findings}.",
            contraindications=["pregnancy", "contrast allergy", "renal insufficiency"]
        )
        
        studies["chest_ct_pe"] = ImagingStudy(
            name="Chest CT Pulmonary Angiogram",
            modality="CT",
            body_part="Chest",
            turnaround_time=60,
            cost=1200.0,
            description="CT angiography for pulmonary embolism",
            findings_template="Pulmonary arteries: {artery_findings}. Lungs: {lung_findings}. Heart: {heart_findings}.",
            contraindications=["pregnancy", "contrast allergy", "renal insufficiency"]
        )
        
        # Cardiac imaging
        studies["ecg"] = ImagingStudy(
            name="Electrocardiogram",
            modality="ECG",
            body_part="Heart",
            turnaround_time=10,
            cost=100.0,
            description="12-lead electrocardiogram",
            findings_template="Rate: {rate} bpm. Rhythm: {rhythm}. Axis: {axis}. Intervals: {intervals}. ST segments: {st_changes}. T waves: {t_waves}.",
            contraindications=[]
        )
        
        studies["echo"] = ImagingStudy(
            name="Echocardiogram",
            modality="Ultrasound",
            body_part="Heart",
            turnaround_time=45,
            cost=600.0,
            description="Transthoracic echocardiogram",
            findings_template="EF: {ef}%. Valves: {valve_findings}. Chambers: {chamber_findings}. Pericardium: {pericardial_findings}.",
            contraindications=[]
        )
        
        studies["stress_test"] = ImagingStudy(
            name="Stress Test",
            modality="Nuclear Medicine",
            body_part="Heart",
            turnaround_time=120,
            cost=1500.0,
            description="Nuclear stress test",
            findings_template="Stress images: {stress_findings}. Rest images: {rest_findings}. Ejection fraction: {ef}%. Reversibility: {reversibility}.",
            contraindications=["acute MI", "unstable angina", "severe aortic stenosis"]
        )
        
        # Abdominal imaging
        studies["abdominal_ct"] = ImagingStudy(
            name="Abdominal CT",
            modality="CT",
            body_part="Abdomen",
            turnaround_time=60,
            cost=800.0,
            description="Computed tomography of abdomen",
            findings_template="Liver: {liver_findings}. Spleen: {spleen_findings}. Kidneys: {kidney_findings}. Bowel: {bowel_findings}. Vessels: {vessel_findings}.",
            contraindications=["pregnancy", "contrast allergy", "renal insufficiency"]
        )
        
        studies["abdominal_ultrasound"] = ImagingStudy(
            name="Abdominal Ultrasound",
            modality="Ultrasound",
            body_part="Abdomen",
            turnaround_time=30,
            cost=300.0,
            description="Abdominal ultrasound",
            findings_template="Liver: {liver_findings}. Gallbladder: {gb_findings}. Kidneys: {kidney_findings}. Spleen: {spleen_findings}. Pancreas: {pancreas_findings}.",
            contraindications=[]
        )
        
        studies["renal_ultrasound"] = ImagingStudy(
            name="Renal Ultrasound",
            modality="Ultrasound",
            body_part="Kidneys",
            turnaround_time=30,
            cost=250.0,
            description="Kidney ultrasound",
            findings_template="Right kidney: {right_kidney}. Left kidney: {left_kidney}. Bladder: {bladder_findings}. Hydronephrosis: {hydronephrosis}.",
            contraindications=[]
        )
        
        # Neurological imaging
        studies["head_ct"] = ImagingStudy(
            name="Head CT",
            modality="CT",
            body_part="Head",
            turnaround_time=30,
            cost=600.0,
            description="Computed tomography of head",
            findings_template="Brain parenchyma: {brain_findings}. Ventricles: {ventricle_findings}. Basal cisterns: {cistern_findings}. Bone: {bone_findings}.",
            contraindications=["pregnancy", "contrast allergy", "renal insufficiency"]
        )
        
        studies["head_mri"] = ImagingStudy(
            name="Head MRI",
            modality="MRI",
            body_part="Head",
            turnaround_time=90,
            cost=1200.0,
            description="Magnetic resonance imaging of head",
            findings_template="Brain parenchyma: {brain_findings}. White matter: {white_matter}. Ventricles: {ventricle_findings}. Vessels: {vessel_findings}.",
            contraindications=["metallic implants", "claustrophobia", "pregnancy"]
        )
        
        studies["cervical_spine_ct"] = ImagingStudy(
            name="Cervical Spine CT",
            modality="CT",
            body_part="Neck",
            turnaround_time=45,
            cost=500.0,
            description="CT of cervical spine",
            findings_template="Alignment: {alignment}. Vertebrae: {vertebrae_findings}. Spinal canal: {canal_findings}. Soft tissues: {soft_tissue_findings}.",
            contraindications=["pregnancy", "contrast allergy"]
        )
        
        # Vascular imaging
        studies["aortic_ct"] = ImagingStudy(
            name="Aortic CT Angiogram",
            modality="CT",
            body_part="Aorta",
            turnaround_time=60,
            cost=1000.0,
            description="CT angiography of aorta",
            findings_template="Aortic diameter: {diameter} cm. Aortic wall: {wall_findings}. Branch vessels: {branch_findings}. Dissection: {dissection_findings}.",
            contraindications=["pregnancy", "contrast allergy", "renal insufficiency"]
        )
        
        studies["venous_doppler"] = ImagingStudy(
            name="Venous Doppler",
            modality="Ultrasound",
            body_part="Extremities",
            turnaround_time=30,
            cost=400.0,
            description="Venous ultrasound for DVT",
            findings_template="Compressibility: {compressibility}. Flow: {flow_findings}. Thrombus: {thrombus_findings}. Valves: {valve_findings}.",
            contraindications=[]
        )
        
        studies["arterial_doppler"] = ImagingStudy(
            name="Arterial Doppler",
            modality="Ultrasound",
            body_part="Extremities",
            turnaround_time=30,
            cost=400.0,
            description="Arterial ultrasound",
            findings_template="Flow velocities: {velocities}. Waveforms: {waveforms}. Stenosis: {stenosis_findings}. Occlusion: {occlusion_findings}.",
            contraindications=[]
        )
        
        # Trauma imaging
        studies["fast_exam"] = ImagingStudy(
            name="FAST Exam",
            modality="Ultrasound",
            body_part="Abdomen/Chest",
            turnaround_time=10,
            cost=200.0,
            description="Focused Assessment with Sonography for Trauma",
            findings_template="RUQ: {ruq_findings}. LUQ: {luq_findings}. Pelvis: {pelvis_findings}. Pericardium: {pericardial_findings}.",
            contraindications=[]
        )
        
        studies["trauma_pan_scan"] = ImagingStudy(
            name="Trauma Pan-Scan",
            modality="CT",
            body_part="Head/Neck/Chest/Abdomen/Pelvis",
            turnaround_time=90,
            cost=2000.0,
            description="Comprehensive trauma CT",
            findings_template="Head: {head_findings}. Neck: {neck_findings}. Chest: {chest_findings}. Abdomen: {abdomen_findings}. Pelvis: {pelvis_findings}.",
            contraindications=["pregnancy", "contrast allergy", "renal insufficiency"]
        )
        
        # Interventional procedures
        studies["angiogram"] = ImagingStudy(
            name="Angiogram",
            modality="Fluoroscopy",
            body_part="Vessels",
            turnaround_time=120,
            cost=3000.0,
            description="Diagnostic angiography",
            findings_template="Vessel patency: {patency}. Stenosis: {stenosis_findings}. Collaterals: {collateral_findings}. Flow: {flow_findings}.",
            contraindications=["pregnancy", "contrast allergy", "renal insufficiency", "bleeding disorder"]
        )
        
        studies["biopsy"] = ImagingStudy(
            name="Image-Guided Biopsy",
            modality="CT/Ultrasound",
            body_part="Variable",
            turnaround_time=60,
            cost=1500.0,
            description="Percutaneous biopsy",
            findings_template="Target: {target_findings}. Approach: {approach}. Specimen: {specimen_findings}. Complications: {complications}.",
            contraindications=["bleeding disorder", "infection at site", "inability to cooperate"]
        )
        
        # Nuclear medicine
        studies["bone_scan"] = ImagingStudy(
            name="Bone Scan",
            modality="Nuclear Medicine",
            body_part="Skeleton",
            turnaround_time=180,
            cost=800.0,
            description="Technetium bone scan",
            findings_template="Uptake pattern: {uptake_pattern}. Focal lesions: {focal_findings}. Distribution: {distribution_findings}.",
            contraindications=["pregnancy", "breastfeeding"]
        )
        
        studies["vq_scan"] = ImagingStudy(
            name="V/Q Scan",
            modality="Nuclear Medicine",
            body_part="Lungs",
            turnaround_time=120,
            cost=1000.0,
            description="Ventilation/perfusion scan",
            findings_template="Ventilation: {ventilation_findings}. Perfusion: {perfusion_findings}. Mismatch: {mismatch_findings}. Probability: {probability}.",
            contraindications=["pregnancy", "breastfeeding"]
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
    
    def interpret_lab_result(self, test_name: str, value: float, patient_state: PatientState) -> Dict[str, Any]:
        """interpret lab test results with clinical context"""
        if test_name not in self.lab_tests:
            return {"error": "Unknown test"}
        
        test = self.lab_tests[test_name]
        interpretation = {
            "test_name": test.name,
            "value": value,
            "unit": test.unit,
            "normal_range": test.normal_range,
            "status": "normal",
            "clinical_significance": test.clinical_significance,
            "recommendations": [],
            "critical_alert": False,
            "follow_up": []
        }
        
        # determine if result is abnormal
        if value < test.normal_range[0]:
            interpretation["status"] = "low"
            if test.critical_low and value <= test.critical_low:
                interpretation["status"] = "critical_low"
                interpretation["critical_alert"] = True
        elif value > test.normal_range[1]:
            interpretation["status"] = "high"
            if test.critical_high and value >= test.critical_high:
                interpretation["status"] = "critical_high"
                interpretation["critical_alert"] = True
        
        # generate clinical recommendations based on result and patient context
        interpretation["recommendations"] = self._generate_recommendations(test_name, value, patient_state)
        interpretation["follow_up"] = self._generate_follow_up(test_name, value, patient_state)
        
        return interpretation
    
    def _generate_recommendations(self, test_name: str, value: float, patient_state: PatientState) -> List[str]:
        """generate clinical recommendations based on test results"""
        recommendations = []
        
        if test_name == "troponin" and value > 0.04:
            recommendations.extend([
                "Consider acute coronary syndrome",
                "Order serial troponins",
                "Obtain ECG immediately",
                "Consider cardiac catheterization if STEMI"
            ])
        
        elif test_name == "potassium" and value > 6.0:
            recommendations.extend([
                "CRITICAL: Hyperkalemia",
                "Check ECG for peaked T waves",
                "Consider calcium gluconate",
                "Consider insulin/dextrose",
                "Consider sodium bicarbonate"
            ])
        
        elif test_name == "potassium" and value < 3.0:
            recommendations.extend([
                "CRITICAL: Hypokalemia",
                "Check ECG for U waves",
                "Consider potassium replacement",
                "Monitor for arrhythmias"
            ])
        
        elif test_name == "sodium" and value < 120:
            recommendations.extend([
                "CRITICAL: Severe hyponatremia",
                "Check for symptoms of cerebral edema",
                "Consider hypertonic saline",
                "Monitor neurologic status"
            ])
        
        elif test_name == "glucose" and value > 400:
            recommendations.extend([
                "CRITICAL: Severe hyperglycemia",
                "Check for ketones",
                "Consider DKA protocol",
                "Monitor electrolytes"
            ])
        
        elif test_name == "glucose" and value < 40:
            recommendations.extend([
                "CRITICAL: Severe hypoglycemia",
                "Administer dextrose immediately",
                "Check for underlying cause",
                "Monitor glucose closely"
            ])
        
        elif test_name == "ph" and value < 7.2:
            recommendations.extend([
                "CRITICAL: Severe acidosis",
                "Identify underlying cause",
                "Consider bicarbonate therapy",
                "Monitor respiratory status"
            ])
        
        elif test_name == "platelets" and value < 50:
            recommendations.extend([
                "CRITICAL: Severe thrombocytopenia",
                "Check for bleeding",
                "Consider platelet transfusion",
                "Investigate underlying cause"
            ])
        
        elif test_name == "hemoglobin" and value < 7:
            recommendations.extend([
                "CRITICAL: Severe anemia",
                "Consider blood transfusion",
                "Investigate underlying cause",
                "Monitor for symptoms"
            ])
        
        elif test_name == "creatinine" and value > 3.0:
            recommendations.extend([
                "CRITICAL: Acute kidney injury",
                "Check for reversible causes",
                "Monitor fluid status",
                "Consider nephrology consult"
            ])
        
        elif test_name == "d_dimer" and value > 0.5:
            recommendations.extend([
                "Elevated D-dimer",
                "Consider VTE evaluation",
                "Order appropriate imaging",
                "Assess clinical probability"
            ])
        
        elif test_name == "bnp" and value > 400:
            recommendations.extend([
                "Elevated BNP",
                "Consider heart failure",
                "Assess volume status",
                "Consider echocardiogram"
            ])
        
        return recommendations
    
    def _generate_follow_up(self, test_name: str, value: float, patient_state: PatientState) -> List[str]:
        """generate follow-up testing recommendations"""
        follow_up = []
        
        if test_name == "troponin" and value > 0.04:
            follow_up.extend([
                "Serial troponins in 3-6 hours",
                "ECG monitoring",
                "Cardiac catheterization if indicated"
            ])
        
        elif test_name == "d_dimer" and value > 0.5:
            follow_up.extend([
                "CT pulmonary angiogram",
                "Venous doppler ultrasound",
                "Repeat D-dimer in 1 week if negative"
            ])
        
        elif test_name == "creatinine" and value > 1.5:
            follow_up.extend([
                "Repeat creatinine in 24 hours",
                "Urinalysis",
                "Renal ultrasound if indicated"
            ])
        
        elif test_name == "glucose" and value > 200:
            follow_up.extend([
                "HbA1c",
                "Fasting glucose",
                "Diabetes education"
            ])
        
        elif test_name == "hemoglobin" and value < 10:
            follow_up.extend([
                "Iron studies",
                "B12/folate levels",
                "Consider bone marrow evaluation"
            ])
        
        return follow_up
    
    def interpret_imaging_result(self, study_name: str, findings: Dict[str, Any], patient_state: PatientState) -> Dict[str, Any]:
        """interpret imaging study results with clinical context"""
        if study_name not in self.imaging_studies:
            return {"error": "Unknown study"}
        
        study = self.imaging_studies[study_name]
        interpretation = {
            "study_name": study.name,
            "modality": study.modality,
            "findings": findings,
            "clinical_impression": "",
            "recommendations": [],
            "critical_findings": False,
            "follow_up": []
        }
        
        # generate clinical impression based on findings
        interpretation["clinical_impression"] = self._generate_imaging_impression(study_name, findings, patient_state)
        interpretation["recommendations"] = self._generate_imaging_recommendations(study_name, findings, patient_state)
        interpretation["follow_up"] = self._generate_imaging_follow_up(study_name, findings, patient_state)
        
        # check for critical findings
        interpretation["critical_findings"] = self._check_critical_imaging_findings(study_name, findings)
        
        return interpretation
    
    def _generate_imaging_impression(self, study_name: str, findings: Dict[str, Any], patient_state: PatientState) -> str:
        """generate clinical impression for imaging study"""
        if study_name == "chest_xray":
            if findings.get("pneumonia", False):
                return "Right lower lobe infiltrate consistent with pneumonia"
            elif findings.get("pneumothorax", False):
                return "Right pneumothorax with mediastinal shift"
            elif findings.get("chf", False):
                return "Pulmonary edema with cardiomegaly"
            else:
                return "Normal chest radiograph"
        
        elif study_name == "head_ct":
            if findings.get("hemorrhage", False):
                return "Intraparenchymal hemorrhage in right frontal lobe"
            elif findings.get("mass", False):
                return "Enhancing mass in left temporal lobe"
            elif findings.get("edema", False):
                return "Diffuse cerebral edema with effacement of sulci"
            else:
                return "Normal head CT"
        
        elif study_name == "chest_ct_pe":
            if findings.get("pe", False):
                return "Multiple pulmonary emboli in bilateral lower lobes"
            else:
                return "No evidence of pulmonary embolism"
        
        elif study_name == "ecg":
            if findings.get("st_elevation", False):
                return "ST elevation in leads II, III, aVF consistent with inferior STEMI"
            elif findings.get("st_depression", False):
                return "ST depression in anterior leads concerning for ischemia"
            else:
                return "Normal sinus rhythm"
        
        else:
            return "Study completed - review with clinical correlation"
    
    def _generate_imaging_recommendations(self, study_name: str, findings: Dict[str, Any], patient_state: PatientState) -> List[str]:
        """generate recommendations based on imaging findings"""
        recommendations = []
        
        if study_name == "chest_xray":
            if findings.get("pneumonia", False):
                recommendations.extend([
                    "Start antibiotics",
                    "Follow-up chest X-ray in 48-72 hours",
                    "Consider sputum culture"
                ])
            elif findings.get("pneumothorax", False):
                recommendations.extend([
                    "CRITICAL: Insert chest tube",
                    "Monitor for tension pneumothorax",
                    "Consider trauma evaluation"
                ])
        
        elif study_name == "head_ct":
            if findings.get("hemorrhage", False):
                recommendations.extend([
                    "CRITICAL: Neurosurgery consultation",
                    "Monitor for increased ICP",
                    "Consider repeat CT in 6 hours"
                ])
            elif findings.get("mass", False):
                recommendations.extend([
                    "CRITICAL: Neurosurgery consultation",
                    "Consider MRI with contrast",
                    "Monitor for neurologic changes"
                ])
        
        elif study_name == "chest_ct_pe":
            if findings.get("pe", False):
                recommendations.extend([
                    "CRITICAL: Anticoagulation therapy",
                    "Consider thrombolysis if massive PE",
                    "Monitor for hemodynamic instability"
                ])
        
        elif study_name == "ecg":
            if findings.get("st_elevation", False):
                recommendations.extend([
                    "CRITICAL: Activate cardiac catheterization",
                    "Aspirin 325mg",
                    "Heparin bolus and infusion"
                ])
        
        return recommendations
    
    def _generate_imaging_follow_up(self, study_name: str, findings: Dict[str, Any], patient_state: PatientState) -> List[str]:
        """generate follow-up recommendations for imaging"""
        follow_up = []
        
        if study_name == "chest_xray":
            if findings.get("pneumonia", False):
                follow_up.append("Repeat chest X-ray in 48-72 hours")
            elif findings.get("mass", False):
                follow_up.extend([
                    "CT chest with contrast",
                    "Consider biopsy"
                ])
        
        elif study_name == "head_ct":
            if findings.get("mass", False):
                follow_up.extend([
                    "MRI brain with contrast",
                    "Neurosurgery consultation"
                ])
        
        elif study_name == "chest_ct_pe":
            if findings.get("pe", False):
                follow_up.extend([
                    "Echocardiogram",
                    "Lower extremity doppler",
                    "Consider IVC filter"
                ])
        
        return follow_up
    
    def _check_critical_imaging_findings(self, study_name: str, findings: Dict[str, Any]) -> bool:
        """check if imaging findings are critical"""
        critical_findings = [
            "pneumothorax", "hemorrhage", "mass", "pe", "st_elevation",
            "aortic_dissection", "bowel_perforation", "spinal_cord_injury"
        ]
        
        for finding in critical_findings:
            if findings.get(finding, False):
                return True
        
        return False
    
    def get_critical_alerts(self, patient_state: PatientState) -> List[Dict[str, Any]]:
        """get all critical lab and imaging alerts for patient"""
        alerts = []
        
        # check lab results
        for test_name, result in patient_state.lab_results.items():
            if test_name in self.lab_tests:
                test = self.lab_tests[test_name]
                value = result.get("value", 0)
                
                if test.critical_low and value <= test.critical_low:
                    alerts.append({
                        "type": "lab",
                        "test": test_name,
                        "value": value,
                        "severity": "critical_low",
                        "message": f"CRITICAL: {test.name} = {value} {test.unit}"
                    })
                
                elif test.critical_high and value >= test.critical_high:
                    alerts.append({
                        "type": "lab",
                        "test": test_name,
                        "value": value,
                        "severity": "critical_high",
                        "message": f"CRITICAL: {test.name} = {value} {test.unit}"
                    })
        
        # check imaging results
        for study_name, result in patient_state.imaging_results.items():
            if study_name in self.imaging_studies:
                findings = result.get("findings", {})
                if self._check_critical_imaging_findings(study_name, findings):
                    study = self.imaging_studies[study_name]
                    alerts.append({
                        "type": "imaging",
                        "study": study_name,
                        "severity": "critical",
                        "message": f"CRITICAL: {study.name} shows critical findings"
                    })
        
        return alerts 