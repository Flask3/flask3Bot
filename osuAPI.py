# osu api
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

def main():
    # 拿dataframe
    command = "select * from birthday"
    result = db.query(command)
    # , columns=['ID', 'Username', 'birthday', 'month']
    df = pd.DataFrame(result, columns=['ID', 'name', 'birthday', 'month', 'day'])

    print(df[df['birthday'] == '4/28']['name'])
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

def get_osuName(id):
    token = get_token()

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    params = {
        'key': int(id)
    }

    id = str(id)
    response = requests.get(f"{API_URL}/users/" + id, params=params, headers=headers)
    name = response.json().get('username') #[0].get('beatmapset')


    return name

if __name__ == '__main__':
    main()

    # name = "Flask"
    # id = 959763
    # add_command = "UPDATE birthday SET name = `{n}` WHERE user_id = {i}".format(n=name, i=id)

    # print(add_command)
    # db.query(add_command) 