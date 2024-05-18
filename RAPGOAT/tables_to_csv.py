import os
from sys import exit
import csv
import sqlite3


def get_database_dir() -> str:
    path = os.getcwd()
    database_dir = path + '/RapGoat.db'
    return database_dir


def check_database(db_dir: str):
    if not os.path.isfile(db_dir):
        print('There is no such database in this directory!')
        exit(1)


def fetch_all(db_dir: str):
    try:
        con = sqlite3.connect(db_dir)
        cur = con.cursor()
    except sqlite3.DatabaseError as e:
        print(f'Data base connection was unsuccessful: {e}')
        exit(1)

    # try:
    #     cur.execute('''
    #             SELECT track_id, track_name, release_date, duration_ms,
    #             popularity, cover_album, artists_names, artists_ids
    #             FROM track_details
    #         ''')
    #     all_data = cur.fetchall()
    # except sqlite3.DatabaseError as e:
    #     print(f'Data Export was unsuccessful: {e}')
    #     exit(1)
    # else:
    #     table_headers: list[str] = [desc[0] for desc in cur.description]

    try:
        cur.execute('''
                SELECT page_url, page_name, followers, followings, 
                tracks, avatar_url
                FROM soundcloud_artist
            ''')
        all_data = cur.fetchall()
    except sqlite3.DatabaseError as e:
        print(f'Data Export was unsuccessful: {e}')
        exit(1)
    else:
        table_headers: list[str] = [desc[0] for desc in cur.description]

    this_dir: str = os.getcwd()
    if not os.path.exists(this_dir + '/CSV'):
        csv_path: str = os.path.join(this_dir, 'CSV')
        os.mkdir(csv_path)
    csv_file_dir: str = this_dir + '/CSV/soundcloud_artist.csv'
    with open(csv_file_dir, 'w', newline='') as csvfile:
        writer = csv.writer(
            csvfile, delimiter=',', lineterminator='\r\n',
            quoting=csv.QUOTE_ALL, escapechar='\\')
        writer.writerow(table_headers)
        writer.writerows(all_data)

    print('Data export was successful')
    con.close()


def main():
    # get database directory
    db_dir: str = get_database_dir()
    # checks if database exists
    check_database(db_dir)
    # create connection to database and fetch all data and calls save_to_csv()
    fetch_all(db_dir)
