"""
Medical Simulator API
provides programmatic access to simulator functionality
"""

from .core import MedicalSimulatorAPI
from .types import *

__version__ = "1.0.0"
__all__ = ["MedicalSimulatorAPI"]

class MedicalSimulatorAPI:
    def get_physiological_status(self) -> dict:
        """get status of all organ systems"""
        return self.sim.simulation.physiological_engine.get_system_status()
    def get_system_detail(self, system: str) -> dict:
        """get detailed parameters for a specific organ system"""
        status = self.sim.simulation.physiological_engine.get_system_status()
        return status.get(system.lower(), {}) 