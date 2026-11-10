import json
from typing import Any, Dict, List, Optional
from playwright.async_api import Page


class DOMExtractor:
    """Extracts and compresses accessibility trees for token-efficient LLM consumption."""

    INTERACTIVE_ROLES = {
        "button", "link", "textbox", "combobox", "checkbox",
        "radio", "menuitem", "tab", "searchbox", "switch"
    }

    CONTENT_ROLES = {
        "heading", "alert", "status", "article", "cell", "row"
    }

    @classmethod
    async def extract_compact_state(cls, page: Page, max_depth: int = 5) -> str:
        """Capture page metadata and pruned accessibility hierarchy."""
        url = page.url
        title = await page.title()
        raw_tree = await page.accessibility.snapshot()

        formatted_lines = [
            f"PAGE_URL: {url}",
            f"PAGE_TITLE: {title}",
            "--- INTERACTIVE & SEMANTIC ELEMENTS ---"
        ]

        if not raw_tree:
            formatted_lines.append("[Empty accessibility tree]")
            return "\n".join(formatted_lines)

        cls._traverse_node(raw_tree, formatted_lines, depth=0, max_depth=max_depth)
        return "\n".join(formatted_lines)

    @classmethod
    def _traverse_node(
        cls,
        node: Dict[str, Any],
        output: List[str],
        depth: int,
        max_depth: int
    ) -> None:
        if depth > max_depth:
            return

        role = node.get("role", "")
        name = node.get("name", "").strip()
        value = node.get("value", "")

        is_interactive = role in cls.INTERACTIVE_ROLES
        is_content = role in cls.CONTENT_ROLES and bool(name)

        if is_interactive or is_content:
            indent = "  " * depth
            details = []
            if name:
                details.append(f'name="{name}"')
            if value:
                details.append(f'value="{value}"')
            if node.get("disabled"):
                details.append("disabled")
            if node.get("selected"):
                details.append("selected")
            if node.get("checked"):
                details.append("checked")

            details_str = " " + " ".join(details) if details else ""
            output.append(f"{indent}- [{role}]{details_str}")

        children = node.get("children", [])
        for child in children:
            cls._traverse_node(child, output, depth + 1, max_depth)
