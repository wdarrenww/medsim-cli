"""
performance assessment and evaluation system
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class PerformanceMetrics:
    """represents performance metrics for a scenario"""
    scenario_id: str
    user_actions: List[str]
    correct_diagnosis: str
    user_diagnosis: Optional[str]
    optimal_actions: List[str]
    completed_actions: List[str]
    time_taken: float  # minutes
    time_limit: float  # minutes
    points_earned: int
    points_possible: int
    overall_score: float  # percentage
    performance_level: str  # pass/fail or optimal/suboptimal


class AssessmentSystem:
    """manages performance assessment and evaluation"""
    
    def __init__(self):
        self.current_assessment: Optional[PerformanceMetrics] = None
        self.assessment_history: List[PerformanceMetrics] = []
        
    def start_assessment(self, scenario_id: str, correct_diagnosis: str, 
                        optimal_actions: List[str], time_limit: float, 
                        points_possible: int) -> None:
        """start a new performance assessment"""
        self.current_assessment = PerformanceMetrics(
            scenario_id=scenario_id,
            user_actions=[],
            correct_diagnosis=correct_diagnosis,
            user_diagnosis=None,
            optimal_actions=optimal_actions,
            completed_actions=[],
            time_taken=0.0,
            time_limit=time_limit,
            points_earned=0,
            points_possible=points_possible,
            overall_score=0.0,
            performance_level="incomplete"
        )
    
    def record_action(self, action: str) -> None:
        """record a user action"""
        if self.current_assessment:
            self.current_assessment.user_actions.append(action)
    
    def record_diagnosis(self, diagnosis: str) -> None:
        """record user's diagnosis"""
        if self.current_assessment:
            self.current_assessment.user_diagnosis = diagnosis
    
    def complete_assessment(self, time_taken: float) -> Dict[str, Any]:
        """complete the assessment and calculate performance"""
        if not self.current_assessment:
            return {}
        
        self.current_assessment.time_taken = time_taken
        
        # calculate performance metrics
        self._calculate_performance()
        
        # create assessment summary
        summary = self._create_assessment_summary()
        
        # add to history
        self.assessment_history.append(self.current_assessment)
        
        return summary
    
    def _calculate_performance(self) -> None:
        """calculate performance metrics"""
        if not self.current_assessment:
            return
        
        # calculate diagnostic accuracy
        diagnostic_correct = (self.current_assessment.user_diagnosis and 
                            self.current_assessment.user_diagnosis.lower() == 
                            self.current_assessment.correct_diagnosis.lower())
        
        # calculate action completion
        completed_optimal_actions = []
        for action in self.current_assessment.user_actions:
            if action.lower() in [opt.lower() for opt in self.current_assessment.optimal_actions]:
                completed_optimal_actions.append(action)
        
        self.current_assessment.completed_actions = completed_optimal_actions
        
        # calculate points
        points = 0
        
        # diagnostic points (30% of total)
        if diagnostic_correct:
            points += int(self.current_assessment.points_possible * 0.3)
        
        # action points (70% of total)
        action_completion_rate = len(completed_optimal_actions) / len(self.current_assessment.optimal_actions)
        points += int(self.current_assessment.points_possible * 0.7 * action_completion_rate)
        
        # time bonus/penalty
        time_efficiency = min(1.0, self.current_assessment.time_limit / self.current_assessment.time_taken)
        if time_efficiency > 0.8:  # completed in 80% of time or less
            points += int(self.current_assessment.points_possible * 0.1)
        
        self.current_assessment.points_earned = min(points, self.current_assessment.points_possible)
        
        # calculate overall score
        self.current_assessment.overall_score = (self.current_assessment.points_earned / 
                                               self.current_assessment.points_possible) * 100
        
        # determine performance level
        if self.current_assessment.overall_score >= 80:
            self.current_assessment.performance_level = "optimal"
        elif self.current_assessment.overall_score >= 60:
            self.current_assessment.performance_level = "suboptimal"
        else:
            self.current_assessment.performance_level = "fail"
    
    def _create_assessment_summary(self) -> Dict[str, Any]:
        """create a comprehensive assessment summary"""
        if not self.current_assessment:
            return {}
        
        # categorize actions
        optimal_actions_completed = self.current_assessment.completed_actions
        optimal_actions_missed = [action for action in self.current_assessment.optimal_actions 
                                if action.lower() not in [comp.lower() for comp in optimal_actions_completed]]
        non_optimal_actions = [action for action in self.current_assessment.user_actions 
                             if action.lower() not in [opt.lower() for opt in self.current_assessment.optimal_actions]]
        
        # diagnostic accuracy
        diagnostic_correct = (self.current_assessment.user_diagnosis and 
                            self.current_assessment.user_diagnosis.lower() == 
                            self.current_assessment.correct_diagnosis.lower())
        
        # time efficiency
        time_efficiency = min(1.0, self.current_assessment.time_limit / self.current_assessment.time_taken)
        
        summary = {
            'scenario_id': self.current_assessment.scenario_id,
            'performance_level': self.current_assessment.performance_level,
            'overall_score': self.current_assessment.overall_score,
            'points_earned': self.current_assessment.points_earned,
            'points_possible': self.current_assessment.points_possible,
            
            # diagnostic assessment
            'diagnostic_correct': diagnostic_correct,
            'correct_diagnosis': self.current_assessment.correct_diagnosis,
            'user_diagnosis': self.current_assessment.user_diagnosis,
            
            # action assessment
            'optimal_actions_completed': optimal_actions_completed,
            'optimal_actions_missed': optimal_actions_missed,
            'non_optimal_actions': non_optimal_actions,
            'action_completion_rate': len(optimal_actions_completed) / len(self.current_assessment.optimal_actions),
            
            # time assessment
            'time_taken': self.current_assessment.time_taken,
            'time_limit': self.current_assessment.time_limit,
            'time_efficiency': time_efficiency,
            
            # detailed breakdown
            'all_user_actions': self.current_assessment.user_actions,
            'all_optimal_actions': self.current_assessment.optimal_actions,
            
            # recommendations
            'recommendations': self._generate_recommendations(),
            
            'timestamp': datetime.now().isoformat()
        }
        
        return summary
    
    def _generate_recommendations(self) -> List[str]:
        """generate performance recommendations"""
        if not self.current_assessment:
            return []
        
        recommendations = []
        
        # diagnostic recommendations
        if not self.current_assessment.user_diagnosis:
            recommendations.append("Consider making a diagnosis based on clinical findings.")
        elif self.current_assessment.user_diagnosis.lower() != self.current_assessment.correct_diagnosis.lower():
            recommendations.append(f"Review the clinical presentation. The correct diagnosis was: {self.current_assessment.correct_diagnosis}")
        
        # action recommendations
        completed_rate = len(self.current_assessment.completed_actions) / len(self.current_assessment.optimal_actions)
        if completed_rate < 0.5:
            recommendations.append("Focus on completing essential clinical actions in future scenarios.")
        elif completed_rate < 0.8:
            recommendations.append("Good progress, but consider completing more optimal actions.")
        
        # time recommendations
        time_efficiency = min(1.0, self.current_assessment.time_limit / self.current_assessment.time_taken)
        if time_efficiency < 0.5:
            recommendations.append("Work on improving time management in clinical scenarios.")
        elif time_efficiency < 0.8:
            recommendations.append("Consider working more efficiently while maintaining quality.")
        
        # specific missed actions
        missed_actions = [action for action in self.current_assessment.optimal_actions 
                         if action.lower() not in [comp.lower() for comp in self.current_assessment.completed_actions]]
        if missed_actions:
            recommendations.append(f"Consider these actions in similar scenarios: {', '.join(missed_actions[:3])}")
        
        return recommendations
    
    def get_assessment_history(self) -> List[Dict[str, Any]]:
        """get assessment history"""
        return [
            {
                'scenario_id': assessment.scenario_id,
                'performance_level': assessment.performance_level,
                'overall_score': assessment.overall_score,
                'time_taken': assessment.time_taken,
                'timestamp': datetime.now().isoformat()
            }
            for assessment in self.assessment_history
        ]
    
    def get_performance_statistics(self) -> Dict[str, Any]:
        """get overall performance statistics"""
        if not self.assessment_history:
            return {}
        
        total_scenarios = len(self.assessment_history)
        optimal_count = sum(1 for a in self.assessment_history if a.performance_level == "optimal")
        suboptimal_count = sum(1 for a in self.assessment_history if a.performance_level == "suboptimal")
        fail_count = sum(1 for a in self.assessment_history if a.performance_level == "fail")
        
        avg_score = sum(a.overall_score for a in self.assessment_history) / total_scenarios
        avg_time = sum(a.time_taken for a in self.assessment_history) / total_scenarios
        
        return {
            'total_scenarios': total_scenarios,
            'optimal_performance': optimal_count,
            'suboptimal_performance': suboptimal_count,
            'failed_scenarios': fail_count,
            'average_score': avg_score,
            'average_time': avg_time,
            'success_rate': (optimal_count + suboptimal_count) / total_scenarios
        } 