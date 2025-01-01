from playwright.async_api import async_playwright
from src.Helpers.setupPlaywrightBrowser import setup_async
import src.Config as cfg
import pytest
import asyncio  # noqa: F401

@pytest.mark.asyncio
async def test_login_with_username():
    async with async_playwright() as playwright:
        page, browser = await setup_async(playwright)
        
        await page.get_by_text("Log in").click()
        await page.wait_for_url(cfg.LOGIN_PAGE, timeout=5000)
        await page.get_by_label("E-mail or username").fill(cfg.USERNAME)
        await page.get_by_label("Password").fill(cfg.PASSWORD)
        await page.get_by_text("Log in").click()
        await page.wait_for_url(cfg.LANDING_PAGE, timeout=5000)
        
        await browser.close()

        assert page.url == cfg.LANDING_PAGE

@pytest.mark.asyncio
async def test_login_with_email():
    async with async_playwright() as playwright:
        page, browser = await setup_async(playwright)
        
        await page.get_by_text("Log in").click()
        await page.wait_for_url(cfg.LOGIN_PAGE, timeout=5000)
        await page.get_by_label("E-mail or username").fill(cfg.E_MAIL)
        await page.get_by_label("Password").fill(cfg.PASSWORD)
        await page.get_by_text("Log in").click()
        await page.wait_for_url(cfg.LANDING_PAGE, timeout=5000)
        
        await browser.close()

        assert page.url == cfg.LANDING_PAGE