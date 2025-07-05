import pytest
from typer.testing import CliRunner
from medsim.cli.interface import app

runner = CliRunner()

def test_start_simulation():
    # start simulation via cli
    result = runner.invoke(app, ['start'])
    assert result.exit_code == 0
    assert 'simulation started' in result.output.lower()

def test_administer_drug_and_monitor():
    # start simulation, give drug, step, check monitor
    runner.invoke(app, ['start'])
    runner.invoke(app, ['give_drug', 'epinephrine', '1.0', 'IV'])
    runner.invoke(app, ['step'])  # step simulation to process drug
    result = runner.invoke(app, ['drugs_monitor'])
    assert 'epinephrine' in result.output.lower()

def test_trends_command():
    runner.invoke(app, ['start'])
    result = runner.invoke(app, ['trends'])
    assert 'trend' in result.output.lower() or 'all trends' in result.output.lower()

def test_alerts_flow():
    runner.invoke(app, ['start'])
    # just check alerts_manage command runs and outputs something reasonable
    result = runner.invoke(app, ['alerts_manage'])
    assert 'alert' in result.output.lower() or 'no active alerts' in result.output.lower() or result.exit_code == 0 