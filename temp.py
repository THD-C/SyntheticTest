from src.Helpers.RandomUser import RandomUser
from playwright.async_api import async_playwright, BrowserType,Browser, Page, expect
import src.Config as cfg
import asyncio


async def main():
    async with async_playwright() as playwright:
        
        chromium: BrowserType = playwright.chromium
        browser: Browser = await chromium.launch(headless=(not cfg.BROWSER_ENABLED))
        context = await browser.new_context()

        # Start tracing before creating / navigating a page.
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        
        
        page: Page = await context.new_page()
        await page.goto(cfg.LANDING_PAGE)
        
        user_account = RandomUser(page)
        
        await user_account.register()
        
        # Open context menu
        await page.get_by_title("Profile").click()

        # Navigate to personal data page
        await page.get_by_text("Profile").click()

        # Check if the data is correct
        await expect(page.get_by_label("Username")).to_have_value(user_account.username, timeout=5000)
        await expect(page.get_by_label("E-mail")).to_have_value(user_account.username_email, timeout=5000)
        
        # Fill in Personal
        await page.get_by_label("Name", exact=True).fill("John")
        await page.get_by_label("Surname").fill("Smith")
        
        # Fill in Address
        await page.get_by_label("Country").fill("Poland")
        await page.get_by_label("City").fill("Warsaw")
        await page.get_by_label("Postal code").fill("00-001")
        await page.get_by_label("Street").fill("Aleje")
        await page.get_by_label("Building").fill("1")
        await page.get_by_label("Country").fill("Poland")
        await page.locator('#buttonSave').dispatch_event('click')
        await asyncio.sleep(5)
        
        
        await page.goto(cfg.LANDING_PAGE)
        
        # Open context menu
        await page.get_by_title("Profile").click()

        # Navigate to personal data page
        await page.get_by_text("Profile").click()
        
        
        # Validate if the data was successfully saved
        await expect(page.get_by_label("Username")).to_have_value(user_account.username, timeout=5000)
        await expect(page.get_by_label("E-mail")).to_have_value(user_account.username_email, timeout=5000)
        await expect(page.get_by_label("Country")).to_have_value("Poland", timeout=5000)
        await expect(page.get_by_label("City")).to_have_value("Warsaw", timeout=5000)
        await expect(page.get_by_label("Postal code")).to_have_value("00-001", timeout=5000)
        await expect(page.get_by_label("Street")).to_have_value("Aleje", timeout=5000)
        await expect(page.get_by_label("Building")).to_have_value("1", timeout=5000)
        await expect(page.get_by_label("Country")).to_have_value("Poland", timeout=5000)
        

        await context.tracing.stop(path = "./trace.zip")
        await browser.close()
            
if __name__ == "__main__":
    asyncio.run(main())