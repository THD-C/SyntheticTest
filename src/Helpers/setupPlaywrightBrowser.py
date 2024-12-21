import playwright.sync_api as sync_pw
import playwright.async_api as async_pw

import src.Config as cfg


def setup(playwright: sync_pw.PlaywrightContextManager) -> tuple[sync_pw.Page, sync_pw.Browser]:
    chromium: sync_pw.BrowserType = playwright.chromium
    browser: sync_pw.Browser = chromium.launch(headless=(not cfg.BROWSER_ENABLED))
    page: sync_pw.Page = browser.new_page()
    page.goto(cfg.LANDING_PAGE)
    
    return page, browser

async def setup_async (playwright: async_pw.PlaywrightContextManager)-> tuple[async_pw.Page, async_pw.Browser]:
    chromium: async_pw.BrowserType = playwright.chromium
    browser: async_pw.Browser = await chromium.launch(headless=(not cfg.BROWSER_ENABLED))
    page: async_pw.Page = await browser.new_page()
    await page.goto(cfg.LANDING_PAGE)
    
    return page, browser

async def setup_async_with_trace (playwright: async_pw.PlaywrightContextManager)-> tuple[async_pw.Page, async_pw.Browser, async_pw.BrowserContext]:
    chromium: async_pw.BrowserType = playwright.chromium
    browser: async_pw.Browser = await chromium.launch(headless=(not cfg.BROWSER_ENABLED))
    context: async_pw.BrowserContext = await browser.new_context()
    
    await context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    page: async_pw.Page = await context.new_page()
    await page.goto(cfg.LANDING_PAGE)
    
    return page, browser, context