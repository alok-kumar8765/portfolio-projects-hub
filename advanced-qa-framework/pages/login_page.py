from core.base_page import BasePage

#class LoginPage(BasePage):
    # Correct locators for https://the-internet.herokuapp.com/login
#    USERNAME_INPUT = "#username"
#    PASSWORD_INPUT = "#password"
#    SUBMIT_BTN = "button[type='submit']"
#    ERROR_MSG = "#flash.error, div#flash"
#    SUCCESS_MSG = "#flash.success"

#    def login(self, username: str, password: str):
#        self.fill(self.USERNAME_INPUT, username)
#        self.fill(self.PASSWORD_INPUT, password)
#        self.click(self.SUBMIT_BTN)

#    def get_flash_message(self) -> str:
#        self.wait_for_selector(("#flash"))
#        return self.get_text("#flash")

# pages/login_page.py
from core.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    SUBMIT_BTN = "button[type='submit']"
    FLASH_MESSAGE = "#flash"

    def login(self, username: str, password: str):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.page.locator(self.SUBMIT_BTN).click()

    def get_flash_message(self) -> str:
        """Grabs the text content of the notification banner after login attempt."""
        self.page.locator(self.FLASH_MESSAGE).wait_for(state="visible")
        return self.page.locator(self.FLASH_MESSAGE).inner_text().strip()