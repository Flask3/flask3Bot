import db
import datetime
import msg_wrapper

def dbquery_today():
    # 得到當前時間的datetime
    t = datetime.datetime.utcnow() + datetime.timedelta(hours=8)

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

    # 得到今天的datetime
    t = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    delta_t = datetime.timedelta(days=1)

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

def dbquery_SubChannels():
    command = "SELECT channel_ID FROM broadcastinfo"
    return db.query(command)

def dbquery_addSubChannel(guildID, channelID):
    # 先查查有沒有加過
    # check 為第一次撈資料庫的結果，如果長度 > 0 代表該頻道曾經加過
    # 理論上check的長度只會有1個 (理論上)
    command = "SELECT channel_ID FROM broadcastinfo WHERE guild_ID = %s" 
    check = db.query(command, guildID) # tuple of tuples

    print("首次撈DB:", check)
    # 沒有
    if (len(check) == 0):
        command = "INSERT INTO broadcastinfo(guild_ID, channel_ID)VALUES(" + guildID + ", " + channelID + ")"
        r = db.query(command)
        if (type(r) is str):
            return r
        else:    
            return "成功將此頻道設為生日推播頻道 !!"

    # 有
    elif (len(check) == 1):
        if (check[0][0] == channelID): # 之前加過而且頻道一樣
            return "此頻道已經是本群的生日推播頻道了 !!"
        else:
            originalChannelID = check[0][0] # 原頻道 (之後可能用的到)
            command = "UPDATE broadcastinfo SET guild_ID=" + guildID + ", channel_ID=" + channelID + " WHERE guild_ID=" + guildID
            r = db.query(command)
            if (type(r) is str):
                return r
            else:
                return "成功將此頻道設為生日推播頻道 !!"

    # 有 但query出兩筆資料 (理論上不可能 但還是防呆)
    else:
        return "此群在資料庫中有兩個推播頻道，或者有什麼東西出錯了，請拿以下的log聯絡Flask#7106:\n" + str(check)

# params:
# user_ID: (str) message.author.ID
def dbquery_Points(user_id):
    command = "SELECT * FROM shangtoutable WHERE user_id = %s"
    check = db.query(command, user_id)

    return msg_wrapper.ShangTouPoints(check)


# params:
# user_ID: (str) message.author.ID
# points: (int) 要加的分

def dbquery_addPoints(user_ID, points):
    # 先確認有沒有資料了
    command = "SELECT * FROM shangtoutable WHERE user_id = %s"
    check = db.query(command, user_ID)

    print("首次撈DB:", check)

    # 沒加過
    if (len(check)) == 0:
        command = "INSERT INTO shangtoutable(user_id, Points, Times)VALUES(" + user_ID + ", " + str(points) + ", " + str(1) + ")"
        db.query(command)

    # 加過
    elif (len(check)) == 1:
        old_points = check[0][1] #舊分數
        old_times = check[0][2]  #舊時間

        new_points = int(old_points) + points   #新分數
        new_times = int(old_times) + 1          #新時間

        command = "UPDATE shangtoutable SET Points=" + str(new_points) + " ,Times=" + str(new_times) + " WHERE user_id=" + user_ID
        db.query(command)

    else:
        print("有出問題")

        
#print(dbquery_Points("117985615009546243"))


# print(dbquery_addSubChannel("943170635096551525", "943170635843117128"))

        

# dbquery_nextNDays(20)
# dbquery_today()   
    