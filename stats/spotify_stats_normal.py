from typing import List, Dict, Tuple

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

    # this section finds all ids of albums of artists with artist's id
    resp_json: List[Dict] = []
    # TODO: shuffle this -> artist_page.items()
    for artist_id in list(artist_page.values()):
        url = f'{base_url}/artists/{artist_id}/albums?limit=50'
        response = requests.get(url, headers=auth_header, proxies=proxies)
        resp_json.append(response.json())

    # this loop adds rest of albums for artists with more than 50 albums
    for albums in resp_json:
        if albums['next'] is not None:
            response = requests.get(
                albums['next'],
                headers=auth_header,
                proxies=proxies
            )
            resp_json.append(response.json())

    # this loop inserts all albums ids into album_id table
    id_list_for_query: List[Tuple] = []
    for album in resp_json:
        for i in range(0, len(album['items'])):
            id_list_for_query.append((album['items'][i]['id'],))

    cur.executemany('''
        INSERT OR IGNORE INTO albums_id (album_id) VALUES (?)
        ''', id_list_for_query)
    con.commit()


def all_tracks():
    # creating table tracks_id to save track_id tracks_name and release_date
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tracks_id (
        track_id TEXT PRIMARY KEY,
        track_name TEXT,
        release_date TEXT
        )
    ''')

    album_ids_list: List[str] = []
    albums_jsons: List[Dict] = []
    id_list_for_query: List[Tuple] = []
    # reading albums ids from database
    for row in cur.execute('''SELECT * FROM albums_id'''):
        album_ids_list.append(row[0])

    for i in range(0, len(album_ids_list), 20):
        album_id_20_string = ','.join(album_ids_list[i: i + 20])
        url = f'{base_url}/albums?ids={album_id_20_string}'
        response = requests.get(url, headers=auth_header, proxies=proxies)
        albums_jsons.append(response.json()['albums'])

    for album_20 in albums_jsons:
        for album in album_20:
            release_date = album['release_date']
            for track in range(0, len(album['tracks']['items'])):
                name = album['tracks']['items'][track]['name']
                track_id = album['tracks']['items'][track]['id']
                id_list_for_query.append((track_id, name, release_date))

    cur.executemany('''
        INSERT OR IGNORE INTO tracks_id (track_id, track_name, release_date)
        VALUES (?, ?, ?)''', id_list_for_query)
    con.commit()



def main():
    # album_ids()
    all_tracks()


if __name__ == '__main__':
    main()
    con.close()
