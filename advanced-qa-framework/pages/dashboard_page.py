from core.base_page import BasePage

class DashboardPage(BasePage):
    WELCOME_HEADER = "h1.welcome-title"
    USER_PROFILE_MENU = "#user-menu"
    LOGOUT_BTN = "button#logout"

    def get_welcome_message(self) -> str:
        self.wait_for_selector(self.WELCOME_HEADER)
        return self.get_text(self.WELCOME_HEADER)

    def logout(self):
        self.click(self.USER_PROFILE_MENU)
        self.click(self.LOGOUT_BTN)