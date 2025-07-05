"""
dynamic scenario generator for medsim: generates patient scenarios using clinical patterns and real data
"""

import random
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging

from medsim.data.clinical_patterns import ClinicalPatterns
from medsim.data.pattern_analyzer import PatternAnalyzer
from medsim.data.dataset_loader import ClinicalRecord

logger = logging.getLogger(__name__)

@dataclass
class DynamicScenarioConfig:
    specialty: Optional[str] = None
    difficulty: Optional[str] = None
    pattern_type: Optional[str] = None
    variety: float = 1.0  # 0 = deterministic, 1 = max variety
    adaptive: bool = True
    user_performance: Optional[Dict[str, float]] = None
    seed: Optional[int] = None
    # add more config as needed

class DynamicScenarioGenerator:
    """generates scenarios programmatically using clinical patterns and real data distributions"""
    def __init__(self, patterns: Optional[ClinicalPatterns] = None, config: Optional[DynamicScenarioConfig] = None):
        self.patterns = patterns or ClinicalPatterns()
        self.config = config or DynamicScenarioConfig()
        if self.config.seed is not None:
            random.seed(self.config.seed)

    def generate_scenario(self, config: Optional[DynamicScenarioConfig] = None) -> Dict[str, Any]:
        """generate a single scenario based on config and patterns"""
        cfg = config or self.config
        pattern = self.patterns.get_random_pattern(specialty=cfg.specialty, difficulty=cfg.difficulty)
        scenario = self.patterns.generate_scenario_from_pattern(
            pattern,
            user_performance=cfg.user_performance if cfg.adaptive else None
        )
        scenario['generation_config'] = cfg.__dict__
        scenario['generated_at'] = datetime.now().isoformat()
        return scenario

    def generate_looped_scenarios(self, n: int = 10, config: Optional[DynamicScenarioConfig] = None) -> List[Dict[str, Any]]:
        """generate a looped sequence of scenarios for continuous simulation"""
        cfg = config or self.config
        scenarios = []
        for i in range(n):
            # optionally adapt difficulty based on simulated user performance
            if cfg.adaptive and cfg.user_performance:
                # simple adaptation: increase difficulty if performance is high
                avg_perf = sum(cfg.user_performance.values()) / len(cfg.user_performance)
                if avg_perf > 0.8:
                    cfg.difficulty = 'hard'
                elif avg_perf < 0.5:
                    cfg.difficulty = 'easy'
                else:
                    cfg.difficulty = 'medium'
            scenario = self.generate_scenario(cfg)
            scenario['loop_index'] = i
            scenarios.append(scenario)
        return scenarios

    def set_config(self, config: DynamicScenarioConfig):
        self.config = config

    def update_user_performance(self, user_performance: Dict[str, float]):
        self.config.user_performance = user_performance

    def get_available_specialties(self) -> List[str]:
        return list(self.patterns.pattern_library.keys())

    def get_available_difficulties(self) -> List[str]:
        # scan all patterns for difficulties
        difficulties = set()
        for specialty in self.patterns.pattern_library.values():
            for pattern in specialty.values():
                for diag in pattern.get('diagnoses', []):
                    difficulties.add(diag.get('difficulty', 'medium'))
        return sorted(list(difficulties)) 