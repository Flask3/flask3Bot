import pandas

# args:
# | today_date  | date物件      |   今天的日期
# | birthday_df | dataframe     |   生日df (update過後的)

# return:
# | result      | dataframe     |   今天誰生日

def query_birthday(today_date, birthday_df):
    print("Querying birthday...")

    today_yday = today_date.timetuple().tm_yday
    result = birthday_df[birthday_df['yday'] == today_yday]

    return result