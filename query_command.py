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

    print(check)
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
            db.query(command)
            if (type(r) is str):
                return r
            else:
                return "成功將此頻道設為生日推播頻道 !!"

    # 有 但query出兩筆資料 (理論上不可能 但還是防呆)
    else:
        return "此群在資料庫中有兩個推播頻道，或者有什麼東西出錯了，請拿以下的log聯絡Flask#7106:\n" + str(check)
            





# print(dbquery_addSubChannel("943170635096551525", "943170635843117128"))

        

# dbquery_nextNDays(20)
# dbquery_today()   
    