from datetime import datetime

from playwright.sync_api import Page, expect


class BasePage:

    ACCEPT_COOKIES = "button[data-tid='banner-accept']"

    def __init__(self, page: Page):
        self.page = page

    def visit(self, url: str):
        self.page.goto(url)
        self.accept_cookies_if_visible()

    def accept_cookies_if_visible(self):
        accept_button = self.page.locator(self.ACCEPT_COOKIES)
        if accept_button.is_visible():
            accept_button.click()

    def to_abbr_month(self, date_str):
        dt = datetime.strptime(date_str, "%B %d, %Y")
        return dt.strftime("%b %d, %Y")

    def click_button(self, name: str):
        self.page.get_by_role("button", name=name).click()

    def expect_text_visible(self, text: str):
        expect(self.page.get_by_text(text)).to_be_visible()
