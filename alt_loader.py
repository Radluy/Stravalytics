import os
import requests
import urllib3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


from stravalib.client import Client


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

def request_access(client_id, client_secret):

    url = 'https://www.strava.com/oauth/authorize'

    data = requests.get(
        url,
        {'client_id':client_id,
        'response_typ':'code',
        'scope':'activity:read',
        'redirect_uri':'localhost'}
    ).json()

    code = data['code']
    data = requests.post(
        'https://www.strava.com/oauth/token',
        {'client_id':client_id,
        'client_secret':client_secret,
        'code':code,
        'grant_type':'authorization_code'}
    ).json()

    return data['refresh_token'] #, data['access_token']


def main():
    # set strava variables
    client_id = "46053"
    client_secret = "3a4d50bd36f4ebc2941470b9a561ecacdcc13e23"
    refresh_token = 'c0c0c329bb284be49feb3a66d388a2f4f02bcfe9'

    access_token = "f1008de91b6744fe3188e17bb31282cf96bfac40"

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
    #activities.to_json('activities/activities1.json')


if __name__ == '__main__':
    #main()
    polyline = "}onkHgkcdBBSTw@LWL{@^s@@GSGMKu@a@y@{@cByAe@g@QcAEc@IkCGw@Cu@UsAKeAUiAACM@MMKC]TWVoBzB[Xg@n@wAbCaAnB}@`Cg@dB}AhHYd@S~@Y`@cBhBk@p@CFOlAEvBObBM`@Wj@u@lAo@r@sAjAoAp@oAf@s@f@WJ[Jy@f@w@Zg@X_Ap@a@Zw@v@aAt@gAhAITEVBbBXvI?~@?PGJARAfE@x@@tDG~GO|GApAEt@?fBUvAL`FVnDp@dHF`@JT?n@dAnJhA|LDZNLP?`@CpAUpAMb@Ml@InAInAQz@IrDe@bBOfBY|D_@zAU\\OjAy@PEbAGd@IZMZW`AoA\\OVGf@EfAFn@EVGt@]`@UzAwApAgBd@c@VQXOXKfBc@|@g@b@IhAe@LCx@_@v@o@t@}@d@u@x@iBx@wA\\y@?MIg@Cc@@}@NaBZmBV_CA]Kk@Ci@CgABaCCwAIaAJPF@H@PEn@GHJDJPv@FDL?`AWBG@s@Au@Fa@D{@Lc@`@{@VUZOXK^I\\ClAB\\BNNp@XXR^d@l@bA`@~@`@hBPXNPZJVXH@d@ErAg@XYn@_@v@g@h@YTYNg@@cBEs@@MHKFCXBJErBmBh@_@bA_Ax@g@VG\\BNHHAJKDILm@HUPURM\\IROrAMTOZ]J?HCBIBUF}BZwBf@qAt@cApBqCP_@r@oBTu@VoAHw@SUICaAoBk@aBeA{Ba@eAIm@GQO{@MOIQ[wAk@mDSw@?]K]]{BAUm@_DWaBD@CWY}@WkAS_@OGC@Ge@c@o@]{@e@{@Oe@CMIQCWMUIk@IOSSKQ]iA[k@M]Gy@Dy@C[?OFULSD[I}@CiAE[?o@@UC_@D}@CkBe@XSEG?sAx@mAl@]XOG_@a@cA{B[e@WYm@Wk@Cw@JSHSLY\\e@t@EXAXZbADP@^ALEHUL_@^UNUb@w@z@Yh@c@^SX_@?i@Re@\\Wb@]ZIVQPc@PeAZUJIHGPMHs@\\QLYJ]RUZS\\QNu@VkAp@a@LeEhCk@X]Vc@h@Q\\UZMZq@bA{AlCgA~AKX]f@GXWNq@`As@h@Wn@AT"
    data = requests.get(
        'https://api.opentopodata.org/v1/srtm30m',
        params={'locations': polyline, 'samples': 5}
    ).json()
    print(data)
