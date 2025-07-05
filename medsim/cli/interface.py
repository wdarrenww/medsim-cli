"""
command-line interface for medical simulator
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from typing import Optional, List, Dict, Any
import sys
import os
from datetime import datetime
import readline
import json
from pathlib import Path

from ..core.simulation import MedicalSimulation, PatientState
from ..core.session import SessionManager
from ..core.physiology import PhysiologicalEngine
from ..core.dialogue import AdvancedDialogueSystem
from ..core.diagnostics import AdvancedDiagnosticSystem
from ..core.treatments import AdvancedTreatmentSystem
from ..scenarios.scenario_manager import ScenarioManager
from ..assessment.performance import AssessmentSystem
from ..api.core import MedicalSimulatorAPI

console = Console()
app = typer.Typer()


class SimulatorCLI:
    """main cli interface for the medical simulator"""
    
    def __init__(self):
        self.simulation = MedicalSimulation()
        self.session_manager = SessionManager()
        self.physiology = PhysiologicalEngine()
        self.dialogue = AdvancedDialogueSystem()
        self.diagnostics = AdvancedDiagnosticSystem()
        self.treatments = AdvancedTreatmentSystem()
        self.scenarios = ScenarioManager()
        self.assessment = AssessmentSystem()
        self.current_patient_id: Optional[str] = None
        self.is_running = False
        self.current_scenario_id: Optional[str] = None
        self.api = MedicalSimulatorAPI()
        self.command_history: List[str] = []
        self.history_file = Path.home() / ".medsim_history"
        self._load_command_history()
        self._setup_autocompletion()
        
    def _load_command_history(self):
        """load command history from file"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    self.command_history = [line.strip() for line in f.readlines()]
        except Exception as e:
            console.print(f"[yellow]Warning: Could not load command history: {e}[/yellow]")
    
    def _save_command_history(self):
        """save command history to file"""
        try:
            with open(self.history_file, 'w') as f:
                for command in self.command_history[-100:]:  # keep last 100 commands
                    f.write(command + '\n')
        except Exception as e:
            console.print(f"[yellow]Warning: Could not save command history: {e}[/yellow]")
    
    def _setup_autocompletion(self):
        """setup command autocompletion"""
        self.available_commands = [
            "help", "start", "scenario", "patient", "vitals", "symptoms", 
            "medications", "procedures", "protocols", "labs", "imaging", 
            "dialogue", "examination", "diagnosis", "save", "load", 
            "status", "step", "pause", "reset", "assessment", "quit",
            "alerts", "interpret", "pending", "available", "api", "json",
            "plugins"
        ]
        
        def completer(text, state):
            options = [cmd for cmd in self.available_commands if cmd.startswith(text)]
            if state < len(options):
                return options[state]
            return None
        
        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")
    
    def _add_to_history(self, command: str):
        """add command to history"""
        if command and command not in self.command_history:
            self.command_history.append(command)
    
    def _get_json_output(self, data: Any) -> str:
        """convert data to JSON string"""
        if hasattr(data, '__dict__'):
            return json.dumps(data.__dict__, default=str, indent=2)
        return json.dumps(data, default=str, indent=2)
    
    def display_welcome(self) -> None:
        """display welcome message"""
        welcome_text = Text("Medical Simulator CLI", style="bold blue")
        subtitle = Text("Professional-grade medical simulation platform", style="italic")
        
        panel = Panel(
            f"{welcome_text}\n{subtitle}",
            border_style="blue",
            padding=(1, 2)
        )
        console.print(panel)
        console.print()
    
    def display_help(self):
        """display help information"""
        console.print("\n[bold cyan]Medical Simulator CLI - Available Commands[/bold cyan]\n")
        
        # core simulation commands
        console.print("[bold yellow]Core Simulation:[/bold yellow]")
        console.print("  start      - Start a new simulation session")
        console.print("  scenario   - Select a specific scenario")
        console.print("  status     - Show current simulation status")
        console.print("  step       - Advance simulation by one time step")
        console.print("  pause      - Pause simulation")
        console.print("  reset      - Reset current simulation")
        console.print("  quit       - Exit simulator")
        
        # patient management
        console.print("\n[bold yellow]Patient Management:[/bold yellow]")
        console.print("  patient    - View patient information")
        console.print("  vitals     - View or update vital signs")
        console.print("  symptoms   - View or add patient symptoms")
        console.print("  medications - View or add patient medications")
        
        # clinical activities
        console.print("\n[bold yellow]Clinical Activities:[/bold yellow]")
        console.print("  dialogue   - Start patient dialogue")
        console.print("  examination - Perform physical examination")
        console.print("  procedures - Perform clinical procedures")
        console.print("  protocols  - Execute clinical protocols")
        
        # diagnostics
        console.print("\n[bold yellow]Diagnostics:[/bold yellow]")
        console.print("  labs       - Order and view lab tests")
        console.print("  imaging    - Order and view imaging studies")
        console.print("  alerts     - Show critical lab/imaging alerts")
        console.print("  interpret  - Interpret lab or imaging results")
        console.print("  pending    - Show pending lab/imaging orders")
        console.print("  available  - Show available tests and studies")
        
        # assessment and data
        console.print("\n[bold yellow]Assessment & Data:[/bold yellow]")
        console.print("  diagnosis  - View current diagnosis")
        console.print("  assessment - View performance assessment")
        console.print("  save       - Save current session")
        console.print("  load       - Load saved session")
        
        # plugin management
        console.print("\n[bold yellow]Plugin Management:[/bold yellow]")
        console.print("  plugins    - List loaded plugins")
        console.print("  plugin     - Manage a specific plugin")
        
        console.print("\n[dim]Type any command to execute it. Use 'help' to see this again.[/dim]")
    
    def start_simulation(self) -> None:
        """start a new simulation session"""
        console.print("[bold green]Starting new simulation session...[/bold green]")
        
        # create a default patient for demonstration
        patient = self.simulation.add_patient(
            patient_id="P001",
            name="John Smith",
            age=58,
            gender="Male"
        )
        
        self.current_patient_id = patient.patient_id
        self.simulation.start_simulation()
        self.is_running = True
        
        console.print(f"[green]✓[/green] Simulation started with patient: {patient.name}")
        console.print(f"[green]✓[/green] Patient ID: {patient.patient_id}")
        console.print()
    
    def show_patient_info(self) -> None:
        """display current patient information"""
        if not self.current_patient_id:
            console.print("[red]No patient selected. Start a simulation first.[/red]")
            return
        
        patient = self.simulation.get_patient(self.current_patient_id)
        if not patient:
            console.print("[red]Patient not found.[/red]")
            return
        
        # create patient info table
        table = Table(title=f"Patient Information - {patient.name}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("ID", patient.patient_id)
        table.add_row("Name", patient.name)
        table.add_row("Age", str(patient.age))
        table.add_row("Gender", patient.gender)
        table.add_row("Timestamp", patient.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        
        console.print(table)
        console.print()
    
    def show_vital_signs(self) -> None:
        """display patient vital signs"""
        if not self.current_patient_id:
            console.print("[red]No patient selected.[/red]")
            return
        
        patient = self.simulation.get_patient(self.current_patient_id)
        if not patient:
            console.print("[red]Patient not found.[/red]")
            return
        
        if not patient.vital_signs:
            console.print("[yellow]No vital signs recorded yet.[/yellow]")
            return
        
        table = Table(title="Vital Signs")
        table.add_column("Vital Sign", style="cyan")
        table.add_column("Value", style="white")
        table.add_column("Unit", style="dim")
        
        vitals_map = {
            'bp_systolic': ('Blood Pressure (Systolic)', 'mmHg'),
            'bp_diastolic': ('Blood Pressure (Diastolic)', 'mmHg'),
            'heart_rate': ('Heart Rate', 'bpm'),
            'respiratory_rate': ('Respiratory Rate', 'breaths/min'),
            'temperature': ('Temperature', '°F'),
            'oxygen_saturation': ('Oxygen Saturation', '%')
        }
        
        for key, (name, unit) in vitals_map.items():
            if key in patient.vital_signs:
                table.add_row(name, str(patient.vital_signs[key]), unit)
        
        console.print(table)
        console.print()
    
    def update_vital_signs(self) -> None:
        """update patient vital signs"""
        if not self.current_patient_id:
            console.print("[red]No patient selected.[/red]")
            return
        
        console.print("[bold]Update Vital Signs[/bold]")
        console.print("Enter new values (press Enter to skip):")
        
        vitals = {}
        
        # collect vital signs input
        bp_systolic = Prompt.ask("Blood Pressure (Systolic)", default="")
        if bp_systolic:
            try:
                vitals['bp_systolic'] = float(bp_systolic)
            except ValueError:
                console.print("[red]Invalid systolic BP value[/red]")
                return
        
        bp_diastolic = Prompt.ask("Blood Pressure (Diastolic)", default="")
        if bp_diastolic:
            try:
                vitals['bp_diastolic'] = float(bp_diastolic)
            except ValueError:
                console.print("[red]Invalid diastolic BP value[/red]")
                return
        
        heart_rate = Prompt.ask("Heart Rate (bpm)", default="")
        if heart_rate:
            try:
                vitals['heart_rate'] = float(heart_rate)
            except ValueError:
                console.print("[red]Invalid heart rate value[/red]")
                return
        
        respiratory_rate = Prompt.ask("Respiratory Rate (breaths/min)", default="")
        if respiratory_rate:
            try:
                vitals['respiratory_rate'] = float(respiratory_rate)
            except ValueError:
                console.print("[red]Invalid respiratory rate value[/red]")
                return
        
        temperature = Prompt.ask("Temperature (°F)", default="")
        if temperature:
            try:
                vitals['temperature'] = float(temperature)
            except ValueError:
                console.print("[red]Invalid temperature value[/red]")
                return
        
        oxygen_saturation = Prompt.ask("Oxygen Saturation (%)", default="")
        if oxygen_saturation:
            try:
                vitals['oxygen_saturation'] = float(oxygen_saturation)
            except ValueError:
                console.print("[red]Invalid oxygen saturation value[/red]")
                return
        
        if vitals:
            patient = self.simulation.get_patient(self.current_patient_id)
            patient.update_vital_signs(vitals)
            console.print("[green]✓[/green] Vital signs updated successfully")
        else:
            console.print("[yellow]No vital signs entered[/yellow]")
        
        console.print()
    
    def show_symptoms(self) -> None:
        """display patient symptoms"""
        if not self.current_patient_id:
            console.print("[red]No patient selected.[/red]")
            return
        
        patient = self.simulation.get_patient(self.current_patient_id)
        if not patient:
            console.print("[red]Patient not found.[/red]")
            return
        
        if not patient.symptoms:
            console.print("[yellow]No symptoms recorded.[/yellow]")
            return
        
        table = Table(title="Patient Symptoms")
        table.add_column("Symptom", style="red")
        
        for symptom in patient.symptoms:
            table.add_row(symptom)
        
        console.print(table)
        console.print()
    
    def add_symptom(self) -> None:
        """add a symptom to the patient"""
        if not self.current_patient_id:
            console.print("[red]No patient selected.[/red]")
            return
        
        symptom = Prompt.ask("Enter symptom to add")
        if symptom:
            patient = self.simulation.get_patient(self.current_patient_id)
            patient.add_symptom(symptom)
            console.print(f"[green]✓[/green] Added symptom: {symptom}")
        else:
            console.print("[yellow]No symptom entered[/yellow]")
        
        console.print()
    
    def show_medications(self) -> None:
        """display patient medications"""
        if not self.current_patient_id:
            console.print("[red]No patient selected.[/red]")
            return
        
        patient = self.simulation.get_patient(self.current_patient_id)
        if not patient:
            console.print("[red]Patient not found.[/red]")
            return
        
        if not patient.medications:
            console.print("[yellow]No medications recorded.[/yellow]")
            return
        
        table = Table(title="Patient Medications")
        table.add_column("Medication", style="blue")
        
        for medication in patient.medications:
            table.add_row(medication)
        
        console.print(table)
        console.print()
    
    def add_medication(self) -> None:
        """add a medication to the patient"""
        if not self.current_patient_id:
            console.print("[red]No patient selected.[/red]")
            return
        
        medication = Prompt.ask("Enter medication to add")
        if medication:
            patient = self.simulation.get_patient(self.current_patient_id)
            patient.add_medication(medication)
            console.print(f"[green]✓[/green] Added medication: {medication}")
        else:
            console.print("[yellow]No medication entered[/yellow]")
        
        console.print()
    
    def show_simulation_status(self) -> None:
        """display current simulation status"""
        state = self.simulation.get_simulation_state()
        
        table = Table(title="Simulation Status")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Status", "Running" if state['is_running'] else "Paused")
        table.add_row("Current Time", f"{state['current_time']:.1f} minutes")
        table.add_row("Patients", str(state['patient_count']))
        table.add_row("Pending Events", str(state['pending_events']))
        
        console.print(table)
        console.print()
    
    def step_simulation(self) -> None:
        """advance simulation by one time step"""
        if not self.is_running:
            console.print("[red]Simulation is not running.[/red]")
            return
        
        self.simulation.step_simulation(1.0)
        console.print("[green]✓[/green] Simulation advanced by 1 minute")
        console.print()
    
    def pause_simulation(self) -> None:
        """pause the simulation"""
        self.simulation.pause_simulation()
        self.is_running = False
        console.print("[yellow]Simulation paused[/yellow]")
        console.print()
    
    def reset_simulation(self) -> None:
        """reset the simulation"""
        if Confirm.ask("Are you sure you want to reset the simulation?"):
            self.simulation.reset_simulation()
            self.current_patient_id = None
            self.is_running = False
            console.print("[green]✓[/green] Simulation reset")
        console.print()
    
    def manage_scenarios(self) -> None:
        """manage scenarios"""
        console.print("[bold]Scenario Management[/bold]")
        
        action = Prompt.ask("Choose action", choices=["list", "start", "progress"])
        
        if action == "list":
            scenarios = self.scenarios.get_available_scenarios()
            table = Table(title="Available Scenarios")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="white")
            table.add_column("Difficulty", style="yellow")
            table.add_column("Time Limit", style="green")
            
            for scenario in scenarios:
                table.add_row(
                    scenario['id'],
                    scenario['title'],
                    scenario['difficulty'],
                    f"{scenario['time_limit']} min"
                )
            console.print(table)
        
        elif action == "start":
            scenario_id = Prompt.ask("Enter scenario ID")
            scenario_data = self.scenarios.start_scenario(scenario_id)
            if scenario_data:
                self.current_scenario_id = scenario_id
                console.print(f"[green]✓[/green] Started scenario: {scenario_data['title']}")
                console.print(f"Learning objectives: {', '.join(scenario_data['learning_objectives'])}")
                
                # start assessment
                self.assessment.start_assessment(
                    scenario_id,
                    self.scenarios.get_scenario(scenario_id).correct_diagnosis,
                    self.scenarios.get_scenario(scenario_id).optimal_actions,
                    self.scenarios.get_scenario(scenario_id).time_limit,
                    self.scenarios.get_scenario(scenario_id).points_possible
                )
            else:
                console.print("[red]Scenario not found[/red]")
        
        elif action == "progress":
            progress = self.scenarios.get_scenario_progress()
            if progress:
                table = Table(title="Scenario Progress")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="white")
                
                table.add_row("Scenario", progress['title'])
                table.add_row("Elapsed Time", f"{progress['elapsed_time']:.1f} min")
                table.add_row("Remaining Time", f"{progress['remaining_time']:.1f} min")
                
                console.print(table)
            else:
                console.print("[yellow]No active scenario[/yellow]")
        
        console.print()
    
    def manage_imaging(self) -> None:
        """manage imaging studies"""
        if not self.current_patient_id:
            console.print("[red]No patient selected.[/red]")
            return
        
        console.print("[bold]Imaging Studies[/bold]")
        
        action = Prompt.ask("Choose action", choices=["list", "order", "results"])
        
        if action == "list":
            studies = self.diagnostics.get_available_imaging_studies()
            table = Table(title="Available Imaging Studies")
            table.add_column("Study", style="cyan")
            table.add_column("Modality", style="white")
            table.add_column("Cost", style="green")
            table.add_column("Time", style="yellow")
            
            for study in studies:
                study_info = self.diagnostics.imaging_studies[study]
                table.add_row(
                    study_info.name,
                    study_info.modality,
                    f"${study_info.cost}",
                    f"{study_info.turnaround_time} min"
                )
            console.print(table)
        
        elif action == "order":
            study_name = Prompt.ask("Enter study name")
            if self.diagnostics.order_imaging_study(study_name, self.current_patient_id, self.simulation.current_time):
                console.print(f"[green]✓[/green] Ordered {study_name}")
                self.assessment.record_action(f"ordered {study_name}")
            else:
                console.print("[red]Invalid study name[/red]")
        
        elif action == "results":
            completed = self.diagnostics.get_completed_results(self.current_patient_id)
            if completed:
                for result in completed:
                    console.print(f"[bold]{result['study_name']}[/bold]")
                    console.print(f"Findings: {result['result']['findings']}")
                    console.print(f"Interpretation: {result['result']['interpretation']}")
                    console.print()
            else:
                console.print("[yellow]No completed imaging results[/yellow]")
        
        console.print()
    
    def interact_with_patient(self) -> None:
        """interact with patient through dialogue"""
        if not self.current_patient_id:
            console.print("[red]No patient selected.[/red]")
            return
        
        console.print("[bold]Patient Dialogue[/bold]")
        console.print("Available question types:")
        
        question_types = [
            "greeting", "how_are_you", "chief_complaint", "pain_location",
            "pain_quality", "pain_severity", "pain_duration", "associated_symptoms",
            "medical_history", "medications", "allergies", "social_history",
            "family_history", "recent_activity"
        ]
        
        for i, q_type in enumerate(question_types, 1):
            console.print(f"{i}. {q_type.replace('_', ' ').title()}")
        
        question_type = Prompt.ask("Enter question type or number")
        
        # convert number to question type if needed
        try:
            num = int(question_type)
            if 1 <= num <= len(question_types):
                question_type = question_types[num - 1]
        except ValueError:
            pass
        
        # get patient context
        patient = self.simulation.get_patient(self.current_patient_id)
        context = {
            'symptoms': patient.symptoms,
            'patient_mood': self.dialogue.patient_mood
        }
        
        response = self.dialogue.get_response(question_type, context)
        console.print(f"[bold]Patient:[/bold] {response}")
        
        self.assessment.record_action(f"asked patient about {question_type}")
        console.print()
    
    def perform_examination(self) -> None:
        """perform physical examination"""
        if not self.current_patient_id:
            console.print("[red]No patient selected.[/red]")
            return
        
        console.print("[bold]Physical Examination[/bold]")
        
        exam_types = [
            "general appearance",
            "vital signs",
            "cardiovascular",
            "respiratory", 
            "abdominal",
            "neurological",
            "extremities"
        ]
        
        for i, exam_type in enumerate(exam_types, 1):
            console.print(f"{i}. {exam_type.title()}")
        
        exam_type = Prompt.ask("Choose examination type or number")
        
        try:
            num = int(exam_type)
            if 1 <= num <= len(exam_types):
                exam_type = exam_types[num - 1]
        except ValueError:
            pass
        
        # generate examination findings based on patient state
        patient = self.simulation.get_patient(self.current_patient_id)
        findings = self._generate_examination_findings(exam_type, patient)
        
        console.print(f"[bold]{exam_type.title()} Examination:[/bold]")
        console.print(findings)
        
        self.assessment.record_action(f"performed {exam_type} examination")
        console.print()
    
    def _generate_examination_findings(self, exam_type: str, patient: PatientState) -> str:
        """generate examination findings based on patient state"""
        if exam_type == "general appearance":
            if any('chest' in s for s in patient.symptoms):
                return "Patient appears anxious and uncomfortable. Diaphoretic and clutching chest."
            elif any('breath' in s for s in patient.symptoms):
                return "Patient appears dyspneic with increased work of breathing."
            else:
                return "Patient appears alert and oriented. No acute distress."
        
        elif exam_type == "vital signs":
            vitals = patient.vital_signs
            return f"Heart rate: {vitals.get('heart_rate', 'N/A')} bpm\nBlood pressure: {vitals.get('bp_systolic', 'N/A')}/{vitals.get('bp_diastolic', 'N/A')} mmHg\nRespiratory rate: {vitals.get('respiratory_rate', 'N/A')} breaths/min\nOxygen saturation: {vitals.get('oxygen_saturation', 'N/A')}%"
        
        elif exam_type == "cardiovascular":
            if any('chest' in s for s in patient.symptoms):
                return "Regular rate and rhythm. No murmurs, gallops, or rubs. Peripheral pulses 2+ bilaterally."
            else:
                return "Regular rate and rhythm. No murmurs or gallops. Peripheral pulses 2+ bilaterally."
        
        elif exam_type == "respiratory":
            if any('breath' in s for s in patient.symptoms):
                return "Decreased breath sounds bilaterally. Diffuse wheezes noted. No crackles or rhonchi."
            else:
                return "Clear to auscultation bilaterally. No wheezes, crackles, or rhonchi."
        
        elif exam_type == "abdominal":
            if any('abdominal' in s or 'pain' in s for s in patient.symptoms):
                return "Tender in right lower quadrant. No rebound or guarding. Bowel sounds present."
            else:
                return "Soft, non-tender, non-distended. Bowel sounds present in all quadrants."
        
        else:
            return "Examination within normal limits."
    
    def make_diagnosis(self) -> None:
        """make a diagnosis"""
        if not self.current_patient_id:
            console.print("[red]No patient selected.[/red]")
            return
        
        console.print("[bold]Make Diagnosis[/bold]")
        diagnosis = Prompt.ask("Enter your diagnosis")
        
        if diagnosis:
            self.assessment.record_diagnosis(diagnosis)
            console.print(f"[green]✓[/green] Diagnosis recorded: {diagnosis}")
        else:
            console.print("[yellow]No diagnosis entered[/yellow]")
        
        console.print()
    
    def save_session(self) -> None:
        """save current session"""
        session_name = Prompt.ask("Enter session name")
        
        if self.session_manager.save_session(self.simulation, session_name):
            console.print(f"[green]✓[/green] Session saved: {session_name}")
        else:
            console.print("[red]Failed to save session[/red]")
        
        console.print()
    
    def load_session(self) -> None:
        """load a saved session"""
        sessions = self.session_manager.list_sessions()
        
        if not sessions:
            console.print("[yellow]No saved sessions found[/yellow]")
            return
        
        table = Table(title="Saved Sessions")
        table.add_column("Name", style="cyan")
        table.add_column("Saved At", style="white")
        table.add_column("Patients", style="green")
        
        for session in sessions:
            table.add_row(
                session['name'],
                session['saved_at'][:19],
                str(session['patient_count'])
            )
        
        console.print(table)
        
        session_name = Prompt.ask("Enter session name to load")
        loaded_simulation = self.session_manager.load_session(session_name)
        
        if loaded_simulation:
            self.simulation = loaded_simulation
            console.print(f"[green]✓[/green] Session loaded: {session_name}")
        else:
            console.print("[red]Failed to load session[/red]")
        
        console.print()
    
    def show_assessment(self) -> None:
        """show performance assessment"""
        if not self.current_scenario_id:
            console.print("[yellow]No active scenario for assessment[/yellow]")
            return
        
        progress = self.scenarios.get_scenario_progress()
        if progress and progress['remaining_time'] <= 0:
            # complete assessment
            summary = self.assessment.complete_assessment(progress['elapsed_time'])
            
            if summary:
                console.print("[bold]Performance Assessment[/bold]")
                
                table = Table(title="Assessment Summary")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="white")
                
                table.add_row("Performance Level", summary['performance_level'].upper())
                table.add_row("Overall Score", f"{summary['overall_score']:.1f}%")
                table.add_row("Points Earned", f"{summary['points_earned']}/{summary['points_possible']}")
                table.add_row("Time Taken", f"{summary['time_taken']:.1f} min")
                table.add_row("Time Limit", f"{summary['time_limit']:.1f} min")
                table.add_row("Diagnostic Correct", "Yes" if summary['diagnostic_correct'] else "No")
                
                console.print(table)
                
                console.print(f"[bold]Correct Diagnosis:[/bold] {summary['correct_diagnosis']}")
                if summary['user_diagnosis']:
                    console.print(f"[bold]Your Diagnosis:[/bold] {summary['user_diagnosis']}")
                
                console.print(f"[bold]Optimal Actions Completed:[/bold] {len(summary['optimal_actions_completed'])}/{len(summary['all_optimal_actions'])}")
                
                if summary['recommendations']:
                    console.print("[bold]Recommendations:[/bold]")
                    for rec in summary['recommendations']:
                        console.print(f"• {rec}")
            else:
                console.print("[red]Assessment not available[/red]")
        else:
            console.print("[yellow]Scenario still in progress[/yellow]")
        
        console.print()
    
    def manage_procedures(self) -> None:
        """manage clinical procedures"""
        if not self.current_patient_id:
            console.print("[red]No patient selected. Start a simulation first.[/red]")
            return
        
        while True:
            console.print("\n[bold]Clinical Procedures[/bold]")
            console.print("1. List available procedures")
            console.print("2. Perform procedure")
            console.print("3. View procedure history")
            console.print("4. Back to main menu")
            
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4"])
            
            if choice == "1":
                self.list_procedures()
            elif choice == "2":
                self.perform_procedure()
            elif choice == "3":
                self.show_procedure_history()
            elif choice == "4":
                break
    
    def list_procedures(self) -> None:
        """list available procedures"""
        procedures = self.treatments.procedures.procedures
        table = Table(title="Available Procedures")
        table.add_column("Procedure", style="cyan")
        table.add_column("Category", style="white")
        table.add_column("Time (min)", style="green")
        table.add_column("Success Rate", style="yellow")
        
        categories = {
            "Airway": ["cricothyrotomy", "bag_valve_mask"],
            "Vascular": ["arterial_line", "intraosseous_access"],
            "Resuscitation": ["defibrillation", "cardioversion", "external_pacing"],
            "Trauma": ["fast_exam", "pelvic_binder"],
            "Neuro": ["lumbar_puncture"],
            "GI": ["ng_tube", "paracentesis"],
            "OB/GYN": ["vaginal_delivery"],
            "Pediatrics": ["broselow_tape"]
        }
        
        for category, proc_list in categories.items():
            for proc_name in proc_list:
                if proc_name in procedures:
                    proc = procedures[proc_name]
                    table.add_row(
                        proc.name,
                        category,
                        str(proc.time_required),
                        f"{proc.success_rate*100:.1f}%"
                    )
        
        console.print(table)
        console.print()
    
    def perform_procedure(self) -> None:
        """perform a clinical procedure"""
        procedures = self.treatments.procedures.procedures
        
        # Show available procedures
        console.print("\n[bold]Available Procedures:[/bold]")
        for i, (name, proc) in enumerate(procedures.items(), 1):
            console.print(f"{i}. {proc.name}")
        
        try:
            choice = int(Prompt.ask("Select procedure number")) - 1
            proc_names = list(procedures.keys())
            if 0 <= choice < len(proc_names):
                proc_name = proc_names[choice]
                self._execute_procedure(proc_name)
            else:
                console.print("[red]Invalid selection[/red]")
        except ValueError:
            console.print("[red]Invalid input[/red]")
    
    def _execute_procedure(self, proc_name: str) -> None:
        """execute a specific procedure"""
        proc = self.treatments.procedures.procedures[proc_name]
        
        console.print(f"\n[bold]Performing: {proc.name}[/bold]")
        console.print(f"Time required: {proc.time_required} minutes")
        console.print(f"Success rate: {proc.success_rate*100:.1f}%")
        
        # Show steps
        console.print("\n[bold]Steps:[/bold]")
        for i, step in enumerate(proc.steps, 1):
            console.print(f"{i}. {step}")
        
        # Show equipment needed
        console.print(f"\n[bold]Equipment needed:[/bold] {', '.join(proc.required_equipment)}")
        
        # Confirm execution
        if Confirm.ask("Proceed with procedure?"):
            result = self.treatments.procedures.perform_procedure(self.current_patient_id, proc_name)
            
            if result["success"]:
                console.print(f"[green]✓[/green] {proc.name} completed successfully")
                if result["complications"]:
                    console.print(f"[yellow]⚠[/yellow] Complications: {', '.join(result['complications'])}")
            else:
                console.print(f"[red]✗[/red] {proc.name} failed: {result.get('error', 'Unknown error')}")
            
            console.print(f"\n[dim]Documentation:[/dim] {result['documentation']}")
        else:
            console.print("[yellow]Procedure cancelled[/yellow]")
    
    def show_procedure_history(self) -> None:
        """show procedure history for current patient"""
        if not self.current_patient_id:
            console.print("[red]No patient selected[/red]")
            return
        
        history = self.treatments.procedures.procedure_history
        patient_history = [h for h in history if h["patient_id"] == self.current_patient_id]
        
        if not patient_history:
            console.print("[yellow]No procedures performed yet[/yellow]")
            return
        
        table = Table(title="Procedure History")
        table.add_column("Procedure", style="cyan")
        table.add_column("Status", style="white")
        table.add_column("Complications", style="yellow")
        table.add_column("Time", style="dim")
        
        for record in patient_history:
            status = "✓ Success" if record["success"] else "✗ Failed"
            complications = ", ".join(record["complications"]) if record["complications"] else "None"
            time = record["timestamp"][:19]  # Show date/time without microseconds
            
            table.add_row(record["procedure"], status, complications, time)
        
        console.print(table)
        console.print()

    def manage_protocols(self) -> None:
        """manage clinical protocols"""
        if not self.current_patient_id:
            console.print("[red]No patient selected. Start a simulation first.[/red]")
            return
        
        while True:
            console.print("\n[bold]Clinical Protocols[/bold]")
            console.print("1. List available protocols")
            console.print("2. Execute protocol")
            console.print("3. View protocol history")
            console.print("4. Back to main menu")
            
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4"])
            
            if choice == "1":
                self.list_protocols()
            elif choice == "2":
                self.execute_protocol()
            elif choice == "3":
                self.show_protocol_history()
            elif choice == "4":
                break
    
    def list_protocols(self) -> None:
        """list available protocols"""
        protocols = self.treatments.procedures.protocols
        table = Table(title="Available Protocols")
        table.add_column("Protocol", style="cyan")
        table.add_column("Indications", style="white")
        table.add_column("Steps", style="green")
        
        for name, protocol in protocols.items():
            indications = ", ".join(protocol.indications)
            steps = f"{len(protocol.steps)} steps"
            table.add_row(protocol.name, indications, steps)
        
        console.print(table)
        console.print()
    
    def execute_protocol(self) -> None:
        """execute a clinical protocol"""
        protocols = self.treatments.procedures.protocols
        
        # Show available protocols
        console.print("\n[bold]Available Protocols:[/bold]")
        for i, (name, protocol) in enumerate(protocols.items(), 1):
            console.print(f"{i}. {protocol.name}")
        
        try:
            choice = int(Prompt.ask("Select protocol number")) - 1
            protocol_names = list(protocols.keys())
            if 0 <= choice < len(protocol_names):
                protocol_name = protocol_names[choice]
                self._execute_protocol(protocol_name)
            else:
                console.print("[red]Invalid selection[/red]")
        except ValueError:
            console.print("[red]Invalid input[/red]")
    
    def _execute_protocol(self, protocol_name: str) -> None:
        """execute a specific protocol"""
        protocol = self.treatments.procedures.protocols[protocol_name]
        
        console.print(f"\n[bold]Executing: {protocol.name}[/bold]")
        
        # Show steps
        console.print("\n[bold]Protocol Steps:[/bold]")
        for i, step in enumerate(protocol.steps, 1):
            console.print(f"{i}. {step}")
        
        # Show bundled orders
        console.print(f"\n[bold]Bundled Orders:[/bold] {', '.join(protocol.bundled_orders)}")
        
        # Confirm execution
        if Confirm.ask("Execute protocol?"):
            # Simulate protocol execution
            console.print(f"[green]✓[/green] {protocol.name} protocol initiated")
            console.print(f"[dim]Documentation:[/dim] {protocol.documentation}")
            
            # Add to protocol history
            record = {
                "patient_id": self.current_patient_id,
                "protocol": protocol_name,
                "timestamp": datetime.now().isoformat(),
                "documentation": protocol.documentation
            }
            self.treatments.procedures.protocol_history.append(record)
        else:
            console.print("[yellow]Protocol cancelled[/yellow]")
    
    def show_protocol_history(self) -> None:
        """show protocol history for current patient"""
        if not self.current_patient_id:
            console.print("[red]No patient selected[/red]")
            return
        
        history = self.treatments.procedures.protocol_history
        patient_history = [h for h in history if h["patient_id"] == self.current_patient_id]
        
        if not patient_history:
            console.print("[yellow]No protocols executed yet[/yellow]")
            return
        
        table = Table(title="Protocol History")
        table.add_column("Protocol", style="cyan")
        table.add_column("Time", style="dim")
        table.add_column("Documentation", style="white")
        
        for record in patient_history:
            time = record["timestamp"][:19]
            table.add_row(record["protocol"], time, record["documentation"])
        
        console.print(table)
        console.print()

    def manage_vitals(self) -> None:
        """manage patient vital signs"""
        if not self.current_patient_id:
            console.print("[red]No patient selected. Start a simulation first.[/red]")
            return
        
        while True:
            console.print("\n[bold]Vital Signs Management[/bold]")
            console.print("1. View vital signs")
            console.print("2. Update vital signs")
            console.print("3. Back to main menu")
            
            choice = Prompt.ask("Select option", choices=["1", "2", "3"])
            
            if choice == "1":
                self.show_vital_signs()
            elif choice == "2":
                self.update_vital_signs()
            elif choice == "3":
                break

    def manage_symptoms(self) -> None:
        """manage patient symptoms"""
        if not self.current_patient_id:
            console.print("[red]No patient selected. Start a simulation first.[/red]")
            return
        
        while True:
            console.print("\n[bold]Symptoms Management[/bold]")
            console.print("1. View symptoms")
            console.print("2. Add symptom")
            console.print("3. Back to main menu")
            
            choice = Prompt.ask("Select option", choices=["1", "2", "3"])
            
            if choice == "1":
                self.show_symptoms()
            elif choice == "2":
                self.add_symptom()
            elif choice == "3":
                break

    def manage_medications(self) -> None:
        """manage patient medications"""
        if not self.current_patient_id:
            console.print("[red]No patient selected. Start a simulation first.[/red]")
            return
        
        while True:
            console.print("\n[bold]Medications Management[/bold]")
            console.print("1. View medications")
            console.print("2. Add medication")
            console.print("3. Back to main menu")
            
            choice = Prompt.ask("Select option", choices=["1", "2", "3"])
            
            if choice == "1":
                self.show_medications()
            elif choice == "2":
                self.add_medication()
            elif choice == "3":
                break

    def manage_labs(self) -> None:
        """manage laboratory tests"""
        if not self.current_patient_id:
            console.print("[red]No patient selected. Start a simulation first.[/red]")
            return
        
        while True:
            console.print("\n[bold]Laboratory Tests[/bold]")
            console.print("1. Order lab test")
            console.print("2. View lab results")
            console.print("3. View pending tests")
            console.print("4. Back to main menu")
            
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4"])
            
            if choice == "1":
                self.order_lab_test()
            elif choice == "2":
                self.view_lab_results()
            elif choice == "3":
                self.view_pending_tests()
            elif choice == "4":
                break

    def order_lab_test(self) -> None:
        """order a laboratory test"""
        available_tests = self.diagnostics.get_available_lab_tests()
        
        console.print("\n[bold]Available Lab Tests:[/bold]")
        for i, test_name in enumerate(available_tests.keys(), 1):
            console.print(f"{i}. {test_name}")
        
        try:
            choice = int(Prompt.ask("Select test number")) - 1
            test_names = list(available_tests.keys())
            if 0 <= choice < len(test_names):
                test_name = test_names[choice]
                test_id = self.diagnostics.order_lab_test(test_name, {})
                console.print(f"[green]✓[/green] Lab test ordered: {test_name}")
                console.print(f"Test ID: {test_id}")
            else:
                console.print("[red]Invalid selection[/red]")
        except ValueError:
            console.print("[red]Invalid input[/red]")

    def view_lab_results(self) -> None:
        """view laboratory test results"""
        results = self.diagnostics.get_test_results()
        
        if not results:
            console.print("[yellow]No lab results available[/yellow]")
            return
        
        table = Table(title="Laboratory Results")
        table.add_column("Test", style="cyan")
        table.add_column("Result", style="white")
        table.add_column("Unit", style="dim")
        table.add_column("Status", style="yellow")
        
        for test_id, result in results.items():
            status = "Critical" if result.get("critical", False) else "Normal"
            table.add_row(
                result.get("test_name", "Unknown"),
                str(result.get("value", "N/A")),
                result.get("unit", ""),
                status
            )
        
        console.print(table)
        console.print()

    def view_pending_tests(self) -> None:
        """view pending laboratory tests"""
        pending = self.diagnostics.get_pending_tests()
        
        if not pending:
            console.print("[yellow]No pending tests[/yellow]")
            return
        
        table = Table(title="Pending Tests")
        table.add_column("Test ID", style="cyan")
        table.add_column("Test Name", style="white")
        table.add_column("Order Time", style="dim")
        table.add_column("Status", style="yellow")
        
        for test_id, test_info in pending.items():
            table.add_row(
                test_id,
                test_info.get("test_name", "Unknown"),
                test_info.get("order_time", "N/A"),
                "Pending"
            )
        
        console.print(table)
        console.print()

    def run(self):
        """run the cli interface"""
        console.print(Panel.fit(
            "Medical Simulator CLI\nProfessional-grade medical simulation platform",
            title="Welcome",
            border_style="blue"
        ))
        
        while True:
            try:
                command = Prompt.ask("medsim>").strip().lower()
                if not command:
                    continue
                self._add_to_history(command)
                
                # plugin management commands
                if command == "plugins":
                    self.list_plugins()
                    continue
                if command.startswith("plugin "):
                    self.handle_plugin_command(command)
                    continue
                # ... rest of command handling ...
                if command == "help":
                    self.display_help()
                elif command == "start":
                    self.start_simulation()
                elif command == "scenario":
                    self.manage_scenarios()
                elif command == "patient":
                    self.show_patient_info()
                elif command == "vitals":
                    self.manage_vitals()
                elif command == "symptoms":
                    self.manage_symptoms()
                elif command == "medications":
                    self.manage_medications()
                elif command == "procedures":
                    self.manage_procedures()
                elif command == "protocols":
                    self.manage_protocols()
                elif command == "labs":
                    self.manage_labs()
                elif command == "imaging":
                    self.manage_imaging()
                elif command == "dialogue":
                    self.interact_with_patient()
                elif command == "examination":
                    self.perform_examination()
                elif command == "diagnosis":
                    self.make_diagnosis()
                elif command == "save":
                    self.save_session()
                elif command == "load":
                    self.load_session()
                elif command == "status":
                    self.show_simulation_status()
                elif command == "step":
                    self.step_simulation()
                elif command == "pause":
                    self.pause_simulation()
                elif command == "reset":
                    self.reset_simulation()
                elif command == "assessment":
                    self.show_assessment()
                elif command == "alerts":
                    self.alerts()
                elif command == "interpret":
                    self.interpret()
                elif command == "pending":
                    self.pending()
                elif command == "available":
                    self.available()
                elif command == "api":
                    self.show_api_info()
                elif command == "json":
                    self.toggle_json_output()
                elif command == "quit":
                    self._save_command_history()
                    console.print("Goodbye!")
                    break
                else:
                    console.print(f"[red]Unknown command: {command}[/red]")
                    console.print("Type 'help' for available commands")
            
            except KeyboardInterrupt:
                self._save_command_history()
                console.print("\nGoodbye!")
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

    def show_api_info(self):
        """show API information and examples"""
        console.print("\n[bold cyan]Medical Simulator API v1.0[/bold cyan]")
        console.print("Programmatic access to simulator functionality\n")
        
        console.print("[bold yellow]Quick Start:[/bold yellow]")
        console.print("```python")
        console.print("from medsim.api import MedicalSimulatorAPI")
        console.print("")
        console.print("# Initialize API")
        console.print("api = MedicalSimulatorAPI()")
        console.print("")
        console.print("# Start simulation")
        console.print("response = api.start_simulation()")
        console.print("")
        console.print("# Get simulation state")
        console.print("state = api.get_simulation_state()")
        console.print("")
        console.print("# Order lab test")
        console.print("api.order_lab_test('troponin')")
        console.print("```")
        
        console.print("\n[bold yellow]Available Methods:[/bold yellow]")
        methods = [
            ("start_simulation()", "Start new simulation session"),
            ("get_simulation_state()", "Get current simulation state"),
            ("update_vitals(data)", "Update patient vital signs"),
            ("order_lab_test(name)", "Order lab test"),
            ("order_imaging_study(name)", "Order imaging study"),
            ("administer_medication(data)", "Administer medication"),
            ("perform_procedure(data)", "Perform clinical procedure"),
            ("start_dialogue(message)", "Start patient dialogue"),
            ("perform_examination(data)", "Perform physical examination"),
            ("step_simulation(steps)", "Advance simulation"),
            ("get_assessment()", "Get performance assessment"),
            ("get_plugins()", "Get plugin information"),
            ("save_session(filename)", "Save session to file"),
            ("load_session(filename)", "Load session from file"),
            ("stop_simulation()", "Stop current simulation")
        ]
        
        for method, description in methods:
            console.print(f"  {method:<25} - {description}")
        
        console.print("\n[bold yellow]Response Format:[/bold yellow]")
        console.print("All API methods return structured responses with:")
        console.print("  • success: boolean indicating success/failure")
        console.print("  • data: response data (if successful)")
        console.print("  • error: error message (if failed)")
        console.print("  • message: human-readable message")
        console.print("  • timestamp: response timestamp")
    
    def toggle_json_output(self):
        """toggle JSON output mode"""
        if not hasattr(self, 'json_output'):
            self.json_output = False
        
        self.json_output = not self.json_output
        mode = "enabled" if self.json_output else "disabled"
        console.print(f"[green]JSON output mode {mode}[/green]")
    
    def _output_json(self, data: Any, title: str = ""):
        """output data in JSON format"""
        if hasattr(self, 'json_output') and self.json_output:
            json_str = self._get_json_output(data)
            if title:
                console.print(f"\n[bold cyan]{title}:[/bold cyan]")
            console.print(json_str)
            return True
        return False

    def list_plugins(self):
        """list all loaded plugins"""
        response = self.api.list_plugins()
        if response.success:
            table = Table(title="Loaded Plugins", show_header=True, header_style="bold magenta")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="white")
            table.add_column("Version", style="yellow")
            table.add_column("Category", style="green")
            table.add_column("Enabled", style="red")
            for plugin in response.data:
                table.add_row(
                    f"{plugin['category']}.{plugin['name']}",
                    plugin['name'],
                    plugin['version'],
                    plugin['category'],
                    "Yes" if plugin['enabled'] else "No"
                )
            console.print(table)
        else:
            console.print(f"[red]Error: {response.error}[/red]")
    
    def handle_plugin_command(self, command: str):
        """handle plugin subcommands"""
        parts = command.split()
        if len(parts) < 3:
            console.print("[yellow]Usage: plugin <load|unload|enable|disable|info|content> <args>[/yellow]")
            return
        subcmd = parts[1]
        if subcmd == "load" and len(parts) == 3:
            path = parts[2]
            response = self.api.load_plugin(path)
            if response.success:
                console.print(f"[green]{response.message}[/green]")
            else:
                console.print(f"[red]Error: {response.error}[/red]")
        elif subcmd == "unload" and len(parts) == 3:
            plugin_id = parts[2]
            response = self.api.unload_plugin(plugin_id)
            if response.success:
                console.print(f"[green]{response.message}[/green]")
            else:
                console.print(f"[red]Error: {response.error}[/red]")
        elif subcmd == "enable" and len(parts) == 3:
            plugin_id = parts[2]
            response = self.api.enable_plugin(plugin_id)
            if response.success:
                console.print(f"[green]{response.message}[/green]")
            else:
                console.print(f"[red]Error: {response.error}[/red]")
        elif subcmd == "disable" and len(parts) == 3:
            plugin_id = parts[2]
            response = self.api.disable_plugin(plugin_id)
            if response.success:
                console.print(f"[green]{response.message}[/green]")
            else:
                console.print(f"[red]Error: {response.error}[/red]")
        elif subcmd == "info" and len(parts) == 3:
            plugin_id = parts[2]
            response = self.api.get_plugin_info(plugin_id)
            if response.success:
                plugin = response.data
                console.print(f"[bold cyan]Plugin Info:[/bold cyan] {plugin['name']} v{plugin['version']} ({plugin['category']})")
                for k, v in plugin.items():
                    console.print(f"  [yellow]{k}[/yellow]: {v}")
            else:
                console.print(f"[red]Error: {response.error}[/red]")
        elif subcmd == "content" and len(parts) == 4:
            plugin_id = parts[2]
            content_type = parts[3]
            response = self.api.get_plugin_content(plugin_id, content_type)
            if response.success:
                console.print(f"[bold cyan]{content_type.title()} from {plugin_id}:[/bold cyan]")
                for item in response.data:
                    console.print(f"  • {item.get('name', item.get('id', str(item)))}")
            else:
                console.print(f"[red]Error: {response.error}[/red]")
        else:
            console.print("[yellow]Usage: plugin <load|unload|enable|disable|info|content> <args>[/yellow]")

    @app.command()
    def alerts(self):
        """show critical lab and imaging alerts"""
        if not self.simulation or not self.simulation.patient_state:
            console.print("❌ No active simulation")
            return
        
        alerts = self.simulation.diagnostics.get_critical_alerts(self.simulation.patient_state)
        
        if not alerts:
            console.print("✅ No critical alerts")
            return
        
        table = Table(title="🚨 Critical Alerts", show_header=True, header_style="bold red")
        table.add_column("Type", style="cyan")
        table.add_column("Test/Study", style="white")
        table.add_column("Value", style="yellow")
        table.add_column("Severity", style="red")
        table.add_column("Message", style="white")
        
        for alert in alerts:
            value = alert.get("value", "N/A")
            severity = alert.get("severity", "critical")
            message = alert.get("message", "")
            
            table.add_row(
                alert["type"].upper(),
                alert.get("test", alert.get("study", "")),
                str(value),
                severity.upper(),
                message
            )
        
        console.print(table)
    
    @app.command()
    def interpret(self):
        """interpret lab or imaging results"""
        if not self.simulation or not self.simulation.patient_state:
            console.print("❌ No active simulation")
            return
        
        # show available results
        lab_results = list(self.simulation.patient_state.lab_results.keys())
        imaging_results = list(self.simulation.patient_state.imaging_results.keys())
        
        if not lab_results and not imaging_results:
            console.print("❌ No results to interpret")
            return
        
        console.print("Available results to interpret:")
        
        if lab_results:
            console.print("\n[cyan]Lab Tests:[/cyan]")
            for test in lab_results:
                console.print(f"  • {test}")
        
        if imaging_results:
            console.print("\n[cyan]Imaging Studies:[/cyan]")
            for study in imaging_results:
                console.print(f"  • {study}")
        
        # get user choice
        result_type = Prompt.ask(
            "\nInterpret [cyan]lab[/cyan] or [cyan]imaging[/cyan] result?",
            choices=["lab", "imaging"],
            default="lab"
        )
        
        if result_type == "lab":
            if not lab_results:
                console.print("❌ No lab results available")
                return
            
            test_name = Prompt.ask(
                "Enter test name",
                choices=lab_results
            )
            
            result = self.simulation.patient_state.lab_results[test_name]
            interpretation = self.simulation.diagnostics.interpret_lab_result(
                test_name, result["value"], self.simulation.patient_state
            )
            
            self._display_lab_interpretation(interpretation)
        
        else:  # imaging
            if not imaging_results:
                console.print("❌ No imaging results available")
                return
            
            study_name = Prompt.ask(
                "Enter study name",
                choices=imaging_results
            )
            
            result = self.simulation.patient_state.imaging_results[study_name]
            interpretation = self.simulation.diagnostics.interpret_imaging_result(
                study_name, result["findings"], self.simulation.patient_state
            )
            
            self._display_imaging_interpretation(interpretation)
    
    def _display_lab_interpretation(self, interpretation: Dict[str, Any]):
        """display lab result interpretation"""
        console.print(f"\n[bold cyan]Lab Result Interpretation[/bold cyan]")
        console.print(f"Test: {interpretation['test_name']}")
        console.print(f"Value: {interpretation['value']} {interpretation['unit']}")
        console.print(f"Normal Range: {interpretation['normal_range'][0]} - {interpretation['normal_range'][1]} {interpretation['unit']}")
        
        # status with color
        status = interpretation['status']
        if status == "normal":
            status_color = "green"
        elif status in ["critical_low", "critical_high"]:
            status_color = "red"
        else:
            status_color = "yellow"
        
        console.print(f"Status: [{status_color}]{status.upper()}[/{status_color}]")
        console.print(f"Clinical Significance: {interpretation['clinical_significance']}")
        
        if interpretation['critical_alert']:
            console.print("\n[bold red]🚨 CRITICAL ALERT 🚨[/bold red]")
        
        if interpretation['recommendations']:
            console.print("\n[bold yellow]Recommendations:[/bold yellow]")
            for rec in interpretation['recommendations']:
                console.print(f"  • {rec}")
        
        if interpretation['follow_up']:
            console.print("\n[bold blue]Follow-up:[/bold blue]")
            for follow in interpretation['follow_up']:
                console.print(f"  • {follow}")
    
    def _display_imaging_interpretation(self, interpretation: Dict[str, Any]):
        """display imaging result interpretation"""
        console.print(f"\n[bold cyan]Imaging Result Interpretation[/bold cyan]")
        console.print(f"Study: {interpretation['study_name']}")
        console.print(f"Modality: {interpretation['modality']}")
        
        if interpretation['critical_findings']:
            console.print("\n[bold red]🚨 CRITICAL FINDINGS 🚨[/bold red]")
        
        console.print(f"\n[bold yellow]Clinical Impression:[/bold yellow]")
        console.print(f"  {interpretation['clinical_impression']}")
        
        if interpretation['recommendations']:
            console.print("\n[bold yellow]Recommendations:[/bold yellow]")
            for rec in interpretation['recommendations']:
                console.print(f"  • {rec}")
        
        if interpretation['follow_up']:
            console.print("\n[bold blue]Follow-up:[/bold blue]")
            for follow in interpretation['follow_up']:
                console.print(f"  • {follow}")
    
    @app.command()
    def pending(self):
        """show pending lab and imaging orders"""
        if not self.simulation or not self.simulation.patient_state:
            console.print("❌ No active simulation")
            return
        
        pending_labs = []
        pending_imaging = []
        
        # check for pending lab results
        for test_name, order_time in self.simulation.diagnostics.test_history.items():
            test = self.simulation.diagnostics.lab_tests.get(test_name)
            if test:
                time_elapsed = self.simulation.current_time - order_time
                if time_elapsed < test.turnaround_time:
                    remaining = test.turnaround_time - time_elapsed
                    pending_labs.append({
                        "test": test.name,
                        "remaining": remaining,
                        "category": test.category
                    })
        
        # check for pending imaging results
        for study_name, order_time in self.simulation.diagnostics.imaging_history.items():
            study = self.simulation.diagnostics.imaging_studies.get(study_name)
            if study:
                time_elapsed = self.simulation.current_time - order_time
                if time_elapsed < study.turnaround_time:
                    remaining = study.turnaround_time - time_elapsed
                    pending_imaging.append({
                        "study": study.name,
                        "remaining": remaining,
                        "modality": study.modality
                    })
        
        if not pending_labs and not pending_imaging:
            console.print("✅ No pending results")
            return
        
        if pending_labs:
            console.print("\n[bold cyan]Pending Lab Results:[/bold cyan]")
            table = Table(show_header=True, header_style="bold")
            table.add_column("Test", style="cyan")
            table.add_column("Category", style="white")
            table.add_column("Time Remaining", style="yellow")
            
            for lab in pending_labs:
                table.add_row(
                    lab["test"],
                    lab["category"],
                    f"{lab['remaining']} minutes"
                )
            
            console.print(table)
        
        if pending_imaging:
            console.print("\n[bold cyan]Pending Imaging Results:[/bold cyan]")
            table = Table(show_header=True, header_style="bold")
            table.add_column("Study", style="cyan")
            table.add_column("Modality", style="white")
            table.add_column("Time Remaining", style="yellow")
            
            for study in pending_imaging:
                table.add_row(
                    study["study"],
                    study["modality"],
                    f"{study['remaining']} minutes"
                )
            
            console.print(table)
    
    @app.command()
    def available(self):
        """show available lab tests and imaging studies"""
        if not self.simulation:
            console.print("❌ No active simulation")
            return
        
        # show lab tests by category
        console.print("\n[bold cyan]Available Lab Tests:[/bold cyan]")
        
        categories = {}
        for test_name, test in self.simulation.diagnostics.lab_tests.items():
            if test.category not in categories:
                categories[test.category] = []
            categories[test.category].append(test)
        
        for category, tests in categories.items():
            console.print(f"\n[bold yellow]{category}:[/bold yellow]")
            for test in tests:
                cost = f"${test.cost:.0f}" if test.cost else "N/A"
                time = f"{test.turnaround_time} min" if test.turnaround_time else "N/A"
                console.print(f"  • {test.name} ({cost}, {time})")
        
        # show imaging studies by modality
        console.print("\n[bold cyan]Available Imaging Studies:[/bold cyan]")
        
        modalities = {}
        for study_name, study in self.simulation.diagnostics.imaging_studies.items():
            if study.modality not in modalities:
                modalities[study.modality] = []
            modalities[study.modality].append(study)
        
        for modality, studies in modalities.items():
            console.print(f"\n[bold yellow]{modality}:[/bold yellow]")
            for study in studies:
                cost = f"${study.cost:.0f}" if study.cost else "N/A"
                time = f"{study.turnaround_time} min" if study.turnaround_time else "N/A"
                console.print(f"  • {study.name} ({cost}, {time})")


@app.command()
def main():
    """medical simulator cli"""
    cli = SimulatorCLI()
    cli.run()


if __name__ == "__main__":
    app() 