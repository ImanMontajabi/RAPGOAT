import sqlite3
from random import shuffle

from selenium import webdriver

url_pattern = r'https://[^"]+'
url_pattern_size = r'(https://[^"]+)-t\d+x\d+(\.jpg)'

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

artist_page: dict[str, str] = {
    'Mahdyar': 'https://soundcloud.com/mahdyar',
    'Dorcci': 'https://soundcloud.com/dorcci',
    'Amir_Tataloo': 'https://soundcloud.com/amirtataloo',
    'Hiphopologist': 'https://soundcloud.com/hiphopologistsoroush',
    'Johar_records': 'https://soundcloud.com/johar-records',
    'Reza_Pishro': 'https://soundcloud.com/reza-pishro-rail',
    'Bahram': 'https://soundcloud.com/bahramnouraei',
    'CatchyBeatz': 'https://soundcloud.com/tiktaak-sr',
    'Ali Owj': 'https://soundcloud.com/owjali',
    'Poori': 'https://soundcloud.com/godpoori',
    'Chrvsi': 'https://soundcloud.com/chvrsi',
    'Young Sudden': 'https://soundcloud.com/youngsudden',
    'Koorosh': 'https://soundcloud.com/koorowsh420',
    'Arta': 'https://soundcloud.com/arta-mir',
    'Arman Miladi': 'https://soundcloud.com/arman-miladi',

}

page_urls: list[str] = list(artist_page.values())
shuffle(page_urls)


my_xpath: dict[str, str] = {
    'sound_body': './/div[contains(@class, "sound__body")]',
    'sound_title': './/a[contains(@class, "soundTitle__title")]',
    'sound_play_list': './/span[contains(@class, "sc-ministats-plays")]',
    's_play': './/span[contains(@class, "sc-visuallyhidden")]',
    's_like': './/button[contains(@class, "sc-button-like")]',
    's_comment': './/a[contains(@class, "sc-ministats-comments")]',
    'upload_date': './/time[contains(@class, "relativeTime")]',
    's_link': './/a[contains(@class, "sc-link-primary")]',
    'cover_link': './/span[contains(@class, "sc-artwork")]',
    'page_stats': './/a[contains(@class, "infoStats__statLink")]',
    'page_name': './/h2[contains(@class, "profileHeaderInfo__userName")]',
    'page_avatar': './/div[contains(@class, "profileHeaderInfo__avatar")]',
    'avatar': './/span[contains(@class, "sc-artwork")]'
}

js_end_of_page_condition = (
    'return window.innerHeight '
    '+ window.pageYOffset '
    '>= document.body.offsetHeight')
js_scroll_down_command = 'window.scrollBy(0, 1000)'

con = sqlite3.connect('rapgoat.db')
cur = con.cursor()

