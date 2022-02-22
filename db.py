import pymysql
import data

# db settings info
db_settings = { 
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "40309andy",
    "db": "bday_test",
    "charset": "utf8"
}

# connecting to database
def query(command, param):
    try:
        conn = pymysql.connect(**db_settings)
        
        with conn.cursor() as cursor:
            
            # get data from data.py

            # df_data = data.read_data_from_csv()
            
            # SQL command
            # command = "INSERT INTO birthday(user_id, name, birthday)VALUES(%s, %s, %s)"

            # execute
            # for idx, rows in df_data.iterrows():
            #     print(rows['User_Id'], rows['Name'], rows['Birthday'])
            #     cursor.execute(command, (rows['User_Id'], rows['Name'], rows['Birthday']))
            cursor.execute(command, param)

            conn.commit()
            # result
            result = cursor.fetchall()
            # print(result)
            return result
            
    except Exception as e:
        print(e)