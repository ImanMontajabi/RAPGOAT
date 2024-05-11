import sqlite3
from random import shuffle

from selenium import webdriver

url_pattern = r'https://[^"]+'
url_pattern_size = r'(https://[^"]+)-t\d+x\d+(\.jpg)'

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox()
driver.set_page_load_timeout(200)
driver.implicitly_wait(30)


artist_page: dict[str, str] = {
    'Mahdyar': 'https://soundcloud.com/mahdyar',
    'Dorcci': 'https://soundcloud.com/dorcci',
    'Amir Tataloo': 'https://soundcloud.com/amirtataloo',
    'Hiphopologist': 'https://soundcloud.com/hiphopologistsoroush',
    'Johar records': 'https://soundcloud.com/johar-records',
    'Reza Pishro': 'https://soundcloud.com/reza-pishro-rail',
    'Bahram': 'https://soundcloud.com/bahramnouraei',
    'CatchyBeatz': 'https://soundcloud.com/tiktaak-sr',
    'Ali Owj': 'https://soundcloud.com/owjali',
    'Poori': 'https://soundcloud.com/godpoori',
    'Chrvsi': 'https://soundcloud.com/chvrsi',
    'Young Sudden': 'https://soundcloud.com/youngsudden',
    'Koorosh': 'https://soundcloud.com/koorowsh420',
    'Arta': 'https://soundcloud.com/arta-mir',
    'Arman Miladi': 'https://soundcloud.com/arman-miladi',
    'Sami Low': 'https://soundcloud.com/sami-low-instrumental',
    'PooBon': 'https://soundcloud.com/tetroparja',
    'Isam': 'https://soundcloud.com/isamdolavion',
    'Sinazaa': 'https://soundcloud.com/sinazza',
    'Ashkan Kagan': 'https://soundcloud.com/ashkankagan',
    'Hichkas': 'https://soundcloud.com/hichkasofficial',
    'Gdaal': 'https://soundcloud.com/gdaal',
    'soelchigini': 'https://soundcloud.com/soelchigini',
    'Peeleh': 'https://soundcloud.com/peeleh',
    'Peymandegar': 'https://soundcloud.com/peymandegar',
    'Meraj Tehrani': 'https://soundcloud.com/merajtehrani',
    'MOTREB': 'https://soundcloud.com/motrebam',
    'Farsea': 'https://soundcloud.com/farsea',
    'Divar': 'https://soundcloud.com/divarrecords',
    'Degaran Tribe': 'https://soundcloud.com/degaran',
    'Dariu$h': 'https://soundcloud.com/tbhkr',
    'ATOUR': 'https://soundcloud.com/atour',
    'Navid': 'https://soundcloud.com/navidsadr',
    'yarapelak': 'https://soundcloud.com/yarapelak',
    'Soall': 'https://soundcloud.com/xsoall',
    'Zoha': 'https://soundcloud.com/zohaofficial',
    'Taher': 'https://soundcloud.com/taherflow',
    'Aein': 'https://soundcloud.com/aeinp',
    'Mc Tes': 'https://soundcloud.com/tesmc',
    'PAPA A$LI': 'https://soundcloud.com/arshiaparvane',
    'Nazli Mcfian': 'https://soundcloud.com/nazlimcfian',
    'Parsalip': 'https://soundcloud.com/parsalipofficial',
    'Alipasha': 'https://soundcloud.com/ali_pashaw',
    'Hoomaan': 'https://soundcloud.com/hoomaanxx',
    'Farshad': 'https://soundcloud.com/farshadhiphop',
    'Ben': 'https://soundcloud.com/benyamin-official',
    'Bamdad': 'https://soundcloud.com/bamdadamman',
    'Melli': 'https://soundcloud.com/mellistream',
    'Safir': 'https://soundcloud.com/safirfarsi',
    'Roody': 'https://soundcloud.com/roodyrapkone',
    'Kaboos': 'https://soundcloud.com/kaboosmusic',
    'VINAK': 'https://soundcloud.com/elvinako',
    'Khalse': 'https://soundcloud.com/khal3music',
    'Sadegh': 'https://soundcloud.com/sadeghvahedi',
    'Sina Saee': 'https://soundcloud.com/sinasae',
    'Asli Stream': 'https://soundcloud.com/aslistream',
    'Maslak021': 'https://soundcloud.com/ali-maslak',
    'Mehrad Hidden': 'https://soundcloud.com/mehradhiddenofficial',
    'Canis': 'https://soundcloud.com/icanisofficial',
    'Wantons': 'https://soundcloud.com/wantons',
    'The Don': 'https://soundcloud.com/thedonofficialll',
    'Amir Khalvat': 'https://soundcloud.com/amirkhalvatofficial',
    'Hamid Sefat': 'https://soundcloud.com/hamidsefat021',
    'Sohrab MJ': 'https://soundcloud.com/haj-ali-77490318',
    '021G': 'https://soundcloud.com/gandom-021',
    'Daniyal': 'https://soundcloud.com/kederdaniyal',
    'Amir Ribar': 'https://soundcloud.com/realribar',
    'Amir Reghab': 'https://soundcloud.com/amirreghab',
    'Hamed Slash': 'https://soundcloud.com/hamedslash',
    'Mehyad': 'https://soundcloud.com/mehyad',
    'Eycin': 'https://soundcloud.com/ey-cin',
    'Mamazimanam': 'https://soundcloud.com/mamazimanam',
    'Dalu': 'https://soundcloud.com/dalumc',
    'Sepehr Cnjim': 'https://soundcloud.com/cnjim',
    'Pidar': 'https://soundcloud.com/piidar',
    'Parhum': 'https://soundcloud.com/parhum',
    'Kaveh': 'https://soundcloud.com/kavehofficial',
    'Ashna': 'https://soundcloud.com/ashnarap',
    'PutaK': 'https://soundcloud.com/pooriaputak',
    'Dara K': 'https://soundcloud.com/darapaydar',
    'Pedi I': 'https://soundcloud.com/pedi-i-463233270',
    'Parsa Simpson': 'https://soundcloud.com/parsa_simpson',
    'PapaBoyz': 'https://soundcloud.com/papa-boyz',
    'Saeed Dehghan': 'https://soundcloud.com/saeed-dehghan',
    'Sajad Shahi': 'https://soundcloud.com/sajadshahi',
    'Hoodadk4': 'https://soundcloud.com/hoodadk4',
    'Pouriya Adroit': 'https://soundcloud.com/poriyaadroit',
    'Matin Fattahi': 'https://soundcloud.com/matinfattahi',
    'Ali Geramy': 'https://soundcloud.com/aligeramy',
    'Tiem': 'https://soundcloud.com/justiem',
    'justina': 'https://soundcloud.com/justinaam',
    'Erfan': 'https://soundcloud.com/erfanpaydar',
    '021kid': 'https://soundcloud.com/021kid',
    'ShahinNajafi': 'https://soundcloud.com/shahinnajafimusic',
    'Dayan_rz': 'https://soundcloud.com/dayanmusic',
    'Shayea': 'https://soundcloud.com/shayea_rap',
    'YAS': 'https://soundcloud.com/yastunes',
    'Merzhak': 'https://soundcloud.com/mer-zhak',
    'sajadii': 'https://soundcloud.com/sajadiiofficial',
    'Jarshaa': 'https://soundcloud.com/jarshaa',
    'Sijal': 'https://soundcloud.com/sijalofficial',
    'TM BAX': 'https://soundcloud.com/tmbax',
    'Tohi': 'https://soundcloud.com/tohi',
    'EpiCure': 'https://soundcloud.com/epicurex',
    'Masin': 'https://soundcloud.com/masinrap',
    'Sibab': 'https://soundcloud.com/sinabofficial',
    'Sina Mafee': 'https://soundcloud.com/sinamafee',
    'Arash Saretan': 'https://soundcloud.com/arashsaretan',
    'BONG MUSIC': 'https://soundcloud.com/user-324173625',
    "Mez'Rab": 'https://soundcloud.com/mezrab',
    'Behzad Leito': 'https://soundcloud.com/bezilei',
    'Toomaj': 'https://soundcloud.com/toomajsalehi',
    'Amin Tijay': 'https://soundcloud.com/amintijayy',
    'Armin Robber': 'https://soundcloud.com/arminrobber',
    'Majhool': 'https://soundcloud.com/officialmajhool',
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
    'avatar': './/span[contains(@class, "sc-artwork")]',
    'end_of_page': './/div[contains(@class, "paging-eof sc-border-light-top")]'
}

con = sqlite3.connect('rapgoat.db')
cur = con.cursor()
