import pymysql
import os
from dotenv import load_dotenv

# db settings info
load_dotenv()
db_settings = { 
    "host": os.environ.get('CLEARDB_HOST'),
    # "port": 3306,
    "user": os.environ.get('CLEARDB_USER'),
    "password": os.environ.get('CLEARDB_PW'),
    "db": os.environ.get('CLEARDB_DBNAME'),
    "charset": "utf8"
}

# connecting to database
def query(command, *param):
    print(command)
    #print(db_settings["host"], db_settings["password"], db_settings["db"], db_settings["user"], db_settings["charset"])
    try:
        conn = pymysql.connect(**db_settings)
        
        with conn.cursor() as cursor:
            
            # get data from data.py

            # df_data = data.read_data_from_csv()
            
            # SQL command
            # commandd = "INSERT INTO birthday(user_id, name, birthday)VALUES(%s, %s, %s)"

            # execute
            # for idx, rows in df_data.iterrows():
            #     print(rows['User_Id'], rows['Name'], rows['Birthday'])
            #     cursor.execute(commandd, (rows['User_Id'], rows['Name'], rows['Birthday']))
            cursor.execute(command, param)

            conn.commit()
            # result
            result = cursor.fetchall()
            print(type(result))
            return result
            
    except Exception as e:
        print(e)
        return "出錯了，如果多試幾次有錯的話可以拿以下的log回報給Flask:\n" + str(e)
