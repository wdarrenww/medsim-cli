"""
comprehensive user interface for intervention management
provides easy access to interventions, organ systems, and adverse effects
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

from .intervention_manager import (
    InterventionManager, InterventionType, OrganSystem, AdverseEventType,
    InterventionDefinition, InterventionOrder
)
from .patient_state_evolution import PatientStateEvolutionEngine, PatientState

@dataclass
class InterventionRequest:
    """user request for an intervention"""
    intervention_name: str
    parameters: Optional[Dict[str, Any]] = None
    delay_minutes: int = 0
    priority: int = 2
    provider: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class InterventionResponse:
    """response to intervention request"""
    success: bool
    order: Optional[InterventionOrder] = None
    message: str = ""
    warnings: List[str] = None
    contraindications: List[str] = None

class InterventionInterface:
    """comprehensive user interface for intervention management"""
    
    def __init__(self):
        self.intervention_manager = InterventionManager()
        self.state_engine = PatientStateEvolutionEngine()
        self.current_patient_state: Optional[PatientState] = None
    
    def set_patient_state(self, patient_state: PatientState):
        """set the current patient state for intervention planning"""
        self.current_patient_state = patient_state
    
    def get_available_interventions(self, organ_system: Optional[str] = None) -> Dict[str, Any]:
        """get available interventions, optionally filtered by organ system"""
        if organ_system:
            organ_enum = OrganSystem(organ_system)
            interventions = self.intervention_manager.get_available_interventions(organ_enum)
        else:
            interventions = self.intervention_manager.get_available_interventions()
        
        result = {}
        for intervention_name in interventions:
            definition = self.intervention_manager.get_intervention_info(intervention_name)
            if definition:
                result[intervention_name] = {
                    "name": definition.name,
                    "type": definition.type.value,
                    "target_organs": [organ.value for organ in definition.target_organs],
                    "duration_minutes": definition.duration_minutes,
                    "success_rate": definition.success_rate,
                    "adverse_event_risk": definition.adverse_event_risk,
                    "contraindications": definition.contraindications,
                    "parameters": definition.parameters,
                    "description": definition.description
                }
        
        return result
    
    def get_intervention_categories(self) -> Dict[str, List[str]]:
        """get interventions organized by category"""
        categories = {}
        for intervention_type in InterventionType:
            interventions = self.intervention_manager.get_orders_by_type(intervention_type)
            categories[intervention_type.value] = [order.name for order in interventions]
        
        return categories
    
    def get_organ_system_interventions(self) -> Dict[str, List[str]]:
        """get interventions organized by target organ system"""
        organ_interventions = {}
        for organ_system in OrganSystem:
            interventions = self.intervention_manager.get_available_interventions(organ_system)
            organ_interventions[organ_system.value] = interventions
        
        return organ_interventions
    
    def request_intervention(self, request: InterventionRequest) -> InterventionResponse:
        """request an intervention with comprehensive validation"""
        # validate intervention exists
        definition = self.intervention_manager.get_intervention_info(request.intervention_name)
        if not definition:
            return InterventionResponse(
                success=False,
                message=f"unknown intervention: {request.intervention_name}"
            )
        
        # check contraindications
        contraindications = self._check_contraindications(request, definition)
        if contraindications:
            return InterventionResponse(
                success=False,
                message="contraindications detected",
                contraindications=contraindications
            )
        
        # check warnings
        warnings = self._check_warnings(request, definition)
        
        # create order
        try:
            order = self.intervention_manager.order_intervention(
                intervention_name=request.intervention_name,
                parameters=request.parameters,
                delay_minutes=request.delay_minutes,
                priority=request.priority,
                provider=request.provider
            )
            
            if request.notes:
                order.notes.append(request.notes)
            
            return InterventionResponse(
                success=True,
                order=order,
                message="intervention ordered successfully",
                warnings=warnings
            )
        
        except Exception as e:
            return InterventionResponse(
                success=False,
                message=f"failed to order intervention: {str(e)}"
            )
    
    def _check_contraindications(self, request: InterventionRequest, definition: InterventionDefinition) -> List[str]:
        """check for contraindications based on patient state and intervention"""
        contraindications = []
        
        if not self.current_patient_state:
            return contraindications
        
        # check organ system function
        for organ in definition.target_organs:
            organ_state = self.current_patient_state.organ_systems.get(organ.value)
            if organ_state and organ_state.function_score < 0.3:
                contraindications.append(f"severe_{organ.value}_dysfunction")
        
        # check vital signs
        vitals = self.current_patient_state.vitals
        if "arrhythmia" in definition.contraindications and vitals.heart_rate > 150:
            contraindications.append("tachyarrhythmia")
        if "respiratory_failure" in definition.contraindications and vitals.oxygen_saturation < 85:
            contraindications.append("respiratory_failure")
        if "shock" in definition.contraindications and vitals.bp_systolic < 80:
            contraindications.append("shock")
        
        # check for allergies
        if "allergy" in definition.contraindications:
            # this would typically check against patient allergy list
            pass
        
        return contraindications
    
    def _check_warnings(self, request: InterventionRequest, definition: InterventionDefinition) -> List[str]:
        """check for warnings based on patient state and intervention"""
        warnings = []
        
        if not self.current_patient_state:
            return warnings
        
        # check organ system function
        for organ in definition.target_organs:
            organ_state = self.current_patient_state.organ_systems.get(organ.value)
            if organ_state and organ_state.function_score < 0.6:
                warnings.append(f"moderate_{organ.value}_dysfunction")
        
        # check for existing adverse events
        if self.current_patient_state.adverse_events:
            warnings.append("patient_has_existing_adverse_events")
        
        return warnings
    
    def execute_interventions(self, current_time: datetime) -> List[InterventionOrder]:
        """execute all due interventions"""
        return self.intervention_manager.execute_due_interventions(current_time)
    
    def get_active_orders(self) -> List[Dict[str, Any]]:
        """get all active orders with detailed information"""
        orders = self.intervention_manager.get_active_orders()
        return [self._order_to_dict(order) for order in orders]
    
    def get_completed_orders(self) -> List[Dict[str, Any]]:
        """get all completed orders with results"""
        orders = self.intervention_manager.get_completed_orders()
        return [self._order_to_dict(order) for order in orders]
    
    def get_failed_orders(self) -> List[Dict[str, Any]]:
        """get all failed orders"""
        orders = self.intervention_manager.get_failed_orders()
        return [self._order_to_dict(order) for order in orders]
    
    def _order_to_dict(self, order: InterventionOrder) -> Dict[str, Any]:
        """convert order to dictionary for easy serialization"""
        return {
            "order_id": order.order_id,
            "name": order.name,
            "type": order.type.value,
            "target_organs": [organ.value for organ in order.target_organs],
            "parameters": order.parameters,
            "ordered_time": order.ordered_time.isoformat(),
            "scheduled_time": order.scheduled_time.isoformat() if order.scheduled_time else None,
            "executed_time": order.executed_time.isoformat() if order.executed_time else None,
            "completed_time": order.completed_time.isoformat() if order.completed_time else None,
            "status": order.status,
            "result": order.result,
            "adverse_events": [event.value for event in order.adverse_events],
            "notes": order.notes,
            "provider": order.provider,
            "priority": order.priority
        }
    
    def cancel_order(self, order_id: str) -> bool:
        """cancel an order"""
        return self.intervention_manager.cancel_order(order_id)
    
    def get_orders_by_organ(self, organ_system: str) -> List[Dict[str, Any]]:
        """get orders targeting a specific organ system"""
        organ_enum = OrganSystem(organ_system)
        orders = self.intervention_manager.get_orders_by_organ(organ_enum)
        return [self._order_to_dict(order) for order in orders]
    
    def get_orders_by_type(self, intervention_type: str) -> List[Dict[str, Any]]:
        """get orders of a specific type"""
        type_enum = InterventionType(intervention_type)
        orders = self.intervention_manager.get_orders_by_type(type_enum)
        return [self._order_to_dict(order) for order in orders]
    
    def get_orders_by_priority(self, priority: int) -> List[Dict[str, Any]]:
        """get orders with a specific priority level"""
        orders = self.intervention_manager.get_orders_by_priority(priority)
        return [self._order_to_dict(order) for order in orders]
    
    def get_adverse_events_summary(self) -> Dict[str, int]:
        """get summary of all adverse events"""
        summary = self.intervention_manager.get_adverse_events_summary()
        return {event.value: count for event, count in summary.items()}
    
    def get_orders_summary(self) -> Dict[str, Any]:
        """get comprehensive summary of all orders"""
        return self.intervention_manager.export_orders_summary()
    
    def get_patient_intervention_recommendations(self) -> List[Dict[str, Any]]:
        """get intervention recommendations based on patient state"""
        if not self.current_patient_state:
            return []
        
        recommendations = []
        
        # analyze organ system dysfunction
        for system_name, organ_state in self.current_patient_state.organ_systems.items():
            if organ_state.function_score < 0.7:
                interventions = self.intervention_manager.get_available_interventions(OrganSystem(system_name))
                for intervention_name in interventions:
                    definition = self.intervention_manager.get_intervention_info(intervention_name)
                    if definition and definition.type in [InterventionType.MEDICATION, InterventionType.SUPPORTIVE]:
                        recommendations.append({
                            "intervention": intervention_name,
                            "reason": f"{system_name}_dysfunction",
                            "severity": "moderate" if organ_state.function_score > 0.5 else "severe",
                            "priority": 3 if organ_state.function_score < 0.5 else 2
                        })
        
        # analyze vital signs
        vitals = self.current_patient_state.vitals
        if vitals.oxygen_saturation < 90:
            recommendations.append({
                "intervention": "oxygen_therapy",
                "reason": "hypoxemia",
                "severity": "severe" if vitals.oxygen_saturation < 85 else "moderate",
                "priority": 4 if vitals.oxygen_saturation < 85 else 3
            })
        
        if vitals.bp_systolic < 90:
            recommendations.append({
                "intervention": "vasopressor",
                "reason": "hypotension",
                "severity": "severe" if vitals.bp_systolic < 80 else "moderate",
                "priority": 4 if vitals.bp_systolic < 80 else 3
            })
        
        if vitals.heart_rate > 120:
            recommendations.append({
                "intervention": "ecg_monitoring",
                "reason": "tachycardia",
                "severity": "moderate",
                "priority": 3
            })
        
        # analyze symptoms
        for symptom in self.current_patient_state.symptoms:
            if "pain" in symptom:
                recommendations.append({
                    "intervention": "sedative",
                    "reason": "pain_management",
                    "severity": "moderate",
                    "priority": 2
                })
            elif "fever" in symptom:
                recommendations.append({
                    "intervention": "antibiotic",
                    "reason": "infection_treatment",
                    "severity": "moderate",
                    "priority": 3
                })
        
        return recommendations
    
    def get_intervention_effectiveness_report(self) -> Dict[str, Any]:
        """get report on intervention effectiveness"""
        completed_orders = self.intervention_manager.get_completed_orders()
        
        effectiveness_data = {}
        for order in completed_orders:
            if order.name not in effectiveness_data:
                effectiveness_data[order.name] = {
                    "total_orders": 0,
                    "successful_orders": 0,
                    "failed_orders": 0,
                    "adverse_events": 0,
                    "avg_duration": 0
                }
            
            data = effectiveness_data[order.name]
            data["total_orders"] += 1
            
            if order.status == "completed":
                data["successful_orders"] += 1
            else:
                data["failed_orders"] += 1
            
            data["adverse_events"] += len(order.adverse_events)
            
            if order.executed_time and order.completed_time:
                duration = (order.completed_time - order.executed_time).total_seconds() / 60
                data["avg_duration"] = (data["avg_duration"] * (data["total_orders"] - 1) + duration) / data["total_orders"]
        
        # calculate success rates
        for intervention_name, data in effectiveness_data.items():
            if data["total_orders"] > 0:
                data["success_rate"] = data["successful_orders"] / data["total_orders"]
                data["adverse_event_rate"] = data["adverse_events"] / data["total_orders"]
        
        return effectiveness_data
    
    def export_intervention_data(self) -> Dict[str, Any]:
        """export comprehensive intervention data"""
        return {
            "orders_summary": self.get_orders_summary(),
            "active_orders": self.get_active_orders(),
            "completed_orders": self.get_completed_orders(),
            "failed_orders": self.get_failed_orders(),
            "adverse_events": self.get_adverse_events_summary(),
            "effectiveness_report": self.get_intervention_effectiveness_report(),
            "recommendations": self.get_patient_intervention_recommendations(),
            "available_interventions": self.get_available_interventions(),
            "organ_system_interventions": self.get_organ_system_interventions(),
            "intervention_categories": self.get_intervention_categories()
        }
    
    def get_quick_intervention_menu(self) -> Dict[str, List[Dict[str, Any]]]:
        """get quick access menu for common interventions"""
        menu = {
            "emergency": [
                {"name": "cpr", "description": "cardiopulmonary resuscitation", "priority": 4},
                {"name": "defibrillation", "description": "cardiac defibrillation", "priority": 4},
                {"name": "emergency_intubation", "description": "emergency airway management", "priority": 4},
                {"name": "vasopressor", "description": "blood pressure support", "priority": 4}
            ],
            "medications": [
                {"name": "antibiotic", "description": "infection treatment", "priority": 3},
                {"name": "sedative", "description": "sedation and pain control", "priority": 2},
                {"name": "insulin", "description": "blood glucose control", "priority": 3},
                {"name": "diuretic", "description": "fluid management", "priority": 2},
                {"name": "anticoagulant", "description": "blood clot prevention", "priority": 3}
            ],
            "procedures": [
                {"name": "intubation", "description": "airway management", "priority": 3},
                {"name": "central_line", "description": "vascular access", "priority": 3},
                {"name": "chest_tube", "description": "chest drainage", "priority": 3},
                {"name": "dialysis", "description": "renal replacement therapy", "priority": 3}
            ],
            "laboratory": [
                {"name": "cbc", "description": "complete blood count", "priority": 2},
                {"name": "chemistry", "description": "basic metabolic panel", "priority": 2},
                {"name": "troponin", "description": "cardiac enzyme", "priority": 3},
                {"name": "arterial_blood_gas", "description": "acid-base status", "priority": 3}
            ],
            "imaging": [
                {"name": "chest_xray", "description": "chest radiograph", "priority": 2},
                {"name": "ct_chest", "description": "chest computed tomography", "priority": 3},
                {"name": "ct_head", "description": "head computed tomography", "priority": 3},
                {"name": "echocardiogram", "description": "cardiac ultrasound", "priority": 2}
            ],
            "supportive": [
                {"name": "oxygen_therapy", "description": "oxygen supplementation", "priority": 2},
                {"name": "mechanical_ventilation", "description": "respiratory support", "priority": 3},
                {"name": "iv_fluids", "description": "intravenous fluids", "priority": 2},
                {"name": "blood_transfusion", "description": "blood product administration", "priority": 3}
            ],
            "monitoring": [
                {"name": "ecg_monitoring", "description": "cardiac monitoring", "priority": 2},
                {"name": "pulse_oximetry", "description": "oxygen saturation monitoring", "priority": 2},
                {"name": "arterial_line", "description": "invasive blood pressure monitoring", "priority": 3}
            ]
        }
        
        return menu 