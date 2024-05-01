from typing import List, Dict, Tuple

import requests

from spotify_auth import auth_header
from init import proxies, artist_page, base_url, cur, con


def albums_details():
    # album_id is final output of this function
    cur.execute('''
        CREATE TABLE IF NOT EXISTS albums_details (
            album_id TEXT PRIMARY KEY,
            album_name TEXT,
            total_tracks TEXT,
            release_date TEXT,
            album_type TEXT,
            artist_names TEXT, 
            artist_ids TEXT,
            cover TEXT
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
            album_id = album['items'][i]['id']
            album_name = album['items'][i]['name']
            total_tracks = album['items'][i]['total_tracks']
            release_date = album['items'][i]['release_date']
            album_type = album['items'][i]['album_type']
            cover = album['items'][i]['images'][0]['url']
            artist_names: List['str'] = []
            artist_ids: List['str'] = []
            for artist in album['items'][i]['artists']:
                artist_names.append(artist['name'])
                artist_ids.append(artist['id'])

            id_list_for_query.append(
                (album_id,
                 album_name,
                 total_tracks,
                 release_date,
                 album_type,
                 ','.join(artist_names),
                 ','.join(artist_ids),
                 cover
                 )
            )

    cur.executemany('''
        INSERT OR IGNORE INTO albums_details (
            album_id, 
            album_name, 
            total_tracks, 
            release_date, 
            album_type, 
            artist_names, 
            artist_ids,
            cover) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
    albums_json: List[Dict] = []
    id_list_for_query: List[Tuple] = []
    # reading albums ids from database
    for row in cur.execute('''SELECT * FROM albums_details'''):
        album_ids_list.append(row[0])

    for i in range(0, len(album_ids_list), 20):
        album_id_20_string = ','.join(album_ids_list[i: i + 20])
        url = f'{base_url}/albums?ids={album_id_20_string}'
        response = requests.get(url, headers=auth_header, proxies=proxies)
        albums_json.append(response.json()['albums'])

    for twenty_albums in albums_json:
        for album in twenty_albums:
            release_date = album['release_date']
            if album['tracks']['next'] is not None:
                next_tracks_url = album['tracks']['next']
                next_response = requests.get(
                    next_tracks_url,
                    headers=auth_header,
                    proxies=proxies)
                albums_json.append(next_response.json()['albums'])
            for track in range(0, len(album['tracks']['items'])):
                name = album['tracks']['items'][track]['name']
                track_id = album['tracks']['items'][track]['id']
                id_list_for_query.append((track_id, name, release_date))

    cur.executemany('''
        INSERT OR IGNORE INTO tracks_id (track_id, track_name, release_date)
        VALUES (?, ?, ?)''', id_list_for_query)
    con.commit()


def track_details():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS track_details (
            track_id TEXT PRIMARY KEY,
            track_name TEXT,
            release_date TEXT,
            duration_ms INTEGER,
            popularity INTEGER,
            cover_album TEXT,
            artists_names TEXT,
            artists_ids TEXT
        )
    ''')

    track_id_list: List[str] = []
    tracks_json: List[Dict] = []
    for row in cur.execute('''SELECT * FROM tracks_id'''):
        track_id_list.append(row[0])

    for i in range(0, len(track_id_list), 50):
        track_id_50_string = ','.join(track_id_list[i: i + 50])
        url = f'{base_url}/tracks?ids={track_id_50_string}'
        response = requests.get(url, headers=auth_header, proxies=proxies)
        tracks_json.append(response.json()['tracks'])

    track_details_for_query: List[Tuple] = []
    for fifty_track in tracks_json:
        for track in fifty_track:
            track_id = track['id']
            track_name = track['name']
            release_date = track['album']['release_date']
            duration_ms = track['duration_ms']
            popularity = track['popularity']
            cover_album = track['album']['images'][0]['url']
            artists_names: List[str] = []
            artists_ids: List[str] = []
            for artist_name in track['artists']:
                artists_names.append(artist_name['name'])
                artists_ids.append(artist_name['id'])

            track_details_for_query.append(
                (track_id,
                 track_name,
                 release_date,
                 duration_ms,
                 popularity,
                 cover_album,
                 ','.join(artists_names),
                 ','.join(artists_ids)
                 )
            )

    cur.executemany('''
        INSERT OR IGNORE INTO track_details (
            track_id,
            track_name,
            release_date,
            duration_ms,
            popularity,
            cover_album,
            artists_names,
            artists_ids) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', track_details_for_query)
    con.commit()


def artist_info():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS artist_info (
            artist_id TEXT PRIMARY KEY,
            name TEXT,
            followers INTEGER,
            popularity INTEGER,
            image TEXT
        )
    ''')

    artists_ids: List[str] = list(artist_page.values())
    fifty_id_list: List[List[str]] = []
    artist_info_for_query: List[Tuple] = []
    for i in range(0,  len(artists_ids), 50):
        fifty_id_list.append(artists_ids[i: i + 50])

    for id_list in fifty_id_list:
        id_list_string = ','.join(id_list)
        url = f'{base_url}/artists/?ids={id_list_string}'
        response = requests.get(url, headers=auth_header, proxies=proxies)
        for artist in response.json()['artists']:
            artist_id = artist['id']
            name = artist['name']
            followers = artist['followers']['total']
            popularity = artist['popularity']
            image = artist['images'][0]['url']
            artist_info_for_query.append(
                (artist_id, name, followers, popularity, image)
            )

    cur.executemany('''
        INSERT OR IGNORE INTO artist_info (
            artist_id, 
            name, 
            followers, 
            popularity, 
            image) VALUES (?, ?, ?, ?, ?)
    ''', artist_info_for_query)
    con.commit()


def main():
    # albums_details()
    # all_tracks()
    # track_details()
    artist_info()


if __name__ == '__main__':
    main()
    con.close()
