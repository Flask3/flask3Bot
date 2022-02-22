import db
import datetime
import msg_wrapper

def dbquery_today():
    # 得到當前時間的struct_time
    t = datetime.date.today()

    print(t)

    # 月、日
    month = t.month
    day = t.day
    
    today_date = str(month) + '/' + str(day)
    # date = "4/28"
    command = "SELECT * FROM birthday WHERE birthday = %s"
    
    return msg_wrapper.today(db.query(command, today_date), today_date) 

# params:
# days: 接下來N天
def dbquery_nextNDays(nextNDays):

    # 得到今天的date
    t = datetime.date.today()
    delta_t = datetime.timedelta(days=1)

    
    t2 = datetime.datetime.now()
    today_date = str(t.month) + '/' + str(t.day)
    command = "SELECT * FROM birthday WHERE birthday = %s" # SQL command

    query_result = [] # result, list of tuples

    # 原理:
    # 迴圈跑N次 每天都+1天下去搜DB
    # 搜DB有更快的方法 但現在先這樣

    for d in range(nextNDays):
        t += delta_t
        date = str(t.month) + '/' + str(t.day)
        query_result.append(db.query(command, date))            # (UID, name, date)

    return msg_wrapper.nextNDays(query_result, today_date, nextNDays)


        

# dbquery_nextNDays(20)
# dbquery_today()   
    