"""
command-line interface for medical simulator
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from typing import Optional, List
import sys
import os

from ..core.simulation import MedicalSimulation, PatientState
from ..core.session import SessionManager
from ..core.physiology import PhysiologicalEngine
from ..core.dialogue import AdvancedDialogueSystem
from ..core.diagnostics import AdvancedDiagnosticSystem
from ..core.treatments import AdvancedTreatmentSystem
from ..scenarios.scenario_manager import ScenarioManager
from ..assessment.performance import AssessmentSystem

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
    
    def display_help(self) -> None:
        """display available commands"""
        table = Table(title="Available Commands")
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        
        commands = [
            ("help", "show this help message"),
            ("start", "start a new simulation"),
            ("scenario", "manage scenarios"),
            ("patient", "manage patients"),
            ("vitals", "view/update patient vital signs"),
            ("symptoms", "manage patient symptoms"),
            ("medications", "manage patient medications"),
            ("labs", "order and view lab results"),
            ("imaging", "order and view imaging studies"),
            ("dialogue", "interact with patient"),
            ("examination", "perform physical examination"),
            ("diagnosis", "make a diagnosis"),
            ("save", "save current session"),
            ("load", "load a saved session"),
            ("status", "show simulation status"),
            ("step", "advance simulation by one time step"),
            ("pause", "pause simulation"),
            ("reset", "reset simulation"),
            ("assessment", "view performance assessment"),
            ("quit", "exit simulator")
        ]
        
        for cmd, desc in commands:
            table.add_row(cmd, desc)
        
        console.print(table)
        console.print()
    
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
    
    def run_interactive(self) -> None:
        """run the interactive cli"""
        self.display_welcome()
        
        while True:
            try:
                command = Prompt.ask("medsim", choices=[
                    "help", "start", "scenario", "patient", "vitals", "symptoms", "medications",
                    "labs", "imaging", "dialogue", "examination", "diagnosis", "save", "load", 
                    "status", "step", "pause", "reset", "assessment", "quit"
                ])
                
                if command == "help":
                    self.display_help()
                elif command == "start":
                    self.start_simulation()
                elif command == "patient":
                    self.show_patient_info()
                elif command == "vitals":
                    action = Prompt.ask("View or Update vitals?", choices=["view", "update"])
                    if action == "view":
                        self.show_vital_signs()
                    else:
                        self.update_vital_signs()
                elif command == "symptoms":
                    action = Prompt.ask("View or Add symptoms?", choices=["view", "add"])
                    if action == "view":
                        self.show_symptoms()
                    else:
                        self.add_symptom()
                elif command == "medications":
                    action = Prompt.ask("View or Add medications?", choices=["view", "add"])
                    if action == "view":
                        self.show_medications()
                    else:
                        self.add_medication()
                elif command == "status":
                    self.show_simulation_status()
                elif command == "step":
                    self.step_simulation()
                elif command == "pause":
                    self.pause_simulation()
                elif command == "reset":
                    self.reset_simulation()
                elif command == "scenario":
                    self.manage_scenarios()
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
                elif command == "assessment":
                    self.show_assessment()
                elif command == "quit":
                    console.print("[bold blue]Goodbye![/bold blue]")
                    break
                else:
                    console.print("[red]Unknown command[/red]")
                    
            except KeyboardInterrupt:
                console.print("\n[bold blue]Goodbye![/bold blue]")
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")


@app.command()
def main():
    """medical simulator cli"""
    cli = SimulatorCLI()
    cli.run_interactive()


if __name__ == "__main__":
    app() 