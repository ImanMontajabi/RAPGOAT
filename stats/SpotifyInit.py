import sqlite3

base_url: str = 'https://api.spotify.com/v1'

proxies: dict[str, str] = {
        'http': 'http://192.168.1.101:8080',
        'https': 'http://192.168.1.101:8080',
    }

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
    'Sasy': '0LkkLM2M97UEG7hi5mLn3u',
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
    'Mazzalini': '7kX7RxxyBtNQhrleSbLdOE',
    'Mahyar': '6GQ9vH1rq23GZhKYrXak9v',
    'Sina Sae': '5er043agmHdVZkWTxL0Lpk',
    'Sina Mafee': '7sqnywamVUfDallF46rrkv',
    'SoelChigini': '7lKpYA0195X6R6Ch04Zizo',
    'PaPa Asli': '68TQoNXS3hAYf7GiVA2lRd',
    'Arman Miladi': '3eqSr81gcNym9KLon3xcRR',
    'Atour': '2UfslS14H0Rv8HOzMHgUKl',
    'REZ': '1l8pQbuaP7I1jEI6g6Jnfu',
    'Sarina': '5Pi22DVdWAZN7zsSMRVtjA',
    'Justina': '1WaCguNeKSENLLlSd0vSVR',
    'Canis': '6OPdGHW0QD6WknWX2tlzJm',
    'Beatbynajwa': '3I36QJUwnZzyxnqIQJkZcy',
    'Shemrooni': '4zuyCgnXCf6stVpIZAVhPn',
    "Mez'Rab": '0VBIFNvmge2DOar9E0gPBO',
    'Rokh': '2CBqYRmN5GKCtfnV4oH472',
    'Kaboos': '7wiZdnWzfr67rEe0NMEYTA',
    'Aein': '60b0BYerc0Rg4zgmWqHD9J',
    'Daygard': '5KYtr6KsIpLwUyBFxNrYKJ',
    'Farsea': '4K296DxqeClfjk2ojL31nS',
    'Neesh Sound': '4dx4Kt2VFQICjy0ur94VEY',
    'Motreb': '3a6Xy3UWd9AA5Zs1Dw22VU',
    'Safir': '5UvGzlSJuUhWwH6NojEKy2',
    'Ben': '2WribQGnFbkNfPEXauQxts',
    'Roody': '7uIAFdTnPBN4PJIPrcwkz3',
    'Mc Tes': '0WlePVQtjzjgNFSrRt67Wz',
    'Soall': '0wjFK2K7K7k5tY9OR1G00b',
    'Soheil Sorb': '21h1VO9sCAKKC3A70VQuZN',
    'YaraPelak': '61Htw6gp56jDjEx1Ruq8YE',
    'Navid': '0g8Hw7BAsdJ2K8pKOmZzxp',
    'Vatani': '1VoK0QGxEtrDjUq4GT3yVy',
    'Amir Khalvat': '3mEVURCsHml1RKlcYjRyiy',
    'Maslak': '6ZWZCww4so7LacgTJiFTWb',
    'Daniyal': '0bRZzB4e6Yj3B64Rcbs1vd',
    'Sajadii': '6gKTNAJ5jCUX5zmkwQ19FS',
    'Moer': '4hW54ZKwP5LBMxJVGwDbLL',
    'Naaji': '0RUqk7JT0uRkJSL2VNytz2',
    'Hamed Slash': '4b2hA3kHcQPL9xi44QubYP',
    'Jarshaa': '66pDL2f3LoOqKBD6BjDvQh',
    'Sibab': '3zyb1Z44UDJ1JFzG6a3JID',
    'Sunboy': '7CdZJMlU1pOTXfIvfwLdtO',
    'Epicure': '3DU50uTJPCGLaMjVS5y8Cu',
    'Ali Ardavan': '1j0dFZXmMgFlDAcjFh490M',
    'Zakhmi': '4jE3X9cADx45YcmBiteecQ',
    'Sogand': '2mGkJsyXC8byI83UHSO4w1',
    'Dara K': '7ecobAeYEEq7KlY5MZfoAE',
    'Pooyan Ardalan': '1JSXGL2864wr8F1jtNKjoT',
    'Farshid': '5S4DYfw4jDoBxdzecDzeSn',
    'Amirali A2': '5nfrdEi3ldkgcAmHwPPRkk',
    'Tik Taak': '7AJU2n7M6XW5j1fdqTdZgI',
    'Octave': '78rQak8MeKSOo0smoQOSVE',
    'Taham': '0Wuyv5K3nFRvaQq3WIb2Ww',
    'Meraj Tehrani': '3P7vhjnuKOIu48DtWq1ICV',
    'Amir Reghab': '5gx2sR7Dcjf3CIzilV4Dgu',
    'Hesam Tiem': '6XsyaCX2jJLaS82vJoiiWi',
    'NimOG': '0sPbLrDkgOdLdHhQzr7cmU',
    'Aliz': '0kvIaNH5ddcv845mDHykJi',
    'Salii': '1CbJU98iMSwvqKAXzQ64CB',
    'Hesam Steps': '3udOiFU3fqyDV2OihyaaYh',
    'Armin Zareei': '4jUdmo1MCAWV2zEGc1uoEK',
    'Lena': '7zH1d81QnIKfrZ71VCnncv',
    'Dariu$h': '3HQedAYh7K5YW4MD108gP3',
    'Ashna': '5Z0flsrz7Q8xJ2arSoYetY',
    'Toomaj': '5mBmrpiMC2lzIWCG0MDOYx',
}

artist_ids = ','.join(list(artist_page.values()))

con = sqlite3.connect('rapgoat.db')
cur = con.cursor()
