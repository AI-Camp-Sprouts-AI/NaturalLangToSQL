"""
Here the schema of the table from client has to be pasted
---

**TABLE NAME** Website Aggregates

**Schema**
    column_name : data_type
    
"""

from faker import Faker
import random

fake = Faker()
 
mock_data = {
        "dt": fake.date_this_decade(),
        "customer_domain": fake.domain_name(),
        "lead_domain": fake.domain_name(),
        "ip_country": fake.country(),
        "no_of_visiting_ips": random.randint(1, 100),
        "no_of_hits": random.randint(1, 1000),
        "lead_domain_name": fake.company(),
        "industry": fake.random_element(elements=("investment management", "consumer services", "hospitality", "information technology & services")),
        "estimated_num_employees": random.choice([None, 10, 1000, 3000]),
        "city": fake.city(),
        "state": fake.state(),
        "company_country": fake.country(),
        "latest_funding_stage": generate_funding_stage(),
        "status": fake.random_element(elements=("Qualified", "NA", "Disqualified", None)),
        "decayed_inbound_score": random.uniform(0, 1) if random.choice([True, False]) else None,
        "decayed_intent_score": random.uniform(0, 1) if random.choice([True, False]) else None,
        "decayed_clubbed_score": `random`.uniform(0, 1) if random.choice([True, False]) else None,
        "last_visit_date": fake.date_this_decade() if random.choice([True, False]) else None,
        "employee_range": generate_employee_range(),
        "revenue_range": generate_revenue_range(),
    }
    mock_data.append(entry)