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
    # start simulation, give drug, check monitor
    runner.invoke(app, ['start'])
    runner.invoke(app, ['give_drug', 'epinephrine', '1.0', 'IV'])
    result = runner.invoke(app, ['monitor'])
    assert 'epinephrine' in result.output.lower()

def test_trends_command():
    runner.invoke(app, ['start'])
    result = runner.invoke(app, ['trends'])
    assert 'trend' in result.output.lower() or 'all trends' in result.output.lower()

def test_alerts_flow():
    runner.invoke(app, ['start'])
    # simulate a condition that would trigger an alert (e.g., low bp)
    # for now, just check alerts command runs
    result = runner.invoke(app, ['alerts_manage'])
    assert result.exit_code == 0
    assert 'alert' in result.output.lower() or 'no active alerts' in result.output.lower() 