"""
real-time monitoring and trending system for drug levels and clinical parameters
"""

import time
import threading
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import statistics
from enum import Enum

from .drug_db import DrugPKPD
from .pharmacology import DrugAdministration
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DrugLevel:
    """drug level data for monitoring"""
    drug_name: str
    concentration: float
    therapeutic_min: float
    therapeutic_max: float
    toxic_threshold: float
    status: str  # therapeutic, subtherapeutic, toxic
    timestamp: datetime = field(default_factory=datetime.now)


class AlertLevel(Enum):
    """alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class TrendPoint:
    """single data point for trending"""
    timestamp: datetime
    value: float
    unit: str
    source: str  # drug name, vital sign, etc.


@dataclass
class TrendData:
    """trending data for a parameter"""
    parameter: str
    unit: str
    data_points: deque = field(default_factory=lambda: deque(maxlen=100))
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    current_value: Optional[float] = None
    trend_direction: str = "stable"  # increasing, decreasing, stable
    trend_strength: float = 0.0  # -1.0 to 1.0
    
    def add_point(self, value: float, timestamp: Optional[datetime] = None):
        """add a new data point"""
        if timestamp is None:
            timestamp = datetime.now()
        
        point = TrendPoint(timestamp, value, self.unit, self.parameter)
        self.data_points.append(point)
        
        # update statistics
        self.current_value = value
        if self.min_value is None or value < self.min_value:
            self.min_value = value
        if self.max_value is None or value > self.max_value:
            self.max_value = value
        
        # calculate trend
        self._calculate_trend()
    
    def _calculate_trend(self):
        """calculate trend direction and strength"""
        if len(self.data_points) < 3:
            return
        
        # get recent values (last 10 points or all if fewer)
        recent_points = list(self.data_points)[-min(10, len(self.data_points)):]
        values = [p.value for p in recent_points]
        
        if len(values) < 3:
            return
        
        # calculate linear regression slope
        n = len(values)
        x_values = list(range(n))
        x_mean = sum(x_values) / n
        y_mean = sum(values) / n
        
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        if denominator == 0:
            self.trend_direction = "stable"
            self.trend_strength = 0.0
            return
        
        slope = numerator / denominator
        
        # normalize slope to -1 to 1 range
        max_slope = max(abs(max(values) - min(values)), 1.0)
        normalized_slope = slope / max_slope
        
        if normalized_slope > 0.1:
            self.trend_direction = "increasing"
            self.trend_strength = min(normalized_slope, 1.0)
        elif normalized_slope < -0.1:
            self.trend_direction = "decreasing"
            self.trend_strength = min(abs(normalized_slope), 1.0)
        else:
            self.trend_direction = "stable"
            self.trend_strength = 0.0
    
    def get_recent_data(self, minutes: int = 60) -> List[TrendPoint]:
        """get data points from last N minutes"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        return [p for p in self.data_points if p.timestamp >= cutoff]
    
    def get_statistics(self) -> Dict[str, Any]:
        """get statistical summary"""
        if not self.data_points:
            return {}
        
        values = [p.value for p in self.data_points]
        return {
            "current": self.current_value,
            "min": self.min_value,
            "max": self.max_value,
            "mean": statistics.mean(values),
            "std": statistics.stdev(values) if len(values) > 1 else 0,
            "trend": self.trend_direction,
            "trend_strength": self.trend_strength,
            "data_points": len(self.data_points)
        }


@dataclass
class Alert:
    """clinical alert"""
    id: str
    level: AlertLevel
    message: str
    parameter: str
    value: float
    unit: str
    timestamp: datetime
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None


class MonitoringSystem:
    """real-time monitoring and trending system"""
    
    def __init__(self):
        self.trends: Dict[str, TrendData] = {}
        self.alerts: List[Alert] = []
        self.monitoring_active = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.alert_callbacks: List[callable] = []
        
        # monitoring intervals (seconds)
        self.drug_level_interval = 30
        self.vital_signs_interval = 60
        self.lab_values_interval = 300
        
        # alert thresholds
        self.alert_thresholds = {
            "heart_rate": {"low": 50, "high": 120},
            "blood_pressure_systolic": {"low": 90, "high": 180},
            "blood_pressure_diastolic": {"low": 60, "high": 110},
            "temperature": {"low": 35.0, "high": 38.5},
            "oxygen_saturation": {"low": 92, "high": 100},
            "respiratory_rate": {"low": 12, "high": 25},
            "glucose": {"low": 70, "high": 200},
            "potassium": {"low": 3.5, "high": 5.5},
            "sodium": {"low": 135, "high": 145},
            "creatinine": {"low": 0.6, "high": 1.2},
        }
    
    def start_monitoring(self):
        """start real-time monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """stop real-time monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def _monitor_loop(self):
        """main monitoring loop"""
        while self.monitoring_active:
            try:
                # monitor drug levels
                self._monitor_drug_levels()
                
                # monitor vital signs
                self._monitor_vital_signs()
                
                # monitor lab values
                self._monitor_lab_values()
                
                # sleep before next cycle
                time.sleep(10)  # check every 10 seconds
                
            except Exception as e:
                print(f"monitoring error: {e}")
                time.sleep(30)  # wait longer on error
    
    def _monitor_drug_levels(self):
        """monitor drug levels and effects"""
        # this would integrate with the drug system
        # for now, we'll use placeholder data
        pass
    
    def _monitor_vital_signs(self):
        """monitor vital signs for alerts"""
        # this would integrate with the physiological system
        # for now, we'll use placeholder data
        pass
    
    def _monitor_lab_values(self):
        """monitor lab values for alerts"""
        # this would integrate with the diagnostic system
        # for now, we'll use placeholder data
        pass
    
    def add_trend_data(self, parameter: str, value: float, unit: str):
        """add data point for trending"""
        if parameter not in self.trends:
            self.trends[parameter] = TrendData(parameter, unit)
        
        self.trends[parameter].add_point(value)
        
        # check for alerts
        self._check_alerts(parameter, value, unit)
    
    def _check_alerts(self, parameter: str, value: float, unit: str):
        """check if value triggers alerts"""
        if parameter not in self.alert_thresholds:
            return
        
        thresholds = self.alert_thresholds[parameter]
        
        # check low threshold
        if "low" in thresholds and value < thresholds["low"]:
            self._create_alert(
                f"{parameter}_low",
                AlertLevel.WARNING if value > thresholds["low"] * 0.8 else AlertLevel.CRITICAL,
                f"{parameter} is low: {value} {unit}",
                parameter, value, unit
            )
        
        # check high threshold
        if "high" in thresholds and value > thresholds["high"]:
            self._create_alert(
                f"{parameter}_high",
                AlertLevel.WARNING if value < thresholds["high"] * 1.2 else AlertLevel.CRITICAL,
                f"{parameter} is high: {value} {unit}",
                parameter, value, unit
            )
    
    def _create_alert(self, alert_id: str, level: AlertLevel, message: str, 
                     parameter: str, value: float, unit: str):
        """create a new alert"""
        # check if alert already exists
        for alert in self.alerts:
            if alert.id == alert_id and not alert.acknowledged:
                return  # alert already exists
        
        alert = Alert(
            id=alert_id,
            level=level,
            message=message,
            parameter=parameter,
            value=value,
            unit=unit,
            timestamp=datetime.now()
        )
        
        self.alerts.append(alert)
        
        # notify callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"alert callback error: {e}")
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str):
        """acknowledge an alert"""
        for alert in self.alerts:
            if alert.id == alert_id and not alert.acknowledged:
                alert.acknowledged = True
                alert.acknowledged_by = acknowledged_by
                alert.acknowledged_at = datetime.now()
                break
    
    def get_active_alerts(self) -> List[Alert]:
        """get unacknowledged alerts"""
        return [alert for alert in self.alerts if not alert.acknowledged]
    
    def get_trend_data(self, parameter: str) -> Optional[TrendData]:
        """get trend data for parameter"""
        return self.trends.get(parameter)
    
    def get_all_trends(self) -> Dict[str, TrendData]:
        """get all trend data"""
        return self.trends.copy()
    
    def clear_old_data(self, hours: int = 24):
        """clear data older than specified hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        for trend in self.trends.values():
            # remove old data points
            trend.data_points = deque(
                [p for p in trend.data_points if p.timestamp >= cutoff],
                maxlen=100
            )
        
        # remove old alerts
        self.alerts = [alert for alert in self.alerts if alert.timestamp >= cutoff]
    
    def add_alert_callback(self, callback: callable):
        """add callback for new alerts"""
        self.alert_callbacks.append(callback)
    
    def get_monitoring_summary(self) -> Dict[str, Any]:
        """get monitoring system summary"""
        active_alerts = self.get_active_alerts()
        
        return {
            "monitoring_active": self.monitoring_active,
            "active_alerts": len(active_alerts),
            "total_trends": len(self.trends),
            "total_alerts": len(self.alerts),
            "trends": {
                param: trend.get_statistics() 
                for param, trend in self.trends.items()
            }
        }


class DrugLevelMonitor:
    """specialized monitor for drug levels and effects"""
    
    def __init__(self, monitoring_system: MonitoringSystem):
        self.monitoring = monitoring_system
        self.drug_levels: Dict[str, List[DrugLevel]] = {}
        self.effect_monitors: Dict[str, Dict[str, float]] = {}
    
    def add_drug_level(self, drug_name: str, level: DrugLevel):
        """add drug level data"""
        if drug_name not in self.drug_levels:
            self.drug_levels[drug_name] = []
        
        self.drug_levels[drug_name].append(level)
        
        # add to trending
        self.monitoring.add_trend_data(
            f"{drug_name}_level",
            level.concentration,
            "mg/L"
        )
        
        # check therapeutic/toxic ranges
        self._check_drug_alerts(drug_name, level)
    
    def _check_drug_alerts(self, drug_name: str, level: DrugLevel):
        """check drug level alerts"""
        # therapeutic range alerts
        if level.concentration < level.therapeutic_min:
            self.monitoring._create_alert(
                f"{drug_name}_subtherapeutic",
                AlertLevel.WARNING,
                f"{drug_name} level is subtherapeutic: {level.concentration:.2f} mg/L",
                f"{drug_name}_level", level.concentration, "mg/L"
            )
        
        if level.concentration > level.toxic_threshold:
            self.monitoring._create_alert(
                f"{drug_name}_toxic",
                AlertLevel.CRITICAL,
                f"{drug_name} level is toxic: {level.concentration:.2f} mg/L",
                f"{drug_name}_level", level.concentration, "mg/L"
            )
    
    def add_effect_data(self, drug_name: str, effect: str, value: float):
        """add drug effect data"""
        if drug_name not in self.effect_monitors:
            self.effect_monitors[drug_name] = {}
        
        self.effect_monitors[drug_name][effect] = value
        
        # add to trending
        self.monitoring.add_trend_data(
            f"{drug_name}_{effect}",
            value,
            "effect_units"
        )
    
    def get_drug_summary(self, drug_name: str) -> Dict[str, Any]:
        """get drug monitoring summary"""
        if drug_name not in self.drug_levels:
            return {}
        
        levels = self.drug_levels[drug_name]
        if not levels:
            return {}
        
        current_level = levels[-1]
        effects = self.effect_monitors.get(drug_name, {})
        
        return {
            "current_level": current_level.concentration,
            "therapeutic_range": f"{current_level.therapeutic_min}-{current_level.therapeutic_max}",
            "toxic_threshold": current_level.toxic_threshold,
            "status": current_level.status,
            "effects": effects,
            "trend": self.monitoring.get_trend_data(f"{drug_name}_level")
        }
    
    def get_all_drug_summaries(self) -> Dict[str, Dict[str, Any]]:
        """get summaries for all monitored drugs"""
        return {
            drug_name: self.get_drug_summary(drug_name)
            for drug_name in self.drug_levels.keys()
        } 