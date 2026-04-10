
from utils.generators import faker
import random
import string
from typing import Dict, Optional


def _random_digits(length: int = 10) -> str:
    return "".join(random.choice(string.digits) for _ in range(length))


def random_email(first_name: str, last_name: str, domain: str = "functionhealth.com") -> str:
    numeric = _random_digits(7)
    username = f"{first_name}.{last_name}+automationjebril{numeric}".lower()
    return f"{username}@{domain}"


def random_phone(country_code: str = "+1") -> str:
    return f"{country_code} {_random_digits(3)}-{_random_digits(3)}-{_random_digits(4)}"


def unique_password() -> str:
    return "12121212Aa"


def generate_member_data(overrides: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Return a valid member payload for signup or test data generation."""
    name = faker.fake_name()
    parts = name.split()
    first_name = parts[0] if len(parts) > 0 else "Test"
    last_name = parts[-1] if len(parts) > 1 else "User"
    member = {
        "name": name,
        "first_name": first_name,
        "last_name": last_name,
        "email": random_email(first_name, last_name),
        "address": faker.fake_address(),
        "phone_number": faker.fake_phone(),
        "dob": str(faker.fake_date_of_birth()),
        "password": unique_password(),
        "sex": faker.random_sex(),
        "zip_code": faker.generate_zip_code()
    }
    if overrides:
        member.update(overrides)
    return member
