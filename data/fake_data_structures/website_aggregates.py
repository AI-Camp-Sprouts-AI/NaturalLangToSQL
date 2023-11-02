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


def main():
    data_structure = {
        'dt': ('DATE', fake.date),
        'customer_domain': ('VARCHAR(255)', fake.domain_name),
        'lead_domain': ('VARCHAR(255)', fake.domain_name),
        'ip_country': ('VARCHAR(255)', generate_rand_null_with_prob(fake.country, 0.05)),
        'no_of_visiting_ips': ('BIGINT', generate_int_in_range(0, 10000)),
        'no_of_hits': ('BIGINT', generate_int_in_range(0, 100)),
        'lead_domain_name': ('VARCHAR(255)', fake.company),
        'industry': ('VARCHAR(255)', generate_rand_from_choices(industry_choices)),
        'estimated_num_employees': ('INTEGER', generate_int_in_range(1, 10000)),
        'city': ('VARCHAR(255)', fake.city),
        'state': ('VARCHAR(255)', fake.state),
        'company_country': ('VARCHAR(255)', fake.country),
        'annual_revenue': ('DOUBLE PRECISION', generate_float_in_range(10000, 1000000)),
        'total_funding': ('DOUBLE PRECISION', generate_float_in_range(10000, 1000000)),
        'latest_funding_stage': ('VARCHAR(255)', generate_rand_from_choices(funding_stage_choices)),
        'status': ('VARCHAR(255)', generate_rand_from_choices(status_choices)),
        'decayed_inbound_score': ('DOUBLE PRECISION', generate_rand_null_with_prob(generate_double_in_range(end=1000), 0.1)),
        'decayed_intent_score': ('DOUBLE PRECISION', generate_rand_null_with_prob(generate_double_in_range(end=1000), 0.1)),
        'decayed_clubbed_score': ('DOUBLE PRECISION', generate_rand_null_with_prob(generate_double_in_range(end=1000), 0.1)),
        'last_visit_date': ('DATE', fake.date),
        'employee_range': ('VARCHAR(255)', generate_int_range(100, 10000)),
        'revenue_range': ('VARCHAR(255)', generate_int_range(1000, 100000000))
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
