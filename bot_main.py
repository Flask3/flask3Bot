from discord.ext import tasks, commands
import discord
import query_command as qc
import datetime
import os
import msg_wrapper
import ngCheck

bot = commands.Bot(command_prefix='!')

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
    # await ctx.channel.send("這個指令目前進廠維修中")
    # query_command.dbquery_today() 會下去撈資料 然後傳值給msg_wrapper 最後傳進來
    await ctx.channel.send(embed = qc.dbquery_today())

# [指令] 接下來N天生日的人 !next
@bot.command(name='next')
async def next (ctx, args):
    # await ctx.channel.send("這個指令目前進廠維修中")
    # print(args)

    if (int(args) > 365 or int(args) < 1):
        await ctx.channel.send("我只吃的到1 ~ 365之間的數字")
    else:
        await ctx.channel.send(embed = qc.dbquery_nextNDays(int(args)))

# [指令] 指定推播頻道 !sub
@bot.command()
async def sub(ctx):
    if ctx.message.author.guild_permissions.administrator is False:
        await ctx.channel.send("要是管理員才能用這個指令喔")
        
    else:
        print("管理員")
        channel = ctx.channel.id
        guild = ctx.guild.id
        print(channel, guild)

        await ctx.channel.send(qc.dbquery_addSubChannel(str(guild), str(channel)))

# [指令] 開台複製文 !開台 [名字]
@bot.command()
async def 開台(ctx, *args):
    print(args)
    t = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    await ctx.channel.send(msg_wrapper.stream(args, t.hour, t.minute))

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
    
    # 要先等bot process其他command
    await bot.process_commands(message) 

    # 
    if message.author == bot.user:
        return
    
    if ngCheck.ShangTouCheck(message.content) is True:
        await message.add_reaction('<:blobglare:945593586907484191>')
    # if ...


# read token, launch
TOKEN = os.environ.get('BOT_TOKEN')

bot.run(TOKEN)