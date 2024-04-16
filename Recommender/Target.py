import requests
import json
def get_lo_hi(handle):
    url = 'https://codeforces.com/api/user.info?handles=' + handle
    try:
        response = requests.get(url)
        x=response.json()

    except:
        print("Not found")
        return (-1,-1)
    current=0
    for con in x['result']:
        if 'maxRating' in con:
            current=int(con['maxRating'])

    target=0
    if current>=1900:
        current=1900
        target = 2100
    elif current>=1600:
        current=1600
        target = 1900
    elif current>=1400:
        current=1400
        target = 1600
    else:
        current=0
        target = 1200
    return (current, target)
