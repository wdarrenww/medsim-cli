from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QSpinBox, QComboBox, 
    QPushButton, QLabel, QTextEdit, QListWidget, QListWidgetItem, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QCheckBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

# Import engines
from ..core.diagnostics import EnhancedDiagnosticSystem
from ..core.treatments import EnhancedTreatmentEngine
from ..core.dialogue import EnhancedDialogueEngine

# Color palette
HIGHLIGHT_COLOR = "#4f8cff"
CRITICAL_COLOR = "#ff4f4f"
WARNING_COLOR = "#ffa726"
SUCCESS_COLOR = "#66bb6a"

class OrderLabDialog(QDialog):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.diagnostic_engine = EnhancedDiagnosticSystem()
        
        self.setWindowTitle("Order Laboratory Test")
        self.setFixedSize(500, 400)
        self.setStyleSheet("background: #f7f9fa;")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # Test selection
        test_group = QGroupBox("Select Test")
        test_layout = QVBoxLayout(test_group)
        
        self.test_list = QListWidget()
        self.test_list.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        
        # Add available tests
        available_tests = self.diagnostic_engine.get_available_lab_tests()
        for test_name, test in list(available_tests.items())[:20]:  # Show first 20
            item = QListWidgetItem(f"{test.name} ({test.category.value}) - ${test.cost:.2f}")
            item.setData(Qt.UserRole, test_name)
            self.test_list.addItem(item)
        
        test_layout.addWidget(self.test_list)
        layout.addWidget(test_group)
        
        # Test details
        details_group = QGroupBox("Test Details")
        details_layout = QFormLayout(details_group)
        
        self.test_name_label = QLabel("Select a test to view details")
        self.test_category_label = QLabel("")
        self.test_cost_label = QLabel("")
        self.test_turnaround_label = QLabel("")
        
        details_layout.addRow("Test:", self.test_name_label)
        details_layout.addRow("Category:", self.test_category_label)
        details_layout.addRow("Cost:", self.test_cost_label)
        details_layout.addRow("Turnaround:", self.test_turnaround_label)
        
        layout.addWidget(details_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(f"background: #ddd; color: #333; border-radius: 4px; padding: 8px 16px;")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.order_btn = QPushButton("Order Test")
        self.order_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px 16px;")
        self.order_btn.clicked.connect(self.order_test)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.order_btn)
        layout.addLayout(btn_layout)
        
        # Connect signals
        self.test_list.itemClicked.connect(self.on_test_selected)

    def on_test_selected(self, item):
        test_name = item.data(Qt.UserRole)
        test = self.diagnostic_engine.get_available_lab_tests()[test_name]
        
        self.test_name_label.setText(test.name)
        self.test_category_label.setText(test.category.value)
        self.test_cost_label.setText(f"${test.cost:.2f}")
        self.test_turnaround_label.setText(f"{test.turnaround_time} minutes")

    def order_test(self):
        current_item = self.test_list.currentItem()
        if current_item:
            test_name = current_item.data(Qt.UserRole)
            result = self.diagnostic_engine.order_lab_test(self.patient_id, test_name)
            QMessageBox.information(self, "Success", f"Ordered {test_name} for patient {self.patient_id}")
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Please select a test to order")

class OrderImagingDialog(QDialog):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.diagnostic_engine = EnhancedDiagnosticSystem()
        
        self.setWindowTitle("Order Imaging Study")
        self.setFixedSize(500, 400)
        self.setStyleSheet("background: #f7f9fa;")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # Study selection
        study_group = QGroupBox("Select Imaging Study")
        study_layout = QVBoxLayout(study_group)
        
        self.study_list = QListWidget()
        self.study_list.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        
        # Add available studies
        available_studies = self.diagnostic_engine.get_available_imaging_studies()
        for study_name, study in available_studies.items():
            item = QListWidgetItem(f"{study.name} ({study.modality.value}) - {study.body_part}")
            item.setData(Qt.UserRole, study_name)
            self.study_list.addItem(item)
        
        study_layout.addWidget(self.study_list)
        layout.addWidget(study_group)
        
        # Study details
        details_group = QGroupBox("Study Details")
        details_layout = QFormLayout(details_group)
        
        self.study_name_label = QLabel("Select a study to view details")
        self.study_modality_label = QLabel("")
        self.study_body_part_label = QLabel("")
        self.study_duration_label = QLabel("")
        
        details_layout.addRow("Study:", self.study_name_label)
        details_layout.addRow("Modality:", self.study_modality_label)
        details_layout.addRow("Body Part:", self.study_body_part_label)
        details_layout.addRow("Duration:", self.study_duration_label)
        
        layout.addWidget(details_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(f"background: #ddd; color: #333; border-radius: 4px; padding: 8px 16px;")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.order_btn = QPushButton("Order Study")
        self.order_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px 16px;")
        self.order_btn.clicked.connect(self.order_study)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.order_btn)
        layout.addLayout(btn_layout)
        
        # Connect signals
        self.study_list.itemClicked.connect(self.on_study_selected)

    def on_study_selected(self, item):
        study_name = item.data(Qt.UserRole)
        study = self.diagnostic_engine.get_available_imaging_studies()[study_name]
        
        self.study_name_label.setText(study.name)
        self.study_modality_label.setText(study.modality.value)
        self.study_body_part_label.setText(study.body_part)
        self.study_duration_label.setText(f"{study.duration} minutes")

    def order_study(self):
        current_item = self.study_list.currentItem()
        if current_item:
            study_name = current_item.data(Qt.UserRole)
            result = self.diagnostic_engine.order_imaging_study(self.patient_id, study_name)
            QMessageBox.information(self, "Success", f"Ordered {study_name} for patient {self.patient_id}")
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Please select a study to order")

class AdministerDrugDialog(QDialog):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.treatment_engine = EnhancedTreatmentEngine()
        
        self.setWindowTitle("Administer Drug")
        self.setFixedSize(500, 400)
        self.setStyleSheet("background: #f7f9fa;")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # Drug selection
        drug_group = QGroupBox("Select Drug")
        drug_layout = QVBoxLayout(drug_group)
        
        self.drug_list = QListWidget()
        self.drug_list.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        
        # Add available drugs
        available_drugs = self.treatment_engine.get_available_drugs()
        for drug_name, drug in list(available_drugs.items())[:20]:  # Show first 20
            routes = ", ".join([route.value for route in drug.routes])
            item = QListWidgetItem(f"{drug.name} ({drug.category.value}) - Routes: {routes}")
            item.setData(Qt.UserRole, drug_name)
            self.drug_list.addItem(item)
        
        drug_layout.addWidget(self.drug_list)
        layout.addWidget(drug_group)
        
        # Administration details
        admin_group = QGroupBox("Administration Details")
        admin_layout = QFormLayout(admin_group)
        
        self.dose_input = QSpinBox()
        self.dose_input.setRange(1, 1000)
        self.dose_input.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ddd;")
        
        self.route_combo = QComboBox()
        self.route_combo.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ddd;")
        
        admin_layout.addRow("Dose:", self.dose_input)
        admin_layout.addRow("Route:", self.route_combo)
        
        layout.addWidget(admin_group)
        
        # Drug details
        details_group = QGroupBox("Drug Details")
        details_layout = QFormLayout(details_group)
        
        self.drug_name_label = QLabel("Select a drug to view details")
        self.drug_category_label = QLabel("")
        self.drug_routes_label = QLabel("")
        
        details_layout.addRow("Drug:", self.drug_name_label)
        details_layout.addRow("Category:", self.drug_category_label)
        details_layout.addRow("Routes:", self.drug_routes_label)
        
        layout.addWidget(details_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(f"background: #ddd; color: #333; border-radius: 4px; padding: 8px 16px;")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.administer_btn = QPushButton("Administer")
        self.administer_btn.setStyleSheet(f"background: {WARNING_COLOR}; color: white; border-radius: 4px; padding: 8px 16px;")
        self.administer_btn.clicked.connect(self.administer_drug)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.administer_btn)
        layout.addLayout(btn_layout)
        
        # Connect signals
        self.drug_list.itemClicked.connect(self.on_drug_selected)

    def on_drug_selected(self, item):
        drug_name = item.data(Qt.UserRole)
        drug = self.treatment_engine.get_available_drugs()[drug_name]
        
        self.drug_name_label.setText(drug.name)
        self.drug_category_label.setText(drug.category.value)
        routes = ", ".join([route.value for route in drug.routes])
        self.drug_routes_label.setText(routes)
        
        # Update route combo
        self.route_combo.clear()
        for route in drug.routes:
            self.route_combo.addItem(route.value)

    def administer_drug(self):
        current_item = self.drug_list.currentItem()
        if current_item and self.route_combo.currentText():
            drug_name = current_item.data(Qt.UserRole)
            dose = self.dose_input.value()
            route = self.route_combo.currentText()
            
            result = self.treatment_engine.administer_drug(self.patient_id, drug_name, dose, route)
            QMessageBox.information(self, "Success", f"Administered {drug_name} to patient {self.patient_id}")
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Please select a drug and route")

class TalkToPatientDialog(QDialog):
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.dialogue_engine = EnhancedDialogueEngine()
        
        self.setWindowTitle("Talk to Patient")
        self.setFixedSize(600, 500)
        self.setStyleSheet("background: #f7f9fa;")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # Conversation area
        conv_group = QGroupBox("Conversation")
        conv_layout = QVBoxLayout(conv_group)
        
        self.conversation_area = QTextEdit()
        self.conversation_area.setStyleSheet("border: 1px solid #ddd; border-radius: 4px; padding: 8px;")
        self.conversation_area.setPlainText("Start a conversation with the patient...")
        conv_layout.addWidget(self.conversation_area)
        
        layout.addWidget(conv_group)
        
        # Message input
        input_group = QGroupBox("Your Message")
        input_layout = QVBoxLayout(input_group)
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message to the patient...")
        self.message_input.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ddd;")
        input_layout.addWidget(self.message_input)
        
        # Question type selection
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Question Type:"))
        
        self.question_type = QComboBox()
        self.question_type.addItems([
            "general", "emotional_assessment", "symptom_inquiry", 
            "treatment_discussion", "medical_history"
        ])
        self.question_type.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ddd;")
        type_layout.addWidget(self.question_type)
        
        input_layout.addLayout(type_layout)
        layout.addWidget(input_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(f"background: #ddd; color: #333; border-radius: 4px; padding: 8px 16px;")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.send_btn = QPushButton("Send Message")
        self.send_btn.setStyleSheet(f"background: {SUCCESS_COLOR}; color: white; border-radius: 4px; padding: 8px 16px;")
        self.send_btn.clicked.connect(self.send_message)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.send_btn)
        layout.addLayout(btn_layout)
        
        # Connect enter key
        self.message_input.returnPressed.connect(self.send_message)

    def send_message(self):
        message = self.message_input.text().strip()
        question_type = self.question_type.currentText()
        
        if message:
            # Get patient response
            response = self.dialogue_engine.get_patient_response(
                self.patient_id, message, question_type
            )
            
            # Update conversation area
            current_text = self.conversation_area.toPlainText()
            new_text = f"{current_text}\n\nDoctor: {message}\nPatient: {response.text}\nEmotion: {response.emotion.value}"
            self.conversation_area.setPlainText(new_text)
            
            # Clear input
            self.message_input.clear()
            
            # Scroll to bottom
            scrollbar = self.conversation_area.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum()) 