import argparse
import asyncio
import sys
from pathlib import Path
from src.config.settings import get_settings
from src.engine.scenario_loader import ScenarioLoader, TestScenario
from src.engine.runner import TestRunner


def parse_args():
    parser = argparse.ArgumentParser(
        description="AI E2E Web Testing Harness (DeepSeek & OpenCode Go compatible)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Run scenario command
    run_parser = subparsers.add_parser("run", help="Execute test scenario from JSON file")
    run_parser.add_argument("scenario", type=Path, help="Path to scenario JSON file")
    _add_shared_options(run_parser)

    # Prompt command
    prompt_parser = subparsers.add_parser("prompt", help="Execute ad-hoc test with custom goal")
    prompt_parser.add_argument("--url", required=True, help="Initial target URL")
    prompt_parser.add_argument("--goal", required=True, help="Natural language objective")
    prompt_parser.add_argument("--name", default="adhoc_test", help="Scenario identifier")
    _add_shared_options(prompt_parser)

    return parser.parse_args()


def _add_shared_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--model", help="AI model name (e.g. deepseek-chat, deepseek-flash)")
    parser.add_argument("--base-url", help="OpenAI-compatible base URL")
    parser.add_argument("--api-key", help="API key for authentication")
    parser.add_argument("--headed", action="store_true", help="Launch browser in headed mode")
    parser.add_argument("--max-steps", type=int, help="Override maximum reasoning steps")


async def async_main():
    args = parse_args()
    settings = get_settings()

    if args.model:
        settings.ai_model_name = args.model
    if args.base_url:
        settings.ai_base_url = args.base_url
    if args.api_key:
        settings.ai_api_key = args.api_key
    if args.headed:
        settings.headless = False
    if args.max_steps:
        settings.max_agent_steps = args.max_steps

    if args.command == "run":
        scenario = ScenarioLoader.load_from_file(args.scenario)
    elif args.command == "prompt":
        scenario = TestScenario(
            name=args.name,
            start_url=args.url,
            goal=args.goal
        )
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)

    runner = TestRunner(settings)
    result = await runner.run_scenario(scenario)
    sys.exit(0 if result.get("status") == "PASSED" else 1)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
