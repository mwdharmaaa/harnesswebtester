import json
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field


class TestScenario(BaseModel):
    """Declarative specification for an AI-driven E2E test."""

    name: str = Field(description="Unique identifier for the test scenario")
    description: str = Field(default="", description="High-level test goal or user story")
    start_url: str = Field(description="Initial URL where browser should navigate")
    goal: str = Field(description="Natural language instruction for the AI driver")
    expected_assertions: List[str] = Field(
        default_factory=list,
        description="Conditions that must pass before concluding the test"
    )
    max_steps: Optional[int] = Field(
        default=None,
        description="Optional custom step limit override"
    )


class ScenarioLoader:
    """Reads and validates test scenarios from JSON files."""

    @classmethod
    def load_from_file(cls, file_path: Path) -> TestScenario:
        """Parse and validate scenario from disk."""
        if not file_path.exists():
            raise FileNotFoundError(f"Scenario file not found at: {file_path}")

        raw_data = json.loads(file_path.read_text(encoding="utf-8"))
        return TestScenario(**raw_data)
