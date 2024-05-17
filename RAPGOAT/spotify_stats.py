import os
import json
import base64
# from time import sleep
from random import shuffle

import requests

from SpotifyInit import proxies, artist_page, base_url, cur, con
from dotenv import load_dotenv


load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def auth_header() -> dict[str, str]:
    auth_string = f'{CLIENT_ID}:{CLIENT_SECRET}'
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    while True:
        try:
            # argument -> proxies=proxies for using this in Iran
            result = requests.post(
                url,
                headers=headers,
                data=data,
                proxies=proxies)
        except Exception as e:
            print(f'auth_header -> post: {e}')
            # sleep(60)
        else:
            break
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return {'Authorization': f'Bearer {token}'}


def albums_details(bunch: list[str]) -> None:
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
    resp_json: list[dict] = []

    for artist_id in bunch:
        header = auth_header()
        url = f'{base_url}/artists/{artist_id}/albums?limit=50'
        while True:
            try:
                # argument -> proxies=proxies for using this in Iran
                response = requests.get(url, headers=header, proxies=proxies)
            except Exception as e:
                print(f'albums_details -> get: {e}')
                # sleep(60)
            else:
                break
        resp_json.append(response.json())

    # this loop adds rest of albums for artists with more than 50 albums
    for albums in resp_json:
        if albums['next'] is not None:
            header = auth_header()
            while True:
                try:
                    # argument -> proxies=proxies for using this in Iran
                    response = requests.get(
                        albums['next'],
                        headers=header,
                        proxies=proxies
                    )
                except Exception as e:
                    print(f'album_details -> get[next]: {e}')
                    # sleep(60)
                else:
                    break
            resp_json.append(response.json())

    # this loop inserts all albums ids into album_id table
    id_list_for_query: list[tuple] = []
    for album in resp_json:
        for i in range(0, len(album['items'])):
            album_id = album['items'][i]['id']
            album_name = album['items'][i]['name']
            total_tracks = album['items'][i]['total_tracks']
            release_date = album['items'][i]['release_date']
            album_type = album['items'][i]['album_type']
            cover = album['items'][i]['images'][0]['url']
            artist_names: list['str'] = []
            artist_ids: list['str'] = []
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
        INSERT OR REPLACE INTO albums_details (
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


def all_tracks(bunch: list[str]) -> None:
    # creating table tracks_id to save track_id tracks_name and release_date
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tracks_id (
            track_id TEXT PRIMARY KEY,
            track_name TEXT,
            release_date TEXT
        )
    ''')

    albums_json: list[dict] = []
    id_list_for_query: list[tuple] = []

    for i in range(0, len(bunch), 20):
        album_id_20_string = ','.join(bunch[i: i + 20])
        header = auth_header()
        url = f'{base_url}/albums?ids={album_id_20_string}'
        while True:
            try:
                # argument -> proxies=proxies for using this in Iran
                response = requests.get(url, headers=header, proxies=proxies)
            except Exception as e:
                print(f'all_track -> get: {e}')
                # sleep(60)
            else:
                break
        albums_json.append(response.json()['albums'])

    for twenty_albums in albums_json:
        for album in twenty_albums:
            release_date = album['release_date']
            if album['tracks']['next'] is not None:
                next_tracks_url = album['tracks']['next']
                header = auth_header()
                while True:
                    try:
                        # argument -> proxies=proxies for using this in Iran
                        next_response = requests.get(
                            next_tracks_url,
                            headers=header,
                            proxies=proxies)
                    except Exception as e:
                        print(f'all_track -> get[next]: {e}')
                        # sleep(60)
                    else:
                        break
                albums_json.append(next_response.json()['albums'])
            for track in range(0, len(album['tracks']['items'])):
                name = album['tracks']['items'][track]['name']
                track_id = album['tracks']['items'][track]['id']
                id_list_for_query.append((track_id, name, release_date))

    cur.executemany('''
        INSERT OR REPLACE INTO tracks_id (track_id, track_name, release_date)
        VALUES (?, ?, ?)''', id_list_for_query)
    con.commit()


def track_details(bunch: list[str]) -> None:
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

    tracks_json: list[dict] = []

    for i in range(0, len(bunch), 50):
        track_id_string: str = ','.join(bunch[i: i + 50])
        header = auth_header()
        url = f'{base_url}/tracks?ids={track_id_string}'
        while True:
            try:
                # argument -> proxies=proxies for using this in Iran
                response = requests.get(url, headers=header, proxies=proxies)
            except Exception as e:
                print(f'track_details -> get: {e}')
                # sleep(60)
            else:
                break
        tracks_json.append(response.json()['tracks'])

    track_details_for_query: list[tuple] = []
    for fifty_track in tracks_json:
        for track in fifty_track:
            track_id = track['id']
            track_name = track['name']
            release_date = track['album']['release_date']
            duration_ms = track['duration_ms']
            popularity = track['popularity']
            cover_album = track['album']['images'][0]['url']
            artists_names: list[str] = []
            artists_ids: list[str] = []
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
        INSERT OR REPLACE INTO track_details (
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


def artist_info(bunch: list[str]) -> None:
    cur.execute('''
        CREATE TABLE IF NOT EXISTS artist_info (
            artist_id TEXT PRIMARY KEY,
            name TEXT,
            followers INTEGER,
            popularity INTEGER,
            image TEXT
        )
    ''')

    artist_info_for_query: list[tuple] = []

    for i in range(0,  len(bunch), 50):
        id_list_string: str = ','.join(bunch[i: i + 50])
        header = auth_header()
        url = f'{base_url}/artists/?ids={id_list_string}'
        while True:
            try:
                # argument -> proxies=proxies for using this in Iran
                response = requests.get(url, headers=header, proxies=proxies)
            except Exception as e:
                print(f'artist_info -> get: {e}')
                # sleep(60)
            else:
                break
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
        INSERT OR REPLACE INTO artist_info (
            artist_id, 
            name, 
            followers, 
            popularity, 
            image) VALUES (?, ?, ?, ?, ?)
    ''', artist_info_for_query)
    con.commit()


def main():
    while True:
        try:
            all_artists_ids: list[str] = list(artist_page.values())
            shuffle(all_artists_ids)
            chunk_artist: int = 5
            len_artist: int = len(all_artists_ids)
            for i in range(0, len_artist, chunk_artist):
                bunch = all_artists_ids[i: i + chunk_artist]
                albums_details(bunch)
                # sleep(300)
            else:
                break
        except Exception as e:
            print(f'albums_details function: {e}')
            # sleep(300)

    # sleep(600)

    while True:
        try:
            all_albums_ids: list[str] = []
            chunk_album: int = 100
            for row in cur.execute('''SELECT * FROM albums_details'''):
                all_albums_ids.append(row[0])
            shuffle(all_albums_ids)
            len_albums: int = len(all_albums_ids)
            for i in range(0, len_albums, chunk_album):
                bunch = all_albums_ids[i: i + chunk_album]
                all_tracks(bunch)
                # sleep(300)
            else:
                break
        except Exception as e:
            print(f'all_track function: {e}')
            # sleep(300

    # sleep(600)

    while True:
        try:
            all_tracks_ids: list[str] = []
            chunk_track: int = 200
            for row in cur.execute('''SELECT * FROM tracks_id'''):
                all_tracks_ids.append(row[0])
            shuffle(all_tracks_ids)
            len_tracks: int = len(all_tracks_ids)
            for i in range(0, len_tracks, chunk_track):
                bunch = all_tracks_ids[i: i + chunk_track]
                track_details(bunch)
                # sleep(300)
            else:
                break
        except Exception as e:
            print(f'track_details function: {e}')

    # sleep(600)

    while True:
        try:
            all_artists_info_ids: list[str] = list(artist_page.values())
            shuffle(all_artists_info_ids)
            chunk_artist: int = 200
            len_artist: int = len(all_artists_info_ids)
            for i in range(0, len_artist, chunk_artist):
                bunch = all_artists_info_ids[i: i + chunk_artist]
                artist_info(bunch)
            else:
                break
        except Exception as e:
            print(f'artist_info function: {e}')
        # sleep(300)

    # sleep(600)

    con.close()
