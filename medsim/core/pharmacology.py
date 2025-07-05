"""
PK/PD Engine and Drug Data Model
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
import math
import random

@dataclass
class DrugPKPD:
    name: str
    class_: str
    route: str
    dose: float
    units: str
    half_life: float
    volume_of_distribution: float
    clearance: float
    absorption: float  # fraction absorbed (0-1)
    protein_binding: float  # fraction (0-1)
    metabolism: str
    elimination: str
    onset: float  # min
    peak: float  # min
    duration: float  # min
    mechanism: str
    effect_targets: List[str]
    effect_curve: Callable[[float], float]  # function of concentration
    side_effects: List[str]
    interactions: List[str]
    contraindications: List[str]
    monitoring: List[str]
    pediatric_dose: Optional[float] = None
    geriatric_dose: Optional[float] = None
    notes: Optional[str] = None

@dataclass
class DrugAdministration:
    drug: DrugPKPD
    start_time: float
    dose: float
    route: str
    patient_weight: float
    concentration: float = 0.0
    last_update: float = 0.0
    completed: bool = False
    adverse_events: List[str] = field(default_factory=list)

    def update_concentration(self, current_time: float):
        """simulate PK: update concentration based on time, dose, and PK parameters"""
        elapsed = current_time - self.last_update
        if elapsed <= 0:
            return self.concentration
        # simple 1-compartment model: C = (Dose/Vd) * e^(-kt)
        k = math.log(2) / self.drug.half_life
        if self.last_update == self.start_time:
            # initial absorption
            absorbed = self.dose * self.drug.absorption
            self.concentration = absorbed / self.drug.volume_of_distribution
        else:
            self.concentration *= math.exp(-k * elapsed)
        self.last_update = current_time
        return self.concentration

    def is_active(self, current_time: float):
        return not self.completed and (current_time - self.start_time) < self.drug.duration

class PKPDEngine:
    def __init__(self, drug_db: Dict[str, DrugPKPD]):
        self.drug_db = drug_db
        self.active_drugs: List[DrugAdministration] = []
        self.current_time: float = 0.0
        self.adverse_events: List[str] = []

    def administer_drug(self, name: str, dose: float, route: str, patient_weight: float):
        drug = self.drug_db.get(name.lower())
        if not drug:
            raise ValueError(f"Drug '{name}' not found in database.")
        admin = DrugAdministration(
            drug=drug,
            start_time=self.current_time,
            dose=dose,
            route=route,
            patient_weight=patient_weight,
            last_update=self.current_time
        )
        self.active_drugs.append(admin)
        return admin

    def update(self, dt: float, physiological_engine):
        self.current_time += dt
        for admin in self.active_drugs:
            if not admin.is_active(self.current_time):
                admin.completed = True
                continue
            conc = admin.update_concentration(self.current_time)
            # apply PD effect to physiological engine
            for target in admin.drug.effect_targets:
                effect = admin.drug.effect_curve(conc)
                self._apply_effect(target, effect, physiological_engine)
            # check for side effects
            self._check_adverse_events(admin, physiological_engine)

    def _apply_effect(self, target: str, effect: float, phys):
        # map effect targets to physiological parameters
        # e.g., 'heart_rate', 'blood_pressure_systolic', etc.
        if hasattr(phys.cardiovascular, target):
            setattr(phys.cardiovascular, target, getattr(phys.cardiovascular, target) + effect)
        elif hasattr(phys.respiratory, target):
            setattr(phys.respiratory, target, getattr(phys.respiratory, target) + effect)
        elif hasattr(phys.renal, target):
            setattr(phys.renal, target, getattr(phys.renal, target) + effect)
        elif hasattr(phys.endocrine, target):
            setattr(phys.endocrine, target, getattr(phys.endocrine, target) + effect)
        elif hasattr(phys.neurological, target):
            setattr(phys.neurological, target, getattr(phys.neurological, target) + effect)
        elif hasattr(phys.gastrointestinal, target):
            setattr(phys.gastrointestinal, target, getattr(phys.gastrointestinal, target) + effect)
        elif hasattr(phys.hematological, target):
            setattr(phys.hematological, target, getattr(phys.hematological, target) + effect)
        elif hasattr(phys.immune, target):
            setattr(phys.immune, target, getattr(phys.immune, target) + effect)
        elif hasattr(phys.hepatic, target):
            setattr(phys.hepatic, target, getattr(phys.hepatic, target) + effect)
        elif hasattr(phys.musculoskeletal, target):
            setattr(phys.musculoskeletal, target, getattr(phys.musculoskeletal, target) + effect)
        # add more as needed

    def _check_adverse_events(self, admin: DrugAdministration, phys):
        # simple example: if concentration > threshold, trigger side effect
        for se in admin.drug.side_effects:
            if random.random() < 0.01:  # placeholder probability
                admin.adverse_events.append(se)
                self.adverse_events.append(f"{admin.drug.name}: {se}")

    def get_active_drugs(self):
        return [a for a in self.active_drugs if not a.completed]

    def get_adverse_events(self):
        return self.adverse_events 