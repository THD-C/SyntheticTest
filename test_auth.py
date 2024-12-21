from playwright.sync_api import sync_playwright
import uuid
import src.Config as cfg
from src.authentication import login, register


def test_authentication_default_user():
    with sync_playwright() as playwright:
        chromium = playwright.chromium
        browser = chromium.launch(headless=(not cfg.BROWSER_ENABLED))
        page = browser.new_page()
        page.goto(cfg.LANDING_PAGE)
        register_result = register(page)
        
        if not register_result:
            login_result = login(page)
            
        browser.close()
        assert login_result or register_result is True

def test_authentication_custom_user():
    with sync_playwright() as playwright:
        chromium = playwright.chromium
        browser = chromium.launch(headless=(not cfg.BROWSER_ENABLED))
        page = browser.new_page()
        page.goto(cfg.LANDING_PAGE)
        username = f"test_{str(uuid.uuid4()).replace('-', '')}"
        password = f"test_{uuid.uuid4()}"
        
        register_result = register(page, username, f"{username}@wp.pl", password)
        if register_result:
            page.get_by_title("Profile").click()
            page.get_by_text("Log out").click()
        
        login_username_result = login(page, username, password)
        if login_username_result:
            page.get_by_title("Profile").click()
            page.get_by_text("Log out").click()
            
        login_email_result = login(page, f"{username}@wp.pl", password)
        
        browser.close()
        
        assert register_result is True
        assert login_username_result is True
        assert login_email_result is True