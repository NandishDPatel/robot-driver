import asyncio
import re
from playwright.async_api import async_playwright

async def run_autonomy(goal: str, headless: bool = True, dry_run: bool = False):
    print(f"Starting autonomous run for goal: {goal}\n")

    # Extract search keyword from goal
    match = re.search(r"(?:find|buy|search for)\s+(.*)", goal, re.IGNORECASE)
    if not match:
        print("❌ Could not understand what to search for.")
        return
    product_name = match.group(1).strip().replace(".", "")
    print(f"🧠 Interpreted product to search for: '{product_name}'\n")

    # Extract URL if provided
    url_match = re.search(r"(https?://[^\s]+)", goal)
    url = url_match.group(1) if url_match else "https://automationexercise.com"
    print(f"🌐 Using site: {url}\n")

    if dry_run:
        print(f"[DRY RUN] Would search for '{product_name}' on {url}")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url)
        await page.wait_for_load_state("networkidle")

        # Try to locate the search bar
        search_box = await page.query_selector("input[name='search']")  # adjust selector
        if not search_box:
            print("❌ Search bar not found on this site.")
            await browser.close()
            return

        await search_box.fill(product_name)
        await page.keyboard.press("Enter")
        await page.wait_for_load_state("networkidle")

        # Try to detect products
        product_elements = await page.query_selector_all(".productinfo.text-center")
        if not product_elements:
            print(f"❌ Product '{product_name}' doesn't exist on this site.")
            await browser.close()
            return

        print(f"✅ Found {len(product_elements)} results for '{product_name}'.\n")

        # Example: extract product names and prices
        products = []
        for product in product_elements:
            name = await product.query_selector_eval("p", "el => el.innerText") if await product.query_selector("p") else "Unnamed"
            price = await product.query_selector_eval("h2", "el => el.innerText") if await product.query_selector("h2") else "N/A"
            products.append({"name": name, "price": price})

        print("🛍️ Products found:")
        for p in products:
            print(p)

        await browser.close()

# Example usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("goal", type=str, help="The goal or task description")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--dry-run", action="store_true", help="Simulate plan without browser actions")
    args = parser.parse_args()

    asyncio.run(run_autonomy(args.goal, headless=args.headless, dry_run=args.dry_run))
