from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QTextEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QFrame, QGridLayout,
    QProgressBar, QSlider, QSpinBox, QComboBox, QCheckBox, QListWidget, QListWidgetItem,
    QTimer, QMessageBox, QDialog, QFormLayout, QLineEdit
)
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPixmap
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Signal
import math
import random
from datetime import datetime, timedelta

# Color palette
HIGHLIGHT_COLOR = "#4f8cff"
CRITICAL_COLOR = "#ff4f4f"
WARNING_COLOR = "#ffa726"
SUCCESS_COLOR = "#66bb6a"
EMERGENCY_RED = "#ff0000"
CODE_BLUE_COLOR = "#0000ff"

class CodeBlueWidget(QWidget):
    """Code Blue emergency simulation widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Emergency header
        header_layout = QHBoxLayout()
        self.emergency_label = QLabel("CODE BLUE")
        self.emergency_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #ff0000; background: #000; padding: 10px; border-radius: 8px;")
        header_layout.addWidget(self.emergency_label)
        
        self.start_code_btn = QPushButton("Start Code Blue")
        self.start_code_btn.setStyleSheet(f"background: {CRITICAL_COLOR}; color: white; border-radius: 4px; padding: 12px; font-size: 16px;")
        self.start_code_btn.clicked.connect(self.start_code_blue)
        header_layout.addWidget(self.start_code_btn)
        
        layout.addLayout(header_layout)
        
        # Code blue timer
        self.timer_label = QLabel("Time: 00:00")
        self.timer_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(self.timer_label)
        
        # CPR quality monitor
        cpr_group = QGroupBox("CPR Quality")
        cpr_layout = QVBoxLayout(cpr_group)
        
        self.compression_rate = QLabel("Compression Rate: 0/min")
        self.compression_depth = QLabel("Compression Depth: 0cm")
        self.ventilation_rate = QLabel("Ventilation Rate: 0/min")
        
        cpr_layout.addWidget(self.compression_rate)
        cpr_layout.addWidget(self.compression_depth)
        cpr_layout.addWidget(self.ventilation_rate)
        
        layout.addWidget(cpr_group)
        
        # Defibrillator
        defib_group = QGroupBox("Defibrillator")
        defib_layout = QVBoxLayout(defib_group)
        
        self.energy_level = QSpinBox()
        self.energy_level.setRange(200, 360)
        self.energy_level.setValue(200)
        self.energy_level.setSuffix(" J")
        
        self.charge_btn = QPushButton("Charge")
        self.charge_btn.setStyleSheet(f"background: {WARNING_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        self.charge_btn.clicked.connect(self.charge_defibrillator)
        
        self.shock_btn = QPushButton("SHOCK")
        self.shock_btn.setStyleSheet(f"background: {CRITICAL_COLOR}; color: white; border-radius: 4px; padding: 12px; font-size: 16px; font-weight: bold;")
        self.shock_btn.clicked.connect(self.deliver_shock)
        self.shock_btn.setEnabled(False)
        
        defib_layout.addWidget(QLabel("Energy Level:"))
        defib_layout.addWidget(self.energy_level)
        defib_layout.addWidget(self.charge_btn)
        defib_layout.addWidget(self.shock_btn)
        
        layout.addWidget(defib_group)
        
        # Medications
        med_group = QGroupBox("Emergency Medications")
        med_layout = QGridLayout(med_group)
        
        medications = [
            ("Epinephrine", "1mg IV", "Every 3-5 minutes"),
            ("Amiodarone", "300mg IV", "First dose"),
            ("Lidocaine", "1.5mg/kg IV", "Alternative to amiodarone"),
            ("Atropine", "1mg IV", "For bradycardia"),
            ("Sodium Bicarbonate", "1mEq/kg IV", "For metabolic acidosis")
        ]
        
        for i, (med, dose, frequency) in enumerate(medications):
            med_layout.addWidget(QLabel(f"{med}:"), i, 0)
            med_layout.addWidget(QLabel(dose), i, 1)
            med_layout.addWidget(QLabel(frequency), i, 2)
            
            admin_btn = QPushButton("Administer")
            admin_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 4px;")
            admin_btn.clicked.connect(lambda checked, m=med: self.administer_medication(m))
            med_layout.addWidget(admin_btn, i, 3)
        
        layout.addWidget(med_group)
        
        # Initialize timer
        self.code_timer = QTimer()
        self.code_timer.timeout.connect(self.update_timer)
        self.elapsed_time = 0
        self.code_active = False

    def start_code_blue(self):
        self.code_active = True
        self.elapsed_time = 0
        self.code_timer.start(1000)  # Update every second
        self.emergency_label.setText("CODE BLUE ACTIVE")
        self.emergency_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #ff0000; background: #000; padding: 10px; border-radius: 8px; animation: blink 1s infinite;")
        
        # Start CPR simulation
        self.cpr_timer = QTimer()
        self.cpr_timer.timeout.connect(self.update_cpr_quality)
        self.cpr_timer.start(2000)  # Update every 2 seconds

    def update_timer(self):
        self.elapsed_time += 1
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.timer_label.setText(f"Time: {minutes:02d}:{seconds:02d}")

    def update_cpr_quality(self):
        # Simulate realistic CPR quality
        compression_rate = random.randint(100, 120)
        compression_depth = random.randint(5, 6)
        ventilation_rate = random.randint(8, 12)
        
        self.compression_rate.setText(f"Compression Rate: {compression_rate}/min")
        self.compression_depth.setText(f"Compression Depth: {compression_depth}cm")
        self.ventilation_rate.setText(f"Ventilation Rate: {ventilation_rate}/min")

    def charge_defibrillator(self):
        self.shock_btn.setEnabled(True)
        self.charge_btn.setText("Charged")
        self.charge_btn.setStyleSheet(f"background: {SUCCESS_COLOR}; color: white; border-radius: 4px; padding: 8px;")

    def deliver_shock(self):
        energy = self.energy_level.value()
        QMessageBox.information(self, "Defibrillation", f"Delivered {energy}J shock")
        self.shock_btn.setEnabled(False)
        self.charge_btn.setText("Charge")
        self.charge_btn.setStyleSheet(f"background: {WARNING_COLOR}; color: white; border-radius: 4px; padding: 8px;")

    def administer_medication(self, medication):
        QMessageBox.information(self, "Medication", f"Administered {medication}")

class TraumaProtocolWidget(QWidget):
    """Trauma protocol simulation widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Trauma assessment
        assessment_group = QGroupBox("Primary Survey (ABCDE)")
        assessment_layout = QVBoxLayout(assessment_group)
        
        # ABCDE checklist
        self.airway_check = QCheckBox("A - Airway: Patent")
        self.breathing_check = QCheckBox("B - Breathing: Normal")
        self.circulation_check = QCheckBox("C - Circulation: Stable")
        self.disability_check = QCheckBox("D - Disability: Alert")
        self.exposure_check = QCheckBox("E - Exposure: Complete")
        
        assessment_layout.addWidget(self.airway_check)
        assessment_layout.addWidget(self.breathing_check)
        assessment_layout.addWidget(self.circulation_check)
        assessment_layout.addWidget(self.disability_check)
        assessment_layout.addWidget(self.exposure_check)
        
        layout.addWidget(assessment_group)
        
        # Trauma interventions
        interventions_group = QGroupBox("Trauma Interventions")
        interventions_layout = QGridLayout(interventions_group)
        
        interventions = [
            ("Chest Tube", "Insert chest tube for pneumothorax"),
            ("IV Access", "Establish large bore IV access"),
            ("Blood Transfusion", "Type and cross for blood products"),
            ("Surgery Consult", "Call trauma surgery"),
            ("Imaging", "Order trauma series (CXR, Pelvis)"),
            ("Antibiotics", "Administer prophylactic antibiotics")
        ]
        
        for i, (intervention, description) in enumerate(interventions):
            interventions_layout.addWidget(QLabel(intervention), i, 0)
            interventions_layout.addWidget(QLabel(description), i, 1)
            
            perform_btn = QPushButton("Perform")
            perform_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 4px;")
            perform_btn.clicked.connect(lambda checked, intv=intervention: self.perform_intervention(intv))
            interventions_layout.addWidget(perform_btn, i, 2)
        
        layout.addWidget(interventions_group)
        
        # Trauma score
        score_group = QGroupBox("Trauma Score")
        score_layout = QHBoxLayout(score_group)
        
        self.gcs_score = QSpinBox()
        self.gcs_score.setRange(3, 15)
        self.gcs_score.setValue(15)
        self.gcs_score.setSuffix(" (GCS)")
        
        self.sbp_score = QSpinBox()
        self.sbp_score.setRange(0, 200)
        self.sbp_score.setValue(120)
        self.sbp_score.setSuffix(" mmHg")
        
        self.rr_score = QSpinBox()
        self.rr_score.setRange(0, 50)
        self.rr_score.setValue(16)
        self.rr_score.setSuffix(" /min")
        
        score_layout.addWidget(QLabel("Glasgow Coma Scale:"))
        score_layout.addWidget(self.gcs_score)
        score_layout.addWidget(QLabel("Systolic BP:"))
        score_layout.addWidget(self.sbp_score)
        score_layout.addWidget(QLabel("Respiratory Rate:"))
        score_layout.addWidget(self.rr_score)
        
        self.calculate_btn = QPushButton("Calculate Score")
        self.calculate_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        self.calculate_btn.clicked.connect(self.calculate_trauma_score)
        score_layout.addWidget(self.calculate_btn)
        
        layout.addWidget(score_group)

    def perform_intervention(self, intervention):
        QMessageBox.information(self, "Intervention", f"Performed {intervention}")

    def calculate_trauma_score(self):
        gcs = self.gcs_score.value()
        sbp = self.sbp_score.value()
        rr = self.rr_score.value()
        
        # Simplified trauma score calculation
        gcs_score = max(0, gcs - 3) // 2
        sbp_score = 4 if sbp > 89 else 3 if sbp > 75 else 2 if sbp > 50 else 1 if sbp > 0 else 0
        rr_score = 4 if rr > 9 and rr < 30 else 3 if rr > 5 and rr < 36 else 2 if rr > 0 and rr < 45 else 1 if rr > 0 else 0
        
        total_score = gcs_score + sbp_score + rr_score
        
        severity = "Minor" if total_score > 12 else "Moderate" if total_score > 8 else "Severe"
        
        QMessageBox.information(self, "Trauma Score", f"Trauma Score: {total_score}/12 ({severity})")

class CriticalCareWidget(QWidget):
    """Critical care monitoring and interventions widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Hemodynamic monitoring
        hemodynamic_group = QGroupBox("Hemodynamic Monitoring")
        hemodynamic_layout = QGridLayout(hemodynamic_group)
        
        # Central venous pressure
        self.cvp_label = QLabel("CVP: 8 mmHg")
        self.cvp_slider = QSlider(Qt.Horizontal)
        self.cvp_slider.setRange(0, 20)
        self.cvp_slider.setValue(8)
        self.cvp_slider.valueChanged.connect(self.update_cvp)
        
        # Pulmonary artery pressure
        self.pap_label = QLabel("PAP: 25/10 mmHg")
        self.pap_slider = QSlider(Qt.Horizontal)
        self.pap_slider.setRange(10, 50)
        self.pap_slider.setValue(25)
        self.pap_slider.valueChanged.connect(self.update_pap)
        
        # Cardiac output
        self.co_label = QLabel("Cardiac Output: 5.0 L/min")
        self.co_slider = QSlider(Qt.Horizontal)
        self.co_slider.setRange(1, 10)
        self.co_slider.setValue(5)
        self.co_slider.valueChanged.connect(self.update_co)
        
        hemodynamic_layout.addWidget(QLabel("Central Venous Pressure:"), 0, 0)
        hemodynamic_layout.addWidget(self.cvp_label, 0, 1)
        hemodynamic_layout.addWidget(self.cvp_slider, 0, 2)
        
        hemodynamic_layout.addWidget(QLabel("Pulmonary Artery Pressure:"), 1, 0)
        hemodynamic_layout.addWidget(self.pap_label, 1, 1)
        hemodynamic_layout.addWidget(self.pap_slider, 1, 2)
        
        hemodynamic_layout.addWidget(QLabel("Cardiac Output:"), 2, 0)
        hemodynamic_layout.addWidget(self.co_label, 2, 1)
        hemodynamic_layout.addWidget(self.co_slider, 2, 2)
        
        layout.addWidget(hemodynamic_group)
        
        # Vasopressor management
        vasopressor_group = QGroupBox("Vasopressor Management")
        vasopressor_layout = QGridLayout(vasopressor_group)
        
        vasopressors = [
            ("Norepinephrine", "0.1-2.0", "mcg/kg/min"),
            ("Dopamine", "2-20", "mcg/kg/min"),
            ("Dobutamine", "2-20", "mcg/kg/min"),
            ("Vasopressin", "0.01-0.04", "units/min"),
            ("Epinephrine", "0.01-0.5", "mcg/kg/min")
        ]
        
        for i, (drug, dose_range, unit) in enumerate(vasopressors):
            vasopressor_layout.addWidget(QLabel(drug), i, 0)
            vasopressor_layout.addWidget(QLabel(f"{dose_range} {unit}"), i, 1)
            
            start_btn = QPushButton("Start")
            start_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 4px;")
            start_btn.clicked.connect(lambda checked, d=drug: self.start_vasopressor(d))
            vasopressor_layout.addWidget(start_btn, i, 2)
            
            stop_btn = QPushButton("Stop")
            stop_btn.setStyleSheet(f"background: {CRITICAL_COLOR}; color: white; border-radius: 4px; padding: 4px;")
            stop_btn.clicked.connect(lambda checked, d=drug: self.stop_vasopressor(d))
            vasopressor_layout.addWidget(stop_btn, i, 3)
        
        layout.addWidget(vasopressor_group)
        
        # Sedation and analgesia
        sedation_group = QGroupBox("Sedation & Analgesia")
        sedation_layout = QGridLayout(sedation_group)
        
        sedatives = [
            ("Propofol", "Sedation", "10-100 mcg/kg/min"),
            ("Midazolam", "Sedation", "0.02-0.1 mg/kg/hr"),
            ("Fentanyl", "Analgesia", "0.5-2 mcg/kg/hr"),
            ("Morphine", "Analgesia", "0.01-0.05 mg/kg/hr"),
            ("Dexmedetomidine", "Sedation", "0.2-1.4 mcg/kg/hr")
        ]
        
        for i, (drug, indication, dose_range) in enumerate(sedatives):
            sedation_layout.addWidget(QLabel(drug), i, 0)
            sedation_layout.addWidget(QLabel(indication), i, 1)
            sedation_layout.addWidget(QLabel(dose_range), i, 2)
            
            admin_btn = QPushButton("Administer")
            admin_btn.setStyleSheet(f"background: {WARNING_COLOR}; color: white; border-radius: 4px; padding: 4px;")
            admin_btn.clicked.connect(lambda checked, d=drug: self.administer_sedative(d))
            sedation_layout.addWidget(admin_btn, i, 3)
        
        layout.addWidget(sedation_group)

    def update_cvp(self, value):
        self.cvp_label.setText(f"CVP: {value} mmHg")

    def update_pap(self, value):
        diastolic = value // 2
        self.pap_label.setText(f"PAP: {value}/{diastolic} mmHg")

    def update_co(self, value):
        self.co_label.setText(f"Cardiac Output: {value}.0 L/min")

    def start_vasopressor(self, drug):
        QMessageBox.information(self, "Vasopressor", f"Started {drug} infusion")

    def stop_vasopressor(self, drug):
        QMessageBox.information(self, "Vasopressor", f"Stopped {drug} infusion")

    def administer_sedative(self, drug):
        QMessageBox.information(self, "Sedation", f"Administered {drug}")

class EmergencyScenarioWidget(QWidget):
    """Emergency scenario simulation widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Scenario selection
        scenario_group = QGroupBox("Emergency Scenarios")
        scenario_layout = QVBoxLayout(scenario_group)
        
        self.scenario_combo = QComboBox()
        self.scenario_combo.addItems([
            "Cardiac Arrest",
            "Trauma - Motor Vehicle Accident",
            "Trauma - Gunshot Wound",
            "Respiratory Failure",
            "Septic Shock",
            "Anaphylaxis",
            "Stroke",
            "Myocardial Infarction"
        ])
        self.scenario_combo.currentTextChanged.connect(self.load_scenario)
        
        self.start_scenario_btn = QPushButton("Start Scenario")
        self.start_scenario_btn.setStyleSheet(f"background: {CRITICAL_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        self.start_scenario_btn.clicked.connect(self.start_scenario)
        
        scenario_layout.addWidget(self.scenario_combo)
        scenario_layout.addWidget(self.start_scenario_btn)
        
        layout.addWidget(scenario_group)
        
        # Scenario details
        self.scenario_text = QTextEdit()
        self.scenario_text.setMaximumHeight(150)
        self.scenario_text.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        layout.addWidget(self.scenario_text)
        
        # Scenario objectives
        self.objectives_list = QListWidget()
        layout.addWidget(self.objectives_list)
        
        # Load initial scenario
        self.load_scenario(self.scenario_combo.currentText())

    def load_scenario(self, scenario_name):
        scenarios = {
            "Cardiac Arrest": {
                "description": "65-year-old male found unresponsive in room. No pulse, no breathing. CPR in progress.",
                "objectives": [
                    "Initiate ACLS protocol",
                    "Establish airway",
                    "Administer epinephrine",
                    "Defibrillate if indicated",
                    "Obtain return of spontaneous circulation"
                ]
            },
            "Trauma - Motor Vehicle Accident": {
                "description": "25-year-old female involved in high-speed MVA. Multiple injuries, altered mental status.",
                "objectives": [
                    "Perform primary survey (ABCDE)",
                    "Establish airway",
                    "Control bleeding",
                    "Stabilize spine",
                    "Order trauma imaging"
                ]
            },
            "Respiratory Failure": {
                "description": "45-year-old male with COPD exacerbation. Severe respiratory distress, SpO2 85%.",
                "objectives": [
                    "Assess airway",
                    "Administer bronchodilators",
                    "Consider intubation",
                    "Start mechanical ventilation",
                    "Monitor oxygenation"
                ]
            },
            "Septic Shock": {
                "description": "70-year-old female with fever, hypotension, and altered mental status. Suspected sepsis.",
                "objectives": [
                    "Obtain blood cultures",
                    "Administer broad-spectrum antibiotics",
                    "Start vasopressors",
                    "Fluid resuscitation",
                    "Source control"
                ]
            }
        }
        
        if scenario_name in scenarios:
            scenario = scenarios[scenario_name]
            self.scenario_text.setPlainText(scenario["description"])
            
            self.objectives_list.clear()
            for objective in scenario["objectives"]:
                item = QListWidgetItem(f"☐ {objective}")
                self.objectives_list.addItem(item)

    def start_scenario(self):
        scenario = self.scenario_combo.currentText()
        QMessageBox.information(self, "Scenario Started", f"Emergency scenario '{scenario}' has begun. Respond appropriately!") 