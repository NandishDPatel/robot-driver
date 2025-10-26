import aiohttp
import asyncio
from typing import Any, Dict, List


async def fetch_mcp_context(mcp_url: str, page_url: str) -> Dict[str, Any]:
    """Try to fetch structured context from a running MCP server.

    This is a best-effort call. The MCP server's exact API may differ; the
    function assumes a simple POST /context endpoint that accepts JSON with
    the page URL. If the server is not available or returns an error, an
    exception is raised and the caller should fallback to a local snapshot.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{mcp_url.rstrip('/')}/context", json={"url": page_url}, timeout=10) as resp:
                resp.raise_for_status()
                return await resp.json()
        except Exception:
            raise


async def snapshot_from_playwright(page) -> Dict[str, Any]:
    """Create a structured page context from Playwright's accessibility snapshot
    plus a small set of interactive elements.

    Returns a dictionary with 'url' and an 'elements' list. Each element is a
    dict: {role, name, text, tag, id, classes, selector_hint}.
    """
    ctx: Dict[str, Any] = {"url": page.url, "elements": []}

    try:
        acc = await page.accessibility.snapshot()
    except Exception:
        acc = None

    # Walk accessibility tree to collect nodes
    def walk_acc(node, out_list: List[Dict[str, Any]]):
        if not node:
            return
        role = node.get("role")
        name = node.get("name")
        value = node.get("value")
        if role or name:
            out_list.append({"role": role, "name": name, "value": value})
        for child in node.get("children", []) or []:
            walk_acc(child, out_list)

    elements = []
    if acc:
        walk_acc(acc, elements)

    # In addition, gather visible interactive elements via CSS
    try:
        interactive = await page.query_selector_all("button, a, input, select, textarea, [role='button'], [role='link']")
        for idx, el in enumerate(interactive):
            try:
                tag = (await el.evaluate("e => e.tagName.toLowerCase()"))
                el_id = await el.get_attribute("id") or ""
                classes = await el.get_attribute("class") or ""
                text = (await el.inner_text()) or ""
                name = await el.get_attribute("aria-label") or None
                selector_hint = el_id and f"#{el_id}" or f"{tag}:nth-of-type({idx + 1})"
                elements.append({
                    "tag": tag,
                    "id": el_id,
                    "classes": classes,
                    "text": text.strip(),
                    "name": name,
                    "selector_hint": selector_hint,
                })
            except Exception:
                continue
    except Exception:
        pass

    ctx["elements"] = elements
    return ctx
