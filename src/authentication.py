from playwright.sync_api import Page, TimeoutError

import src.Config as cfg


def login(page: Page, username: str = cfg.USERNAME, password: str = cfg.PASSWORD) -> bool:
    page.get_by_text("Log in").click()
    page.wait_for_url(cfg.LOGIN_PAGE, timeout=5000)
    page.get_by_label("E-mail or username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_text("Log in").click()
    try:
        page.wait_for_url(cfg.LANDING_PAGE, timeout=5000)
    except TimeoutError:
        print("Login failed")
        return False

    print("Login successful")
    return True

def register(page: Page, username: str = cfg.USERNAME, email: str = cfg.E_MAIL, password: str = cfg.PASSWORD) -> bool:
    page.get_by_text("Log in").click()
    page.wait_for_url(cfg.LOGIN_PAGE, timeout=5000)
    page.get_by_text("Register").click()
    page.wait_for_url(cfg.REGISTER_PAGE, timeout=5000)
    page.get_by_label("Username").fill(username)
    page.get_by_label("E-mail").fill(email)
    page.get_by_label("Password").fill(password)
    page.get_by_text("I accept the privacy policy").click()
    page.get_by_text("Register").click()
    
    try:
        page.wait_for_url(cfg.LANDING_PAGE, timeout=5000)
    except TimeoutError:
        print("Registration failed")
        return False
    
    print("Registration successful")
    return True