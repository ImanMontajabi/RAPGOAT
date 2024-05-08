
artist_page: dict[str, str] = {
    'Mahdyar': 'https://soundcloud.com/mahdyar/tracks',
    'Poori': 'https://soundcloud.com/godpoori/tracks',
    'Dorcci': 'https://soundcloud.com/dorcci/tracks',
    'Amir_Tataloo': 'https://soundcloud.com/amirtataloo/tracks',
    'Hiphopologist': 'https://soundcloud.com/hiphopologistsoroush/tracks',
    'Johar_records': 'https://soundcloud.com/johar-records/tracks',
    'Reza_Pishro': 'https://soundcloud.com/reza-pishro-rail/tracks',
    'Bahram': 'https://soundcloud.com/bahramnouraei/tracks',
    'CatchyBeatz': 'https://soundcloud.com/tiktaak-sr/tracks',
}

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
}

js_end_of_page_condition = (
    'return window.innerHeight '
    '+ window.pageYOffset '
    '>= document.body.offsetHeight')

js_scroll_down_command = 'window.scrollBy(0, 1000)'
