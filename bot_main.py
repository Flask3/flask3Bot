from discord.ext import tasks, commands
import discord
from datetime import date, datetime, timedelta
import os
import pandas as pd
from utils.wiki import RandomWikiPage, SearchPage
from utils.update_birthday_df import get_updated_df
from utils.query_birthday import query_birthday
from utils.msg_wrapper import msg_wrap_birthday

# global var for task, probably risky but idc
changed_gap = False

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
birthday_df = pd.DataFrame()

# 當bot啟動完成時
@bot.event
async def on_ready():
    print('目前登入身份：', bot.user)
    guilds = await bot.fetch_guilds(limit=150).flatten()
    print(guilds)

    global birthday_df 
    birthday_df = get_updated_df()
    count_time.start()


# [指令] 今天生日的人 !today
@bot.command(name='today')
async def today(ctx):
    try:
        ### 今天的日期
        today_date = date.today()
        
        ### 先查今天有誰生日
        query_result = query_birthday(today_date, birthday_df)

        ### 把搜尋結果 + 今天的日期一起送給msg_wrapper
        embed_msg = msg_wrap_birthday(query_result, today_date)

        await ctx.send(embed = embed_msg)
    except (e):
        print(e)
        await ctx.send("我發生了一些問題，請聯絡Flask")

# [指令] 接下來N天生日的人 !next
# @bot.command(name='next')
# async def next (ctx, args):

#     if (int(args) > 365 or int(args) < 1):
#         await ctx.send("我只吃的到1 ~ 365之間的數字")
#     else:
#         await ctx.send(embed = qc.dbquery_nextNDays(int(args)))


# [指令] 開台複製文 !開台 [名字]
@bot.command()
async def 開台(ctx, *args):
    print("開台參數:", args)
    t = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    await ctx.send(msg_wrapper.stream(args, t.hour, t.minute))

# [指令] 加好友複製文 !加好友 [名字]
@bot.command()
async def 加好友(ctx, *args):
    await ctx.send(msg_wrapper.friend(args))

# [指令] 隨機產生一個維基百科頁面
@bot.command()
async def wiki(ctx, *args):

    # random
    if (len(args) == 0):
        await ctx.send(embed = RandomWikiPage())
    else:
        result = SearchPage(' '.join(args))
        if (type(result) == str):
            await ctx.send(' '.join(args) + "的" + result)
        else:
            await ctx.send(' '.join(args) + "的查詢結果：", embed = result)
            


########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################

# [我專用ㄉ] 送訊息到某個地方
@bot.command()
async def send(ctx, channel, *args):
    author = ctx.message.author.id
    
    if (author != 198333824633929728): 
        return
    else:
        channel = bot.get_channel(int(channel))
        msg = await channel.send(' '.join(args))
        # await msg.add_reaction("🎂")
        # await msg.add_reaction("<:blobsad:774287305354510376>")

# [推播] 每天00:00廣播誰今天生日
@tasks.loop(seconds=60)
async def count_time():
    
    t = datetime.utcnow() + timedelta(hours=8)
    print(t.hour, ':', t.minute, ':', t.second)
    
    global changed_gap
    if t.second != 0 and changed_gap == False:
        count_time.change_interval(seconds = 60 - t.second)
        changed_gap = True
    
    else:
        count_time.change_interval(seconds = 60)

    if t.hour == 0 and t.minute == 0:
        ...

        # query是:
        # - 要傳送的訊息
        # - 今天生日的人數 (為了reaction用的)

        # get today's query result

        ### 今天的日期
        today_date = date.today()
        
        ### 先查今天有誰生日
        query_result = query_birthday(today_date, birthday_df)

        ### 把搜尋結果 + 今天的日期一起送給msg_wrapper
        embed_msg = msg_wrap_birthday(query_result, today_date)

        
        # c為tuple
        channel = bot.get_channel(946105625513984040)
        sent_msg = await channel.send(embed = embed_msg)
        print("成功送訊息到", channel)

        # react emote
        if len(query_result) == 0:
            await sent_msg.add_reaction("<:blobsad:774287305354510376>")
        else:
            await sent_msg.add_reaction("🎂")

# 當有訊息時
@bot.event
async def on_message(message):
        
    if message.author == bot.user:
        return
    # 要先等bot process其他command
    await bot.process_commands(message) 

    # if ...

# @bot.event
# async def on_command_error(ctx, exception):
#     print("######################### exception #########################")
#     print(exception)
#     print("######################### exception #########################")


if __name__ == '__main__':
    # read token, launch
    TOKEN = os.environ.get('BOT_TOKEN')
    
    bot.run(TOKEN)