"""
enhanced treatment system with sophisticated drug interactions and clinical protocols
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import random
import math
import json


class DrugCategory(Enum):
    """enhanced drug categories"""
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    ANALGESIC = "analgesic"
    ANTIBIOTIC = "antibiotic"
    ANTICOAGULANT = "anticoagulant"
    ANTIEMETIC = "antiemetic"
    DIURETIC = "diuretic"
    INSULIN = "insulin"
    SEDATIVE = "sedative"
    VASOPRESSOR = "vasopressor"
    BRONCHODILATOR = "bronchodilator"
    ANTIARRHYTHMIC = "antiarrhythmic"


class Route(Enum):
    """drug administration routes"""
    ORAL = "oral"
    INTRAVENOUS = "iv"
    INTRAMUSCULAR = "im"
    SUBCUTANEOUS = "sc"
    INHALED = "inhaled"
    TOPICAL = "topical"
    RECTAL = "rectal"
    SUBLINGUAL = "sublingual"


class InteractionSeverity(Enum):
    """drug interaction severity levels"""
    NONE = "none"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CONTRAINDICATED = "contraindicated"


@dataclass
class DrugInteraction:
    """drug interaction definition"""
    drug1: str
    drug2: str
    severity: InteractionSeverity
    mechanism: str
    effect: str
    recommendation: str
    evidence_level: str = "moderate"  # low, moderate, high


@dataclass
class DrugLevel:
    """enhanced drug level monitoring"""
    drug_name: str
    current_level: float
    therapeutic_range: Tuple[float, float]
    unit: str
    timestamp: datetime
    is_therapeutic: bool = True
    is_toxic: bool = False
    requires_dose_adjustment: bool = False
    half_life: float = 0.0  # hours
    clearance_rate: float = 0.0  # L/hour


@dataclass
class Drug:
    """enhanced drug definition"""
    name: str
    category: DrugCategory
    routes: List[Route]
    dosing_info: Dict[str, Any]
    therapeutic_range: Optional[Tuple[float, float]] = None
    unit: str = ""
    half_life: float = 0.0  # hours
    protein_binding: float = 0.0  # percentage
    metabolism: str = ""
    excretion: str = ""
    contraindications: List[str] = field(default_factory=list)
    side_effects: List[str] = field(default_factory=list)
    monitoring_required: bool = False
    cost_per_unit: float = 0.0


@dataclass
class TreatmentProtocol:
    """enhanced treatment protocol"""
    name: str
    condition: str
    description: str
    steps: List[Dict[str, Any]]
    evidence_level: str = "moderate"
    success_rate: float = 0.8
    duration: int = 0  # hours
    cost: float = 0.0
    complications: List[str] = field(default_factory=list)


@dataclass
class TreatmentSession:
    """enhanced treatment session"""
    patient_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    treatments: List[Dict[str, Any]] = field(default_factory=list)
    protocols_used: List[str] = field(default_factory=list)
    outcomes: List[str] = field(default_factory=list)
    complications: List[str] = field(default_factory=list)
    success: bool = True


class EnhancedTreatmentEngine:
    """enhanced treatment engine with sophisticated drug management"""
    
    def __init__(self):
        self.drugs = self._initialize_drugs()
        self.interactions = self._initialize_interactions()
        self.protocols = self._initialize_protocols()
        self.active_treatments: Dict[str, List[Dict[str, Any]]] = {}
        self.drug_levels: Dict[str, List[DrugLevel]] = {}
        self.treatment_sessions: List[TreatmentSession] = []
    
    def _initialize_drugs(self) -> Dict[str, Drug]:
        """initialize comprehensive drug database"""
        drugs = {}
        
        # cardiovascular drugs
        drugs["nitroglycerin"] = Drug(
            name="Nitroglycerin",
            category=DrugCategory.CARDIOVASCULAR,
            routes=[Route.SUBLINGUAL, Route.INTRAVENOUS, Route.TOPICAL],
            dosing_info={
                "sublingual": {"dose": "0.4 mg", "frequency": "every 5 minutes", "max": "3 doses"},
                "iv": {"dose": "5-200 mcg/min", "titration": "every 3-5 minutes"},
                "topical": {"dose": "0.5-2 inches", "frequency": "every 8 hours"}
            },
            therapeutic_range=(0.1, 10.0),
            unit="mcg/mL",
            half_life=1.5,
            contraindications=["hypotension", "right ventricular infarction"],
            side_effects=["headache", "hypotension", "reflex tachycardia"],
            monitoring_required=True,
            cost_per_unit=2.0
        )
        
        drugs["aspirin"] = Drug(
            name="Aspirin",
            category=DrugCategory.CARDIOVASCULAR,
            routes=[Route.ORAL, Route.RECTAL],
            dosing_info={
                "oral": {"dose": "81-325 mg", "frequency": "daily"},
                "rectal": {"dose": "300-600 mg", "frequency": "every 4-6 hours"}
            },
            contraindications=["bleeding disorder", "peptic ulcer disease", "allergy"],
            side_effects=["gastrointestinal bleeding", "allergic reaction", "tinnitus"],
            cost_per_unit=0.1
        )
        
        drugs["metoprolol"] = Drug(
            name="Metoprolol",
            category=DrugCategory.CARDIOVASCULAR,
            routes=[Route.ORAL, Route.INTRAVENOUS],
            dosing_info={
                "oral": {"dose": "25-100 mg", "frequency": "twice daily"},
                "iv": {"dose": "5 mg", "frequency": "every 5 minutes", "max": "15 mg"}
            },
            therapeutic_range=(50, 200),
            unit="ng/mL",
            half_life=3.5,
            contraindications=["bradycardia", "heart block", "cardiogenic shock"],
            side_effects=["bradycardia", "hypotension", "fatigue"],
            monitoring_required=True,
            cost_per_unit=0.5
        )
        
        # respiratory drugs
        drugs["albuterol"] = Drug(
            name="Albuterol",
            category=DrugCategory.BRONCHODILATOR,
            routes=[Route.INHALED, Route.INTRAVENOUS],
            dosing_info={
                "inhaled": {"dose": "2 puffs", "frequency": "every 4-6 hours"},
                "iv": {"dose": "0.5-10 mcg/min", "titration": "every 10-15 minutes"}
            },
            contraindications=["hypersensitivity"],
            side_effects=["tremor", "tachycardia", "hypokalemia"],
            cost_per_unit=1.0
        )
        
        # analgesic drugs
        drugs["morphine"] = Drug(
            name="Morphine",
            category=DrugCategory.ANALGESIC,
            routes=[Route.INTRAVENOUS, Route.INTRAMUSCULAR, Route.ORAL],
            dosing_info={
                "iv": {"dose": "2-10 mg", "frequency": "every 2-4 hours"},
                "im": {"dose": "5-15 mg", "frequency": "every 4 hours"},
                "oral": {"dose": "15-30 mg", "frequency": "every 4 hours"}
            },
            therapeutic_range=(10, 80),
            unit="ng/mL",
            half_life=2.0,
            contraindications=["respiratory depression", "paralytic ileus"],
            side_effects=["respiratory depression", "sedation", "constipation"],
            monitoring_required=True,
            cost_per_unit=5.0
        )
        
        drugs["acetaminophen"] = Drug(
            name="Acetaminophen",
            category=DrugCategory.ANALGESIC,
            routes=[Route.ORAL, Route.RECTAL],
            dosing_info={
                "oral": {"dose": "500-1000 mg", "frequency": "every 4-6 hours", "max": "4000 mg/day"},
                "rectal": {"dose": "325-650 mg", "frequency": "every 4-6 hours"}
            },
            therapeutic_range=(10, 30),
            unit="mcg/mL",
            half_life=2.0,
            contraindications=["liver disease", "alcoholism"],
            side_effects=["hepatotoxicity", "allergic reaction"],
            cost_per_unit=0.2
        )
        
        # antibiotic drugs
        drugs["ceftriaxone"] = Drug(
            name="Ceftriaxone",
            category=DrugCategory.ANTIBIOTIC,
            routes=[Route.INTRAVENOUS, Route.INTRAMUSCULAR],
            dosing_info={
                "iv": {"dose": "1-2 g", "frequency": "every 12-24 hours"},
                "im": {"dose": "1-2 g", "frequency": "every 12-24 hours"}
            },
            contraindications=["penicillin allergy"],
            side_effects=["diarrhea", "allergic reaction", "phlebitis"],
            cost_per_unit=15.0
        )
        
        # anticoagulant drugs
        drugs["heparin"] = Drug(
            name="Heparin",
            category=DrugCategory.ANTICOAGULANT,
            routes=[Route.INTRAVENOUS, Route.SUBCUTANEOUS],
            dosing_info={
                "iv": {"dose": "80 units/kg bolus", "maintenance": "18 units/kg/hour"},
                "sc": {"dose": "5000-10000 units", "frequency": "every 8-12 hours"}
            },
            therapeutic_range=(0.3, 0.7),
            unit="units/mL",
            half_life=1.5,
            contraindications=["active bleeding", "heparin-induced thrombocytopenia"],
            side_effects=["bleeding", "thrombocytopenia", "osteoporosis"],
            monitoring_required=True,
            cost_per_unit=8.0
        )
        
        # insulin
        drugs["insulin_regular"] = Drug(
            name="Insulin Regular",
            category=DrugCategory.INSULIN,
            routes=[Route.SUBCUTANEOUS, Route.INTRAVENOUS],
            dosing_info={
                "sc": {"dose": "0.1-1.0 units/kg", "frequency": "before meals"},
                "iv": {"dose": "0.1 units/kg/hour", "titration": "based on glucose"}
            },
            therapeutic_range=(70, 140),
            unit="mg/dL (glucose)",
            half_life=1.0,
            contraindications=["hypoglycemia"],
            side_effects=["hypoglycemia", "weight gain"],
            monitoring_required=True,
            cost_per_unit=2.0
        )
        
        return drugs
    
    def _initialize_interactions(self) -> List[DrugInteraction]:
        """initialize drug interaction database"""
        interactions = []
        
        # aspirin interactions
        interactions.append(DrugInteraction(
            drug1="aspirin",
            drug2="heparin",
            severity=InteractionSeverity.MODERATE,
            mechanism="Increased bleeding risk",
            effect="Enhanced anticoagulation",
            recommendation="Monitor bleeding parameters closely"
        ))
        
        interactions.append(DrugInteraction(
            drug1="aspirin",
            drug2="metoprolol",
            severity=InteractionSeverity.MILD,
            mechanism="No direct interaction",
            effect="May be used together safely",
            recommendation="Monitor for additive cardiovascular effects"
        ))
        
        # nitroglycerin interactions
        interactions.append(DrugInteraction(
            drug1="nitroglycerin",
            drug2="sildenafil",
            severity=InteractionSeverity.CONTRAINDICATED,
            mechanism="Enhanced vasodilation",
            effect="Severe hypotension",
            recommendation="Contraindicated - avoid combination"
        ))
        
        # morphine interactions
        interactions.append(DrugInteraction(
            drug1="morphine",
            drug2="alcohol",
            severity=InteractionSeverity.SEVERE,
            mechanism="Enhanced CNS depression",
            effect="Increased sedation and respiratory depression",
            recommendation="Avoid alcohol while taking morphine"
        ))
        
        interactions.append(DrugInteraction(
            drug1="morphine",
            drug2="metoprolol",
            severity=InteractionSeverity.MILD,
            mechanism="No significant interaction",
            effect="May be used together",
            recommendation="Monitor for additive effects"
        ))
        
        return interactions
    
    def _initialize_protocols(self) -> Dict[str, TreatmentProtocol]:
        """initialize treatment protocols"""
        protocols = {}
        
        # chest pain protocol
        protocols["chest_pain"] = TreatmentProtocol(
            name="Chest Pain Protocol",
            condition="Acute chest pain",
            description="Standard protocol for evaluation and treatment of chest pain",
            steps=[
                {"action": "ECG", "time": 0, "description": "Immediate 12-lead ECG"},
                {"action": "Aspirin", "time": 5, "description": "325 mg aspirin PO"},
                {"action": "Nitroglycerin", "time": 10, "description": "0.4 mg SL, repeat x2 if needed"},
                {"action": "Morphine", "time": 15, "description": "2-4 mg IV if pain persists"},
                {"action": "Heparin", "time": 20, "description": "80 units/kg bolus + 18 units/kg/hour"}
            ],
            evidence_level="high",
            success_rate=0.85,
            duration=2,
            cost=500.0,
            complications=["bleeding", "allergic reaction", "hypotension"]
        )
        
        # asthma exacerbation protocol
        protocols["asthma_exacerbation"] = TreatmentProtocol(
            name="Asthma Exacerbation Protocol",
            condition="Acute asthma exacerbation",
            description="Standard protocol for treatment of asthma exacerbation",
            steps=[
                {"action": "Albuterol", "time": 0, "description": "2 puffs inhaled"},
                {"action": "Oxygen", "time": 5, "description": "2-4 L/min via nasal cannula"},
                {"action": "Prednisone", "time": 10, "description": "40-60 mg PO"},
                {"action": "Ipratropium", "time": 15, "description": "2 puffs inhaled"}
            ],
            evidence_level="high",
            success_rate=0.90,
            duration=4,
            cost=200.0,
            complications=["tremor", "tachycardia", "hyperglycemia"]
        )
        
        # sepsis protocol
        protocols["sepsis"] = TreatmentProtocol(
            name="Sepsis Protocol",
            condition="Severe sepsis/septic shock",
            description="Surviving Sepsis Campaign guidelines",
            steps=[
                {"action": "Ceftriaxone", "time": 0, "description": "2 g IV"},
                {"action": "Fluids", "time": 5, "description": "30 mL/kg crystalloid"},
                {"action": "Vasopressor", "time": 30, "description": "Norepinephrine if needed"},
                {"action": "Corticosteroids", "time": 60, "description": "Hydrocortisone if indicated"}
            ],
            evidence_level="high",
            success_rate=0.75,
            duration=6,
            cost=1000.0,
            complications=["allergic reaction", "adrenal insufficiency", "arrhythmia"]
        )
        
        return protocols
    
    def administer_drug(self, patient_id: str, drug_name: str, dose: float, 
                       route: str, timestamp: datetime = None) -> str:
        """administer a drug to a patient"""
        if drug_name not in self.drugs:
            return f"Error: Drug '{drug_name}' not found"
        
        drug = self.drugs[drug_name]
        route_enum = Route(route.lower())
        
        if route_enum not in drug.routes:
            return f"Error: Route '{route}' not available for {drug_name}"
        
        # check for drug interactions
        interactions = self._check_drug_interactions(patient_id, drug_name)
        if interactions:
            interaction_warnings = []
            for interaction in interactions:
                if interaction.severity in [InteractionSeverity.SEVERE, InteractionSeverity.CONTRAINDICATED]:
                    interaction_warnings.append(f"CRITICAL: {interaction.effect}")
                else:
                    interaction_warnings.append(f"Warning: {interaction.effect}")
        
        # record administration
        administration = {
            'drug_name': drug_name,
            'dose': dose,
            'route': route,
            'timestamp': timestamp or datetime.now(),
            'category': drug.category.value,
            'interactions': interactions if interactions else []
        }
        
        if patient_id not in self.active_treatments:
            self.active_treatments[patient_id] = []
        
        self.active_treatments[patient_id].append(administration)
        
        # initialize drug level monitoring if required
        if drug.monitoring_required:
            if patient_id not in self.drug_levels:
                self.drug_levels[patient_id] = []
            
            # simulate initial drug level
            initial_level = random.uniform(drug.therapeutic_range[0], drug.therapeutic_range[1]) if drug.therapeutic_range else 0.0
            
            drug_level = DrugLevel(
                drug_name=drug_name,
                current_level=initial_level,
                therapeutic_range=drug.therapeutic_range or (0.0, 0.0),
                unit=drug.unit,
                timestamp=timestamp or datetime.now(),
                half_life=drug.half_life,
                clearance_rate=random.uniform(0.5, 2.0)
            )
            
            self.drug_levels[patient_id].append(drug_level)
        
        result = f"✓ Administered {dose} {drug_name} via {route}"
        if interactions:
            result += f"\n⚠️ Drug interactions detected: {', '.join(interaction_warnings)}"
        
        return result
    
    def _check_drug_interactions(self, patient_id: str, new_drug: str) -> List[DrugInteraction]:
        """check for drug interactions with currently active drugs"""
        interactions = []
        
        if patient_id in self.active_treatments:
            active_drugs = [treatment['drug_name'] for treatment in self.active_treatments[patient_id]]
            
            for interaction in self.interactions:
                if ((interaction.drug1 == new_drug and interaction.drug2 in active_drugs) or
                    (interaction.drug2 == new_drug and interaction.drug1 in active_drugs)):
                    interactions.append(interaction)
        
        return interactions
    
    def get_active_treatments(self, patient_id: str) -> List[Dict[str, Any]]:
        """get active treatments for a patient"""
        return self.active_treatments.get(patient_id, [])
    
    def get_drug_levels(self, patient_id: str) -> List[DrugLevel]:
        """get drug levels for a patient"""
        return self.drug_levels.get(patient_id, [])
    
    def update_drug_levels(self, patient_id: str, current_time: datetime = None) -> List[str]:
        """update drug levels based on pharmacokinetics"""
        if current_time is None:
            current_time = datetime.now()
        
        updates = []
        
        if patient_id in self.drug_levels:
            for drug_level in self.drug_levels[patient_id]:
                # calculate time elapsed
                time_elapsed = (current_time - drug_level.timestamp).total_seconds() / 3600  # hours
                
                # calculate new level based on half-life
                if drug_level.half_life > 0:
                    decay_factor = math.exp(-time_elapsed * math.log(2) / drug_level.half_life)
                    new_level = drug_level.current_level * decay_factor
                    
                    if new_level != drug_level.current_level:
                        old_level = drug_level.current_level
                        drug_level.current_level = new_level
                        drug_level.timestamp = current_time
                        
                        # update therapeutic status
                        if drug_level.therapeutic_range:
                            drug_level.is_therapeutic = (drug_level.therapeutic_range[0] <= new_level <= drug_level.therapeutic_range[1])
                            drug_level.is_toxic = new_level > drug_level.therapeutic_range[1]
                        
                        updates.append(f"Drug level {drug_level.drug_name}: {old_level:.2f} → {new_level:.2f}")
        
        return updates
    
    def start_treatment_protocol(self, patient_id: str, protocol_name: str) -> str:
        """start a treatment protocol for a patient"""
        if protocol_name not in self.protocols:
            return f"Error: Protocol '{protocol_name}' not found"
        
        protocol = self.protocols[protocol_name]
        
        session = TreatmentSession(
            patient_id=patient_id,
            start_time=datetime.now(),
            protocols_used=[protocol_name]
        )
        
        self.treatment_sessions.append(session)
        
        return f"✓ Started {protocol_name} protocol for patient {patient_id}"
    
    def get_available_drugs(self) -> Dict[str, Drug]:
        """get all available drugs"""
        return self.drugs.copy()
    
    def get_available_protocols(self) -> Dict[str, TreatmentProtocol]:
        """get all available protocols"""
        return self.protocols.copy()
    
    def search_drugs(self, query: str) -> Dict[str, Drug]:
        """search drugs by name or category"""
        query = query.lower()
        results = {}
        for name, drug in self.drugs.items():
            if (query in name.lower() or 
                query in drug.category.value.lower()):
                results[name] = drug
        return results
    
    def get_drug_interactions(self, drug_name: str) -> List[DrugInteraction]:
        """get all interactions for a specific drug"""
        interactions = []
        for interaction in self.interactions:
            if interaction.drug1 == drug_name or interaction.drug2 == drug_name:
                interactions.append(interaction)
        return interactions
    
    def get_critical_alerts(self) -> List[Dict[str, Any]]:
        """get critical drug alerts"""
        alerts = []
        
        for patient_id, drug_levels in self.drug_levels.items():
            for drug_level in drug_levels:
                if drug_level.is_toxic or not drug_level.is_therapeutic:
                    alerts.append({
                        'patient_id': patient_id,
                        'drug_name': drug_level.drug_name,
                        'level': drug_level.current_level,
                        'unit': drug_level.unit,
                        'therapeutic_range': drug_level.therapeutic_range,
                        'status': 'toxic' if drug_level.is_toxic else 'subtherapeutic',
                        'timestamp': drug_level.timestamp
                    })
        
        return alerts 