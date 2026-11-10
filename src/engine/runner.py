import logging
from typing import Dict, Any
from src.config.settings import HarnessSettings
from src.browser.session import BrowserSession
from src.browser.actions import BrowserActions
from src.ai.client_factory import create_ai_client
from src.ai.agent_driver import AIAgentDriver
from src.engine.scenario_loader import TestScenario
from src.engine.assertion_engine import AssertionEngine
from src.engine.reporter import TestReporter

logger = logging.getLogger(__name__)


class TestRunner:
    """Coordinates browser lifecycle, AI reasoning steps, assertions, and reporting."""

    def __init__(self, settings: HarnessSettings):
        self.settings = settings

    async def run_scenario(self, scenario: TestScenario) -> Dict[str, Any]:
        """Execute full E2E scenario autonomously."""
        reporter = TestReporter(scenario.name, self.settings.report_dir)
        session = BrowserSession(self.settings)
        client = create_ai_client(self.settings)

        final_status = "FAILED"
        final_summary = "Execution aborted unexpectedly"

        try:
            page = await session.start()
            actions = BrowserActions(page)
            agent = AIAgentDriver(client, self.settings, actions)

            # Initial navigation
            await actions.navigate(scenario.start_url)
            reporter.record_step({
                "step": 0,
                "tool": "navigate_to",
                "args": {"url": scenario.start_url},
                "result": {"status": "success"}
            })

            max_steps = scenario.max_steps or self.settings.max_agent_steps

            for step_idx in range(1, max_steps + 1):
                is_finished, step_data = await agent.step(scenario.goal, step_idx)
                reporter.record_step(step_data)

                if is_finished:
                    final_status = step_data.get("result", {}).get("status", "FAILED")
                    final_summary = step_data.get("result", {}).get("summary", "Agent signaled finish.")
                    break
            else:
                final_summary = f"Reached maximum allowed step threshold ({max_steps}) without completion."

            # Verify declarative assertions if any
            for assertion in scenario.expected_assertions:
                res = await AssertionEngine.evaluate(page, "text_present", assertion)
                reporter.record_assertion(res)
                if not res.get("passed"):
                    final_status = "FAILED"
                    final_summary += f" [Assertion Failed: {assertion}]"

        except Exception as err:
            logger.exception("Unexpected error during scenario execution: %s", err)
            final_status = "FAILED"
            final_summary = f"Fatal execution exception: {str(err)}"

        finally:
            if final_status == "FAILED" and self.settings.screenshot_on_failure:
                try:
                    path = await session.take_screenshot(f"{scenario.name}_failure")
                    reporter.record_screenshot(path)
                except Exception as shot_err:
                    logger.warning("Failed to capture error screenshot: %s", shot_err)

            await session.close()

        reporter.generate(final_status, final_summary)
        return {"scenario": scenario.name, "status": final_status, "summary": final_summary}
