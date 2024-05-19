import os
from sys import exit
import csv
import sqlite3


"""
This script converts SQLite database tables to CSV files.
The database file is assumed to be named 'RapGoat.db' and located in the
current working directory. The CSV files will be saved in a 'CSV' subdirectory
within the current working directory."""


def get_database_dir() -> str:
    """
    Get the directory of the database file.
    :return:
        str: The absolute path to the database file."""

    path = os.getcwd()
    database_dir = os.path.join(path, 'RapGoat.db')
    return database_dir


def check_database(db_dir: str) -> None:
    """Check if the database file exists in the specified directory."""
    if not os.path.isfile(db_dir):
        print('There is no such database in this directory!')
        exit(1)


def convertor(database_dir: str) -> None:
    """
    Convert the database tables to CSV files.
    :arg:
        database_dir (str): The path to the database file.
    :raise:
        SystemExit: If database connection or data export fails."""

    check_database(database_dir)

    try:
        con = sqlite3.connect(database_dir)
        cur = con.cursor()
    except sqlite3.DatabaseError as e:
        print(f'Data base connection was unsuccessful > {e}')
        exit(1)
    else:
        # table_list includes all table name that includes in our database
        table_list = get_table_names(cur)

    for table in table_list:
        table_name = table[0]
        try:
            cur.execute(f'''
                    SELECT * FROM {table_name}
                ''')
            all_data = cur.fetchall()
        except sqlite3.DatabaseError as e:
            print(f'Data Export from {table_name} was unsuccessful > {e}')
            exit(1)
        else:
            '''According to PEP 249, this read-only attribute is a sequence of 
            7-items sequences. Each of these sequences contains information
            describing one result column. Here we need just "name". 
            name,type_code,display_size,internal_size,precision,scale,null_ok
            '''
            table_headers: list[str] = [desc[0] for desc in cur.description]

        '''Creates CSV folder in this place, if it not exists'''
        this_dir: str = os.getcwd()
        if not os.path.exists(this_dir + '/CSV'):
            print(f'Such a directory did not exist.\nNow is created...')
            csv_dir: str = os.path.join(this_dir, 'CSV')
            os.mkdir(csv_dir)

        '''Defines name of .csv file and opens it to write data in it'''
        csv_file_dir: str = this_dir + f'/CSV/{table_name}.csv'
        try:
            with open(csv_file_dir, 'w', newline='') as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=',', lineterminator='\r\n',
                    quoting=csv.QUOTE_ALL, escapechar='\\')
                writer.writerow(table_headers)
                # Replace not exist values with null instead of empty string
                for row in all_data:
                    data_with_none = [
                        'NULL' if value is None else value for value in row
                    ]
                    writer.writerow(data_with_none)
        except IOError as e:
            print(f'convertor > {e}')
        else:
            print('Data export was successful.')

    con.close()


def get_table_names(cur: sqlite3.Cursor) -> list:
    """
    Retrieve the list of table names in the database.
    :arg:
        cur (sqlite3.Cursor): The database cursor.
    :return:
        list: A list of table names.
    :raise:
        SystemExit: If fetching table names fails."""

    try:
        cur.execute('''
            SELECT name FROM sqlite_master WHERE type='table';
        ''')
    except sqlite3.Error as e:
        print(f'get_table_name > failed to retrieve table names > {e}')
        exit(1)
    else:
        return cur.fetchall()


def main():
    """The main function to execute the database to CSV conversion process."""
    database_dir = get_database_dir()
    convertor(database_dir)
