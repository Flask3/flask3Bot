# osu api
from tkinter import E
import requests
from pprint import pprint
import db
import pandas as pd

API_URL = 'https://osu.ppy.sh/api/v2'
TOKEN_URL = 'https://osu.ppy.sh/oauth/token'

def get_token():
    data = {
        "client_id": 13604,
        "client_secret": "AaAQvY6rZxWPGUONaZzMykQLc6eLIcvHLe44ZBc0",
        'grant_type': 'client_credentials',
        'scope': 'public'
    }

    response = requests.post(TOKEN_URL, data=data)

    return response.json().get('access_token')

# def main():
    # print(df[df['birthday'] == '4/28']['name'])
    # for idx, row in df.iterrows():
        
    #     id = row["ID"]
    #     old_name = row["Username"]

    #     ## osu api
    #     ## get name
    #     try:
    #         name = get_osuName(id)
    #     except Exception as e:
    #         print(id)
    #         print(e)
    #         continue

    #     print("dbName:", old_name, "/ CurrentName:", name)

    #     if (old_name != name):
    #         print("Detected inconsistencies, updating database...")
    #         add_command = "UPDATE birthday SET name = \"{name}\" WHERE (user_id = \"{id}\")".format(name = name, id = id)
    #         db.query(add_command)

    # result = db.query(command)
    # df = pd.DataFrame(result)
    # print(df)

def getBadgeAmount():
    token = get_token()

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    for page in range(4,37):
        
        params = {
            'country': 'TW',
            'page': page
        }

        # id = str(id)
        try:
            response = requests.get(f"{API_URL}/rankings/osu/performance", params=params, headers=headers)
            r = response.json()
            for idx in range(0,50):
                rank = r['ranking'][0]['global_rank']

                if (rank <= 9999 or rank >= 100000): 
                    continue
                else:
                    name = r['ranking'][idx]['user']['username'] #[0].get('beatmapset')
                    id = r['ranking'][idx]['user']['id']

                    # print(name, id)
                    response = requests.get(f"{API_URL}/users/" + str(id) + "/osu", headers=headers)
                    badge_amount = len(response.json().get('badges'))

                    print(name, badge_amount)
        except Exception as e:
            print(e)    


        
        
            


    # return badge_amount

def test():
    token = get_token()

    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    params = {
                'country': 'TW',
                'page': 1
            }

    response = requests.get(f"{API_URL}/rankings/osu/performance", params=params, headers=headers)
    r = response.json()['ranking'][49]
    pprint(r)
if __name__ == '__main__':
    # id = 959763


    # response = requests.get(f"{API_URL}/users/" + str(id) + "/osu", headers=headers)
    # badge_amount = len(response.json().get('badges'))
    
    # pprint(badge_amount)
    getBadgeAmount()

    # name = "Flask"
    # id = 959763
    # add_command = "UPDATE birthday SET name = `{n}` WHERE user_id = {i}".format(n=name, i=id)

    # print(add_command)
    # db.query(add_command) 