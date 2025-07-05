"""
advanced scripted dialogue system with context-aware responses and emotional states
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import random
import json


@dataclass
class PatientEmotionalState:
    """patient emotional state affecting dialogue responses"""
    anxiety_level: float = 0.0  # 0-1 scale
    pain_level: float = 0.0  # 0-1 scale
    trust_level: float = 0.5  # 0-1 scale
    cooperation_level: float = 0.7  # 0-1 scale
    confusion_level: float = 0.0  # 0-1 scale
    frustration_level: float = 0.0  # 0-1 scale
    
    def update_from_interaction(self, interaction_type: str, quality: float) -> None:
        """update emotional state based on interaction quality"""
        if interaction_type == "reassurance":
            self.anxiety_level = max(0, self.anxiety_level - quality * 0.3)
            self.trust_level = min(1.0, self.trust_level + quality * 0.2)
        elif interaction_type == "explanation":
            self.confusion_level = max(0, self.confusion_level - quality * 0.4)
            self.trust_level = min(1.0, self.trust_level + quality * 0.15)
        elif interaction_type == "pain_management":
            self.pain_level = max(0, self.pain_level - quality * 0.5)
            self.cooperation_level = min(1.0, self.cooperation_level + quality * 0.3)
        elif interaction_type == "rushed_interaction":
            self.frustration_level = min(1.0, self.frustration_level + 0.3)
            self.trust_level = max(0, self.trust_level - 0.2)
        elif interaction_type == "ignored_concerns":
            self.frustration_level = min(1.0, self.frustration_level + 0.4)
            self.cooperation_level = max(0, self.cooperation_level - 0.3)


@dataclass
class DialogueContext:
    """context for dialogue responses"""
    question_type: str = ""
    previous_questions: List[str] = field(default_factory=list)
    patient_condition: Dict[str, Any] = field(default_factory=dict)
    time_elapsed: float = 0.0
    interventions_performed: List[str] = field(default_factory=list)
    medications_given: List[str] = field(default_factory=list)
    tests_ordered: List[str] = field(default_factory=list)
    emotional_state: PatientEmotionalState = field(default_factory=PatientEmotionalState)


class AdvancedDialogueSystem:
    """advanced dialogue system with context-aware responses"""
    
    def __init__(self):
        self.patient_profiles = self._load_patient_profiles()
        self.response_templates = self._load_response_templates()
        self.emotional_modifiers = self._load_emotional_modifiers()
        self.context_history = []
        self.conversation_flow = []
        
    def _load_patient_profiles(self) -> Dict[str, Dict[str, Any]]:
        """load patient personality profiles"""
        return {
            "cooperative": {
                "baseline_trust": 0.8,
                "baseline_cooperation": 0.9,
                "response_style": "detailed",
                "emotional_expression": "moderate",
                "medical_knowledge": "basic"
            },
            "anxious": {
                "baseline_trust": 0.4,
                "baseline_cooperation": 0.6,
                "response_style": "brief",
                "emotional_expression": "high",
                "medical_knowledge": "minimal"
            },
            "stoic": {
                "baseline_trust": 0.7,
                "baseline_cooperation": 0.8,
                "response_style": "minimal",
                "emotional_expression": "low",
                "medical_knowledge": "moderate"
            },
            "elderly": {
                "baseline_trust": 0.9,
                "baseline_cooperation": 0.95,
                "response_style": "detailed",
                "emotional_expression": "moderate",
                "medical_knowledge": "basic"
            },
            "pediatric": {
                "baseline_trust": 0.6,
                "baseline_cooperation": 0.7,
                "response_style": "simple",
                "emotional_expression": "high",
                "medical_knowledge": "minimal"
            }
        }
    
    def _load_response_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """load response templates for different question types"""
        return {
            "pain_assessment": {
                "cooperative": [
                    "The pain is about a {intensity} out of 10. It's {location} and feels {quality}.",
                    "I'd say it's a {intensity}/10. {location} hurts the most, and it's {quality}.",
                    "The pain is {intensity}/10. It's in my {location} and feels {quality}."
                ],
                "anxious": [
                    "It really hurts! Like a {intensity}/10. My {location} is {quality}.",
                    "The pain is terrible, maybe {intensity}/10. My {location} feels {quality}.",
                    "It's so painful! {intensity}/10. My {location} is {quality}."
                ],
                "stoic": [
                    "Pain level {intensity}/10. {location}. {quality}.",
                    "{intensity}/10. {location}. {quality}.",
                    "Pain: {intensity}/10. {location}. {quality}."
                ]
            },
            "symptom_inquiry": {
                "cooperative": [
                    "I've been experiencing {symptoms} for about {duration}.",
                    "The symptoms started {duration} ago. I have {symptoms}.",
                    "I've had {symptoms} for {duration} now."
                ],
                "anxious": [
                    "I'm really worried about {symptoms}. It's been {duration}.",
                    "I have {symptoms} and it's been {duration}. I'm scared.",
                    "These {symptoms} started {duration} ago. I'm very concerned."
                ],
                "stoic": [
                    "{symptoms}. {duration}.",
                    "Symptoms: {symptoms}. Duration: {duration}.",
                    "{symptoms} for {duration}."
                ]
            },
            "medical_history": {
                "cooperative": [
                    "I have a history of {conditions}. I take {medications}.",
                    "My medical history includes {conditions}. Current medications: {medications}.",
                    "I've had {conditions} in the past. I'm on {medications}."
                ],
                "anxious": [
                    "I have {conditions} and take {medications}. I'm worried about my health.",
                    "My medical history: {conditions}. Medications: {medications}. I'm concerned.",
                    "I have {conditions} and take {medications}. I'm very anxious about this."
                ],
                "stoic": [
                    "History: {conditions}. Meds: {medications}.",
                    "{conditions}. {medications}.",
                    "Medical: {conditions}. Current: {medications}."
                ]
            },
            "allergies": {
                "cooperative": [
                    "I'm allergic to {allergies}. I had {reactions}.",
                    "My allergies include {allergies}. The reactions were {reactions}.",
                    "I'm allergic to {allergies}. I experienced {reactions}."
                ],
                "anxious": [
                    "I'm very allergic to {allergies}! I had {reactions}.",
                    "I'm allergic to {allergies}. The reactions were {reactions}. I'm worried.",
                    "I have severe allergies to {allergies}. I had {reactions}."
                ],
                "stoic": [
                    "Allergies: {allergies}. Reactions: {reactions}.",
                    "{allergies}. {reactions}.",
                    "Allergic to {allergies}. {reactions}."
                ]
            },
            "social_history": {
                "cooperative": [
                    "I work as a {occupation}. I {smoking_status} and {alcohol_use}.",
                    "I'm a {occupation}. I {smoking_status} and {alcohol_use}.",
                    "I work in {occupation}. I {smoking_status} and {alcohol_use}."
                ],
                "anxious": [
                    "I'm a {occupation}. I {smoking_status} and {alcohol_use}. I'm worried about my job.",
                    "I work as a {occupation}. I {smoking_status} and {alcohol_use}. I'm concerned.",
                    "I'm a {occupation}. I {smoking_status} and {alcohol_use}. I'm anxious about this."
                ],
                "stoic": [
                    "Occupation: {occupation}. Smoking: {smoking_status}. Alcohol: {alcohol_use}.",
                    "{occupation}. {smoking_status}. {alcohol_use}.",
                    "Work: {occupation}. {smoking_status}. {alcohol_use}."
                ]
            },
            "family_history": {
                "cooperative": [
                    "My family has a history of {conditions}. My {relation} had {specific_condition}.",
                    "In my family, we have {conditions}. My {relation} had {specific_condition}.",
                    "Family history includes {conditions}. My {relation} had {specific_condition}."
                ],
                "anxious": [
                    "My family has {conditions}. My {relation} had {specific_condition}. I'm worried.",
                    "In my family: {conditions}. My {relation} had {specific_condition}. I'm concerned.",
                    "Family history: {conditions}. My {relation} had {specific_condition}. I'm anxious."
                ],
                "stoic": [
                    "Family: {conditions}. {relation}: {specific_condition}.",
                    "{conditions}. {relation}: {specific_condition}.",
                    "Family history: {conditions}. {relation}: {specific_condition}."
                ]
            },
            "current_medications": {
                "cooperative": [
                    "I'm currently taking {medications} for {reasons}.",
                    "My current medications are {medications}. They're for {reasons}.",
                    "I take {medications} for {reasons}."
                ],
                "anxious": [
                    "I'm on {medications} for {reasons}. I'm worried about side effects.",
                    "I take {medications} for {reasons}. I'm concerned about interactions.",
                    "My medications are {medications} for {reasons}. I'm anxious about this."
                ],
                "stoic": [
                    "Meds: {medications}. For: {reasons}.",
                    "{medications}. {reasons}.",
                    "Current: {medications}. Reason: {reasons}."
                ]
            },
            "last_oral_intake": {
                "cooperative": [
                    "I last ate {food} about {time} ago. I drank {fluids}.",
                    "I had {food} {time} ago. I also had {fluids}.",
                    "Last meal was {food} {time} ago. I drank {fluids}."
                ],
                "anxious": [
                    "I ate {food} {time} ago. I had {fluids}. I'm worried about surgery.",
                    "Last meal: {food} {time} ago. Fluids: {fluids}. I'm concerned.",
                    "I had {food} {time} ago and {fluids}. I'm anxious about this."
                ],
                "stoic": [
                    "Last meal: {food} {time} ago. Fluids: {fluids}.",
                    "{food} {time} ago. {fluids}.",
                    "Food: {food} {time} ago. Drinks: {fluids}."
                ]
            },
            "events_leading": {
                "cooperative": [
                    "I was {activity} when {event} happened. Then I felt {symptoms}.",
                    "I was {activity} and then {event} occurred. I developed {symptoms}.",
                    "While {activity}, {event} happened. I started having {symptoms}."
                ],
                "anxious": [
                    "I was {activity} when {event} happened! I got {symptoms} and I'm scared.",
                    "I was {activity} and {event} occurred. I developed {symptoms}. I'm worried.",
                    "While {activity}, {event} happened. I felt {symptoms}. I'm very concerned."
                ],
                "stoic": [
                    "Activity: {activity}. Event: {event}. Symptoms: {symptoms}.",
                    "{activity}. {event}. {symptoms}.",
                    "Was {activity}. {event}. Then {symptoms}."
                ]
            }
        }
    
    def _load_emotional_modifiers(self) -> Dict[str, Dict[str, str]]:
        """load emotional modifiers for responses"""
        return {
            "high_anxiety": {
                "prefix": ["I'm really worried about...", "I'm scared that...", "I'm very concerned about..."],
                "suffix": ["...and I'm very anxious.", "...this is really frightening.", "...I'm quite worried."]
            },
            "high_pain": {
                "prefix": ["The pain is really bad...", "It hurts so much...", "The pain is terrible..."],
                "suffix": ["...and it's getting worse.", "...I can't take much more.", "...it's unbearable."]
            },
            "low_trust": {
                "prefix": ["I'm not sure...", "I don't know if...", "I'm hesitant to..."],
                "suffix": ["...but I'm not convinced.", "...I'm still worried.", "...I'm not sure this will help."]
            },
            "high_frustration": {
                "prefix": ["I've already told you...", "I don't understand why...", "This is taking too long..."],
                "suffix": ["...and I'm getting frustrated.", "...this is ridiculous.", "...I'm tired of this."]
            },
            "confusion": {
                "prefix": ["I don't really understand...", "I'm confused about...", "I'm not sure what..."],
                "suffix": ["...can you explain that again?", "...I'm still confused.", "...I need clarification."]
            }
        }
    
    def get_patient_response(self, question: str, context: DialogueContext, 
                           patient_profile: str = "cooperative") -> str:
        """generate context-aware patient response"""
        # determine question type
        question_type = self._classify_question(question)
        
        # update emotional state based on interaction
        self._update_emotional_state(context, question_type)
        
        # get base response template
        response = self._get_base_response(question_type, patient_profile, context)
        
        # apply emotional modifiers
        response = self._apply_emotional_modifiers(response, context.emotional_state)
        
        # add context-specific details
        response = self._add_context_details(response, context, question_type)
        
        # record interaction
        self._record_interaction(question, response, context)
        
        return response
    
    def _classify_question(self, question: str) -> str:
        """classify the type of question being asked"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["pain", "hurt", "ache", "discomfort"]):
            return "pain_assessment"
        elif any(word in question_lower for word in ["symptom", "feel", "experience", "notice"]):
            return "symptom_inquiry"
        elif any(word in question_lower for word in ["history", "medical history", "past"]):
            return "medical_history"
        elif any(word in question_lower for word in ["allergy", "allergic", "reaction"]):
            return "allergies"
        elif any(word in question_lower for word in ["work", "job", "occupation", "smoke", "drink", "alcohol"]):
            return "social_history"
        elif any(word in question_lower for word in ["family", "parent", "sibling", "relative"]):
            return "family_history"
        elif any(word in question_lower for word in ["medication", "medicine", "pill", "drug"]):
            return "current_medications"
        elif any(word in question_lower for word in ["eat", "food", "meal", "drink", "last"]):
            return "last_oral_intake"
        elif any(word in question_lower for word in ["happen", "occur", "event", "leading", "before"]):
            return "events_leading"
        else:
            return "general_inquiry"
    
    def _get_base_response(self, question_type: str, patient_profile: str, 
                          context: DialogueContext) -> str:
        """get base response template"""
        if question_type not in self.response_templates:
            return "I'm not sure how to answer that."
        
        templates = self.response_templates[question_type].get(patient_profile, 
                    self.response_templates[question_type]["cooperative"])
        
        return random.choice(templates)
    
    def _update_emotional_state(self, context: DialogueContext, question_type: str) -> None:
        """update emotional state based on interaction"""
        # increase anxiety for medical questions
        if question_type in ["medical_history", "allergies", "current_medications"]:
            context.emotional_state.anxiety_level = min(1.0, context.emotional_state.anxiety_level + 0.1)
        
        # increase pain awareness for pain questions
        if question_type == "pain_assessment":
            context.emotional_state.pain_level = min(1.0, context.emotional_state.pain_level + 0.2)
        
        # increase confusion for complex questions
        if question_type in ["family_history", "events_leading"]:
            context.emotional_state.confusion_level = min(1.0, context.emotional_state.confusion_level + 0.15)
    
    def _apply_emotional_modifiers(self, response: str, emotional_state: PatientEmotionalState) -> str:
        """apply emotional modifiers to response"""
        modifiers = []
        
        if emotional_state.anxiety_level > 0.7:
            modifiers.append(random.choice(self.emotional_modifiers["high_anxiety"]["prefix"]))
        if emotional_state.pain_level > 0.8:
            modifiers.append(random.choice(self.emotional_modifiers["high_pain"]["prefix"]))
        if emotional_state.trust_level < 0.3:
            modifiers.append(random.choice(self.emotional_modifiers["low_trust"]["prefix"]))
        if emotional_state.frustration_level > 0.6:
            modifiers.append(random.choice(self.emotional_modifiers["high_frustration"]["prefix"]))
        if emotional_state.confusion_level > 0.5:
            modifiers.append(random.choice(self.emotional_modifiers["confusion"]["prefix"]))
        
        # apply prefix modifiers
        if modifiers:
            response = " ".join(modifiers) + " " + response
        
        # apply suffix modifiers
        suffix_modifiers = []
        if emotional_state.anxiety_level > 0.6:
            suffix_modifiers.append(random.choice(self.emotional_modifiers["high_anxiety"]["suffix"]))
        if emotional_state.pain_level > 0.7:
            suffix_modifiers.append(random.choice(self.emotional_modifiers["high_pain"]["suffix"]))
        if emotional_state.trust_level < 0.4:
            suffix_modifiers.append(random.choice(self.emotional_modifiers["low_trust"]["suffix"]))
        if emotional_state.frustration_level > 0.5:
            suffix_modifiers.append(random.choice(self.emotional_modifiers["high_frustration"]["suffix"]))
        if emotional_state.confusion_level > 0.4:
            suffix_modifiers.append(random.choice(self.emotional_modifiers["confusion"]["suffix"]))
        
        if suffix_modifiers:
            response += " " + " ".join(suffix_modifiers)
        
        return response
    
    def _add_context_details(self, response: str, context: DialogueContext, 
                           question_type: str) -> str:
        """add context-specific details to response"""
        # fill in template variables based on context
        if question_type == "pain_assessment":
            response = response.format(
                intensity=random.randint(3, 8),
                location=random.choice(["chest", "abdomen", "head", "back", "arm", "leg"]),
                quality=random.choice(["sharp", "dull", "throbbing", "burning", "cramping", "aching"])
            )
        elif question_type == "symptom_inquiry":
            response = response.format(
                symptoms=random.choice(["nausea", "dizziness", "shortness of breath", "chest pain", "headache"]),
                duration=random.choice(["a few hours", "several days", "about a week", "since this morning"])
            )
        elif question_type == "medical_history":
            response = response.format(
                conditions=random.choice(["hypertension", "diabetes", "asthma", "depression", "arthritis"]),
                medications=random.choice(["lisinopril", "metformin", "albuterol", "sertraline", "ibuprofen"])
            )
        elif question_type == "allergies":
            response = response.format(
                allergies=random.choice(["penicillin", "sulfa drugs", "aspirin", "latex", "peanuts"]),
                reactions=random.choice(["rash", "swelling", "difficulty breathing", "hives", "nausea"])
            )
        elif question_type == "social_history":
            response = response.format(
                occupation=random.choice(["teacher", "construction worker", "nurse", "retired", "student"]),
                smoking_status=random.choice(["don't smoke", "quit 5 years ago", "smoke occasionally", "never smoked"]),
                alcohol_use=random.choice(["don't drink", "occasionally", "socially", "rarely"])
            )
        elif question_type == "family_history":
            response = response.format(
                conditions=random.choice(["heart disease", "diabetes", "cancer", "hypertension", "asthma"]),
                relation=random.choice(["father", "mother", "sister", "brother", "grandfather"]),
                specific_condition=random.choice(["heart attack", "diabetes", "lung cancer", "stroke", "breast cancer"])
            )
        elif question_type == "current_medications":
            response = response.format(
                medications=random.choice(["lisinopril", "metformin", "aspirin", "atorvastatin", "omeprazole"]),
                reasons=random.choice(["high blood pressure", "diabetes", "heart disease", "acid reflux", "cholesterol"])
            )
        elif question_type == "last_oral_intake":
            response = response.format(
                food=random.choice(["sandwich", "pizza", "salad", "soup", "breakfast"]),
                time=random.choice(["2 hours", "4 hours", "6 hours", "8 hours", "12 hours"]),
                fluids=random.choice(["water", "coffee", "soda", "juice", "tea"])
            )
        elif question_type == "events_leading":
            response = response.format(
                activity=random.choice(["working", "exercising", "sleeping", "eating", "driving"]),
                event=random.choice(["I felt chest pain", "I became dizzy", "I fell", "I had trouble breathing", "I felt nauseous"]),
                symptoms=random.choice(["chest pain", "shortness of breath", "dizziness", "nausea", "sweating"])
            )
        
        return response
    
    def _record_interaction(self, question: str, response: str, context: DialogueContext) -> None:
        """record the interaction for conversation history"""
        self.conversation_flow.append({
            'timestamp': context.time_elapsed,
            'question': question,
            'response': response,
            'emotional_state': {
                'anxiety': context.emotional_state.anxiety_level,
                'pain': context.emotional_state.pain_level,
                'trust': context.emotional_state.trust_level,
                'cooperation': context.emotional_state.cooperation_level,
                'confusion': context.emotional_state.confusion_level,
                'frustration': context.emotional_state.frustration_level
            }
        })
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """get summary of conversation flow and emotional progression"""
        if not self.conversation_flow:
            return {"message": "No conversation recorded yet."}
        
        return {
            'total_interactions': len(self.conversation_flow),
            'emotional_progression': self._analyze_emotional_progression(),
            'conversation_flow': self.conversation_flow[-5:],  # last 5 interactions
            'overall_emotional_state': self._get_overall_emotional_state()
        }
    
    def _analyze_emotional_progression(self) -> Dict[str, List[float]]:
        """analyze how emotional states changed over time"""
        progression = {
            'anxiety': [],
            'pain': [],
            'trust': [],
            'cooperation': [],
            'confusion': [],
            'frustration': []
        }
        
        for interaction in self.conversation_flow:
            emotional_state = interaction['emotional_state']
            for key in progression:
                progression[key].append(emotional_state[key])
        
        return progression
    
    def _get_overall_emotional_state(self) -> Dict[str, float]:
        """get average emotional state across all interactions"""
        if not self.conversation_flow:
            return {}
        
        latest = self.conversation_flow[-1]['emotional_state']
        return latest
    
    def reset_conversation(self) -> None:
        """reset conversation history"""
        self.conversation_flow.clear()
        self.context_history.clear() 