import discord
import pandas

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
        for t in range(len(query_result)):

            embedded_msg_desc += "[" + str(query_result.iat[t,1]) + "](https://osu.ppy.sh/users/" + str(query_result.iat[t,0]) + ")\n"
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

def friend(name):
    msg = "每次看" + ' '.join(name) + "加好友，我都好羨慕，你長得帥，球技又好，又有錢，朋友也多，還可以加好友，隨便加個好友都讓我羨慕不已。我書讀得少，又是鄉下來的，又邊緣，沒見過多少世面，所以我只能默默的看你加好友，時不時點個讚，有時間也留個2句，這樣好像可以假裝和你很熟。"
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

# sorted = dataframe
# names = array
def ng_rank(sorted, names):
   

    embedded_msg_desc = "```分數\t次數\t名字\n-----------------------------\n"

    for idx, row in sorted.iterrows():
        print(idx)
        name = names[idx]
        points = row['Points']
        times = row['Times']
        embedded_msg_desc += f"{points}\t{times}\t{name}\n"
        
        # 處理tab
        # for i in range(12 - len(name))) :
        

        if idx > 10: break

    embedded_msg_desc += "```"
    return embedded_msg_desc

# 維基百科Page
# return 一個Embed message
def wikiPage(title, summary, page_url, img_url):
    embedded_msg_title = title
    embedded_msg_desc = summary

    print(embedded_msg_title)
    print(embedded_msg_desc)
    
    embedded_msg = discord.Embed(title = embedded_msg_title, url= page_url, description = embedded_msg_desc)

    if len(img_url) != 0:
        embedded_msg.set_thumbnail(url=img_url)

    return embedded_msg

    

    


