from time import sleep
import re
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions

from SoundcloudInit import (
    artist_page, my_xpath, js_end_of_page_condition, js_scroll_down_command)


# options = webdriver.FirefoxOptions()
# options.add_argument('--headless')

driver = webdriver.Firefox()
page_urls: List[str] = list(artist_page.values())
for url in page_urls:
    driver.get(url)

    '''scroll down to the bottom of the page'''
    while True:
        '''scroll down 1000 pixels'''
        driver.execute_script(js_scroll_down_command)
        '''wait for page to load'''
        sleep(3)
        '''check if at bottom of page'''
        if driver.execute_script(js_end_of_page_condition):
            break

    sound_body = driver.find_elements(By.XPATH, value=my_xpath['sound_body'])
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
        except exceptions.NoSuchElementException:
            play = None
        try:
            like = sound.find_element(By.XPATH, value=my_xpath['s_like']).text
        except exceptions.NoSuchElementException:
            like = None
        try:
            comment = sound.find_element(
                By.XPATH, value=my_xpath['s_comment']).text.split('\n')[1]
        except exceptions.NoSuchElementException:
            comment = None
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
            full_size_cover = re.sub(
                pattern=r'(https://[^"]+)-t200x200(\.jpg")',
                repl=r'\1-t500x500\2',
                string=cover_style)

        except exceptions.NoSuchElementException:
            full_size_cover = None
        print(f'{title} | plays: {play} |'
              f' likes: {like} | comments: {comment}'
              f' | uploaded at: {upload_date_time}'
              f' | link: {link} | cover: {full_size_cover}')

driver.quit()
