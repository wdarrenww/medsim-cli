from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QLabel, QStackedWidget, QFrame,
    QDialog, QLineEdit, QFormLayout, QSpinBox, QComboBox, QTextEdit, QScrollArea, QGridLayout, QGroupBox, QListWidgetItem,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QInputDialog
)
from PySide6.QtGui import QIcon, QFont, QColor
from PySide6.QtCore import Qt, QSize, Signal, QTimer
import sys
from datetime import datetime

# Import session manager and engines
from ..core.session import session_manager
from ..core.physiology import EnhancedPhysiologicalEngine
from ..core.diagnostics import EnhancedDiagnosticSystem
from ..core.treatments import EnhancedTreatmentEngine
from ..core.dialogue import EnhancedDialogueEngine

# Import dialogs
from .dialogs import OrderLabDialog, OrderImagingDialog, AdministerDrugDialog, TalkToPatientDialog

# Import enhanced widgets
from .enhanced_widgets import (
    ECGWaveformWidget, PulseOximeterWidget, DrugInteractionWidget, 
    PatientTimelineWidget, ProcedureWidget, VentilatorWidget
)

# Import emergency widgets
from .emergency_widgets import (
    CodeBlueWidget, TraumaProtocolWidget, CriticalCareWidget, EmergencyScenarioWidget
)

# Import imaging widgets
from .imaging_widgets import (
    XRayViewerWidget, CTScanViewerWidget, UltrasoundWidget
)

# Import documentation widgets
from .documentation_widgets import (
    ProgressNoteWidget, DischargeSummaryWidget, MedicationReconciliationWidget, ClinicalDecisionSupportWidget
)

# minimalist color palette
BG_COLOR = "#f7f9fa"
SIDEBAR_COLOR = "#222e3a"
SIDEBAR_TEXT = "#eaf0f6"
HIGHLIGHT_COLOR = "#4f8cff"
CRITICAL_COLOR = "#ff4f4f"
WARNING_COLOR = "#ffa726"
SUCCESS_COLOR = "#66bb6a"

class AddPatientDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Patient")
        self.setFixedSize(400, 300)
        self.setStyleSheet(f"background: {BG_COLOR};")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        self.patient_id = QLineEdit()
        self.patient_id.setPlaceholderText("e.g., P001")
        self.patient_id.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ddd;")
        
        self.name = QLineEdit()
        self.name.setPlaceholderText("Full name")
        self.name.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ddd;")
        
        self.age = QSpinBox()
        self.age.setRange(0, 120)
        self.age.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ddd;")
        
        self.gender = QComboBox()
        self.gender.addItems(["Male", "Female", "Other"])
        self.gender.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ddd;")
        
        self.height = QSpinBox()
        self.height.setRange(50, 250)
        self.height.setSuffix(" cm")
        self.height.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ddd;")
        
        self.weight = QSpinBox()
        self.weight.setRange(1, 300)
        self.weight.setSuffix(" kg")
        self.weight.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ddd;")
        
        form_layout.addRow("Patient ID:", self.patient_id)
        form_layout.addRow("Name:", self.name)
        form_layout.addRow("Age:", self.age)
        form_layout.addRow("Gender:", self.gender)
        form_layout.addRow("Height:", self.height)
        form_layout.addRow("Weight:", self.weight)
        
        layout.addLayout(form_layout)
        
        # buttons
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(f"background: #ddd; color: #333; border-radius: 4px; padding: 8px 16px;")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.add_btn = QPushButton("Add Patient")
        self.add_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px 16px;")
        self.add_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.add_btn)
        layout.addLayout(btn_layout)

class PatientSidebar(QFrame):
    patient_selected = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self.setStyleSheet(f"background: {SIDEBAR_COLOR}; border: none;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.title = QLabel("Patients")
        self.title.setStyleSheet(f"color: {SIDEBAR_TEXT}; font-size: 22px; font-weight: bold;")
        layout.addWidget(self.title)

        self.patient_list = QListWidget()
        self.patient_list.setStyleSheet(f"background: {SIDEBAR_COLOR}; color: {SIDEBAR_TEXT}; border-radius: 8px; font-size: 16px;")
        self.patient_list.itemClicked.connect(self.on_patient_selected)
        layout.addWidget(self.patient_list, 1)

        self.add_btn = QPushButton("+ Add Patient")
        self.add_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 6px; padding: 8px 0; font-size: 15px;")
        self.add_btn.clicked.connect(self.show_add_dialog)
        layout.addWidget(self.add_btn)

        layout.addStretch(1)
        
        # session info
        self.session_info = QLabel("Session: 0 patients")
        self.session_info.setStyleSheet(f"color: {SIDEBAR_TEXT}; font-size: 12px; opacity: 0.7;")
        layout.addWidget(self.session_info)
        
        # Update session info
        self.update_session_info()

    def on_patient_selected(self, item):
        patient_id = item.data(Qt.UserRole)
        self.patient_selected.emit(patient_id)

    def show_add_dialog(self):
        dialog = AddPatientDialog(self)
        if dialog.exec() == QDialog.Accepted:
            patient_id = dialog.patient_id.text()
            name = dialog.name.text()
            age = dialog.age.value()
            gender = dialog.gender.currentText()
            height = dialog.height.value()
            weight = dialog.weight.value()
            
            # Create patient in session manager
            result = session_manager.create_patient_session(patient_id, name)
            
            # Create patient in physiological engine
            physio_engine = EnhancedPhysiologicalEngine()
            physio_engine.create_patient(patient_id, name, age, gender.lower(), height, weight)
            
            # Add to list
            item = QListWidgetItem(f"{name} ({patient_id})")
            item.setData(Qt.UserRole, patient_id)
            self.patient_list.addItem(item)
            
            # Update session info
            self.update_session_info()
            
            # Emit signal
            self.patient_selected.emit(patient_id)
            
            QMessageBox.information(self, "Success", f"Patient {name} added successfully!")

    def update_session_info(self):
        stats = session_manager.get_session_statistics()
        self.session_info.setText(f"Session: {stats['total_patients']} patients")

class VitalsWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Vital Signs", parent)
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QGridLayout(self)
        layout.setSpacing(12)
        
        # Create vital sign labels
        self.vitals = [
            ("Heart Rate", "80", "bpm", "normal"),
            ("Blood Pressure", "120/80", "mmHg", "normal"),
            ("Respiratory Rate", "16", "/min", "normal"),
            ("Temperature", "37.0", "°C", "normal"),
            ("Oxygen Saturation", "98", "%", "normal"),
            ("Blood Glucose", "100", "mg/dL", "normal")
        ]
        
        self.vital_labels = {}
        
        for i, (name, value, unit, status) in enumerate(self.vitals):
            row = i // 2
            col = i % 2 * 2
            
            # Vital name
            name_label = QLabel(name)
            name_label.setStyleSheet("font-weight: normal; color: #666;")
            layout.addWidget(name_label, row, col)
            
            # Value with status color
            status_color = SUCCESS_COLOR if status == "normal" else WARNING_COLOR if status == "warning" else CRITICAL_COLOR
            value_label = QLabel(f"{value} {unit}")
            value_label.setStyleSheet(f"font-weight: bold; color: {status_color}; font-size: 16px;")
            layout.addWidget(value_label, row, col + 1)
            
            self.vital_labels[name] = value_label

    def update_vitals(self, vitals_data):
        """Update vitals with real data"""
        for name, value, unit in vitals_data:
            if name in self.vital_labels:
                self.vital_labels[name].setText(f"{value} {unit}")

class AlertsWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Critical Alerts", parent)
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        self.alerts_list = QListWidget()
        self.alerts_list.setStyleSheet("border: none; background: transparent;")
        layout.addWidget(self.alerts_list)

    def update_alerts(self, alerts):
        """Update alerts with real data"""
        self.alerts_list.clear()
        for alert in alerts:
            item = QListWidgetItem(f"⚠️ {alert}")
            item.setForeground(QColor(CRITICAL_COLOR))
            self.alerts_list.addItem(item)

class LabsWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Laboratory Tests", parent)
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Add order button
        self.order_btn = QPushButton("Order Lab Test")
        self.order_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        layout.addWidget(self.order_btn)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Test", "Value", "Unit", "Status"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.results_table)

class ImagingWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Imaging Studies", parent)
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Add imaging modality tabs
        imaging_tabs = QTabWidget()
        imaging_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QTabBar::tab {
                background: #f0f0f0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
            }
        """)
        
        # X-ray tab
        xray_tab = QWidget()
        xray_layout = QVBoxLayout(xray_tab)
        self.xray_widget = XRayViewerWidget()
        xray_layout.addWidget(self.xray_widget)
        imaging_tabs.addTab(xray_tab, "X-Ray")
        
        # CT tab
        ct_tab = QWidget()
        ct_layout = QVBoxLayout(ct_tab)
        self.ct_widget = CTScanViewerWidget()
        ct_layout.addWidget(self.ct_widget)
        imaging_tabs.addTab(ct_tab, "CT Scan")
        
        # Ultrasound tab
        us_tab = QWidget()
        us_layout = QVBoxLayout(us_tab)
        self.us_widget = UltrasoundWidget()
        us_layout.addWidget(self.us_widget)
        imaging_tabs.addTab(us_tab, "Ultrasound")
        
        layout.addWidget(imaging_tabs)
        
        # Add order button
        self.imaging_order_btn = QPushButton("Order Imaging")
        self.imaging_order_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        self.imaging_order_btn.clicked.connect(self.order_imaging)
        layout.addWidget(self.imaging_order_btn)

class TreatmentsWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Treatments", parent)
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Add treatment button
        self.add_btn = QPushButton("Administer Drug")
        self.add_btn.setStyleSheet(f"background: {WARNING_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        layout.addWidget(self.add_btn)
        
        # Active treatments table
        self.treatments_table = QTableWidget()
        self.treatments_table.setColumnCount(4)
        self.treatments_table.setHorizontalHeaderLabels(["Drug", "Dose", "Route", "Time"])
        self.treatments_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.treatments_table)

class CommunicationWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Patient Communication", parent)
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Talk button
        self.talk_btn = QPushButton("Talk to Patient")
        self.talk_btn.setStyleSheet(f"background: {SUCCESS_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        layout.addWidget(self.talk_btn)
        
        # Conversation area
        self.conversation_area = QTextEdit()
        self.conversation_area.setMaximumHeight(200)
        self.conversation_area.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        self.conversation_area.setPlainText("No conversation yet...")
        layout.addWidget(self.conversation_area)

class PatientDashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_patient_id = None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Header
        header_layout = QHBoxLayout()
        self.patient_title = QLabel("Select a patient to view details")
        self.patient_title.setStyleSheet("font-size: 24px; color: #333; font-weight: 500;")
        header_layout.addWidget(self.patient_title)
        
        # Action buttons
        self.update_btn = QPushButton("Update Vitals")
        self.update_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px 16px;")
        self.update_btn.clicked.connect(self.update_vitals)
        header_layout.addWidget(self.update_btn)
        
        self.talk_btn = QPushButton("Talk to Patient")
        self.talk_btn.setStyleSheet(f"background: {SUCCESS_COLOR}; color: white; border-radius: 4px; padding: 8px 16px;")
        self.talk_btn.clicked.connect(self.talk_to_patient)
        header_layout.addWidget(self.talk_btn)
        
        layout.addLayout(header_layout)
        
        # Tab widget for different sections
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QTabBar::tab {
                background: #f0f0f0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
            }
        """)
        
        # Overview tab
        overview_tab = QWidget()
        overview_layout = QHBoxLayout(overview_tab)
        
        # Left column - Vitals and Alerts
        left_column = QVBoxLayout()
        self.vitals_widget = VitalsWidget()
        left_column.addWidget(self.vitals_widget)
        
        self.alerts_widget = AlertsWidget()
        left_column.addWidget(self.alerts_widget)
        
        overview_layout.addLayout(left_column)
        
        # Right column - Patient info and actions
        right_column = QVBoxLayout()
        
        # Patient info group
        info_group = QGroupBox("Patient Information")
        info_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        info_layout = QVBoxLayout(info_group)
        self.info_text = QTextEdit()
        self.info_text.setMaximumHeight(150)
        self.info_text.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        self.info_text.setPlainText("No patient selected")
        info_layout.addWidget(self.info_text)
        
        right_column.addWidget(info_group)
        
        # Quick actions
        actions_group = QGroupBox("Quick Actions")
        actions_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        actions_layout = QVBoxLayout(actions_group)
        
        # Create action buttons with connections
        self.order_lab_btn = QPushButton("Order Lab Test")
        self.order_lab_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px; margin: 2px;")
        self.order_lab_btn.clicked.connect(self.order_lab_test)
        actions_layout.addWidget(self.order_lab_btn)
        
        self.order_imaging_btn = QPushButton("Order Imaging")
        self.order_imaging_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px; margin: 2px;")
        self.order_imaging_btn.clicked.connect(self.order_imaging)
        actions_layout.addWidget(self.order_imaging_btn)
        
        self.administer_drug_btn = QPushButton("Administer Drug")
        self.administer_drug_btn.setStyleSheet(f"background: {WARNING_COLOR}; color: white; border-radius: 4px; padding: 8px; margin: 2px;")
        self.administer_drug_btn.clicked.connect(self.administer_drug)
        actions_layout.addWidget(self.administer_drug_btn)
        
        self.add_symptom_btn = QPushButton("Add Symptom")
        self.add_symptom_btn.setStyleSheet(f"background: {CRITICAL_COLOR}; color: white; border-radius: 4px; padding: 8px; margin: 2px;")
        self.add_symptom_btn.clicked.connect(self.add_symptom)
        actions_layout.addWidget(self.add_symptom_btn)
        
        right_column.addWidget(actions_group)
        right_column.addStretch(1)
        
        overview_layout.addLayout(right_column)
        
        # Add tabs
        self.tab_widget.addTab(overview_tab, "Overview")
        
        # Labs tab
        labs_tab = QWidget()
        labs_layout = QVBoxLayout(labs_tab)
        self.labs_widget = LabsWidget()
        self.labs_widget.order_btn.clicked.connect(self.order_lab_test)
        labs_layout.addWidget(self.labs_widget)
        self.tab_widget.addTab(labs_tab, "Laboratory")
        
        # Imaging tab
        imaging_tab = QWidget()
        imaging_layout = QVBoxLayout(imaging_tab)
        self.imaging_widget = ImagingWidget()
        self.imaging_widget.imaging_order_btn.clicked.connect(self.order_imaging)
        imaging_layout.addWidget(self.imaging_widget)
        self.tab_widget.addTab(imaging_tab, "Imaging")
        
        # Treatments tab
        treatments_tab = QWidget()
        treatments_layout = QVBoxLayout(treatments_tab)
        self.treatments_widget = TreatmentsWidget()
        self.treatments_widget.add_btn.clicked.connect(self.administer_drug)
        treatments_layout.addWidget(self.treatments_widget)
        self.tab_widget.addTab(treatments_tab, "Treatments")
        
        # Communication tab
        communication_tab = QWidget()
        communication_layout = QVBoxLayout(communication_tab)
        self.communication_widget = CommunicationWidget()
        self.communication_widget.talk_btn.clicked.connect(self.talk_to_patient)
        communication_layout.addWidget(self.communication_widget)
        self.tab_widget.addTab(communication_tab, "Communication")
        
        # Enhanced Monitoring tab
        monitoring_tab = QWidget()
        monitoring_layout = QVBoxLayout(monitoring_tab)
        
        # ECG and Pulse Oximeter
        monitoring_top = QHBoxLayout()
        self.ecg_widget = ECGWaveformWidget()
        monitoring_top.addWidget(self.ecg_widget)
        
        self.pulse_widget = PulseOximeterWidget()
        monitoring_top.addWidget(self.pulse_widget)
        
        monitoring_layout.addLayout(monitoring_top)
        
        # Drug interactions
        self.drug_interaction_widget = DrugInteractionWidget()
        monitoring_layout.addWidget(self.drug_interaction_widget)
        
        self.tab_widget.addTab(monitoring_tab, "Enhanced Monitoring")
        
        # Patient History tab
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)
        self.timeline_widget = PatientTimelineWidget()
        history_layout.addWidget(self.timeline_widget)
        self.tab_widget.addTab(history_tab, "Patient History")
        
        # Procedures tab
        procedures_tab = QWidget()
        procedures_layout = QVBoxLayout(procedures_tab)
        self.procedure_widget = ProcedureWidget()
        procedures_layout.addWidget(self.procedure_widget)
        self.tab_widget.addTab(procedures_tab, "Procedures")
        
        # Ventilator tab
        ventilator_tab = QWidget()
        ventilator_layout = QVBoxLayout(ventilator_tab)
        self.ventilator_widget = VentilatorWidget()
        ventilator_layout.addWidget(self.ventilator_widget)
        self.tab_widget.addTab(ventilator_tab, "Ventilator")
        
        # Emergency Medicine tabs
        # Code Blue tab
        code_blue_tab = QWidget()
        code_blue_layout = QVBoxLayout(code_blue_tab)
        self.code_blue_widget = CodeBlueWidget()
        code_blue_layout.addWidget(self.code_blue_widget)
        self.tab_widget.addTab(code_blue_tab, "Code Blue")
        
        # Trauma Protocol tab
        trauma_tab = QWidget()
        trauma_layout = QVBoxLayout(trauma_tab)
        self.trauma_widget = TraumaProtocolWidget()
        trauma_layout.addWidget(self.trauma_widget)
        self.tab_widget.addTab(trauma_tab, "Trauma Protocol")
        
        # Critical Care tab
        critical_care_tab = QWidget()
        critical_care_layout = QVBoxLayout(critical_care_tab)
        self.critical_care_widget = CriticalCareWidget()
        critical_care_layout.addWidget(self.critical_care_widget)
        self.tab_widget.addTab(critical_care_tab, "Critical Care")
        
        # Emergency Scenarios tab
        scenarios_tab = QWidget()
        scenarios_layout = QVBoxLayout(scenarios_tab)
        self.scenarios_widget = EmergencyScenarioWidget()
        scenarios_layout.addWidget(self.scenarios_widget)
        self.tab_widget.addTab(scenarios_tab, "Emergency Scenarios")
        
        # Documentation tab
        documentation_tab = QWidget()
        documentation_layout = QVBoxLayout(documentation_tab)
        
        # Documentation tabs
        doc_tabs = QTabWidget()
        doc_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QTabBar::tab {
                background: #f0f0f0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
            }
        """)
        
        # Progress Notes tab
        progress_notes_tab = QWidget()
        progress_notes_layout = QVBoxLayout(progress_notes_tab)
        self.progress_notes_widget = ProgressNoteWidget()
        progress_notes_layout.addWidget(self.progress_notes_widget)
        doc_tabs.addTab(progress_notes_tab, "Progress Notes")
        
        # Discharge Summary tab
        discharge_tab = QWidget()
        discharge_layout = QVBoxLayout(discharge_tab)
        self.discharge_widget = DischargeSummaryWidget()
        discharge_layout.addWidget(self.discharge_widget)
        doc_tabs.addTab(discharge_tab, "Discharge Summary")
        
        # Medication Reconciliation tab
        med_recon_tab = QWidget()
        med_recon_layout = QVBoxLayout(med_recon_tab)
        self.med_recon_widget = MedicationReconciliationWidget()
        med_recon_layout.addWidget(self.med_recon_widget)
        doc_tabs.addTab(med_recon_tab, "Medication Reconciliation")
        
        # Clinical Decision Support tab
        cds_tab = QWidget()
        cds_layout = QVBoxLayout(cds_tab)
        self.cds_widget = ClinicalDecisionSupportWidget()
        cds_layout.addWidget(self.cds_widget)
        doc_tabs.addTab(cds_tab, "Clinical Decision Support")
        
        documentation_layout.addWidget(doc_tabs)
        self.tab_widget.addTab(documentation_tab, "Documentation")
        
        layout.addWidget(self.tab_widget)

    def set_current_patient(self, patient_id):
        """Set the current patient for all actions"""
        self.current_patient_id = patient_id

    def update_vitals(self):
        """Manually update vitals for current patient"""
        if self.current_patient_id:
            # Trigger physiological update
            self.parent().physio_engine.update_patient(self.current_patient_id)
            # Refresh display
            self.parent().on_patient_selected(self.current_patient_id)

    def order_lab_test(self):
        """Open lab test ordering dialog"""
        if self.current_patient_id:
            dialog = OrderLabDialog(self.current_patient_id, self)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Warning", "Please select a patient first")

    def order_imaging(self):
        """Open imaging ordering dialog"""
        if self.current_patient_id:
            dialog = OrderImagingDialog(self.current_patient_id, self)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Warning", "Please select a patient first")

    def administer_drug(self):
        """Open drug administration dialog"""
        if self.current_patient_id:
            dialog = AdministerDrugDialog(self.current_patient_id, self)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Warning", "Please select a patient first")

    def add_symptom(self):
        """Add symptom to patient"""
        if self.current_patient_id:
            symptom, ok = QInputDialog.getText(self, "Add Symptom", "Enter symptom:")
            if ok and symptom:
                # Add symptom to patient
                self.parent().physio_engine.add_symptom(self.current_patient_id, symptom)
                QMessageBox.information(self, "Success", f"Added symptom: {symptom}")
        else:
            QMessageBox.warning(self, "Warning", "Please select a patient first")

    def talk_to_patient(self):
        """Open patient communication dialog"""
        if self.current_patient_id:
            dialog = TalkToPatientDialog(self.current_patient_id, self)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Warning", "Please select a patient first")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medsim - Medical Simulation")
        self.setMinimumSize(1200, 800)  # Increased size for enhanced features
        self.setStyleSheet(f"background: {BG_COLOR};")
        self.setWindowIcon(QIcon())
        
        # Initialize engines
        self.physio_engine = EnhancedPhysiologicalEngine()
        self.diagnostic_engine = EnhancedDiagnosticSystem()
        self.treatment_engine = EnhancedTreatmentEngine()
        self.dialogue_engine = EnhancedDialogueEngine()

        # main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # sidebar
        self.sidebar = PatientSidebar()
        self.sidebar.patient_selected.connect(self.on_patient_selected)
        main_layout.addWidget(self.sidebar)

        # main dashboard area
        self.dashboard = QStackedWidget()
        self.patient_dashboard = PatientDashboard()
        self.dashboard.addWidget(self.patient_dashboard)
        main_layout.addWidget(self.dashboard, 1)

        self.setCentralWidget(main_widget)
        
        # Add some sample patients
        self.add_sample_patients()
        
        # Setup timer for updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_patient_data)
        self.update_timer.start(5000)  # Update every 5 seconds

    def on_patient_selected(self, patient_id):
        self.patient_dashboard.set_current_patient(patient_id)
        self.patient_dashboard.patient_title.setText(f"Patient: {patient_id}")
        
        # Get patient data
        patient = self.physio_engine.get_patient(patient_id)
        if patient:
            vitals = patient.get_available_vitals()
            critical_vitals = patient.get_critical_vitals()
            
            # Update vitals display
            vitals_data = []
            for name, data in vitals.items():
                vitals_data.append((name.replace('_', ' ').title(), str(data['value']), data['unit']))
            
            self.patient_dashboard.vitals_widget.update_vitals(vitals_data)
            
            # Update alerts
            alerts = [f"{vital['name']}: {vital['value']} {vital['unit']}" for vital in critical_vitals]
            self.patient_dashboard.alerts_widget.update_alerts(alerts)
            
            # Update ECG rhythm based on heart rate
            heart_rate = vitals.get('heart_rate', {}).get('value', 80)
            self.patient_dashboard.ecg_widget.set_heart_rate(heart_rate)
            
            # Set ECG rhythm based on patient condition
            if heart_rate > 100:
                self.patient_dashboard.ecg_widget.set_rhythm("tachycardia")
            elif heart_rate < 60:
                self.patient_dashboard.ecg_widget.set_rhythm("bradycardia")
            else:
                self.patient_dashboard.ecg_widget.set_rhythm("normal")
            
            # Update patient info
            summary = patient.get_summary()
            info_text = f"""Patient ID: {summary['patient_id']}
Name: {summary['name']}
Age: {summary['age']} | Gender: {summary['gender']}
Height: {summary['height_cm']}cm | Weight: {summary['weight_kg']}kg
Symptoms: {len(summary['symptoms'])}
Active Diseases: {len(summary['active_diseases'])}
Treatments: {summary['treatments']}
Stress Level: {summary['stress_level']:.2f}
Pain Level: {summary['pain_level']:.1f}
Last Updated: {datetime.now().strftime('%H:%M:%S')}"""
            
            self.patient_dashboard.info_text.setPlainText(info_text)

    def update_patient_data(self):
        """Update patient data periodically"""
        current_patient = session_manager.get_current_patient()
        if current_patient:
            # Update physiological data
            self.physio_engine.update_all_patients()
            self.treatment_engine.update_drug_levels(current_patient)
            
            # Refresh display if this patient is selected
            if self.patient_dashboard.current_patient_id == current_patient:
                self.on_patient_selected(current_patient)

    def add_sample_patients(self):
        sample_patients = [
            ("P001", "Sarah Johnson", 58, "female", 165, 75),
            ("P002", "Michael Chen", 45, "male", 175, 80),
            ("P003", "Emily Rodriguez", 32, "female", 160, 65)
        ]
        
        for patient_id, name, age, gender, height, weight in sample_patients:
            # Create in session manager
            session_manager.create_patient_session(patient_id, name)
            
            # Create in physiological engine
            self.physio_engine.create_patient(patient_id, name, age, gender, height, weight)
            
            # Add to list
            item = QListWidgetItem(f"{name} ({patient_id})")
            item.setData(Qt.UserRole, patient_id)
            self.sidebar.patient_list.addItem(item)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 