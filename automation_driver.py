from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

BASE_URL = "https://automationexercise.com"

class LoginHandler:
    def __init__(self, page):
        self.page = page

    async def login(self, username, password):
        print("Navigating to login page...\n", flush=True)
        await self.page.goto(f"{BASE_URL}/login", timeout=10000)

        print("Filling login credentials...", flush=True)
        await self.page.fill('input[data-qa="login-email"]', username)
        await self.page.fill('input[data-qa="login-password"]', password)
        await self.page.click('button[data-qa="login-button"]')

        try:
            await self.page.wait_for_selector("a[href='/logout']", timeout=5000)
            print("Logged in successfully!\n", flush=True)
            return True
        except PlaywrightTimeoutError:
            print("Login failed: Invalid username or password\n", flush=True)
            return False


class ProductSearcher:
    def __init__(self, page):
        self.page = page

    async def search_product(self, product_name):
        print("Navigating to Products page...", flush=True)
        await self.page.goto(f"{BASE_URL}/products", timeout=30000)

        print(f"Searching for product: {product_name}\n", flush=True)
        try:
            await self.page.fill('input#search_product', product_name)
            await self.page.click('button#submit_search')
        except PlaywrightTimeoutError:
            print("Search input/button not found, cannot search product.", flush=True)
            return {"status": "error", "message": "Search elements not found"}

        try:
            await self.page.wait_for_selector(".features_items .productinfo, .product-image-wrapper", timeout=3000)
        except PlaywrightTimeoutError:
            print(f"No products found for '{product_name}'", flush=True)
            return {"status": "not_found", "message": f"Product '{product_name}' not found."}

        products = await self.page.query_selector_all(".features_items .productinfo, .product-image-wrapper .productinfo")
        
        matched_products = []
        
        for prod in products:
            name_el = await prod.query_selector("p")
            if not name_el:
                continue
            name = (await name_el.inner_text()).strip()
            
            # partial match (case-insensitive)
            if product_name.lower() in name.lower():
                matched_products.append(prod)

        # print(f"Matched products count: {len(matched_products)}")

        if len(matched_products) > 0:
            print(f"Success! Product {product_name} found.\n", flush=True)
            prod = matched_products[0]
            name_el = await prod.query_selector("h2, h3, h4")
            price_el = await prod.query_selector(".product-price, .price, h2:has-text('Rs'), .productinfo h2")
            desc_el = await prod.query_selector("p")

            name = (await name_el.inner_text()).strip() if name_el else "Unknown"
            price = (await price_el.inner_text()).strip() if price_el else "Unknown"
            desc = (await desc_el.inner_text()).strip() if desc_el else "No description"

            result = {
                "status": "success",
                "product_name": name,
                "price": price,
                "description": desc
            }
            print("Single product found:", result, flush=True)
            return result
        else:
            print(f"Product '{product_name}' not found or multiple matches found.", flush=True)
            return {"status": "not_found", "message": f"Product '{product_name}' not found or multiple matches found."}


class RobotDriver:
    async def run(self, username, password, product):
        print("Starting AutomationExercise Robot Driver\n", flush=True)

        async with async_playwright() as p:
            # headless=False for debugging, set True for deployment
            browser = await p.chromium.launch(headless=False, slow_mo=50)
            page = await browser.new_page()

            login_handler = LoginHandler(page)
            logged_in = await login_handler.login(username, password)

            if not logged_in:
                await browser.close()
                return {"status": "error", "message": "Invalid login credentials"}

            searcher = ProductSearcher(page)
            result = await searcher.search_product(product)

            await browser.close()
            return result
