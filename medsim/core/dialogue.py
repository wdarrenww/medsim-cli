"""
enhanced dialogue system with sophisticated patient communication and emotional modeling
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import random
import json


class EmotionalState(Enum):
    """enhanced emotional states"""
    CALM = "calm"
    ANXIOUS = "anxious"
    FEARFUL = "fearful"
    ANGRY = "angry"
    DEPRESSED = "depressed"
    CONFUSED = "confused"
    AGITATED = "agitated"
    HOPEFUL = "hopeful"
    RELIEVED = "relieved"
    PAIN = "pain"


class CommunicationStyle(Enum):
    """patient communication styles"""
    DIRECT = "direct"
    EVASIVE = "evasive"
    DETAILED = "detailed"
    VAGUE = "vague"
    COOPERATIVE = "cooperative"
    RESISTANT = "resistant"
    EMOTIONAL = "emotional"
    LOGICAL = "logical"


class PainLevel(Enum):
    """pain level descriptions"""
    NONE = "no pain"
    MILD = "mild discomfort"
    MODERATE = "moderate pain"
    SEVERE = "severe pain"
    EXCRUCIATING = "excruciating pain"


@dataclass
class PatientEmotion:
    """enhanced patient emotional state"""
    primary_emotion: EmotionalState
    intensity: float  # 0.0 to 1.0
    duration: timedelta
    triggers: List[str] = field(default_factory=list)
    coping_mechanisms: List[str] = field(default_factory=list)
    affects_communication: bool = True


@dataclass
class DialogueContext:
    """enhanced dialogue context"""
    patient_id: str
    current_emotion: PatientEmotion
    communication_style: CommunicationStyle
    pain_level: PainLevel
    trust_level: float  # 0.0 to 1.0
    understanding_level: float  # 0.0 to 1.0
    previous_topics: List[str] = field(default_factory=list)
    sensitive_topics: List[str] = field(default_factory=list)
    preferred_terms: Dict[str, str] = field(default_factory=dict)
    cultural_background: str = ""
    language_preference: str = "english"


@dataclass
class DialogueResponse:
    """enhanced dialogue response"""
    text: str
    emotion: EmotionalState
    confidence: float  # 0.0 to 1.0
    reveals_information: bool = False
    requires_followup: bool = False
    suggests_action: bool = False
    emotional_impact: float = 0.0  # -1.0 to 1.0


@dataclass
class ConversationHistory:
    """enhanced conversation history"""
    timestamp: datetime
    speaker: str  # "doctor" or "patient"
    message: str
    emotion: EmotionalState
    context_notes: str = ""
    followup_required: bool = False


class EnhancedDialogueEngine:
    """enhanced dialogue engine with sophisticated patient communication"""
    
    def __init__(self):
        self.conversations: Dict[str, List[ConversationHistory]] = {}
        self.patient_contexts: Dict[str, DialogueContext] = {}
        self.emotional_responses = self._initialize_emotional_responses()
        self.communication_patterns = self._initialize_communication_patterns()
        self.pain_responses = self._initialize_pain_responses()
    
    def _initialize_emotional_responses(self) -> Dict[EmotionalState, List[str]]:
        """initialize emotional response patterns"""
        responses = {}
        
        responses[EmotionalState.CALM] = [
            "I'm feeling okay today.",
            "I'm doing alright, thank you for asking.",
            "I feel pretty good right now.",
            "I'm managing well."
        ]
        
        responses[EmotionalState.ANXIOUS] = [
            "I'm a bit worried about what's happening.",
            "I feel nervous about the test results.",
            "I'm anxious about the procedure.",
            "I can't stop thinking about my symptoms."
        ]
        
        responses[EmotionalState.FEARFUL] = [
            "I'm scared about what this might be.",
            "I'm afraid of what the tests will show.",
            "I'm terrified about the surgery.",
            "I'm really frightened about my condition."
        ]
        
        responses[EmotionalState.ANGRY] = [
            "I'm frustrated with how long this is taking.",
            "I'm angry that no one seems to know what's wrong.",
            "I'm mad about the side effects of the medication.",
            "I'm upset about the cost of treatment."
        ]
        
        responses[EmotionalState.DEPRESSED] = [
            "I just don't feel like myself anymore.",
            "I'm so tired of being sick.",
            "I feel hopeless about getting better.",
            "I don't see the point of continuing treatment."
        ]
        
        responses[EmotionalState.CONFUSED] = [
            "I don't really understand what's happening.",
            "I'm confused about the treatment plan.",
            "I'm not sure what the doctor is telling me.",
            "I feel lost with all this medical jargon."
        ]
        
        responses[EmotionalState.AGITATED] = [
            "I can't sit still, I'm so restless.",
            "I'm feeling really worked up right now.",
            "I'm agitated and can't relax.",
            "I'm on edge and can't calm down."
        ]
        
        responses[EmotionalState.HOPEFUL] = [
            "I'm hopeful that the treatment will work.",
            "I feel optimistic about my recovery.",
            "I'm looking forward to getting better.",
            "I have hope that things will improve."
        ]
        
        responses[EmotionalState.RELIEVED] = [
            "I'm relieved to hear good news.",
            "I feel better knowing what's going on.",
            "I'm glad the test results were normal.",
            "I'm relieved the procedure went well."
        ]
        
        responses[EmotionalState.PAIN] = [
            "I'm in a lot of pain right now.",
            "The pain is really bad today.",
            "I can't get comfortable because of the pain.",
            "The pain is making it hard to function."
        ]
        
        return responses
    
    def _initialize_communication_patterns(self) -> Dict[CommunicationStyle, Dict[str, Any]]:
        """initialize communication style patterns"""
        patterns = {}
        
        patterns[CommunicationStyle.DIRECT] = {
            "responses": [
                "Yes, I have chest pain.",
                "No, I don't smoke.",
                "I take aspirin daily.",
                "The pain started yesterday."
            ],
            "question_style": "direct",
            "detail_level": "high",
            "cooperation": "high"
        }
        
        patterns[CommunicationStyle.EVASIVE] = {
            "responses": [
                "I'm not sure about that.",
                "Maybe, I don't really remember.",
                "I think so, but I'm not certain.",
                "I'd rather not talk about that."
            ],
            "question_style": "indirect",
            "detail_level": "low",
            "cooperation": "low"
        }
        
        patterns[CommunicationStyle.DETAILED] = {
            "responses": [
                "The pain started exactly at 3:45 PM yesterday while I was walking up the stairs. It felt like pressure in my chest and radiated to my left arm. I also felt short of breath and sweaty.",
                "I take aspirin 81mg every morning, metoprolol 25mg twice daily, and atorvastatin 20mg at bedtime. I've been taking them for about 2 years now.",
                "My family history includes my father who had a heart attack at age 55, my mother has diabetes, and my brother has high blood pressure."
            ],
            "question_style": "detailed",
            "detail_level": "very_high",
            "cooperation": "high"
        }
        
        patterns[CommunicationStyle.VAGUE] = {
            "responses": [
                "I don't feel well.",
                "It hurts somewhere.",
                "I take some pills.",
                "I'm not sure when it started."
            ],
            "question_style": "vague",
            "detail_level": "very_low",
            "cooperation": "variable"
        }
        
        patterns[CommunicationStyle.COOPERATIVE] = {
            "responses": [
                "I'll do whatever you recommend.",
                "I want to get better, so I'll follow your advice.",
                "I'm willing to try any treatment you suggest.",
                "I trust your medical judgment."
            ],
            "question_style": "cooperative",
            "detail_level": "medium",
            "cooperation": "very_high"
        }
        
        patterns[CommunicationStyle.RESISTANT] = {
            "responses": [
                "I don't want to take that medication.",
                "I'm not sure I need this test.",
                "I'd rather not have that procedure.",
                "I think I know what's best for me."
            ],
            "question_style": "defensive",
            "detail_level": "low",
            "cooperation": "low"
        }
        
        patterns[CommunicationStyle.EMOTIONAL] = {
            "responses": [
                "I'm so scared about what's happening to me!",
                "I can't believe this is happening again!",
                "I'm really worried about my family!",
                "I feel like my life is falling apart!"
            ],
            "question_style": "emotional",
            "detail_level": "medium",
            "cooperation": "variable"
        }
        
        patterns[CommunicationStyle.LOGICAL] = {
            "responses": [
                "Based on my symptoms, I believe it could be related to my previous diagnosis.",
                "I've researched this condition and understand the treatment options.",
                "I'd like to discuss the risks and benefits of each approach.",
                "I prefer evidence-based treatments."
            ],
            "question_style": "analytical",
            "detail_level": "high",
            "cooperation": "high"
        }
        
        return patterns
    
    def _initialize_pain_responses(self) -> Dict[PainLevel, List[str]]:
        """initialize pain response patterns"""
        responses = {}
        
        responses[PainLevel.NONE] = [
            "I don't have any pain right now.",
            "I'm pain-free at the moment.",
            "No pain to report.",
            "I feel fine, no discomfort."
        ]
        
        responses[PainLevel.MILD] = [
            "I have a slight discomfort.",
            "It's just a mild ache.",
            "I notice a little tenderness.",
            "There's some minor discomfort."
        ]
        
        responses[PainLevel.MODERATE] = [
            "The pain is noticeable but manageable.",
            "It's moderately painful but I can function.",
            "I have moderate pain that's distracting.",
            "The pain is significant but not severe."
        ]
        
        responses[PainLevel.SEVERE] = [
            "The pain is really bad right now.",
            "I'm in severe pain and it's hard to focus.",
            "The pain is intense and affecting my daily activities.",
            "I'm experiencing severe pain that's very distressing."
        ]
        
        responses[PainLevel.EXCRUCIATING] = [
            "The pain is unbearable!",
            "I can't take this pain anymore!",
            "It's the worst pain I've ever experienced!",
            "I'm in excruciating pain and need help immediately!"
        ]
        
        return responses
    
    def initialize_patient_context(self, patient_id: str, emotional_state: EmotionalState = None,
                                 communication_style: CommunicationStyle = None) -> str:
        """initialize dialogue context for a patient"""
        if emotional_state is None:
            emotional_state = random.choice(list(EmotionalState))
        
        if communication_style is None:
            communication_style = random.choice(list(CommunicationStyle))
        
        pain_level = random.choice(list(PainLevel))
        trust_level = random.uniform(0.3, 1.0)
        understanding_level = random.uniform(0.2, 0.9)
        
        emotion = PatientEmotion(
            primary_emotion=emotional_state,
            intensity=random.uniform(0.3, 1.0),
            duration=timedelta(minutes=random.randint(30, 180)),
            triggers=["medical procedures", "uncertainty about diagnosis"],
            coping_mechanisms=["deep breathing", "positive thinking"],
            affects_communication=True
        )
        
        context = DialogueContext(
            patient_id=patient_id,
            current_emotion=emotion,
            communication_style=communication_style,
            pain_level=pain_level,
            trust_level=trust_level,
            understanding_level=understanding_level,
            sensitive_topics=["family history", "mental health", "substance use"],
            preferred_terms={"heart attack": "cardiac event", "cancer": "condition"},
            cultural_background=random.choice(["american", "hispanic", "asian", "african-american"]),
            language_preference="english"
        )
        
        self.patient_contexts[patient_id] = context
        
        if patient_id not in self.conversations:
            self.conversations[patient_id] = []
        
        return f"✓ Initialized dialogue context for patient {patient_id}"
    
    def get_patient_response(self, patient_id: str, doctor_message: str, 
                           question_type: str = "general") -> DialogueResponse:
        """generate a patient response to a doctor's message"""
        if patient_id not in self.patient_contexts:
            self.initialize_patient_context(patient_id)
        
        context = self.patient_contexts[patient_id]
        emotion = context.current_emotion
        style = context.communication_style
        
        # determine response based on question type and emotional state
        if question_type == "pain_assessment":
            response_text = self._generate_pain_response(context)
        elif question_type == "emotional_assessment":
            response_text = self._generate_emotional_response(context)
        elif question_type == "symptom_inquiry":
            response_text = self._generate_symptom_response(context, doctor_message)
        elif question_type == "treatment_discussion":
            response_text = self._generate_treatment_response(context, doctor_message)
        elif question_type == "medical_history":
            response_text = self._generate_history_response(context, doctor_message)
        else:
            response_text = self._generate_general_response(context, doctor_message)
        
        # adjust response based on communication style
        response_text = self._apply_communication_style(response_text, style)
        
        # determine emotional impact
        emotional_impact = self._calculate_emotional_impact(doctor_message, context)
        
        # update emotional state based on interaction
        self._update_emotional_state(context, emotional_impact)
        
        # record conversation
        self._record_conversation(patient_id, "doctor", doctor_message, emotion.primary_emotion)
        self._record_conversation(patient_id, "patient", response_text, emotion.primary_emotion)
        
        return DialogueResponse(
            text=response_text,
            emotion=emotion.primary_emotion,
            confidence=random.uniform(0.7, 1.0),
            reveals_information=random.choice([True, False]),
            requires_followup=random.choice([True, False]),
            suggests_action=random.choice([True, False]),
            emotional_impact=emotional_impact
        )
    
    def _generate_pain_response(self, context: DialogueContext) -> str:
        """generate pain assessment response"""
        pain_responses = self.pain_responses[context.pain_level]
        base_response = random.choice(pain_responses)
        
        if context.pain_level in [PainLevel.SEVERE, PainLevel.EXCRUCIATING]:
            base_response += " I really need something for the pain."
        
        return base_response
    
    def _generate_emotional_response(self, context: DialogueContext) -> str:
        """generate emotional assessment response"""
        emotion_responses = self.emotional_responses[context.current_emotion.primary_emotion]
        return random.choice(emotion_responses)
    
    def _generate_symptom_response(self, context: DialogueContext, doctor_message: str) -> str:
        """generate symptom inquiry response"""
        if "chest pain" in doctor_message.lower():
            if context.current_emotion.primary_emotion in [EmotionalState.FEARFUL, EmotionalState.ANXIOUS]:
                return "Yes, I have chest pain and I'm really worried about it. It feels like pressure and sometimes radiates to my arm."
            else:
                return "Yes, I have some chest pain. It's been on and off for the past few hours."
        
        elif "shortness of breath" in doctor_message.lower():
            return "I do feel short of breath, especially when I walk or climb stairs."
        
        elif "fever" in doctor_message.lower():
            return "I think I might have a fever. I feel hot and sweaty."
        
        else:
            return "I'm not sure about that symptom. Can you be more specific?"
    
    def _generate_treatment_response(self, context: DialogueContext, doctor_message: str) -> str:
        """generate treatment discussion response"""
        if context.communication_style == CommunicationStyle.COOPERATIVE:
            return "I'm willing to try whatever treatment you recommend. I trust your medical judgment."
        elif context.communication_style == CommunicationStyle.RESISTANT:
            return "I'm not sure I want that treatment. Are there other options?"
        elif context.communication_style == CommunicationStyle.LOGICAL:
            return "I'd like to understand the risks and benefits of this treatment before deciding."
        else:
            return "I'll think about it and let you know."
    
    def _generate_history_response(self, context: DialogueContext, doctor_message: str) -> str:
        """generate medical history response"""
        if context.communication_style == CommunicationStyle.DETAILED:
            return "My father had a heart attack at age 55, my mother has diabetes, and I have high blood pressure myself."
        elif context.communication_style == CommunicationStyle.EVASIVE:
            return "I'm not sure about my family history. I don't really know much about that."
        else:
            return "My family has some history of heart disease and diabetes."
    
    def _generate_general_response(self, context: DialogueContext, doctor_message: str) -> str:
        """generate general response"""
        if context.current_emotion.primary_emotion == EmotionalState.ANXIOUS:
            return "I'm feeling a bit nervous about all of this. Can you explain what's happening?"
        elif context.current_emotion.primary_emotion == EmotionalState.PAIN:
            return "I'm in pain and really need help. Can you do something about it?"
        else:
            return "I understand. What do you recommend?"
    
    def _apply_communication_style(self, response: str, style: CommunicationStyle) -> str:
        """apply communication style to response"""
        patterns = self.communication_patterns[style]
        
        if style == CommunicationStyle.EMOTIONAL:
            response += " I'm really emotional about this!"
        elif style == CommunicationStyle.VAGUE:
            response = response.replace("chest pain", "discomfort")
            response = response.replace("severe", "some")
        
        return response
    
    def _calculate_emotional_impact(self, message: str, context: DialogueContext) -> float:
        """calculate emotional impact of doctor's message"""
        impact = 0.0
        
        # positive words
        positive_words = ["good", "better", "improving", "reassuring", "normal", "fine"]
        for word in positive_words:
            if word in message.lower():
                impact += 0.2
        
        # negative words
        negative_words = ["serious", "urgent", "emergency", "critical", "dangerous", "worrying"]
        for word in negative_words:
            if word in message.lower():
                impact -= 0.3
        
        # question types
        if "how are you feeling" in message.lower():
            impact += 0.1  # shows concern
        elif "pain" in message.lower():
            impact -= 0.1  # reminds of pain
        
        return max(-1.0, min(1.0, impact))
    
    def _update_emotional_state(self, context: DialogueContext, emotional_impact: float):
        """update patient's emotional state based on interaction"""
        current_emotion = context.current_emotion.primary_emotion
        
        if emotional_impact > 0.3:
            # positive impact
            if current_emotion in [EmotionalState.ANXIOUS, EmotionalState.FEARFUL]:
                context.current_emotion.primary_emotion = EmotionalState.HOPEFUL
            elif current_emotion == EmotionalState.PAIN:
                context.current_emotion.primary_emotion = EmotionalState.RELIEVED
        elif emotional_impact < -0.3:
            # negative impact
            if current_emotion in [EmotionalState.CALM, EmotionalState.HOPEFUL]:
                context.current_emotion.primary_emotion = EmotionalState.ANXIOUS
            elif current_emotion == EmotionalState.RELIEVED:
                context.current_emotion.primary_emotion = EmotionalState.FEARFUL
        
        # update intensity
        context.current_emotion.intensity = max(0.1, min(1.0, 
            context.current_emotion.intensity + emotional_impact * 0.2))
    
    def _record_conversation(self, patient_id: str, speaker: str, message: str, emotion: EmotionalState):
        """record conversation history"""
        history_entry = ConversationHistory(
            timestamp=datetime.now(),
            speaker=speaker,
            message=message,
            emotion=emotion
        )
        
        self.conversations[patient_id].append(history_entry)
    
    def get_conversation_history(self, patient_id: str) -> List[ConversationHistory]:
        """get conversation history for a patient"""
        return self.conversations.get(patient_id, [])
    
    def get_patient_context(self, patient_id: str) -> Optional[DialogueContext]:
        """get patient dialogue context"""
        return self.patient_contexts.get(patient_id)
    
    def update_patient_emotion(self, patient_id: str, emotion: EmotionalState, intensity: float = None):
        """update patient's emotional state"""
        if patient_id in self.patient_contexts:
            context = self.patient_contexts[patient_id]
            context.current_emotion.primary_emotion = emotion
            if intensity is not None:
                context.current_emotion.intensity = intensity
    
    def get_emotional_summary(self, patient_id: str) -> Dict[str, Any]:
        """get emotional summary for a patient"""
        if patient_id not in self.patient_contexts:
            return {"error": "Patient context not found"}
        
        context = self.patient_contexts[patient_id]
        return {
            'current_emotion': context.current_emotion.primary_emotion.value,
            'emotion_intensity': context.current_emotion.intensity,
            'communication_style': context.communication_style.value,
            'pain_level': context.pain_level.value,
            'trust_level': context.trust_level,
            'understanding_level': context.understanding_level,
            'conversation_count': len(self.conversations.get(patient_id, []))
        } 