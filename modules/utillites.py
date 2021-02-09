import discord
from discord.ext import commands

import datetime
import requests
import json

from google_trans_new import google_translator 
from io import BytesIO
import os

import sys
import weather_pic 
from utills.u_mongo import Mongo
from utills.config import Tokens

async def lang_text(guild_id):
    record = await Mongo.get_record('cfg_ser', 'guild_id', str(guild_id))
    final_lang = record['lang']
    with open('language.json', 'r', encoding='utf-8') as file:
        text = json.loads(file.read())
        return text[final_lang]


class Utillites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lyrics(self, ctx, *, lyrics_name):
        text = (await lang_text(ctx.message.guild.id))['lyrics']

        ksoft_search = f"https://api.ksoft.si/lyrics/search?q={lyrics_name}&limit=1"
        ksoft_auth = requests.get(ksoft_search, headers={"Authorization": (Tokens.ksoft_keys)})
        re_ksoft = json.loads(ksoft_auth.text)

        try:
            lyrics = re_ksoft['data'][0]['lyrics']
        except IndexError:
            await ctx.send(text['error'])
        else:
            artist = re_ksoft['data'][0]['artist']
            name_song = re_ksoft['data'][0]['name']

            genuis_search = f'https://api.genius.com/search?q={artist}%20{name_song}'
            genuis_auth = requests.get(genuis_search, headers={"Authorization": (Tokens.Genius_key)})
            re_genuis = json.loads(genuis_auth.text)
            try:
                image_album = re_genuis['response']['hits'][0]['result']['header_image_url']
            except:
                image_album = ''

            len_text = len(lyrics)
            if len_text > 2048:
                s = lyrics[:2047]
                s1 = lyrics[2048:4095]
                em = discord.Embed(description=(s), color=0xd8a903)
                em.set_author(name = f'{artist} - {name_song}', url= re_ksoft['data'][0]['url'])
                em.set_thumbnail(url=(image_album))
                em1 = discord.Embed(title='', description=(s1), color=0xd8a903)
                em1.set_footer(text="Powered by KSoft.Si", icon_url= "https://cdn.ksoft.si/images/Logo1024-W.png")
                await ctx.send(embed=em)
                await ctx.send(embed=em1)

            elif len_text < 2047:
                em = discord.Embed(description=(lyrics), color=0xd8a903)
                em.set_author(name = f'{artist} - {name_song}', url= re_ksoft['data'][0]['url'])
                em.set_thumbnail(url=(image_album))
                em.set_footer(text="Powered by KSoft.Si", icon_url= "https://cdn.ksoft.si/images/Logo1024-W.png")
                await ctx.send(embed=em)

    @lyrics.error
    async def error_lyrics(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            text = (await lang_text(ctx.message.guild.id))['lyrics']
            await ctx.send(text['lyrics_error'])

    # Переводчик
    @commands.command(aliases=['ts', 'tr', 'перевод'])
    async def translate(self, ctx, *, arg1):
        """
        Translate Ru-En
        """
        translator = google_translator()
        ru = translator.translate(text=f'{arg1}', lang_tgt='ru')
        en = translator.translate(text=f'{arg1}', lang_tgt='en')
        em1 = discord.Embed(title="**Translate**", color=ctx.author.color)
        em1.add_field(name="English", value=en, inline=False)
        await ctx.send(embed=em1)
        em1 = discord.Embed(title="**Translate**", color=ctx.author.color)
        em1.add_field(name="Russian", value=ru, inline=False)
        await ctx.send(embed=em1)

    #@translate.error
    async def translate_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            text = (await lang_text(ctx.message.guild.id))['Translate']
            await ctx.send(text['translate_error'])

    @commands.command()
    async def lastfm(self, ctx, userfm, arg=None):
        text = await lang_text(ctx.message.guild.id)
        """
        Check profile or last tracklist +[last]
        """
        url_list = f"http://ws.audioscrobbler.com/2.0/?method=user.getRecentTracks&user={userfm}&api_key={Tokens.TokenLastFM}&format=json&limit=4"
        url_User = f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={userfm}&api_key={Tokens.TokenLastFM}&format=json"
        if arg == "last":
            i = 0
            r = requests.get(url_list)
            requests_json = r.json()
            playedcount = f"Played Total = {requests_json['recenttracks']['@attr']['total']}"
            one = f"{requests_json['recenttracks']['track'][i]['artist']['#text']} - {requests_json['recenttracks']['track'][i]['name']}"
            i = i + 1
            two = f"{requests_json['recenttracks']['track'][i]['artist']['#text']} - {requests_json['recenttracks']['track'][i]['name']}"
            i = i + 1
            three = f"{requests_json['recenttracks']['track'][i]['artist']['#text']} - {requests_json['recenttracks']['track'][i]['name']}"
            i = i + 1
            four = f"{requests_json['recenttracks']['track'][i]['artist']['#text']} - {requests_json['recenttracks']['track'][i]['name']}"
            i = i + 1
            five = f"{requests_json['recenttracks']['track'][i]['artist']['#text']} - {requests_json['recenttracks']['track'][i]['name']}"

            em1 = discord.Embed(title="Last track",
                                description=f"1.{one}\n--------------------\n2.{two}\n--------------------\n3.{three}\n--------------------\n4.{four}\n--------------------\n5.{five}",
                                color=ctx.author.color)
            em1.set_footer(text=playedcount, icon_url=ctx.author.avatar_url_as(format=None))
            await ctx.send(embed=em1)
        else:
            r = requests.get(url_User)
            request_json = r.json()
            try:
                cplaylist = request_json['user']["playlists"]
            except KeyError:
                await ctx.send((text['errors']['no_found_user']).format(userfm))
            else:
                playcount = request_json["user"]["playcount"]
                username = request_json["user"]["name"]
                dateregister = int(request_json["user"]["registered"]["unixtime"])
                dateregister2 = (datetime.datetime.utcfromtimestamp(dateregister).strftime('%Y-%m-%d %H:%M:%S'))

            em = discord.Embed(title=username,
                               description=f"**Playlist** = {cplaylist}\n**PlayCount**= {playcount}\n**Register** = {dateregister2}",
                               color=ctx.author.color)
            await ctx.send(embed=em)

    @lastfm.error
    async def lastfm_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(description=f"{ctx.prefix}lastfm <nickname profile LastFM> <last>")
            await ctx.send(embed=em)


    @commands.command()
    async def weather(self, ctx, arg):
        text = (await lang_text(ctx.message.guild.id))['Weather']
        url= f"https://api.openweathermap.org/data/2.5/weather?q={arg}&appid={Tokens.Weather_key}&units=metric"
        responce = (requests.get(url)).json()
        if responce['cod'] == '404':
            await ctx.send(text['cod_404'])
        elif responce['cod'] == '401':
            await ctx.send(text['cod_401'])
        else:
            endpoint = weather_pic.weather_start(arg, responce, ctx.author.id, text)
            with open(endpoint, 'rb') as fp:
                await ctx.send(file = discord.File(fp,'weather.png'))
            os.unlink(endpoint)

    @weather.error
    async def weather_error(self,ctx,error):
        text= (await lang_text(ctx.message.guild.id))['Weather']
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(text['weather_error'])

def setup(bot):
    bot.add_cog(Utillites(bot))
