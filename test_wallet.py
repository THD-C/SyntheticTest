from src.Helpers.RandomUser import RandomUser
import src.Config as cfg
from playwright.async_api import async_playwright, expect
from src.Helpers.setupPlaywrightBrowser import setup_async
import pytest
import asyncio  # noqa: F401


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
            
@pytest.mark.asyncio
async def test_add_money_to_wallet():
    async with async_playwright() as playwright:
        page, browser = await setup_async(playwright)
        
        # Login
        await page.get_by_text("Log in").click()
        await page.wait_for_url(cfg.LOGIN_PAGE, timeout=5000)
        await page.get_by_label("E-mail or username").fill(cfg.USERNAME)
        await page.get_by_label("Password").fill(cfg.PASSWORD)
        await page.get_by_text("Log in").click()
        
        # Open context menu
        await page.get_by_title("Profile").click()

        # Navigate to personal data page
        await page.get_by_text("Profile").click()
        
        # Open Wallet panel
        await page.locator("div.dx-item-content.dx-tab-content").filter(has_text="Wallets").click()
        
        # Check if wallet exists
        wallet_exist: bool = False
        try:
            await expect(page.locator("td[aria-describedby*='dx-col-3']").filter(has_text="USD")).to_have_count(1)
            wallet_exist = True
        except Exception:
            print("Wallet does not exist")
            
        if not wallet_exist:
            # Open context to create new wallet
            await page.get_by_role("button", name="Add", exact=True).click()
            
            # Select USD from list and save
            await page.get_by_placeholder("Select...").click()
            await page.get_by_text("usd", exact=True).click()
            await page.get_by_role("button", name="Save", exact=True).dispatch_event('click')
            
            # Check if wallet was created
            await expect(page.locator("td[aria-describedby*='dx-col-3']").filter(has_text="USD")).to_have_count(1)
        
        # Get current money balance
        USD_row_locator = page.locator("//tr[td[contains(text(), 'USD')]]")
        current_money = await USD_row_locator.locator("td[aria-describedby*='dx-col-5']").text_content()
        current_money = float(current_money.strip()) + 100.0
        
        # Press Add money button
        await page.get_by_title("Add money").click()
        
        # Fill in amount
        await page.get_by_label("Amount (min 1)").fill("100")
        
        # Press Add button
        await page.get_by_label("Adding money to wallet USD").get_by_label("Add").click()
        
        # Check if money was added
        await expect(USD_row_locator.locator("td[aria-describedby*='dx-col-5']").filter(has_text=str(current_money))).to_have_count(1)
        
        await browser.close()
        
@pytest.mark.asyncio
async def test_remove_wallet():
    async with async_playwright() as playwright:
        page, browser = await setup_async(playwright)
        
        # Login
        await page.get_by_text("Log in").click()
        await page.wait_for_url(cfg.LOGIN_PAGE, timeout=5000)
        await page.get_by_label("E-mail or username").fill(cfg.USERNAME)
        await page.get_by_label("Password").fill(cfg.PASSWORD)
        await page.get_by_text("Log in").click()
        
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
        await page.get_by_text("pln", exact=True).click()
        await page.get_by_role("button", name="Save", exact=True).dispatch_event('click')
        
        # Check if wallet was created
        await expect(page.locator("td[aria-describedby*='dx-col-3']").filter(has_text="pln")).to_have_count(1)
        
        # Find the row containing "PLN" and click the delete button within that row
        pln_row_locator = page.locator("//tr[td[contains(text(), 'PLN')]]")
        delete_button_locator = pln_row_locator.locator(".dx-icon-trash")
        
        # Press Delete button
        await delete_button_locator.click()
        
        # Confirm deletion
        await page.get_by_text("Yes").click()
        
        await browser.close()