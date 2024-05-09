from time import sleep
import re

from selenium.webdriver.common.by import By
from selenium.common import exceptions

from SoundcloudInit import (
    driver,
    my_xpath,
    js_end_of_page_condition,
    js_scroll_down_command,
    url_pattern,
    page_urls,
    con,
    cur)


def scroll_down(url: str) -> None:
    while True:
        try:
            driver.get(url + '/tracks')
        except Exception as e:
            print(e)
            driver.quit()
            # sleep(30)
        else:
            break
    while True:
        '''scroll down 1000 pixels'''
        driver.execute_script(js_scroll_down_command)
        '''wait for page to load'''
        sleep(3)
        '''check if at bottom of page'''
        if driver.execute_script(js_end_of_page_condition):
            break


def extract_hq_image_url(style: str) -> str:
    match = re.search(url_pattern, style)
    if match:
        url = match.group()
        url_hq = url.replace('-t200x200.jpg', '-t500x500.jpg')
        return url_hq


def string_to_int(number: str) -> None | int:
    if number.endswith('K'):
        number_digits = number.split('K')[0]
        number_init = int(float(number_digits) * 1000)
    elif number.endswith('M'):
        number_digits = number.split('M')[0]
        number_init = int(float(number_digits) * 1000_000)
    elif ',' in number:
        number_digits = ''.join(number.split(','))
        number_init = int(number_digits)
    else:
        try:
            number_init = int(number)
        except Exception as e:
            print(e)
            return None

    return number_init


def init_tables():
    cur.execute('''
            CREATE TABLE IF NOT EXISTS soundcloud_tracks (
                track_url TEXT PRIMARY KEY,
                page_name TEXT,
                track_title TEXT,
                plays INTEGER,
                likes INTEGER,
                comments INTEGER,
                upload_datetime TEXT,
                cover_url TEXT
            )
        ''')

    cur.execute('''
            CREATE TABLE IF NOT EXISTS soundcloud_artist (
                page_url TEXT PRIMARY KEY,
                page_name TEXT,
                followers INTEGER,
                followings INTEGER,
                tracks INTEGER,
                avatar_url TEXT
            )
        ''')


def main():
    init_tables()

    for url in page_urls:
        tracks_info_for_query: list[tuple] = []
        page_info_for_query: list[tuple] = []

        '''this initializes driver, scroll down to bottom of the page
        and ensures that the page loads as expected'''
        while True:
            try:
                scroll_down(url)
            except Exception as e:
                print(e)
                # sleep(30)
                scroll_down(url)
            else:
                break

        '''This extracts page information such as name, followers, ... '''
        page_name = driver.find_element(
            By.XPATH, value=my_xpath['page_name'])
        name = page_name.text
        if name.endswith(' Verified'):
            name = name.replace(' Verified', '')

        artist_stats = driver.find_elements(
            By.XPATH, value=my_xpath['page_stats'])
        stats: list = []
        for stat in artist_stats:
            stats.extend(stat.get_attribute('title').split(' '))

        followers_int = string_to_int(stats[0])
        following_int = string_to_int(stats[3])
        tracks_int = string_to_int(stats[5])

        page_avatar = driver.find_element(
            By.XPATH, value=my_xpath['page_avatar'])
        avatar_url = page_avatar.find_element(
            By.XPATH, value=my_xpath['avatar'])
        avatar_style = avatar_url.get_attribute('style')
        avatar_url = extract_hq_image_url(avatar_style)

        page_info_for_query.append((
            url, name, followers_int, following_int, tracks_int, avatar_url))

        '''This extracts tracks infos from soundcloud page'''
        sound_body = driver.find_elements(
            By.XPATH, value=my_xpath['sound_body'])
        for sound in sound_body:
            try:
                title = sound.find_element(
                    By.XPATH, value=my_xpath['sound_title']).text
            except exceptions.NoSuchElementException:
                title = None
            try:
                play_list = sound.find_element(
                    By.XPATH, value=my_xpath['sound_play_list'])
                play = play_list.find_element(
                    By.XPATH, value=my_xpath['s_play']).text.split(' ')[0]
                play_int = string_to_int(play)
            except exceptions.NoSuchElementException:
                play_int = None
            try:
                like = sound.find_element(
                    By.XPATH, value=my_xpath['s_like']).text
                like_int = string_to_int(like)
            except exceptions.NoSuchElementException:
                like_int = None
            try:
                comment = sound.find_element(
                    By.XPATH, value=my_xpath['s_comment']).text.split('\n')[1]
                comment_int = string_to_int(comment)
            except exceptions.NoSuchElementException:
                comment_int = None
            try:
                upload_date_time = sound.find_element(
                    By.XPATH,
                    value=my_xpath['upload_date']).get_attribute('datetime')
            except exceptions.NoSuchElementException:
                upload_date_time = None
            try:
                link = sound.find_element(
                    By.XPATH, value=my_xpath['s_link']).get_attribute('href')
            except exceptions.NoSuchElementException:
                link = None
            try:
                cover_style = sound.find_element(
                    By.XPATH,
                    value=my_xpath['cover_link']).get_attribute('style')
                cover_url = extract_hq_image_url(cover_style)

            except exceptions.NoSuchElementException:
                cover_url = None

            tracks_info_for_query.append((
                link, name, title, play_int, like_int, comment_int,
                upload_date_time, cover_url))

        cur.executemany('''
                INSERT OR IGNORE INTO soundcloud_tracks (
                    track_url,
                    page_name,
                    track_title,
                    plays,
                    likes,
                    comments,
                    upload_datetime,
                    cover_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', tracks_info_for_query)

        cur.executemany('''
            INSERT OR IGNORE INTO soundcloud_artist (
                page_url,
                page_name,
                followers,
                followings,
                tracks,
                avatar_url
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', page_info_for_query)
        con.commit()

    driver.quit()
    con.close()


if __name__ == '__main__':
    main()
