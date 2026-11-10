# AI E2E Web Testing Harness

Autonomous End-to-End web testing harness engineered with Playwright and the official OpenAI SDK. Designed for seamless, zero-friction interoperability with OpenAI-compatible providers, specifically DeepSeek (`deepseek-chat`, `deepseek-flash`) and OpenCode Go.

---

## Architectural Overview

```text
[ Natural Language Test Spec / User Journey ]
                      |
                      v
      +-------------------------------+
      |       Test Runner Core        |
      |   (Scenario Loader & State)   |
      +---------------+---------------+
                      |
                      v
    +-----------------------------------+
    |      Browser Worker (Playwright)  | <----+
    |  - Navigate / Click / Input       |      |
    |  - Accessibility Tree Snapshot    |      | Executed
    +-----------------+-----------------+      | Actions
                      |                        |
             AOM State Snapshot                |
                      v                        |
    +-----------------------------------+      |
    |      OpenAI Client Adapter        |      |
    | (DeepSeek / OpenCode via baseURL) |      |
    |  - Function Calling Schema        | -----+
    |  - Step Verification & Assertions |
    +-----------------+-----------------+
                      |
                      v
        [ Test Report & Trace Logs ]
```

---

## Why OpenAI SDK for DeepSeek & OpenCode Go?

1. **Native Drop-In Interoperability**: DeepSeek and OpenCode Go implement the standard OpenAI Chat Completions API with Function Calling. Configuring `AI_BASE_URL` and `AI_API_KEY` routes requests directly without requiring custom REST wrapper libraries.
2. **Standard Function Calling**: Tool calling signatures (`tools`, `tool_choice`, `tool_calls`) match the OpenAI SDK specifications directly, allowing reliable execution with `deepseek-chat` and low-latency `deepseek-flash`.
3. **Resilient Retries & Async Stream**: The official `openai` SDK handles connection pooling, timeouts, and automated retries out of the box.

---

## Directory Structure

```text
ai-web-test-harness/
├── .env.example              # Environment variables blueprint
├── .gitignore                # Git exclusions
├── Dockerfile                # Playwright headless container image
├── docker-compose.yml        # Docker orchestration specification
├── install.sh                # Single-enter installer (Linux / macOS / WSL)
├── install.ps1               # Single-enter installer (Windows PowerShell)
├── run.sh                    # Single-enter test runner (Linux / macOS / WSL)
├── run.ps1                   # Single-enter test runner (Windows PowerShell)
├── test.sh                   # Automated pytest runner (Linux / macOS / WSL)
├── test.ps1                  # Automated pytest runner (Windows PowerShell)
├── pyproject.toml            # Project packaging specification
├── requirements.txt          # Python dependency manifests
├── scenarios/                # Declarative test scenario JSON files
│   ├── sample_login.json
│   └── sample_search.json
├── src/
│   ├── ai/
│   │   ├── agent_driver.py   # Autonomous reasoning and tool dispatch loop
│   │   ├── client_factory.py # Async OpenAI client factory
│   │   └── tool_schemas.py   # OpenAI function definitions
│   ├── browser/
│   │   ├── actions.py        # Resilient atomic browser actions
│   │   ├── dom_extractor.py  # Pruned accessibility tree extractor
│   │   └── session.py        # Playwright browser lifecycle manager
│   ├── config/
│   │   └── settings.py       # Central configuration and environment loader
│   ├── engine/
│   │   ├── assertion_engine.py # Live DOM and text assertion engine
│   │   ├── reporter.py       # JSON, Markdown, and CLI table reporting
│   │   ├── runner.py         # Test execution coordinator
│   │   └── scenario_loader.py# Scenario validation and parser
│   └── cli.py                # Command-line entrypoint
└── tests/                    # Automated test suites
    ├── test_assertion.py
    ├── test_config.py
    └── test_scenario_loader.py
```

---

## Quickstart

### 1. Installation

Run the single-enter installer:

```bash
# Linux / macOS / Git Bash
./install.sh

# Windows PowerShell
.\install.ps1
```

### 2. Configure Environment

Copy `.env.example` to `.env` and provide your API credentials:

```bash
# DeepSeek configuration
AI_BASE_URL=https://api.deepseek.com/v1
AI_API_KEY=sk-your-deepseek-api-key
AI_MODEL_NAME=deepseek-chat

# OpenCode Go configuration
# AI_BASE_URL=https://api.opencode.go.id/v1
# AI_API_KEY=your-opencode-api-key
# AI_MODEL_NAME=deepseek-flash
```

### 3. Running Scenarios

Run a test scenario from a JSON file:

```bash
./run.sh run scenarios/sample_search.json
```

Or run an ad-hoc test directly via natural language:

```bash
./run.sh prompt --url "https://example.com" --goal "Verify that the header says Example Domain"
```

Launch with a visible browser window (headed mode):

```bash
./run.sh run scenarios/sample_login.json --headed
```

### 4. Running Unit Tests

Execute the automated test suite:

```bash
./test.sh
```

---

## Authoring Test Scenarios

Test scenarios are declarative JSON files placed inside `scenarios/`:

```json
{
  "name": "checkout_flow_test",
  "description": "Verify product addition to cart and checkout navigation",
  "start_url": "https://store.example.com",
  "goal": "Click on the first product, add it to the cart, navigate to cart, and verify item total.",
  "expected_assertions": [
    "Cart Summary",
    "Total:"
  ],
  "max_steps": 15
}
```

---

## Containerized Execution (Docker)

To run the harness in an isolated container:

```bash
docker compose up --build
```

Reports and failure screenshots will be saved automatically to the mounted `./reports` directory.
