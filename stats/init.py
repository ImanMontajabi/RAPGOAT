import sqlite3

base_url = 'https://api.spotify.com/v1'

proxies = {
        'http': 'http://192.168.1.105:8080',
        'https': 'http://192.168.1.105:8080',
    }

artist_page = {
    'Fadaei': '5aWL79DpD45MzDMwCTZqsN'
}

artist_ids = ','.join(list(artist_page.values()))

con = sqlite3.connect('rapgoat.db')
cur = con.cursor()


'''
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
'Ali Owj': '1QLYXMAVVrk6WLYeARVBKn',
'Sohrab Mj': '2B4DnBz9uzJN5nPgLEHCt7',
'Eycin': '3jXjY8STCMtS1T6d7xdw0r',
'Koorosh': '1UjD9VWeqDDlDSvNlnFTdl',
'Arta': '6gPKjPIXbBBnuLyLEq79Sz',
'Sami Low': '4mST4sikQtpiH5dIkRxaCT',
'Sepehr Khalse': '2SFwcduI9cdZsG6UxnBm3C',
'Erfan': '1yPzb9mqugowOfUs2vIOgL',
'Gdaal': '7mGDv3CYlPghTIWzE6tOpv',
'Hamid Sefat': '0hnMiXDRQxJYr0TuSpCuiI',
'Dalu': '0BX4QfYgm05DzBJyA6hqVJ',
'Amin Tijay': '3JS9sHeI06RtolBR5s5O0L',
'Chvrsi': '7Hj58arwOvp6exTny9r5Ie',
'Young Sudden': '0PGOS7VHyBpbxRhWgO4tZB',
'Alireza Jj': '3tecdksDTajgP8xxkuDgyJ',
'Sijal': '5F0BGBdSL945Bzxrq8aGbn',
'Saman Wilson': '2CwNkCPsqVs4jRRpFJxR3H',
'Ho3ein': '5vVveQB8n4kETe67waTS3t',
'Masin': '0QKP5an5PwgDyG0QPsLRxe',
'Bbal': '5pfml2Js6lEgUgefTRE4ec',
'Ahood': '6RI9dCO9scZq1ZaEsNj0FK',
'Ali Geramy': '5C2k7gNXFOiW09K3nCjBmq',
'Mamazi': '4L42EENVSu2ZE8cwhVVeh8',
'Dorcci': '6jj9lOTeZC28LkPoXK9hiT',
'Tamara': '3PAFlEdGkJz6qNNh5f2uxM',
'Matin Fattahi': '4ymFcVI8Yr4vK8xx2ybmLI',
'Pouriya Adroit': '7lH1vL9VXRSTutpZ0JOyim',
'Tiem': '2ZgLpNVB2qQTifvz3l8xIY',
'TM Bax': '0RN2n6EdV90CQmfhfxqv0f',
'Poobon': '4hdsAoRTkGU11DynAg7iTw',
'Parsalip': '3HdBTStjnFIoDKFSUQ0V1H',
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
'Sasy': '0LkkLM2M97UEG7hi5mLn3u'
'Shahin Najafi': '1W5u8Bz2yimyuuI8QNYsNO',
'Paya': '62AW9VlTxtw554o2Sll0fK',
'Mahdyar': '0FNHT8Xv2B3q4SoBAXgnq2',
'Ashkan Kagan': '2D66FABcMx1DcjVtrVAeHL',
'Saeed Dehghan': '4Fur00fBe3AKKXw7tlVXmr',
'Imanemun': '6NY0pmZsboMa0qoHDswbdv',
'Saretan': '5bal1WJousVM8g27E8fhmo',
'Farshad': '2dMpZWdHDNwkgthq5z0RE2',
'Bamdad': '28PKM2pUlv1CXnc98XFVrY',
'RiRi': '2sGxtw89iJP7EgucbwlKUv',
'I.Da': '3yCy9BtcIjUfrOwqXsz2Th',
'Arma': '3CKuPYmXvMJ0URm90z8cKD',
'Yasna': '3jsEU8O3FGj4cnbL1qicau',
'Ali T': '4AoHhIECjOXoAgdnb4SBjV',
'Parsa Simpson': '5wvDF7PuwGQuohqPkW6cdB',
'Lowke!': '4K7zSelumgDWRnyO16yDJa',
'Hooman': '6UJS43T8NPhmWmmpFY0hzP',
'Isam': '2oJHjkrwOU6fFBoDiW1jDP',
'Nasim': '4RuefpFp7IwhlQW8Cii86Q',
'Madgal': '59c59jqSTrVDZhSyrnaCLz',
'''