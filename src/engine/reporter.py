import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from rich.console import Console
from rich.table import Table


class TestReporter:
    """Formats and exports test execution results to terminal and files."""

    def __init__(self, scenario_name: str, output_dir: Path):
        self.scenario_name = scenario_name
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.start_time = time.time()
        self.steps: List[Dict[str, Any]] = []
        self.assertions: List[Dict[str, Any]] = []
        self.screenshots: List[str] = []
        self.console = Console()

    def record_step(self, step_data: Dict[str, Any]) -> None:
        self.steps.append(step_data)

    def record_assertion(self, assertion_data: Dict[str, Any]) -> None:
        self.assertions.append(assertion_data)

    def record_screenshot(self, screenshot_path: Path) -> None:
        self.screenshots.append(str(screenshot_path))

    def generate(self, final_status: str, summary: str) -> Path:
        """Write report artifacts to disk and display summary."""
        duration_s = round(time.time() - self.start_time, 2)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_data = {
            "scenario": self.scenario_name,
            "status": final_status,
            "duration_seconds": duration_s,
            "summary": summary,
            "timestamp": timestamp,
            "total_steps": len(self.steps),
            "steps": self.steps,
            "assertions": self.assertions,
            "screenshots": self.screenshots
        }

        # Save JSON
        json_file = self.output_dir / f"{self.scenario_name}_{timestamp}.json"
        json_file.write_text(json.dumps(report_data, indent=2), encoding="utf-8")

        # Save Markdown
        md_file = self.output_dir / f"{self.scenario_name}_{timestamp}.md"
        self._write_markdown(md_file, report_data)

        # Print Table
        self._render_console_summary(report_data)
        return json_file

    def _render_console_summary(self, data: Dict[str, Any]) -> None:
        table = Table(title=f"Test Result: {data['scenario']}")
        table.add_column("Property", style="bold cyan")
        table.add_column("Value")

        table.add_row("Status", f"[{'green' if data['status'] == 'PASSED' else 'red'}]{data['status']}[/]")
        table.add_row("Duration", f"{data['duration_seconds']}s")
        table.add_row("Total Steps", str(data["total_steps"]))
        table.add_row("Summary", data["summary"])
        self.console.print(table)

    def _write_markdown(self, path: Path, data: Dict[str, Any]) -> None:
        lines = [
            f"# Test Report: {data['scenario']}",
            "",
            f"- **Status**: `{data['status']}`",
            f"- **Duration**: {data['duration_seconds']} seconds",
            f"- **Timestamp**: {data['timestamp']}",
            f"- **Summary**: {data['summary']}",
            "",
            "## Steps Executed",
            ""
        ]
        for step in data["steps"]:
            lines.append(f"- Step {step.get('step')}: Tool `{step.get('tool')}`")
        path.write_text("\n".join(lines), encoding="utf-8")
