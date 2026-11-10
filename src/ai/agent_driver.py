import json
import logging
from typing import Any, Dict, List, Optional, Tuple
from openai import AsyncOpenAI
from src.config.settings import HarnessSettings
from src.browser.dom_extractor import DOMExtractor
from src.browser.actions import BrowserActions
from src.ai.tool_schemas import HARNESS_TOOLS

logger = logging.getLogger(__name__)


class AIAgentDriver:
    """Orchestrates LLM reasoning cycles and browser tool executions."""

    SYSTEM_INSTRUCTION = (
        "You are an autonomous senior QA test automation engineer driving an E2E browser harness. "
        "Your objective is to verify the specified test scenario. "
        "Analyze the given Page State (Accessibility Tree & URL), decide the exact next single action, "
        "and invoke the corresponding tool. Once the test goal is fully verified, or if a fatal error occurs, "
        "call 'finish_test' with status 'PASSED' or 'FAILED'."
    )

    def __init__(self, client: AsyncOpenAI, settings: HarnessSettings, actions: BrowserActions):
        self.client = client
        self.settings = settings
        self.actions = actions
        self.history: List[Dict[str, Any]] = [
            {"role": "system", "content": self.SYSTEM_INSTRUCTION}
        ]

    async def step(self, goal: str, step_index: int) -> Tuple[bool, Dict[str, Any]]:
        """Run a single autonomous observation-reasoning-action cycle."""
        state_repr = await DOMExtractor.extract_compact_state(self.actions.page)
        user_message = (
            f"Test Objective: {goal}\n"
            f"Step Index: {step_index}/{self.settings.max_agent_steps}\n"
            f"Current Page State:\n{state_repr}"
        )

        current_messages = [*self.history, {"role": "user", "content": user_message}]

        try:
            response = await self.client.chat.completions.create(
                model=self.settings.ai_model_name,
                messages=current_messages,
                tools=HARNESS_TOOLS,
                tool_choice="auto",
                parallel_tool_calls=False,
                temperature=0.1,
            )
        except Exception as err:
            logger.error("LLM API call failed: %s", str(err))
            return True, {"status": "FAILED", "summary": f"LLM API request error: {str(err)}"}

        message = response.choices[0].message
        self.history.append({"role": "user", "content": user_message})
        self.history.append(message.model_dump(exclude_unset=True))

        if not message.tool_calls:
            return False, {"step": step_index, "action": "none", "reasoning": message.content}

        tool_call = message.tool_calls[0]
        fn_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments or "{}")

        return await self._dispatch_tool(tool_call.id, fn_name, args, step_index)

    async def _dispatch_tool(
        self, call_id: str, name: str, args: Dict[str, Any], step_index: int
    ) -> Tuple[bool, Dict[str, Any]]:
        """Execute selected tool and append result to context history."""
        tool_result: Dict[str, Any] = {}
        is_finished = False

        if name == "navigate_to":
            tool_result = await self.actions.navigate(args.get("url", ""))
        elif name == "click_element":
            tool_result = await self.actions.click(args.get("selector", ""))
        elif name == "fill_input":
            tool_result = await self.actions.fill(args.get("selector", ""), args.get("text", ""))
        elif name == "press_key":
            tool_result = await self.actions.press_key(args.get("key", ""))
        elif name == "wait_seconds":
            tool_result = await self.actions.wait_seconds(float(args.get("seconds", 1.0)))
        elif name == "finish_test":
            is_finished = True
            tool_result = {"status": args.get("status", "FAILED"), "summary": args.get("summary", "")}
        else:
            tool_result = {"status": "error", "message": f"Unknown tool: {name}"}

        self.history.append({
            "role": "tool",
            "tool_call_id": call_id,
            "content": json.dumps(tool_result),
        })

        step_record = {
            "step": step_index,
            "tool": name,
            "args": args,
            "result": tool_result,
            "is_finished": is_finished
        }
        return is_finished, step_record
