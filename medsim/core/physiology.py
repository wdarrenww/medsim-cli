"""
advanced physiological model for cardiovascular, respiratory, and renal systems
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import math
import random


@dataclass
class CardiovascularSystem:
    """advanced cardiovascular system parameters"""
    heart_rate: float = 80.0  # bpm
    blood_pressure_systolic: float = 120.0  # mmHg
    blood_pressure_diastolic: float = 80.0  # mmHg
    cardiac_output: float = 5.0  # L/min
    stroke_volume: float = 62.5  # ml
    peripheral_resistance: float = 1.0  # arbitrary units
    ejection_fraction: float = 65.0  # %
    cardiac_index: float = 3.0  # L/min/m²
    pulmonary_capillary_wedge_pressure: float = 8.0  # mmHg
    central_venous_pressure: float = 5.0  # mmHg
    coronary_perfusion_pressure: float = 80.0  # mmHg
    
    def update_from_stress(self, stress_level: float, time_delta: float) -> None:
        """update cardiovascular parameters based on stress with time progression"""
        # acute stress response
        self.heart_rate += stress_level * 25 * time_delta
        self.blood_pressure_systolic += stress_level * 20 * time_delta
        self.blood_pressure_diastolic += stress_level * 12 * time_delta
        self.cardiac_output += stress_level * 2.0 * time_delta
        
        # chronic stress effects
        if stress_level > 0.7:
            self.ejection_fraction -= stress_level * 5 * time_delta
            self.coronary_perfusion_pressure -= stress_level * 10 * time_delta
        
        # maintain physiological limits
        self.heart_rate = max(40, min(220, self.heart_rate))
        self.blood_pressure_systolic = max(70, min(250, self.blood_pressure_systolic))
        self.blood_pressure_diastolic = max(40, min(150, self.blood_pressure_diastolic))
        self.ejection_fraction = max(20, min(80, self.ejection_fraction))
        self.cardiac_output = max(2.0, min(15.0, self.cardiac_output))
    
    def update_from_medication(self, medication: str, dose: float, time_delta: float) -> None:
        """update cardiovascular parameters based on medication with time progression"""
        if medication.lower() == "nitroglycerin":
            # rapid vasodilator effect
            self.blood_pressure_systolic -= dose * 15 * time_delta
            self.blood_pressure_diastolic -= dose * 8 * time_delta
            self.peripheral_resistance -= dose * 0.3 * time_delta
            self.coronary_perfusion_pressure += dose * 20 * time_delta
            self.heart_rate += dose * 10 * time_delta  # reflex tachycardia
            
        elif medication.lower() == "aspirin":
            # minimal acute cardiovascular effect
            pass
            
        elif medication.lower() == "epinephrine":
            # potent vasopressor effect
            self.heart_rate += dose * 40 * time_delta
            self.blood_pressure_systolic += dose * 30 * time_delta
            self.blood_pressure_diastolic += dose * 20 * time_delta
            self.cardiac_output += dose * 3.0 * time_delta
            self.peripheral_resistance += dose * 0.5 * time_delta
            
        elif medication.lower() == "metoprolol":
            # beta blockade
            self.heart_rate -= dose * 15 * time_delta
            self.blood_pressure_systolic -= dose * 10 * time_delta
            self.blood_pressure_diastolic -= dose * 8 * time_delta
            self.cardiac_output -= dose * 1.5 * time_delta
            
        elif medication.lower() == "lisinopril":
            # ace inhibition
            self.blood_pressure_systolic -= dose * 8 * time_delta
            self.blood_pressure_diastolic -= dose * 5 * time_delta
            self.peripheral_resistance -= dose * 0.2 * time_delta
            
        elif medication.lower() == "furosemide":
            # diuretic effect on cardiovascular system
            self.central_venous_pressure -= dose * 2 * time_delta
            self.pulmonary_capillary_wedge_pressure -= dose * 3 * time_delta
    
    def update_from_disease(self, disease: str, severity: float, time_delta: float) -> None:
        """update cardiovascular parameters based on disease progression"""
        if disease.lower() == "myocardial_infarction":
            # acute mi effects
            self.ejection_fraction -= severity * 15 * time_delta
            self.cardiac_output -= severity * 2.0 * time_delta
            self.heart_rate += severity * 20 * time_delta
            self.coronary_perfusion_pressure -= severity * 25 * time_delta
            
        elif disease.lower() == "congestive_heart_failure":
            # chf effects
            self.ejection_fraction -= severity * 10 * time_delta
            self.cardiac_output -= severity * 1.5 * time_delta
            self.heart_rate += severity * 15 * time_delta
            self.pulmonary_capillary_wedge_pressure += severity * 8 * time_delta
            
        elif disease.lower() == "septic_shock":
            # septic shock effects
            self.blood_pressure_systolic -= severity * 30 * time_delta
            self.blood_pressure_diastolic -= severity * 20 * time_delta
            self.heart_rate += severity * 35 * time_delta
            self.cardiac_output += severity * 2.0 * time_delta  # initially increased
    
    def get_vital_signs(self) -> Dict[str, float]:
        """get current cardiovascular vital signs"""
        return {
            'heart_rate': self.heart_rate,
            'bp_systolic': self.blood_pressure_systolic,
            'bp_diastolic': self.blood_pressure_diastolic,
            'cardiac_output': self.cardiac_output,
            'ejection_fraction': self.ejection_fraction
        }
    
    def get_advanced_parameters(self) -> Dict[str, float]:
        """get advanced cardiovascular parameters"""
        return {
            'stroke_volume': self.stroke_volume,
            'peripheral_resistance': self.peripheral_resistance,
            'cardiac_index': self.cardiac_index,
            'pcwp': self.pulmonary_capillary_wedge_pressure,
            'cvp': self.central_venous_pressure,
            'coronary_perfusion_pressure': self.coronary_perfusion_pressure
        }


@dataclass
class RespiratorySystem:
    """advanced respiratory system parameters"""
    respiratory_rate: float = 16.0  # breaths/min
    tidal_volume: float = 500.0  # ml
    minute_ventilation: float = 8.0  # L/min
    oxygen_saturation: float = 98.0  # %
    end_tidal_co2: float = 40.0  # mmHg
    lung_compliance: float = 1.0  # arbitrary units
    airway_resistance: float = 1.0  # arbitrary units
    functional_residual_capacity: float = 2.5  # L
    vital_capacity: float = 4.5  # L
    peak_expiratory_flow: float = 400.0  # L/min
    alveolar_oxygen_pressure: float = 100.0  # mmHg
    alveolar_co2_pressure: float = 40.0  # mmHg
    
    def update_from_stress(self, stress_level: float, time_delta: float) -> None:
        """update respiratory parameters based on stress with time progression"""
        # acute stress response
        self.respiratory_rate += stress_level * 12 * time_delta
        self.minute_ventilation = self.respiratory_rate * self.tidal_volume / 1000
        
        # chronic stress effects
        if stress_level > 0.6:
            self.lung_compliance -= stress_level * 0.2 * time_delta
            self.airway_resistance += stress_level * 0.3 * time_delta
        
        # maintain physiological limits
        self.respiratory_rate = max(8, min(50, self.respiratory_rate))
        self.oxygen_saturation = max(85, min(100, self.oxygen_saturation))
        self.lung_compliance = max(0.3, min(2.0, self.lung_compliance))
        self.airway_resistance = max(0.5, min(3.0, self.airway_resistance))
    
    def update_from_medication(self, medication: str, dose: float, time_delta: float) -> None:
        """update respiratory parameters based on medication with time progression"""
        if medication.lower() == "albuterol":
            # bronchodilator effect
            self.lung_compliance += dose * 0.4 * time_delta
            self.airway_resistance -= dose * 0.5 * time_delta
            self.respiratory_rate -= dose * 3 * time_delta
            self.peak_expiratory_flow += dose * 50 * time_delta
            
        elif medication.lower() == "morphine":
            # respiratory depressant effect
            self.respiratory_rate -= dose * 6 * time_delta
            self.tidal_volume -= dose * 100 * time_delta
            self.oxygen_saturation -= dose * 3 * time_delta
            self.minute_ventilation = self.respiratory_rate * self.tidal_volume / 1000
            
        elif medication.lower() == "furosemide":
            # can affect pulmonary vascular resistance
            pass
            
        elif medication.lower() == "nitroglycerin":
            # can improve pulmonary blood flow
            self.alveolar_oxygen_pressure += dose * 5 * time_delta
    
    def update_from_disease(self, disease: str, severity: float, time_delta: float) -> None:
        """update respiratory parameters based on disease progression"""
        if disease.lower() == "copd_exacerbation":
            # copd effects
            self.lung_compliance -= severity * 0.3 * time_delta
            self.airway_resistance += severity * 0.4 * time_delta
            self.respiratory_rate += severity * 8 * time_delta
            self.oxygen_saturation -= severity * 6 * time_delta
            self.peak_expiratory_flow -= severity * 80 * time_delta
            
        elif disease.lower() == "pneumonia":
            # pneumonia effects
            self.lung_compliance -= severity * 0.4 * time_delta
            self.oxygen_saturation -= severity * 8 * time_delta
            self.respiratory_rate += severity * 10 * time_delta
            self.alveolar_oxygen_pressure -= severity * 15 * time_delta
            
        elif disease.lower() == "pulmonary_embolism":
            # pe effects
            self.oxygen_saturation -= severity * 12 * time_delta
            self.respiratory_rate += severity * 15 * time_delta
            self.alveolar_oxygen_pressure -= severity * 25 * time_delta
    
    def get_vital_signs(self) -> Dict[str, float]:
        """get current respiratory vital signs"""
        return {
            'respiratory_rate': self.respiratory_rate,
            'oxygen_saturation': self.oxygen_saturation,
            'minute_ventilation': self.minute_ventilation,
            'end_tidal_co2': self.end_tidal_co2
        }
    
    def get_advanced_parameters(self) -> Dict[str, float]:
        """get advanced respiratory parameters"""
        return {
            'tidal_volume': self.tidal_volume,
            'lung_compliance': self.lung_compliance,
            'airway_resistance': self.airway_resistance,
            'functional_residual_capacity': self.functional_residual_capacity,
            'vital_capacity': self.vital_capacity,
            'peak_expiratory_flow': self.peak_expiratory_flow,
            'alveolar_oxygen_pressure': self.alveolar_oxygen_pressure,
            'alveolar_co2_pressure': self.alveolar_co2_pressure
        }


@dataclass
class RenalSystem:
    """advanced renal system parameters"""
    urine_output: float = 1.0  # ml/min
    creatinine: float = 1.0  # mg/dL
    bun: float = 15.0  # mg/dL
    gfr: float = 100.0  # ml/min/1.73m²
    sodium: float = 140.0  # mEq/L
    potassium: float = 4.0  # mEq/L
    chloride: float = 102.0  # mEq/L
    bicarbonate: float = 24.0  # mEq/L
    urine_specific_gravity: float = 1.020
    fractional_excretion_sodium: float = 1.0  # %
    renal_blood_flow: float = 1200.0  # ml/min
    
    def update_from_stress(self, stress_level: float, time_delta: float) -> None:
        """update renal parameters based on stress with time progression"""
        # stress affects renal perfusion
        if stress_level > 0.5:
            self.urine_output *= (1 - stress_level * 0.4 * time_delta)
            self.gfr *= (1 - stress_level * 0.15 * time_delta)
            self.renal_blood_flow *= (1 - stress_level * 0.2 * time_delta)
            
            # stress can cause electrolyte imbalances
            if stress_level > 0.7:
                self.sodium += stress_level * 2 * time_delta
                self.potassium += stress_level * 0.3 * time_delta
    
    def update_from_medication(self, medication: str, dose: float, time_delta: float) -> None:
        """update renal parameters based on medication with time progression"""
        if medication.lower() == "furosemide":
            # diuretic effect
            self.urine_output += dose * 8 * time_delta
            self.sodium -= dose * 2 * time_delta
            self.potassium -= dose * 0.5 * time_delta
            self.urine_specific_gravity -= dose * 0.005 * time_delta
            
        elif medication.lower() == "ace_inhibitor":
            # can affect renal function
            self.gfr *= (1 - dose * 0.08 * time_delta)
            self.potassium += dose * 0.2 * time_delta
            
        elif medication.lower() == "heparin":
            # minimal renal effect
            pass
            
        elif medication.lower() == "morphine":
            # can cause urinary retention
            self.urine_output *= (1 - dose * 0.3 * time_delta)
    
    def update_from_disease(self, disease: str, severity: float, time_delta: float) -> None:
        """update renal parameters based on disease progression"""
        if disease.lower() == "acute_kidney_injury":
            # aki effects
            self.gfr -= severity * 20 * time_delta
            self.creatinine += severity * 0.5 * time_delta
            self.bun += severity * 3 * time_delta
            self.urine_output *= (1 - severity * 0.6 * time_delta)
            
        elif disease.lower() == "sepsis":
            # sepsis effects on kidneys
            self.gfr -= severity * 15 * time_delta
            self.creatinine += severity * 0.3 * time_delta
            self.urine_output *= (1 - severity * 0.4 * time_delta)
            self.sodium -= severity * 2 * time_delta  # hyponatremia
    
    def get_lab_values(self) -> Dict[str, float]:
        """get current renal lab values"""
        return {
            'creatinine': self.creatinine,
            'bun': self.bun,
            'gfr': self.gfr,
            'sodium': self.sodium,
            'potassium': self.potassium,
            'chloride': self.chloride,
            'bicarbonate': self.bicarbonate
        }
    
    def get_advanced_parameters(self) -> Dict[str, float]:
        """get advanced renal parameters"""
        return {
            'urine_output': self.urine_output,
            'urine_specific_gravity': self.urine_specific_gravity,
            'fractional_excretion_sodium': self.fractional_excretion_sodium,
            'renal_blood_flow': self.renal_blood_flow
        }


@dataclass
class EndocrineSystem:
    """advanced endocrine system parameters"""
    glucose: float = 90.0  # mg/dL
    insulin: float = 10.0  # μU/mL
    cortisol: float = 15.0  # μg/dL
    tsh: float = 2.0  # μIU/mL
    t4: float = 8.0  # μg/dL
    hba1c: float = 5.5  # %
    ketones: float = 0.1  # mmol/L
    def update(self, patient_state: Dict[str, Any], time_delta: float) -> None:
        # Placeholder for endocrine update logic
        pass

@dataclass
class NeurologicalSystem:
    """advanced neurological system parameters"""
    gcs: int = 15  # Glasgow Coma Scale
    pupils_equal: bool = True
    seizure_activity: bool = False
    focal_deficit: bool = False
    icp: float = 10.0  # mmHg
    def update(self, patient_state: Dict[str, Any], time_delta: float) -> None:
        # Placeholder for neuro update logic
        pass

@dataclass
class GastrointestinalSystem:
    """advanced GI/liver system parameters"""
    ast: float = 25.0  # U/L
    alt: float = 25.0  # U/L
    bilirubin: float = 1.0  # mg/dL
    albumin: float = 4.0  # g/dL
    inr: float = 1.0
    amylase: float = 50.0  # U/L
    lipase: float = 50.0  # U/L
    gi_bleed: bool = False
    def update(self, patient_state: Dict[str, Any], time_delta: float) -> None:
        # Placeholder for GI/liver update logic
        pass

@dataclass
class HematologySystem:
    """advanced hematology system parameters"""
    wbc: float = 7.0  # K/μL
    hgb: float = 14.0  # g/dL
    hct: float = 42.0  # %
    platelets: float = 250.0  # K/μL
    reticulocyte: float = 1.0  # %
    d_dimer: float = 0.2  # μg/mL
    fibrinogen: float = 300.0  # mg/dL
    def update(self, patient_state: Dict[str, Any], time_delta: float) -> None:
        # Placeholder for hematology update logic
        pass


class PhysiologicalEngine:
    """advanced physiological engine coordinating all systems"""
    
    def __init__(self):
        self.cardiovascular = CardiovascularSystem()
        self.respiratory = RespiratorySystem()
        self.renal = RenalSystem()
        self.endocrine = EndocrineSystem()
        self.neurological = NeurologicalSystem()
        self.gastrointestinal = GastrointestinalSystem()
        self.hematology = HematologySystem()
        self.time_factor = 0.0  # cumulative time effect
        self.stress_level = 0.0  # current stress level
        self.disease_states = {}  # active disease states
        self.medication_history = []  # medication administration history
        self.physiological_alerts = []  # critical parameter alerts
        
    def update_systems(self, time_delta: float, events: List[Dict[str, Any]]) -> None:
        """update all physiological systems based on time and events"""
        self.time_factor += time_delta
        
        # process events that affect physiology
        for event in events:
            if event['type'] == 'medication_effect':
                self._apply_medication_effect(event['data'], time_delta)
            elif event['type'] == 'stress_change':
                self.stress_level = event['data'].get('stress_level', 0.0)
            elif event['type'] == 'disease_progression':
                self._apply_disease_effect(event['data'], time_delta)
            elif event['type'] == 'intervention':
                self._apply_intervention_effect(event['data'], time_delta)
        
        # update systems based on current state
        self.cardiovascular.update_from_stress(self.stress_level, time_delta)
        self.respiratory.update_from_stress(self.stress_level, time_delta)
        self.renal.update_from_stress(self.stress_level, time_delta)
        
        # update disease progression
        self._update_disease_progression(time_delta)
        
        # gradual recovery from stress
        if self.stress_level > 0:
            self.stress_level = max(0, self.stress_level - time_delta * 0.05)
        
        # check for critical alerts
        self._check_physiological_alerts()
        
        # Update new systems
        self.endocrine.update({}, time_delta)
        self.neurological.update({}, time_delta)
        self.gastrointestinal.update({}, time_delta)
        self.hematology.update({}, time_delta)
    
    def _apply_medication_effect(self, data: Dict[str, Any], time_delta: float) -> None:
        """apply medication effects to physiological systems"""
        medication = data.get('medication', '')
        dose = data.get('dose', 1.0)
        
        self.cardiovascular.update_from_medication(medication, dose, time_delta)
        self.respiratory.update_from_medication(medication, dose, time_delta)
        self.renal.update_from_medication(medication, dose, time_delta)
        
        # record medication administration
        self.medication_history.append({
            'medication': medication,
            'dose': dose,
            'time': self.time_factor,
            'effects': data.get('effects', {})
        })
    
    def _apply_disease_effect(self, data: Dict[str, Any], time_delta: float) -> None:
        """apply disease effects to physiological systems"""
        disease = data.get('disease', '')
        severity = data.get('severity', 1.0)
        
        # add to active disease states
        self.disease_states[disease] = {
            'severity': severity,
            'onset_time': self.time_factor,
            'progression_rate': data.get('progression_rate', 0.1)
        }
        
        self.cardiovascular.update_from_disease(disease, severity, time_delta)
        self.respiratory.update_from_disease(disease, severity, time_delta)
        self.renal.update_from_disease(disease, severity, time_delta)
    
    def _apply_intervention_effect(self, data: Dict[str, Any], time_delta: float) -> None:
        """apply intervention effects (procedures, etc.)"""
        intervention = data.get('intervention', '')
        
        if intervention.lower() == 'intubation':
            self.respiratory.respiratory_rate = 12.0
            self.respiratory.tidal_volume = 600.0
            self.respiratory.minute_ventilation = 7.2
            
        elif intervention.lower() == 'chest_compressions':
            self.cardiovascular.heart_rate = 100.0
            self.cardiovascular.blood_pressure_systolic = 80.0
            self.cardiovascular.cardiac_output = 2.0
            
        elif intervention.lower() == 'defibrillation':
            self.cardiovascular.heart_rate = 80.0
            self.cardiovascular.blood_pressure_systolic = 120.0
            self.stress_level = 0.0
    
    def _update_disease_progression(self, time_delta: float) -> None:
        """update disease progression over time"""
        for disease, state in list(self.disease_states.items()):
            # increase severity over time
            state['severity'] += state['progression_rate'] * time_delta
            
            # apply updated disease effects
            self.cardiovascular.update_from_disease(disease, state['severity'], time_delta)
            self.respiratory.update_from_disease(disease, state['severity'], time_delta)
            self.renal.update_from_disease(disease, state['severity'], time_delta)
            
            # check for resolution or critical progression
            if state['severity'] >= 1.0:
                # disease has reached maximum severity
                pass
            elif state['severity'] <= 0:
                # disease has resolved
                del self.disease_states[disease]
    
    def _check_physiological_alerts(self) -> None:
        """check for critical physiological parameters"""
        self.physiological_alerts.clear()
        
        # cardiovascular alerts
        if self.cardiovascular.heart_rate > 150:
            self.physiological_alerts.append("Tachycardia - Heart rate > 150 bpm")
        elif self.cardiovascular.heart_rate < 50:
            self.physiological_alerts.append("Bradycardia - Heart rate < 50 bpm")
            
        if self.cardiovascular.blood_pressure_systolic > 180:
            self.physiological_alerts.append("Hypertension - Systolic BP > 180 mmHg")
        elif self.cardiovascular.blood_pressure_systolic < 90:
            self.physiological_alerts.append("Hypotension - Systolic BP < 90 mmHg")
            
        if self.cardiovascular.ejection_fraction < 40:
            self.physiological_alerts.append("Reduced ejection fraction < 40%")
        
        # respiratory alerts
        if self.respiratory.oxygen_saturation < 90:
            self.physiological_alerts.append("Hypoxemia - SpO2 < 90%")
        elif self.respiratory.oxygen_saturation < 95:
            self.physiological_alerts.append("Mild hypoxemia - SpO2 < 95%")
            
        if self.respiratory.respiratory_rate > 30:
            self.physiological_alerts.append("Tachypnea - Respiratory rate > 30/min")
        elif self.respiratory.respiratory_rate < 8:
            self.physiological_alerts.append("Bradypnea - Respiratory rate < 8/min")
        
        # renal alerts
        if self.renal.gfr < 60:
            self.physiological_alerts.append("Reduced GFR < 60 ml/min/1.73m²")
        if self.renal.creatinine > 2.0:
            self.physiological_alerts.append("Elevated creatinine > 2.0 mg/dL")
        if self.renal.potassium > 5.5:
            self.physiological_alerts.append("Hyperkalemia - K+ > 5.5 mEq/L")
    
    def get_all_vital_signs(self) -> Dict[str, float]:
        """get vital signs from all systems"""
        vitals = {}
        vitals.update(self.cardiovascular.get_vital_signs())
        vitals.update(self.respiratory.get_vital_signs())
        return vitals
    
    def get_lab_values(self) -> Dict[str, float]:
        """get lab values from all systems"""
        labs = {}
        labs.update(self.renal.get_lab_values())
        return labs
    
    def get_advanced_parameters(self) -> Dict[str, Any]:
        """get advanced parameters from all systems"""
        return {
            'cardiovascular': self.cardiovascular.get_advanced_parameters(),
            'respiratory': self.respiratory.get_advanced_parameters(),
            'renal': self.renal.get_advanced_parameters()
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """get comprehensive system status"""
        return {
            'cardiovascular': {
                'heart_rate': self.cardiovascular.heart_rate,
                'blood_pressure': f"{self.cardiovascular.blood_pressure_systolic:.0f}/{self.cardiovascular.blood_pressure_diastolic:.0f}",
                'cardiac_output': self.cardiovascular.cardiac_output,
                'ejection_fraction': self.cardiovascular.ejection_fraction
            },
            'respiratory': {
                'respiratory_rate': self.respiratory.respiratory_rate,
                'oxygen_saturation': self.respiratory.oxygen_saturation,
                'minute_ventilation': self.respiratory.minute_ventilation,
                'peak_expiratory_flow': self.respiratory.peak_expiratory_flow
            },
            'renal': {
                'urine_output': self.renal.urine_output,
                'creatinine': self.renal.creatinine,
                'gfr': self.renal.gfr,
                'potassium': self.renal.potassium
            },
            'stress_level': self.stress_level,
            'time_factor': self.time_factor,
            'active_diseases': list(self.disease_states.keys()),
            'physiological_alerts': self.physiological_alerts.copy()
        }
    
    def get_medication_history(self) -> List[Dict[str, Any]]:
        """get medication administration history"""
        return self.medication_history.copy() 