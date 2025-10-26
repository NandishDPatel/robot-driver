import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError


# CONFIG: Credentials and product to search
USERNAME = "nanlogx@gmail.co"   # Replace with valid AutomationExercise email
PASSWORD = "Login@12345"          # Replace with valid password
SEARCH_PRODUCT = "dress"           # Product to search
BASE_URL = "https://automationexercise.com" 

class LoginHandler:
    def __init__(self, page):
        self.page = page

    async def login(self, username, password):
        print("Navigating to login page...\n")
        await self.page.goto(f"{BASE_URL}/login", timeout=5000)

        print("Filling login credentials...")
        await self.page.fill('input[data-qa="login-email"]', username)
        await self.page.fill('input[data-qa="login-password"]', password)
        await self.page.click('button[data-qa="login-button"]')

        try:
            await self.page.wait_for_selector("a[href='/logout']", timeout=5000)
            print("Logged in successfully!\n")
            return True
        except PlaywrightTimeoutError:
            print("Login failed: Invalid username or password\n")
            return False

class ProductSearcher:
    def __init__(self, page):
        self.page = page

    async def search_product(self, product_name):
        print("Navigating to Products page...")
        await self.page.goto(f"{BASE_URL}/products", timeout=30000)

        print(f"Searching for product: {product_name}")
        try:
            await self.page.fill('input#search_product', product_name)
            await self.page.click('button#submit_search')
        except PlaywrightTimeoutError:
            print("Search input/button not found, cannot search product.")
            return False

        try:
            await self.page.wait_for_selector(".features_items .productinfo, .product-image-wrapper", timeout=3000)
        except PlaywrightTimeoutError:
            print(f"\nProduct '{product_name}' not found.")
            return False

        products = await self.page.query_selector_all(".features_items .productinfo, .product-image-wrapper")
        for prod in products:
            text = (await prod.inner_text()) or ""
            if product_name.lower() in text.lower():
                name_el = await prod.query_selector("h2, h3, h4, p")
                price_el = await prod.query_selector(".product-price, .price, h2:has-text('Rs'), .productinfo h2")
                desc_el = await prod.query_selector("p")

                name = (await name_el.inner_text()).strip() if name_el else "Unknown"
                price = (await price_el.inner_text()).strip() if price_el else "Unknown"
                desc = (await desc_el.inner_text()).strip() if desc_el else "No description"

                print(f"\nProduct {SEARCH_PRODUCT} found!\n")
                print("First product details:")
                print(f"Name: {name}")
                print(f"Price: {price}")
                print(f"Description: {desc}")
                return True

        print(f"Product '{product_name}' not found in results.")
        return False

class RobotDriver:
    async def run(self, username, password, product):
        print("Starting AutomationExercise Robot Driver\n")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=100)
            page = await browser.new_page()

            login_handler = LoginHandler(page)
            logged_in = await login_handler.login(username, password)

            if not logged_in:
                await browser.close()
                return

            searcher = ProductSearcher(page)
            await searcher.search_product(product)

            await browser.close()

if __name__ == "__main__":
    driver = RobotDriver()
    asyncio.run(driver.run(USERNAME, PASSWORD, SEARCH_PRODUCT))