# Take in the schema (JSON/plain string)
import pandas as pd
from faker import Faker

# Fake data generator
def fake_data(count):
    fake = Faker()
    data = []
    for it in range(count):
        entry = {'ID': fake.random_number(), 'Name': fake.name(), 'Country': fake.country(), 'DOB': fake.date_of_birth(),'Registered Phone Number': fake.phone_number(), 'Email': fake.email(), 'Timestamp': fake.time()}
        data.append(entry);
    return data

# Work in progress
def take_input():
    pass