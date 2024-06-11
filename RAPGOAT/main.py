import spotify_stats
import soundcloud_stats
import tables_to_csv


if __name__ == '__main__':
    print('main() > spotify is started...')
    try:
        spotify_stats.main()
    except Exception as e:
        print(f'main() > Updating process spotify in'
              f' main.py encountered an error > {e}')
    else:
        print('main() > Spotify successfully updated')

    try:
        print('main() > soundcloud is started...')
        soundcloud_stats.main()
    except Exception as e:
        print(f'main() > Updating process soundcloud'
              f' in main.py encountered an error > {e}')
    else:
        print('main() > Soundcloud successfully updated')

    try:
        print('main() > convertor is started...')
        tables_to_csv.main()
    except Exception as e:
        print(f'main() > Updating process table to csv'
              f' in main.py encountered an error > {e}')
    else:
        print('main() > Export tables to csv successfully executed')
