import discord

# 處理要送出的訊息
# 會用到的指令：推播、!today
def today(query_result, today_date): # 前面是tuple 後面是日期

    # title : 今天 (日期) 生日的玩家有:
    # description : ID_1(osu profile link)
    #               ID_2(osu profile link)
    #               或者沒有人
    
    embedded_msg_title = "今天 (" + today_date + ") 生日的玩家有：\n"
    embedded_msg_desc = ""

    if (len(query_result) != 0):
        for t in query_result:
            embedded_msg_desc += "[" + t[1] + "](https://osu.ppy.sh/users/" + t[0] + ")\n"
    else: # 今天沒人生日
        embedded_msg_desc = "沒有人"

    embed_msg = discord.Embed(title = embedded_msg_title, description = embedded_msg_desc)

    print(embedded_msg_title, embedded_msg_desc)

    return embed_msg


# 會用到的指令：!next N
def nextNDays(query_result, today_date, nextNDays):

    # title : 接下來 (N) 天 生日的玩家有:
    # description : ID_1(osu profile link)
    #               ID_2(osu profile link)
    #               或者沒有人
    
    embedded_msg_title = "今天 (" + today_date + ") 接下來 " + str(nextNDays) + " 日內生日的玩家有：\n"
    embedded_msg_desc = ""

    if (len(query_result) != 0):
        for q in query_result:
            for t in q:
                # 沒辦法加空格 只好這樣ㄌ
                embedded_msg_desc += t[2] + " [" + t[1] + "](https://osu.ppy.sh/users/" + t[0] + ")" + "\n"
    else: # 都沒人生日
        embedded_msg_desc += "沒有人"

    embed_msg = discord.Embed(title = embedded_msg_title, description = embedded_msg_desc)

    print(embedded_msg_title, embedded_msg_desc)

    return embed_msg

# 會用到的指令：!開台
def stream(name, hour, min):

    msg = "在今天"
    if hour == 0:
        msg += "半夜"
        hour += 12
    elif hour >= 1 and hour <= 5:
        msg += "半夜"
    elif hour >= 6 and hour <= 11:
        msg += "早上"
    elif hour == 12:
        msg += "中午"
    elif hour >= 13 and hour <= 17:
        hour -= 12
        msg += "下午"
    else:
        hour -= 12
        msg += "晚上"

    new_name = ' '.join(name)
    msg += str(hour) + ':' 
    msg += str(min) if len(str(min)) > 1 else "0" + str(min) # 格式化分鐘
    msg += "的時候，我最喜歡的實況主"
    msg += new_name
    msg += "，居然還沒開臺，我心裡想著，今天是不是不會開臺，我一直等待著discord的訊息跳出來，就是為了可以看一場直播，這時我心裡想著，會不會要等到明天，想著想著，眼淚就流下來了。想著，我是不是又要等到明天。"

    print(msg)
    return msg

def ShangTouPoints(check): #tuple of tuples
    points = 0
    times = 0

    if len(check) == 1:
        points = int(check[0][1])
        times = int(check[0][2])
    elif len(check) == 0:
        pass
    else:
        print("可能怪怪的")
    
    msg = "上頭分數: " + str(points) + " 上頭次數: " + str(times)

    return msg



