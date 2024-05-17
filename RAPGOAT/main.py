import soundcloud_stats
import spotify_stats
import tables_to_csv


if __name__ == '__main__':
    print('- spotify is started...')
    try:
        spotify_stats.main()
    except Exception as e:
        print(f'Updating process spotify in main.py encountered an error: {e}')
    else:
        print('Spotify successfully updated')

    # try:
    #     soundcloud_stats.main()
    # except Exception as e:
    #     print(f'Updating process soundcloud'
    #           f' in main.py encountered an error: {e}')
    # else:
    #     print('Soundcloud successfully updated')
    #
    # try:
    #     tables_to_csv.main()
    # except Exception as e:
    #     print(f'Updating process table to csv'
    #           f' in main.py encountered an error: {e}')
    # else:
    #     print('Tables to csv successfully updated')
