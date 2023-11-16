"""
Here the schema of the table from client has to be pasted
---

**TABLE NAME** Website Aggregates

**Schema**
    column_name : data_type
    
"""

from src.utils import generate_double_in_range, \
    generate_rand_from_choices, \
    get_structure_for_faker, \
    generate_date_between, \
    get_table_blueprint

from src.mock_data_generator import create_mock_data

from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

department_choices = [
    'Sales',
    'Marketing',
    'Finance',
    'Human Resources',
    'IT',
    'customer service',
    'Operations'
]

start_date = datetime.now().date() - timedelta(days=600)


def main():
    data_structure = {
        'first_name': ('VARCHAR(50)', fake.first_name),
        'last_name': ('VARCHAR(50)', fake.last_name),
        'joining_date': ('DATE', generate_date_between(start_date)),
        'salary': ('DECIMAL(10,2)', generate_double_in_range(1000, 10000)),
        'department': ('VARCHAR(50)', generate_rand_from_choices(department_choices))
    }
    return [{
        'column_blueprint': get_table_blueprint(data_structure),
        'fake_data_structure': get_structure_for_faker(data_structure)
    }]

# Only for testing


if __name__ == '__main__':
    records = main()
    for record in records:
        structure = record.get('fake_data_structure', {})
        print(create_mock_data(structure, 1))
