import requests 
import json
import pickle
import time
from os import path

with open('config.json', 'r') as f:
    config = json.load(f)

def get_access_token():
    STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET = config['client_id'], config['client_secret']

    if not path.exists('access_token.pickle'):
        refresh_response = requests.post(url='https://www.strava.com/api/v3/oauth/token', 
                                            data={'client_id': STRAVA_CLIENT_ID,
                                            'client_secret': STRAVA_CLIENT_SECRET,
                                            'grant_type': 'authorization_code',
                                            'code': config['code']})
        access_token = refresh_response.json()
        print(access_token)
        with open('access_token.pickle', 'wb') as f:
            pickle.dump(access_token, f)
        print('First token saved to file')

    with open('access_token.pickle', 'rb') as f:
        access_token = pickle.load(f)
        
    print('Latest access token read from file:')
    print(access_token)

    if time.time() > access_token['expires_at']:
        print('Token has expired, will refresh')
        refresh_response = requests.post(url='https://www.strava.com/api/v3/oauth/token', 
                                         data={'client_id': STRAVA_CLIENT_ID,
                                         'client_secret': STRAVA_CLIENT_SECRET,
                                         'grant_type': 'refresh_token',
                                         'refresh_token': access_token['refresh_token']})
        access_token = refresh_response.json()
        print(access_token)
        with open('access_token.pickle', 'wb') as f:
            pickle.dump(access_token, f)
        print('Refreshed token saved to file')
            
    else:
        print('Token still valid, expires at {}'
            .format(time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(access_token['expires_at']))))

    return access_token


if __name__ == '__main__':
    access_token = get_access_token()
    index = 0
    finished = False
    while not finished:
        index += 1
        response = requests.get(url='https://www.strava.com/api/v3/athlete/activities',
                                headers={'Authorization': f"Bearer {access_token['access_token']}"},
                                params={'page': index, 'per_page': 100})
        if response.text == '[]' or index == 10:
            finished = True
            continue
        with open(f"activities/activities_{index}.json", 'w') as f:
            json.dump(response.json(), f)

