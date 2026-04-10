from pages.base_page import BasePage
import re
import utils.waiters.network_waits as network_waits


class MemberJoinPage(BasePage):
    # Locators
    FIRST_NAME_INPUT = "#firstName"
    LAST_NAME_INPUT = "#lastName"
    EMAIL_INPUT = "#email"
    PHONE_NUMBER_INPUT = "#phoneNumber"
    PASSWORD_INPUT = "#password"
    TERMS_OF_USE_CHECKBOX = re.compile("agree to Ezra", re.I)
    SUBMIT_BUTTON = "Submit"
    FOOTER_NOTIFICATION_TOAST = ".toast.--visible"
    SELECT_YOUR_PLAN_PAGE_URL_SUBSTRING = "sign-up/select-plan"

    def fill_legal_first_name(self, first_name: str):
        self.page.locator(self.FIRST_NAME_INPUT).fill(first_name)

    def fill_legal_last_name(self, last_name: str):
        self.page.locator(self.LAST_NAME_INPUT).fill(last_name)

    def fill_email(self, email: str):
        self.page.locator(self.EMAIL_INPUT).fill(email)

    def fill_phone_number(self, phone_number: str):
        self.page.locator(self.PHONE_NUMBER_INPUT).fill(phone_number)

    def fill_password(self, password: str):
        self.page.locator(self.PASSWORD_INPUT).fill(password)

    def accept_terms_and_conditions(self):
        self.page.get_by_role("button", name=self.TERMS_OF_USE_CHECKBOX).click()
        
    def tap_submit(self):
        network_waits.wait_for_track(self.page)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.get_by_role("button", name=self.SUBMIT_BUTTON).click()
        try:
            self.page.wait_for_url(f"**/{self.SELECT_YOUR_PLAN_PAGE_URL_SUBSTRING}", timeout=5000)
        except Exception:
            if self.page.locator(self.FOOTER_NOTIFICATION_TOAST).is_visible(timeout=2000):
                self.page.get_by_role("button", name=self.SUBMIT_BUTTON).click()
            else:
                raise AssertionError("Navigation to select plan page failed and no toast footer was present after the initial submit.")