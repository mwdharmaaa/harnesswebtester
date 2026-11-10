# AI E2E Web Testing Harness (Desktop & CLI)

Autonomous End-to-End web testing application engineered with Playwright, OpenAI SDK, and an Electron desktop workspace. Designed with the same architectural pedigree as **Commanda** and **AI Code Editor**, enabling seamless interoperability with DeepSeek (`deepseek-chat`, `deepseek-flash`) and OpenCode Go.

---

## Architectural Overview

```text
┌────────────────────────────────────────────────────────┐
│           Electron Frameless Desktop GUI               │
│   (Scenario Manager │ Live Stream Logs │ Settings)     │
└───────────────────────────┬────────────────────────────┘
                            │ Typed IPC Bridge
┌───────────────────────────▼────────────────────────────┐
│                  Harness Engine Core                   │
│         (AOM Extractor │ AI Reasoning Loop)            │
└───────────────────────────┬────────────────────────────┘
                            │ OpenAI SDK & Tool Calls
┌───────────────────────────▼────────────────────────────┐
│      OpenAI-Compatible Gateway (DeepSeek / OpenCode)   │
│               deepseek-chat │ deepseek-flash           │
└────────────────────────────────────────────────────────┘
```

---

## Operation Modes

### 1. Desktop GUI Application (Commanda / AI Code Editor Style)
- Frameless monochrome dark workspace (`#0c0c0e`).
- Real-time streaming execution feed and active tool badges.
- Visual scenario picker and live testing status pills.
- Built-in credentials and model switcher for DeepSeek and OpenCode Go.

Launch via:
```bash
# Linux / macOS / Git Bash
./runapp.sh

# Windows PowerShell
.\runapp.ps1
```

### 2. Autonomous Terminal CLI & CI Runner
- Headless execution engine for automated pipelines and terminal workflows.
- Rich ASCII terminal summaries, JSON report exports, and failure screenshots.

Launch via:
```bash
./run.sh run scenarios/sample_search.json
# Or ad-hoc prompt:
./run.sh prompt --url "https://html.duckduckgo.com/html/" --goal "Verify search results appear"
```

---

## Directory Architecture

```text
ai-web-test-harness/
├── electron/
│   ├── main/
│   │   ├── index.cjs             # Window lifecycle, frameless window, menu
│   │   ├── ipc_handlers.cjs      # IPC handlers for scenarios, reports, runs
│   │   └── process_bridge.cjs    # Real-time stdout/stderr log stream bridge
│   ├── preload/
│   │   └── preload.cjs           # Secure contextBridge exposure
│   └── renderer/
│       ├── app.js                # Frontend reactive state and IPC dispatch
│       ├── index.html            # Frameless titlebar and dock layout
│       └── styles.css            # Linear/Raycast dark theme typography
├── scenarios/                    # Declarative test scenario JSON files
├── src/                          # Autonomous AI testing engine (Python)
├── tests/                        # Automated unit tests
├── Dockerfile                    # Containerized Playwright headless build
├── docker-compose.yml            # Container orchestration specification
├── install.sh / install.ps1      # Single-enter installer
├── run.sh / run.ps1              # Terminal CLI runner
├── runapp.sh / runapp.ps1        # Desktop GUI application launcher
├── test.sh / test.ps1            # Unit test runner
├── package.json                  # Desktop package specification
├── pyproject.toml                # Engine packaging specification
└── requirements.txt              # Python dependencies
```

---

## Configuration

Set credentials via `.env` or in the Desktop GUI Settings tab:

```bash
# DeepSeek API (Default)
AI_BASE_URL=https://api.deepseek.com/v1
AI_API_KEY=your_deepseek_api_key
AI_MODEL_NAME=deepseek-chat

# OpenCode Go Gateway (Alternative)
# AI_BASE_URL=https://api.opencode.go.id/v1
# AI_API_KEY=your_opencode_api_key
# AI_MODEL_NAME=deepseek-flash
```
