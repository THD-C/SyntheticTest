from src.Helpers.RandomUser import RandomUser
import src.Config as cfg
from playwright.async_api import async_playwright, expect
from src.Helpers.setupPlaywrightBrowser import setup_async
import pytest
import asyncio  # noqa: F401


@pytest.mark.asyncio
async def test_buy_crypto_instant():
    async with async_playwright() as playwright:
        page, browser = await setup_async(playwright)

        # Login
        await page.get_by_text("Log in").click()
        await page.wait_for_url(cfg.LOGIN_PAGE, timeout=5000)
        await page.get_by_label("E-mail or username").fill(cfg.USERNAME)
        await page.get_by_label("Password").fill(cfg.PASSWORD)
        await page.get_by_text("Log in").click()

        # Navigate to Wallets page
        await page.get_by_title("Profile").click()
        await page.get_by_text("Profile").click()
        await page.locator("div.dx-item-content.dx-tab-content").filter(
            has_text="Wallets"
        ).click()

        wallet_exist: bool = False
        try:
            await expect(
                page.locator("td[aria-describedby*='dx-col-3']").filter(has_text="USD")
            ).to_have_count(1)
            wallet_exist = True
        except Exception:
            pass

        if not wallet_exist:
            await page.get_by_role("button", name="Add", exact=True).click()
            await page.get_by_placeholder("Select...").click()
            await page.get_by_text("usd", exact=True).click()
            await page.get_by_role("button", name="Save", exact=True).dispatch_event(
                "click"
            )
            await expect(
                page.locator("td[aria-describedby*='dx-col-3']").filter(has_text="USD")
            ).to_have_count(1)

        # Get current money balance
        USD_row_locator = page.locator("//tr[td[contains(text(), 'USD')]]")
        current_money = await USD_row_locator.locator(
            "td[aria-describedby*='dx-col-5']"
        ).text_content()

        has_money: bool = False
        try:
            if float(current_money) > 2:
                has_money = True
        except Exception:
            pass

        if not has_money:
            # Add money to wallet
            await page.get_by_title("Add money").click()
            await page.get_by_label("Amount (min 1)").fill("100")
            await page.get_by_label("Adding money to wallet USD").get_by_label(
                "Add"
            ).click()

        # Go to Stock tab
        await page.get_by_text("Stock").click()

        await page.wait_for_url("http://thdc/en/stock/list", timeout=5000)

        # Click on search button in first row
        await page.locator("xpath=//tbody/tr[1]/td[1]/div/dx-button/div/i").click()

        # Get number of operations before
        ops_num = await page.get_by_text(" -1.00 USD ").count()

        await page.get_by_text("Buy", exact=True).click()
        await page.get_by_label("Amount").fill("1")
        await page.get_by_text("Confirm order").click()

        # Get number of operations after new order
        await page.get_by_text("Stock").click()
        await page.locator("xpath=//tbody/tr[1]/td[1]/div/dx-button/div/i").click()

        # Check if new operation was added
        expect(page.get_by_text(" -1.00 USD ")).to_have_count(ops_num + 1)

        await browser.close()
