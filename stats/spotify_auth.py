import os
import json
import base64

from dotenv import load_dotenv
import requests

from init import proxies


load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def auth_header():
    auth_string = f'{CLIENT_ID}:{CLIENT_SECRET}'
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = requests.post(url, headers=headers, data=data, proxies=proxies)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return {'Authorization': f'Bearer {token}'}


auth_header = auth_header()
