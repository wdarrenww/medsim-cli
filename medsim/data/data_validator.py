"""
data validator for ensuring clinical data quality and structure
"""

import json
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
import logging
from pathlib import Path

from .dataset_loader import ClinicalRecord

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """result of data validation"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    quality_score: float = 0.0
    completeness_score: float = 0.0
    consistency_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DataQualityMetrics:
    """metrics for data quality assessment"""
    total_records: int
    valid_records: int
    completeness_rate: float
    consistency_rate: float
    anomaly_rate: float
    duplicate_rate: float
    missing_fields: Dict[str, int]
    invalid_values: Dict[str, int]
    field_distributions: Dict[str, Dict[str, int]]


class DataValidator:
    """validates clinical datasets for quality and structure"""
    
    def __init__(self):
        self.required_fields = {
            'demographics': ['age', 'gender'],
            'presentation': ['chief_complaint', 'symptoms'],
            'diagnosis': ['primary'],
            'treatment': ['medications'],
            'outcome': ['disposition']
        }
        
        self.field_constraints = {
            'age': {'min': 0, 'max': 120, 'type': 'integer'},
            'gender': {'values': ['male', 'female', 'other'], 'type': 'categorical'},
            'heart_rate': {'min': 30, 'max': 250, 'type': 'numeric'},
            'bp_systolic': {'min': 60, 'max': 250, 'type': 'numeric'},
            'bp_diastolic': {'min': 40, 'max': 150, 'type': 'numeric'},
            'respiratory_rate': {'min': 8, 'max': 50, 'type': 'numeric'},
            'temperature': {'min': 90, 'max': 110, 'type': 'numeric'},
            'oxygen_saturation': {'min': 70, 'max': 100, 'type': 'numeric'}
        }
        
        self.anonymization_fields = [
            'patient_id', 'name', 'address', 'phone', 'ssn', 'medical_record_number'
        ]
    
    def validate_dataset(self, records: List[ClinicalRecord]) -> ValidationResult:
        """perform comprehensive dataset validation"""
        if not records:
            return ValidationResult(
                is_valid=False,
                errors=["No records provided for validation"],
                quality_score=0.0
            )
        
        result = ValidationResult(is_valid=False)
        
        # perform various validation checks
        self._validate_structure(records, result)
        self._validate_completeness(records, result)
        self._validate_consistency(records, result)
        self._validate_anonymization(records, result)
        self._validate_anomalies(records, result)
        self._validate_duplicates(records, result)
        
        # calculate quality scores
        result.quality_score = self._calculate_quality_score(result)
        result.completeness_score = self._calculate_completeness_score(records)
        result.consistency_score = self._calculate_consistency_score(records)
        
        # determine overall validity
        result.is_valid = len(result.errors) == 0 and result.quality_score >= 0.7
        
        return result
    
    def _validate_structure(self, records: List[ClinicalRecord], result: ValidationResult):
        """validate data structure and required fields"""
        for i, record in enumerate(records):
            # check required fields exist
            for section, required in self.required_fields.items():
                section_data = getattr(record, section, {})
                for field in required:
                    if field not in section_data or not section_data[field]:
                        result.errors.append(
                            f"Record {i}: Missing required field '{field}' in {section}"
                        )
            
            # check data types
            if hasattr(record, 'demographics') and record.demographics:
                age = record.demographics.get('age')
                if age is not None and not isinstance(age, (int, float)):
                    result.errors.append(f"Record {i}: Age must be numeric, got {type(age)}")
    
    def _validate_completeness(self, records: List[ClinicalRecord], result: ValidationResult):
        """validate data completeness"""
        total_fields = 0
        filled_fields = 0
        
        for i, record in enumerate(records):
            # check demographics completeness
            demographics = getattr(record, 'demographics', {})
            for field in ['age', 'gender', 'race', 'ethnicity']:
                total_fields += 1
                if demographics.get(field):
                    filled_fields += 1
                else:
                    result.warnings.append(f"Record {i}: Missing demographic field '{field}'")
            
            # check presentation completeness
            presentation = getattr(record, 'presentation', {})
            for field in ['chief_complaint', 'symptoms', 'vital_signs']:
                total_fields += 1
                if presentation.get(field):
                    filled_fields += 1
                else:
                    result.warnings.append(f"Record {i}: Missing presentation field '{field}'")
            
            # check diagnosis completeness
            diagnosis = getattr(record, 'diagnosis', {})
            total_fields += 1
            if diagnosis.get('primary'):
                filled_fields += 1
            else:
                result.warnings.append(f"Record {i}: Missing primary diagnosis")
        
        completeness_rate = filled_fields / total_fields if total_fields > 0 else 0
        result.metadata['completeness_rate'] = completeness_rate
        
        if completeness_rate < 0.8:
            result.warnings.append(f"Low completeness rate: {completeness_rate:.2%}")
    
    def _validate_consistency(self, records: List[ClinicalRecord], result: ValidationResult):
        """validate data consistency and logical relationships"""
        for i, record in enumerate(records):
            # validate vital signs consistency
            vitals = getattr(record, 'presentation', {}).get('vital_signs', {})
            
            # check blood pressure consistency
            bp_systolic = vitals.get('bp_systolic')
            bp_diastolic = vitals.get('bp_diastolic')
            if bp_systolic and bp_diastolic:
                if bp_systolic <= bp_diastolic:
                    result.errors.append(
                        f"Record {i}: Systolic BP ({bp_systolic}) must be greater than diastolic BP ({bp_diastolic})"
                    )
            
            # check heart rate consistency with age
            heart_rate = vitals.get('heart_rate')
            age = getattr(record, 'demographics', {}).get('age')
            if heart_rate and age:
                if age < 18 and heart_rate > 200:
                    result.warnings.append(
                        f"Record {i}: Unusual heart rate ({heart_rate}) for age {age}"
                    )
                elif age > 65 and heart_rate > 120:
                    result.warnings.append(
                        f"Record {i}: Elevated heart rate ({heart_rate}) for age {age}"
                    )
            
            # check diagnosis-treatment consistency
            diagnosis = getattr(record, 'diagnosis', {}).get('primary', '').lower()
            treatments = getattr(record, 'treatment', {}).get('medications', [])
            
            # check for appropriate treatments for common diagnoses
            if 'mi' in diagnosis or 'stemi' in diagnosis:
                cardiac_meds = ['aspirin', 'nitroglycerin', 'heparin', 'clopidogrel']
                if not any(med.lower() in [t.lower() for t in treatments] for med in cardiac_meds):
                    result.warnings.append(
                        f"Record {i}: STEMI diagnosis without typical cardiac medications"
                    )
    
    def _validate_anonymization(self, records: List[ClinicalRecord], result: ValidationResult):
        """validate that sensitive data has been properly anonymized"""
        for i, record in enumerate(records):
            # check for potential PII in text fields
            presentation = getattr(record, 'presentation', {})
            chief_complaint = presentation.get('chief_complaint', '')
            
            # check for potential names in chief complaint
            if any(word.istitle() and len(word) > 2 for word in chief_complaint.split()):
                result.warnings.append(
                    f"Record {i}: Potential name found in chief complaint"
                )
            
            # check for phone numbers or SSN patterns
            import re
            phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
            ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
            
            if re.search(phone_pattern, chief_complaint):
                result.errors.append(f"Record {i}: Phone number found in chief complaint")
            
            if re.search(ssn_pattern, chief_complaint):
                result.errors.append(f"Record {i}: SSN found in chief complaint")
    
    def _validate_anomalies(self, records: List[ClinicalRecord], result: ValidationResult):
        """detect statistical anomalies in the data"""
        # collect vital signs for anomaly detection
        vitals_data = {
            'heart_rate': [],
            'bp_systolic': [],
            'bp_diastolic': [],
            'respiratory_rate': [],
            'temperature': [],
            'oxygen_saturation': []
        }
        
        for record in records:
            vitals = getattr(record, 'presentation', {}).get('vital_signs', {})
            for vital, values in vitals_data.items():
                if vital in vitals:
                    values.append(vitals[vital])
        
        # detect outliers using IQR method
        for vital, values in vitals_data.items():
            if len(values) > 10:  # need sufficient data
                values = np.array(values)
                q1, q3 = np.percentile(values, [25, 75])
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                outliers = values[(values < lower_bound) | (values > upper_bound)]
                if len(outliers) > 0:
                    result.warnings.append(
                        f"Found {len(outliers)} outliers in {vital}: {outliers.tolist()}"
                    )
    
    def _validate_duplicates(self, records: List[ClinicalRecord], result: ValidationResult):
        """detect potential duplicate records"""
        record_signatures = []
        
        for i, record in enumerate(records):
            # create signature based on key fields
            signature = {
                'age': getattr(record, 'demographics', {}).get('age'),
                'gender': getattr(record, 'demographics', {}).get('gender'),
                'chief_complaint': getattr(record, 'presentation', {}).get('chief_complaint'),
                'primary_diagnosis': getattr(record, 'diagnosis', {}).get('primary')
            }
            record_signatures.append((i, signature))
        
        # find potential duplicates
        from collections import defaultdict
        signature_groups = defaultdict(list)
        
        for i, signature in record_signatures:
            # create hashable signature
            sig_key = tuple(sorted(signature.items()))
            signature_groups[sig_key].append(i)
        
        # report potential duplicates
        for signature, indices in signature_groups.items():
            if len(indices) > 1:
                result.warnings.append(
                    f"Potential duplicate records found: {indices}"
                )
    
    def _calculate_quality_score(self, result: ValidationResult) -> float:
        """calculate overall data quality score"""
        base_score = 1.0
        
        # penalize for errors
        error_penalty = len(result.errors) * 0.1
        base_score -= min(error_penalty, 0.5)
        
        # penalize for warnings
        warning_penalty = len(result.warnings) * 0.02
        base_score -= min(warning_penalty, 0.3)
        
        return max(0.0, base_score)
    
    def _calculate_completeness_score(self, records: List[ClinicalRecord]) -> float:
        """calculate data completeness score"""
        if not records:
            return 0.0
        
        total_fields = 0
        filled_fields = 0
        
        for record in records:
            # count demographics fields
            demographics = getattr(record, 'demographics', {})
            for field in ['age', 'gender', 'race', 'ethnicity']:
                total_fields += 1
                if demographics.get(field):
                    filled_fields += 1
            
            # count presentation fields
            presentation = getattr(record, 'presentation', {})
            for field in ['chief_complaint', 'symptoms', 'vital_signs']:
                total_fields += 1
                if presentation.get(field):
                    filled_fields += 1
            
            # count diagnosis fields
            diagnosis = getattr(record, 'diagnosis', {})
            total_fields += 1
            if diagnosis.get('primary'):
                filled_fields += 1
        
        return filled_fields / total_fields if total_fields > 0 else 0.0
    
    def _calculate_consistency_score(self, records: List[ClinicalRecord]) -> float:
        """calculate data consistency score"""
        if not records:
            return 0.0
        
        consistent_records = 0
        
        for record in records:
            is_consistent = True
            
            # check vital signs consistency
            vitals = getattr(record, 'presentation', {}).get('vital_signs', {})
            bp_systolic = vitals.get('bp_systolic')
            bp_diastolic = vitals.get('bp_diastolic')
            
            if bp_systolic and bp_diastolic:
                if bp_systolic <= bp_diastolic:
                    is_consistent = False
            
            # check age-gender consistency
            demographics = getattr(record, 'demographics', {})
            age = demographics.get('age')
            gender = demographics.get('gender')
            
            if age and gender:
                if age < 0 or age > 120:
                    is_consistent = False
                if gender not in ['male', 'female', 'other']:
                    is_consistent = False
            
            if is_consistent:
                consistent_records += 1
        
        return consistent_records / len(records)
    
    def get_quality_metrics(self, records: List[ClinicalRecord]) -> DataQualityMetrics:
        """get comprehensive quality metrics"""
        if not records:
            return DataQualityMetrics(
                total_records=0,
                valid_records=0,
                completeness_rate=0.0,
                consistency_rate=0.0,
                anomaly_rate=0.0,
                duplicate_rate=0.0,
                missing_fields={},
                invalid_values={},
                field_distributions={}
            )
        
        # calculate basic metrics
        total_records = len(records)
        valid_records = sum(1 for r in records if self._is_record_valid(r))
        
        # calculate missing fields
        missing_fields = defaultdict(int)
        invalid_values = defaultdict(int)
        field_distributions = defaultdict(lambda: defaultdict(int))
        
        for record in records:
            # demographics
            demographics = getattr(record, 'demographics', {})
            for field in ['age', 'gender', 'race', 'ethnicity']:
                if not demographics.get(field):
                    missing_fields[f'demographics.{field}'] += 1
                else:
                    field_distributions[f'demographics.{field}'][str(demographics[field])] += 1
            
            # presentation
            presentation = getattr(record, 'presentation', {})
            for field in ['chief_complaint', 'symptoms']:
                if not presentation.get(field):
                    missing_fields[f'presentation.{field}'] += 1
            
            # diagnosis
            diagnosis = getattr(record, 'diagnosis', {})
            if not diagnosis.get('primary'):
                missing_fields['diagnosis.primary'] += 1
        
        # calculate rates
        completeness_rate = 1.0 - (sum(missing_fields.values()) / (total_records * len(missing_fields))) if missing_fields else 1.0
        consistency_rate = self._calculate_consistency_score(records)
        anomaly_rate = self._calculate_anomaly_rate(records)
        duplicate_rate = self._calculate_duplicate_rate(records)
        
        return DataQualityMetrics(
            total_records=total_records,
            valid_records=valid_records,
            completeness_rate=completeness_rate,
            consistency_rate=consistency_rate,
            anomaly_rate=anomaly_rate,
            duplicate_rate=duplicate_rate,
            missing_fields=dict(missing_fields),
            invalid_values=dict(invalid_values),
            field_distributions=dict(field_distributions)
        )
    
    def _is_record_valid(self, record: ClinicalRecord) -> bool:
        """check if a single record is valid"""
        # check required fields
        demographics = getattr(record, 'demographics', {})
        if not demographics.get('age') or not demographics.get('gender'):
            return False
        
        presentation = getattr(record, 'presentation', {})
        if not presentation.get('chief_complaint'):
            return False
        
        diagnosis = getattr(record, 'diagnosis', {})
        if not diagnosis.get('primary'):
            return False
        
        return True
    
    def _calculate_anomaly_rate(self, records: List[ClinicalRecord]) -> float:
        """calculate anomaly rate in the dataset"""
        if not records:
            return 0.0
        
        anomaly_count = 0
        
        for record in records:
            vitals = getattr(record, 'presentation', {}).get('vital_signs', {})
            
            # check for extreme vital signs
            if vitals.get('heart_rate', 0) > 200 or vitals.get('heart_rate', 0) < 30:
                anomaly_count += 1
            elif vitals.get('bp_systolic', 0) > 250 or vitals.get('bp_systolic', 0) < 60:
                anomaly_count += 1
            elif vitals.get('temperature', 0) > 110 or vitals.get('temperature', 0) < 90:
                anomaly_count += 1
        
        return anomaly_count / len(records)
    
    def _calculate_duplicate_rate(self, records: List[ClinicalRecord]) -> float:
        """calculate duplicate rate in the dataset"""
        if not records:
            return 0.0
        
        # create signatures for duplicate detection
        signatures = []
        for record in records:
            signature = (
                getattr(record, 'demographics', {}).get('age'),
                getattr(record, 'demographics', {}).get('gender'),
                getattr(record, 'presentation', {}).get('chief_complaint'),
                getattr(record, 'diagnosis', {}).get('primary')
            )
            signatures.append(signature)
        
        # count duplicates
        from collections import Counter
        signature_counts = Counter(signatures)
        duplicate_count = sum(count - 1 for count in signature_counts.values() if count > 1)
        
        return duplicate_count / len(records)
    
    def generate_validation_report(self, records: List[ClinicalRecord]) -> Dict[str, Any]:
        """generate comprehensive validation report"""
        validation_result = self.validate_dataset(records)
        quality_metrics = self.get_quality_metrics(records)
        
        return {
            'validation_result': {
                'is_valid': validation_result.is_valid,
                'errors': validation_result.errors,
                'warnings': validation_result.warnings,
                'quality_score': validation_result.quality_score,
                'completeness_score': validation_result.completeness_score,
                'consistency_score': validation_result.consistency_score
            },
            'quality_metrics': {
                'total_records': quality_metrics.total_records,
                'valid_records': quality_metrics.valid_records,
                'completeness_rate': quality_metrics.completeness_rate,
                'consistency_rate': quality_metrics.consistency_rate,
                'anomaly_rate': quality_metrics.anomaly_rate,
                'duplicate_rate': quality_metrics.duplicate_rate,
                'missing_fields': quality_metrics.missing_fields,
                'field_distributions': quality_metrics.field_distributions
            },
            'recommendations': self._generate_recommendations(validation_result, quality_metrics)
        }
    
    def _generate_recommendations(self, validation_result: ValidationResult, 
                                 quality_metrics: DataQualityMetrics) -> List[str]:
        """generate recommendations for data improvement"""
        recommendations = []
        
        if validation_result.quality_score < 0.8:
            recommendations.append("Data quality score is below 0.8 - consider data cleaning")
        
        if quality_metrics.completeness_rate < 0.9:
            recommendations.append("Low completeness rate - fill missing required fields")
        
        if quality_metrics.consistency_rate < 0.95:
            recommendations.append("Low consistency rate - check for logical errors")
        
        if quality_metrics.anomaly_rate > 0.05:
            recommendations.append("High anomaly rate - review extreme values")
        
        if quality_metrics.duplicate_rate > 0.01:
            recommendations.append("Duplicate records detected - consider deduplication")
        
        if len(validation_result.errors) > 0:
            recommendations.append("Critical errors found - must be fixed before use")
        
        if len(validation_result.warnings) > 10:
            recommendations.append("Many warnings - consider data review")
        
        return recommendations 