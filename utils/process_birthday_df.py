"""
#   This file is mainly focused on pre-processing the dataframe
"""

import pandas as pd
from datetime import datetime, date

csv_path = "/home/nlplab/andy/flask3Bot_Test/birthday.csv"

# 就是讀那個csv成一個Dataframe
def get_birthday_df():
    print("Fetching Dataframe from .csv ...")
    df = pd.read_csv(csv_path)
    print("Finished Fetching Dataframe from .csv")

    return df


def get_yearday_list(df):
    print("Appending Yearday to DataFrame...")

    # 得到所有的yday
    yday_list = []
    for birthday in df['Birthday']:
        [month, day] = list(map(int, birthday.split('/')))
        
        d = date(2000, month, day)
        yday = d.timetuple().tm_yday
        yday_list.append(yday)
        
    # append上dataframe
    df['yday'] = yday_list

    print("Finished Appending Yearday to DataFrame.")
    return yday_list

def append_yearday():
    df = get_birthday_df()
    yday_list = get_yearday_list(df)

    df['yday'] = yday_list
    # df.to_csv(csv_path)             # save

    return df