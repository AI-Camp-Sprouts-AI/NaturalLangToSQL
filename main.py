#created using faker library and pandas
#if run, code is supposed to display a datatable

import pandas as pd
!pip install faker 
from faker import Faker
fake = Faker()


data = [{'ID': fake.random_number(), 'Name': fake.name(), 'Country': fake.country(), 'DOB': fake.date_of_birth(), 'Registered Phone Number': fake.phone_number(), 'Email': fake.email(), 'Timestamp': fake.time()},
         {'ID': fake.random_number(), 'Name': fake.name(), 'Country': fake.country(), 'DOB': fake.date_of_birth(), 'Registered Phone Number': fake.phone_number(), 'Email': fake.email(), 'Timestamp': fake.time()},
         {'ID': fake.random_number(), 'Name': fake.name(), 'Country': fake.country(), 'DOB': fake.date_of_birth(), 'Registered Phone Number': fake.phone_number(), 'Email': fake.email(), 'Timestamp': fake.time()},
         {'ID': fake.random_number(), 'Name': fake.name(), 'Country': fake.country(), 'DOB': fake.date_of_birth(), 'Registered Phone Number': fake.phone_number(), 'Email': fake.email(), 'Timestamp': fake.time()},
         {'ID': fake.random_number(), 'Name': fake.name(), 'Country': fake.country(), 'DOB': fake.date_of_birth(), 'Registered Phone Number': fake.phone_number(), 'Email': fake.email(), 'Timestamp': fake.time()]

df = pd.DataFrame.from_dict(data)
df
