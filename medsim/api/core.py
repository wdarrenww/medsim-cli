"""
Core API for medical simulator
provides programmatic access to simulator functionality
"""

from typing import Dict, List, Any, Optional, Union
import json
import logging
from datetime import datetime
from pathlib import Path

from ..core.simulation import MedicalSimulation
from ..core.session import PatientState
from ..core.plugins import plugin_registry
from .types import *

logger = logging.getLogger(__name__)

class MedicalSimulatorAPI:
    """main API class for medical simulator"""
    
    def __init__(self):
        self.simulation: Optional[MedicalSimulation] = None
        self.session_id: Optional[str] = None
        self._action_history: List[Action] = []
    
    def start_simulation(self, scenario_id: Optional[str] = None) -> APIResponse:
        """start a new simulation session"""
        try:
            self.simulation = MedicalSimulation()
            if scenario_id:
                self.simulation.load_scenario(scenario_id)
            else:
                self.simulation.start()
            
            self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            logger.info(f"Started simulation session: {self.session_id}")
            
            return APIResponse(
                success=True,
                data={"session_id": self.session_id},
                message="Simulation started successfully"
            )
        except Exception as e:
            logger.error(f"Failed to start simulation: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message="Failed to start simulation"
            )
    
    def get_simulation_state(self) -> APIResponse:
        """get current simulation state"""
        if not self.simulation:
            return APIResponse(
                success=False,
                error="No active simulation",
                message="No simulation is currently running"
            )
        
        try:
            patient_state = self.simulation.patient_state
            
            # convert to API types
            patient_info = PatientInfo(
                id=patient_state.patient_id,
                name=patient_state.name,
                age=patient_state.age,
                gender=patient_state.gender,
                weight=patient_state.weight,
                height=patient_state.height,
                allergies=patient_state.allergies,
                medications=[med["name"] for med in patient_state.medications],
                conditions=patient_state.conditions,
                status=PatientStatus.STABLE  # would be determined by vitals
            )
            
            vitals = VitalSigns(
                blood_pressure_systolic=patient_state.vitals["blood_pressure_systolic"],
                blood_pressure_diastolic=patient_state.vitals["blood_pressure_diastolic"],
                heart_rate=patient_state.vitals["heart_rate"],
                respiratory_rate=patient_state.vitals["respiratory_rate"],
                temperature=patient_state.vitals["temperature"],
                oxygen_saturation=patient_state.vitals["oxygen_saturation"]
            )
            
            # convert lab results
            lab_results = []
            for test_name, result in patient_state.lab_results.items():
                lab_results.append(LabResult(
                    test_name=test_name,
                    value=result["value"],
                    unit=result.get("unit", ""),
                    normal_range=result.get("normal_range", (0, 0)),
                    status=result.get("status", "normal"),
                    critical=result.get("critical", False)
                ))
            
            # convert imaging results
            imaging_results = []
            for study_name, result in patient_state.imaging_results.items():
                imaging_results.append(ImagingResult(
                    study_name=study_name,
                    modality=result.get("modality", ""),
                    findings=result.get("findings", {}),
                    clinical_impression=result.get("clinical_impression", ""),
                    critical_findings=result.get("critical_findings", False)
                ))
            
            # convert medications
            medications = []
            for med in patient_state.medications:
                medications.append(Medication(
                    name=med["name"],
                    dose=med["dose"],
                    route=med["route"],
                    frequency=med["frequency"]
                ))
            
            simulation_state = SimulationState(
                status=SimulationStatus.RUNNING if self.simulation.running else SimulationStatus.PAUSED,
                current_time=datetime.fromtimestamp(self.simulation.current_time),
                elapsed_time=self.simulation.current_time,
                patient=patient_info,
                vitals=vitals,
                lab_results=lab_results,
                imaging_results=imaging_results,
                medications=medications
            )
            
            return APIResponse(
                success=True,
                data=simulation_state,
                message="Simulation state retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Failed to get simulation state: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message="Failed to get simulation state"
            )
    
    def update_vitals(self, vitals_data: VitalUpdateRequest) -> VitalsResponse:
        """update patient vital signs"""
        if not self.simulation:
            return APIResponse(
                success=False,
                error="No active simulation",
                message="No simulation is currently running"
            )
        
        try:
            # validate vitals data
            required_vitals = ["blood_pressure_systolic", "blood_pressure_diastolic", 
                             "heart_rate", "respiratory_rate", "temperature", "oxygen_saturation"]
            
            for vital in required_vitals:
                if vital not in vitals_data:
                    return APIResponse(
                        success=False,
                        error=f"Missing required vital: {vital}",
                        message="All vital signs are required"
                    )
            
            # update vitals
            self.simulation.patient_state.vitals.update(vitals_data)
            
            # record action
            action = Action(
                type=ActionType.VITAL_UPDATE,
                name="Update Vitals",
                parameters=vitals_data
            )
            self._action_history.append(action)
            
            return APIResponse(
                success=True,
                data=vitals_data,
                message="Vital signs updated successfully"
            )
        except Exception as e:
            logger.error(f"Failed to update vitals: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message="Failed to update vital signs"
            )
    
    def order_lab_test(self, test_name: str) -> LabResponse:
        """order a lab test"""
        if not self.simulation:
            return APIResponse(
                success=False,
                error="No active simulation",
                message="No simulation is currently running"
            )
        
        try:
            result = self.simulation.diagnostics.order_lab_test(test_name)
            
            # record action
            action = Action(
                type=ActionType.LAB_ORDER,
                name=f"Order Lab Test: {test_name}",
                parameters={"test_name": test_name},
                result=result
            )
            self._action_history.append(action)
            
            return APIResponse(
                success=True,
                data=result,
                message=f"Lab test '{test_name}' ordered successfully"
            )
        except Exception as e:
            logger.error(f"Failed to order lab test: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message=f"Failed to order lab test '{test_name}'"
            )
    
    def order_imaging_study(self, study_name: str) -> ImagingResponse:
        """order an imaging study"""
        if not self.simulation:
            return APIResponse(
                success=False,
                error="No active simulation",
                message="No simulation is currently running"
            )
        
        try:
            result = self.simulation.diagnostics.order_imaging_study(study_name)
            
            # record action
            action = Action(
                type=ActionType.IMAGING_ORDER,
                name=f"Order Imaging: {study_name}",
                parameters={"study_name": study_name},
                result=result
            )
            self._action_history.append(action)
            
            return APIResponse(
                success=True,
                data=result,
                message=f"Imaging study '{study_name}' ordered successfully"
            )
        except Exception as e:
            logger.error(f"Failed to order imaging study: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message=f"Failed to order imaging study '{study_name}'"
            )
    
    def administer_medication(self, medication_data: MedicationRequest) -> MedicationResponse:
        """administer medication to patient"""
        if not self.simulation:
            return APIResponse(
                success=False,
                error="No active simulation",
                message="No simulation is currently running"
            )
        
        try:
            result = self.simulation.treatments.administer_medication(
                medication_data["name"],
                medication_data["dose"],
                medication_data["route"]
            )
            
            # record action
            action = Action(
                type=ActionType.MEDICATION,
                name=f"Administer Medication: {medication_data['name']}",
                parameters=medication_data,
                result=result
            )
            self._action_history.append(action)
            
            return APIResponse(
                success=True,
                data=result,
                message=f"Medication '{medication_data['name']}' administered successfully"
            )
        except Exception as e:
            logger.error(f"Failed to administer medication: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message=f"Failed to administer medication '{medication_data['name']}'"
            )
    
    def perform_procedure(self, procedure_data: ProcedureRequest) -> ProcedureResponse:
        """perform a clinical procedure"""
        if not self.simulation:
            return APIResponse(
                success=False,
                error="No active simulation",
                message="No simulation is currently running"
            )
        
        try:
            result = self.simulation.procedures.perform_procedure(
                procedure_data["name"],
                procedure_data.get("parameters", {})
            )
            
            # record action
            action = Action(
                type=ActionType.PROCEDURE,
                name=f"Perform Procedure: {procedure_data['name']}",
                parameters=procedure_data,
                result=result
            )
            self._action_history.append(action)
            
            return APIResponse(
                success=True,
                data=result,
                message=f"Procedure '{procedure_data['name']}' performed successfully"
            )
        except Exception as e:
            logger.error(f"Failed to perform procedure: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message=f"Failed to perform procedure '{procedure_data['name']}'"
            )
    
    def start_dialogue(self, message: str) -> DialogueResponse:
        """start patient dialogue"""
        if not self.simulation:
            return APIResponse(
                success=False,
                error="No active simulation",
                message="No simulation is currently running"
            )
        
        try:
            response = self.simulation.dialogue.get_response(message)
            
            # record action
            action = Action(
                type=ActionType.DIALOGUE,
                name="Patient Dialogue",
                parameters={"message": message},
                result={"response": response}
            )
            self._action_history.append(action)
            
            return APIResponse(
                success=True,
                data={"response": response},
                message="Dialogue response generated successfully"
            )
        except Exception as e:
            logger.error(f"Failed to start dialogue: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message="Failed to generate dialogue response"
            )
    
    def perform_examination(self, examination_data: ExaminationRequest) -> ExaminationResponse:
        """perform physical examination"""
        if not self.simulation:
            return APIResponse(
                success=False,
                error="No active simulation",
                message="No simulation is currently running"
            )
        
        try:
            result = self.simulation.perform_examination(
                examination_data["system"],
                examination_data.get("findings", {})
            )
            
            # record action
            action = Action(
                type=ActionType.EXAMINATION,
                name=f"Physical Examination: {examination_data['system']}",
                parameters=examination_data,
                result=result
            )
            self._action_history.append(action)
            
            return APIResponse(
                success=True,
                data=result,
                message=f"Examination of {examination_data['system']} completed successfully"
            )
        except Exception as e:
            logger.error(f"Failed to perform examination: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message=f"Failed to perform examination of {examination_data['system']}"
            )
    
    def step_simulation(self, steps: int = 1) -> APIResponse:
        """advance simulation by specified number of steps"""
        if not self.simulation:
            return APIResponse(
                success=False,
                error="No active simulation",
                message="No simulation is currently running"
            )
        
        try:
            for _ in range(steps):
                self.simulation.step()
            
            return APIResponse(
                success=True,
                data={"steps_completed": steps},
                message=f"Simulation advanced by {steps} step(s)"
            )
        except Exception as e:
            logger.error(f"Failed to step simulation: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message="Failed to advance simulation"
            )
    
    def get_assessment(self) -> AssessmentResponse:
        """get performance assessment"""
        if not self.simulation:
            return APIResponse(
                success=False,
                error="No active simulation",
                message="No simulation is currently running"
            )
        
        try:
            assessment = Assessment(
                scenario_id=self.simulation.scenario_id if hasattr(self.simulation, 'scenario_id') else "unknown",
                start_time=datetime.fromtimestamp(self.simulation.start_time),
                actions=self._action_history,
                score=self.simulation.get_score() if hasattr(self.simulation, 'get_score') else None,
                feedback=self.simulation.get_feedback() if hasattr(self.simulation, 'get_feedback') else [],
                passed=self.simulation.passed if hasattr(self.simulation, 'passed') else None
            )
            
            return APIResponse(
                success=True,
                data=assessment,
                message="Assessment retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Failed to get assessment: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message="Failed to get assessment"
            )
    
    def get_plugins(self) -> PluginResponse:
        """get information about loaded plugins"""
        try:
            plugin_info = plugin_registry.get_plugin_info()
            return APIResponse(
                success=True,
                data=plugin_info,
                message="Plugin information retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Failed to get plugins: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message="Failed to get plugin information"
            )
    
    def save_session(self, filename: str) -> APIResponse:
        """save current simulation session"""
        if not self.simulation:
            return APIResponse(
                success=False,
                error="No active simulation",
                message="No simulation is currently running"
            )
        
        try:
            self.simulation.save_session(filename)
            return APIResponse(
                success=True,
                data={"filename": filename},
                message="Session saved successfully"
            )
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message="Failed to save session"
            )
    
    def load_session(self, filename: str) -> APIResponse:
        """load simulation session from file"""
        try:
            self.simulation = MedicalSimulation()
            self.simulation.load_session(filename)
            return APIResponse(
                success=True,
                data={"filename": filename},
                message="Session loaded successfully"
            )
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message="Failed to load session"
            )
    
    def stop_simulation(self) -> APIResponse:
        """stop current simulation"""
        if not self.simulation:
            return APIResponse(
                success=False,
                error="No active simulation",
                message="No simulation is currently running"
            )
        
        try:
            self.simulation.stop()
            return APIResponse(
                success=True,
                message="Simulation stopped successfully"
            )
        except Exception as e:
            logger.error(f"Failed to stop simulation: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                message="Failed to stop simulation"
            )
    
    def list_plugins(self) -> PluginResponse:
        """list all loaded plugins"""
        try:
            plugins = plugin_registry.get_plugin_info()
            return APIResponse(success=True, data=plugins, message="Plugins listed successfully")
        except Exception as e:
            return APIResponse(success=False, error=str(e), message="Failed to list plugins")

    def load_plugin(self, path: str) -> PluginResponse:
        """load a plugin from a file path"""
        try:
            plugin_registry.load_plugins_from_directory(str(Path(path).parent))
            return APIResponse(success=True, message=f"Plugin(s) loaded from {path}")
        except Exception as e:
            return APIResponse(success=False, error=str(e), message="Failed to load plugin")

    def unload_plugin(self, plugin_id: str) -> PluginResponse:
        """unload a plugin by id"""
        try:
            result = plugin_registry.unregister_plugin(plugin_id)
            if result:
                return APIResponse(success=True, message=f"Plugin {plugin_id} unloaded")
            else:
                return APIResponse(success=False, error="Plugin not found", message="Plugin not found")
        except Exception as e:
            return APIResponse(success=False, error=str(e), message="Failed to unload plugin")

    def enable_plugin(self, plugin_id: str) -> PluginResponse:
        """enable a plugin by id"""
        try:
            plugin = plugin_registry.get_plugin(plugin_id)
            if plugin:
                plugin.enabled = True
                return APIResponse(success=True, message=f"Plugin {plugin_id} enabled")
            else:
                return APIResponse(success=False, error="Plugin not found", message="Plugin not found")
        except Exception as e:
            return APIResponse(success=False, error=str(e), message="Failed to enable plugin")

    def disable_plugin(self, plugin_id: str) -> PluginResponse:
        """disable a plugin by id"""
        try:
            plugin = plugin_registry.get_plugin(plugin_id)
            if plugin:
                plugin.enabled = False
                return APIResponse(success=True, message=f"Plugin {plugin_id} disabled")
            else:
                return APIResponse(success=False, error="Plugin not found", message="Plugin not found")
        except Exception as e:
            return APIResponse(success=False, error=str(e), message="Failed to disable plugin")

    def get_plugin_info(self, plugin_id: str) -> PluginResponse:
        """get info for a specific plugin"""
        try:
            plugin = plugin_registry.get_plugin(plugin_id)
            if plugin:
                return APIResponse(success=True, data=plugin.get_info(), message="Plugin info retrieved")
            else:
                return APIResponse(success=False, error="Plugin not found", message="Plugin not found")
        except Exception as e:
            return APIResponse(success=False, error=str(e), message="Failed to get plugin info")

    def get_plugin_content(self, plugin_id: str, content_type: str) -> PluginResponse:
        """get content from a plugin (scenarios, drugs, etc)"""
        try:
            plugin = plugin_registry.get_plugin(plugin_id)
            if not plugin:
                return APIResponse(success=False, error="Plugin not found", message="Plugin not found")
            if hasattr(plugin, f'get_{content_type}'):
                content = getattr(plugin, f'get_{content_type}')()
                return APIResponse(success=True, data=content, message=f"{content_type} retrieved from plugin")
            else:
                return APIResponse(success=False, error="Content type not found", message="Content type not found")
        except Exception as e:
            return APIResponse(success=False, error=str(e), message="Failed to get plugin content") 