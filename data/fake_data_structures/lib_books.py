import random
import sys
from faker import Faker

from src.mock_data_generator import add_mock_data_to_db

fake = Faker()

book_choices = [
    "The Labyrinth of Lost Dreams",
    "Moonlit Melodies",
    "Shadows and Intrigue",
    "Digital Revolution: Navigating the Tech Landscape",
    "Economics Unraveled: Understanding the Global Marketplace",
    "Quantum Quandaries",
    "How to be a Logician",
    "This Statement is False",
    "Unveiling the Cosmos: A Journey through Space Exploration",
    "Serenade of the Silver Moon",
    "Angel",
    "Mindful Living: Cultivating Peace in a Busy World",
    "Sanctum Unveiled",
    "Aetherial Tides: Saga of the Starforged",
    "The Labyrinth of Lost Dreams",
    "Monkeys On a Typewriter",
    "The Bear and The Goose"
]

genre_choices = [
    "Science Fiction",
    "Historical Fiction",
    "Self-help",
    "Science",
    "History",
    "True Crime",
    "Fantasy",
    "Thriller",
    "Mystery",
    "Romance",
    "Comedy"
]

status_choices = [
    "available",
    "checked-out"
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
         'BookID' : ('INT', generate_int_in_range()),
         'BookName' : ('VARCHAR(50)', generate_rand_from_choices(book_choices)),
         'BookAuthor' : ('VARCHAR(50)', fake.name),
         'BookGenre' : ('VARCHAR(50)', generate_rand_from_choices(genre_choices)),
         'BookStatus' : ('VARCHAR(50)', generate_rand_from_choices(status_choices)),
         'CheckoutDate' : ('VARCHAR(50)', fake.date)
  
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
    output = main()
    record = output['fake_data_structure']
    print(test_fake_data_generation(record))
