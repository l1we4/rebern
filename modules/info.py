import discord
from discord.ext import commands

import json
from utills.u_mongo import Mongo
import datetime

import time
import psutil
import cpuinfo
from cpuinfo import get_cpu_info
import platform

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
            idd = user or str(ctx.author)
            try:
                member = await self.bot.fetch_user(int(idd))
            except:
                member = await commands.UserConverter().convert(ctx, idd)

            em = discord.Embed(title=f'{member.name}#{member.discriminator}', color= member.color)
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
                pass
            elif lvl == "high":
                lvl1 = text['high']
                pass
            elif lvl == "medium":
                lvl1 = text['medium']
                pass
            elif lvl == "low":
                lvl1 = text['low']
                pass
            else:
                lvl1 = text['none']

            name = guild.name
            idd= guild.id
            icon = guild.icon_url
            owner = guild.owner
            count= guild.member_count
            region= guild.region
            create_ac= guild.created_at.strftime('**[%d-%m-%Y]** `%H:%M:%S`')
            ib= 0
            im= 0

            for listt in guild.members:

                if listt.bot == False:
                    
                    im = im+1
                elif listt.bot == True:
                    ib = ib+1

            emServer = discord.Embed(title=name)
            emServer.add_field(name="Create", value= create_ac, inline= True)
            emServer.add_field(name= "Owner", value=owner, inline=False)
            emServer.add_field(name="User/Bot/Member", value=f"{im}/{ib}/{count}", inline= True)
            emServer.add_field(name="Region",value=region, inline=True)
            emServer.add_field(name="Verification level",value =(lvl1),inline= False)   
            emServer.set_thumbnail(url=icon)
            emServer.set_footer(text=f"ID: {idd}")
            await ctx.send(embed=emServer)   
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
                p1= platform.linux_distribution()[0]
                p2= platform.linux_distribution()[1]
                p3= platform.linux_distribution()[2]
            elif os == "Windows":
                p1=platform.win32_ver()[0]
                p2=""
                p3=platform.win32_ver()[1]
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
            idd = arg or str(ctx.author.mention)
            try:
                ping = await commands.UserConverter().convert(ctx, idd)
            except:
                user = await self.bot.fetch_user(int(idd))
            else:
                user = discord.utils.get(ctx.message.guild.members, name = ping.name)
        
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

def setup(bot):
    bot.add_cog(Info(bot))