import discord
from discord.ext import commands

import json
from utills.u_mongo import Mongo
import datetime

async def lang_text(guild_id):
    record = await Mongo.get_record('cfg_ser','guild_id',str(guild_id))
    final_lang= record['lang']
    with open('language.json','r', encoding='utf-8') as file:
        text = json.loads(file.read())
        return text[final_lang]

class Info(commands.Cog):
    def __init__(self,bot):
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
                member = await commands.UserConverter().convert(ctx, idd)
            except:
                member = await self.bot.fetch_user(idd)
            else:
                member = discord.utils.get(ctx.author.guild.members, name = member.name)
            
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
        if arg == "status":
            if ctx.author.activity.name == "Spotify":

                activity = ctx.author.activity
                time_all = datetime.datetime.utcfromtimestamp(activity.duration.seconds).strftime('%H:%M:%S')
                time2 = int(activity.end.timestamp()) - int(datetime.datetime.now().timestamp())
                spotify_end = datetime.datetime.utcfromtimestamp(time2).strftime('%H:%M:%S')
                
                em = discord.Embed(
                    title = activity.name, 
                    description = (text['spotify']).format(activity.name, activity.title, activity.artist, activity.album, time_all, spotify_end),
                    color = activity.color)
                em.set_thumbnail(url = activity.album_cover_url)
                await ctx.send(embed = em)

            elif ctx.author.activity.type[0] == "custom":
                activity = ctx.author.activity

                name = (text['activity']['name']).format(activity.name)
                if activity.emoji == None:
                    emoji = ""
                else:
                    emoji = (text['activity']['emoji']).format(activity.emoji)

                em = discord.Embed(
                    title = "Custom Status",
                    description = f"{name}\n{emoji}",
                    color = ctx.author.color)
                await ctx.send(embed = em)

            elif ctx.author.activity.type[0] == "playing":

                activity = ctx.author.activity

                details = activity.details
                state = activity.state

                name = (text['activity']['name']).format(activity.name)

                try:
                    app_id = activity.application_id
                except AttributeError:
                    app_id = ""
                else:
                    app_id = (text['activity']['app_id']).format(app_id)
                


                try:
                    large_image = activity.large_image_url
                except AttributeError:
                    large_image = None

                try:
                    small_image = activity.small_image_url
                except AttributeError:
                    small_image = None

                try:
                    large_text = activity.large_image_text
                except AttributeError:
                    large_text = None

                try:
                    small_text = activity.small_image_text
                except AttributeError:
                    small_text = None

                if small_image != None or small_text != None:
                    small_image_full = f"__Small image:__ [{activity.small_image_text}]({small_image})\n"
                elif small_image == None and small_text == None:
                    small_image_full= ""

                if large_image != None or large_text != None:
                    large_image_full = f"__Large Image:__ [{activity.large_image_text}]({large_image})\n"
                elif large_image == None and large_text == None:
                    large_image_full = ""

                try:
                    duration_start = activity.timestamps['start']
                except KeyError:
                    duration_start = ""
                    cheker_start = None
                else:
                    time1 = str(datetime.datetime.now().timestamp())[:10]
                    time2 = str(duration_start)[:10]
                    time = (int(time2) - int(time1))*(-1)
                    time_start = datetime.datetime.utcfromtimestamp(time).strftime('%H:%M:%S')
                    duration_start = (text['activity']['duration']['start']).format(time_start)
                    cheker_start = True

                try:
                    duration_end = activity.timestamps['end']
                except KeyError:
                    duration_end = ""
                    cheker_end = None
                else:
                    time1 = str(datetime.datetime.now().timestamp())[:10]
                    time2 = str(duration_end)[:10]
                    time = (int(time2) - int(time1))*(-1)
                    time_end = datetime.datetime.utcfromtimestamp(time).strftime('%H:%M:%S')
                    duration_end = (text['activity']['duration']['end']).format(time_end)
                    cheker_end = True

                if cheker_start == True or cheker_end == True:
                    duration = (text['activity']['duration']['text']).format(duration_start, duration_end)

                if details == None:
                    details = ""
                else:
                    details = (text['activity']['details']).format(details)

                if state == None:
                    state = ""
                else:
                    state = (text['activity']['state']).format(state)

                em = discord.Embed(
                    title = activity.name,
                    description = f'{name}{details}{state}{large_image_full}{small_image_full}{duration}')

                if large_image == None:
                    large_image = ""
                
                if small_image == None:
                    small_image = ""

                em.set_thumbnail(url = large_image)
                em.set_footer(text= app_id, icon_url = small_image)
                await ctx.send(embed = em)

        elif arg == "server":
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

        else:
            idd = arg or str(ctx.author)
            try:
                member = await commands.UserConverter().convert(ctx , idd) 
            except:
                user = await self.bot.fetch_user(idd)
            else:
                user = discord.utils.get(ctx.message.guild.members, name = member.name)   
            
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