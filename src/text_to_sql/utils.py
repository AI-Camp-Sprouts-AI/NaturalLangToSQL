import random
import sys
import hashlib
from faker import Faker
from datetime import datetime
fake = Faker()


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
    has_id = check_for_id(data_structure)
    auto_id_generate_string = 'ID SERIAL PRIMARY KEY,'
    return ('' if has_id else auto_id_generate_string) + ' ,'.join([
        f'{key} {data_structure[key][0]}' for key in data_structure.keys()
    ])


def get_structure_for_faker(data_structure):
    return {
        key: data_structure[key][1] for key in data_structure.keys()
    }


def generate_date_between(start, end=datetime.now().date()):

    def generate_date():
        return fake.date_between(start, end)

    return generate_date


def generate_at_end(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.generate_at_end = True
    return wrapper


def generate_using(func, *keys):
    @generate_at_end
    def construct(src):
        return func(*[src.get(key, None) for key in keys])
    return construct


def hash_fun(*args):
    value = ''.join(filter(lambda x: x, args))
    return hashlib.sha256(value.encode()).hexdigest()


def generate_closure(func, *args):
    def closure():
        return func(*[arg() for arg in args])
    return closure


def check_for_id(object):
    return any('_id' in key or key == 'id'for key in object)
