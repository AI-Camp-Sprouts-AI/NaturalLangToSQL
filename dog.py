from faker import Faker
import random

fake = Faker()

def generate_fake_dog_data(num_records):
    fake_data = []
    for _ in range(num_records):
        record = {
            'dog_weight': round(random.uniform(5.0, 100.0), 2),
            'dog_name': fake.name(),
            'dog_country': fake.country(),
            'owner_name': fake.name(),
            'dog_age': random.randint(1, 17)
        }
        fake_data.append(record)
    return fake_data

# Generate 10 fake dog records
fake_dog_data = generate_fake_dog_data(10)
print(fake_dog_data)
