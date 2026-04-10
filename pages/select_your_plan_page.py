from pages.base_page import BasePage

class SelectYourPlanPage(BasePage):

    SELECT_YOUR_PLAN_PAGE_URL_SUBSTRING = "sign-up/select-plan"
    DOB_INPUT = "#dob"
    SUBMIT_BUTTON = "Submit"
    SEX_AT_BIRTH_DROPDOWN = ".multiselect__tags"
    SCAN_PLAN_TILES = ".encounter-card__title-container"
    CONTINUE_BUTTON = "select-plan-submit-btn"

    def wait_for_select_your_plan_page(self):
        self.page.wait_for_url(f"**/{self.SELECT_YOUR_PLAN_PAGE_URL_SUBSTRING}", timeout=10000)

    def fill_dob(self, dob: str):
        self.page.locator(self.DOB_INPUT).fill(dob)

    def tap_submit(self):
        self.page.get_by_role("button", name=self.SUBMIT_BUTTON).click()

    def select_sex_at_birth(self, sex: str):
        self.page.locator(self.SEX_AT_BIRTH_DROPDOWN).click()
        self.page.get_by_text(sex).first.click()

    def select_scan(self, scan_name: str):
        self.page.locator(self.SCAN_PLAN_TILES, has=self.page.get_by_text(scan_name, exact=True)).click()

    def tap_continue(self):
        self.page.get_by_test_id(self.CONTINUE_BUTTON).click()
