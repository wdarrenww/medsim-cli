"""
pattern analyzer for identifying clinical patterns from datasets
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import logging
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

from .dataset_loader import ClinicalRecord

logger = logging.getLogger(__name__)


@dataclass
class ClinicalPattern:
    """represents a clinical pattern identified from data"""
    pattern_id: str
    pattern_type: str  # symptom_cluster, diagnosis_treatment, temporal, demographic
    frequency: float
    confidence: float
    characteristics: Dict[str, Any]
    examples: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PatternCluster:
    """represents a cluster of similar clinical patterns"""
    cluster_id: str
    patterns: List[ClinicalPattern]
    centroid: Dict[str, Any]
    size: int
    specialty: str
    difficulty_level: str


class PatternAnalyzer:
    """analyzes clinical datasets to identify patterns for scenario generation"""
    
    def __init__(self):
        self.patterns: Dict[str, ClinicalPattern] = {}
        self.clusters: Dict[str, PatternCluster] = {}
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        
    def analyze_dataset(self, records: List[ClinicalRecord]) -> Dict[str, Any]:
        """perform comprehensive pattern analysis on dataset"""
        if not records:
            return {}
        
        analysis_results = {
            'symptom_patterns': self._analyze_symptom_patterns(records),
            'diagnosis_patterns': self._analyze_diagnosis_patterns(records),
            'treatment_patterns': self._analyze_treatment_patterns(records),
            'temporal_patterns': self._analyze_temporal_patterns(records),
            'demographic_patterns': self._analyze_demographic_patterns(records),
            'outcome_patterns': self._analyze_outcome_patterns(records),
            'specialty_patterns': self._analyze_specialty_patterns(records)
        }
        
        # cluster patterns
        self._cluster_patterns(analysis_results)
        
        return analysis_results
    
    def _analyze_symptom_patterns(self, records: List[ClinicalRecord]) -> List[ClinicalPattern]:
        """analyze symptom clusters and patterns"""
        patterns = []
        
        # collect all symptom clusters
        symptom_clusters = []
        for record in records:
            symptoms = record.get_symptom_cluster()
            if symptoms:
                symptom_clusters.append(symptoms)
        
        if not symptom_clusters:
            return patterns
        
        # find frequent symptom combinations
        cluster_counter = Counter()
        for cluster in symptom_clusters:
            # normalize cluster (sort, lowercase)
            normalized = tuple(sorted([s.lower().strip() for s in cluster]))
            cluster_counter[normalized] += 1
        
        total_records = len(records)
        
        # create patterns for frequent clusters
        for cluster, count in cluster_counter.most_common(20):
            frequency = count / total_records
            if frequency >= 0.01:  # at least 1% frequency
                pattern = ClinicalPattern(
                    pattern_id=f"symptom_cluster_{len(patterns)}",
                    pattern_type="symptom_cluster",
                    frequency=frequency,
                    confidence=min(frequency * 10, 1.0),  # confidence based on frequency
                    characteristics={
                        'symptoms': list(cluster),
                        'symptom_count': len(cluster),
                        'avg_symptoms_per_case': len(cluster)
                    },
                    examples=[f"Cluster with {count} occurrences"]
                )
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_diagnosis_patterns(self, records: List[ClinicalRecord]) -> List[ClinicalPattern]:
        """analyze diagnosis patterns and relationships"""
        patterns = []
        
        # collect diagnoses and their characteristics
        diagnosis_data = defaultdict(list)
        for record in records:
            diagnosis = record.get_primary_diagnosis()
            if diagnosis and diagnosis != 'unknown':
                diagnosis_data[diagnosis].append({
                    'age': record.demographics.get('age', 0),
                    'gender': record.demographics.get('gender', ''),
                    'symptoms': record.get_symptom_cluster(),
                    'outcome': record.outcome.get('disposition', ''),
                    'length_of_stay': record.outcome.get('length_of_stay', 0)
                })
        
        total_records = len(records)
        
        for diagnosis, cases in diagnosis_data.items():
            if len(cases) >= 5:  # minimum cases for pattern
                frequency = len(cases) / total_records
                
                # analyze characteristics
                ages = [case['age'] for case in cases if case['age'] > 0]
                genders = [case['gender'] for case in cases if case['gender']]
                dispositions = [case['outcome'] for case in cases if case['outcome']]
                lengths_of_stay = [case['length_of_stay'] for case in cases if case['length_of_stay'] > 0]
                
                pattern = ClinicalPattern(
                    pattern_id=f"diagnosis_{len(patterns)}",
                    pattern_type="diagnosis_pattern",
                    frequency=frequency,
                    confidence=min(frequency * 5, 1.0),
                    characteristics={
                        'diagnosis': diagnosis,
                        'avg_age': np.mean(ages) if ages else 0,
                        'age_std': np.std(ages) if ages else 0,
                        'gender_distribution': dict(Counter(genders)),
                        'common_dispositions': dict(Counter(dispositions)),
                        'avg_length_of_stay': np.mean(lengths_of_stay) if lengths_of_stay else 0,
                        'case_count': len(cases)
                    },
                    examples=[f"{len(cases)} cases of {diagnosis}"]
                )
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_treatment_patterns(self, records: List[ClinicalRecord]) -> List[ClinicalPattern]:
        """analyze treatment patterns and sequences"""
        patterns = []
        
        # collect treatment sequences
        treatment_sequences = []
        for record in records:
            sequence = record.get_treatment_sequence()
            if sequence:
                treatment_sequences.append(sequence)
        
        if not treatment_sequences:
            return patterns
        
        # find common treatment patterns
        sequence_counter = Counter()
        for sequence in treatment_sequences:
            # normalize sequence
            normalized = tuple([t.lower().strip() for t in sequence])
            sequence_counter[normalized] += 1
        
        total_records = len(records)
        
        for sequence, count in sequence_counter.most_common(15):
            frequency = count / total_records
            if frequency >= 0.01:
                pattern = ClinicalPattern(
                    pattern_id=f"treatment_sequence_{len(patterns)}",
                    pattern_type="treatment_sequence",
                    frequency=frequency,
                    confidence=min(frequency * 8, 1.0),
                    characteristics={
                        'treatment_sequence': list(sequence),
                        'sequence_length': len(sequence),
                        'common_treatments': list(set(sequence))
                    },
                    examples=[f"Sequence with {count} occurrences"]
                )
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_temporal_patterns(self, records: List[ClinicalRecord]) -> List[ClinicalPattern]:
        """analyze temporal patterns in patient care"""
        patterns = []
        
        temporal_data = []
        for record in records:
            temporal = record.temporal_data
            if temporal:
                temporal_data.append(temporal)
        
        if not temporal_data:
            return patterns
        
        # analyze time intervals
        arrival_to_diagnosis = [t.get('arrival_to_diagnosis', 0) for t in temporal_data if t.get('arrival_to_diagnosis', 0) > 0]
        diagnosis_to_treatment = [t.get('diagnosis_to_treatment', 0) for t in temporal_data if t.get('diagnosis_to_treatment', 0) > 0]
        treatment_to_discharge = [t.get('treatment_to_discharge', 0) for t in temporal_data if t.get('treatment_to_discharge', 0) > 0]
        
        if arrival_to_diagnosis:
            pattern = ClinicalPattern(
                pattern_id="temporal_arrival_diagnosis",
                pattern_type="temporal_pattern",
                frequency=len(arrival_to_diagnosis) / len(records),
                confidence=0.8,
                characteristics={
                    'avg_arrival_to_diagnosis': np.mean(arrival_to_diagnosis),
                    'std_arrival_to_diagnosis': np.std(arrival_to_diagnosis),
                    'median_arrival_to_diagnosis': np.median(arrival_to_diagnosis)
                },
                examples=["Time from arrival to diagnosis patterns"]
            )
            patterns.append(pattern)
        
        if diagnosis_to_treatment:
            pattern = ClinicalPattern(
                pattern_id="temporal_diagnosis_treatment",
                pattern_type="temporal_pattern",
                frequency=len(diagnosis_to_treatment) / len(records),
                confidence=0.8,
                characteristics={
                    'avg_diagnosis_to_treatment': np.mean(diagnosis_to_treatment),
                    'std_diagnosis_to_treatment': np.std(diagnosis_to_treatment),
                    'median_diagnosis_to_treatment': np.median(diagnosis_to_treatment)
                },
                examples=["Time from diagnosis to treatment patterns"]
            )
            patterns.append(pattern)
        
        return patterns
    
    def _analyze_demographic_patterns(self, records: List[ClinicalRecord]) -> List[ClinicalPattern]:
        """analyze demographic patterns and relationships"""
        patterns = []
        
        # analyze age groups
        age_groups = [record.get_age_group() for record in records]
        age_distribution = Counter(age_groups)
        
        for age_group, count in age_distribution.items():
            frequency = count / len(records)
            if frequency >= 0.05:  # at least 5% of cases
                pattern = ClinicalPattern(
                    pattern_id=f"demographic_age_{age_group}",
                    pattern_type="demographic_pattern",
                    frequency=frequency,
                    confidence=0.9,
                    characteristics={
                        'age_group': age_group,
                        'count': count,
                        'common_diagnoses': self._get_common_diagnoses_by_age_group(records, age_group)
                    },
                    examples=[f"{count} cases in {age_group} age group"]
                )
                patterns.append(pattern)
        
        # analyze gender patterns
        genders = [record.demographics.get('gender', '') for record in records]
        gender_distribution = Counter(genders)
        
        for gender, count in gender_distribution.items():
            if gender and count >= 10:  # minimum cases
                frequency = count / len(records)
                pattern = ClinicalPattern(
                    pattern_id=f"demographic_gender_{gender}",
                    pattern_type="demographic_pattern",
                    frequency=frequency,
                    confidence=0.9,
                    characteristics={
                        'gender': gender,
                        'count': count,
                        'common_diagnoses': self._get_common_diagnoses_by_gender(records, gender)
                    },
                    examples=[f"{count} cases for {gender} patients"]
                )
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_outcome_patterns(self, records: List[ClinicalRecord]) -> List[ClinicalPattern]:
        """analyze outcome patterns and relationships"""
        patterns = []
        
        # analyze dispositions
        dispositions = [record.outcome.get('disposition', '') for record in records]
        disposition_distribution = Counter(dispositions)
        
        for disposition, count in disposition_distribution.items():
            if disposition and count >= 5:
                frequency = count / len(records)
                pattern = ClinicalPattern(
                    pattern_id=f"outcome_disposition_{disposition}",
                    pattern_type="outcome_pattern",
                    frequency=frequency,
                    confidence=0.8,
                    characteristics={
                        'disposition': disposition,
                        'count': count,
                        'avg_length_of_stay': self._get_avg_los_by_disposition(records, disposition)
                    },
                    examples=[f"{count} cases with {disposition} disposition"]
                )
                patterns.append(pattern)
        
        # analyze mortality patterns
        mortality_cases = [r for r in records if r.outcome.get('mortality', False)]
        if mortality_cases:
            frequency = len(mortality_cases) / len(records)
            pattern = ClinicalPattern(
                pattern_id="outcome_mortality",
                pattern_type="outcome_pattern",
                frequency=frequency,
                confidence=0.9,
                characteristics={
                    'mortality_rate': frequency,
                    'common_diagnoses': self._get_common_diagnoses(mortality_cases),
                    'avg_age': np.mean([r.demographics.get('age', 0) for r in mortality_cases])
                },
                examples=[f"{len(mortality_cases)} mortality cases"]
            )
            patterns.append(pattern)
        
        return patterns
    
    def _analyze_specialty_patterns(self, records: List[ClinicalRecord]) -> List[ClinicalPattern]:
        """analyze patterns by medical specialty"""
        patterns = []
        
        # categorize records by specialty
        specialty_records = defaultdict(list)
        for record in records:
            diagnosis = record.get_primary_diagnosis()
            specialties = self._categorize_diagnosis_to_specialty(diagnosis)
            for specialty in specialties:
                specialty_records[specialty].append(record)
        
        for specialty, specialty_cases in specialty_records.items():
            if len(specialty_cases) >= 10:  # minimum cases for specialty
                frequency = len(specialty_cases) / len(records)
                pattern = ClinicalPattern(
                    pattern_id=f"specialty_{specialty}",
                    pattern_type="specialty_pattern",
                    frequency=frequency,
                    confidence=0.8,
                    characteristics={
                        'specialty': specialty,
                        'case_count': len(specialty_cases),
                        'common_diagnoses': self._get_common_diagnoses(specialty_cases),
                        'avg_age': np.mean([r.demographics.get('age', 0) for r in specialty_cases]),
                        'gender_distribution': dict(Counter([r.demographics.get('gender', '') for r in specialty_cases]))
                    },
                    examples=[f"{len(specialty_cases)} cases in {specialty}"]
                )
                patterns.append(pattern)
        
        return patterns
    
    def _categorize_diagnosis_to_specialty(self, diagnosis: str) -> List[str]:
        """categorize diagnosis to medical specialties"""
        diagnosis_lower = diagnosis.lower()
        specialties = []
        
        specialty_keywords = {
            'cardiology': ['heart', 'cardiac', 'chest pain', 'mi', 'chf', 'arrhythmia'],
            'emergency': ['trauma', 'emergency', 'acute', 'overdose'],
            'neurology': ['stroke', 'seizure', 'headache', 'neurological', 'tia'],
            'respiratory': ['copd', 'asthma', 'pneumonia', 'respiratory', 'dyspnea'],
            'surgery': ['appendicitis', 'cholecystitis', 'surgical', 'hernia'],
            'pediatrics': ['pediatric', 'child', 'infant', 'fever'],
            'obstetrics': ['pregnancy', 'labor', 'delivery', 'obstetric'],
            'psychiatry': ['psychiatric', 'depression', 'anxiety', 'suicide']
        }
        
        for specialty, keywords in specialty_keywords.items():
            if any(keyword in diagnosis_lower for keyword in keywords):
                specialties.append(specialty)
        
        return specialties if specialties else ['general']
    
    def _get_common_diagnoses(self, records: List[ClinicalRecord]) -> Dict[str, int]:
        """get common diagnoses from records"""
        diagnoses = [r.get_primary_diagnosis() for r in records]
        return dict(Counter(diagnoses).most_common(5))
    
    def _get_common_diagnoses_by_age_group(self, records: List[ClinicalRecord], age_group: str) -> Dict[str, int]:
        """get common diagnoses for specific age group"""
        age_records = [r for r in records if r.get_age_group() == age_group]
        return self._get_common_diagnoses(age_records)
    
    def _get_common_diagnoses_by_gender(self, records: List[ClinicalRecord], gender: str) -> Dict[str, int]:
        """get common diagnoses for specific gender"""
        gender_records = [r for r in records if r.demographics.get('gender', '').lower() == gender.lower()]
        return self._get_common_diagnoses(gender_records)
    
    def _get_avg_los_by_disposition(self, records: List[ClinicalRecord], disposition: str) -> float:
        """get average length of stay for specific disposition"""
        disposition_records = [r for r in records if r.outcome.get('disposition', '') == disposition]
        los_values = [r.outcome.get('length_of_stay', 0) for r in disposition_records if r.outcome.get('length_of_stay', 0) > 0]
        return np.mean(los_values) if los_values else 0
    
    def _cluster_patterns(self, analysis_results: Dict[str, List[ClinicalPattern]]):
        """cluster similar patterns together"""
        all_patterns = []
        for pattern_list in analysis_results.values():
            all_patterns.extend(pattern_list)
        
        if len(all_patterns) < 2:
            return
        
        # create feature vectors for clustering
        feature_vectors = []
        for pattern in all_patterns:
            vector = [
                pattern.frequency,
                pattern.confidence,
                len(pattern.characteristics),
                pattern.characteristics.get('avg_age', 0) / 100,  # normalize age
                pattern.characteristics.get('sequence_length', 0) / 10  # normalize sequence length
            ]
            feature_vectors.append(vector)
        
        # perform clustering
        n_clusters = min(5, len(all_patterns) // 2)
        if n_clusters < 2:
            return
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(feature_vectors)
        
        # group patterns by cluster
        cluster_groups = defaultdict(list)
        for pattern, label in zip(all_patterns, cluster_labels):
            cluster_groups[label].append(pattern)
        
        # create pattern clusters
        for cluster_id, patterns in cluster_groups.items():
            if len(patterns) >= 2:
                # determine specialty and difficulty
                specialties = [p.characteristics.get('specialty', 'general') for p in patterns if p.characteristics.get('specialty')]
                specialty = max(set(specialties), key=specialties.count) if specialties else 'general'
                
                avg_frequency = np.mean([p.frequency for p in patterns])
                difficulty = 'easy' if avg_frequency > 0.1 else 'medium' if avg_frequency > 0.05 else 'hard'
                
                cluster = PatternCluster(
                    cluster_id=f"cluster_{cluster_id}",
                    patterns=patterns,
                    centroid=kmeans.cluster_centers_[cluster_id].tolist(),
                    size=len(patterns),
                    specialty=specialty,
                    difficulty_level=difficulty
                )
                self.clusters[f"cluster_{cluster_id}"] = cluster
    
    def get_patterns_by_type(self, pattern_type: str) -> List[ClinicalPattern]:
        """get patterns of specific type"""
        return [p for p in self.patterns.values() if p.pattern_type == pattern_type]
    
    def get_patterns_by_specialty(self, specialty: str) -> List[ClinicalPattern]:
        """get patterns for specific specialty"""
        return [p for p in self.patterns.values() 
                if p.characteristics.get('specialty', '') == specialty]
    
    def get_patterns_by_difficulty(self, difficulty: str) -> List[ClinicalPattern]:
        """get patterns by difficulty level"""
        return [p for p in self.patterns.values() 
                if p.characteristics.get('difficulty', 'medium') == difficulty]
    
    def export_patterns(self, filepath: str) -> bool:
        """export patterns to json file"""
        try:
            patterns_data = {
                'patterns': [self._pattern_to_dict(p) for p in self.patterns.values()],
                'clusters': [self._cluster_to_dict(c) for c in self.clusters.values()]
            }
            
            with open(filepath, 'w') as f:
                json.dump(patterns_data, f, indent=2, default=str)
            
            return True
        except Exception as e:
            logger.error(f"error exporting patterns: {e}")
            return False
    
    def _pattern_to_dict(self, pattern: ClinicalPattern) -> Dict[str, Any]:
        """convert pattern to dictionary for serialization"""
        return {
            'pattern_id': pattern.pattern_id,
            'pattern_type': pattern.pattern_type,
            'frequency': pattern.frequency,
            'confidence': pattern.confidence,
            'characteristics': pattern.characteristics,
            'examples': pattern.examples,
            'metadata': pattern.metadata
        }
    
    def _cluster_to_dict(self, cluster: PatternCluster) -> Dict[str, Any]:
        """convert cluster to dictionary for serialization"""
        return {
            'cluster_id': cluster.cluster_id,
            'patterns': [self._pattern_to_dict(p) for p in cluster.patterns],
            'centroid': cluster.centroid,
            'size': cluster.size,
            'specialty': cluster.specialty,
            'difficulty_level': cluster.difficulty_level
        } 