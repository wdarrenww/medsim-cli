"""
enhanced CLI interface with comprehensive medical simulation capabilities
"""

import typer
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import json
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich.columns import Columns
from rich.console import Group

from ..core.physiology import EnhancedPhysiologicalEngine, DiscoveryMethod, OrganSystem, DiseaseState
from ..core.diagnostics import EnhancedDiagnosticSystem, TestCategory, ImagingModality
from ..core.treatments import EnhancedTreatmentEngine, DrugCategory, Route, InteractionSeverity
from ..core.dialogue import EnhancedDialogueEngine, EmotionalState, CommunicationStyle, PainLevel
from ..core.symptoms import SymptomLibrary
from ..core.session import GlobalCLISession

# initialize global session
cli_session = GlobalCLISession()

# initialize engines
physio_engine = EnhancedPhysiologicalEngine()
diagnostic_engine = EnhancedDiagnosticSystem()
treatment_engine = EnhancedTreatmentEngine()
dialogue_engine = EnhancedDialogueEngine()
symptom_library = SymptomLibrary()

console = Console()
app = typer.Typer(help="Enhanced Medical Simulation CLI")


@app.command()
def create_patient(
    patient_id: str = typer.Option(..., "--id", "-i", help="Patient ID"),
    name: str = typer.Option(..., "--name", "-n", help="Patient name"),
    age: int = typer.Option(..., "--age", "-a", help="Patient age"),
    gender: str = typer.Option(..., "--gender", "-g", help="Patient gender"),
    height_cm: float = typer.Option(..., "--height", help="Height in cm"),
    weight_kg: float = typer.Option(..., "--weight", help="Weight in kg")
):
    """create a new patient profile"""
    result = physio_engine.create_patient(patient_id, name, age, gender, height_cm, weight_kg)
    console.print(f"[green]{result}[/green]")
    
    # initialize dialogue context
    dialogue_engine.initialize_patient_context(patient_id)
    
    # store in session
    cli_session.set_current_patient(patient_id)
    
    console.print(f"[blue]Patient {patient_id} created and set as current patient[/blue]")


@app.command()
def discover_info(
    info_type: str = typer.Option(..., "--type", "-t", help="Type of information to discover"),
    method: str = typer.Option("calculation", "--method", "-m", help="Discovery method"),
    value: Optional[str] = typer.Option(None, "--value", "-v", help="Value to discover")
):
    """discover patient information"""
    patient_id = cli_session.get_current_patient()
    if not patient_id:
        console.print("[red]No current patient. Use create-patient first.[/red]")
        return
    
    try:
        discovery_method = DiscoveryMethod(method.lower())
    except ValueError:
        console.print(f"[red]Invalid discovery method: {method}[/red]")
        return
    
    # handle different info types
    if info_type == "bmi":
        result = physio_engine.discover_patient_information(patient_id, "bmi", discovery_method)
    elif info_type == "body_surface_area":
        result = physio_engine.discover_patient_information(patient_id, "body_surface_area", discovery_method)
    elif info_type == "ideal_body_weight":
        result = physio_engine.discover_patient_information(patient_id, "ideal_body_weight", discovery_method)
    elif info_type == "medical_history" and value:
        # parse medical history from value
        history_items = [item.strip() for item in value.split(",")]
        result = physio_engine.discover_patient_information(patient_id, "medical_history", discovery_method, history_items)
    elif info_type == "medications" and value:
        # parse medications from value
        med_items = [item.strip() for item in value.split(",")]
        result = physio_engine.discover_patient_information(patient_id, "medications", discovery_method, med_items)
    elif info_type == "allergies" and value:
        # parse allergies from value
        allergy_items = [item.strip() for item in value.split(",")]
        result = physio_engine.discover_patient_information(patient_id, "allergies", discovery_method, allergy_items)
    else:
        console.print(f"[red]Invalid info type or missing value: {info_type}[/red]")
        return
    
    console.print(f"[green]{result}[/green]")


@app.command()
def update_vitals(
    heart_rate: Optional[int] = typer.Option(None, "--hr", help="Heart rate"),
    systolic_bp: Optional[int] = typer.Option(None, "--sbp", help="Systolic blood pressure"),
    diastolic_bp: Optional[int] = typer.Option(None, "--dbp", help="Diastolic blood pressure"),
    respiratory_rate: Optional[int] = typer.Option(None, "--rr", help="Respiratory rate"),
    temperature: Optional[float] = typer.Option(None, "--temp", help="Temperature"),
    oxygen_saturation: Optional[float] = typer.Option(None, "--o2", help="Oxygen saturation"),
    blood_glucose: Optional[float] = typer.Option(None, "--glucose", help="Blood glucose"),
    creatinine: Optional[float] = typer.Option(None, "--creatinine", help="Creatinine"),
    sodium: Optional[float] = typer.Option(None, "--sodium", help="Sodium"),
    potassium: Optional[float] = typer.Option(None, "--potassium", help="Potassium")
):
    """update patient vital signs"""
    patient_id = cli_session.get_current_patient()
    if not patient_id:
        console.print("[red]No current patient. Use create-patient first.[/red]")
        return
    
    vitals = {}
    if heart_rate is not None:
        vitals['heart_rate'] = heart_rate
    if systolic_bp is not None:
        vitals['systolic_bp'] = systolic_bp
    if diastolic_bp is not None:
        vitals['diastolic_bp'] = diastolic_bp
    if respiratory_rate is not None:
        vitals['respiratory_rate'] = respiratory_rate
    if temperature is not None:
        vitals['temperature'] = temperature
    if oxygen_saturation is not None:
        vitals['oxygen_saturation'] = oxygen_saturation
    if blood_glucose is not None:
        vitals['blood_glucose'] = blood_glucose
    if creatinine is not None:
        vitals['creatinine'] = creatinine
    if sodium is not None:
        vitals['sodium'] = sodium
    if potassium is not None:
        vitals['potassium'] = potassium
    
    if not vitals:
        console.print("[red]No vitals provided to update[/red]")
        return
    
    result = physio_engine.update_patient_vitals(patient_id, vitals)
    console.print(f"[green]{result}[/green]")


@app.command()
def show_vitals():
    """show current patient vital signs"""
    patient_id = cli_session.get_current_patient()
    if not patient_id:
        console.print("[red]No current patient. Use create-patient first.[/red]")
        return
    
    patient = physio_engine.get_patient(patient_id)
    if not patient:
        console.print("[red]Patient not found[/red]")
        return
    
    vitals = patient.get_available_vitals()
    critical_vitals = patient.get_critical_vitals()
    
    # create vitals table
    table = Table(title=f"Vital Signs - Patient {patient_id}")
    table.add_column("Vital", style="cyan")
    table.add_column("Value", style="white")
    table.add_column("Unit", style="blue")
    table.add_column("Normal Range", style="green")
    table.add_column("Alert Level", style="red")
    
    for vital_name, vital_data in vitals.items():
        alert_color = "red" if vital_data['alert_level'] != "normal" else "green"
        table.add_row(
            vital_name.replace("_", " ").title(),
            str(vital_data['value']),
            vital_data['unit'],
            f"{vital_data['normal_range'][0]}-{vital_data['normal_range'][1]}",
            f"[{alert_color}]{vital_data['alert_level']}[/{alert_color}]"
        )
    
    console.print(table)
    
    if critical_vitals:
        console.print("\n[red]⚠️ CRITICAL VITALS:[/red]")
        for vital in critical_vitals:
            console.print(f"[red]• {vital['name']}: {vital['value']} {vital['unit']} ({vital['alert_level']})[/red]")


@app.command()
def add_symptom(symptom: str = typer.Option(..., "--symptom", "-s", help="Symptom to add")):
    """add a symptom to the current patient"""
    patient_id = cli_session.get_current_patient()
    if not patient_id:
        console.print("[red]No current patient. Use create-patient first.[/red]")
        return
    
    result = physio_engine.add_patient_symptom(patient_id, symptom)
    console.print(f"[green]{result}[/green]")


@app.command()
def add_disease(
    disease_name: str = typer.Option(..., "--disease", "-d", help="Disease name"),
    system: str = typer.Option(..., "--system", "-s", help="Organ system"),
    severity: float = typer.Option(0.5, "--severity", help="Disease severity (0.0-1.0)")
):
    """add a disease process to the current patient"""
    patient_id = cli_session.get_current_patient()
    if not patient_id:
        console.print("[red]No current patient. Use create-patient first.[/red]")
        return
    
    try:
        organ_system = OrganSystem(system.lower())
    except ValueError:
        console.print(f"[red]Invalid organ system: {system}[/red]")
        return
    
    result = physio_engine.add_patient_disease(patient_id, disease_name, organ_system, severity)
    console.print(f"[green]{result}[/green]")


@app.command()
def order_lab(
    test_name: str = typer.Option(..., "--test", "-t", help="Lab test to order")
):
    """order a lab test for the current patient"""
    patient_id = cli_session.get_current_patient()
    if not patient_id:
        console.print("[red]No current patient. Use create-patient first.[/red]")
        return
    
    result = diagnostic_engine.order_lab_test(patient_id, test_name)
    console.print(f"[green]{result}[/green]")


@app.command()
def order_imaging(
    study_name: str = typer.Option(..., "--study", "-s", help="Imaging study to order")
):
    """order an imaging study for the current patient"""
    patient_id = cli_session.get_current_patient()
    if not patient_id:
        console.print("[red]No current patient. Use create-patient first.[/red]")
        return
    
    result = diagnostic_engine.order_imaging_study(patient_id, study_name)
    console.print(f"[green]{result}[/green]")


@app.command()
def complete_lab(
    test_name: str = typer.Option(..., "--test", "-t", help="Lab test to complete"),
    value: float = typer.Option(..., "--value", "-v", help="Test result value")
):
    """complete a lab test with result"""
    patient_id = cli_session.get_current_patient()
    if not patient_id:
        console.print("[red]No current patient. Use create-patient first.[/red]")
        return
    
    try:
        result = diagnostic_engine.complete_lab_test(patient_id, test_name, value)
        console.print(f"[green]✓ Lab test completed: {test_name} = {value}[/green]")
        
        if result.requires_action:
            console.print(f"[red]⚠️ ACTION REQUIRED: {result.interpretation}[/red]")
        
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")


@app.command()
def complete_imaging(
    study_name: str = typer.Option(..., "--study", "-s", help="Imaging study to complete"),
    findings: str = typer.Option(..., "--findings", "-f", help="Imaging findings (JSON)")
):
    """complete an imaging study with results"""
    patient_id = cli_session.get_current_patient()
    if not patient_id:
        console.print("[red]No current patient. Use create-patient first.[/red]")
        return
    
    try:
        findings_dict = json.loads(findings)
        result = diagnostic_engine.complete_imaging_study(patient_id, study_name, findings_dict)
        console.print(f"[green]✓ Imaging study completed: {study_name}[/green]")
        console.print(f"[blue]Impression: {result.impression}[/blue]")
        
        if result.recommendations:
            console.print(f"[yellow]Recommendations: {', '.join(result.recommendations)}[/yellow]")
        
    except json.JSONDecodeError:
        console.print("[red]Error: Invalid JSON format for findings[/red]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")


@app.command()
def administer_drug(
    drug_name: str = typer.Option(..., "--drug", "-d", help="Drug to administer"),
    dose: float = typer.Option(..., "--dose", help="Drug dose"),
    route: str = typer.Option(..., "--route", "-r", help="Administration route")
):
    """administer a drug to the current patient"""
    patient_id = cli_session.get_current_patient()
    if not patient_id:
        console.print("[red]No current patient. Use create-patient first.[/red]")
        return
    
    result = treatment_engine.administer_drug(patient_id, drug_name, dose, route)
    console.print(f"[green]{result}[/green]")


@app.command()
def start_protocol(
    protocol_name: str = typer.Option(..., "--protocol", "-p", help="Treatment protocol to start")
):
    """start a treatment protocol for the current patient"""
    patient_id = cli_session.get_current_patient()
    if not patient_id:
        console.print("[red]No current patient. Use create-patient first.[/red]")
        return
    
    result = treatment_engine.start_treatment_protocol(patient_id, protocol_name)
    console.print(f"[green]{result}[/green]")


@app.command()
def talk_to_patient(
    message: str = typer.Option(..., "--message", "-m", help="Message to patient"),
    question_type: str = typer.Option("general", "--type", "-t", help="Question type")
):
    """talk to the current patient"""
    patient_id = cli_session.get_current_patient()
    if not patient_id:
        console.print("[red]No current patient. Use create-patient first.[/red]")
        return
    
    response = dialogue_engine.get_patient_response(patient_id, message, question_type)
    
    # display conversation
    console.print(f"\n[blue]Doctor:[/blue] {message}")
    console.print(f"[green]Patient:[/green] {response.text}")
    
    # show emotional context
    emotion_color = "red" if response.emotion in [EmotionalState.ANXIOUS, EmotionalState.FEARFUL, EmotionalState.PAIN] else "green"
    console.print(f"[{emotion_color}]Patient emotion: {response.emotion.value}[/{emotion_color}]")
    
    if response.requires_followup:
        console.print("[yellow]⚠️ Follow-up recommended[/yellow]")


@app.command()
def show_patient_summary():
    """show comprehensive patient summary"""
    patient_id = cli_session.get_current_patient()
    if not patient_id:
        console.print("[red]No current patient. Use create-patient first.[/red]")
        return
    
    summary = physio_engine.get_patient_summary(patient_id)
    
    # create summary panel
    panel = Panel(
        f"[bold]Patient Summary[/bold]\n"
        f"ID: {summary['patient_id']}\n"
        f"Name: {summary['name']}\n"
        f"Age: {summary['age']} | Gender: {summary['gender']}\n"
        f"Height: {summary['height_cm']}cm | Weight: {summary['weight_kg']}kg\n"
        f"Symptoms: {len(summary['symptoms'])}\n"
        f"Active Diseases: {len(summary['active_diseases'])}\n"
        f"Treatments: {summary['treatments']}\n"
        f"Assessment Notes: {summary['assessment_notes']}\n"
        f"Stress Level: {summary['stress_level']:.2f}\n"
        f"Pain Level: {summary['pain_level']:.1f}\n"
        f"Consciousness: {summary['consciousness_level']}\n"
        f"Mobility: {summary['mobility_status']}",
        title="Patient Information",
        border_style="blue"
    )
    
    console.print(panel)
    
    # show discovered information
    if summary['discovered_info']:
        console.print("\n[bold]Discovered Information:[/bold]")
        for info_type, info in summary['discovered_info'].items():
            console.print(f"• {info_type}: {info['value']} (via {info['discovery_method']})")


@app.command()
def show_critical_alerts():
    """show all critical alerts"""
    # physiological alerts
    physio_alerts = physio_engine.get_critical_alerts()
    
    # diagnostic alerts
    diagnostic_alerts = diagnostic_engine.get_critical_alerts()
    
    # treatment alerts
    treatment_alerts = treatment_engine.get_critical_alerts()
    
    all_alerts = []
    
    if physio_alerts:
        for alert in physio_alerts:
            all_alerts.append({
                'type': 'Physiological',
                'patient': alert['patient_name'],
                'alert': f"{alert['vital_name']}: {alert['value']} {alert['unit']}",
                'level': alert['alert_level']
            })
    
    if diagnostic_alerts:
        for alert in diagnostic_alerts:
            all_alerts.append({
                'type': 'Laboratory',
                'patient': alert['patient_id'],
                'alert': f"{alert['test_name']}: {alert['value']} {alert['unit']}",
                'level': alert['critical_level']
            })
    
    if treatment_alerts:
        for alert in treatment_alerts:
            all_alerts.append({
                'type': 'Treatment',
                'patient': alert['patient_id'],
                'alert': f"{alert['drug_name']}: {alert['level']} {alert['unit']}",
                'level': alert['status']
            })
    
    if all_alerts:
        table = Table(title="Critical Alerts")
        table.add_column("Type", style="cyan")
        table.add_column("Patient", style="blue")
        table.add_column("Alert", style="red")
        table.add_column("Level", style="yellow")
        
        for alert in all_alerts:
            table.add_row(alert['type'], alert['patient'], alert['alert'], alert['level'])
        
        console.print(table)
    else:
        console.print("[green]No critical alerts at this time[/green]")


@app.command()
def update_simulation():
    """update all simulation systems"""
    patient_id = cli_session.get_current_patient()
    if not patient_id:
        console.print("[red]No current patient. Use create-patient first.[/red]")
        return
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task1 = progress.add_task("Updating physiological systems...", total=None)
        physio_updates = physio_engine.update_all_patients()
        progress.update(task1, completed=True)
        
        task2 = progress.add_task("Updating drug levels...", total=None)
        drug_updates = treatment_engine.update_drug_levels(patient_id)
        progress.update(task2, completed=True)
        
        task3 = progress.add_task("Updating disease processes...", total=None)
        disease_updates = physio_engine.update_patient_diseases(patient_id)
        progress.update(task3, completed=True)
    
    # show updates
    all_updates = physio_updates + drug_updates + disease_updates
    if all_updates:
        console.print("[yellow]Simulation Updates:[/yellow]")
        for update in all_updates:
            console.print(f"• {update}")
    else:
        console.print("[green]No simulation updates[/green]")


@app.command()
def show_library(
    library_type: str = typer.Option(..., "--type", "-t", help="Library type (symptoms, procedures, labs, imaging, drugs, protocols)")
):
    """show comprehensive medical library"""
    if library_type == "symptoms":
        symptoms = symptom_library.get_all_symptoms()
        table = Table(title="Symptom Library")
        table.add_column("Symptom", style="cyan")
        table.add_column("Category", style="blue")
        table.add_column("Severity", style="yellow")
        table.add_column("Description", style="white")
        
        for symptom in symptoms[:20]:  # limit to first 20
            table.add_row(
                symptom['name'],
                symptom['category'],
                symptom['severity'],
                symptom['description'][:50] + "..." if len(symptom['description']) > 50 else symptom['description']
            )
        
        console.print(table)
        console.print(f"[blue]Showing 20 of {len(symptoms)} symptoms. Use search for more.[/blue]")
    
    elif library_type == "drugs":
        drugs = treatment_engine.get_available_drugs()
        table = Table(title="Drug Library")
        table.add_column("Drug", style="cyan")
        table.add_column("Category", style="blue")
        table.add_column("Routes", style="yellow")
        table.add_column("Monitoring", style="green")
        
        for name, drug in list(drugs.items())[:20]:
            routes = ", ".join([route.value for route in drug.routes])
            monitoring = "Yes" if drug.monitoring_required else "No"
            table.add_row(name, drug.category.value, routes, monitoring)
        
        console.print(table)
        console.print(f"[blue]Showing 20 of {len(drugs)} drugs. Use search for more.[/blue]")
    
    elif library_type == "protocols":
        protocols = treatment_engine.get_available_protocols()
        table = Table(title="Treatment Protocols")
        table.add_column("Protocol", style="cyan")
        table.add_column("Condition", style="blue")
        table.add_column("Success Rate", style="yellow")
        table.add_column("Duration", style="green")
        
        for name, protocol in protocols.items():
            success_pct = f"{protocol.success_rate * 100:.0f}%"
            duration = f"{protocol.duration}h" if protocol.duration > 0 else "Variable"
            table.add_row(name, protocol.condition, success_pct, duration)
        
        console.print(table)
    
    elif library_type == "labs":
        labs = diagnostic_engine.get_available_lab_tests()
        table = Table(title="Laboratory Tests")
        table.add_column("Test", style="cyan")
        table.add_column("Category", style="blue")
        table.add_column("Turnaround", style="yellow")
        table.add_column("Cost", style="green")
        
        for name, test in list(labs.items())[:20]:
            turnaround = f"{test.turnaround_time}min"
            cost = f"${test.cost:.2f}"
            table.add_row(name, test.category.value, turnaround, cost)
        
        console.print(table)
        console.print(f"[blue]Showing 20 of {len(labs)} lab tests. Use search for more.[/blue]")
    
    elif library_type == "imaging":
        imaging = diagnostic_engine.get_available_imaging_studies()
        table = Table(title="Imaging Studies")
        table.add_column("Study", style="cyan")
        table.add_column("Modality", style="blue")
        table.add_column("Body Part", style="yellow")
        table.add_column("Duration", style="green")
        
        for name, study in imaging.items():
            duration = f"{study.duration}min"
            table.add_row(name, study.modality.value, study.body_part, duration)
        
        console.print(table)
    
    else:
        console.print(f"[red]Unknown library type: {library_type}[/red]")


@app.command()
def search_library(
    query: str = typer.Option(..., "--query", "-q", help="Search query"),
    library_type: str = typer.Option("all", "--type", "-t", help="Library type to search")
):
    """search medical library"""
    if library_type == "symptoms" or library_type == "all":
        symptoms = symptom_library.search_symptoms(query)
        if symptoms:
            console.print(f"\n[bold]Symptom Search Results for '{query}':[/bold]")
            for symptom in symptoms[:10]:
                console.print(f"• {symptom['name']} ({symptom['category']}) - {symptom['description'][:100]}...")
    
    if library_type == "drugs" or library_type == "all":
        drugs = treatment_engine.search_drugs(query)
        if drugs:
            console.print(f"\n[bold]Drug Search Results for '{query}':[/bold]")
            for name, drug in list(drugs.items())[:10]:
                console.print(f"• {name} ({drug.category.value}) - Routes: {', '.join([r.value for r in drug.routes])}")
    
    if library_type == "labs" or library_type == "all":
        labs = diagnostic_engine.search_lab_tests(query)
        if labs:
            console.print(f"\n[bold]Lab Test Search Results for '{query}':[/bold]")
            for name, test in list(labs.items())[:10]:
                console.print(f"• {name} ({test.category.value}) - {test.turnaround_time}min, ${test.cost:.2f}")


@app.command()
def show_help():
    """show comprehensive help"""
    help_text = """
[bold]Enhanced Medical Simulation CLI[/bold]

[bold]Patient Management:[/bold]
• create-patient: Create a new patient profile
• discover-info: Discover patient information (BMI, medical history, etc.)
• show-patient-summary: Show comprehensive patient summary

[bold]Physiological Monitoring:[/bold]
• update-vitals: Update patient vital signs
• show-vitals: Display current vital signs with alerts
• add-symptom: Add symptoms to patient
• add-disease: Add disease processes
• update-simulation: Update all simulation systems

[bold]Diagnostics:[/bold]
• order-lab: Order laboratory tests
• order-imaging: Order imaging studies
• complete-lab: Complete lab tests with results
• complete-imaging: Complete imaging studies with findings

[bold]Treatment:[/bold]
• administer-drug: Administer medications
• start-protocol: Start treatment protocols
• show-critical-alerts: Display all critical alerts

[bold]Patient Communication:[/bold]
• talk-to-patient: Interact with patient
• show-emotional-summary: Show patient emotional state

[bold]Medical Libraries:[/bold]
• show-library: Display medical libraries (symptoms, drugs, protocols, labs, imaging)
• search-library: Search medical libraries

[bold]Examples:[/bold]
• Create patient: create-patient --id P001 --name "John Doe" --age 45 --gender male --height 175 --weight 80
• Update vitals: update-vitals --hr 85 --sbp 140 --dbp 90
• Order lab: order-lab --test cbc
• Administer drug: administer-drug --drug aspirin --dose 325 --route oral
• Talk to patient: talk-to-patient --message "How are you feeling today?" --type emotional_assessment
"""
    
    console.print(Panel(help_text, title="Help", border_style="blue"))


if __name__ == "__main__":
    app() 