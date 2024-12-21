import uuid
from dataclasses import dataclass, field
from playwright.async_api import Page
import src.Config as cfg  

@dataclass
class RandomUser:
    username: str = field(init=False, default_factory=lambda: f"test_{str(uuid.uuid4()).replace('-', '')}")
    password: str = field(init=False, default_factory=lambda: f"test_{uuid.uuid4()}")
    playwright_page: Page = field(init=True, default=None)
    
    
    @property
    def username_email(self) -> str:
        return self.username + "@wp.pl"
    
    async def register(self):
        await self.playwright_page.get_by_text("Log in").click()
        await self.playwright_page.wait_for_url(cfg.LOGIN_PAGE, timeout=5000)
        await self.playwright_page.get_by_text("Register").click()
        await self.playwright_page.wait_for_url(cfg.REGISTER_PAGE, timeout=5000)
        await self.playwright_page.get_by_label("Username").fill(self.username)
        await self.playwright_page.get_by_label("E-mail").fill(self.username_email)
        await self.playwright_page.get_by_label("Password").fill(self.password)
        await self.playwright_page.get_by_text("I accept the privacy policy").click()
        await self.playwright_page.get_by_text("Register").click()
        
        try:
            await self.playwright_page.wait_for_url(cfg.LANDING_PAGE, timeout=5000)
        except TimeoutError:
            print("Registration failed")
            return False
        
        print("Registration successful")
        return True