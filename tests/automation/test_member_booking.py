import pytest
from pages.member_join_page import MemberJoinPage
from pages.member_sign_in_page import MemberSignInPage
from pages.reserve_your_appointment import ReserveYourAppointmentPage
from pages.schedule_your_scan import ScheduleYourScanPage
from pages.select_your_plan_page import SelectYourPlanPage
from utils.config_loaders.config import MEMBER_URL
from utils.generators.member_generator import generate_member_data
from utils.test_data.card_data import CARD_TEST_DATA_DECLINED, CARD_TEST_DATA_SUCCESS
from utils.test_data.scan_packages import SCAN_PACKAGES


@pytest.fixture
def booking_setup(page):
    # Generate member test data
    member = generate_member_data()
    scan_package = SCAN_PACKAGES["mri_scan"]

    # # 1. Go to sign-up page
    member_sign_in_page = MemberSignInPage(page)        
    member_sign_in_page.open(MEMBER_URL)
    member_sign_in_page.tap_join_link()
    member_sign_in_page.accept_cookies_if_visible()

    # # 2. Fill member info and accept terms
    member_join_page = MemberJoinPage(page)
    member_join_page.fill_legal_first_name(member["first_name"])
    member_join_page.fill_legal_last_name(member["last_name"])
    member_join_page.fill_email(member["email"])
    member_join_page.fill_phone_number(member["phone_number"])
    member_join_page.fill_password(member["password"])
    member_join_page.accept_terms_and_conditions()
    member_join_page.tap_submit()

    # # 3. Select plan and continue
    select_your_plan_page = SelectYourPlanPage(page)
    select_your_plan_page.wait_for_select_your_plan_page()
    select_your_plan_page.fill_dob(member["dob"])
    select_your_plan_page.select_sex_at_birth(member["sex"])
    select_your_plan_page.select_scan(scan_package["name"])
    select_your_plan_page.tap_continue()

    # # 4. Choose center and appointment
    schedule_your_scan_page = ScheduleYourScanPage(page)
    schedule_your_scan_page.wait_for_schedule_your_scan_page()
    schedule_your_scan_page.select_random_location()
    schedule_your_scan_page.select_random_enabled_date(member)
    schedule_your_scan_page.select_random_time_slot(member)
    schedule_your_scan_page.tap_continue()

    yield member, scan_package

@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.P1
def test_verify_member_can_complete_booking_with_valid_card(page, booking_setup):
        """
        End-to-end: Member completes booking with valid card info
        """
        # # common setuup
        member, scan_package = booking_setup

        # # Generate test data
        card = CARD_TEST_DATA_SUCCESS["visa"]

        # # 5. Enter valid card payment details
        reserve_your_appointment_page = ReserveYourAppointmentPage(page)
        reserve_your_appointment_page.wait_for_reserve_your_appointment_page()
        reserve_your_appointment_page.assert_scan_price(scan_package["price"])
        reserve_your_appointment_page.fill_card_details(card_number=card["number"], expiration_date=card["expiration_date"], cvc=card["cvc"], zip_code=member["zip_code"])
        reserve_your_appointment_page.tap_continue()
        
        # # 6. Verify scan is confirmed
        reserve_your_appointment_page.verify_member_successfully_completed_booking(member)

        # # 7. Verify booking in internal hub portal
        # # This would have to be an Independent test case, where we submit this flow via api, than login to hub portal and do the verification


@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.P1
def test_verify_payment_is_declined_when_member_enters_invalid_card_payment_details(page, booking_setup):
        """
        End-to-end: Member attempts booking with invalid card info
        """
        # # common setuup
        member, scan_package = booking_setup

        # # Generate test data
        card = CARD_TEST_DATA_DECLINED["generic_decline"]

        # # 5. Enter declined card payment details
        reserve_your_appointment_page = ReserveYourAppointmentPage(page)
        reserve_your_appointment_page.wait_for_reserve_your_appointment_page()
        reserve_your_appointment_page.assert_scan_price(scan_package["price"])
        reserve_your_appointment_page.fill_card_details(card_number=card["number"], expiration_date=card["expiration_date"], cvc=card["cvc"], zip_code=member["zip_code"])
        reserve_your_appointment_page.tap_continue()
        reserve_your_appointment_page.verify_payment_declined(card["error_description"])
        