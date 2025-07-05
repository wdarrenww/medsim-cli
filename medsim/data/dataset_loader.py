"""
clinical dataset loader for handling anonymized medical data
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class ClinicalRecord:
    """represents a single clinical patient record"""
    patient_id: str
    demographics: Dict[str, Any]
    presentation: Dict[str, Any]
    diagnosis: Dict[str, Any]
    treatment: Dict[str, Any]
    outcome: Dict[str, Any]
    temporal_data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_age_group(self) -> str:
        """get age group for analysis"""
        age = self.demographics.get('age', 0)
        if age < 18:
            return 'pediatric'
        elif age < 65:
            return 'adult'
        else:
            return 'geriatric'
    
    def get_primary_diagnosis(self) -> str:
        """get primary diagnosis"""
        return self.diagnosis.get('primary', 'unknown')
    
    def get_symptom_cluster(self) -> List[str]:
        """get symptom cluster for pattern analysis"""
        return self.presentation.get('symptoms', [])
    
    def get_treatment_sequence(self) -> List[str]:
        """get treatment sequence for analysis"""
        return self.treatment.get('sequence', [])


@dataclass
class DatasetMetadata:
    """metadata about the clinical dataset"""
    name: str
    source: str
    record_count: int
    date_range: Dict[str, datetime]
    specialties: List[str]
    demographics_summary: Dict[str, Any]
    anonymization_level: str
    quality_score: float
    last_updated: datetime


class ClinicalDatasetLoader:
    """loads and manages clinical datasets for scenario generation"""
    
    def __init__(self, data_directory: str = "data"):
        self.data_directory = Path(data_directory)
        self.datasets: Dict[str, List[ClinicalRecord]] = {}
        self.metadata: Dict[str, DatasetMetadata] = {}
        self.supported_formats = ['.csv', '.json', '.parquet', '.xlsx']
        
    def load_dataset(self, filename: str, dataset_name: Optional[str] = None) -> bool:
        """load a clinical dataset from file"""
        filepath = self.data_directory / filename
        
        if not filepath.exists():
            logger.error(f"dataset file not found: {filepath}")
            return False
        
        if dataset_name is None:
            dataset_name = filepath.stem
        
        try:
            file_extension = filepath.suffix.lower()
            
            if file_extension == '.csv':
                records = self._load_csv_dataset(filepath)
            elif file_extension == '.json':
                records = self._load_json_dataset(filepath)
            elif file_extension == '.parquet':
                records = self._load_parquet_dataset(filepath)
            elif file_extension == '.xlsx':
                records = self._load_excel_dataset(filepath)
            else:
                logger.error(f"unsupported file format: {file_extension}")
                return False
            
            if records:
                self.datasets[dataset_name] = records
                self.metadata[dataset_name] = self._generate_metadata(dataset_name, records)
                logger.info(f"loaded dataset '{dataset_name}' with {len(records)} records")
                return True
            else:
                logger.error(f"no valid records found in {filename}")
                return False
                
        except Exception as e:
            logger.error(f"error loading dataset {filename}: {e}")
            return False
    
    def _load_csv_dataset(self, filepath: Path) -> List[ClinicalRecord]:
        """load dataset from csv format"""
        df = pd.read_csv(filepath)
        records = []
        
        for _, row in df.iterrows():
            try:
                record = self._parse_record_from_row(row)
                if record:
                    records.append(record)
            except Exception as e:
                logger.warning(f"skipping invalid record: {e}")
                continue
        
        return records
    
    def _load_json_dataset(self, filepath: Path) -> List[ClinicalRecord]:
        """load dataset from json format"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        records = []
        patient_records = data.get('patient_records', [])
        
        for record_data in patient_records:
            try:
                record = self._parse_record_from_dict(record_data)
                if record:
                    records.append(record)
            except Exception as e:
                logger.warning(f"skipping invalid record: {e}")
                continue
        
        return records
    
    def _load_parquet_dataset(self, filepath: Path) -> List[ClinicalRecord]:
        """load dataset from parquet format"""
        df = pd.read_parquet(filepath)
        records = []
        
        for _, row in df.iterrows():
            try:
                record = self._parse_record_from_row(row)
                if record:
                    records.append(record)
            except Exception as e:
                logger.warning(f"skipping invalid record: {e}")
                continue
        
        return records
    
    def _load_excel_dataset(self, filepath: Path) -> List[ClinicalRecord]:
        """load dataset from excel format"""
        df = pd.read_excel(filepath)
        records = []
        
        for _, row in df.iterrows():
            try:
                record = self._parse_record_from_row(row)
                if record:
                    records.append(record)
            except Exception as e:
                logger.warning(f"skipping invalid record: {e}")
                continue
        
        return records
    
    def _parse_record_from_row(self, row: pd.Series) -> Optional[ClinicalRecord]:
        """parse clinical record from dataframe row"""
        try:
            # handle different column naming conventions
            patient_id = str(row.get('patient_id', row.get('id', f"P{hash(str(row))}")))
            
            demographics = {
                'age': int(row.get('age', 0)),
                'gender': str(row.get('gender', 'unknown')),
                'race': str(row.get('race', 'unknown')),
                'ethnicity': str(row.get('ethnicity', 'unknown')),
                'insurance': str(row.get('insurance', 'unknown'))
            }
            
            presentation = {
                'chief_complaint': str(row.get('chief_complaint', '')),
                'symptoms': self._parse_list_field(row.get('symptoms', '')),
                'vital_signs': self._parse_vital_signs(row),
                'arrival_time': self._parse_datetime(row.get('arrival_time', ''))
            }
            
            diagnosis = {
                'primary': str(row.get('primary_diagnosis', '')),
                'secondary': self._parse_list_field(row.get('secondary_diagnoses', '')),
                'icd_codes': self._parse_list_field(row.get('icd_codes', ''))
            }
            
            treatment = {
                'medications': self._parse_list_field(row.get('medications', '')),
                'procedures': self._parse_list_field(row.get('procedures', '')),
                'sequence': self._parse_list_field(row.get('treatment_sequence', ''))
            }
            
            outcome = {
                'disposition': str(row.get('disposition', '')),
                'length_of_stay': float(row.get('length_of_stay', 0)),
                'mortality': bool(row.get('mortality', False)),
                'readmission': bool(row.get('readmission', False))
            }
            
            temporal_data = {
                'arrival_to_diagnosis': float(row.get('arrival_to_diagnosis', 0)),
                'diagnosis_to_treatment': float(row.get('diagnosis_to_treatment', 0)),
                'treatment_to_discharge': float(row.get('treatment_to_discharge', 0))
            }
            
            return ClinicalRecord(
                patient_id=patient_id,
                demographics=demographics,
                presentation=presentation,
                diagnosis=diagnosis,
                treatment=treatment,
                outcome=outcome,
                temporal_data=temporal_data
            )
            
        except Exception as e:
            logger.warning(f"error parsing record: {e}")
            return None
    
    def _parse_record_from_dict(self, record_data: Dict[str, Any]) -> Optional[ClinicalRecord]:
        """parse clinical record from dictionary"""
        try:
            return ClinicalRecord(
                patient_id=record_data.get('patient_id', 'unknown'),
                demographics=record_data.get('demographics', {}),
                presentation=record_data.get('presentation', {}),
                diagnosis=record_data.get('diagnosis', {}),
                treatment=record_data.get('treatment', {}),
                outcome=record_data.get('outcome', {}),
                temporal_data=record_data.get('temporal_data', {}),
                metadata=record_data.get('metadata', {})
            )
        except Exception as e:
            logger.warning(f"error parsing record from dict: {e}")
            return None
    
    def _parse_list_field(self, field: Any) -> List[str]:
        """parse list field from various formats"""
        if isinstance(field, list):
            return [str(item) for item in field]
        elif isinstance(field, str):
            if field.startswith('[') and field.endswith(']'):
                # parse json-like string
                try:
                    import ast
                    return [str(item) for item in ast.literal_eval(field)]
                except:
                    pass
            # split by common delimiters
            for delimiter in [';', ',', '|']:
                if delimiter in field:
                    return [item.strip() for item in field.split(delimiter) if item.strip()]
            return [field] if field else []
        else:
            return []
    
    def _parse_vital_signs(self, row: pd.Series) -> Dict[str, float]:
        """parse vital signs from row"""
        vitals = {}
        vital_fields = ['heart_rate', 'bp_systolic', 'bp_diastolic', 
                      'respiratory_rate', 'temperature', 'oxygen_saturation']
        
        for field in vital_fields:
            value = row.get(field)
            if pd.notna(value) and value != '':
                try:
                    vitals[field] = float(value)
                except:
                    continue
        
        return vitals
    
    def _parse_datetime(self, dt_str: str) -> Optional[datetime]:
        """parse datetime string"""
        if not dt_str or pd.isna(dt_str):
            return None
        
        try:
            return pd.to_datetime(dt_str)
        except:
            return None
    
    def _generate_metadata(self, dataset_name: str, records: List[ClinicalRecord]) -> DatasetMetadata:
        """generate metadata for dataset"""
        if not records:
            return DatasetMetadata(
                name=dataset_name,
                source="unknown",
                record_count=0,
                date_range={},
                specialties=[],
                demographics_summary={},
                anonymization_level="unknown",
                quality_score=0.0,
                last_updated=datetime.now()
            )
        
        # analyze demographics
        ages = [r.demographics.get('age', 0) for r in records if r.demographics.get('age', 0) > 0]
        genders = [r.demographics.get('gender', '') for r in records]
        
        demographics_summary = {
            'age_mean': np.mean(ages) if ages else 0,
            'age_std': np.std(ages) if ages else 0,
            'gender_distribution': dict(pd.Series(genders).value_counts()),
            'total_records': len(records)
        }
        
        # analyze specialties and diagnoses
        diagnoses = [r.get_primary_diagnosis() for r in records]
        specialties = self._categorize_specialties(diagnoses)
        
        # estimate date range
        date_range = self._estimate_date_range(records)
        
        return DatasetMetadata(
            name=dataset_name,
            source="loaded_dataset",
            record_count=len(records),
            date_range=date_range,
            specialties=specialties,
            demographics_summary=demographics_summary,
            anonymization_level="verified",
            quality_score=self._calculate_quality_score(records),
            last_updated=datetime.now()
        )
    
    def _categorize_specialties(self, diagnoses: List[str]) -> List[str]:
        """categorize diagnoses into medical specialties"""
        specialty_keywords = {
            'cardiology': ['heart', 'cardiac', 'chest pain', 'mi', 'chf'],
            'emergency': ['trauma', 'emergency', 'acute'],
            'neurology': ['stroke', 'seizure', 'headache', 'neurological'],
            'respiratory': ['copd', 'asthma', 'pneumonia', 'respiratory'],
            'surgery': ['appendicitis', 'cholecystitis', 'surgical'],
            'pediatrics': ['pediatric', 'child', 'infant'],
            'obstetrics': ['pregnancy', 'labor', 'delivery', 'obstetric']
        }
        
        specialties = set()
        for diagnosis in diagnoses:
            diagnosis_lower = diagnosis.lower()
            for specialty, keywords in specialty_keywords.items():
                if any(keyword in diagnosis_lower for keyword in keywords):
                    specialties.add(specialty)
        
        return list(specialties)
    
    def _estimate_date_range(self, records: List[ClinicalRecord]) -> Dict[str, datetime]:
        """estimate date range from records"""
        dates = []
        for record in records:
            arrival_time = record.presentation.get('arrival_time')
            if arrival_time:
                dates.append(arrival_time)
        
        if dates:
            return {
                'start': min(dates),
                'end': max(dates)
            }
        else:
            return {}
    
    def _calculate_quality_score(self, records: List[ClinicalRecord]) -> float:
        """calculate data quality score"""
        if not records:
            return 0.0
        
        total_fields = 0
        filled_fields = 0
        
        for record in records:
            # check demographics completeness
            for field in ['age', 'gender']:
                total_fields += 1
                if record.demographics.get(field):
                    filled_fields += 1
            
            # check presentation completeness
            for field in ['chief_complaint', 'symptoms']:
                total_fields += 1
                if record.presentation.get(field):
                    filled_fields += 1
            
            # check diagnosis completeness
            total_fields += 1
            if record.diagnosis.get('primary'):
                filled_fields += 1
        
        return filled_fields / total_fields if total_fields > 0 else 0.0
    
    def get_dataset(self, dataset_name: str) -> Optional[List[ClinicalRecord]]:
        """get loaded dataset by name"""
        return self.datasets.get(dataset_name)
    
    def get_dataset_metadata(self, dataset_name: str) -> Optional[DatasetMetadata]:
        """get dataset metadata"""
        return self.metadata.get(dataset_name)
    
    def list_datasets(self) -> List[str]:
        """list all loaded datasets"""
        return list(self.datasets.keys())
    
    def get_dataset_summary(self, dataset_name: str) -> Dict[str, Any]:
        """get comprehensive dataset summary"""
        records = self.get_dataset(dataset_name)
        metadata = self.get_dataset_metadata(dataset_name)
        
        if not records or not metadata:
            return {}
        
        # analyze patterns
        diagnoses = [r.get_primary_diagnosis() for r in records]
        age_groups = [r.get_age_group() for r in records]
        dispositions = [r.outcome.get('disposition', '') for r in records]
        
        return {
            'metadata': metadata,
            'diagnosis_distribution': dict(pd.Series(diagnoses).value_counts()),
            'age_group_distribution': dict(pd.Series(age_groups).value_counts()),
            'disposition_distribution': dict(pd.Series(dispositions).value_counts()),
            'avg_length_of_stay': np.mean([r.outcome.get('length_of_stay', 0) for r in records]),
            'mortality_rate': np.mean([r.outcome.get('mortality', False) for r in records]),
            'readmission_rate': np.mean([r.outcome.get('readmission', False) for r in records])
        }
    
    def filter_records(self, dataset_name: str, filters: Dict[str, Any]) -> List[ClinicalRecord]:
        """filter records based on criteria"""
        records = self.get_dataset(dataset_name)
        if not records:
            return []
        
        filtered_records = records
        
        # apply filters
        if 'age_min' in filters:
            filtered_records = [r for r in filtered_records 
                              if r.demographics.get('age', 0) >= filters['age_min']]
        
        if 'age_max' in filters:
            filtered_records = [r for r in filtered_records 
                              if r.demographics.get('age', 0) <= filters['age_max']]
        
        if 'gender' in filters:
            filtered_records = [r for r in filtered_records 
                              if r.demographics.get('gender', '').lower() == filters['gender'].lower()]
        
        if 'diagnosis_keywords' in filters:
            keywords = filters['diagnosis_keywords']
            filtered_records = [r for r in filtered_records 
                              if any(keyword.lower() in r.get_primary_diagnosis().lower() 
                                    for keyword in keywords)]
        
        if 'specialty' in filters:
            specialty = filters['specialty'].lower()
            filtered_records = [r for r in filtered_records 
                              if specialty in self._categorize_specialties([r.get_primary_diagnosis()])]
        
        return filtered_records 