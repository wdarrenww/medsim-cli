"""
enhanced scenario generator with disease progression and dynamic patient loading
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import random
import json

from ..core.dynamic_patient_loader import DynamicPatientLoader, PatientLoadConfig, PatientLoadResult
from ..core.disease_progression import DiseaseProgressionEngine
from ..data.clinical_patterns import ClinicalPatterns
from .scenario_generator import DynamicScenarioGenerator, DynamicScenarioConfig


@dataclass
class EnhancedScenarioConfig:
    """enhanced scenario configuration"""
    specialty: Optional[str] = None
    difficulty: str = "medium"
    complexity_level: str = "moderate"  # simple, moderate, complex
    temporal_progression: bool = True
    disease_progression: bool = True
    social_determinants: bool = True
    realistic_outcomes: bool = True
    adaptive_difficulty: bool = True
    user_performance: Optional[Dict[str, float]] = None
    scenario_duration_hours: float = 4.0
    complication_probability: float = 0.3
    treatment_response_variability: float = 0.2
    include_underlying_cause: bool = True
    include_misleading_clues: bool = True
    include_incomplete_history: bool = True
    include_system_barriers: bool = True


@dataclass
class TemporalEvent:
    """represents a temporal event in scenario progression"""
    timestamp: datetime
    event_type: str  # disease_progression, complication, treatment, vital_change
    description: str
    severity_change: float
    new_symptoms: List[str]
    new_findings: List[str]
    required_actions: List[str]


@dataclass
class EnhancedScenario:
    """enhanced scenario with temporal progression"""
    scenario_id: str
    title: str
    description: str
    specialty: str
    difficulty: str
    patient_load_result: PatientLoadResult
    temporal_events: List[TemporalEvent]
    disease_progression_timeline: List[Dict[str, Any]]
    treatment_timeline: List[Dict[str, Any]]
    outcome_probabilities: Dict[str, float]
    learning_objectives: List[str]
    key_decision_points: List[Dict[str, Any]]
    created_at: datetime
    config: EnhancedScenarioConfig
    underlying_cause: Optional[str] = None
    underlying_cause_rationale: Optional[str] = None
    misleading_clues: List[str] = field(default_factory=list)
    incomplete_history: Optional[str] = None
    system_barriers: List[str] = field(default_factory=list)
    differential_diagnosis: List[str] = field(default_factory=list)
    final_diagnosis: Optional[str] = None


class EnhancedScenarioGenerator:
    """enhanced scenario generator with disease progression and temporal events"""
    
    def __init__(self):
        self.patient_loader = DynamicPatientLoader()
        self.disease_engine = DiseaseProgressionEngine()
        self.patterns = ClinicalPatterns()
        self.base_generator = DynamicScenarioGenerator()
        
        # temporal event templates
        self.event_templates = self._initialize_event_templates()
        
        # outcome probability models
        self.outcome_models = self._initialize_outcome_models()
    
    def _initialize_event_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """initialize temporal event templates"""
        return {
            "acute_coronary_syndrome": [
                {
                    "time_offset_hours": 0.5,
                    "event_type": "disease_progression",
                    "description": "Patient develops worsening chest pain with radiation to left arm",
                    "severity_change": 0.2,
                    "new_symptoms": ["increased chest pain", "left arm pain"],
                    "new_findings": ["elevated troponin", "st depression on ecg"],
                    "required_actions": ["repeat ecg", "order cardiac enzymes", "administer nitroglycerin"]
                },
                {
                    "time_offset_hours": 1.0,
                    "event_type": "complication",
                    "description": "Patient develops ventricular arrhythmia",
                    "severity_change": 0.4,
                    "new_symptoms": ["palpitations", "dizziness"],
                    "new_findings": ["ventricular tachycardia", "hypotension"],
                    "required_actions": ["defibrillation", "antiarrhythmic medication", "emergent cath lab"]
                }
            ],
            "pneumonia": [
                {
                    "time_offset_hours": 2.0,
                    "event_type": "disease_progression",
                    "description": "Patient develops respiratory distress",
                    "severity_change": 0.3,
                    "new_symptoms": ["increased shortness of breath", "use of accessory muscles"],
                    "new_findings": ["decreased oxygen saturation", "increased respiratory rate"],
                    "required_actions": ["oxygen therapy", "chest x-ray", "consider intubation"]
                },
                {
                    "time_offset_hours": 4.0,
                    "event_type": "complication",
                    "description": "Patient develops pleural effusion",
                    "severity_change": 0.2,
                    "new_symptoms": ["pleuritic chest pain"],
                    "new_findings": ["pleural effusion on imaging", "decreased breath sounds"],
                    "required_actions": ["thoracentesis", "chest tube placement"]
                }
            ],
            "sepsis": [
                {
                    "time_offset_hours": 1.0,
                    "event_type": "disease_progression",
                    "description": "Patient develops septic shock",
                    "severity_change": 0.5,
                    "new_symptoms": ["hypotension", "altered mental status"],
                    "new_findings": ["lactic acidosis", "decreased urine output"],
                    "required_actions": ["vasopressors", "broad spectrum antibiotics", "fluid resuscitation"]
                },
                {
                    "time_offset_hours": 3.0,
                    "event_type": "complication",
                    "description": "Patient develops acute respiratory distress syndrome",
                    "severity_change": 0.4,
                    "new_symptoms": ["severe respiratory distress"],
                    "new_findings": ["bilateral infiltrates", "hypoxemia"],
                    "required_actions": ["mechanical ventilation", "prone positioning"]
                }
            ]
        }
    
    def _initialize_outcome_models(self) -> Dict[str, Dict[str, float]]:
        """initialize outcome probability models"""
        return {
            "acute_coronary_syndrome": {
                "survival": 0.95,
                "complete_recovery": 0.70,
                "complications": 0.30,
                "readmission": 0.15,
                "mortality": 0.05
            },
            "pneumonia": {
                "survival": 0.90,
                "complete_recovery": 0.80,
                "complications": 0.20,
                "readmission": 0.10,
                "mortality": 0.10
            },
            "sepsis": {
                "survival": 0.75,
                "complete_recovery": 0.50,
                "complications": 0.50,
                "readmission": 0.25,
                "mortality": 0.25
            },
            "stroke": {
                "survival": 0.85,
                "complete_recovery": 0.30,
                "complications": 0.70,
                "readmission": 0.20,
                "mortality": 0.15
            }
        }
    
    def generate_enhanced_scenario(self, config: EnhancedScenarioConfig) -> EnhancedScenario:
        """generate an enhanced scenario with temporal progression"""
        # load dynamic patient
        patient_config = PatientLoadConfig(
            specialty=config.specialty,
            difficulty=config.difficulty,
            complexity_level=config.complexity_level,
            social_determinants=config.social_determinants,
            comorbidities=True,
            disease_progression=config.disease_progression,
            realistic_vitals=True,
            medication_history=True
        )
        
        patient_result = self.patient_loader.load_patient(patient_config)
        
        # generate temporal events
        temporal_events = self._generate_temporal_events(patient_result, config)
        
        # generate disease progression timeline
        disease_timeline = self._generate_disease_timeline(patient_result, config)
        
        # generate treatment timeline
        treatment_timeline = self._generate_treatment_timeline(patient_result, config)
        
        # calculate outcome probabilities
        outcome_probabilities = self._calculate_outcome_probabilities(patient_result, config)
        
        # generate learning objectives
        learning_objectives = self._generate_learning_objectives(patient_result, config)
        
        # generate key decision points
        key_decision_points = self._generate_key_decision_points(patient_result, temporal_events, config)
        
        # underlying cause logic
        underlying_cause, rationale = None, None
        if config.include_underlying_cause and random.random() < (0.7 if config.difficulty=="hard" else 0.3):
            underlying_cause, rationale = self._select_underlying_cause(patient_result, config)
        # misleading clues
        misleading_clues = []
        if config.include_misleading_clues and config.difficulty in ["medium", "hard"]:
            misleading_clues = self._generate_misleading_clues(patient_result, config)
        # incomplete history
        incomplete_history = None
        if config.include_incomplete_history and config.difficulty=="hard":
            incomplete_history = self._generate_incomplete_history(patient_result, config)
        # system barriers
        system_barriers = []
        if config.include_system_barriers and config.difficulty=="hard":
            system_barriers = self._generate_system_barriers(patient_result, config)
        # differential/final diagnosis
        differential = self._generate_differential(patient_result, config)
        final_dx = underlying_cause or (differential[0] if differential else None)
        
        # create scenario
        scenario = EnhancedScenario(
            scenario_id=f"enhanced_{random.randint(1000, 9999)}",
            title=self._generate_scenario_title(patient_result, config),
            description=self._generate_scenario_description(patient_result, config),
            specialty=config.specialty or "emergency_medicine",
            difficulty=config.difficulty,
            patient_load_result=patient_result,
            temporal_events=temporal_events,
            disease_progression_timeline=disease_timeline,
            treatment_timeline=treatment_timeline,
            outcome_probabilities=outcome_probabilities,
            learning_objectives=learning_objectives,
            key_decision_points=key_decision_points,
            created_at=datetime.now(),
            config=config,
            underlying_cause=underlying_cause,
            underlying_cause_rationale=rationale,
            misleading_clues=misleading_clues,
            incomplete_history=incomplete_history,
            system_barriers=system_barriers,
            differential_diagnosis=differential,
            final_diagnosis=final_dx
        )
        
        return scenario
    
    def _generate_temporal_events(self, patient_result: PatientLoadResult, 
                                config: EnhancedScenarioConfig) -> List[TemporalEvent]:
        """generate temporal events for scenario progression"""
        events = []
        
        if not config.temporal_progression:
            return events
        
        # get primary disease
        primary_disease = None
        if patient_result.disease_states:
            primary_disease = patient_result.disease_states[0].disease_name
        
        if not primary_disease or primary_disease not in self.event_templates:
            return events
        
        # generate events based on templates
        event_templates = self.event_templates[primary_disease]
        
        for template in event_templates:
            # adjust timing based on difficulty
            time_offset = template["time_offset_hours"]
            if config.difficulty == "easy":
                time_offset *= 1.5  # more time to react
            elif config.difficulty == "hard":
                time_offset *= 0.7  # less time to react
            
            # add randomness
            time_offset += random.uniform(-0.5, 0.5)
            time_offset = max(0.1, time_offset)
            
            # determine if event occurs based on probability
            if random.random() < config.complication_probability:
                event = TemporalEvent(
                    timestamp=datetime.now() + timedelta(hours=time_offset),
                    event_type=template["event_type"],
                    description=template["description"],
                    severity_change=template["severity_change"],
                    new_symptoms=template["new_symptoms"],
                    new_findings=template["new_findings"],
                    required_actions=template["required_actions"]
                )
                events.append(event)
        
        # sort events by timestamp
        events.sort(key=lambda x: x.timestamp)
        
        return events
    
    def _generate_disease_timeline(self, patient_result: PatientLoadResult, 
                                 config: EnhancedScenarioConfig) -> List[Dict[str, Any]]:
        """generate disease progression timeline"""
        timeline = []
        
        if not config.disease_progression:
            return timeline
        
        current_time = datetime.now()
        
        for disease_state in patient_result.disease_states:
            disease_name = disease_state.disease_name
            
            # simulate progression over scenario duration
            duration_hours = config.scenario_duration_hours
            time_steps = int(duration_hours * 4)  # every 15 minutes
            
            for i in range(time_steps):
                time_offset = i * 0.25  # 15 minutes
                simulation_time = current_time + timedelta(hours=time_offset)
                
                # progress disease
                progressed_state = self.disease_engine.progress_disease(
                    patient_result.patient.patient_id,
                    disease_name,
                    timedelta(hours=time_offset)
                )
                
                if progressed_state:
                    timeline_entry = {
                        "timestamp": simulation_time,
                        "disease_name": disease_name,
                        "stage": progressed_state.stage.value,
                        "severity": progressed_state.severity_score,
                        "symptoms": self._get_current_symptoms(progressed_state),
                        "vital_signs": self._get_current_vitals(patient_result.patient, progressed_state)
                    }
                    timeline.append(timeline_entry)
        
        return timeline
    
    def _generate_treatment_timeline(self, patient_result: PatientLoadResult, 
                                   config: EnhancedScenarioConfig) -> List[Dict[str, Any]]:
        """generate treatment timeline with responses"""
        timeline = []
        
        # get available treatments for patient's conditions
        available_treatments = []
        for condition in patient_result.patient.conditions:
            condition_lower = condition.lower()
            
            if "coronary" in condition_lower or "heart" in condition_lower:
                available_treatments.extend(["aspirin", "nitroglycerin", "morphine"])
            elif "pneumonia" in condition_lower or "respiratory" in condition_lower:
                available_treatments.extend(["antibiotics", "oxygen", "albuterol"])
            elif "sepsis" in condition_lower:
                available_treatments.extend(["antibiotics", "fluids", "vasopressors"])
        
        # generate treatment timeline
        current_time = datetime.now()
        treatment_interval = config.scenario_duration_hours / 4  # 4 treatments over scenario
        
        for i in range(4):
            if available_treatments:
                treatment_name = random.choice(available_treatments)
                
                # calculate treatment response
                base_effectiveness = 0.8
                if config.treatment_response_variability > 0:
                    effectiveness_variation = random.uniform(
                        -config.treatment_response_variability,
                        config.treatment_response_variability
                    )
                    effectiveness = max(0.1, min(1.0, base_effectiveness + effectiveness_variation))
                else:
                    effectiveness = base_effectiveness
                
                treatment_time = current_time + timedelta(hours=i * treatment_interval)
                
                timeline_entry = {
                    "timestamp": treatment_time,
                    "treatment": treatment_name,
                    "effectiveness": effectiveness,
                    "response_type": self._get_response_type(effectiveness),
                    "side_effects": self._generate_side_effects(treatment_name, effectiveness),
                    "patient_response": self._get_patient_response(effectiveness)
                }
                timeline.append(timeline_entry)
        
        return timeline
    
    def _calculate_outcome_probabilities(self, patient_result: PatientLoadResult, 
                                       config: EnhancedScenarioConfig) -> Dict[str, float]:
        """calculate outcome probabilities based on patient state"""
        if not patient_result.disease_states:
            return {"survival": 0.95, "complete_recovery": 0.90}
        
        # get primary disease
        primary_disease = patient_result.disease_states[0].disease_name
        base_outcomes = self.outcome_models.get(primary_disease, {})
        
        # adjust based on patient factors
        adjusted_outcomes = {}
        for outcome, base_prob in base_outcomes.items():
            adjusted_prob = base_prob
            
            # adjust for severity
            max_severity = max(d.severity_score for d in patient_result.disease_states)
            if max_severity > 0.8:
                adjusted_prob *= 0.7  # worse outcomes for severe disease
            elif max_severity < 0.3:
                adjusted_prob *= 1.2  # better outcomes for mild disease
            
            # adjust for social determinants
            social_multiplier = patient_result.social_context.get("risk_multiplier", 1.0)
            adjusted_prob *= (2.0 - social_multiplier)  # inverse relationship
            
            # adjust for age
            if patient_result.patient.age > 80:
                adjusted_prob *= 0.8
            elif patient_result.patient.age > 65:
                adjusted_prob *= 0.9
            
            adjusted_outcomes[outcome] = max(0.0, min(1.0, adjusted_prob))
        
        return adjusted_outcomes
    
    def _generate_learning_objectives(self, patient_result: PatientLoadResult, 
                                    config: EnhancedScenarioConfig) -> List[str]:
        """generate learning objectives based on patient state"""
        objectives = []
        
        # base objectives
        objectives.extend([
            "assess patient presentation systematically",
            "formulate appropriate differential diagnosis",
            "order relevant diagnostic studies",
            "initiate timely treatment interventions"
        ])
        
        # specialty-specific objectives
        if config.specialty == "emergency_medicine":
            objectives.extend([
                "recognize life-threatening conditions",
                "prioritize interventions based on acuity",
                "manage multiple simultaneous problems"
            ])
        elif config.specialty == "cardiology":
            objectives.extend([
                "interpret cardiac diagnostic studies",
                "manage acute coronary syndromes",
                "recognize cardiac complications"
            ])
        
        # difficulty-specific objectives
        if config.difficulty == "hard":
            objectives.extend([
                "manage complex comorbidities",
                "recognize atypical presentations",
                "coordinate multidisciplinary care"
            ])
        
        # complexity-specific objectives
        if config.complexity_level == "complex":
            objectives.extend([
                "manage multiple organ system involvement",
                "coordinate care with multiple specialists",
                "address social determinants of health"
            ])
        
        return objectives
    
    def _generate_key_decision_points(self, patient_result: PatientLoadResult, 
                                    temporal_events: List[TemporalEvent], 
                                    config: EnhancedScenarioConfig) -> List[Dict[str, Any]]:
        """generate key decision points for scenario"""
        decision_points = []
        
        # initial assessment decision point
        decision_points.append({
            "timestamp": datetime.now(),
            "description": "Initial patient assessment and triage",
            "required_actions": ["vital_signs", "history", "physical_exam"],
            "critical_decisions": ["acuity_level", "immediate_interventions"],
            "time_pressure": "high" if config.difficulty == "hard" else "moderate"
        })
        
        # add decision points for temporal events
        for event in temporal_events:
            decision_points.append({
                "timestamp": event.timestamp,
                "description": f"Response to {event.event_type}: {event.description}",
                "required_actions": event.required_actions,
                "critical_decisions": ["escalation_level", "intervention_choice"],
                "time_pressure": "high" if event.severity_change > 0.3 else "moderate"
            })
        
        # final disposition decision point
        final_time = datetime.now() + timedelta(hours=config.scenario_duration_hours)
        decision_points.append({
            "timestamp": final_time,
            "description": "Final disposition and follow-up planning",
            "required_actions": ["disposition_decision", "follow_up_arrangements"],
            "critical_decisions": ["admission_vs_discharge", "specialist_consultation"],
            "time_pressure": "low"
        })
        
        return decision_points
    
    def _generate_scenario_title(self, patient_result: PatientLoadResult, 
                               config: EnhancedScenarioConfig) -> str:
        """generate scenario title"""
        patient = patient_result.patient
        primary_condition = patient.conditions[0] if patient.conditions else "Medical Emergency"
        
        titles = {
            "acute_coronary_syndrome": f"Acute Coronary Syndrome in {patient.age}y {patient.gender}",
            "pneumonia": f"Severe Pneumonia in {patient.age}y {patient.gender}",
            "sepsis": f"Septic Shock in {patient.age}y {patient.gender}",
            "stroke": f"Acute Stroke in {patient.age}y {patient.gender}"
        }
        
        return titles.get(primary_condition.lower(), f"{primary_condition} in {patient.age}y {patient.gender}")
    
    def _generate_scenario_description(self, patient_result: PatientLoadResult, 
                                    config: EnhancedScenarioConfig) -> str:
        """generate scenario description"""
        patient = patient_result.patient
        description = f"A {patient.age}-year-old {patient.gender} presents with "
        
        if patient.symptoms:
            description += ", ".join(patient.symptoms[:3])
        else:
            description += "acute medical condition"
        
        description += f". Patient has {len(patient.conditions)} chronic conditions"
        
        if patient_result.social_context.get("determinants"):
            description += f" and faces {len(patient_result.social_context['determinants'])} social challenges"
        
        description += f". This is a {config.difficulty} complexity case requiring "
        description += f"{config.complexity_level} level management."
        
        return description
    
    def _get_current_symptoms(self, disease_state) -> List[str]:
        """get current symptoms for disease state"""
        disease_def = self.disease_engine.disease_definitions[disease_state.disease_name]
        current_stage = disease_state.stage.value
        
        if current_stage in disease_def["stages"]:
            return disease_def["stages"][current_stage]["symptoms"]
        
        return []
    
    def _get_current_vitals(self, patient, disease_state) -> Dict[str, float]:
        """get current vital signs adjusted for disease state"""
        vitals = patient.vital_signs.copy()
        
        # adjust vitals based on disease severity
        severity = disease_state.severity_score
        
        if "coronary" in disease_state.disease_name:
            vitals["heart_rate"] += int(severity * 20)
            vitals["bp_systolic"] += int(severity * 15)
        
        elif "pneumonia" in disease_state.disease_name:
            vitals["respiratory_rate"] += int(severity * 8)
            vitals["oxygen_saturation"] -= int(severity * 5)
        
        return vitals
    
    def _get_response_type(self, effectiveness: float) -> str:
        """get treatment response type based on effectiveness"""
        if effectiveness >= 0.8:
            return "excellent"
        elif effectiveness >= 0.6:
            return "good"
        elif effectiveness >= 0.4:
            return "moderate"
        elif effectiveness >= 0.2:
            return "poor"
        else:
            return "resistant"
    
    def _generate_side_effects(self, treatment_name: str, effectiveness: float) -> List[str]:
        """generate side effects for treatment"""
        side_effects = []
        
        # lower effectiveness may indicate more side effects
        side_effect_probability = 0.3 * (1.0 - effectiveness)
        
        treatment_side_effects = {
            "aspirin": ["gastrointestinal_bleeding", "allergic_reaction"],
            "nitroglycerin": ["headache", "hypotension"],
            "antibiotics": ["diarrhea", "allergic_reaction"],
            "oxygen": ["oxygen_toxicity", "dry_mucous_membranes"]
        }
        
        if treatment_name in treatment_side_effects:
            for side_effect in treatment_side_effects[treatment_name]:
                if random.random() < side_effect_probability:
                    side_effects.append(side_effect)
        
        return side_effects
    
    def _get_patient_response(self, effectiveness: float) -> str:
        """get patient response to treatment"""
        if effectiveness >= 0.8:
            return "Patient reports significant improvement"
        elif effectiveness >= 0.6:
            return "Patient reports moderate improvement"
        elif effectiveness >= 0.4:
            return "Patient reports minimal improvement"
        elif effectiveness >= 0.2:
            return "Patient reports no improvement"
        else:
            return "Patient reports worsening symptoms"
    
    def get_enhanced_scenario_summary(self, scenario: EnhancedScenario) -> Dict[str, Any]:
        """get comprehensive scenario summary"""
        return {
            "scenario_id": scenario.scenario_id,
            "title": scenario.title,
            "description": scenario.description,
            "specialty": scenario.specialty,
            "difficulty": scenario.difficulty,
            "patient_summary": {
                "age": scenario.patient_load_result.patient.age,
                "gender": scenario.patient_load_result.patient.gender,
                "conditions": scenario.patient_load_result.patient.conditions,
                "symptoms": scenario.patient_load_result.patient.symptoms,
                "medications": scenario.patient_load_result.patient.medications
            },
            "disease_states": [
                {
                    "name": d.disease_name,
                    "stage": d.stage.value,
                    "severity": d.severity_score,
                    "prognosis": d.prognosis
                }
                for d in scenario.patient_load_result.disease_states
            ],
            "temporal_events": [
                {
                    "time": e.timestamp.isoformat(),
                    "type": e.event_type,
                    "description": e.description,
                    "severity_change": e.severity_change
                }
                for e in scenario.temporal_events
            ],
            "outcome_probabilities": scenario.outcome_probabilities,
            "learning_objectives": scenario.learning_objectives,
            "key_decision_points": len(scenario.key_decision_points),
            "medical_complexity": scenario.patient_load_result.medical_complexity,
            "risk_score": scenario.patient_load_result.risk_score
        }
    
    def _select_underlying_cause(self, patient_result, config):
        # pick a root cause from conditions or add a hidden one
        possible_causes = [c for c in patient_result.patient.conditions if "secondary" not in c.lower()]
        if not possible_causes:
            return None, None
        cause = random.choice(possible_causes)
        rationale = f"Underlying cause is {cause} due to risk factors and presentation."
        return cause, rationale
    
    def _generate_misleading_clues(self, patient_result, config):
        clues = ["Patient reports vague abdominal pain.", "History from unreliable source.", "Recent travel, but unrelated."]
        return random.sample(clues, k=min(2, len(clues)))
    
    def _generate_incomplete_history(self, patient_result, config):
        return "Patient unable to provide full history due to confusion."
    
    def _generate_system_barriers(self, patient_result, config):
        return ["Lab results delayed due to system outage.", "Language barrier requires interpreter."]
    
    def _generate_differential(self, patient_result, config):
        # generate plausible differentials
        base = [c for c in patient_result.patient.conditions]
        distractors = ["viral syndrome", "medication side effect", "functional disorder"]
        return base + random.sample(distractors, k=2) 