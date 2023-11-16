
"""

1. Create a function named as 'add_mock_data_to_db'
2. The function should have 4 arguments - 
    1. Table Name - as a String
    2. Column Blueprint - as a String
    3. Fake Data Structure - as a Dictionary
    4. Count - as a Int (number)
3. Check whether the table exists using check_exists ( Refer database_connector help.txt ) for the syntax
4. If Table doesn't exists -> Create Table using 'create_table' , you will be using the table name and the column blueprint
5. If Table exists or if the table is created, Create the fake data from the fake data structure
    1. Looping over keys in the data structure
    eg: fake_data_structure = {
        name : fake.name
    }
    complete_fake_value = []
    for i in range(count):
        fake_data = {}
        for key in dict:
            value = dict[key]
            fake_value = value()
            fake_data[key] = fake_value

        complete_fake_value.append(fake_data)

6. Add this created 'complete_fake_value' to the database, For this you will be using a function called 'insert_rows'
        
"""

from src.database_connector import check_exists, create_table, insert_records


def create_mock_data(record: dict, count: int = 1):
    fake_data = []
    for _ in range(count):
        fake_record = {}
        for key, func in record.items():
            if func and not hasattr(func, 'generate_at_end'):
                fake_record[key] = func()
        for key, func in record.items():
            if func and hasattr(func, 'generate_at_end'):
                fake_record[key] = func(fake_record)
        fake_data.append(fake_record)

    return fake_data


def add_mock_data_to_db(table_name: str, col_blueprint: str, data_structure: dict, count: int):
    if not check_exists(table_name):
        create_table(table_name, col_blueprint)
        print(f'Created table {table_name}')
    mock_data = create_mock_data(data_structure, count)
    insert_records(table_name, mock_data)
    print(f'Inserted {count} rows')
