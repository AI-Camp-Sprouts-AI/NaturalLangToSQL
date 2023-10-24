# Extremely basic SQL functions that haven't been tested
# Not sure if connection is properly maintained until end of application
# If I understand correctly, Python will close it automatically at end so no need to close conn or cur
# Please correct me if I'm (probably) wrong

"""
This file has to be used to create the connection to the database

This module should expose functions to
1. Create a Table
2. Add Rows to Database
3. Delete Rows from Database
4. Check whether the table exists
5. Run some select queries on the database


I leave the structure of this module implementation to the developer.

The database connection initialization has to be done within this module,
and that connection has to be maintained till the end of the application.

"""

import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def initialize_connection():
    # Load credentials from .env file
    params = {
      'dbname': os.environ.get('DB_NAME'),
      'user': os.environ.get('USER'),
      'password': os.environ.get('PASSWORD'),
      'host': os.environ.get('HOST'),
      'port': os.environ.get('PORT')
    }
    
    # Connect to the database
    conn = psycopg2.connect(**params)
    
    # Create a cursor
    cur = conn.cursor()

# Execute arbitrary PostgreSQL commands yourself
def execute_command(command):
    cur.execute(command)

# Fetch all and print results
def fetch_and_print():
    try:
        result = cur.fetchall()
        print(result)
    except:
        print("No results")

# Create new table with given column names
# Include datatype following column name
# Example: "COLUMN_NAME DATATYPE"
def create_table(table_name, *columns):
    column_names = ", ".join(columns)
    sql = f"CREATE TABLE {table_name} ({column_names});"
    cur.execute(sql)

# Delete an existing table by name
def drop_table(table_name):
    sql = f"DROP TABLE {table_name};"
    cur.execute(sql)

# Select columns by column name(s).
# If specifying filters, combine into one string and pass as argument
def select(table_name, *column_names, specifiers=None):
    sql = "SELECT " + ", ".join(column_names)
    if specifiers != None:
        sql += " FROM %s WHERE %s;" % table_name, specifiers
    else:
        sql += "FROM %s;" % table_name
    cur.execute(sql)

# Insert new records into an existing table
# records should be a dictionary of "column_name":"value"s
# Prefix the dictionary with two asterisks e.g. **my_dictionary
def insert_records(table_name, **records):
    columns = ", ".join(list(records.keys()))
    values = ", ".join(list(records.values()))
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
    cur.execute(sql)

# Delete records from an existing table
# Pass specifiers as a single combined string
# If specifiers is omitted, delete all records
def delete_records(table_name, specifiers=None):
    sql = f"DELETE FROM {table_name}" + ";" if specifiers==None else f"WHERE {specifiers};"
    cur.execute(sql)

initialize_connection()
fetch_and_print()