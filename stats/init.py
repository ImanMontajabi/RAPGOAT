import sqlite3

base_url = 'https://api.spotify.com/v1'

proxies = {
        'http': 'http://192.168.1.105:8080',
        'https': 'http://192.168.1.105:8080',
    }

artist_page = {
    'Shapur': '6kbLiMnkNZHlvMpTv5iK9h',
    'Hiphopologist': '45YMrIBH74j8e2wNlRSSdK'
}

artist_ids = ','.join(list(artist_page.values()))

con = sqlite3.connect('rapgoat.db')
cur = con.cursor()

"""
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
'Amir Tataloo': '5CEosSs2y4M9THNGI6mej8'
"""