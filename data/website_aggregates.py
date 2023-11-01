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


record = {
    'dt': fake.date,
    'customer_domain': fake.domain_name,
    'lead_domain':  fake.domain_name,
    'ip_country': generate_rand_null_with_prob(fake.country, 0.05),
    'no_of_visiting_ips': generate_int_in_range(0, 10000),
    'no_of_hits': generate_int_in_range(0, 100),
    'lead_domain_name': fake.company,
    'industry': generate_rand_from_choices(industry_choices),
    'estimated_num_employees': generate_int_in_range(1, 10000),
    'city': fake.city,
    'state': fake.state,
    'company_country': fake.country,
    'annual_revenue': generate_float_in_range(10000, 1000000),
    'total_funding': generate_float_in_range(10000, 1000000),
    'latest_funding_stage': generate_rand_from_choices(funding_stage_choices),
    'status': generate_rand_from_choices(status_choices),
    'decayed_inbound_score': generate_rand_null_with_prob(generate_double_in_range(end=1000), 0.1),
    'decayed_intent_score': generate_rand_null_with_prob(generate_double_in_range(end=1000), 0.1),
    'decayed_clubbed_score': generate_rand_null_with_prob(generate_double_in_range(end=1000), 0.1),
    'last_visit_date': fake.date,
    'employee_range': generate_int_range(100, 10000),
    'revenue_range':  generate_int_range(1000, 100000000)
}


def generate_fake_data(num_records=1):
    fake_data = []
    for _ in range(num_records):
        fake_record = {
            key: record[key]() for key in record.keys()
        }
        fake_data.append(fake_record)

    return fake_data