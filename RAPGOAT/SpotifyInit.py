from sys import exit
import sqlite3

base_url: str = 'https://api.spotify.com/v1'

proxies: dict[str, str] = {
        'http': 'http://192.168.1.101:9090',
        'https': 'http://192.168.1.101:9090',
    }

try:
    con = sqlite3.connect('RapGoat.db')
    cur = con.cursor()
except sqlite3.DatabaseError as e:
    print(f'Database connection was unsuccessful: {e}')
    exit(1)

artist_page: dict[str, str] = {
    'Fadaei': '5aWL79DpD45MzDMwCTZqsN',
    'Shapur': '6kbLiMnkNZHlvMpTv5iK9h',
    'Quf': '1LyLFeSDfvcGc8K6caTl05',
    'Hiphopologist': '45YMrIBH74j8e2wNlRSSdK',
    'Vinak': '1sKlyO3CCEvjeTN6Uck39S',
    'Poori': '5uEEhLt2ETeApnvs40MOxk',
    'Hichkas': '2X90kCLyxyPeJ5nynJGbvT',
    '021kid': '578d6XzxI0bCSi49dK0Qpx',
    '021g': '6U5mXNse56YUIYMdoPexGj',
    'Sajad Shahi': '3VzZOmXc8pZRfNxoiliE1A',
    'Reza Pishro': '0u4qrFczDmAsJesHPgbnru',
    'Amir Tataloo': '5CEosSs2y4M9THNGI6mej8',
    'Mehrad Hidden': '0jCVTRvQkILbJvpviTpvd1',
    'Yas': '7b8pXheEOc28fyFJnQzqmL',
    'Eycin': '3jXjY8STCMtS1T6d7xdw0r',
    'Koorosh': '1UjD9VWeqDDlDSvNlnFTdl',
    'Arta': '6gPKjPIXbBBnuLyLEq79Sz',
    'Sepehr Khalse': '2SFwcduI9cdZsG6UxnBm3C',
    'Gdaal': '7mGDv3CYlPghTIWzE6tOpv',
    'Dalu': '0BX4QfYgm05DzBJyA6hqVJ',
    'Amin Tijay': '3JS9sHeI06RtolBR5s5O0L',
    'Chvrsi': '7Hj58arwOvp6exTny9r5Ie',
    'Young Sudden': '0PGOS7VHyBpbxRhWgO4tZB',
    'Ho3ein': '5vVveQB8n4kETe67waTS3t',
    'Ahood': '6RI9dCO9scZq1ZaEsNj0FK',
    'Ali Geramy': '5C2k7gNXFOiW09K3nCjBmq',
    'Dorcci': '6jj9lOTeZC28LkPoXK9hiT',
    'Matin Fattahi': '4ymFcVI8Yr4vK8xx2ybmLI',
    'Pouriya Adroit': '7lH1vL9VXRSTutpZ0JOyim',
    'Tiem': '2ZgLpNVB2qQTifvz3l8xIY',
    'Putak': '1VURARf1CD5wkFgIexChyq',
    'Ali Sorena': '1gNqCEatbX4cKskpTzyAsI',
    'Tohi': '7pBXdJN9S9N9nNifjPixET',
    'Catchybeatz': '25JIQIFASUvrcnzFL9CQhZ',
    'Hoodadk4': '1wJm5nKEUlhdV48hMMwzAm',
    'Shayea': '3QNGoF6VzVNnkpjJDT3NHq',
    'Sadegh': '1PgsdK1Ll4oK28g6KLPOg1',
    'Sasy': '0LkkLM2M97UEG7hi5mLn3u',
    'Shahin Najafi': '1W5u8Bz2yimyuuI8QNYsNO',
    'Paya': '62AW9VlTxtw554o2Sll0fK',
    'Mahdyar': '0FNHT8Xv2B3q4SoBAXgnq2',
    'Ashkan Kagan': '2D66FABcMx1DcjVtrVAeHL',
    'Saeed Dehghan': '4Fur00fBe3AKKXw7tlVXmr',
    'SoelChigini': '7lKpYA0195X6R6Ch04Zizo',
    'Atour': '2UfslS14H0Rv8HOzMHgUKl',
    'Epicure': '3DU50uTJPCGLaMjVS5y8Cu',
    'Hesam Tiem': '6XsyaCX2jJLaS82vJoiiWi',
    'NimOG': '0sPbLrDkgOdLdHhQzr7cmU',
    'Dariu$h': '3HQedAYh7K5YW4MD108gP3',
}

artist_ids = ','.join(list(artist_page.values()))
