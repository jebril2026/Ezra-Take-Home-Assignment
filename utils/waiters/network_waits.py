"""
Utilities for waiting on specific network responses in Playwright tests.
"""

def wait_for_month_availability(page, timeout=15000):
    """Wait for the /availability/scan/bymonth endpoint to return a 200 response."""
    page.wait_for_event(
        "response",
        predicate=lambda r: (
            "/packages/api/availability/scan/bymonth" in r.url and
            r.status == 200
        ),
        timeout=timeout,
    )

def wait_for_booking_locations(page, timeout=10000):
    """Wait for the /centers endpoint to return a 200 response."""
    page.wait_for_event(
        "response",
        predicate=lambda r: (
            "/packages/api/package/" in r.url
            and r.url.endswith("/centers")
            and r.status == 200
        ),
        timeout=timeout,
    )

def wait_for_track(page, timeout=10000):
    page.wait_for_event(
        "response",
        predicate=lambda r: "/track" in r.url and r.status == 200,
        timeout=timeout,
    )
