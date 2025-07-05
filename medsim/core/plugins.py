"""
Plugin system for medical simulator
enables modular architecture for extensibility
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Type, Union
from dataclasses import dataclass, field
import importlib
import inspect
import os
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class PluginMetadata:
    """metadata for plugin registration"""
    name: str
    version: str
    description: str
    author: str
    category: str
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    config_schema: Optional[Dict[str, Any]] = None

class BasePlugin(ABC):
    """base class for all plugins"""
    
    def __init__(self, metadata: PluginMetadata, config: Optional[Dict[str, Any]] = None):
        self.metadata = metadata
        self.config = config or {}
        self.enabled = True
        self._validate_config()
    
    @abstractmethod
    def initialize(self) -> bool:
        """initialize the plugin"""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """cleanup plugin resources"""
        pass
    
    def _validate_config(self) -> None:
        """validate plugin configuration"""
        if self.metadata.config_schema:
            # basic schema validation
            for key, schema in self.metadata.config_schema.items():
                if key in self.config:
                    expected_type = schema.get("type")
                    if expected_type and not isinstance(self.config[key], expected_type):
                        raise ValueError(f"Invalid config for {key}: expected {expected_type}")
    
    def get_info(self) -> Dict[str, Any]:
        """get plugin information"""
        return {
            "name": self.metadata.name,
            "version": self.metadata.version,
            "description": self.metadata.description,
            "author": self.metadata.author,
            "category": self.metadata.category,
            "enabled": self.enabled,
            "config": self.config
        }

class SpecialtyPlugin(BasePlugin):
    """plugin for medical specialties"""
    
    def __init__(self, metadata: PluginMetadata, config: Optional[Dict[str, Any]] = None):
        super().__init__(metadata, config)
        self.scenarios: List[Dict[str, Any]] = []
        self.procedures: List[Dict[str, Any]] = []
        self.protocols: List[Dict[str, Any]] = []
        self.drugs: List[Dict[str, Any]] = []
        self.lab_tests: List[Dict[str, Any]] = []
        self.imaging_studies: List[Dict[str, Any]] = []
    
    def initialize(self) -> bool:
        """initialize specialty plugin"""
        try:
            self._load_specialty_content()
            logger.info(f"Specialty plugin '{self.metadata.name}' initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize specialty plugin '{self.metadata.name}': {e}")
            return False
    
    def cleanup(self) -> None:
        """cleanup specialty plugin"""
        self.scenarios.clear()
        self.procedures.clear()
        self.protocols.clear()
        self.drugs.clear()
        self.lab_tests.clear()
        self.imaging_studies.clear()
    
    def _load_specialty_content(self) -> None:
        """load specialty-specific content"""
        # this would be implemented by specific specialty plugins
        pass
    
    def get_scenarios(self) -> List[Dict[str, Any]]:
        """get specialty scenarios"""
        return self.scenarios.copy()
    
    def get_procedures(self) -> List[Dict[str, Any]]:
        """get specialty procedures"""
        return self.procedures.copy()
    
    def get_protocols(self) -> List[Dict[str, Any]]:
        """get specialty protocols"""
        return self.protocols.copy()
    
    def get_drugs(self) -> List[Dict[str, Any]]:
        """get specialty drugs"""
        return self.drugs.copy()
    
    def get_lab_tests(self) -> List[Dict[str, Any]]:
        """get specialty lab tests"""
        return self.lab_tests.copy()
    
    def get_imaging_studies(self) -> List[Dict[str, Any]]:
        """get specialty imaging studies"""
        return self.imaging_studies.copy()

class DrugPlugin(BasePlugin):
    """plugin for drug databases"""
    
    def __init__(self, metadata: PluginMetadata, config: Optional[Dict[str, Any]] = None):
        super().__init__(metadata, config)
        self.drugs: Dict[str, Dict[str, Any]] = {}
    
    def initialize(self) -> bool:
        """initialize drug plugin"""
        try:
            self._load_drug_database()
            logger.info(f"Drug plugin '{self.metadata.name}' initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize drug plugin '{self.metadata.name}': {e}")
            return False
    
    def cleanup(self) -> None:
        """cleanup drug plugin"""
        self.drugs.clear()
    
    def _load_drug_database(self) -> None:
        """load drug database"""
        # this would be implemented by specific drug plugins
        pass
    
    def get_drug(self, drug_name: str) -> Optional[Dict[str, Any]]:
        """get drug information"""
        return self.drugs.get(drug_name)
    
    def search_drugs(self, query: str) -> List[Dict[str, Any]]:
        """search drugs by name or indication"""
        results = []
        query_lower = query.lower()
        
        for drug_name, drug_info in self.drugs.items():
            if (query_lower in drug_name.lower() or 
                query_lower in drug_info.get("indications", "").lower() or
                query_lower in drug_info.get("class", "").lower()):
                results.append(drug_info)
        
        return results
    
    def get_all_drugs(self) -> List[Dict[str, Any]]:
        """get all drugs"""
        return list(self.drugs.values())

class ScenarioPlugin(BasePlugin):
    """plugin for scenario databases"""
    
    def __init__(self, metadata: PluginMetadata, config: Optional[Dict[str, Any]] = None):
        super().__init__(metadata, config)
        self.scenarios: Dict[str, Dict[str, Any]] = {}
    
    def initialize(self) -> bool:
        """initialize scenario plugin"""
        try:
            self._load_scenarios()
            logger.info(f"Scenario plugin '{self.metadata.name}' initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize scenario plugin '{self.metadata.name}': {e}")
            return False
    
    def cleanup(self) -> None:
        """cleanup scenario plugin"""
        self.scenarios.clear()
    
    def _load_scenarios(self) -> None:
        """load scenarios"""
        # this would be implemented by specific scenario plugins
        pass
    
    def get_scenario(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        """get scenario by id"""
        return self.scenarios.get(scenario_id)
    
    def search_scenarios(self, query: str) -> List[Dict[str, Any]]:
        """search scenarios by title or description"""
        results = []
        query_lower = query.lower()
        
        for scenario_id, scenario in self.scenarios.items():
            if (query_lower in scenario.get("title", "").lower() or
                query_lower in scenario.get("description", "").lower() or
                query_lower in scenario.get("specialty", "").lower()):
                results.append(scenario)
        
        return results
    
    def get_scenarios_by_specialty(self, specialty: str) -> List[Dict[str, Any]]:
        """get scenarios by specialty"""
        return [s for s in self.scenarios.values() if s.get("specialty") == specialty]
    
    def get_all_scenarios(self) -> List[Dict[str, Any]]:
        """get all scenarios"""
        return list(self.scenarios.values())

class PhysiologicalPlugin(BasePlugin):
    """plugin for physiological models"""
    
    def __init__(self, metadata: PluginMetadata, config: Optional[Dict[str, Any]] = None):
        super().__init__(metadata, config)
        self.systems: Dict[str, Any] = {}
    
    def initialize(self) -> bool:
        """initialize physiological plugin"""
        try:
            self._load_physiological_models()
            logger.info(f"Physiological plugin '{self.metadata.name}' initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize physiological plugin '{self.metadata.name}': {e}")
            return False
    
    def cleanup(self) -> None:
        """cleanup physiological plugin"""
        self.systems.clear()
    
    def _load_physiological_models(self) -> None:
        """load physiological models"""
        # this would be implemented by specific physiological plugins
        pass
    
    def update_system(self, system_name: str, patient_state: Any, delta_time: float) -> None:
        """update physiological system"""
        if system_name in self.systems:
            self.systems[system_name].update(patient_state, delta_time)
    
    def get_system_parameters(self, system_name: str) -> Dict[str, Any]:
        """get system parameters"""
        if system_name in self.systems:
            return self.systems[system_name].get_parameters()
        return {}
    
    def get_all_systems(self) -> List[str]:
        """get all available systems"""
        return list(self.systems.keys())

class PluginRegistry:
    """central plugin registry"""
    
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}
        self.plugin_types: Dict[str, Type[BasePlugin]] = {
            "specialty": SpecialtyPlugin,
            "drug": DrugPlugin,
            "scenario": ScenarioPlugin,
            "physiological": PhysiologicalPlugin
        }
    
    def register_plugin(self, plugin: BasePlugin) -> bool:
        """register a plugin"""
        try:
            plugin_id = f"{plugin.metadata.category}.{plugin.metadata.name}"
            if plugin_id in self.plugins:
                logger.warning(f"Plugin {plugin_id} already registered, overwriting")
            
            self.plugins[plugin_id] = plugin
            logger.info(f"Registered plugin: {plugin_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to register plugin: {e}")
            return False
    
    def unregister_plugin(self, plugin_id: str) -> bool:
        """unregister a plugin"""
        if plugin_id in self.plugins:
            plugin = self.plugins[plugin_id]
            plugin.cleanup()
            del self.plugins[plugin_id]
            logger.info(f"Unregistered plugin: {plugin_id}")
            return True
        return False
    
    def get_plugin(self, plugin_id: str) -> Optional[BasePlugin]:
        """get plugin by id"""
        return self.plugins.get(plugin_id)
    
    def get_plugins_by_category(self, category: str) -> List[BasePlugin]:
        """get plugins by category"""
        return [p for p in self.plugins.values() if p.metadata.category == category]
    
    def get_all_plugins(self) -> List[BasePlugin]:
        """get all plugins"""
        return list(self.plugins.values())
    
    def initialize_plugins(self) -> None:
        """initialize all plugins"""
        for plugin in self.plugins.values():
            if plugin.enabled:
                plugin.initialize()
    
    def cleanup_plugins(self) -> None:
        """cleanup all plugins"""
        for plugin in self.plugins.values():
            plugin.cleanup()
    
    def load_plugins_from_directory(self, plugin_dir: str) -> None:
        """load plugins from directory"""
        plugin_path = Path(plugin_dir)
        if not plugin_path.exists():
            logger.warning(f"Plugin directory does not exist: {plugin_dir}")
            return
        
        for plugin_file in plugin_path.glob("*.py"):
            if plugin_file.name.startswith("__"):
                continue
            
            try:
                module_name = plugin_file.stem
                spec = importlib.util.spec_from_file_location(module_name, plugin_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # look for plugin classes
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, BasePlugin) and 
                        obj != BasePlugin):
                        # instantiate plugin
                        plugin = obj()
                        self.register_plugin(plugin)
                        
            except Exception as e:
                logger.error(f"Failed to load plugin from {plugin_file}: {e}")
    
    def get_plugin_info(self) -> List[Dict[str, Any]]:
        """get information about all plugins"""
        return [plugin.get_info() for plugin in self.plugins.values()]

# global plugin registry
plugin_registry = PluginRegistry() 