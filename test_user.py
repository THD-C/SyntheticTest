from src.Helpers.RandomUser import RandomUser
from playwright.async_api import async_playwright, BrowserType,Browser, Page, expect
import src.Config as cfg
from src.Helpers.setupPlaywrightBrowser import setup_async
import pytest
import asyncio

@pytest.mark.asyncio
async def test_read_personal_data():
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

        # Check if the data is correct
        await expect(page.get_by_label("Username")).to_have_value("admin", timeout=5000)
        await expect(page.get_by_label("E-mail")).to_have_value("admin@thdc.pl", timeout=5000)

        # Check user data
        await expect(page.get_by_label("Username")).to_have_value(cfg.USERNAME, timeout=5000)
        await expect(page.get_by_label("E-mail")).to_have_value(cfg.E_MAIL, timeout=5000)
        await expect(page.get_by_label("Country")).to_have_value("Poland", timeout=5000)
        await expect(page.get_by_label("City")).to_have_value("Lodz", timeout=5000)
        await expect(page.get_by_label("Postal code")).to_have_value("90-924", timeout=5000)
        await expect(page.get_by_label("Street")).to_have_value("Zeromskiego", timeout=5000)
        await expect(page.get_by_label("Building")).to_have_value("116", timeout=5000)
        await expect(page.get_by_label("Country")).to_have_value("Poland", timeout=5000)
        
        await browser.close()

@pytest.mark.asyncio
async def test_fill_in_personal_data():
    async with async_playwright() as playwright:
        page, browser = await setup_async(playwright)
        
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
        
        # Go back to the landing page
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
        

        await browser.close()