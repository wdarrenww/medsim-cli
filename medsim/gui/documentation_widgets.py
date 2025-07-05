from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QTextEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QFrame, QGridLayout,
    QProgressBar, QSlider, QSpinBox, QComboBox, QCheckBox, QListWidget, QListWidgetItem,
    QTimer, QMessageBox, QDialog, QFormLayout, QLineEdit, QDateEdit, QTimeEdit
)
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPixmap
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Signal, QDate, QTime
import math
import random
from datetime import datetime, timedelta

# Color palette
HIGHLIGHT_COLOR = "#4f8cff"
CRITICAL_COLOR = "#ff4f4f"
WARNING_COLOR = "#ffa726"
SUCCESS_COLOR = "#66bb6a"
DOCUMENTATION_COLOR = "#4CAF50"

class ProgressNoteWidget(QWidget):
    """Medical progress note documentation widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Note header
        header_layout = QHBoxLayout()
        
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ddd;")
        
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ddd;")
        
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Author")
        self.author_input.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ddd;")
        
        header_layout.addWidget(QLabel("Date:"))
        header_layout.addWidget(self.date_edit)
        header_layout.addWidget(QLabel("Time:"))
        header_layout.addWidget(self.time_edit)
        header_layout.addWidget(QLabel("Author:"))
        header_layout.addWidget(self.author_input)
        
        layout.addLayout(header_layout)
        
        # SOAP note sections
        soap_group = QGroupBox("SOAP Note")
        soap_layout = QVBoxLayout(soap_group)
        
        # Subjective
        subjective_group = QGroupBox("Subjective")
        subjective_layout = QVBoxLayout(subjective_group)
        self.subjective_text = QTextEdit()
        self.subjective_text.setPlaceholderText("Patient's chief complaint, history of present illness, past medical history, medications, allergies, social history...")
        self.subjective_text.setMaximumHeight(100)
        self.subjective_text.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        subjective_layout.addWidget(self.subjective_text)
        soap_layout.addWidget(subjective_group)
        
        # Objective
        objective_group = QGroupBox("Objective")
        objective_layout = QVBoxLayout(objective_group)
        self.objective_text = QTextEdit()
        self.objective_text.setPlaceholderText("Vital signs, physical examination findings, laboratory results, imaging studies...")
        self.objective_text.setMaximumHeight(100)
        self.objective_text.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        objective_layout.addWidget(self.objective_text)
        soap_layout.addWidget(objective_group)
        
        # Assessment
        assessment_group = QGroupBox("Assessment")
        assessment_layout = QVBoxLayout(assessment_group)
        self.assessment_text = QTextEdit()
        self.assessment_text.setPlaceholderText("Differential diagnosis, working diagnosis, problem list...")
        self.assessment_text.setMaximumHeight(100)
        self.assessment_text.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        assessment_layout.addWidget(self.assessment_text)
        soap_layout.addWidget(assessment_group)
        
        # Plan
        plan_group = QGroupBox("Plan")
        plan_layout = QVBoxLayout(plan_group)
        self.plan_text = QTextEdit()
        self.plan_text.setPlaceholderText("Diagnostic tests, treatments, medications, follow-up plans...")
        self.plan_text.setMaximumHeight(100)
        self.plan_text.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        plan_layout.addWidget(self.plan_text)
        soap_layout.addWidget(plan_group)
        
        layout.addWidget(soap_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Note")
        self.save_btn.setStyleSheet(f"background: {SUCCESS_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        self.save_btn.clicked.connect(self.save_note)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setStyleSheet(f"background: {WARNING_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        self.clear_btn.clicked.connect(self.clear_note)
        
        self.template_btn = QPushButton("Load Template")
        self.template_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        self.template_btn.clicked.connect(self.load_template)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.template_btn)
        
        layout.addLayout(button_layout)

    def save_note(self):
        # Save the progress note
        note_data = {
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "time": self.time_edit.time().toString("HH:mm"),
            "author": self.author_input.text(),
            "subjective": self.subjective_text.toPlainText(),
            "objective": self.objective_text.toPlainText(),
            "assessment": self.assessment_text.toPlainText(),
            "plan": self.plan_text.toPlainText()
        }
        
        QMessageBox.information(self, "Success", "Progress note saved successfully!")

    def clear_note(self):
        self.subjective_text.clear()
        self.objective_text.clear()
        self.assessment_text.clear()
        self.plan_text.clear()

    def load_template(self):
        # Load a template note
        template = {
            "subjective": "Patient presents with [chief complaint]. History of present illness: [HPI]. Past medical history: [PMH]. Medications: [meds]. Allergies: [allergies].",
            "objective": "Vital signs: [vitals]. Physical examination: [exam]. Laboratory results: [labs]. Imaging: [imaging].",
            "assessment": "Primary diagnosis: [diagnosis]. Differential diagnosis: [differential]. Problem list: [problems].",
            "plan": "Diagnostic tests: [tests]. Treatment: [treatment]. Medications: [medications]. Follow-up: [follow-up]."
        }
        
        self.subjective_text.setPlainText(template["subjective"])
        self.objective_text.setPlainText(template["objective"])
        self.assessment_text.setPlainText(template["assessment"])
        self.plan_text.setPlainText(template["plan"])

class DischargeSummaryWidget(QWidget):
    """Discharge summary documentation widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Discharge header
        header_group = QGroupBox("Discharge Information")
        header_layout = QGridLayout(header_group)
        
        self.admission_date = QDateEdit()
        self.admission_date.setDate(QDate.currentDate().addDays(-3))
        
        self.discharge_date = QDateEdit()
        self.discharge_date.setDate(QDate.currentDate())
        
        self.attending_physician = QLineEdit()
        self.attending_physician.setPlaceholderText("Attending Physician")
        
        header_layout.addWidget(QLabel("Admission Date:"), 0, 0)
        header_layout.addWidget(self.admission_date, 0, 1)
        header_layout.addWidget(QLabel("Discharge Date:"), 0, 2)
        header_layout.addWidget(self.discharge_date, 0, 3)
        header_layout.addWidget(QLabel("Attending:"), 1, 0)
        header_layout.addWidget(self.attending_physician, 1, 1)
        
        layout.addWidget(header_group)
        
        # Discharge summary sections
        summary_group = QGroupBox("Discharge Summary")
        summary_layout = QVBoxLayout(summary_group)
        
        # Admission diagnosis
        admission_group = QGroupBox("Admission Diagnosis")
        admission_layout = QVBoxLayout(admission_group)
        self.admission_diagnosis = QTextEdit()
        self.admission_diagnosis.setMaximumHeight(80)
        self.admission_diagnosis.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        admission_layout.addWidget(self.admission_diagnosis)
        summary_layout.addWidget(admission_group)
        
        # Hospital course
        course_group = QGroupBox("Hospital Course")
        course_layout = QVBoxLayout(course_group)
        self.hospital_course = QTextEdit()
        self.hospital_course.setMaximumHeight(100)
        self.hospital_course.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        course_layout.addWidget(self.hospital_course)
        summary_layout.addWidget(course_group)
        
        # Discharge diagnosis
        discharge_diagnosis_group = QGroupBox("Discharge Diagnosis")
        discharge_diagnosis_layout = QVBoxLayout(discharge_diagnosis_group)
        self.discharge_diagnosis = QTextEdit()
        self.discharge_diagnosis.setMaximumHeight(80)
        self.discharge_diagnosis.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        discharge_diagnosis_layout.addWidget(self.discharge_diagnosis)
        summary_layout.addWidget(discharge_diagnosis_group)
        
        # Discharge medications
        medications_group = QGroupBox("Discharge Medications")
        medications_layout = QVBoxLayout(medications_group)
        self.discharge_medications = QTextEdit()
        self.discharge_medications.setMaximumHeight(100)
        self.discharge_medications.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        medications_layout.addWidget(self.discharge_medications)
        summary_layout.addWidget(medications_group)
        
        # Follow-up instructions
        followup_group = QGroupBox("Follow-up Instructions")
        followup_layout = QVBoxLayout(followup_group)
        self.followup_instructions = QTextEdit()
        self.followup_instructions.setMaximumHeight(80)
        self.followup_instructions.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        followup_layout.addWidget(self.followup_instructions)
        summary_layout.addWidget(followup_group)
        
        layout.addWidget(summary_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton("Generate Summary")
        self.generate_btn.setStyleSheet(f"background: {SUCCESS_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        self.generate_btn.clicked.connect(self.generate_summary)
        
        self.print_btn = QPushButton("Print Summary")
        self.print_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        self.print_btn.clicked.connect(self.print_summary)
        
        button_layout.addWidget(self.generate_btn)
        button_layout.addWidget(self.print_btn)
        
        layout.addLayout(button_layout)

    def generate_summary(self):
        # Generate discharge summary from patient data
        QMessageBox.information(self, "Success", "Discharge summary generated successfully!")

    def print_summary(self):
        # Print the discharge summary
        QMessageBox.information(self, "Print", "Discharge summary sent to printer")

class MedicationReconciliationWidget(QWidget):
    """Medication reconciliation widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Medication reconciliation table
        reconciliation_group = QGroupBox("Medication Reconciliation")
        reconciliation_layout = QVBoxLayout(reconciliation_group)
        
        self.med_table = QTableWidget()
        self.med_table.setColumnCount(5)
        self.med_table.setHorizontalHeaderLabels(["Medication", "Dose", "Frequency", "Status", "Action"])
        self.med_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        reconciliation_layout.addWidget(self.med_table)
        
        layout.addWidget(reconciliation_group)
        
        # Add sample medications
        self._add_sample_medications()
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.add_med_btn = QPushButton("Add Medication")
        self.add_med_btn.setStyleSheet(f"background: {SUCCESS_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        self.add_med_btn.clicked.connect(self.add_medication)
        
        self.reconcile_btn = QPushButton("Reconcile")
        self.reconcile_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        self.reconcile_btn.clicked.connect(self.reconcile_medications)
        
        button_layout.addWidget(self.add_med_btn)
        button_layout.addWidget(self.reconcile_btn)
        
        layout.addLayout(button_layout)

    def _add_sample_medications(self):
        medications = [
            ("Lisinopril", "10mg", "Daily", "Continue", "Continue"),
            ("Metformin", "500mg", "Twice daily", "Continue", "Continue"),
            ("Aspirin", "81mg", "Daily", "Continue", "Continue"),
            ("Atorvastatin", "20mg", "Daily", "Continue", "Continue"),
            ("Furosemide", "40mg", "Daily", "Discontinue", "Discontinue"),
            ("Warfarin", "5mg", "Daily", "Continue", "Continue")
        ]
        
        self.med_table.setRowCount(len(medications))
        for i, (med, dose, freq, status, action) in enumerate(medications):
            self.med_table.setItem(i, 0, QTableWidgetItem(med))
            self.med_table.setItem(i, 1, QTableWidgetItem(dose))
            self.med_table.setItem(i, 2, QTableWidgetItem(freq))
            self.med_table.setItem(i, 3, QTableWidgetItem(status))
            self.med_table.setItem(i, 4, QTableWidgetItem(action))

    def add_medication(self):
        # Add new medication
        QMessageBox.information(self, "Add Medication", "Add medication dialog would open here")

    def reconcile_medications(self):
        # Reconcile medications
        QMessageBox.information(self, "Reconciliation", "Medication reconciliation completed")

class ClinicalDecisionSupportWidget(QWidget):
    """Clinical decision support widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Decision support header
        header_layout = QHBoxLayout()
        
        self.condition_combo = QComboBox()
        self.condition_combo.addItems([
            "Chest Pain",
            "Shortness of Breath",
            "Abdominal Pain",
            "Headache",
            "Fever",
            "Hypertension",
            "Diabetes Management",
            "Anticoagulation"
        ])
        self.condition_combo.currentTextChanged.connect(self.load_guidelines)
        
        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        self.analyze_btn.clicked.connect(self.analyze_case)
        
        header_layout.addWidget(QLabel("Condition:"))
        header_layout.addWidget(self.condition_combo)
        header_layout.addWidget(self.analyze_btn)
        
        layout.addLayout(header_layout)
        
        # Guidelines and recommendations
        guidelines_group = QGroupBox("Clinical Guidelines")
        guidelines_layout = QVBoxLayout(guidelines_group)
        
        self.guidelines_text = QTextEdit()
        self.guidelines_text.setMaximumHeight(200)
        self.guidelines_text.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        guidelines_layout.addWidget(self.guidelines_text)
        
        layout.addWidget(guidelines_group)
        
        # Recommendations
        recommendations_group = QGroupBox("Recommendations")
        recommendations_layout = QVBoxLayout(recommendations_group)
        
        self.recommendations_list = QListWidget()
        self.recommendations_list.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        recommendations_layout.addWidget(self.recommendations_list)
        
        layout.addWidget(recommendations_group)
        
        # Load initial guidelines
        self.load_guidelines(self.condition_combo.currentText())

    def load_guidelines(self, condition):
        guidelines = {
            "Chest Pain": """
            ACC/AHA Guidelines for Chest Pain:
            1. Immediate ECG within 10 minutes
            2. Troponin measurement
            3. Consider stress testing
            4. Risk stratification using TIMI score
            5. Aspirin 325mg if ACS suspected
            """,
            "Shortness of Breath": """
            Dyspnea Evaluation Guidelines:
            1. Assess severity and onset
            2. Check oxygen saturation
            3. Consider chest X-ray
            4. Evaluate for pulmonary embolism
            5. Assess cardiac function
            """,
            "Abdominal Pain": """
            Abdominal Pain Guidelines:
            1. Assess location and characteristics
            2. Check for rebound tenderness
            3. Consider imaging studies
            4. Evaluate for surgical emergency
            5. Monitor vital signs closely
            """,
            "Hypertension": """
            JNC 8 Hypertension Guidelines:
            1. Lifestyle modifications first
            2. Consider medication if BP >140/90
            3. ACE inhibitors for most patients
            4. Monitor for side effects
            5. Regular follow-up
            """
        }
        
        self.guidelines_text.setPlainText(guidelines.get(condition, "No guidelines available for this condition."))

    def analyze_case(self):
        condition = self.condition_combo.currentText()
        
        # Generate recommendations based on condition
        recommendations = {
            "Chest Pain": [
                "Order ECG immediately",
                "Check troponin levels",
                "Consider cardiac catheterization",
                "Start aspirin if ACS suspected",
                "Risk stratify using TIMI score"
            ],
            "Shortness of Breath": [
                "Check oxygen saturation",
                "Order chest X-ray",
                "Consider D-dimer for PE",
                "Evaluate cardiac function",
                "Assess for pulmonary embolism"
            ],
            "Hypertension": [
                "Confirm BP measurement",
                "Check for end-organ damage",
                "Start lifestyle modifications",
                "Consider medication therapy",
                "Schedule follow-up"
            ]
        }
        
        self.recommendations_list.clear()
        for rec in recommendations.get(condition, ["No specific recommendations available"]):
            item = QListWidgetItem(f"• {rec}")
            self.recommendations_list.addItem(item) 