from time import sleep
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions


# options = webdriver.FirefoxOptions()
# options.add_argument('--headless')

driver = webdriver.Firefox()

Mahdyar = 'https://soundcloud.com/mahdyar/tracks'
Poori = 'https://soundcloud.com/godpoori/tracks'
Dorcci = 'https://soundcloud.com/dorcci/tracks'
Amir_Tataloo = 'https://soundcloud.com/amirtataloo/tracks'
Hiphopologist = 'https://soundcloud.com/hiphopologistsoroush/tracks'
Johar_records = 'https://soundcloud.com/johar-records/tracks'
Reza_Pishro = 'https://soundcloud.com/reza-pishro-rail/tracks'
Bahram = 'https://soundcloud.com/bahramnouraei/tracks'
CatchyBeatz = 'https://soundcloud.com/tiktaak-sr/tracks'

driver.get(CatchyBeatz)
'''-----------------------------------------------------------------------'''
sound_body = './/div[contains(@class, "sound__body")]'
'''-----------------------------------------------------------------------'''
sound_title = './/a[contains(@class, "soundTitle__title")]'
'''-----------------------------------------------------------------------'''
sound_play_list = './/span[contains(@class, "sc-ministats-plays")]'
s_play = './/span[contains(@class, "sc-visuallyhidden")]'
'''-----------------------------------------------------------------------'''
s_like = './/button[contains(@class, "sc-button-like")]'
s_comment = './/a[contains(@class, "sc-ministats-comments")]'
upload_date = './/time[contains(@class, "relativeTime")]'
'''-----------------------------------------------------------------------'''
s_link = './/a[contains(@class, "sc-link-primary")]'
'''-----------------------------------------------------------------------'''
cover_link = './/span[contains(@class, "sc-artwork")]'
'''-----------------------------------------------------------------------'''
js_end_of_page_condition = (
    'return window.innerHeight '
    '+ window.pageYOffset '
    '>= document.body.offsetHeight')

js_scroll_down_command = 'window.scrollBy(0, 1000)'
# scroll down to the bottom of the page
while True:
    # scroll down 1000 pixels
    driver.execute_script(js_scroll_down_command)
    # wait for page to load
    sleep(3)
    # check if at bottom of page
    if driver.execute_script(js_end_of_page_condition):
        break


sound_body = driver.find_elements(By.XPATH, value=sound_body)
n = 1
for sound in sound_body:
    try:
        title = sound.find_element(By.XPATH, value=sound_title).text
    except exceptions.NoSuchElementException:
        title = None

    try:
        play_list = sound.find_element(By.XPATH, value=sound_play_list)
        play = play_list.find_element(
            By.XPATH, value=s_play).text.split(' ')[0]
    except exceptions.NoSuchElementException:
        play = None

    try:
        like = sound.find_element(By.XPATH, value=s_like).text
    except exceptions.NoSuchElementException:
        like = None

    try:
        comment = sound.find_element(By.XPATH, value=s_comment)\
            .text.split('\n')[1]
    except exceptions.NoSuchElementException:
        comment = None

    try:
        upload_date_time = sound.find_element(
            By.XPATH, value=upload_date).get_attribute('datetime')
    except exceptions.NoSuchElementException:
        upload_date_time = None

    try:
        link = sound.find_element(By.XPATH, value=s_link).get_attribute('href')
    except exceptions.NoSuchElementException:
        link = None

    try:
        cover_style = sound.find_element(
            By.XPATH,
            value=cover_link).get_attribute('style')
        full_size_cover = re.sub(
            pattern=r'(https://[^"]+)-t200x200(\.jpg")',
            repl=r'\1-t500x500\2',
            string=cover_style)

    except exceptions.NoSuchElementException:
        full_size_cover = None
    print(f'{n} {title} | plays: {play} |'
          f' likes: {like} | comments: {comment}'
          f' | uploaded at: {upload_date_time}'
          f' | link: {link} | cover: {full_size_cover}')
    n += 1


driver.quit()
