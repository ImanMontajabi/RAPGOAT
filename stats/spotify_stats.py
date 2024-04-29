import asyncio
from typing import List

import aiohttp

from spotify_auth import auth_header
from init import proxies, artist_page, base_url


async def all_albums():
    all_artists_ids: List[str] = list(artist_page.values())

    async with aiohttp.ClientSession() as session:
        artist_album_tasks = []
        for artist_id in all_artists_ids:
            url = f'{base_url}/artists/{artist_id}/albums?limit=50'
            artist_album_tasks.append(
                session.get(url, headers=auth_header, proxy=proxies['http']))
        albums_resp = await asyncio.gather(*artist_album_tasks)
        for resp in albums_resp:
            print(resp.headers.get('Retry-After', 10))
        albums_json = [await resp.json() for resp in albums_resp]

        # this section checks if each artist/id has more than 50 albums
        for album in albums_json:
            if album['next'] is not None:
                async with session.get(
                        album['next'],
                        headers=auth_header,
                        proxy=proxies['http']
                ) as next_resp:
                    albums_json.append(await next_resp.json())

        # I retrieve all albums ids from responses
        albums_ids: List[str] = []
        for artists_albums in albums_json:
            for i in range(0, len(artists_albums['items'])):
                albums_ids.append(artists_albums['items'][i]['id'])


# async def all_tracks():
#     # I want to get all tracks of artists
#     all_tracks_tasks = []
#     for album_id in albums_ids:
#         tracks_url = f'{base_url}/albums/{album_id}/tracks?limit=50'
#         all_tracks_tasks.append(
#             session.get(
#                 tracks_url,
#                 headers=auth_header,
#                 proxy=proxies['http']
#             )
#         )
#     tracks_resp = await asyncio.gather(*all_tracks_tasks)
#     tracks_json = [await resp.json() for resp in tracks_resp]
#
#     # this section checks if each album has more than 50 tracks in album
#     for track in tracks_json:
#         if track['next'] is not None:
#             async with session.get(
#                     track['next'],
#                     headers=auth_header,
#                     proxy=proxies['http']
#             ) as track_next_resp:
#                 tracks_json.append(track_next_resp)
#
#
# return tracks_json


async def main():
    await all_albums()

if __name__ == '__main__':
    asyncio.run(main())
