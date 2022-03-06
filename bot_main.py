from discord.ext import tasks, commands
import discord
import query_command as qc
import datetime
import os
import msg_wrapper
import ngCheck

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 當bot啟動完成時
@bot.event
async def on_ready():
    print('目前登入身份：', bot.user)
    guilds = await bot.fetch_guilds(limit=150).flatten()
    print(guilds)

    test_task.start()

# [指令] 今天生日的人 !today
@bot.command(name='today')
async def today(ctx):
    # await ctx.send("這個指令目前進廠維修中")
    # query_command.dbquery_today() 會下去撈資料 然後傳值給msg_wrapper 最後傳進來
    await ctx.send(embed = qc.dbquery_today())

# [指令] 接下來N天生日的人 !next
@bot.command(name='next')
async def next (ctx, args):
    # await ctx.send("這個指令目前進廠維修中")
    # print(args)

    if (int(args) > 365 or int(args) < 1):
        await ctx.send("我只吃的到1 ~ 365之間的數字")
    else:
        await ctx.send(embed = qc.dbquery_nextNDays(int(args)))

# [指令] 指定推播頻道 !sub
@bot.command()
async def sub(ctx):
    if ctx.message.author.guild_permissions.administrator is False:
        await ctx.send("要是管理員才能用這個指令喔")
        
    else:
        print("管理員")
        channel = ctx.channel.id
        guild = ctx.guild.id
        print(channel, guild)

        await ctx.send(qc.dbquery_addSubChannel(str(guild), str(channel)))

# [指令] 開台複製文 !開台 [名字]
@bot.command()
async def 開台(ctx, *args):
    print("開台參數:", args)
    t = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    await ctx.send(msg_wrapper.stream(args, t.hour, t.minute))

@bot.command()
async def 加好友(ctx, *args):
    await ctx.send(msg_wrapper.friend(args))

# [指令] 得到上頭分數 !ngstats
@bot.command()
async def 上頭(ctx, *args):
    author = ctx.message.author

    if (len(args) == 0):
        await ctx.send(author.display_name + qc.dbquery_Points(author.id))
    elif (len(args) == 1): # 查別人的
        if ctx.message.mentions:
            raw_id = "".join(args)  # with <@!.....>
            id = raw_id[3:-1] if "<@!" in raw_id else raw_id[2:-1]
            name = bot.get_user(int(id)).display_name
            print("display name:", name)
            await ctx.send(name + " " + qc.dbquery_Points(id))
        else:
            await ctx.send("請使用 !上頭 @用戶")
    else: #大於ㄧ個args
        await ctx.send("後面只能帶一個參數")
    
    


# [推播] 每天00:00廣播誰今天生日
@tasks.loop(seconds=60)
async def test_task():
    
    t = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    # print(t.hour, ':', t.minute)

    if t.hour == 0 and t.minute == 0:
        # 之後會改
        msg = qc.dbquery_today()
        channels = qc.dbquery_SubChannels() # tuple of tuples
        
        for c in channels:
            # c為tuple
            channel = bot.get_channel(int(c[0])) 
            await channel.send(embed = msg)
            print("成功送訊息到", channel)

# 當有訊息時
@bot.event
async def on_message(message):
        
    if message.author == bot.user:
        return
    # 要先等bot process其他command
    await bot.process_commands(message) 
    
    msg = message.content.replace("睪", "高") if "睪" in message.content else message.content
    ShangTouPoint = ngCheck.ShangTouCheck(msg)
    if ShangTouPoint > 0:
        await message.add_reaction('<:blobglare:945593586907484191>')
        # SQL
        qc.dbquery_addPoints(str(message.author.id), ShangTouPoint)

    # if ...

@bot.event
async def on_command_error(ctx, exception):
    print("######################### exception #########################")
    print(exception)
    print("######################### exception #########################")

# read token, launch
TOKEN = os.environ.get('BOT_TOKEN')

bot.run(TOKEN)