
from src.database_connector import check_exists, create_table, insert_records


def create_mock_data(record: dict, count: int):
    fake_data = []
    for _ in range(count):
        fake_record = {
            key: record[key]() for key in record.keys()
        }
        fake_data.append(fake_record)

    return fake_data


def add_mock_data_to_db(table_name: str, col_blueprint: str, data_structure: dict, count: int):
    if not check_exists(table_name):
        create_table(table_name, col_blueprint)
        print(f'Created table {table_name}')
    else:
        mock_data = create_mock_data(data_structure, count)
        insert_records(table_name, mock_data)
        print(f'Inserted {count} rows')
