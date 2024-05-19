import re
from time import sleep
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

from SoundcloudInit import (
    my_xpath,
    url_pattern,
    page_urls
    )


def scroll_down(driver, url: str) -> None:
    last_height: int
    new_height: int
    while True:
        driver.execute_script('window.scrollBy(0, 350);')
        # this variable changes scrawling speed
        sleep(2)
        if driver.execute_script('return window.innerHeight + \
        window.pageYOffset >= document.body.offsetHeight'):
            try:
                element_present = ec.presence_of_element_located(
                    (By.XPATH,
                     my_xpath['end_of_page']))
                WebDriverWait(driver, timeout=10).until(element_present)
                print(f'{url} reached end of the page.')
            except TimeoutException:
                print(f"{url} couldn't reach end of the page")
                get_url(driver, url)
                if run_scroll_down(driver, url) is None:
                    break
            else:
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
        number_int = int(float(number_digits) * 1000)
    elif number.endswith('M'):
        number_digits = number.split('M')[0]
        number_int = int(float(number_digits) * 1000_000)
    elif ',' in number:
        number_digits = ''.join(number.split(','))
        number_int = int(number_digits)
    else:
        try:
            number_int = int(number)
        except Exception as e:
            print(f'string_to_int() > converting number failed > {e}')
            return None

    return number_int


def initialize_tables(cur):
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


def page_information(driver, url: str) -> list[tuple]:
    page_info_for_query: list[tuple] = []
    try:
        page_name = driver.find_element(
            By.XPATH, value=my_xpath['page_name'])
        name = page_name.text
        if name.endswith(' Verified'):
            name = name.replace(' Verified', '')
    except exceptions.NoSuchElementException as e:
        print(f'page_information() > page_name > {e}')
        name = None

    try:
        artist_stats = driver.find_elements(
            By.XPATH, value=my_xpath['page_stats'])
        stats: list = []
        for stat in artist_stats:
            stats.extend(stat.get_attribute('title').split(' '))

        followers_int = string_to_int(stats[0])
        following_int = string_to_int(stats[3])
        tracks_int = string_to_int(stats[5])
    except Exception as e:
        print(f'page_information > page_stats > {e}')
        followers_int = None
        following_int = None
        tracks_int = None

    try:
        page_avatar = driver.find_element(
            By.XPATH, value=my_xpath['page_avatar'])
        avatar_url = page_avatar.find_element(
            By.XPATH, value=my_xpath['avatar'])
        avatar_style = avatar_url.get_attribute('style')
        avatar_url = extract_hq_image_url(avatar_style)
    except exceptions.NoSuchElementException as e:
        print(f'page_information() > page_avatar > {e}')
        avatar_url = None

    page_info_for_query.append((
        url, name, followers_int, following_int, tracks_int, avatar_url))
    return page_info_for_query


def save_page_information(cur, page_info_for_query: [tuple]):
    cur.executemany('''
        INSERT OR REPLACE INTO soundcloud_artist (
            page_url,
            page_name,
            followers,
            followings,
            tracks,
            avatar_url
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', page_info_for_query)


def tracks_information(driver) -> list[tuple]:
    tracks_info_for_query: list[tuple] = []
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
        try:
            page_name = driver.find_element(
                By.XPATH, value=my_xpath['page_name'])
            name = page_name.text
            if name.endswith(' Verified'):
                name = name.replace(' Verified', '')
        except exceptions.NoSuchElementException as e:
            print(f'tracks_information > page_name > {e}')
            name = None

        tracks_info_for_query.append((
            link, name, title, play_int, like_int, comment_int,
            upload_date_time, cover_url))

    return tracks_info_for_query


def save_tracks_information(cur, tracks_info_for_query: list[tuple]):
    cur.executemany('''
        INSERT OR REPLACE INTO soundcloud_tracks (
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


def get_url(driver, url: str) -> None:
    while True:
        try:
            driver.get(url + '/tracks')
        except Exception as e:
            print(f'get_url() > {e}')
        else:
            break


def run_scroll_down(driver, url: str) -> None:
    while True:
        try:
            scroll_down(driver, url)
        except Exception as e:
            print(f'run_scroll_down() > {e}')
            sleep(5)
            get_url(driver, url)
        else:
            break


def scraper(url_chunk: list):
    tracks_info_for_query: list[tuple]
    page_info_for_query: list[tuple]

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(300)
    driver.implicitly_wait(10)

    try:
        con = sqlite3.connect('RapGoat.db')
        cur = con.cursor()
    except sqlite3.DatabaseError as e:
        print(f'scraper > Database connection was unsuccessful > {e}')
        exit(1)

    initialize_tables(cur)

    for url in url_chunk:
        '''this initializes driver, scroll down to bottom of the page
            and ensures that the page loads as expected'''
        get_url(driver, url)
        run_scroll_down(driver, url)
        '''This extracts page information such as name, followers, ... '''
        page_info_for_query = page_information(driver, url)
        '''This extracts tracks infos from soundcloud page'''
        tracks_info_for_query = tracks_information(driver)
        '''This function saves page data into soundcloud_artist table'''
        save_page_information(cur, page_info_for_query)
        '''This function saves tracks data into soundcloud_tracks table'''
        save_tracks_information(cur, tracks_info_for_query)
        con.commit()
    driver.quit()
    con.close()


def main():
    """
    For every 5 urls (c_size) create one thread
    and maximum active threads are 10 (max_workers)

    :param:
    :return:
    """

    max_workers: int = 2
    page_urls_length: int = len(page_urls)

    if page_urls_length < max_workers:
        max_workers = page_urls_length

    c_size: int = page_urls_length // max_workers
    chunked_list = [
        page_urls[i: i + c_size] for i in range(0, page_urls_length, c_size)]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(scraper, url_chunk) for url_chunk in chunked_list]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f'main() > ThreadPoolExecutor > {e}')
