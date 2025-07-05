"""
API type definitions for medical simulator
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class PatientStatus(Enum):
    """patient status enumeration"""
    STABLE = "stable"
    CRITICAL = "critical"
    IMPROVING = "improving"
    DETERIORATING = "deteriorating"
    DECEASED = "deceased"

class SimulationStatus(Enum):
    """simulation status enumeration"""
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"

class ActionType(Enum):
    """action type enumeration"""
    MEDICATION = "medication"
    PROCEDURE = "procedure"
    LAB_ORDER = "lab_order"
    IMAGING_ORDER = "imaging_order"
    DIALOGUE = "dialogue"
    EXAMINATION = "examination"
    VITAL_UPDATE = "vital_update"

@dataclass
class PatientInfo:
    """patient information structure"""
    id: str
    name: str
    age: int
    gender: str
    weight: float
    height: float
    allergies: List[str] = field(default_factory=list)
    medications: List[str] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)
    status: PatientStatus = PatientStatus.STABLE

@dataclass
class VitalSigns:
    """vital signs structure"""
    blood_pressure_systolic: int
    blood_pressure_diastolic: int
    heart_rate: int
    respiratory_rate: int
    temperature: float
    oxygen_saturation: int
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class LabResult:
    """lab result structure"""
    test_name: str
    value: float
    unit: str
    normal_range: tuple
    status: str
    timestamp: datetime = field(default_factory=datetime.now)
    critical: bool = False

@dataclass
class ImagingResult:
    """imaging result structure"""
    study_name: str
    modality: str
    findings: Dict[str, Any]
    clinical_impression: str
    critical_findings: bool = False
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Medication:
    """medication structure"""
    name: str
    dose: str
    route: str
    frequency: str
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    active: bool = True

@dataclass
class Procedure:
    """procedure structure"""
    name: str
    category: str
    success: bool
    complications: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class SimulationState:
    """simulation state structure"""
    status: SimulationStatus
    current_time: datetime
    elapsed_time: float
    patient: PatientInfo
    vitals: VitalSigns
    lab_results: List[LabResult] = field(default_factory=list)
    imaging_results: List[ImagingResult] = field(default_factory=list)
    medications: List[Medication] = field(default_factory=list)
    procedures: List[Procedure] = field(default_factory=list)
    actions: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class Action:
    """action structure"""
    type: ActionType
    name: str
    parameters: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = True
    result: Optional[Dict[str, Any]] = None

@dataclass
class Assessment:
    """assessment structure"""
    scenario_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    actions: List[Action] = field(default_factory=list)
    score: Optional[float] = None
    feedback: List[str] = field(default_factory=list)
    passed: Optional[bool] = None

@dataclass
class PluginInfo:
    """plugin information structure"""
    name: str
    version: str
    description: str
    author: str
    category: str
    enabled: bool
    config: Dict[str, Any] = field(default_factory=dict)

@dataclass
class APIResponse:
    """standard API response structure"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

# API request/response types
PatientUpdateRequest = Dict[str, Any]
VitalUpdateRequest = Dict[str, Any]
MedicationRequest = Dict[str, Any]
LabOrderRequest = Dict[str, Any]
ImagingOrderRequest = Dict[str, Any]
ProcedureRequest = Dict[str, Any]
DialogueRequest = Dict[str, Any]
ExaminationRequest = Dict[str, Any]

# API response types
PatientResponse = APIResponse
VitalsResponse = APIResponse
LabResponse = APIResponse
ImagingResponse = APIResponse
MedicationResponse = APIResponse
ProcedureResponse = APIResponse
DialogueResponse = APIResponse
ExaminationResponse = APIResponse
AssessmentResponse = APIResponse
PluginResponse = APIResponse 