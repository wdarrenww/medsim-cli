from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QTextEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QFrame, QGridLayout,
    QProgressBar, QSlider, QSpinBox, QComboBox, QCheckBox, QListWidget, QListWidgetItem,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem
)
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPixmap, QBrush, QRadialGradient
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Signal, QRectF, QPointF
import math
import random
from datetime import datetime, timedelta

# Color palette
HIGHLIGHT_COLOR = "#4f8cff"
CRITICAL_COLOR = "#ff4f4f"
WARNING_COLOR = "#ffa726"
SUCCESS_COLOR = "#66bb6a"
IMAGING_COLOR = "#00ffff"

class XRayViewerWidget(QWidget):
    """X-ray image viewer with annotations and findings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.study_combo = QComboBox()
        self.study_combo.addItems([
            "Chest X-ray - Normal",
            "Chest X-ray - Pneumonia",
            "Chest X-ray - Pneumothorax",
            "Chest X-ray - CHF",
            "Chest X-ray - COPD",
            "Abdominal X-ray - Normal",
            "Abdominal X-ray - Bowel Obstruction",
            "Abdominal X-ray - Free Air",
            "Cervical Spine - Normal",
            "Cervical Spine - Fracture"
        ])
        self.study_combo.currentTextChanged.connect(self.load_xray)
        
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(0, 100)
        self.contrast_slider.setValue(50)
        self.contrast_slider.valueChanged.connect(self.update_contrast)
        
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(0, 100)
        self.brightness_slider.setValue(50)
        self.brightness_slider.valueChanged.connect(self.update_brightness)
        
        controls_layout.addWidget(QLabel("Study:"))
        controls_layout.addWidget(self.study_combo)
        controls_layout.addWidget(QLabel("Contrast:"))
        controls_layout.addWidget(self.contrast_slider)
        controls_layout.addWidget(QLabel("Brightness:"))
        controls_layout.addWidget(self.brightness_slider)
        
        layout.addLayout(controls_layout)
        
        # Image viewer
        self.image_view = QGraphicsView()
        self.image_view.setMinimumHeight(400)
        self.image_view.setStyleSheet("border: 2px solid #ddd; border-radius: 4px;")
        
        self.scene = QGraphicsScene()
        self.image_view.setScene(self.scene)
        
        layout.addWidget(self.image_view)
        
        # Findings panel
        findings_group = QGroupBox("Radiological Findings")
        findings_layout = QVBoxLayout(findings_group)
        
        self.findings_text = QTextEdit()
        self.findings_text.setMaximumHeight(150)
        self.findings_text.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        findings_layout.addWidget(self.findings_text)
        
        layout.addWidget(findings_group)
        
        # Load initial image
        self.load_xray(self.study_combo.currentText())

    def load_xray(self, study_name):
        # Clear existing items
        self.scene.clear()
        
        # Create simulated X-ray image
        width = 600
        height = 400
        
        # Create base image with different patterns based on study
        if "Chest" in study_name:
            if "Normal" in study_name:
                self._create_normal_chest_xray(width, height)
            elif "Pneumonia" in study_name:
                self._create_pneumonia_chest_xray(width, height)
            elif "Pneumothorax" in study_name:
                self._create_pneumothorax_chest_xray(width, height)
            elif "CHF" in study_name:
                self._create_chf_chest_xray(width, height)
            elif "COPD" in study_name:
                self._create_copd_chest_xray(width, height)
        elif "Abdominal" in study_name:
            if "Normal" in study_name:
                self._create_normal_abdomen_xray(width, height)
            elif "Bowel Obstruction" in study_name:
                self._create_bowel_obstruction_xray(width, height)
            elif "Free Air" in study_name:
                self._create_free_air_xray(width, height)
        elif "Cervical Spine" in study_name:
            if "Normal" in study_name:
                self._create_normal_cspine_xray(width, height)
            elif "Fracture" in study_name:
                self._create_cspine_fracture_xray(width, height)
        
        # Update findings
        self._update_findings(study_name)

    def _create_normal_chest_xray(self, width, height):
        # Create normal chest X-ray pattern
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(200, 200, 200))  # Light gray background
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        
        # Draw lungs
        painter.drawEllipse(100, 150, 150, 200)  # Left lung
        painter.drawEllipse(350, 150, 150, 200)  # Right lung
        
        # Draw heart shadow
        painter.setBrush(QBrush(QColor(150, 150, 150)))
        painter.drawEllipse(250, 200, 100, 120)
        
        # Draw ribs
        for i in range(5):
            y = 120 + i * 30
            painter.drawLine(50, y, 550, y)
        
        painter.end()
        
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)

    def _create_pneumonia_chest_xray(self, width, height):
        # Create pneumonia pattern
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(200, 200, 200))
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        
        # Draw lungs with infiltrate
        painter.drawEllipse(100, 150, 150, 200)
        painter.drawEllipse(350, 150, 150, 200)
        
        # Add infiltrate in right lower lobe
        painter.setBrush(QBrush(QColor(80, 80, 80)))
        painter.drawEllipse(380, 280, 100, 60)
        
        painter.end()
        
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)

    def _create_pneumothorax_chest_xray(self, width, height):
        # Create pneumothorax pattern
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(200, 200, 200))
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        
        # Draw lungs
        painter.drawEllipse(100, 150, 150, 200)
        painter.drawEllipse(350, 150, 150, 200)
        
        # Add pneumothorax (air outside lung)
        painter.setBrush(QBrush(QColor(220, 220, 220)))
        painter.drawEllipse(320, 150, 80, 200)
        
        painter.end()
        
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)

    def _create_chf_chest_xray(self, width, height):
        # Create CHF pattern
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(200, 200, 200))
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        
        # Draw enlarged heart
        painter.setBrush(QBrush(QColor(150, 150, 150)))
        painter.drawEllipse(220, 180, 160, 140)
        
        # Draw pulmonary edema
        painter.setBrush(QBrush(QColor(120, 120, 120)))
        painter.drawEllipse(100, 150, 150, 200)
        painter.drawEllipse(350, 150, 150, 200)
        
        painter.end()
        
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)

    def _create_copd_chest_xray(self, width, height):
        # Create COPD pattern
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(200, 200, 200))
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        
        # Draw hyperinflated lungs
        painter.drawEllipse(80, 120, 170, 230)
        painter.drawEllipse(350, 120, 170, 230)
        
        # Flattened diaphragm
        painter.drawLine(50, 350, 550, 350)
        
        painter.end()
        
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)

    def _create_normal_abdomen_xray(self, width, height):
        # Create normal abdominal X-ray
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(200, 200, 200))
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        
        # Draw bowel gas pattern
        for i in range(8):
            x = 100 + i * 60
            y = 150 + random.randint(-20, 20)
            painter.drawEllipse(x, y, 40, 30)
        
        painter.end()
        
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)

    def _create_bowel_obstruction_xray(self, width, height):
        # Create bowel obstruction pattern
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(200, 200, 200))
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        
        # Draw dilated loops
        painter.setBrush(QBrush(QColor(180, 180, 180)))
        painter.drawEllipse(150, 200, 100, 80)
        painter.drawEllipse(350, 200, 100, 80)
        
        painter.end()
        
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)

    def _create_free_air_xray(self, width, height):
        # Create free air pattern
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(200, 200, 200))
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        
        # Draw free air under diaphragm
        painter.setBrush(QBrush(QColor(220, 220, 220)))
        painter.drawEllipse(200, 50, 200, 60)
        
        painter.end()
        
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)

    def _create_normal_cspine_xray(self, width, height):
        # Create normal cervical spine X-ray
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(200, 200, 200))
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        
        # Draw vertebrae
        for i in range(7):
            y = 100 + i * 40
            painter.drawEllipse(250, y, 100, 30)
        
        painter.end()
        
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)

    def _create_cspine_fracture_xray(self, width, height):
        # Create cervical spine fracture pattern
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(200, 200, 200))
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        
        # Draw vertebrae with fracture
        for i in range(7):
            y = 100 + i * 40
            if i == 3:  # Fracture at C4
                painter.setBrush(QBrush(QColor(150, 150, 150)))
                painter.drawEllipse(250, y, 100, 30)
                painter.drawLine(300, y, 300, y + 30)
            else:
                painter.drawEllipse(250, y, 100, 30)
        
        painter.end()
        
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)

    def update_contrast(self, value):
        # Simulate contrast adjustment
        pass

    def update_brightness(self, value):
        # Simulate brightness adjustment
        pass

    def _update_findings(self, study_name):
        findings = {
            "Chest X-ray - Normal": "Normal cardiac silhouette. Clear lung fields. No infiltrates or effusions. Normal mediastinal contours.",
            "Chest X-ray - Pneumonia": "Right lower lobe infiltrate. No pleural effusion. Normal cardiac silhouette.",
            "Chest X-ray - Pneumothorax": "Large right pneumothorax. Mediastinal shift to the left. No rib fractures.",
            "Chest X-ray - CHF": "Cardiomegaly. Bilateral pulmonary edema. Kerley B lines present.",
            "Chest X-ray - COPD": "Hyperinflated lungs. Flattened diaphragms. Increased AP diameter.",
            "Abdominal X-ray - Normal": "Normal bowel gas pattern. No obstruction or free air.",
            "Abdominal X-ray - Bowel Obstruction": "Multiple dilated small bowel loops. Air-fluid levels present.",
            "Abdominal X-ray - Free Air": "Free air under both hemidiaphragms. Suggestive of perforation.",
            "Cervical Spine - Normal": "Normal cervical spine alignment. No fractures or dislocations.",
            "Cervical Spine - Fracture": "Fracture of C4 vertebral body. No dislocation. Normal alignment maintained."
        }
        
        self.findings_text.setPlainText(findings.get(study_name, "No findings available."))

class CTScanViewerWidget(QWidget):
    """CT scan viewer with multiple slices"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.study_combo = QComboBox()
        self.study_combo.addItems([
            "Head CT - Normal",
            "Head CT - Hemorrhage",
            "Head CT - Mass",
            "Chest CT - Normal",
            "Chest CT - PE",
            "Chest CT - Pneumonia",
            "Abdominal CT - Normal",
            "Abdominal CT - Appendicitis"
        ])
        self.study_combo.currentTextChanged.connect(self.load_ct)
        
        self.slice_slider = QSlider(Qt.Horizontal)
        self.slice_slider.setRange(0, 20)
        self.slice_slider.setValue(10)
        self.slice_slider.valueChanged.connect(self.update_slice)
        
        controls_layout.addWidget(QLabel("Study:"))
        controls_layout.addWidget(self.study_combo)
        controls_layout.addWidget(QLabel("Slice:"))
        controls_layout.addWidget(self.slice_slider)
        
        layout.addLayout(controls_layout)
        
        # CT viewer
        self.ct_view = QGraphicsView()
        self.ct_view.setMinimumHeight(400)
        self.ct_view.setStyleSheet("border: 2px solid #ddd; border-radius: 4px;")
        
        self.ct_scene = QGraphicsScene()
        self.ct_view.setScene(self.ct_scene)
        
        layout.addWidget(self.ct_view)
        
        # Load initial CT
        self.load_ct(self.study_combo.currentText())

    def load_ct(self, study_name):
        self.ct_scene.clear()
        self._create_ct_slice(study_name, self.slice_slider.value())

    def update_slice(self, slice_num):
        study_name = self.study_combo.currentText()
        self._create_ct_slice(study_name, slice_num)

    def _create_ct_slice(self, study_name, slice_num):
        width = 400
        height = 400
        
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(50, 50, 50))  # Dark background for CT
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        
        if "Head CT" in study_name:
            self._create_head_ct_slice(painter, width, height, slice_num, study_name)
        elif "Chest CT" in study_name:
            self._create_chest_ct_slice(painter, width, height, slice_num, study_name)
        elif "Abdominal CT" in study_name:
            self._create_abdomen_ct_slice(painter, width, height, slice_num, study_name)
        
        painter.end()
        
        item = QGraphicsPixmapItem(pixmap)
        self.ct_scene.addItem(item)

    def _create_head_ct_slice(self, painter, width, height, slice_num, study_name):
        # Create head CT slice
        center_x, center_y = width // 2, height // 2
        
        # Draw skull
        painter.setPen(QPen(QColor(150, 150, 150), 2))
        painter.drawEllipse(center_x - 80, center_y - 80, 160, 160)
        
        # Draw brain tissue
        painter.setPen(QPen(QColor(100, 100, 100), 1))
        painter.drawEllipse(center_x - 70, center_y - 70, 140, 140)
        
        if "Hemorrhage" in study_name and slice_num > 5:
            # Add hemorrhage
            painter.setBrush(QBrush(QColor(80, 80, 80)))
            painter.drawEllipse(center_x - 20, center_y - 30, 40, 30)
        
        if "Mass" in study_name and slice_num > 8:
            # Add mass
            painter.setBrush(QBrush(QColor(120, 120, 120)))
            painter.drawEllipse(center_x + 20, center_y - 20, 30, 40)

    def _create_chest_ct_slice(self, painter, width, height, slice_num, study_name):
        # Create chest CT slice
        center_x, center_y = width // 2, height // 2
        
        # Draw lungs
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        painter.drawEllipse(center_x - 120, center_y - 60, 80, 120)
        painter.drawEllipse(center_x + 40, center_y - 60, 80, 120)
        
        # Draw heart
        painter.setPen(QPen(QColor(150, 150, 150), 2))
        painter.drawEllipse(center_x - 30, center_y - 40, 60, 80)
        
        if "PE" in study_name and slice_num > 10:
            # Add pulmonary embolism
            painter.setBrush(QBrush(QColor(100, 100, 100)))
            painter.drawEllipse(center_x + 60, center_y - 20, 20, 15)
        
        if "Pneumonia" in study_name and slice_num > 8:
            # Add pneumonia
            painter.setBrush(QBrush(QColor(120, 120, 120)))
            painter.drawEllipse(center_x - 100, center_y + 20, 60, 40)

    def _create_abdomen_ct_slice(self, painter, width, height, slice_num, study_name):
        # Create abdominal CT slice
        center_x, center_y = width // 2, height // 2
        
        # Draw abdominal organs
        painter.setPen(QPen(QColor(150, 150, 150), 1))
        painter.drawEllipse(center_x - 100, center_y - 80, 200, 160)
        
        if "Appendicitis" in study_name and slice_num > 12:
            # Add inflamed appendix
            painter.setBrush(QBrush(QColor(120, 120, 120)))
            painter.drawEllipse(center_x + 60, center_y + 40, 20, 30)

class UltrasoundWidget(QWidget):
    """Ultrasound simulator with realistic imaging"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.us_study_combo = QComboBox()
        self.us_study_combo.addItems([
            "Cardiac Echo - Normal",
            "Cardiac Echo - CHF",
            "Abdominal US - Normal",
            "Abdominal US - Gallstones",
            "Abdominal US - Aortic Aneurysm",
            "Obstetric US - Normal Pregnancy",
            "Obstetric US - Ectopic Pregnancy"
        ])
        self.us_study_combo.currentTextChanged.connect(self.load_ultrasound)
        
        self.depth_slider = QSlider(Qt.Horizontal)
        self.depth_slider.setRange(5, 20)
        self.depth_slider.setValue(10)
        self.depth_slider.valueChanged.connect(self.update_depth)
        
        controls_layout.addWidget(QLabel("Study:"))
        controls_layout.addWidget(self.us_study_combo)
        controls_layout.addWidget(QLabel("Depth:"))
        controls_layout.addWidget(self.depth_slider)
        
        layout.addLayout(controls_layout)
        
        # Ultrasound viewer
        self.us_view = QGraphicsView()
        self.us_view.setMinimumHeight(400)
        self.us_view.setStyleSheet("border: 2px solid #ddd; border-radius: 4px;")
        
        self.us_scene = QGraphicsScene()
        self.us_view.setScene(self.us_scene)
        
        layout.addWidget(self.us_view)
        
        # Load initial ultrasound
        self.load_ultrasound(self.us_study_combo.currentText())

    def load_ultrasound(self, study_name):
        self.us_scene.clear()
        self._create_ultrasound_image(study_name)

    def update_depth(self, depth):
        study_name = self.us_study_combo.currentText()
        self._create_ultrasound_image(study_name)

    def _create_ultrasound_image(self, study_name):
        width = 500
        height = 400
        
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(0, 0, 0))  # Black background for ultrasound
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if "Cardiac Echo" in study_name:
            self._create_cardiac_echo(painter, width, height, study_name)
        elif "Abdominal US" in study_name:
            self._create_abdominal_us(painter, width, height, study_name)
        elif "Obstetric US" in study_name:
            self._create_obstetric_us(painter, width, height, study_name)
        
        painter.end()
        
        item = QGraphicsPixmapItem(pixmap)
        self.us_scene.addItem(item)

    def _create_cardiac_echo(self, painter, width, height, study_name):
        # Create cardiac echo image
        center_x, center_y = width // 2, height // 2
        
        # Draw heart chambers
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        
        # Left ventricle
        painter.drawEllipse(center_x - 60, center_y - 40, 120, 80)
        
        # Right ventricle
        painter.drawEllipse(center_x + 40, center_y - 30, 80, 60)
        
        # Atria
        painter.drawEllipse(center_x - 40, center_y - 80, 80, 40)
        painter.drawEllipse(center_x + 20, center_y - 80, 80, 40)
        
        if "CHF" in study_name:
            # Add dilated chambers
            painter.setBrush(QBrush(QColor(200, 200, 200)))
            painter.drawEllipse(center_x - 80, center_y - 50, 160, 100)

    def _create_abdominal_us(self, painter, width, height, study_name):
        # Create abdominal ultrasound image
        center_x, center_y = width // 2, height // 2
        
        # Draw liver
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.drawEllipse(center_x - 100, center_y - 60, 200, 120)
        
        if "Gallstones" in study_name:
            # Add gallstones
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            for i in range(3):
                x = center_x - 50 + i * 30
                y = center_y - 20
                painter.drawEllipse(x, y, 15, 15)
        
        if "Aortic Aneurysm" in study_name:
            # Add dilated aorta
            painter.setPen(QPen(QColor(255, 255, 255), 3))
            painter.drawEllipse(center_x - 20, center_y - 40, 40, 80)

    def _create_obstetric_us(self, painter, width, height, study_name):
        # Create obstetric ultrasound image
        center_x, center_y = width // 2, height // 2
        
        # Draw uterus
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.drawEllipse(center_x - 80, center_y - 60, 160, 120)
        
        if "Normal Pregnancy" in study_name:
            # Add fetus
            painter.setBrush(QBrush(QColor(200, 200, 200)))
            painter.drawEllipse(center_x - 30, center_y - 20, 60, 40)
            
            # Add heartbeat
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawEllipse(center_x - 5, center_y - 5, 10, 10)
        
        if "Ectopic Pregnancy" in study_name:
            # Add ectopic pregnancy
            painter.setBrush(QBrush(QColor(200, 200, 200)))
            painter.drawEllipse(center_x + 100, center_y - 30, 40, 30) 