from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QTextEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QFrame, QGridLayout,
    QProgressBar, QSlider, QSpinBox, QComboBox, QCheckBox, QListWidget, QListWidgetItem
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
ECG_COLOR = "#00ff00"
PULSE_COLOR = "#ff0000"

class ECGWaveformWidget(QWidget):
    """Realistic ECG waveform display with multiple rhythms"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(150)
        self.setStyleSheet("background: black; border-radius: 8px;")
        
        # ECG parameters
        self.heart_rate = 80
        self.rhythm_type = "normal"  # normal, atrial_fib, ventricular_tachy, asystole
        self.amplitude = 1.0
        self.noise_level = 0.1
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # 20 FPS
        
        # Rhythm patterns
        self.rhythm_patterns = {
            "normal": self._normal_rhythm,
            "atrial_fib": self._atrial_fibrillation,
            "ventricular_tachy": self._ventricular_tachycardia,
            "asystole": self._asystole,
            "bradycardia": self._bradycardia,
            "tachycardia": self._tachycardia
        }

    def set_heart_rate(self, rate):
        self.heart_rate = rate

    def set_rhythm(self, rhythm):
        self.rhythm_type = rhythm

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set up coordinate system
        width = self.width()
        height = self.height()
        painter.translate(0, height // 2)
        
        # Draw grid
        self._draw_grid(painter, width, height)
        
        # Draw ECG waveform
        painter.setPen(QPen(QColor(ECG_COLOR), 2))
        
        # Generate ECG data
        time_points = 1000
        data_points = []
        
        for i in range(time_points):
            x = (i / time_points) * width
            t = (i / time_points) * 10  # 10 seconds of data
            y = self.rhythm_patterns[self.rhythm_type](t) * height * 0.3
            data_points.append((x, y))
        
        # Draw waveform
        for i in range(len(data_points) - 1):
            x1, y1 = data_points[i]
            x2, y2 = data_points[i + 1]
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def _draw_grid(self, painter, width, height):
        """Draw ECG grid lines"""
        painter.setPen(QPen(QColor(50, 50, 50), 1))
        
        # Vertical lines (0.2s intervals)
        for x in range(0, width, width // 50):
            painter.drawLine(x, -height//2, x, height//2)
        
        # Horizontal lines
        for y in range(-height//2, height//2, height//10):
            painter.drawLine(0, y, width, y)

    def _normal_rhythm(self, t):
        """Generate normal sinus rhythm"""
        freq = self.heart_rate / 60.0
        phase = 2 * math.pi * freq * t
        
        # P wave
        p_wave = 0.1 * math.exp(-((phase - 0.5) ** 2) / 0.01)
        
        # QRS complex
        qrs = 0.8 * math.exp(-((phase - 1.0) ** 2) / 0.005)
        
        # T wave
        t_wave = 0.3 * math.exp(-((phase - 1.5) ** 2) / 0.02)
        
        # Add noise
        noise = random.uniform(-self.noise_level, self.noise_level)
        
        return p_wave + qrs + t_wave + noise

    def _atrial_fibrillation(self, t):
        """Generate atrial fibrillation pattern"""
        freq = self.heart_rate / 60.0
        phase = 2 * math.pi * freq * t
        
        # Irregular rhythm
        irregular_phase = phase + random.uniform(-0.5, 0.5)
        
        # P waves are irregular or absent
        p_wave = 0.05 * math.exp(-((irregular_phase - 0.5) ** 2) / 0.02)
        
        # QRS complex
        qrs = 0.8 * math.exp(-((phase - 1.0) ** 2) / 0.005)
        
        # T wave
        t_wave = 0.3 * math.exp(-((phase - 1.5) ** 2) / 0.02)
        
        noise = random.uniform(-self.noise_level, self.noise_level)
        return p_wave + qrs + t_wave + noise

    def _ventricular_tachycardia(self, t):
        """Generate ventricular tachycardia pattern"""
        freq = (self.heart_rate + 100) / 60.0  # Fast rate
        phase = 2 * math.pi * freq * t
        
        # Wide QRS complexes
        qrs = 1.2 * math.exp(-((phase - 1.0) ** 2) / 0.01)
        
        # No clear P waves
        p_wave = 0
        
        # T wave
        t_wave = 0.4 * math.exp(-((phase - 1.5) ** 2) / 0.02)
        
        noise = random.uniform(-self.noise_level, self.noise_level)
        return p_wave + qrs + t_wave + noise

    def _asystole(self, t):
        """Generate asystole (flatline)"""
        return random.uniform(-0.1, 0.1)

    def _bradycardia(self, t):
        """Generate bradycardia pattern"""
        freq = (self.heart_rate - 30) / 60.0  # Slow rate
        phase = 2 * math.pi * freq * t
        return self._normal_rhythm(t / (freq * 60 / self.heart_rate))

    def _tachycardia(self, t):
        """Generate tachycardia pattern"""
        freq = (self.heart_rate + 40) / 60.0  # Fast rate
        phase = 2 * math.pi * freq * t
        return self._normal_rhythm(t / (freq * 60 / self.heart_rate))

class PulseOximeterWidget(QWidget):
    """Realistic pulse oximeter display with waveform"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(100)
        self.setStyleSheet("background: #1a1a1a; border-radius: 8px; color: white;")
        
        layout = QVBoxLayout(self)
        
        # SpO2 display
        self.spo2_label = QLabel("SpO2: 98%")
        self.spo2_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #00ff00;")
        layout.addWidget(self.spo2_label)
        
        # Pulse rate
        self.pulse_label = QLabel("Pulse: 80 bpm")
        self.pulse_label.setStyleSheet("font-size: 18px; color: #ff0000;")
        layout.addWidget(self.pulse_label)
        
        # Waveform widget
        self.waveform = PulseWaveformWidget()
        layout.addWidget(self.waveform)
        
        # Timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_values)
        self.timer.start(1000)

    def update_values(self):
        # Simulate realistic SpO2 and pulse changes
        spo2 = random.randint(95, 100)
        pulse = random.randint(70, 90)
        
        self.spo2_label.setText(f"SpO2: {spo2}%")
        self.pulse_label.setText(f"Pulse: {pulse} bpm")
        
        # Color coding
        if spo2 < 95:
            self.spo2_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ff0000;")
        else:
            self.spo2_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #00ff00;")

class PulseWaveformWidget(QWidget):
    """Pulse oximeter waveform display"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(60)
        self.setStyleSheet("background: #1a1a1a; border: none;")
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        
        self.time_offset = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Draw waveform
        painter.setPen(QPen(QColor(PULSE_COLOR), 2))
        
        points = []
        for x in range(width):
            t = (x + self.time_offset) / 50.0
            y = height//2 + 20 * math.sin(2 * math.pi * 1.2 * t) * math.exp(-0.1 * t)
            points.append((x, y))
        
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
        
        self.time_offset += 2

class DrugInteractionWidget(QWidget):
    """Drug interaction checker and display"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Drug Interactions")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Interaction table
        self.interaction_table = QTableWidget()
        self.interaction_table.setColumnCount(4)
        self.interaction_table.setHorizontalHeaderLabels(["Drug 1", "Drug 2", "Severity", "Effect"])
        self.interaction_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.interaction_table)
        
        # Add sample interactions
        self._add_sample_interactions()

    def _add_sample_interactions(self):
        interactions = [
            ("Warfarin", "Aspirin", "High", "Increased bleeding risk"),
            ("Digoxin", "Furosemide", "Medium", "Electrolyte imbalance"),
            ("Amiodarone", "Warfarin", "High", "Enhanced anticoagulation"),
            ("Metformin", "Furosemide", "Low", "Reduced metformin efficacy"),
            ("Lisinopril", "Ibuprofen", "Medium", "Reduced blood pressure control")
        ]
        
        self.interaction_table.setRowCount(len(interactions))
        for i, (drug1, drug2, severity, effect) in enumerate(interactions):
            self.interaction_table.setItem(i, 0, QTableWidgetItem(drug1))
            self.interaction_table.setItem(i, 1, QTableWidgetItem(drug2))
            
            severity_item = QTableWidgetItem(severity)
            if severity == "High":
                severity_item.setBackground(QColor(CRITICAL_COLOR))
            elif severity == "Medium":
                severity_item.setBackground(QColor(WARNING_COLOR))
            else:
                severity_item.setBackground(QColor(SUCCESS_COLOR))
            self.interaction_table.setItem(i, 2, severity_item)
            
            self.interaction_table.setItem(i, 3, QTableWidgetItem(effect))

class PatientTimelineWidget(QWidget):
    """Patient history timeline with medical events"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Patient Timeline")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Timeline events
        self.timeline_list = QListWidget()
        self.timeline_list.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        layout.addWidget(self.timeline_list)
        
        # Add sample timeline
        self._add_sample_timeline()

    def _add_sample_timeline(self):
        events = [
            ("2024-01-15 08:30", "Patient admitted with chest pain", "Admission"),
            ("2024-01-15 09:15", "ECG shows ST elevation", "Diagnostic"),
            ("2024-01-15 09:45", "Aspirin 325mg administered", "Treatment"),
            ("2024-01-15 10:00", "Cardiology consult ordered", "Consultation"),
            ("2024-01-15 10:30", "Troponin elevated", "Lab Result"),
            ("2024-01-15 11:00", "Heparin drip started", "Treatment")
        ]
        
        for timestamp, event, category in events:
            item = QListWidgetItem(f"[{timestamp}] {event} ({category})")
            if category == "Treatment":
                item.setForeground(QColor(HIGHLIGHT_COLOR))
            elif category == "Diagnostic":
                item.setForeground(QColor(WARNING_COLOR))
            elif category == "Admission":
                item.setForeground(QColor(CRITICAL_COLOR))
            self.timeline_list.addItem(item)

class ProcedureWidget(QWidget):
    """Medical procedure simulation widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Medical Procedures")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Procedure selection
        procedure_layout = QHBoxLayout()
        self.procedure_combo = QComboBox()
        self.procedure_combo.addItems([
            "Central Line Insertion",
            "Intubation",
            "Chest Tube Insertion",
            "Lumbar Puncture",
            "Paracentesis",
            "Thoracentesis"
        ])
        procedure_layout.addWidget(QLabel("Procedure:"))
        procedure_layout.addWidget(self.procedure_combo)
        
        self.start_btn = QPushButton("Start Procedure")
        self.start_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        self.start_btn.clicked.connect(self.start_procedure)
        procedure_layout.addWidget(self.start_btn)
        
        layout.addLayout(procedure_layout)
        
        # Procedure steps
        self.steps_list = QListWidget()
        self.steps_list.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        layout.addWidget(self.steps_list)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("QProgressBar { border: 2px solid #ddd; border-radius: 4px; }")
        layout.addWidget(self.progress_bar)

    def start_procedure(self):
        procedure = self.procedure_combo.currentText()
        self.steps_list.clear()
        self.progress_bar.setValue(0)
        
        # Define procedure steps
        steps = {
            "Central Line Insertion": [
                "Prepare sterile field",
                "Administer local anesthesia",
                "Insert introducer needle",
                "Place guidewire",
                "Dilate tract",
                "Insert central line",
                "Confirm placement with X-ray",
                "Secure line and dress site"
            ],
            "Intubation": [
                "Pre-oxygenate patient",
                "Prepare laryngoscope and tube",
                "Position patient",
                "Insert laryngoscope",
                "Visualize vocal cords",
                "Insert endotracheal tube",
                "Inflate cuff",
                "Confirm placement",
                "Secure tube"
            ],
            "Chest Tube Insertion": [
                "Prepare sterile field",
                "Administer local anesthesia",
                "Make skin incision",
                "Blunt dissection to pleura",
                "Insert chest tube",
                "Connect to drainage system",
                "Secure tube and dress site"
            ]
        }
        
        if procedure in steps:
            for i, step in enumerate(steps[procedure]):
                item = QListWidgetItem(f"{i+1}. {step}")
                self.steps_list.addItem(item)
            
            # Animate progress
            self._animate_progress()

    def _animate_progress(self):
        self.progress_bar.setValue(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_progress)
        self.timer.start(1000)  # Update every second

    def _update_progress(self):
        current = self.progress_bar.value()
        if current < 100:
            self.progress_bar.setValue(current + 10)
        else:
            self.timer.stop()

class VentilatorWidget(QWidget):
    """Mechanical ventilator simulation widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Mechanical Ventilator")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Ventilator settings
        settings_layout = QGridLayout()
        
        # Tidal Volume
        settings_layout.addWidget(QLabel("Tidal Volume (mL):"), 0, 0)
        self.tidal_volume = QSpinBox()
        self.tidal_volume.setRange(200, 800)
        self.tidal_volume.setValue(500)
        settings_layout.addWidget(self.tidal_volume, 0, 1)
        
        # Respiratory Rate
        settings_layout.addWidget(QLabel("Respiratory Rate (/min):"), 1, 0)
        self.resp_rate = QSpinBox()
        self.resp_rate.setRange(8, 35)
        self.resp_rate.setValue(12)
        settings_layout.addWidget(self.resp_rate, 1, 1)
        
        # PEEP
        settings_layout.addWidget(QLabel("PEEP (cmH2O):"), 2, 0)
        self.peep = QSpinBox()
        self.peep.setRange(0, 20)
        self.peep.setValue(5)
        settings_layout.addWidget(self.peep, 2, 1)
        
        # FiO2
        settings_layout.addWidget(QLabel("FiO2 (%):"), 3, 0)
        self.fio2 = QSpinBox()
        self.fio2.setRange(21, 100)
        self.fio2.setValue(40)
        settings_layout.addWidget(self.fio2, 3, 1)
        
        layout.addLayout(settings_layout)
        
        # Ventilator waveform
        self.vent_waveform = VentilatorWaveformWidget()
        layout.addWidget(self.vent_waveform)
        
        # Apply button
        self.apply_btn = QPushButton("Apply Settings")
        self.apply_btn.setStyleSheet(f"background: {HIGHLIGHT_COLOR}; color: white; border-radius: 4px; padding: 8px;")
        self.apply_btn.clicked.connect(self.apply_settings)
        layout.addWidget(self.apply_btn)

    def apply_settings(self):
        # Update ventilator waveform with new settings
        self.vent_waveform.set_settings(
            self.tidal_volume.value(),
            self.resp_rate.value(),
            self.peep.value(),
            self.fio2.value()
        )

class VentilatorWaveformWidget(QWidget):
    """Ventilator pressure/flow waveform display"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(120)
        self.setStyleSheet("background: black; border-radius: 8px;")
        
        self.tidal_volume = 500
        self.resp_rate = 12
        self.peep = 5
        self.fio2 = 40
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        
        self.time_offset = 0

    def set_settings(self, tv, rr, peep, fio2):
        self.tidal_volume = tv
        self.resp_rate = rr
        self.peep = peep
        self.fio2 = fio2

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Draw pressure waveform
        painter.setPen(QPen(QColor(255, 255, 0), 2))  # Yellow for pressure
        
        points = []
        for x in range(width):
            t = (x + self.time_offset) / 50.0
            cycle_time = 60.0 / self.resp_rate
            
            # Pressure waveform
            if t % cycle_time < 0.4:  # Inspiration
                pressure = self.peep + 20 * math.sin(math.pi * (t % cycle_time) / 0.4)
            else:  # Expiration
                pressure = self.peep + 5 * math.exp(-(t % cycle_time - 0.4) / 0.6)
            
            y = height//2 - pressure * 2
            points.append((x, y))
        
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
        
        self.time_offset += 1 