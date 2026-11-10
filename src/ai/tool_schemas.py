from typing import List, Dict, Any

HARNESS_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "navigate_to",
            "description": "Navigate page to an absolute URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Target absolute URL (e.g. https://example.com)"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "click_element",
            "description": "Click an interactive element using a selector, text, or accessibility name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "selector": {"type": "string", "description": "Locator such as 'text=Login', 'role=button', or CSS"}
                },
                "required": ["selector"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fill_input",
            "description": "Type text into a designated input, textbox, or search field.",
            "parameters": {
                "type": "object",
                "properties": {
                    "selector": {"type": "string", "description": "Input locator or accessibility reference"},
                    "text": {"type": "string", "description": "Text value to fill into field"}
                },
                "required": ["selector", "text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "press_key",
            "description": "Send a keyboard button event (e.g. 'Enter', 'Escape', 'ArrowDown').",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Standard keyboard key name"}
                },
                "required": ["key"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "wait_seconds",
            "description": "Pause execution to await dynamic network or rendering operations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "seconds": {"type": "number", "description": "Duration in seconds (e.g. 1.5)"}
                },
                "required": ["seconds"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "assert_condition",
            "description": "Verify page state condition (text presence, element existence, or URL match).",
            "parameters": {
                "type": "object",
                "properties": {
                    "condition_type": {
                        "type": "string",
                        "enum": ["text_present", "element_visible", "url_contains"],
                        "description": "Type of assertion check"
                    },
                    "expected": {"type": "string", "description": "Expected text string, substring, or selector"}
                },
                "required": ["condition_type", "expected"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "finish_test",
            "description": "Declare final result of the E2E test execution and end loop.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["PASSED", "FAILED"],
                        "description": "Final test outcome status"
                    },
                    "summary": {"type": "string", "description": "Explanatory rationale of test outcome"}
                },
                "required": ["status", "summary"]
            }
        }
    }
]
