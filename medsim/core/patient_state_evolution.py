"""
comprehensive patient state evolution engine for real-time simulation
models vitals, symptoms, organ function, and integrates disease and intervention effects
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import random
import math

from .disease_progression import DiseaseProgressionEngine, DiseaseState

class OrganSystem(Enum):
    """comprehensive organ systems"""
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
    """comprehensive adverse event types"""
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
    HYPOGLYCEMIA = "hypoglycemia"
    HYPERGLYCEMIA = "hyperglycemia"
    ELECTROLYTE_IMBALANCE = "electrolyte_imbalance"
    ACID_BASE_DISTURBANCE = "acid_base_disturbance"
    DELIRIUM = "delirium"
    PRESSURE_ULCER = "pressure_ulcer"
    DEEP_VEIN_THROMBOSIS = "deep_vein_thrombosis"
    PULMONARY_EMBOLISM = "pulmonary_embolism"
    ASPIRATION = "aspiration"
    MALNUTRITION = "malnutrition"

@dataclass
class OrganSystemState:
    """comprehensive state of a specific organ system"""
    name: str
    function_score: float  # 0.0 (failure) to 1.0 (normal)
    dysfunctions: List[str] = field(default_factory=list)
    specific_metrics: Dict[str, float] = field(default_factory=dict)
    interventions: List[str] = field(default_factory=list)
    adverse_events: List[str] = field(default_factory=list)

@dataclass
class VitalSigns:
    """comprehensive vital signs"""
    heart_rate: float
    bp_systolic: float
    bp_diastolic: float
    mean_arterial_pressure: float
    respiratory_rate: float
    oxygen_saturation: float
    temperature: float
    pain_score: float = 0.0
    consciousness_level: str = "alert"
    capillary_refill: float = 2.0
    urine_output: float = 50.0  # ml/hr

@dataclass
class PatientState:
    """comprehensive patient state at a time point"""
    vitals: VitalSigns
    symptoms: List[str]
    organ_systems: Dict[str, OrganSystemState]
    disease_states: List[DiseaseState]
    interventions: List[Dict[str, Any]] = field(default_factory=list)
    adverse_events: List[AdverseEventType] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    consciousness: str = "alert"
    mobility: str = "independent"
    nutrition_status: str = "adequate"
    skin_integrity: str = "intact"

class PatientStateEvolutionEngine:
    """comprehensive engine for real-time patient state evolution"""
    
    def __init__(self):
        self.disease_engine = DiseaseProgressionEngine()
        self.organ_systems = [system.value for system in OrganSystem]
        
    def initialize_patient_state(self, disease_states: List[DiseaseState],
                                base_vitals: Optional[Dict[str, float]] = None) -> PatientState:
        """initialize comprehensive patient state from disease states and base vitals"""
        if base_vitals is None:
            base_vitals = {
                "heart_rate": 80,
                "bp_systolic": 120,
                "bp_diastolic": 80,
                "mean_arterial_pressure": 93,
                "respiratory_rate": 16,
                "oxygen_saturation": 98,
                "temperature": 98.6,
                "pain_score": 0.0,
                "consciousness_level": "alert",
                "capillary_refill": 2.0,
                "urine_output": 50.0
            }
        
        vitals = VitalSigns(**base_vitals)
        organ_states = self._initialize_organ_systems()
        symptoms = []
        
        for ds in disease_states:
            symptoms.extend(self._get_symptoms_for_stage(ds))
        
        return PatientState(
            vitals=vitals,
            symptoms=list(set(symptoms)),
            organ_systems=organ_states,
            disease_states=disease_states.copy(),
            interventions=[],
            adverse_events=[],
            timestamp=datetime.now()
        )
    
    def _initialize_organ_systems(self) -> Dict[str, OrganSystemState]:
        """initialize all organ systems with baseline function"""
        systems = {}
        for system_name in self.organ_systems:
            specific_metrics = self._get_baseline_metrics(system_name)
            systems[system_name] = OrganSystemState(
                name=system_name,
                function_score=1.0,
                dysfunctions=[],
                specific_metrics=specific_metrics,
                interventions=[],
                adverse_events=[]
            )
        return systems
    
    def _get_baseline_metrics(self, system_name: str) -> Dict[str, float]:
        """get baseline metrics for each organ system"""
        baseline_metrics = {
            "cardiovascular": {
                "cardiac_output": 5.0,
                "stroke_volume": 70.0,
                "ejection_fraction": 65.0,
                "central_venous_pressure": 8.0
            },
            "respiratory": {
                "tidal_volume": 500.0,
                "vital_capacity": 4000.0,
                "fev1": 3500.0,
                "pao2": 95.0,
                "paco2": 40.0
            },
            "renal": {
                "glomerular_filtration_rate": 100.0,
                "creatinine_clearance": 100.0,
                "urine_specific_gravity": 1.020,
                "sodium_excretion": 150.0
            },
            "hepatic": {
                "bilirubin_total": 1.0,
                "bilirubin_direct": 0.3,
                "alt": 25.0,
                "ast": 25.0,
                "albumin": 4.0
            },
            "neurological": {
                "glasgow_coma_scale": 15.0,
                "pupil_size": 3.0,
                "motor_response": 6.0,
                "verbal_response": 5.0
            },
            "hematological": {
                "hemoglobin": 14.0,
                "white_blood_cells": 7000.0,
                "platelets": 250000.0,
                "prothrombin_time": 12.0
            },
            "immune": {
                "cd4_count": 800.0,
                "immunoglobulin_g": 1000.0,
                "complement_c3": 120.0,
                "esr": 15.0
            },
            "endocrine": {
                "glucose": 100.0,
                "insulin": 10.0,
                "cortisol": 15.0,
                "tsh": 2.5
            },
            "gastrointestinal": {
                "gastric_ph": 2.0,
                "bowel_sounds": 1.0,
                "liver_size": 15.0,
                "spleen_size": 12.0
            },
            "musculoskeletal": {
                "muscle_strength": 5.0,
                "range_of_motion": 1.0,
                "bone_density": 1.0,
                "joint_stability": 1.0
            },
            "integumentary": {
                "skin_turgor": 1.0,
                "capillary_refill": 2.0,
                "skin_temperature": 98.6,
                "wound_healing": 1.0
            }
        }
        return baseline_metrics.get(system_name, {})
    
    def evolve_state(self, state: PatientState, time_step: timedelta,
                     interventions: Optional[List[Dict[str, Any]]] = None) -> PatientState:
        """evolve comprehensive patient state over a time step"""
        # progress diseases
        new_disease_states = []
        for ds in state.disease_states:
            progressed = self.disease_engine.progress_disease(
                ds.disease_name, ds.disease_name, time_step
            )
            new_disease_states.append(progressed or ds)
        
        # update organ systems with comprehensive effects
        organ_states = self._update_organ_systems_comprehensive(state.organ_systems, new_disease_states, interventions)
        
        # update vitals with detailed calculations
        vitals = self._update_vitals_comprehensive(state.vitals, new_disease_states, organ_states, interventions)
        
        # update symptoms with organ-specific manifestations
        symptoms = self._update_symptoms_comprehensive(new_disease_states, organ_states)
        
        # apply interventions and track their effects
        interventions = interventions or []
        
        # comprehensive adverse event checking
        adverse_events = self._check_adverse_events_comprehensive(new_disease_states, interventions, organ_states, vitals)
        
        # update consciousness and mobility
        consciousness = self._update_consciousness(state.consciousness, organ_states, vitals)
        mobility = self._update_mobility(state.mobility, organ_states, vitals)
        nutrition_status = self._update_nutrition_status(state.nutrition_status, organ_states, interventions)
        skin_integrity = self._update_skin_integrity(state.skin_integrity, organ_states, vitals)
        
        return PatientState(
            vitals=vitals,
            symptoms=symptoms,
            organ_systems=organ_states,
            disease_states=new_disease_states,
            interventions=interventions,
            adverse_events=adverse_events,
            timestamp=state.timestamp + time_step,
            consciousness=consciousness,
            mobility=mobility,
            nutrition_status=nutrition_status,
            skin_integrity=skin_integrity
        )
    
    def _update_organ_systems_comprehensive(self, organ_states: Dict[str, OrganSystemState], 
                                          disease_states: List[DiseaseState],
                                          interventions: Optional[List[Dict[str, Any]]]) -> Dict[str, OrganSystemState]:
        """comprehensive organ system updates with detailed metrics"""
        new_states = {}
        
        for system_name, current_state in organ_states.items():
            new_state = OrganSystemState(
                name=current_state.name,
                function_score=current_state.function_score,
                dysfunctions=current_state.dysfunctions.copy(),
                specific_metrics=current_state.specific_metrics.copy(),
                interventions=current_state.interventions.copy(),
                adverse_events=current_state.adverse_events.copy()
            )
            
            # apply disease effects
            new_state = self._apply_disease_effects(new_state, disease_states)
            
            # apply intervention effects
            if interventions:
                new_state = self._apply_intervention_effects(new_state, interventions)
            
            # apply organ system interactions
            new_state = self._apply_organ_interactions(new_state, organ_states)
            
            # clamp function scores
            new_state.function_score = max(0.0, min(1.0, new_state.function_score))
            
            new_states[system_name] = new_state
        
        return new_states
    
    def _apply_disease_effects(self, organ_state: OrganSystemState, disease_states: List[DiseaseState]) -> OrganSystemState:
        """apply disease-specific effects to organ systems"""
        for ds in disease_states:
            severity = ds.severity_score
            
            if organ_state.name == "cardiovascular":
                if ds.disease_name in ["sepsis", "acute_coronary_syndrome", "heart_failure"]:
                    organ_state.function_score -= severity * 0.1
                    organ_state.specific_metrics["cardiac_output"] -= severity * 0.5
                    organ_state.specific_metrics["ejection_fraction"] -= severity * 5.0
                    if severity > 0.7:
                        organ_state.dysfunctions.append("cardiogenic_shock")
                
            elif organ_state.name == "respiratory":
                if ds.disease_name in ["pneumonia", "sepsis", "acute_respiratory_distress_syndrome"]:
                    organ_state.function_score -= severity * 0.12
                    organ_state.specific_metrics["pao2"] -= severity * 15.0
                    organ_state.specific_metrics["tidal_volume"] -= severity * 100.0
                    if severity > 0.6:
                        organ_state.dysfunctions.append("respiratory_failure")
                
            elif organ_state.name == "renal":
                if ds.disease_name in ["sepsis", "acute_kidney_injury", "heart_failure"]:
                    organ_state.function_score -= severity * 0.08
                    organ_state.specific_metrics["glomerular_filtration_rate"] -= severity * 20.0
                    if severity > 0.8:
                        organ_state.dysfunctions.append("acute_kidney_injury")
                
            elif organ_state.name == "hepatic":
                if ds.disease_name in ["sepsis", "liver_failure", "hepatitis"]:
                    organ_state.function_score -= severity * 0.06
                    organ_state.specific_metrics["albumin"] -= severity * 0.5
                    if severity > 0.7:
                        organ_state.dysfunctions.append("hepatic_failure")
                
            elif organ_state.name == "neurological":
                if ds.disease_name in ["stroke", "sepsis", "encephalopathy"]:
                    organ_state.function_score -= severity * 0.15
                    organ_state.specific_metrics["glasgow_coma_scale"] -= severity * 3.0
                    if severity > 0.6:
                        organ_state.dysfunctions.append("altered_mental_status")
                
            elif organ_state.name == "hematological":
                if ds.disease_name in ["sepsis", "disseminated_intravascular_coagulation"]:
                    organ_state.function_score -= severity * 0.10
                    organ_state.specific_metrics["platelets"] -= severity * 50000.0
                    if severity > 0.7:
                        organ_state.dysfunctions.append("coagulopathy")
                
            elif organ_state.name == "immune":
                if ds.disease_name in ["sepsis", "immunodeficiency"]:
                    organ_state.function_score -= severity * 0.20
                    organ_state.specific_metrics["cd4_count"] -= severity * 200.0
                    if severity > 0.5:
                        organ_state.dysfunctions.append("immunosuppression")
                
            elif organ_state.name == "endocrine":
                if ds.disease_name in ["diabetes", "adrenal_insufficiency"]:
                    organ_state.function_score -= severity * 0.05
                    organ_state.specific_metrics["glucose"] += severity * 50.0
                    if severity > 0.6:
                        organ_state.dysfunctions.append("metabolic_dysfunction")
                
            elif organ_state.name == "gastrointestinal":
                if ds.disease_name in ["sepsis", "bowel_obstruction", "pancreatitis"]:
                    organ_state.function_score -= severity * 0.07
                    organ_state.specific_metrics["gastric_ph"] += severity * 1.0
                    if severity > 0.6:
                        organ_state.dysfunctions.append("ileus")
                
            elif organ_state.name == "musculoskeletal":
                if ds.disease_name in ["sepsis", "immobility"]:
                    organ_state.function_score -= severity * 0.03
                    organ_state.specific_metrics["muscle_strength"] -= severity * 1.0
                    if severity > 0.5:
                        organ_state.dysfunctions.append("muscle_atrophy")
                
            elif organ_state.name == "integumentary":
                if ds.disease_name in ["sepsis", "immobility"]:
                    organ_state.function_score -= severity * 0.04
                    organ_state.specific_metrics["skin_turgor"] -= severity * 0.2
                    if severity > 0.6:
                        organ_state.dysfunctions.append("pressure_ulcer_risk")
        
        return organ_state
    
    def _apply_intervention_effects(self, organ_state: OrganSystemState, interventions: List[Dict[str, Any]]) -> OrganSystemState:
        """apply intervention effects to organ systems"""
        for intervention in interventions:
            intervention_name = intervention.get("name", "")
            intervention_type = intervention.get("type", "")
            
            if intervention_type == "medication":
                if intervention_name == "vasopressor":
                    if organ_state.name == "cardiovascular":
                        organ_state.function_score += 0.1
                        organ_state.specific_metrics["cardiac_output"] += 0.5
                        organ_state.specific_metrics["mean_arterial_pressure"] += 10.0
                
                elif intervention_name == "antibiotic":
                    if organ_state.name == "immune":
                        organ_state.function_score += 0.05
                        organ_state.specific_metrics["white_blood_cells"] += 1000.0
                
                elif intervention_name == "diuretic":
                    if organ_state.name == "renal":
                        organ_state.specific_metrics["urine_output"] += 20.0
                    if organ_state.name == "cardiovascular":
                        organ_state.specific_metrics["central_venous_pressure"] -= 2.0
                
                elif intervention_name == "insulin":
                    if organ_state.name == "endocrine":
                        organ_state.specific_metrics["glucose"] -= 30.0
                
                elif intervention_name == "sedative":
                    if organ_state.name == "neurological":
                        organ_state.specific_metrics["glasgow_coma_scale"] -= 2.0
                    if organ_state.name == "respiratory":
                        organ_state.function_score -= 0.05
                        organ_state.specific_metrics["respiratory_rate"] -= 2.0
            
            elif intervention_type == "procedure":
                if "intubation" in intervention_name:
                    if organ_state.name == "respiratory":
                        organ_state.function_score += 0.15
                        organ_state.specific_metrics["pao2"] += 10.0
                
                elif "dialysis" in intervention_name:
                    if organ_state.name == "renal":
                        organ_state.function_score += 0.2
                        organ_state.specific_metrics["glomerular_filtration_rate"] += 10.0
            
            elif intervention_type == "supportive":
                if "oxygen" in intervention_name:
                    if organ_state.name == "respiratory":
                        organ_state.specific_metrics["pao2"] += 5.0
                
                elif "mechanical_ventilation" in intervention_name:
                    if organ_state.name == "respiratory":
                        organ_state.function_score += 0.25
                        organ_state.specific_metrics["tidal_volume"] += 200.0
        
        return organ_state
    
    def _apply_organ_interactions(self, organ_state: OrganSystemState, all_organs: Dict[str, OrganSystemState]) -> OrganSystemState:
        """apply interactions between organ systems"""
        # cardiovascular affects all other systems
        if organ_state.name != "cardiovascular" and all_organs["cardiovascular"].function_score < 0.6:
            organ_state.function_score -= 0.05
        
        # respiratory affects cardiovascular
        if organ_state.name == "cardiovascular" and all_organs["respiratory"].function_score < 0.5:
            organ_state.function_score -= 0.08
            organ_state.specific_metrics["cardiac_output"] -= 1.0
        
        # renal affects cardiovascular
        if organ_state.name == "cardiovascular" and all_organs["renal"].function_score < 0.4:
            organ_state.specific_metrics["mean_arterial_pressure"] += 15.0
        
        # hepatic affects coagulation
        if organ_state.name == "hematological" and all_organs["hepatic"].function_score < 0.5:
            organ_state.specific_metrics["prothrombin_time"] += 3.0
        
        return organ_state
    
    def _update_vitals_comprehensive(self, vitals: VitalSigns, disease_states: List[DiseaseState],
                                   organ_states: Dict[str, OrganSystemState],
                                   interventions: Optional[List[Dict[str, Any]]]) -> VitalSigns:
        """comprehensive vital signs update with detailed calculations"""
        new_vitals = VitalSigns(
            heart_rate=vitals.heart_rate,
            bp_systolic=vitals.bp_systolic,
            bp_diastolic=vitals.bp_diastolic,
            mean_arterial_pressure=vitals.mean_arterial_pressure,
            respiratory_rate=vitals.respiratory_rate,
            oxygen_saturation=vitals.oxygen_saturation,
            temperature=vitals.temperature,
            pain_score=vitals.pain_score,
            consciousness_level=vitals.consciousness_level,
            capillary_refill=vitals.capillary_refill,
            urine_output=vitals.urine_output
        )
        
        # cardiovascular effects
        cv_system = organ_states["cardiovascular"]
        if cv_system.function_score < 0.7:
            new_vitals.heart_rate += (1.0 - cv_system.function_score) * 20
            new_vitals.bp_systolic -= (1.0 - cv_system.function_score) * 20
            new_vitals.mean_arterial_pressure = (new_vitals.bp_systolic + 2 * new_vitals.bp_diastolic) / 3
        
        # respiratory effects
        resp_system = organ_states["respiratory"]
        if resp_system.function_score < 0.7:
            new_vitals.oxygen_saturation -= (1.0 - resp_system.function_score) * 15
            new_vitals.respiratory_rate += (1.0 - resp_system.function_score) * 8
        
        # renal effects
        renal_system = organ_states["renal"]
        if renal_system.function_score < 0.6:
            new_vitals.urine_output -= (1.0 - renal_system.function_score) * 30
        
        # neurological effects
        neuro_system = organ_states["neurological"]
        if neuro_system.function_score < 0.5:
            new_vitals.consciousness_level = "confused"
        if neuro_system.function_score < 0.3:
            new_vitals.consciousness_level = "unresponsive"
        
        # temperature effects from disease
        for ds in disease_states:
            if ds.disease_name in ["sepsis", "infection"]:
                new_vitals.temperature += ds.severity_score * 3.0
        
        # intervention effects
        if interventions:
            for intervention in interventions:
                if intervention.get("type") == "medication":
                    if intervention.get("name") == "vasopressor":
                        new_vitals.bp_systolic += 15
                        new_vitals.mean_arterial_pressure += 10
                    elif intervention.get("name") == "sedative":
                        new_vitals.respiratory_rate -= 3
                        new_vitals.consciousness_level = "sedated"
                    elif intervention.get("name") == "antibiotic":
                        new_vitals.temperature -= 0.5
        
        # clamp vitals to realistic ranges
        new_vitals.heart_rate = max(30, min(180, new_vitals.heart_rate))
        new_vitals.bp_systolic = max(60, min(200, new_vitals.bp_systolic))
        new_vitals.bp_diastolic = max(30, min(120, new_vitals.bp_diastolic))
        new_vitals.mean_arterial_pressure = max(40, min(150, new_vitals.mean_arterial_pressure))
        new_vitals.respiratory_rate = max(6, min(40, new_vitals.respiratory_rate))
        new_vitals.oxygen_saturation = max(70, min(100, new_vitals.oxygen_saturation))
        new_vitals.temperature = max(93, min(107, new_vitals.temperature))
        new_vitals.pain_score = max(0, min(10, new_vitals.pain_score))
        new_vitals.urine_output = max(0, min(200, new_vitals.urine_output))
        
        return new_vitals
    
    def _update_symptoms_comprehensive(self, disease_states: List[DiseaseState], 
                                     organ_states: Dict[str, OrganSystemState]) -> List[str]:
        """comprehensive symptom updates with organ-specific manifestations"""
        symptoms = []
        
        # disease-specific symptoms
        for ds in disease_states:
            symptoms.extend(self._get_symptoms_for_stage(ds))
        
        # organ dysfunction symptoms
        for system_name, organ in organ_states.items():
            if organ.function_score < 0.5:
                symptoms.extend(self._get_organ_dysfunction_symptoms(system_name, organ))
        
        return list(set(symptoms))
    
    def _get_organ_dysfunction_symptoms(self, system_name: str, organ_state: OrganSystemState) -> List[str]:
        """get symptoms specific to organ dysfunction"""
        symptoms_map = {
            "cardiovascular": ["chest_pain", "dyspnea", "fatigue", "edema", "palpitations"],
            "respiratory": ["dyspnea", "cough", "wheezing", "cyanosis", "respiratory_distress"],
            "renal": ["oliguria", "edema", "hypertension", "fatigue", "nausea"],
            "hepatic": ["jaundice", "ascites", "confusion", "bleeding", "fatigue"],
            "neurological": ["confusion", "seizures", "weakness", "numbness", "headache"],
            "hematological": ["bleeding", "bruising", "fatigue", "pallor", "fever"],
            "immune": ["fever", "fatigue", "recurrent_infections", "weight_loss"],
            "endocrine": ["polyuria", "polydipsia", "weight_loss", "fatigue", "confusion"],
            "gastrointestinal": ["nausea", "vomiting", "abdominal_pain", "diarrhea", "constipation"],
            "musculoskeletal": ["weakness", "pain", "stiffness", "decreased_mobility"],
            "integumentary": ["rash", "ulcers", "edema", "pruritus", "discoloration"]
        }
        
        base_symptoms = symptoms_map.get(system_name, [])
        if organ_state.function_score < 0.3:
            base_symptoms.append(f"{system_name}_failure")
        
        return base_symptoms
    
    def _check_adverse_events_comprehensive(self, disease_states: List[DiseaseState],
                                          interventions: List[Dict[str, Any]],
                                          organ_states: Dict[str, OrganSystemState],
                                          vitals: VitalSigns) -> List[AdverseEventType]:
        """comprehensive adverse event checking"""
        events = []
        
        # intervention-related adverse events
        for intervention in interventions:
            intervention_name = intervention.get("name", "")
            intervention_type = intervention.get("type", "")
            
            if intervention_type == "medication":
                if intervention_name == "antibiotic" and random.random() < 0.05:
                    events.append(AdverseEventType.ALLERGIC_REACTION)
                if intervention_name == "vasopressor" and organ_states["cardiovascular"].function_score < 0.5 and random.random() < 0.1:
                    events.append(AdverseEventType.ARRHYTHMIA)
                if intervention_name == "anticoagulant" and random.random() < 0.08:
                    events.append(AdverseEventType.BLEEDING)
                if intervention_name == "sedative" and organ_states["respiratory"].function_score < 0.6 and random.random() < 0.15:
                    events.append(AdverseEventType.RESPIRATORY_DEPRESSION)
                if intervention_name == "insulin" and random.random() < 0.03:
                    events.append(AdverseEventType.HYPOGLYCEMIA)
            
            elif intervention_type == "procedure":
                if "intubation" in intervention_name and random.random() < 0.08:
                    events.append(AdverseEventType.INFECTION)
                if "catheterization" in intervention_name and random.random() < 0.12:
                    events.append(AdverseEventType.INFECTION)
                if "dialysis" in intervention_name and random.random() < 0.05:
                    events.append(AdverseEventType.HYPOTENSION)
        
        # disease-related adverse events
        for ds in disease_states:
            if ds.severity_score > 0.95 and random.random() < 0.2:
                events.append(AdverseEventType.CARDIAC_ARREST)
            if ds.severity_score > 0.9 and ds.disease_name == "sepsis" and random.random() < 0.15:
                events.append(AdverseEventType.SEPSIS)
            if ds.severity_score > 0.8 and ds.disease_name == "stroke" and random.random() < 0.1:
                events.append(AdverseEventType.STROKE)
        
        # vital sign-based adverse events
        if vitals.heart_rate > 150 or vitals.heart_rate < 40:
            events.append(AdverseEventType.ARRHYTHMIA)
        if vitals.bp_systolic < 80:
            events.append(AdverseEventType.HYPOTENSION)
        if vitals.oxygen_saturation < 85:
            events.append(AdverseEventType.RESPIRATORY_DEPRESSION)
        if vitals.temperature > 104:
            events.append(AdverseEventType.SEPSIS)
        
        # organ failure adverse events
        for system_name, organ in organ_states.items():
            if organ.function_score < 0.2:
                events.append(AdverseEventType.ORGAN_FAILURE)
        
        return list(set(events))
    
    def _update_consciousness(self, current_consciousness: str, organ_states: Dict[str, OrganSystemState], vitals: VitalSigns) -> str:
        """update consciousness level based on organ function and vitals"""
        neuro_system = organ_states["neurological"]
        
        if neuro_system.function_score < 0.3:
            return "coma"
        elif neuro_system.function_score < 0.5:
            return "stupor"
        elif neuro_system.function_score < 0.7:
            return "confused"
        elif vitals.consciousness_level == "sedated":
            return "sedated"
        else:
            return "alert"
    
    def _update_mobility(self, current_mobility: str, organ_states: Dict[str, OrganSystemState], vitals: VitalSigns) -> str:
        """update mobility status"""
        if vitals.consciousness_level in ["coma", "stupor"]:
            return "bedbound"
        elif organ_states["musculoskeletal"].function_score < 0.4:
            return "assisted"
        elif vitals.heart_rate > 120 or vitals.bp_systolic < 90:
            return "limited"
        else:
            return "independent"
    
    def _update_nutrition_status(self, current_nutrition: str, organ_states: Dict[str, OrganSystemState], interventions: List[Dict[str, Any]]) -> str:
        """update nutrition status"""
        if organ_states["gastrointestinal"].function_score < 0.3:
            return "impaired"
        elif any("nutrition" in intervention.get("name", "") for intervention in interventions):
            return "supplemented"
        else:
            return "adequate"
    
    def _update_skin_integrity(self, current_integrity: str, organ_states: Dict[str, OrganSystemState], vitals: VitalSigns) -> str:
        """update skin integrity status"""
        if organ_states["integumentary"].function_score < 0.4:
            return "compromised"
        elif vitals.consciousness_level in ["coma", "stupor"] or organ_states["musculoskeletal"].function_score < 0.3:
            return "at_risk"
        else:
            return "intact"
    
    def get_organ_system_summary(self, organ_states: Dict[str, OrganSystemState]) -> Dict[str, Any]:
        """get comprehensive summary of organ system status"""
        summary = {}
        for system_name, organ in organ_states.items():
            summary[system_name] = {
                "function_score": organ.function_score,
                "dysfunctions": organ.dysfunctions,
                "key_metrics": {k: v for k, v in organ.specific_metrics.items() if k in self._get_key_metrics(system_name)},
                "interventions": organ.interventions,
                "adverse_events": organ.adverse_events
            }
        return summary
    
    def _get_key_metrics(self, system_name: str) -> List[str]:
        """get key metrics for each organ system"""
        key_metrics = {
            "cardiovascular": ["cardiac_output", "ejection_fraction", "mean_arterial_pressure"],
            "respiratory": ["pao2", "paco2", "tidal_volume"],
            "renal": ["glomerular_filtration_rate", "urine_output"],
            "hepatic": ["bilirubin_total", "albumin", "alt"],
            "neurological": ["glasgow_coma_scale"],
            "hematological": ["hemoglobin", "platelets", "white_blood_cells"],
            "immune": ["cd4_count"],
            "endocrine": ["glucose", "insulin"],
            "gastrointestinal": ["gastric_ph"],
            "musculoskeletal": ["muscle_strength"],
            "integumentary": ["skin_turgor", "capillary_refill"]
        }
        return key_metrics.get(system_name, [])
    
    def get_patient_summary(self, state: PatientState) -> Dict[str, Any]:
        """get comprehensive patient summary"""
        return {
            "vitals": {
                "heart_rate": state.vitals.heart_rate,
                "bp_systolic": state.vitals.bp_systolic,
                "bp_diastolic": state.vitals.bp_diastolic,
                "mean_arterial_pressure": state.vitals.mean_arterial_pressure,
                "respiratory_rate": state.vitals.respiratory_rate,
                "oxygen_saturation": state.vitals.oxygen_saturation,
                "temperature": state.vitals.temperature,
                "consciousness_level": state.vitals.consciousness_level
            },
            "organ_systems": self.get_organ_system_summary(state.organ_systems),
            "symptoms": state.symptoms,
            "adverse_events": [event.value for event in state.adverse_events],
            "consciousness": state.consciousness,
            "mobility": state.mobility,
            "nutrition_status": state.nutrition_status,
            "skin_integrity": state.skin_integrity,
            "timestamp": state.timestamp.isoformat()
        }

    def _get_symptoms_for_stage(self, ds: DiseaseState) -> List[str]:
        # get symptoms for current stage
        disease_def = self.disease_engine.disease_definitions.get(ds.disease_name, {})
        stage = ds.stage.value if hasattr(ds.stage, 'value') else ds.stage
        if disease_def and "stages" in disease_def and stage in disease_def["stages"]:
            return disease_def["stages"][stage]["symptoms"]
        return [] 