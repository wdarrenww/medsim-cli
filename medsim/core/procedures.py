"""
comprehensive medical procedures library for simulation
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class ProcedureCategory(Enum):
    """procedure categories"""
    DIAGNOSTIC = "diagnostic"
    THERAPEUTIC = "therapeutic"
    SURGICAL = "surgical"
    EMERGENCY = "emergency"
    PREVENTIVE = "preventive"


class ProcedureComplexity(Enum):
    """procedure complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    CRITICAL = "critical"


@dataclass
class Procedure:
    """medical procedure definition"""
    name: str
    category: ProcedureCategory
    complexity: ProcedureComplexity
    description: str
    indications: List[str] = field(default_factory=list)
    contraindications: List[str] = field(default_factory=list)
    complications: List[str] = field(default_factory=list)
    equipment_required: List[str] = field(default_factory=list)
    personnel_required: List[str] = field(default_factory=list)
    duration_minutes: int = 30
    success_rate: float = 0.95
    cost: float = 500.0
    anesthesia_required: bool = False
    sterile_technique: bool = True
    follow_up_required: bool = False
    recovery_time_hours: int = 0


class ComprehensiveProcedureLibrary:
    """comprehensive library of medical procedures"""
    
    def __init__(self):
        self.procedures = self._initialize_procedures()
    
    def _initialize_procedures(self) -> Dict[str, Procedure]:
        """initialize comprehensive procedure library"""
        procedures = {}
        
        # diagnostic procedures
        procedures["lumbar_puncture"] = Procedure(
            name="Lumbar Puncture",
            category=ProcedureCategory.DIAGNOSTIC,
            complexity=ProcedureComplexity.MODERATE,
            description="Insertion of needle into subarachnoid space to collect CSF",
            indications=["meningitis", "subarachnoid hemorrhage", "multiple sclerosis"],
            contraindications=["increased intracranial pressure", "coagulopathy", "local infection"],
            complications=["headache", "infection", "bleeding", "nerve injury"],
            equipment_required=["spinal needle", "sterile gloves", "antiseptic", "local anesthetic"],
            personnel_required=["physician", "nurse"],
            duration_minutes=30,
            success_rate=0.90,
            cost=800.0,
            anesthesia_required=False,
            sterile_technique=True,
            follow_up_required=True,
            recovery_time_hours=4
        )
        
        procedures["thoracentesis"] = Procedure(
            name="Thoracentesis",
            category=ProcedureCategory.DIAGNOSTIC,
            complexity=ProcedureComplexity.MODERATE,
            description="Removal of fluid from pleural space",
            indications=["pleural effusion", "pneumonia", "malignancy"],
            contraindications=["coagulopathy", "local infection", "small effusion"],
            complications=["pneumothorax", "bleeding", "infection", "re-expansion pulmonary edema"],
            equipment_required=["needle", "syringe", "sterile gloves", "antiseptic"],
            personnel_required=["physician", "nurse"],
            duration_minutes=20,
            success_rate=0.95,
            cost=600.0,
            anesthesia_required=False,
            sterile_technique=True,
            follow_up_required=True,
            recovery_time_hours=2
        )
        
        procedures["paracentesis"] = Procedure(
            name="Paracentesis",
            category=ProcedureCategory.DIAGNOSTIC,
            complexity=ProcedureComplexity.MODERATE,
            description="Removal of fluid from abdominal cavity",
            indications=["ascites", "peritonitis", "malignancy"],
            contraindications=["coagulopathy", "local infection", "bowel obstruction"],
            complications=["bleeding", "infection", "bowel perforation", "hypotension"],
            equipment_required=["needle", "syringe", "sterile gloves", "antiseptic"],
            personnel_required=["physician", "nurse"],
            duration_minutes=30,
            success_rate=0.95,
            cost=500.0,
            anesthesia_required=False,
            sterile_technique=True,
            follow_up_required=True,
            recovery_time_hours=2
        )
        
        procedures["bone_marrow_biopsy"] = Procedure(
            name="Bone Marrow Biopsy",
            category=ProcedureCategory.DIAGNOSTIC,
            complexity=ProcedureComplexity.MODERATE,
            description="Removal of bone marrow for analysis",
            indications=["anemia", "leukemia", "lymphoma", "infection"],
            contraindications=["coagulopathy", "local infection", "thrombocytopenia"],
            complications=["bleeding", "infection", "pain", "fracture"],
            equipment_required=["biopsy needle", "sterile gloves", "antiseptic", "local anesthetic"],
            personnel_required=["physician", "nurse"],
            duration_minutes=45,
            success_rate=0.90,
            cost=1200.0,
            anesthesia_required=False,
            sterile_technique=True,
            follow_up_required=True,
            recovery_time_hours=6
        )
        
        # therapeutic procedures
        procedures["central_line_insertion"] = Procedure(
            name="Central Line Insertion",
            category=ProcedureCategory.THERAPEUTIC,
            complexity=ProcedureComplexity.COMPLEX,
            description="Insertion of catheter into central vein",
            indications=["long-term IV access", "TPN", "chemotherapy", "hemodialysis"],
            contraindications=["coagulopathy", "local infection", "venous thrombosis"],
            complications=["infection", "bleeding", "pneumothorax", "thrombosis"],
            equipment_required=["central line kit", "sterile gloves", "antiseptic", "ultrasound"],
            personnel_required=["physician", "nurse"],
            duration_minutes=60,
            success_rate=0.85,
            cost=1500.0,
            anesthesia_required=False,
            sterile_technique=True,
            follow_up_required=True,
            recovery_time_hours=2
        )
        
        procedures["chest_tube_insertion"] = Procedure(
            name="Chest Tube Insertion",
            category=ProcedureCategory.THERAPEUTIC,
            complexity=ProcedureComplexity.COMPLEX,
            description="Insertion of tube into pleural space",
            indications=["pneumothorax", "pleural effusion", "hemothorax"],
            contraindications=["coagulopathy", "local infection", "small pneumothorax"],
            complications=["infection", "bleeding", "lung injury", "tube dislodgement"],
            equipment_required=["chest tube", "sterile gloves", "antiseptic", "local anesthetic"],
            personnel_required=["physician", "nurse"],
            duration_minutes=45,
            success_rate=0.90,
            cost=1000.0,
            anesthesia_required=False,
            sterile_technique=True,
            follow_up_required=True,
            recovery_time_hours=4
        )
        
        procedures["endotracheal_intubation"] = Procedure(
            name="Endotracheal Intubation",
            category=ProcedureCategory.EMERGENCY,
            complexity=ProcedureComplexity.CRITICAL,
            description="Insertion of tube into trachea for ventilation",
            indications=["respiratory failure", "airway protection", "general anesthesia"],
            contraindications=["facial trauma", "airway obstruction", "cervical spine injury"],
            complications=["esophageal intubation", "trauma", "infection", "tube dislodgement"],
            equipment_required=["endotracheal tube", "laryngoscope", "stylet", "suction"],
            personnel_required=["physician", "nurse", "respiratory therapist"],
            duration_minutes=5,
            success_rate=0.95,
            cost=800.0,
            anesthesia_required=True,
            sterile_technique=False,
            follow_up_required=True,
            recovery_time_hours=0
        )
        
        procedures["cardiopulmonary_resuscitation"] = Procedure(
            name="Cardiopulmonary Resuscitation",
            category=ProcedureCategory.EMERGENCY,
            complexity=ProcedureComplexity.CRITICAL,
            description="Emergency procedure for cardiac arrest",
            indications=["cardiac arrest", "respiratory arrest"],
            contraindications=["do not resuscitate order", "obvious death"],
            complications=["rib fractures", "organ injury", "brain injury"],
            equipment_required=["defibrillator", "airway equipment", "medications"],
            personnel_required=["physician", "nurse", "respiratory therapist"],
            duration_minutes=30,
            success_rate=0.30,
            cost=2000.0,
            anesthesia_required=False,
            sterile_technique=False,
            follow_up_required=True,
            recovery_time_hours=0
        )
        
        # surgical procedures
        procedures["appendectomy"] = Procedure(
            name="Appendectomy",
            category=ProcedureCategory.SURGICAL,
            complexity=ProcedureComplexity.MODERATE,
            description="Surgical removal of appendix",
            indications=["acute appendicitis", "appendiceal abscess"],
            contraindications=["severe comorbidities", "patient refusal"],
            complications=["infection", "bleeding", "bowel injury", "adhesions"],
            equipment_required=["surgical instruments", "laparoscope", "sterile drapes"],
            personnel_required=["surgeon", "anesthesiologist", "nurse"],
            duration_minutes=90,
            success_rate=0.95,
            cost=5000.0,
            anesthesia_required=True,
            sterile_technique=True,
            follow_up_required=True,
            recovery_time_hours=24
        )
        
        procedures["cholecystectomy"] = Procedure(
            name="Cholecystectomy",
            category=ProcedureCategory.SURGICAL,
            complexity=ProcedureComplexity.MODERATE,
            description="Surgical removal of gallbladder",
            indications=["cholecystitis", "gallstones", "biliary colic"],
            contraindications=["severe comorbidities", "patient refusal"],
            complications=["infection", "bleeding", "bile duct injury", "adhesions"],
            equipment_required=["surgical instruments", "laparoscope", "sterile drapes"],
            personnel_required=["surgeon", "anesthesiologist", "nurse"],
            duration_minutes=120,
            success_rate=0.95,
            cost=8000.0,
            anesthesia_required=True,
            sterile_technique=True,
            follow_up_required=True,
            recovery_time_hours=48
        )
        
        procedures["hernia_repair"] = Procedure(
            name="Hernia Repair",
            category=ProcedureCategory.SURGICAL,
            complexity=ProcedureComplexity.MODERATE,
            description="Surgical repair of abdominal wall hernia",
            indications=["inguinal hernia", "umbilical hernia", "incisional hernia"],
            contraindications=["severe comorbidities", "patient refusal"],
            complications=["infection", "bleeding", "recurrence", "chronic pain"],
            equipment_required=["surgical instruments", "mesh", "sterile drapes"],
            personnel_required=["surgeon", "anesthesiologist", "nurse"],
            duration_minutes=60,
            success_rate=0.90,
            cost=6000.0,
            anesthesia_required=True,
            sterile_technique=True,
            follow_up_required=True,
            recovery_time_hours=24
        )
        
        # emergency procedures
        procedures["cricothyrotomy"] = Procedure(
            name="Cricothyrotomy",
            category=ProcedureCategory.EMERGENCY,
            complexity=ProcedureComplexity.CRITICAL,
            description="Emergency airway access through cricothyroid membrane",
            indications=["failed intubation", "upper airway obstruction", "facial trauma"],
            contraindications=["laryngeal trauma", "cervical spine injury"],
            complications=["bleeding", "infection", "vocal cord injury", "esophageal injury"],
            equipment_required=["scalpel", "tracheostomy tube", "sterile gloves"],
            personnel_required=["physician", "nurse"],
            duration_minutes=5,
            success_rate=0.80,
            cost=1500.0,
            anesthesia_required=False,
            sterile_technique=False,
            follow_up_required=True,
            recovery_time_hours=0
        )
        
        procedures["pericardiocentesis"] = Procedure(
            name="Pericardiocentesis",
            category=ProcedureCategory.EMERGENCY,
            complexity=ProcedureComplexity.CRITICAL,
            description="Removal of fluid from pericardial space",
            indications=["cardiac tamponade", "pericardial effusion"],
            contraindications=["coagulopathy", "small effusion"],
            complications=["cardiac injury", "bleeding", "infection", "pneumothorax"],
            equipment_required=["needle", "syringe", "sterile gloves", "ECG"],
            personnel_required=["physician", "nurse"],
            duration_minutes=30,
            success_rate=0.85,
            cost=2000.0,
            anesthesia_required=False,
            sterile_technique=True,
            follow_up_required=True,
            recovery_time_hours=4
        )
        
        procedures["emergency_laparotomy"] = Procedure(
            name="Emergency Laparotomy",
            category=ProcedureCategory.EMERGENCY,
            complexity=ProcedureComplexity.CRITICAL,
            description="Emergency abdominal surgery",
            indications=["peritonitis", "abdominal trauma", "bowel obstruction"],
            contraindications=["patient refusal", "futility"],
            complications=["infection", "bleeding", "organ injury", "adhesions"],
            equipment_required=["surgical instruments", "sterile drapes", "suction"],
            personnel_required=["surgeon", "anesthesiologist", "nurse"],
            duration_minutes=180,
            success_rate=0.70,
            cost=15000.0,
            anesthesia_required=True,
            sterile_technique=True,
            follow_up_required=True,
            recovery_time_hours=72
        )
        
        # preventive procedures
        procedures["vaccination"] = Procedure(
            name="Vaccination",
            category=ProcedureCategory.PREVENTIVE,
            complexity=ProcedureComplexity.SIMPLE,
            description="Administration of vaccine for disease prevention",
            indications=["disease prevention", "travel", "occupational requirements"],
            contraindications=["allergy to vaccine", "pregnancy", "immunosuppression"],
            complications=["local reaction", "fever", "allergic reaction", "anaphylaxis"],
            equipment_required=["syringe", "needle", "vaccine", "alcohol swab"],
            personnel_required=["nurse", "physician"],
            duration_minutes=5,
            success_rate=0.99,
            cost=50.0,
            anesthesia_required=False,
            sterile_technique=True,
            follow_up_required=False,
            recovery_time_hours=0
        )
        
        procedures["screening_colonoscopy"] = Procedure(
            name="Screening Colonoscopy",
            category=ProcedureCategory.PREVENTIVE,
            complexity=ProcedureComplexity.MODERATE,
            description="Endoscopic examination of colon for cancer screening",
            indications=["colorectal cancer screening", "family history", "age 50+"],
            contraindications=["bowel perforation", "severe colitis", "patient refusal"],
            complications=["bleeding", "perforation", "infection", "sedation complications"],
            equipment_required=["colonoscope", "biopsy forceps", "sedation medications"],
            personnel_required=["gastroenterologist", "nurse", "anesthesiologist"],
            duration_minutes=60,
            success_rate=0.95,
            cost=2000.0,
            anesthesia_required=True,
            sterile_technique=True,
            follow_up_required=True,
            recovery_time_hours=4
        )
        
        procedures["mammography"] = Procedure(
            name="Mammography",
            category=ProcedureCategory.PREVENTIVE,
            complexity=ProcedureComplexity.SIMPLE,
            description="X-ray imaging of breast for cancer screening",
            indications=["breast cancer screening", "age 40+", "family history"],
            contraindications=["pregnancy", "recent breast surgery"],
            complications=["radiation exposure", "false positive", "anxiety"],
            equipment_required=["mammography machine", "compression paddles"],
            personnel_required=["radiologic technologist", "radiologist"],
            duration_minutes=15,
            success_rate=0.98,
            cost=200.0,
            anesthesia_required=False,
            sterile_technique=False,
            follow_up_required=False,
            recovery_time_hours=0
        )
        
        # diagnostic procedures
        procedures["endoscopy"] = Procedure(
            name="Upper Endoscopy",
            category=ProcedureCategory.DIAGNOSTIC,
            complexity=ProcedureComplexity.MODERATE,
            description="Endoscopic examination of upper GI tract",
            indications=["dysphagia", "abdominal pain", "GI bleeding", "reflux"],
            contraindications=["bowel perforation", "severe bleeding", "patient refusal"],
            complications=["bleeding", "perforation", "infection", "sedation complications"],
            equipment_required=["endoscope", "biopsy forceps", "sedation medications"],
            personnel_required=["gastroenterologist", "nurse", "anesthesiologist"],
            duration_minutes=30,
            success_rate=0.95,
            cost=1500.0,
            anesthesia_required=True,
            sterile_technique=True,
            follow_up_required=True,
            recovery_time_hours=2
        )
        
        procedures["bronchoscopy"] = Procedure(
            name="Bronchoscopy",
            category=ProcedureCategory.DIAGNOSTIC,
            complexity=ProcedureComplexity.MODERATE,
            description="Endoscopic examination of airways",
            indications=["cough", "hemoptysis", "lung mass", "infection"],
            contraindications=["severe respiratory distress", "coagulopathy", "patient refusal"],
            complications=["bleeding", "infection", "pneumothorax", "sedation complications"],
            equipment_required=["bronchoscope", "biopsy forceps", "sedation medications"],
            personnel_required=["pulmonologist", "nurse", "respiratory therapist"],
            duration_minutes=45,
            success_rate=0.90,
            cost=2000.0,
            anesthesia_required=True,
            sterile_technique=True,
            follow_up_required=True,
            recovery_time_hours=4
        )
        
        return procedures
    
    def get_procedure(self, name: str) -> Optional[Procedure]:
        """get a specific procedure by name"""
        return self.procedures.get(name.lower().replace(" ", "_"))
    
    def get_procedures_by_category(self, category: ProcedureCategory) -> List[Procedure]:
        """get all procedures in a category"""
        return [procedure for procedure in self.procedures.values() if procedure.category == category]
    
    def get_procedures_by_complexity(self, complexity: ProcedureComplexity) -> List[Procedure]:
        """get all procedures of a specific complexity"""
        return [procedure for procedure in self.procedures.values() if procedure.complexity == complexity]
    
    def search_procedures(self, query: str) -> List[Procedure]:
        """search procedures by name or description"""
        query = query.lower()
        results = []
        for procedure in self.procedures.values():
            if (query in procedure.name.lower() or 
                query in procedure.description.lower() or
                any(query in indication.lower() for indication in procedure.indications)):
                results.append(procedure)
        return results
    
    def get_emergency_procedures(self) -> List[Procedure]:
        """get emergency procedures"""
        return [procedure for procedure in self.procedures.values() if procedure.category == ProcedureCategory.EMERGENCY]
    
    def get_critical_procedures(self) -> List[Procedure]:
        """get procedures with critical complexity"""
        return [procedure for procedure in self.procedures.values() if procedure.complexity == ProcedureComplexity.CRITICAL]
    
    def get_all_procedures(self) -> Dict[str, Procedure]:
        """get all procedures"""
        return self.procedures.copy() 