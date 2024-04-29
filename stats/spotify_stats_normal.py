from time import sleep
from typing import List, Dict


import requests

from spotify_auth import auth_header
from init import proxies, artist_page, base_url, cur, con


def album_ids():
    # album_id is final output of this function
    cur.execute('''
        CREATE TABLE IF NOT EXISTS albums_id (
            album_id TEXT PRIMARY KEY
        )
    ''')
 # ))))))))))))))))))))))))))))))))))
    # get all ids stored in database
    db_ids: list = []
    for row in cur.execute('''SELECT * FROM albums_id'''):
        db_ids.append(row[0])

    # this section finds all ids of albums of artists with artist's id
    resp_json: List[Dict] = []
    # TODO: shuffle this -> artist_page.items()
    for artist_id in list(artist_page.values()):
        url = f'{base_url}/artists/{artist_id}/albums?limit=50'
        response = requests.get(url, headers=auth_header, proxies=proxies)

        # TODO: replace this section
        # to avoiding spotify rate limit (status code 429)
        cool_down = response.headers.get('Retrying-After')
        if cool_down is not None:
            print(f'cool down for: {cool_down}')  # TODO: delete this later!
            sleep(int(cool_down) + 5)

        # check if there are artist's information in database
        first_id_albums = [new_id['id'] for new_id in response.json()['items']]
        print(f'first albums: {first_id_albums} len: {len(first_id_albums)}')
        unique_ids = [uid for uid in first_id_albums if uid not in db_ids]
        print(f'unique ids: {unique_ids} len: {len(unique_ids)}')
        if len(unique_ids) == len(first_id_albums):
            resp_json.append(response.json())
        elif len(unique_ids) < len(first_id_albums):
            for uid in unique_ids:
                cur.execute('''
                            INSERT OR IGNORE INTO albums_id VALUES (?)
                            ''', (uid,))
                con.commit()

    # this loop adds rest of albums for artists with more than 50 albums
    for albums in resp_json:
        if albums['next'] is not None:
            response = requests.get(
                albums['next'],
                headers=auth_header,
                proxies=proxies
            )
            # to avoiding spotify rate limit (status code 429)
            cool_down = response.headers.get('Retrying-After')
            if cool_down is not None:
                print(
                    f'cool down for: {cool_down}')  # TODO: delete this later!
                sleep(int(cool_down) + 5)
            resp_json.append(response.json())

    # this loop insert all albums ids into album_id table
    for album in resp_json:
        for i in range(0, len(album['items'])):
            album_id = album['items'][i]['id']
            cur.execute('''
                        INSERT OR IGNORE INTO albums_id VALUES (?)
                        ''', (album_id,))
            con.commit()
    con.close()


def main():
    album_ids()


if __name__ == '__main__':
    main()
# cur.execute('''
#     DELETE FROM albums WHERE artist='Shapur'
# ''')


# cur.execute('''
#     CREATE TABLE IF NOT EXISTS albums_id (
#         album_id TEXT PRIMARY KEY
#     )
# ''')
#
#
# sample_data = [
#     ('Fadaei', '5aWL79DpD45MzDMwCTZqsN'),
#     ('Shapur', '6kbLiMnkNZHlvMpTv5iK9h'),
#     ('Fadaei', '578d6XzxI0bCSi49dK0Qpx')
# ]

# for album_id in sample_data:
#     cur.execute('''
#         INSERT OR IGNORE INTO albums VALUES (?)
#     ''', (album_id,))
#
#
# con.commit()

# Print all records in the albums table
# for row in cur.execute('''SELECT * FROM albums'''):
#     print(row)
#
#
# con.close()
