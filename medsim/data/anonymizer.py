"""
data anonymizer for ensuring clinical data privacy
"""

import re
import hashlib
import uuid
import random
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class AnonymizationConfig:
    """configuration for data anonymization"""
    preserve_medical_info: bool = True
    preserve_demographics: bool = True
    preserve_temporal_data: bool = True
    hash_identifiers: bool = True
    add_noise_to_ages: bool = True
    age_noise_range: int = 2
    preserve_geographic_region: bool = False
    preserve_zip_code_prefix: bool = False
    max_zip_digits: int = 3


@dataclass
class AnonymizationResult:
    """result of data anonymization"""
    original_count: int
    anonymized_count: int
    removed_pii_count: int
    hashed_identifiers: List[str]
    added_noise_count: int
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class DataAnonymizer:
    """anonymizes clinical data to remove PII while preserving medical relevance"""
    
    def __init__(self, config: Optional[AnonymizationConfig] = None):
        self.config = config or AnonymizationConfig()
        
        # patterns for PII detection
        self.pii_patterns = {
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'medical_record': r'\bMRN[:\s]*\d+\b',
            'patient_id': r'\bPAT[:\s]*\d+\b',
            'address': r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr)\b',
            'zip_code': r'\b\d{5}(?:-\d{4})?\b'
        }
        
        # medical terms that should be preserved
        self.medical_terms = {
            'diagnoses', 'symptoms', 'medications', 'procedures', 'allergies',
            'vital_signs', 'lab_results', 'imaging_findings', 'treatment_plans'
        }
        
        # demographic fields that can be preserved with modification
        self.demographic_fields = {
            'age', 'gender', 'race', 'ethnicity', 'insurance_type'
        }
    
    def anonymize_dataset(self, data: Union[List[Dict], Dict], 
                         dataset_name: str = "dataset") -> Union[List[Dict], Dict]:
        """anonymize entire dataset"""
        if isinstance(data, list):
            return self._anonymize_records(data, dataset_name)
        elif isinstance(data, dict):
            return self._anonymize_single_record(data, dataset_name)
        else:
            raise ValueError("Data must be list of records or single record dict")
    
    def _anonymize_records(self, records: List[Dict], dataset_name: str) -> List[Dict]:
        """anonymize list of clinical records"""
        anonymized_records = []
        result = AnonymizationResult(
            original_count=len(records),
            anonymized_count=0,
            removed_pii_count=0,
            hashed_identifiers=[],
            added_noise_count=0
        )
        
        for i, record in enumerate(records):
            try:
                anonymized_record = self._anonymize_single_record(record, f"{dataset_name}_record_{i}")
                anonymized_records.append(anonymized_record)
                result.anonymized_count += 1
                
                # count PII removals
                result.removed_pii_count += self._count_pii_removals(record, anonymized_record)
                
            except Exception as e:
                result.errors.append(f"Error anonymizing record {i}: {e}")
                logger.error(f"Error anonymizing record {i}: {e}")
        
        logger.info(f"Anonymized {result.anonymized_count}/{result.original_count} records")
        return anonymized_records
    
    def _anonymize_single_record(self, record: Dict, record_id: str) -> Dict:
        """anonymize a single clinical record"""
        anonymized = {}
        
        # anonymize each section
        for section, section_data in record.items():
            if section == 'demographics':
                anonymized[section] = self._anonymize_demographics(section_data, record_id)
            elif section == 'presentation':
                anonymized[section] = self._anonymize_presentation(section_data, record_id)
            elif section == 'diagnosis':
                anonymized[section] = self._anonymize_diagnosis(section_data, record_id)
            elif section == 'treatment':
                anonymized[section] = self._anonymize_treatment(section_data, record_id)
            elif section == 'outcome':
                anonymized[section] = self._anonymize_outcome(section_data, record_id)
            elif section == 'temporal_data':
                anonymized[section] = self._anonymize_temporal_data(section_data, record_id)
            else:
                # preserve other medical sections
                anonymized[section] = self._anonymize_generic_section(section_data, record_id)
        
        return anonymized
    
    def _anonymize_demographics(self, demographics: Dict, record_id: str) -> Dict:
        """anonymize demographic information"""
        anonymized = {}
        
        for field, value in demographics.items():
            if field == 'patient_id':
                anonymized[field] = self._hash_identifier(value, record_id)
            elif field == 'name':
                # remove names completely
                continue
            elif field == 'age' and self.config.add_noise_to_ages:
                anonymized[field] = self._add_age_noise(value)
            elif field == 'gender':
                anonymized[field] = value  # preserve gender
            elif field == 'race':
                anonymized[field] = value  # preserve race
            elif field == 'ethnicity':
                anonymized[field] = value  # preserve ethnicity
            elif field == 'address':
                # remove or generalize address
                if self.config.preserve_geographic_region:
                    anonymized[field] = self._generalize_address(value)
                else:
                    continue
            elif field == 'phone':
                # remove phone numbers
                continue
            elif field == 'email':
                # remove email addresses
                continue
            elif field == 'ssn':
                # remove SSN
                continue
            elif field == 'insurance':
                anonymized[field] = value  # preserve insurance type
            else:
                # preserve other demographic fields
                anonymized[field] = value
        
        return anonymized
    
    def _anonymize_presentation(self, presentation: Dict, record_id: str) -> Dict:
        """anonymize presentation information"""
        anonymized = {}
        
        for field, value in presentation.items():
            if field == 'chief_complaint':
                anonymized[field] = self._clean_text_pii(value)
            elif field == 'symptoms':
                if isinstance(value, list):
                    anonymized[field] = [self._clean_text_pii(symptom) for symptom in value]
                else:
                    anonymized[field] = self._clean_text_pii(value)
            elif field == 'vital_signs':
                anonymized[field] = value  # preserve vital signs
            elif field == 'arrival_time':
                anonymized[field] = self._anonymize_timestamp(value)
            else:
                anonymized[field] = self._clean_text_pii(value)
        
        return anonymized
    
    def _anonymize_diagnosis(self, diagnosis: Dict, record_id: str) -> Dict:
        """anonymize diagnosis information"""
        anonymized = {}
        
        for field, value in diagnosis.items():
            if field == 'primary':
                anonymized[field] = value  # preserve primary diagnosis
            elif field == 'secondary':
                if isinstance(value, list):
                    anonymized[field] = [self._clean_text_pii(diag) for diag in value]
                else:
                    anonymized[field] = self._clean_text_pii(value)
            elif field == 'icd_codes':
                anonymized[field] = value  # preserve ICD codes
            else:
                anonymized[field] = self._clean_text_pii(value)
        
        return anonymized
    
    def _anonymize_treatment(self, treatment: Dict, record_id: str) -> Dict:
        """anonymize treatment information"""
        anonymized = {}
        
        for field, value in treatment.items():
            if field == 'medications':
                if isinstance(value, list):
                    anonymized[field] = [self._clean_text_pii(med) for med in value]
                else:
                    anonymized[field] = self._clean_text_pii(value)
            elif field == 'procedures':
                if isinstance(value, list):
                    anonymized[field] = [self._clean_text_pii(proc) for proc in value]
                else:
                    anonymized[field] = self._clean_text_pii(value)
            elif field == 'sequence':
                if isinstance(value, list):
                    anonymized[field] = [self._clean_text_pii(step) for step in value]
                else:
                    anonymized[field] = self._clean_text_pii(value)
            else:
                anonymized[field] = self._clean_text_pii(value)
        
        return anonymized
    
    def _anonymize_outcome(self, outcome: Dict, record_id: str) -> Dict:
        """anonymize outcome information"""
        anonymized = {}
        
        for field, value in outcome.items():
            if field == 'disposition':
                anonymized[field] = value  # preserve disposition
            elif field == 'length_of_stay':
                anonymized[field] = value  # preserve LOS
            elif field == 'mortality':
                anonymized[field] = value  # preserve mortality
            elif field == 'readmission':
                anonymized[field] = value  # preserve readmission
            else:
                anonymized[field] = value
        
        return anonymized
    
    def _anonymize_temporal_data(self, temporal_data: Dict, record_id: str) -> Dict:
        """anonymize temporal data"""
        if not self.config.preserve_temporal_data:
            return {}
        
        anonymized = {}
        
        for field, value in temporal_data.items():
            if isinstance(value, (int, float)):
                # preserve numeric temporal data
                anonymized[field] = value
            elif isinstance(value, str):
                # clean text temporal data
                anonymized[field] = self._clean_text_pii(value)
            else:
                anonymized[field] = value
        
        return anonymized
    
    def _anonymize_generic_section(self, section_data: Dict, record_id: str) -> Dict:
        """anonymize generic section data"""
        anonymized = {}
        
        for field, value in section_data.items():
            if isinstance(value, dict):
                anonymized[field] = self._anonymize_generic_section(value, record_id)
            elif isinstance(value, list):
                anonymized[field] = [self._clean_text_pii(item) if isinstance(item, str) else item for item in value]
            elif isinstance(value, str):
                anonymized[field] = self._clean_text_pii(value)
            else:
                anonymized[field] = value
        
        return anonymized
    
    def _hash_identifier(self, identifier: str, record_id: str) -> str:
        """hash patient identifier"""
        if not self.config.hash_identifiers:
            return f"anon_{record_id}"
        
        # create deterministic hash
        hash_input = f"{identifier}_{record_id}"
        return f"anon_{hashlib.md5(hash_input.encode()).hexdigest()[:8]}"
    
    def _add_age_noise(self, age: Union[int, float]) -> int:
        """add noise to age while preserving age group"""
        if not isinstance(age, (int, float)):
            return age
        
        noise = random.randint(-self.config.age_noise_range, self.config.age_noise_range)
        noisy_age = age + noise
        
        # ensure age stays within reasonable bounds
        return max(0, min(120, noisy_age))
    
    def _generalize_address(self, address: str) -> str:
        """generalize address to preserve region only"""
        if not address:
            return ""
        
        # extract city/state from address
        address_parts = address.split(',')
        if len(address_parts) >= 2:
            city_state = address_parts[-2].strip()
            return f"Generalized Location: {city_state}"
        else:
            return "Generalized Location"
    
    def _clean_text_pii(self, text: str) -> str:
        """remove PII from text while preserving medical information"""
        if not isinstance(text, str):
            return text
        
        cleaned_text = text
        
        # remove phone numbers
        cleaned_text = re.sub(self.pii_patterns['phone'], '[PHONE]', cleaned_text)
        
        # remove SSN
        cleaned_text = re.sub(self.pii_patterns['ssn'], '[SSN]', cleaned_text)
        
        # remove email addresses
        cleaned_text = re.sub(self.pii_patterns['email'], '[EMAIL]', cleaned_text)
        
        # remove credit card numbers
        cleaned_text = re.sub(self.pii_patterns['credit_card'], '[CARD]', cleaned_text)
        
        # remove medical record numbers
        cleaned_text = re.sub(self.pii_patterns['medical_record'], '[MRN]', cleaned_text)
        
        # remove patient IDs
        cleaned_text = re.sub(self.pii_patterns['patient_id'], '[PATIENT_ID]', cleaned_text)
        
        # remove addresses
        cleaned_text = re.sub(self.pii_patterns['address'], '[ADDRESS]', cleaned_text)
        
        # remove or generalize zip codes
        if self.config.preserve_zip_code_prefix:
            cleaned_text = re.sub(r'\b(\d{3})\d{2}(?:-\d{4})?\b', r'\1XX', cleaned_text)
        else:
            cleaned_text = re.sub(self.pii_patterns['zip_code'], '[ZIP]', cleaned_text)
        
        # remove potential names (capitalized words that might be names)
        # but preserve medical terms
        words = cleaned_text.split()
        cleaned_words = []
        
        for word in words:
            if (word.istitle() and len(word) > 2 and 
                word.lower() not in self.medical_terms and
                not word.isupper()):  # don't replace acronyms
                cleaned_words.append('[NAME]')
            else:
                cleaned_words.append(word)
        
        cleaned_text = ' '.join(cleaned_words)
        
        return cleaned_text
    
    def _anonymize_timestamp(self, timestamp: Union[str, datetime]) -> str:
        """anonymize timestamp while preserving temporal relationships"""
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                return timestamp
        
        if isinstance(timestamp, datetime):
            # preserve date but remove specific time
            return timestamp.strftime('%Y-%m-%d')
        else:
            return str(timestamp)
    
    def _count_pii_removals(self, original: Dict, anonymized: Dict) -> int:
        """count how many PII elements were removed"""
        count = 0
        
        # count removed fields
        original_keys = set(original.keys())
        anonymized_keys = set(anonymized.keys())
        removed_keys = original_keys - anonymized_keys
        
        count += len(removed_keys)
        
        # count PII patterns in text fields
        for section in ['presentation', 'diagnosis', 'treatment']:
            if section in original and section in anonymized:
                original_text = str(original[section])
                anonymized_text = str(anonymized[section])
                
                # count pattern removals
                for pattern_name, pattern in self.pii_patterns.items():
                    original_matches = len(re.findall(pattern, original_text))
                    anonymized_matches = len(re.findall(pattern, anonymized_text))
                    count += original_matches - anonymized_matches
        
        return count
    
    def validate_anonymization(self, original_data: Union[List[Dict], Dict], 
                             anonymized_data: Union[List[Dict], Dict]) -> Dict[str, Any]:
        """validate that anonymization was successful"""
        validation_result = {
            'pii_remaining': [],
            'medical_info_preserved': True,
            'anonymization_score': 0.0,
            'warnings': []
        }
        
        if isinstance(original_data, list) and isinstance(anonymized_data, list):
            # validate multiple records
            total_pii_found = 0
            total_medical_preserved = 0
            
            for i, (orig, anon) in enumerate(zip(original_data, anonymized_data)):
                pii_found = self._check_remaining_pii(anon)
                medical_preserved = self._check_medical_preservation(orig, anon)
                
                total_pii_found += len(pii_found)
                if medical_preserved:
                    total_medical_preserved += 1
                
                if pii_found:
                    validation_result['pii_remaining'].append({
                        'record_index': i,
                        'pii_found': pii_found
                    })
            
            validation_result['anonymization_score'] = 1.0 - (total_pii_found / (len(original_data) * 10))
            validation_result['medical_info_preserved'] = total_medical_preserved == len(original_data)
        
        return validation_result
    
    def _check_remaining_pii(self, data: Dict) -> List[str]:
        """check for remaining PII in anonymized data"""
        pii_found = []
        data_str = json.dumps(data, default=str)
        
        for pattern_name, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, data_str)
            if matches:
                pii_found.append(f"{pattern_name}: {matches}")
        
        return pii_found
    
    def _check_medical_preservation(self, original: Dict, anonymized: Dict) -> bool:
        """check if medical information was preserved"""
        # check key medical fields are preserved
        medical_fields = ['diagnosis', 'symptoms', 'medications', 'vital_signs']
        
        for field in medical_fields:
            if field in original and field not in anonymized:
                return False
            elif field in original and field in anonymized:
                # check that medical content is preserved
                orig_content = str(original[field])
                anon_content = str(anonymized[field])
                
                # should contain medical terms
                medical_terms = ['pain', 'fever', 'shortness', 'chest', 'heart', 'blood']
                if any(term in orig_content.lower() for term in medical_terms):
                    if not any(term in anon_content.lower() for term in medical_terms):
                        return False
        
        return True
    
    def generate_anonymization_report(self, original_data: Union[List[Dict], Dict], 
                                    anonymized_data: Union[List[Dict], Dict]) -> Dict[str, Any]:
        """generate comprehensive anonymization report"""
        validation = self.validate_anonymization(original_data, anonymized_data)
        
        if isinstance(original_data, list):
            original_count = len(original_data)
            anonymized_count = len(anonymized_data)
        else:
            original_count = 1
            anonymized_count = 1
        
        return {
            'summary': {
                'original_records': original_count,
                'anonymized_records': anonymized_count,
                'anonymization_score': validation['anonymization_score'],
                'medical_info_preserved': validation['medical_info_preserved']
            },
            'validation': validation,
            'recommendations': self._generate_anonymization_recommendations(validation)
        }
    
    def _generate_anonymization_recommendations(self, validation: Dict[str, Any]) -> List[str]:
        """generate recommendations for anonymization improvement"""
        recommendations = []
        
        if validation['anonymization_score'] < 0.9:
            recommendations.append("Anonymization score below 0.9 - review PII removal")
        
        if validation['pii_remaining']:
            recommendations.append(f"Found {len(validation['pii_remaining'])} records with remaining PII")
        
        if not validation['medical_info_preserved']:
            recommendations.append("Medical information may have been over-anonymized")
        
        if validation['anonymization_score'] < 0.8:
            recommendations.append("Consider additional PII detection patterns")
        
        return recommendations 