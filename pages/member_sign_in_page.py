from pages.base_page import BasePage


class MemberSignInPage(BasePage):
    # Locators
    JOIN_LINK = "Join"

    def open(self, url: str):
        self.visit(url)

    def tap_join_link(self):
        self.page.get_by_role("link", name=self.JOIN_LINK).click()
