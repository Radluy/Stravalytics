import os
import requests
import urllib3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


# curl -X GET "https://www.strava.com/api/v3/athlete/activities?page=1&per_page=200" -H 
#  "accept: application/json" -H  "authorization: Bearer f12ab48c5d98248cac066ec263259aa815731dad" 
# > activities.json

 # define function to get a new access token
def get_access_token(client_id, client_secret, refresh_token):

    oauth_url = 'https://www.strava.com/oauth/token'
    payload = {
        'client_id': client_id, 
        'client_secret': client_secret, 
        'refresh_token': refresh_token, 
        'grant_type': 'refresh_token', 
        'f': 'json', 
    }
    
    r = requests.post(oauth_url, data=payload, verify=False)
    
    access_token = r.json()['access_token']   
    return access_token

# define function to get your strava data
def get_data(access_token, per_page=200, page=1):
 
   activities_url = 'https://www.strava.com/api/v3/athlete/activities'
   headers = {'Authorization': 'Bearer' + access_token}
   params = {'per_page': per_page, 'page': page}
   
   data = requests.get(
       activities_url, 
       headers=headers, 
       params=params
   ).json()
 
   return data


def main():
    # set strava variables
    client_id = "46053"
    client_secret = "3a4d50bd36f4ebc2941470b9a561ecacdcc13e23"
    refresh_token = "371fa08ac0c21c4799e6eeec8d9581921fe35c0d"

    access_token = get_access_token(client_id, client_secret, refresh_token)

    # get you strava data
    max_number_of_pages = 10
    data = list()
    for page_number in tqdm(range(1, max_number_of_pages + 1)):
        page_data = get_data(access_token, page=page_number)
        if page_data == []:
            break
        data.append(page_data)
    
    # data dictionaries
    data_dictionaries = []
    for page in data:
        data_dictionaries.extend(page)
    # print number of activities
    print(f'Number of activities downloaded: {len(data_dictionaries)}')

    activities = pd.json_normalize(data_dictionaries)
    print(activities)


if __name__ == '__main__':
    main()
