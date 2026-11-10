from pathlib import Path
from src.engine.scenario_loader import ScenarioLoader, TestScenario


def test_scenario_loader_valid(tmp_path: Path):
    scenario_file = tmp_path / "test_scenario.json"
    scenario_file.write_text("""
    {
        "name": "mock_test",
        "description": "Mock description",
        "start_url": "https://example.com",
        "goal": "Verify title",
        "expected_assertions": ["Example Domain"],
        "max_steps": 5
    }
    """, encoding="utf-8")

    loaded = ScenarioLoader.load_from_file(scenario_file)
    assert isinstance(loaded, TestScenario)
    assert loaded.name == "mock_test"
    assert loaded.start_url == "https://example.com"
    assert loaded.max_steps == 5
    assert len(loaded.expected_assertions) == 1
