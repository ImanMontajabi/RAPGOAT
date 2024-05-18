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
    'Amir Tataloo': 'https://soundcloud.com/amirtataloo',
    'Hiphopologist': 'https://soundcloud.com/hiphopologistsoroush',
    'Reza Pishro': 'https://soundcloud.com/reza-pishro-rail',
    'Bahram': 'https://soundcloud.com/bahramnouraei',
    'CatchyBeatz': 'https://soundcloud.com/tiktaak-sr',
    'Poori': 'https://soundcloud.com/godpoori',
    'Chrvsi': 'https://soundcloud.com/chvrsi',
    'Young Sudden': 'https://soundcloud.com/youngsudden',
    'Koorosh': 'https://soundcloud.com/koorowsh420',
    'Arta': 'https://soundcloud.com/arta-mir',
    'Arman Miladi': 'https://soundcloud.com/arman-miladi',
    'Sami Low': 'https://soundcloud.com/sami-low-instrumental',
    'PooBon': 'https://soundcloud.com/tetroparja',
    'Isam': 'https://soundcloud.com/isamdolavion',
    'Ali Sorena': 'https://soundcloud.com/alisorena',
    'Sinazaa': 'https://soundcloud.com/sinazza',
    'Ashkan Kagan': 'https://soundcloud.com/ashkankagan',
    'Hichkas': 'https://soundcloud.com/hichkasofficial',
    'Gdaal': 'https://soundcloud.com/gdaal',
    'soelchigini': 'https://soundcloud.com/soelchigini',
    'Divar': 'https://soundcloud.com/divarrecords',
    'Dariu$h': 'https://soundcloud.com/tbhkr',
    'ATOUR': 'https://soundcloud.com/atour',
    'Nazli Mcfian': 'https://soundcloud.com/nazlimcfian',
    'Parsalip': 'https://soundcloud.com/parsalipofficial',
    'Hoomaan': 'https://soundcloud.com/hoomaanxx',
    'VINAK': 'https://soundcloud.com/elvinako',
    'Khalse': 'https://soundcloud.com/khal3music',
    'Sadegh': 'https://soundcloud.com/sadeghvahedi',
    'Sina Saee': 'https://soundcloud.com/sinasae',
    'Asli Stream': 'https://soundcloud.com/aslistream',
    'Mehrad Hidden': 'https://soundcloud.com/mehradhiddenofficial',
    'Canis': 'https://soundcloud.com/icanisofficial',
    'Wantons': 'https://soundcloud.com/wantons',
    'Amir Khalvat': 'https://soundcloud.com/amirkhalvatofficial',
    'Hamid Sefat': 'https://soundcloud.com/hamidsefat021',
    'Sohrab MJ': 'https://soundcloud.com/haj-ali-77490318',
    '021G': 'https://soundcloud.com/gandom-021',
    'Daniyal': 'https://soundcloud.com/daniyal_official',
    'Amir Ribar': 'https://soundcloud.com/realribar',
    'Amir Reghab': 'https://soundcloud.com/amirreghab',
    'Mehyad': 'https://soundcloud.com/mehyad',
    'Eycin': 'https://soundcloud.com/ey-cin',
    'Mamazimanam': 'https://soundcloud.com/mamazimanam',
    'Dalu': 'https://soundcloud.com/dalumc',
    'Sepehr Cnjim': 'https://soundcloud.com/cnjim',
    'PutaK': 'https://soundcloud.com/pooriaputak',
    'Parsa Simpson': 'https://soundcloud.com/parsa_simpson',
    'PapaBoyz': 'https://soundcloud.com/papa-boyz',
    'Saeed Dehghan': 'https://soundcloud.com/saeed-dehghan',
    'Sajad Shahi': 'https://soundcloud.com/sajadshahi',
    'Hoodadk4': 'https://soundcloud.com/hoodadk4',
    'Pouriya Adroit': 'https://soundcloud.com/poriyaadroit',
    'Matin Fattahi': 'https://soundcloud.com/matinfattahi',
    'Ali Geramy': 'https://soundcloud.com/aligeramy',
    'Tiem': 'https://soundcloud.com/justiem',
    'HesamTiem': 'https://soundcloud.com/hesamtiem',
    '021kid': 'https://soundcloud.com/021kid',
    'ShahinNajafi': 'https://soundcloud.com/shahinnajafimusic',
    'Shayea': 'https://soundcloud.com/shayea_rap',
    'YAS': 'https://soundcloud.com/yastunes',
    'Sina Mafee': 'https://soundcloud.com/sinamafee',
    'Arash Saretan': 'https://soundcloud.com/arashsaretan',
    'Behzad Leito': 'https://soundcloud.com/bezilei',
    'Amin Tijay': 'https://soundcloud.com/amintijayy',
    'Pouriaa': 'https://soundcloud.com/pouriaa021',
    'Lenna': 'https://soundcloud.com/llennah',
}

page_urls: list[str] = list(artist_page.values())
shuffle(page_urls)
