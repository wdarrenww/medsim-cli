"""
comprehensive symptoms library for medical simulation
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class SymptomSeverity(Enum):
    """symptom severity levels"""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


class SymptomCategory(Enum):
    """symptom categories"""
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    GASTROINTESTINAL = "gastrointestinal"
    NEUROLOGICAL = "neurological"
    MUSCULOSKELETAL = "musculoskeletal"
    DERMATOLOGICAL = "dermatological"
    GENITOURINARY = "genitourinary"
    ENDOCRINE = "endocrine"
    HEMATOLOGICAL = "hematological"
    PSYCHIATRIC = "psychiatric"
    GENERAL = "general"


@dataclass
class Symptom:
    """symptom definition"""
    name: str
    category: SymptomCategory
    description: str
    severity: SymptomSeverity
    associated_conditions: List[str] = field(default_factory=list)
    differential_diagnosis: List[str] = field(default_factory=list)
    red_flags: List[str] = field(default_factory=list)
    common_causes: List[str] = field(default_factory=list)
    typical_duration: str = ""
    aggravating_factors: List[str] = field(default_factory=list)
    relieving_factors: List[str] = field(default_factory=list)
    associated_symptoms: List[str] = field(default_factory=list)


class ComprehensiveSymptomLibrary:
    """comprehensive library of medical symptoms"""
    
    def __init__(self):
        self.symptoms = self._initialize_symptoms()
    
    def _initialize_symptoms(self) -> Dict[str, Symptom]:
        """initialize comprehensive symptom library"""
        symptoms = {}
        
        # cardiovascular symptoms
        symptoms["chest_pain"] = Symptom(
            name="Chest Pain",
            category=SymptomCategory.CARDIOVASCULAR,
            description="Pain or discomfort in the chest area",
            severity=SymptomSeverity.SEVERE,
            associated_conditions=["myocardial infarction", "angina", "aortic dissection", "pulmonary embolism"],
            differential_diagnosis=["GERD", "costochondritis", "pneumonia", "anxiety"],
            red_flags=["crushing pain", "radiation to arm/jaw", "sweating", "shortness of breath"],
            common_causes=["coronary artery disease", "musculoskeletal", "gastrointestinal"],
            typical_duration="variable",
            aggravating_factors=["exertion", "stress", "cold weather"],
            relieving_factors=["rest", "nitroglycerin", "antacids"],
            associated_symptoms=["shortness of breath", "nausea", "sweating", "dizziness"]
        )
        
        symptoms["shortness_of_breath"] = Symptom(
            name="Shortness of Breath",
            category=SymptomCategory.RESPIRATORY,
            description="Difficulty breathing or feeling of breathlessness",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["heart failure", "pneumonia", "COPD", "pulmonary embolism"],
            differential_diagnosis=["anxiety", "anemia", "obesity", "deconditioning"],
            red_flags=["sudden onset", "chest pain", "cyanosis", "altered mental status"],
            common_causes=["cardiac", "pulmonary", "anxiety"],
            typical_duration="variable",
            aggravating_factors=["exertion", "lying flat", "exposure to triggers"],
            relieving_factors=["rest", "upright position", "bronchodilators"],
            associated_symptoms=["chest pain", "cough", "fatigue", "anxiety"]
        )
        
        symptoms["palpitations"] = Symptom(
            name="Palpitations",
            category=SymptomCategory.CARDIOVASCULAR,
            description="Sensation of rapid, irregular, or forceful heartbeat",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["atrial fibrillation", "ventricular tachycardia", "anxiety"],
            differential_diagnosis=["normal sinus rhythm", "premature beats", "anxiety"],
            red_flags=["syncope", "chest pain", "shortness of breath"],
            common_causes=["anxiety", "caffeine", "medications", "arrhythmias"],
            typical_duration="minutes to hours",
            aggravating_factors=["stress", "caffeine", "alcohol"],
            relieving_factors=["rest", "vagal maneuvers"],
            associated_symptoms=["anxiety", "chest pain", "dizziness"]
        )
        
        symptoms["syncope"] = Symptom(
            name="Syncope",
            category=SymptomCategory.NEUROLOGICAL,
            description="Temporary loss of consciousness due to decreased blood flow to brain",
            severity=SymptomSeverity.SEVERE,
            associated_conditions=["cardiac arrhythmia", "orthostatic hypotension", "seizure"],
            differential_diagnosis=["vasovagal", "cardiac", "neurological", "psychogenic"],
            red_flags=["chest pain", "palpitations", "head injury", "focal neurological signs"],
            common_causes=["vasovagal", "orthostatic", "cardiac", "neurological"],
            typical_duration="seconds to minutes",
            aggravating_factors=["prolonged standing", "dehydration", "pain"],
            relieving_factors=["lying down", "hydration"],
            associated_symptoms=["dizziness", "nausea", "sweating", "palpitations"]
        )
        
        # respiratory symptoms
        symptoms["cough"] = Symptom(
            name="Cough",
            category=SymptomCategory.RESPIRATORY,
            description="Sudden expulsion of air from lungs",
            severity=SymptomSeverity.MILD,
            associated_conditions=["upper respiratory infection", "pneumonia", "COPD", "asthma"],
            differential_diagnosis=["post-nasal drip", "GERD", "medication side effect"],
            red_flags=["blood in sputum", "weight loss", "fever", "chest pain"],
            common_causes=["viral infection", "allergies", "smoking", "medications"],
            typical_duration="days to weeks",
            aggravating_factors=["cold air", "allergens", "lying down"],
            relieving_factors=["humidifier", "cough suppressants", "treating underlying cause"],
            associated_symptoms=["sore throat", "runny nose", "fever", "fatigue"]
        )
        
        symptoms["wheezing"] = Symptom(
            name="Wheezing",
            category=SymptomCategory.RESPIRATORY,
            description="High-pitched whistling sound during breathing",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["asthma", "COPD", "bronchitis", "heart failure"],
            differential_diagnosis=["foreign body", "tumor", "vocal cord dysfunction"],
            red_flags=["severe respiratory distress", "cyanosis", "altered mental status"],
            common_causes=["asthma", "COPD", "bronchitis", "allergies"],
            typical_duration="variable",
            aggravating_factors=["allergens", "exercise", "cold air", "respiratory infections"],
            relieving_factors=["bronchodilators", "steroids", "avoiding triggers"],
            associated_symptoms=["shortness of breath", "cough", "chest tightness"]
        )
        
        # gastrointestinal symptoms
        symptoms["abdominal_pain"] = Symptom(
            name="Abdominal Pain",
            category=SymptomCategory.GASTROINTESTINAL,
            description="Pain or discomfort in the abdomen",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["appendicitis", "cholecystitis", "diverticulitis", "peptic ulcer"],
            differential_diagnosis=["irritable bowel syndrome", "constipation", "gas", "anxiety"],
            red_flags=["severe pain", "rigid abdomen", "fever", "vomiting"],
            common_causes=["gas", "constipation", "infection", "inflammation"],
            typical_duration="variable",
            aggravating_factors=["eating", "movement", "stress"],
            relieving_factors=["rest", "heat", "antacids"],
            associated_symptoms=["nausea", "vomiting", "diarrhea", "constipation"]
        )
        
        symptoms["nausea"] = Symptom(
            name="Nausea",
            category=SymptomCategory.GASTROINTESTINAL,
            description="Sensation of wanting to vomit",
            severity=SymptomSeverity.MILD,
            associated_conditions=["gastroenteritis", "pregnancy", "migraine", "medication side effect"],
            differential_diagnosis=["anxiety", "motion sickness", "food poisoning"],
            red_flags=["severe abdominal pain", "headache", "fever", "dehydration"],
            common_causes=["viral infection", "pregnancy", "medications", "anxiety"],
            typical_duration="hours to days",
            aggravating_factors=["strong odors", "certain foods", "motion"],
            relieving_factors=["rest", "small meals", "antiemetics"],
            associated_symptoms=["vomiting", "abdominal pain", "dizziness", "sweating"]
        )
        
        symptoms["vomiting"] = Symptom(
            name="Vomiting",
            category=SymptomCategory.GASTROINTESTINAL,
            description="Forceful expulsion of stomach contents",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["gastroenteritis", "pregnancy", "migraine", "food poisoning"],
            differential_diagnosis=["anxiety", "motion sickness", "medication side effect"],
            red_flags=["blood in vomit", "severe abdominal pain", "headache", "dehydration"],
            common_causes=["viral infection", "food poisoning", "pregnancy", "medications"],
            typical_duration="hours to days",
            aggravating_factors=["certain foods", "motion", "strong odors"],
            relieving_factors=["rest", "hydration", "antiemetics"],
            associated_symptoms=["nausea", "abdominal pain", "dehydration", "weakness"]
        )
        
        symptoms["diarrhea"] = Symptom(
            name="Diarrhea",
            category=SymptomCategory.GASTROINTESTINAL,
            description="Loose, watery stools occurring more frequently than normal",
            severity=SymptomSeverity.MILD,
            associated_conditions=["gastroenteritis", "food poisoning", "irritable bowel syndrome"],
            differential_diagnosis=["medication side effect", "anxiety", "dietary changes"],
            red_flags=["blood in stool", "severe abdominal pain", "dehydration", "fever"],
            common_causes=["viral infection", "food poisoning", "medications", "dietary changes"],
            typical_duration="days",
            aggravating_factors=["certain foods", "stress", "medications"],
            relieving_factors=["hydration", "bland diet", "antidiarrheals"],
            associated_symptoms=["abdominal pain", "nausea", "dehydration", "weakness"]
        )
        
        symptoms["constipation"] = Symptom(
            name="Constipation",
            category=SymptomCategory.GASTROINTESTINAL,
            description="Infrequent or difficult bowel movements",
            severity=SymptomSeverity.MILD,
            associated_conditions=["irritable bowel syndrome", "hypothyroidism", "medication side effect"],
            differential_diagnosis=["dehydration", "low fiber diet", "lack of exercise"],
            red_flags=["severe abdominal pain", "blood in stool", "weight loss"],
            common_causes=["low fiber diet", "dehydration", "lack of exercise", "medications"],
            typical_duration="days to weeks",
            aggravating_factors=["low fiber diet", "dehydration", "sedentary lifestyle"],
            relieving_factors=["high fiber diet", "hydration", "exercise", "laxatives"],
            associated_symptoms=["abdominal pain", "bloating", "straining", "hard stools"]
        )
        
        # neurological symptoms
        symptoms["headache"] = Symptom(
            name="Headache",
            category=SymptomCategory.NEUROLOGICAL,
            description="Pain in the head or upper neck",
            severity=SymptomSeverity.MILD,
            associated_conditions=["migraine", "tension headache", "cluster headache", "meningitis"],
            differential_diagnosis=["sinusitis", "eye strain", "dehydration", "anxiety"],
            red_flags=["sudden severe pain", "fever", "altered mental status", "focal neurological signs"],
            common_causes=["tension", "dehydration", "lack of sleep", "stress"],
            typical_duration="hours to days",
            aggravating_factors=["stress", "lack of sleep", "certain foods", "bright lights"],
            relieving_factors=["rest", "pain medications", "hydration", "dark room"],
            associated_symptoms=["nausea", "sensitivity to light", "sensitivity to sound"]
        )
        
        symptoms["dizziness"] = Symptom(
            name="Dizziness",
            category=SymptomCategory.NEUROLOGICAL,
            description="Sensation of spinning or lightheadedness",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["vertigo", "orthostatic hypotension", "anxiety", "inner ear problems"],
            differential_diagnosis=["dehydration", "medication side effect", "anemia"],
            red_flags=["focal neurological signs", "chest pain", "palpitations", "syncope"],
            common_causes=["inner ear problems", "dehydration", "anxiety", "medications"],
            typical_duration="minutes to hours",
            aggravating_factors=["sudden movement", "standing up quickly", "stress"],
            relieving_factors=["rest", "hydration", "avoiding triggers"],
            associated_symptoms=["nausea", "sweating", "palpitations", "anxiety"]
        )
        
        symptoms["numbness"] = Symptom(
            name="Numbness",
            category=SymptomCategory.NEUROLOGICAL,
            description="Loss of sensation in a part of the body",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["peripheral neuropathy", "stroke", "carpal tunnel syndrome"],
            differential_diagnosis=["anxiety", "medication side effect", "compression"],
            red_flags=["sudden onset", "focal distribution", "weakness", "speech problems"],
            common_causes=["nerve compression", "diabetes", "vitamin deficiency", "medications"],
            typical_duration="variable",
            aggravating_factors=["prolonged pressure", "repetitive motion", "cold"],
            relieving_factors=["changing position", "treating underlying cause"],
            associated_symptoms=["tingling", "weakness", "pain", "burning"]
        )
        
        symptoms["weakness"] = Symptom(
            name="Weakness",
            category=SymptomCategory.NEUROLOGICAL,
            description="Reduced strength in muscles",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["stroke", "multiple sclerosis", "myasthenia gravis", "muscle disease"],
            differential_diagnosis=["fatigue", "deconditioning", "anxiety", "depression"],
            red_flags=["sudden onset", "focal distribution", "speech problems", "vision changes"],
            common_causes=["deconditioning", "fatigue", "anxiety", "medications"],
            typical_duration="variable",
            aggravating_factors=["exertion", "stress", "lack of sleep"],
            relieving_factors=["rest", "exercise", "treating underlying cause"],
            associated_symptoms=["fatigue", "numbness", "pain", "difficulty with activities"]
        )
        
        # musculoskeletal symptoms
        symptoms["joint_pain"] = Symptom(
            name="Joint Pain",
            category=SymptomCategory.MUSCULOSKELETAL,
            description="Pain in or around joints",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["arthritis", "gout", "bursitis", "tendonitis"],
            differential_diagnosis=["overuse", "injury", "infection", "autoimmune disease"],
            red_flags=["severe pain", "swelling", "redness", "fever"],
            common_causes=["overuse", "injury", "aging", "inflammation"],
            typical_duration="days to weeks",
            aggravating_factors=["movement", "weight bearing", "cold weather"],
            relieving_factors=["rest", "ice", "heat", "anti-inflammatory medications"],
            associated_symptoms=["stiffness", "swelling", "reduced range of motion"]
        )
        
        symptoms["back_pain"] = Symptom(
            name="Back Pain",
            category=SymptomCategory.MUSCULOSKELETAL,
            description="Pain in the back, usually lower back",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["herniated disc", "muscle strain", "spinal stenosis", "arthritis"],
            differential_diagnosis=["kidney stone", "infection", "tumor", "referred pain"],
            red_flags=["saddle anesthesia", "bowel/bladder dysfunction", "fever", "weight loss"],
            common_causes=["muscle strain", "poor posture", "lifting", "aging"],
            typical_duration="days to weeks",
            aggravating_factors=["lifting", "bending", "sitting", "standing"],
            relieving_factors=["rest", "heat", "ice", "exercise", "physical therapy"],
            associated_symptoms=["stiffness", "muscle spasms", "radiating pain"]
        )
        
        # dermatological symptoms
        symptoms["rash"] = Symptom(
            name="Rash",
            category=SymptomCategory.DERMATOLOGICAL,
            description="Area of irritated or swollen skin",
            severity=SymptomSeverity.MILD,
            associated_conditions=["allergic reaction", "infection", "autoimmune disease", "contact dermatitis"],
            differential_diagnosis=["eczema", "psoriasis", "fungal infection", "viral exanthem"],
            red_flags=["widespread", "blisters", "fever", "difficulty breathing"],
            common_causes=["allergic reaction", "infection", "irritation", "autoimmune"],
            typical_duration="days to weeks",
            aggravating_factors=["scratching", "certain soaps", "allergens", "stress"],
            relieving_factors=["cooling", "moisturizing", "antihistamines", "steroids"],
            associated_symptoms=["itching", "redness", "swelling", "pain"]
        )
        
        symptoms["itching"] = Symptom(
            name="Itching",
            category=SymptomCategory.DERMATOLOGICAL,
            description="Sensation that causes desire to scratch",
            severity=SymptomSeverity.MILD,
            associated_conditions=["allergic reaction", "dry skin", "infection", "liver disease"],
            differential_diagnosis=["anxiety", "medication side effect", "parasites"],
            red_flags=["widespread", "blisters", "fever", "jaundice"],
            common_causes=["dry skin", "allergic reaction", "infection", "anxiety"],
            typical_duration="variable",
            aggravating_factors=["heat", "sweating", "certain fabrics", "stress"],
            relieving_factors=["cooling", "moisturizing", "antihistamines", "avoiding triggers"],
            associated_symptoms=["rash", "redness", "dry skin", "scratching"]
        )
        
        # genitourinary symptoms
        symptoms["dysuria"] = Symptom(
            name="Dysuria",
            category=SymptomCategory.GENITOURINARY,
            description="Pain or burning during urination",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["urinary tract infection", "bladder infection", "kidney stone", "STI"],
            differential_diagnosis=["irritation", "allergic reaction", "medication side effect"],
            red_flags=["fever", "flank pain", "blood in urine", "frequency"],
            common_causes=["urinary tract infection", "irritation", "allergic reaction"],
            typical_duration="days",
            aggravating_factors=["urination", "certain foods", "dehydration"],
            relieving_factors=["hydration", "antibiotics", "pain medications"],
            associated_symptoms=["frequency", "urgency", "blood in urine", "fever"]
        )
        
        symptoms["frequency"] = Symptom(
            name="Urinary Frequency",
            category=SymptomCategory.GENITOURINARY,
            description="Need to urinate more often than usual",
            severity=SymptomSeverity.MILD,
            associated_conditions=["urinary tract infection", "diabetes", "prostate enlargement"],
            differential_diagnosis=["increased fluid intake", "anxiety", "medication side effect"],
            red_flags=["pain", "blood in urine", "fever", "weight loss"],
            common_causes=["urinary tract infection", "diabetes", "increased fluid intake"],
            typical_duration="days to weeks",
            aggravating_factors=["caffeine", "alcohol", "diuretics", "anxiety"],
            relieving_factors=["treating underlying cause", "reducing fluid intake"],
            associated_symptoms=["urgency", "dysuria", "nocturia", "incontinence"]
        )
        
        # endocrine symptoms
        symptoms["fatigue"] = Symptom(
            name="Fatigue",
            category=SymptomCategory.GENERAL,
            description="Extreme tiredness or lack of energy",
            severity=SymptomSeverity.MILD,
            associated_conditions=["anemia", "hypothyroidism", "depression", "sleep apnea"],
            differential_diagnosis=["lack of sleep", "stress", "deconditioning", "medication side effect"],
            red_flags=["weight loss", "fever", "night sweats", "shortness of breath"],
            common_causes=["lack of sleep", "stress", "anemia", "depression"],
            typical_duration="days to weeks",
            aggravating_factors=["lack of sleep", "stress", "poor nutrition", "sedentary lifestyle"],
            relieving_factors=["adequate sleep", "exercise", "good nutrition", "stress management"],
            associated_symptoms=["weakness", "difficulty concentrating", "mood changes", "sleep problems"]
        )
        
        symptoms["weight_loss"] = Symptom(
            name="Weight Loss",
            category=SymptomCategory.GENERAL,
            description="Unintentional loss of body weight",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["cancer", "hyperthyroidism", "diabetes", "depression"],
            differential_diagnosis=["dietary changes", "increased activity", "medication side effect"],
            red_flags=["rapid loss", "fever", "night sweats", "pain"],
            common_causes=["dietary changes", "increased activity", "stress", "medications"],
            typical_duration="weeks to months",
            aggravating_factors=["poor appetite", "nausea", "diarrhea", "stress"],
            relieving_factors=["adequate nutrition", "treating underlying cause"],
            associated_symptoms=["fatigue", "weakness", "poor appetite", "night sweats"]
        )
        
        symptoms["fever"] = Symptom(
            name="Fever",
            category=SymptomCategory.GENERAL,
            description="Elevated body temperature above normal",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["infection", "inflammation", "cancer", "autoimmune disease"],
            differential_diagnosis=["heat exposure", "medication side effect", "exercise"],
            red_flags=["high fever", "altered mental status", "severe headache", "neck stiffness"],
            common_causes=["infection", "inflammation", "medications", "heat exposure"],
            typical_duration="days",
            aggravating_factors=["infection", "inflammation", "dehydration"],
            relieving_factors=["antipyretics", "cooling", "hydration", "treating cause"],
            associated_symptoms=["chills", "sweating", "headache", "body aches"]
        )
        
        symptoms["night_sweats"] = Symptom(
            name="Night Sweats",
            category=SymptomCategory.GENERAL,
            description="Excessive sweating during sleep",
            severity=SymptomSeverity.MODERATE,
            associated_conditions=["infection", "cancer", "hyperthyroidism", "menopause"],
            differential_diagnosis=["hot environment", "medication side effect", "anxiety"],
            red_flags=["weight loss", "fever", "pain", "lymphadenopathy"],
            common_causes=["infection", "medications", "anxiety", "hot environment"],
            typical_duration="days to weeks",
            aggravating_factors=["hot environment", "heavy bedding", "stress", "medications"],
            relieving_factors=["cool environment", "light bedding", "treating underlying cause"],
            associated_symptoms=["fever", "weight loss", "fatigue", "chills"]
        )
        
        return symptoms
    
    def get_symptom(self, name: str) -> Optional[Symptom]:
        """get a specific symptom by name"""
        return self.symptoms.get(name.lower().replace(" ", "_"))
    
    def get_symptoms_by_category(self, category: SymptomCategory) -> List[Symptom]:
        """get all symptoms in a category"""
        return [symptom for symptom in self.symptoms.values() if symptom.category == category]
    
    def get_symptoms_by_severity(self, severity: SymptomSeverity) -> List[Symptom]:
        """get all symptoms of a specific severity"""
        return [symptom for symptom in self.symptoms.values() if symptom.severity == severity]
    
    def search_symptoms(self, query: str) -> List[Symptom]:
        """search symptoms by name or description"""
        query = query.lower()
        results = []
        for symptom in self.symptoms.values():
            if (query in symptom.name.lower() or 
                query in symptom.description.lower() or
                any(query in condition.lower() for condition in symptom.associated_conditions)):
                results.append(symptom)
        return results
    
    def get_red_flag_symptoms(self) -> List[Symptom]:
        """get symptoms with red flags"""
        return [symptom for symptom in self.symptoms.values() if symptom.red_flags]
    
    def get_critical_symptoms(self) -> List[Symptom]:
        """get symptoms with critical severity"""
        return [symptom for symptom in self.symptoms.values() if symptom.severity == SymptomSeverity.CRITICAL]
    
    def get_all_symptoms(self) -> Dict[str, Symptom]:
        """get all symptoms"""
        return self.symptoms.copy() 