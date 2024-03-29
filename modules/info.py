import discord
from discord.ext import commands

import json

from discord.ext.commands.core import command
from utills.u_mongo import Mongo
import datetime

import time
import psutil
import cpuinfo
from cpuinfo import get_cpu_info
import platform
import distro

async def lang_text(guild_id):
    record = await Mongo.get_record('cfg_ser','guild_id',str(guild_id))
    final_lang= record['lang']
    with open('language.json','r', encoding='utf-8') as file:
        text = json.loads(file.read())
        return text[final_lang]

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, user = None):
        if user == "server" or user == str(ctx.author.guild.id):
            guild = ctx.guild
            webp = guild.icon_url_as(format=None, static_format='webp', size=2048)
            png = guild.icon_url_as(format=None, static_format='png', size=2048)
            jpg = guild.icon_url_as(format=None, static_format='jpg', size=2048)
            em = discord.Embed(title=f'{guild.name}')
            em.set_image(url = guild.icon_url)

        else:
            idd = user or str(ctx.author.id)
            try:
                member = await commands.MemberConverter().convert(ctx, idd)
            except:
                member = await self.bot.fetch_user(int(idd))

            em = discord.Embed(title = f'{member.name}#{member.discriminator}', color = member.color)
            webp = member.avatar_url_as(format=None, static_format='webp', size=2048)
            png = member.avatar_url_as(format=None, static_format='png', size=2048)
            jpg = member.avatar_url_as(format=None, static_format='jpg', size=2048) 
            em.set_image(url=member.avatar_url)

        em.add_field(name="Link as", value=f"[webp]({webp}) | [jpg]({jpg}) | [png]({png})")
        await ctx.send(embed = em)

    @commands.command()
    async def info(self, ctx, arg = None):
        text= (await lang_text(ctx.message.guild.id))['info']

        if arg == "server":
            guild = ctx.author.guild
            lvl= str(guild.verification_level)

            if lvl == "extreme":
                lvl1 = text['extreme']
                color = 0xff0000
                pass
            elif lvl == "high":
                lvl1 = text['high']
                color = 0xffa500 
                pass
            elif lvl == "medium":
                lvl1 = text['medium']
                color = 0xffff00
                pass
            elif lvl == "low":
                lvl1 = text['low']
                color = 0x329932
                pass
            else:
                lvl1 = text['none']
                color = 0x00000

            name = guild.name
            idd= guild.id
            icon = guild.icon_url
            owner = guild.owner
            count= guild.member_count
            region= str(guild.region)
            create_ac= guild.created_at.strftime('**[%d-%m-%Y]** `%H:%M:%S`')
            ib= 0
            im= 0

            for listt in guild.members:

                if listt.bot == False:
                    
                    im = im+1
                elif listt.bot == True:
                    ib = ib+1

            emServer = discord.Embed(title=name, color = color)
            emServer.add_field(name="Create", value= create_ac, inline= True)
            emServer.add_field(name= "Owner", value=owner, inline=False)
            emServer.add_field(name="User/Bot/Member", value=f"{im}/{ib}/{count}", inline= True)
            emServer.add_field(name="Region",value=region.title(), inline=True)
            emServer.add_field(name="Verification level",value =(lvl1),inline= False)   
            emServer.set_thumbnail(url=icon)
            emServer.set_footer(text=f"ID: {idd}")
            await ctx.send(embed=emServer)   

        elif arg == "status":
            activity = ctx.author.activity
            text_activity = text['activity']

            if activity.type[0] == "custom":
                name = text_activity['name'].format(activity.name)
                
                if activity.emoji == None:
                    emoji = ""
                else:
                    emoji = text_activity['emoji'].format(activity.emoji)

                em = discord.Embed(title = "Custom Status", description = f"{name}\n{emoji}", color = ctx.author.color)
                await ctx.send(embed = em)

            elif activity.name == "Spotify":
                time_all = datetime.datetime.utcfromtimestamp(activity.duration.seconds).strftime('%H:%M:%S')
                time2 = int(activity.end.timestamp()) - int(datetime.datetime.now().timestamp())
                spotify_end = datetime.datetime.utcfromtimestamp(time2).strftime('%H:%M:%S')
                
                em = discord.Embed(
                    title = activity.name, 
                    description = (text['spotify']).format(activity.name, activity.title, activity.artist, activity.album, time_all, spotify_end),
                    color = activity.color)
                em.set_thumbnail(url = activity.album_cover_url)
                await ctx.send(embed = em)
            
            elif activity.type[0] == "playing":
                name = text_activity["name"].format(activity.name)
                
                try:
                    app_id = activity.application_id
                except AttributeError:
                    app_id = ''
                else:
                    app_id = text_activity['app_id'].format(activity.application_id)

                try:
                    details = activity.details
                except AttributeError:
                    details = ''
                else:
                    if details == None:
                        details = ''
                    else:
                        details = (text_activity['details']).format(details)

                try:
                    state = activity.state
                except AttributeError:
                    state = ''
                else:
                    if state == None:
                        state = ''""''
                    else:
                        state = (text_activity['state']).format(state)

                try:
                    large_image = activity.large_image_url
                except AttributeError:
                    large_image = None
                
                try: 
                    small_image = activity.small_image_url
                except AttributeError:
                    small_image = None
                
                try:
                    large_image_text = activity.large_image_text
                except AttributeError:
                    large_image_text = None
                
                try:
                    small_image_text = activity.small_image_text
                except AttributeError:
                    small_image_text = None

                if small_image != None or small_image_text != None:
                    small_image_full = f'__Smaill Image:__ [{activity.small_image_text}]({small_image})\n'
                elif small_image == None and small_image_text == None:
                    small_image_full = ''


                if large_image != None or large_image_text != None:
                    large_image_full = f"__Large Image:__ [{activity.large_image_text}]({large_image})\n"
                elif large_image == None and large_image_text == None:
                    large_image_full = ''

                if large_image == None:
                    large_image = ''
                if small_image == None:
                    small_image = ''
                
                try:
                    activity.timestamps['start']
                except AttributeError:
                    duration = ''
                else:
                    dr1 = str(activity.timestamps['start'])[:10]
                    dr2 = round(datetime.datetime.now().timestamp())
                    fl =  datetime.datetime.utcfromtimestamp(dr2 - int(dr1)).strftime('%H:%M:%S')
                    duration = text_activity['duration']['text'].format(fl, '')

                em = discord.Embed(
                    title = activity.name,
                    description = f'{name}{details}{state}{large_image_full}{small_image_full}{duration}')

                em.set_thumbnail(url = large_image)
                em.set_footer(text= app_id, icon_url = small_image)
                await ctx.send(embed = em)  


        elif arg == "bot":
        #Total
            tG = 0
            tM = 0
            for guild in self.bot.guilds:
                tG = tG + 1
                try:
                    tM = int(guild.member_count) + tM
                except:
                    pass
        #CPU
            cpu_count= psutil.cpu_count()
            cpu_name= get_cpu_info()['brand_raw']
        #RAM
            totalmem= psutil.virtual_memory().total //1024//1024
            used= psutil.virtual_memory().used  //1024//1024
            freemem= psutil.virtual_memory().available //1024//1024

        #OS
            nOS= platform.uname().system
            vOS= platform.uname().release
            os = platform.system()
            if os == "Linux":
                p1= distro.linux_distribution()[0]
                p2= distro.linux_distribution()[1]
                p3= distro.linux_distribution()[2]
            elif os == "Windows":
                p1= platform.win32_ver()[0]
                p2= ""
                p3= platform.win32_ver()[1]
        #Время работы
            time_now = datetime.datetime.now().timestamp()
            psutil_day = int(datetime.datetime.fromtimestamp(time_now - psutil.boot_time()).strftime("%d")) - 1
            boot_time = datetime.datetime.fromtimestamp(time_now - psutil.boot_time()).strftime("%H:%M:%S")
            boot_time = (f"{psutil_day} days, {boot_time}")
        #Работа Бота
            psutil_day = int(datetime.datetime.fromtimestamp(time_now - int(psutil.Process().create_time())).strftime("%d")) - 1
            boot_time_bot = datetime.datetime.fromtimestamp(time_now - int(psutil.Process().create_time())).strftime("%H:%M:%S")
            boot_time_bot = (f"{psutil_day} days, {boot_time_bot}")

            em1= discord.Embed(title = 'Statistic Bot',
            description= f"""**Tag:** __{self.bot.user}__
                —>**Id:** __{self.bot.user.id}__
                **Total Guild:** __{tG}__
                **Total Member:** __{tM}__
                **Python:** __{platform.python_version()}__ (**discord.py:** __{discord.__version__}__)
                **System**
                —>**CPU:** __{cpu_name}({cpu_count}x Сore)__
                —>**RAM:** __{used}Mb/{freemem}Mb/{totalmem}Mb__
                —>**OS:** {nOS} {platform.architecture()[0]} (**{p1.title()} {p2}** {p3}) [{vOS}]
                **Uptime**
                —>**System:** __{boot_time}__
                —>**Bot:** __{boot_time_bot}__""")
            em1.set_thumbnail(url = self.bot.user.avatar_url)
                
            await ctx.send(embed = em1)

        else:
            idd = arg or str(ctx.author.id)
            try:
                user = await commands.MemberConverter().convert(ctx, idd)
            except:
                user = await self.bot.fetch_user(int(idd))


            if user == None:
                em = discord.Embed(title = "Error", description = "User no found", color = 0xff0000)
                await ctx.send(embed = em)
            else:
                create_time = user.created_at.strftime('`[%d-%m-%Y]` `%H:%M:%S`')
                try:
                    join_date= user.joined_at.strftime('`[%d-%m-%Y]` `%H:%M:%S`')
                except AttributeError:
                    join_date = ""
                else:
                    join_date = f"__Join Date:__ {join_date}\n"
                color = user.colour
                color = str(color)[1:7]
                if color == "000000":
                    color = ""
                else:
                    color = f"__Color:__ **{color}\n**"
                em1= discord.Embed(
                    description= f'''__Name:__ **{user}**
                __ID:__ **{user.id}**
                __Create Time:__ {create_time}
                {join_date}{color}''',
                    colour = user.color)
                em1.set_author(name=f"User Info",icon_url = ctx.author.avatar_url)
                em1.set_thumbnail(url= user.avatar_url)
                await ctx.send(embed = em1)



    @avatar.error
    async def avatar_error(self, ctx, error):
        text = (await lang_text(ctx.message.guild.id))['errors']
        em = discord.Embed(title= "Error",
        description = (text['no_found_user']).format(ctx.args[2]),
        color = 0xe5e500)
        await ctx.send(embed = em)            


def setup(bot):
    bot.add_cog(Info(bot))