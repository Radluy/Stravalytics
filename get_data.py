import requests 
import json
from stravalib.client import Client
import pickle
import time
from os import path

with open('config.json', 'r') as f:
    config = json.load(f)

def main():
    client = Client()
    MY_STRAVA_CLIENT_ID, MY_STRAVA_CLIENT_SECRET = config['client_id'], config['client_secret']
    
    if not path.isfile('access_token.pickle'):
        #url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID,
        #                        redirect_uri='http://127.0.0.1:5000/authorization',
        #                        scope=['read_all','activity:read_all']
        #                        )
        
        CODE = 'ffd466e4ebc24b90d39d502290664f5b878f09c7'
        access_token = client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID,
                                              client_secret=MY_STRAVA_CLIENT_SECRET,
                                              code=CODE)
        with open('access_token.pickle', 'wb') as f:
            pickle.dump(access_token, f)

    with open('access_token.pickle', 'rb') as f:
        access_token = pickle.load(f)
        
    print('Latest access token read from file:')
    print(access_token)

    if time.time() > access_token['expires_at']:
        print('Token has expired, will refresh')
        refresh_response = client.refresh_access_token(client_id=MY_STRAVA_CLIENT_ID, 
                                                client_secret=MY_STRAVA_CLIENT_SECRET, 
                                                refresh_token=access_token['refresh_token'])
        access_token = refresh_response
        with open('access_token.pickle', 'wb') as f:
            pickle.dump(refresh_response, f)
        print('Refreshed token saved to file')

        client.access_token = refresh_response['access_token']
        client.refresh_token = refresh_response['refresh_token']
        client.token_expires_at = refresh_response['expires_at']
            
    else:
        print('Token still valid, expires at {}'
            .format(time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(access_token['expires_at']))))

        client.access_token = access_token['access_token']
        client.refresh_token = access_token['refresh_token']
        client.token_expires_at = access_token['expires_at']







if __name__=='__main__':
    main()