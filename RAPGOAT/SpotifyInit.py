from sys import exit
import sqlite3

base_url: str = 'https://api.spotify.com/v1'

proxies: dict[str, str] = {
        'http': 'http://192.168.1.101:8080',
        'https': 'http://192.168.1.101:8080',
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
    'Sohrab Mj': '2B4DnBz9uzJN5nPgLEHCt7',
    'Eycin': '3jXjY8STCMtS1T6d7xdw0r',
    'Koorosh': '1UjD9VWeqDDlDSvNlnFTdl',
    'Arta': '6gPKjPIXbBBnuLyLEq79Sz',
    'Sami Low': '4mST4sikQtpiH5dIkRxaCT',
    'Sepehr Khalse': '2SFwcduI9cdZsG6UxnBm3C',
    'Gdaal': '7mGDv3CYlPghTIWzE6tOpv',
    'Hamid Sefat': '0hnMiXDRQxJYr0TuSpCuiI',
    'Dalu': '0BX4QfYgm05DzBJyA6hqVJ',
    'Amin Tijay': '3JS9sHeI06RtolBR5s5O0L',
    'Chvrsi': '7Hj58arwOvp6exTny9r5Ie',
    'Young Sudden': '0PGOS7VHyBpbxRhWgO4tZB',
    'Alireza Jj': '3tecdksDTajgP8xxkuDgyJ',
    'Sijal': '5F0BGBdSL945Bzxrq8aGbn',
    'Ho3ein': '5vVveQB8n4kETe67waTS3t',
    'Masin': '0QKP5an5PwgDyG0QPsLRxe',
    'Bbal': '5pfml2Js6lEgUgefTRE4ec',
    'Ahood': '6RI9dCO9scZq1ZaEsNj0FK',
    'Ali Geramy': '5C2k7gNXFOiW09K3nCjBmq',
    'Dorcci': '6jj9lOTeZC28LkPoXK9hiT',
    'Tamara': '3PAFlEdGkJz6qNNh5f2uxM',
    'Matin Fattahi': '4ymFcVI8Yr4vK8xx2ybmLI',
    'Pouriya Adroit': '7lH1vL9VXRSTutpZ0JOyim',
    'Tiem': '2ZgLpNVB2qQTifvz3l8xIY',
    'Poobon': '4hdsAoRTkGU11DynAg7iTw',
    'Putak': '1VURARf1CD5wkFgIexChyq',
    'Behzad Leito': '4zNEj5bkHE0kNSpfIwgdvu',
    'Ali Sorena': '1gNqCEatbX4cKskpTzyAsI',
    'Bahram': '57LWeRc7ybAWTsS2vS1GA7',
    'Tohi': '7pBXdJN9S9N9nNifjPixET',
    'PapaBoyz': '6wM6v2jCn7AXZREd2syCt3',
    'Catchybeatz': '25JIQIFASUvrcnzFL9CQhZ',
    'Hoodadk4': '1wJm5nKEUlhdV48hMMwzAm',
    'Merzhak': '6JRWq2ja4nHQVqUnLtWarc',
    'Shayea': '3QNGoF6VzVNnkpjJDT3NHq',
    'Sadegh': '1PgsdK1Ll4oK28g6KLPOg1',
    'Sasy': '0LkkLM2M97UEG7hi5mLn3u',
    'Shahin Najafi': '1W5u8Bz2yimyuuI8QNYsNO',
    'Paya': '62AW9VlTxtw554o2Sll0fK',
    'Mahdyar': '0FNHT8Xv2B3q4SoBAXgnq2',
    'Ashkan Kagan': '2D66FABcMx1DcjVtrVAeHL',
    'Saeed Dehghan': '4Fur00fBe3AKKXw7tlVXmr',
    'Sina Sae': '5er043agmHdVZkWTxL0Lpk',
    'Sina Mafee': '7sqnywamVUfDallF46rrkv',
    'SoelChigini': '7lKpYA0195X6R6Ch04Zizo',
    'Atour': '2UfslS14H0Rv8HOzMHgUKl',
    'REZ': '1l8pQbuaP7I1jEI6g6Jnfu',
    'Canis': '6OPdGHW0QD6WknWX2tlzJm',
    'Safir': '5UvGzlSJuUhWwH6NojEKy2',
    'Amir Khalvat': '3mEVURCsHml1RKlcYjRyiy',
    'Daniyal': '0bRZzB4e6Yj3B64Rcbs1vd',
    'Sajadii': '6gKTNAJ5jCUX5zmkwQ19FS',
    'Epicure': '3DU50uTJPCGLaMjVS5y8Cu',
    'Hesam Tiem': '6XsyaCX2jJLaS82vJoiiWi',
    'NimOG': '0sPbLrDkgOdLdHhQzr7cmU',
    'Dariu$h': '3HQedAYh7K5YW4MD108gP3',
    'Pouriaa': '4ieDlQoZpwiWJmL5OytsQW',
    'Kaveh': '6fR4bmvdi3nLYzLji6JVK1',
}

artist_ids = ','.join(list(artist_page.values()))
