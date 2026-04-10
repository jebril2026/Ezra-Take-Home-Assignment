from pages.base_page import BasePage

class ReserveYourAppointmentPage(BasePage):

    CONTINUE_BUTTON = "[data-test='submit']"
    CARD_NUMBER_INPUT = "#payment-numberInput"
    EXPIRATION_DATE_INPUT = "#payment-expiryInput"
    CVC_INPUT = "#payment-cvcInput"
    ZIP_CODE_INPUT = "#payment-postalCodeInput"
    SCAN_PRICE_TEXT = ".pricing-detail .h4"
    STRIPE_IFRAME = 'iframe[title="Secure payment input frame"]'
    SCAN_CONFIRMATION_PAGE_URL_SUBSTRING = "sign-up/scan-confirm"
    SCAN_CONFIRMATION_TILE = ".scan-details"
    RESERVE_YOUR_APPOINTMENT_PAGE_URL_SUBSTRING = "sign-up/reserve-appointment"
    PAYMENT_DECLINED_ERROR_MESSAGE = "#Field-numberError"

    def wait_for_reserve_your_appointment_page(self):
        self.page.wait_for_url(f"**/{self.RESERVE_YOUR_APPOINTMENT_PAGE_URL_SUBSTRING}", timeout=15000)

    def fill_card_details(self, card_number, expiration_date, cvc, zip_code):
        self.page.wait_for_load_state("domcontentloaded")
        frame = self.page.frame_locator(self.STRIPE_IFRAME).first
        frame.locator(self.CARD_NUMBER_INPUT).fill(card_number)
        frame.locator(self.EXPIRATION_DATE_INPUT).fill(expiration_date)
        frame.locator(self.CVC_INPUT).fill(cvc)
        frame.locator(self.ZIP_CODE_INPUT).fill(zip_code)

    def assert_scan_price(self, expected_price: str):
        price_locator = self.page.locator(self.SCAN_PRICE_TEXT)
        price_locator.wait_for(state="visible", timeout=5000)
        actual_price = price_locator.inner_text().strip()
        assert actual_price == expected_price, f"Expected scan price '{expected_price}', but got '{actual_price}'"

    def tap_continue(self):
        self.page.locator(self.CONTINUE_BUTTON).click()

    def verify_member_successfully_completed_booking(self, member):
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_url(f"**/{self.SCAN_CONFIRMATION_PAGE_URL_SUBSTRING}", timeout=15000)
        assert self.SCAN_CONFIRMATION_PAGE_URL_SUBSTRING in self.page.url, f"Expected to be on scan confirmation page, but URL is: {self.page.url}"
        scan_details = self.page.locator(self.SCAN_CONFIRMATION_TILE)
        scan_details.wait_for(state="visible", timeout=5000)
        assert scan_details.is_visible(), "Scan details are not visible on the confirmation page."
        scan_details_text = scan_details.inner_text()
        abbr_appointment_date = self.to_abbr_month(member["appointment_date"])
        assert abbr_appointment_date in scan_details_text, f"Expected date '{member['appointment_date']}' not found in scan details: {scan_details_text}"
        assert member["appointment_time"] in scan_details_text, f"Expected time '{member['appointment_time']}' not found in scan details: {scan_details_text}"

    def verify_payment_declined(self, expected_error_message):
        frame = self.page.frame_locator(self.STRIPE_IFRAME).first
        error_locator = frame.locator(self.PAYMENT_DECLINED_ERROR_MESSAGE)
        error_locator.wait_for(state="visible", timeout=10000)
        assert error_locator.is_visible(), f"Expected error message '{expected_error_message}' not visible on the page."
        actual_error_message = error_locator.inner_text().strip()
        assert actual_error_message == expected_error_message, f"Expected error message '{expected_error_message}', but got '{actual_error_message}'"
