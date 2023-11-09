"""
Here the schema of the table from client has to be pasted
---

**TABLE NAME** Website Aggregates

**Schema**
    column_name : data_type
    
"""

import random
import sys
from faker import Faker

from src.mock_data_generator import add_mock_data_to_db

fake = Faker()

funding_stage_choices = [
    "Series E",
    "Other",
    "Seed",
    "None",
    "Equity Crowdfunding",
    "Series F",
    "Series C",
    "Series G",
    "Series D",
    "Convertible Note",
    "Angel",
    "Private Equity",
    "Venture (Round not Specified)",
    "Series H",
    "Debt Financing",
    "Series A",
    "Series B"
]

industry_choices = [
    "financial services",
    "healthcare",
    "retail",
    "manufacturing",
    "education",
    "media and entertainment",
    "real estate",
    "automotive",
    "energy",
    "telecommunications",
    "food and beverage",
    "sports and recreation",
    "fashion",
    "agriculture",
    "construction"
]

status_choices = [
    "Qualified",
    "NA",
    "Disqualified",
    "NULL"
]


def generate_rand_null_with_prob(generator, null_probability=0.5):
    weights = [1 - null_probability, null_probability]
    return lambda: random.choices([generator(), None], weights=weights, k=1)[0]


def generate_int_in_range(start=0, end=sys.maxsize):
    return lambda: random.randint(start, end)


def generate_float_in_range(start=0, end=sys.maxsize):
    return lambda: round(random.uniform(start, end), 2)


def generate_rand_from_choices(choices):
    return lambda: random.choice(choices)


def generate_double_in_range(start=0, end=sys.maxsize):
    return lambda: round(random.uniform(start, end), 4)


def generate_int_range(start=0, end=sys.maxsize):
    def generate_range():
        range_start = random.randint(start, end)
        range_end = random.randint(range_start, end)
        return f'{range_start} - {range_end}'
    return generate_range


def get_table_blueprint(data_structure):
    return ', '.join([
        f'{key} {data_structure[key][0]}' for key in data_structure.keys()
    ])


def get_structure_for_faker(data_structure):
    return {
        key: data_structure[key][1] for key in data_structure.keys()
    }

# fake.number -> Func instance
# fake.number() -> random number

# Follow this structure for custom fake functions
def custom_generator():
  def actual_function():
    # logic
    return random_value
  return actual_function

def main():
    data_structure = {
        'EmployeeID' : ('INT', fake.number),
        'FirstName' :('VARCHAR(50)', fake.first_name),
      
  
    }
    return {
        'column_blueprint': get_table_blueprint(data_structure),
        'fake_data_structure': get_structure_for_faker(data_structure)
    }
# Only for testing


def test_fake_data_generation(record, num_records=1):
    fake_data = []
    for _ in range(num_records):
        fake_record = {
            key: record[key]() for key in record.keys()
        }
        fake_data.append(fake_record)

    return fake_data


if __name__ == '__main__':
    record = main()
    add_mock_data_to_db(record)  # Just for testing
