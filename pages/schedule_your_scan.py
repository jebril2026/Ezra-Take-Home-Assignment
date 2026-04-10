from pages.base_page import BasePage
import re
import random
import utils.waiters.network_waits as network_waits

class ScheduleYourScanPage(BasePage):

    DOB_INPUT = "#dob"
    LOCATION_CARDS = ".location-card"
    CALENDAR_TITLE = ".calendar-title"
    DATE_PICKER_ENABLED_DAYS = ".vuecal__cell:not(.vuecal__cell--disabled):not(.vuecal__cell--out-of-scope)"
    DATE_PICKER_RIGHT_ARROW = ".icon__arrow:not(.icon__arrow--left)"
    APPOINTMENT_SLOTS = ".appointments__individual-appointment"
    CONTINUE_BUTTON = "[data-test='submit']"
    SCHEDULE_YOUR_SCAN_PAGE_URL_SUBSTRING = "sign-up/schedule-scan"

    def wait_for_schedule_your_scan_page(self):
        self.page.wait_for_url(f"**/{self.SCHEDULE_YOUR_SCAN_PAGE_URL_SUBSTRING}", timeout=15000)

    def select_random_location(self):
        network_waits.wait_for_booking_locations(self.page)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_selector(self.LOCATION_CARDS, state="visible", timeout=5000)
        locations = self.page.locator(self.LOCATION_CARDS).filter(visible=True)
        count = locations.count()
        if count == 0:
            raise Exception("No visible locations found!")
        recommended = locations.get_by_text("Recommended")
        if recommended.count() > 0:
            recommended.first.click()
            return
        random_index = random.randint(0, count - 1)
        locations.nth(random_index).click()
    
    
    def select_random_enabled_date(self, member):
        network_waits.wait_for_month_availability(self.page)
        self.page.wait_for_selector(self.DATE_PICKER_ENABLED_DAYS, state="visible", timeout=5000)
        for _ in range(3):
            enabled_dates = self.page.locator(self.DATE_PICKER_ENABLED_DAYS).filter(visible=True)
            count = enabled_dates.count()
            if count > 0:
                random_index = random.randint(0, count - 1)
                date_cell = enabled_dates.nth(random_index)
                day_text = date_cell.inner_text().strip()
                day_number = re.search(r"\d+", day_text)
                if day_number:
                    day_number = day_number.group()
                else:
                    raise Exception(f"Could not extract day from cell text: {day_text}")
                month_year = self.page.locator(self.CALENDAR_TITLE).inner_text().strip()
                month, year = month_year.split()
                full_date = f"{month} {day_number}, {year}"
                if member is not None:
                    member["appointment_date"] = full_date
                date_cell.click()
                return
            self.page.locator(self.DATE_PICKER_RIGHT_ARROW).filter(visible=True).click()
        raise Exception("No enabled dates found in any month!")


    def select_random_time_slot(self, member):
        network_waits.wait_for_track(self.page)
        self.page.wait_for_load_state("domcontentloaded")
        time_slots = self.page.locator(self.APPOINTMENT_SLOTS).filter(visible=True)
        count = time_slots.count()
        if count == 0:
            raise Exception("No visible time slots found!")
        random_index = random.randint(0, count - 1)
        time_tile = time_slots.nth(random_index)
        time_text = time_tile.inner_text().strip()
        if member is not None:
            member["appointment_time"] = time_text
        time_tile.click()

    def tap_continue(self):
        self.page.locator(self.CONTINUE_BUTTON).click()
