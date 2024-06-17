from random import shuffle

url_pattern = r'https://[^"]+'
url_pattern_size = r'(https://[^"]+)-t\d+x\d+(\.jpg)'

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
    'avatar': './/span[contains(@class, "sc-artwork")]',
    'end_of_page': './/div[contains(@class, "paging-eof sc-border-light-top")]'
}

artist_page: dict[str, str] = {
    'Mahdyar': 'https://soundcloud.com/mahdyar',
    'Dorcci': 'https://soundcloud.com/dorcci',
    'Hiphopologist': 'https://soundcloud.com/hiphopologistsoroush',
    'Reza Pishro': 'https://soundcloud.com/reza-pishro-rail',
    'CatchyBeatz': 'https://soundcloud.com/tiktaak-sr',
    'Poori': 'https://soundcloud.com/godpoori',
    'Chrvsi': 'https://soundcloud.com/chvrsi',
    'Young Sudden': 'https://soundcloud.com/youngsudden',
    'Koorosh': 'https://soundcloud.com/koorowsh420',
    'Arta': 'https://soundcloud.com/arta-mir',
    'Ali Sorena': 'https://soundcloud.com/alisorena',
    'Ashkan Kagan': 'https://soundcloud.com/ashkankagan',
    'Hichkas': 'https://soundcloud.com/hichkasofficial',
    'Gdaal': 'https://soundcloud.com/gdaal',
    'Dariu$h': 'https://soundcloud.com/tbhkr',
    'VINAK': 'https://soundcloud.com/elvinako',
    '021G': 'https://soundcloud.com/gandom-021',
    'Eycin': 'https://soundcloud.com/ey-cin',
    'Dalu': 'https://soundcloud.com/dalumc',
    'PutaK': 'https://soundcloud.com/pooriaputak',
    'Sajad Shahi': 'https://soundcloud.com/sajadshahi',
    'Hoodadk4': 'https://soundcloud.com/hoodadk4',
    'Pouriya Adroit': 'https://soundcloud.com/poriyaadroit',
    'Matin Fattahi': 'https://soundcloud.com/matinfattahi',
    'Ali Geramy': 'https://soundcloud.com/aligeramy',
    'Tiem': 'https://soundcloud.com/justiem',
    'HesamTiem': 'https://soundcloud.com/hesamtiem',
    '021kid': 'https://soundcloud.com/021kid',
    'Amin Tijay': 'https://soundcloud.com/amintijayy',
}

page_urls: list[str] = list(artist_page.values())
shuffle(page_urls)
