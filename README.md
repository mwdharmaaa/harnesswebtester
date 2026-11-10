# AI E2E Web Testing Harness

Autonomous End-to-End web testing harness powered by Playwright and OpenAI SDK. Built to execute dynamic test scenarios with custom OpenAI-compatible API providers including DeepSeek (`deepseek-chat`, `deepseek-flash`) and OpenCode Go.

---

## Key Features

- **Multi-Provider OpenAI SDK Support**: Seamlessly point to DeepSeek (`https://api.deepseek.com/v1`) or OpenCode Go endpoints via standard `OPENAI_BASE_URL` and `OPENAI_API_KEY`.
- **Token-Efficient Accessibility Pruning**: Extracts Playwright Accessibility Object Model (AOM) snapshots instead of bloated raw HTML DOM, reducing context token overhead by up to 90%.
- **Atomic Tool Calling**: DeepSeek function calling drives atomic browser operations: navigation, click, input, assertion verification, and error recovery.
- **Single-Enter Shell Orchestration**: Pre-configured `run.sh`, `test.sh`, and `install.sh` scripts for zero cognitive friction.
- **Trace & Artifact Recording**: Automated screenshot capture and JSON/Markdown test run reporting.
