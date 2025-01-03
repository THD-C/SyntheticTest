from src.Helpers.RandomUser import RandomUser
from playwright.async_api import async_playwright, expect
import src.Config as cfg
from src.Helpers.setupPlaywrightBrowser import setup_async
import uuid
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
        
        # await asyncio.sleep(5)
        
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
        
@pytest.mark.asyncio
async def test_change_password():
    async with async_playwright() as playwright:
        page, browser = await setup_async(playwright)
        
        user_account = RandomUser(page)
        new_password = f"test_{uuid.uuid4()}"
        
        await user_account.register()
        
        # Open context menu
        await page.get_by_title("Profile").click()

        # Navigate to personal data page
        await page.get_by_text("Profile").click()
        
        # Open Password panel
        await page.locator("div.dx-item-content.dx-tab-content").filter(has_text="Password").click()
        
        # Fill in old and new password
        await page.get_by_label("Old password").fill(user_account.password)
        await page.get_by_label("New password").fill(new_password)
        
        await page.get_by_text("Change").click()
        
        # Log out
        await page.get_by_title("Profile").click()
        await page.get_by_text("Log out").click()
        
        # Log in with new password
        await page.get_by_text("Log in").click()
        await page.wait_for_url(cfg.LOGIN_PAGE, timeout=5000)
        await page.get_by_label("E-mail or username").fill(user_account.username)
        await page.get_by_label("Password").fill(new_password)
        await page.get_by_text("Log in").click()
        
        await page.wait_for_url(cfg.LANDING_PAGE, timeout=5000)
        
        await browser.close()
        
@pytest.mark.asyncio
async def test_delete_user():
    async with async_playwright() as playwright:
        page, browser = await setup_async(playwright)
        
        user_account = RandomUser(page)
        
        await user_account.register()
        
        # Log out
        await page.get_by_title("Profile").click()
        await page.get_by_text("Log out").click()
        
        # Login as admin
        await page.get_by_text("Log in").click()
        await page.wait_for_url(cfg.LOGIN_PAGE, timeout=5000)
        await page.get_by_label("E-mail or username").fill(cfg.USERNAME)
        await page.get_by_label("Password").fill(cfg.PASSWORD)
        await page.get_by_text("Log in").click()
        
        # Open context menu
        await page.get_by_title("Profile").click()

        # Navigate to personal data page
        await page.get_by_text("Admin").click()
        
        # Set items per page to 100
        await page.get_by_label("Items per page: 100").click()
        
        # Locate the row containing the specific username
        row_locator = page.locator(f"//tr[td[contains(text(), '{user_account.username}')]]")
        
        # Remove the user
        await row_locator.get_by_title("Delete").click()
        await page.get_by_text("Yes").click()
        
        # Check if user was removed
        expect(page.locator(f"//tr[td[contains(text(), '{user_account.username}')]]")).to_have_count(0)
        
        await browser.close()
        
@pytest.mark.asyncio
async def test_elevate_user_permissions():
    async with async_playwright() as playwright:
        page, browser = await setup_async(playwright)
        
        user_account = RandomUser(page)
        
        await user_account.register()
        
        # Log out
        await page.get_by_title("Profile").click()
        await page.get_by_text("Log out").click()
        
        # Login as admin
        await page.get_by_text("Log in").click()
        await page.wait_for_url(cfg.LOGIN_PAGE, timeout=5000)
        await page.get_by_label("E-mail or username").fill(cfg.USERNAME)
        await page.get_by_label("Password").fill(cfg.PASSWORD)
        await page.get_by_text("Log in").click()
        
        # Open context menu
        await page.get_by_title("Profile").click()

        # Navigate to personal data page
        await page.get_by_text("Admin").click()
        
        # Set items per page to 100
        await page.get_by_label("Items per page: 100").click()
        
        # Locate the row containing the specific username
        row_locator = page.locator(f"//tr[td[contains(text(), '{user_account.username}')]]")
        await row_locator.get_by_title("Edit").click()
        
        # Change permissions
        await page.get_by_placeholder("Select...").click()
        await page.get_by_text("BLOGGER_USER", exact=True).click()
        await page.get_by_role("button", name="Change", exact=True).dispatch_event('click')

        """    TO BE DELIVERED (once this info will be available on Frontend)
            # Check if permissions were changed
            await page.goto(page.url)
            await page.get_by_label("Items per page: 100").click()
            row_locator = page.locator(f"//tr[td[contains(text(), '{user_account.username}')]]")
            await row_locator.get_by_title("Edit").click()
        """
        
        
        await browser.close()