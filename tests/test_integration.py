import pytest
from medsim.core.simulation import MedicalSimulation
from medsim.core.monitoring import MonitoringSystem

@pytest.fixture
def sim():
    # create a new simulation instance
    return MedicalSimulation()

def test_simulation_starts_and_monitors(sim):
    # start simulation and check monitoring
    sim.start_simulation()
    assert sim.current_state.monitoring_active
    assert sim.monitoring.monitoring_active

def test_administer_drug_adds_to_monitoring(sim):
    sim.start_simulation()
    sim.administer_drug('epinephrine', 1.0, 'IV')
    sim.update_simulation()  # step simulation to process drug
    summary = sim.get_drug_monitoring_summary()
    # check that epinephrine is tracked
    assert 'epinephrine' in summary
    # check that level is in expected range
    assert summary['epinephrine']['current_level'] > 0

def test_trend_data_updates(sim):
    sim.start_simulation()
    sim._update_vital_signs()
    trends = sim.get_all_trends()
    # should have at least one vital sign trend
    assert any(trends.values()) 