from src.Helpers.RandomUser import RandomUser
from playwright.async_api import async_playwright, expect
from src.Helpers.setupPlaywrightBrowser import setup_async
import pytest
import asyncio


@pytest.mark.asyncio
async def test_create_wallet_data():
    async with async_playwright() as playwright:
        page, browser = await setup_async(playwright)

        user_account = RandomUser(page)

        await user_account.register()
        
        # Open context menu
        await page.get_by_title("Profile").click()

        # Navigate to personal data page
        await page.get_by_text("Profile").click()
        
        # Open Wallet panel
        await page.locator("div.dx-item-content.dx-tab-content").filter(has_text="Wallets").click()
        
        # Open context to create new wallet
        await page.get_by_role("button", name="Add", exact=True).click()
        
        # Select USD from list and save
        await page.get_by_placeholder("Select...").click()
        await page.get_by_text("usd", exact=True).click()
        await page.get_by_role("button", name="Save", exact=True).dispatch_event('click')
        
        # Check if wallet was created
        await expect(page.locator("td[aria-describedby*='dx-col-3']").filter(has_text="USD")).to_have_count(1)

        await browser.close()
            