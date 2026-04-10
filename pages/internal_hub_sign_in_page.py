from pages.base_page import BasePage


class InternalHubSignInPage(BasePage):
    # Locators
    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"
    SIGN_IN_BUTTON = ".submit-btn"
    INTERNAL_HUB_MEMBERS_PAGE_URL_SUBSTRING = "members"
    MEMBER_SEARCH_INPUT = ".search-box .default-border"

    def open(self, url: str):
        self.visit(url)

    def login(self, email: str, password: str):
        self.page.locator(self.EMAIL_INPUT).fill(email)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.SIGN_IN_BUTTON).click()

    def wait_for_internal_hub_members_page(self):
        self.page.wait_for_url(f"**/{self.INTERNAL_HUB_MEMBERS_PAGE_URL_SUBSTRING}", timeout=15000)

    def search_member_by_email(self, email: str):
        self.page.locator(self.MEMBER_SEARCH_INPUT).fill(email)
        self.page.locator(self.MEMBER_SEARCH_INPUT).press("Enter")
 
