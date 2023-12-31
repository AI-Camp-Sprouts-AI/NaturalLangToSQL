# Functions to interact with postgreSQL database
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
from psycopg2 import sql
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def init_connection(params=None):
    if params is None:
        params = {
            'dbname': os.environ.get("DB_NAME"),
            'user': os.environ.get("USERNAME"),
            'password': os.environ.get("PASSWORD"),
            'host': os.environ.get("HOST"),
            'port': os.environ.get("PORT")
        }
    # Connect to the database
    conn = psycopg2.connect(**params)
    # Execute all statements without needing to call commit()
    conn.autocommit = True
    # Create a cursor
    cur = conn.cursor()
    return conn, cur


def connect_and_execute_command(params, command):
    connection, cursor = init_connection(params)
    result = None
    # print("\n[DEBUG] - Command: %s" % command)
    try:
        cursor.execute(command)
    except Exception as e:
        print("Error in Execution", e)
    try:
        result = cursor.fetchall()
    except Exception as e:
        print("Error in Fetch : ", e)
    cursor.close()
    return result


def execute_command(command):
    conn, cur = init_connection()
    result = None
    # print("\n[DEBUG] - Command: %s" % command)
    try:
        cur.execute(command)
    except Exception as e:
        print("Error in Execution", e)
    try:
        result = cur.fetchall()
    except Exception as e:
        print("Error in Fetch : ", e)
    return result

# Create new table with given column names
# Include datatype following column name
# Example: "COLUMN_NAME DATATYPE"
# Specify schema with table_name (i.e. schema.table)


def create_table(table_name, *columns):
    conn, cur = init_connection()
    with conn:
        with conn.cursor() as cursor:
            column_names = ", ".join(columns)
            sql = f"CREATE TABLE {table_name} ({column_names});"
            cur.execute(sql)

# Delete an existing table by name


def drop_table(table_name):
    conn, cur = init_connection()
    with conn:
        with conn.cursor() as cursor:
            sql = f"DROP TABLE {table_name};"
            cur.execute(sql)

# Select columns by column name(s).
# column_names is a list of column names to be retrieved
# selectors is an optional dictionary where value in key-value is either a value to match against or a tuple
# first element of tuple is the operator (<,>,!=,BETWEEN,IN,etc) and second element is value


def select(table_name, column_names, selectors=None):
    conn, cur = init_connection()
    with conn:
        with conn.cursor() as cursor:
            columns = sql.SQL(", ").join(sql.Identifier(col)
                                         for col in column_names)
            table = sql.Identifier(table_name)
            query = sql.SQL("SELECT {columns} FROM {table}").format(
                columns=columns, table=table)

            # If selectors are provided, add them to the query using the WHERE clause
            if selectors:
                conditions = []
                parameters = []
                for key, value in selectors.items():
                    # Check if the value is a tuple of two elements
                    if isinstance(value, tuple) and len(value) == 2:
                        # If so, use the first element as the operator and the second element as the parameter
                        operator = value[0]
                        parameter = value[1]
                    else:
                        # Otherwise, use "=" as the default operator and the value as the parameter
                        operator = "="
                        parameter = value
                    conditions.append(sql.Composed(
                        [sql.Identifier(key), sql.SQL(operator), sql.Placeholder()]))
                    parameters.append(parameter)

                conditions = sql.SQL(" AND ").join(conditions)
                query = query + \
                    sql.SQL(" WHERE {conditions}").format(
                        conditions=conditions)

            cursor.execute(query, parameters if selectors else None)
            results = cursor.fetchall()

            return [dict(zip(column_names, row)) for row in results]

# Insert new records into an existing table
# records is a list of dictionaries containing key-values representing column_name:value
# each dictionary in the list is a new record


def insert_records(table_name, records):
    conn, cur = init_connection()
    with conn:
        with conn.cursor() as cursor:
            columns = sql.SQL(", ").join(sql.Identifier(col)
                                         for col in records[0].keys())
            values = sql.SQL(", ").join(sql.Placeholder()
                                        for _ in records[0].values())
            table = sql.Identifier(table_name)
            query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values});").format(
                table=table, columns=columns, values=values)
            try:
                cursor.executemany(query, [list(record.values())
                                           for record in records])
            except Exception as e:
                print('Error occured', e)

# Delete records from an existing table
# selectors is a dictionary where values of key-value is the value to match against or a tuple where the first element is an operator (<,>,!=,BETWEEN, IN, etc) and the second is what to evaluate
# If selector is omitted, delete all records


def delete_records(table_name, selectors=None):
    conn, cur = init_connection()
    with conn:
        with conn.cursor() as cursor:
            table = sql.Identifier(table_name)
            query = sql.SQL("DELETE FROM {table}").format(table=table)

            # If selectors are provided, add them to the query using the WHERE clause
            if selectors:
                conditions = []
                parameters = []
                for key, value in selectors.items():
                    # Check if the value is a tuple of two elements
                    if isinstance(value, tuple) and len(value) == 2:
                        # If so, use the first element as the operator and the second element as the parameter
                        operator = value[0]
                        parameter = value[1]
                    else:
                        # Otherwise, use "=" as the default operator and the value as the parameter
                        operator = "="
                        parameter = value
                    conditions.append(sql.Composed(
                        [sql.Identifier(key), sql.SQL(operator), sql.Placeholder()]))
                    parameters.append(parameter)
                conditions = sql.SQL(" AND ").join(conditions)
                query = query + \
                    sql.SQL(" WHERE {conditions}").format(
                        conditions=conditions)
            cursor.execute(query, parameters if selectors else None)
            count = cursor.rowcount
            return count

# Check if table exists


def check_exists(table_name):
    conn, cur = init_connection()
    with conn:
        with conn.cursor() as cursor:
            table = sql.Literal(table_name)
            query = sql.SQL(
                "SELECT * FROM information_schema.tables WHERE table_name = {table};").format(table=table)
            try:
                cursor.execute(query)
                result = cursor.fetchone()
            except Exception as e:
                result = False
                print(e)
            # Return True if result is not None, False otherwise
            return bool(result)


# print(execute_command("SELECT no_of_visiting_ips FROM website_aggregates WHERE customer_domain = 'hardy.net' or customer_domain = 'brown.com';"))
