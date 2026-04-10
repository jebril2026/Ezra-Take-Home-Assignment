from faker import Faker
from datetime import date, timedelta
import random

fake = Faker()

def fake_name():
    return fake.name()

def fake_email():
    return fake.email()

def fake_address():
    return fake.address().replace('\n', ', ')

def fake_phone():
    phone = fake.numerify("+1-###-###-####")
    return phone

def fake_date_of_birth():
    today = date.today()
    min_age = 18
    max_age = 80
    start_date = today - timedelta(days=365 * max_age)
    end_date = today - timedelta(days=365 * min_age)
    dob = fake.date_between(start_date=start_date, end_date=end_date)
    return dob.strftime("%m-%d-%Y")

def random_sex():
    return random.choice(["Male", "Female"])

def generate_zip_code():
    return fake.zipcode()
