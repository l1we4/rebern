import discord
from discord.ext import commands
import discord.utils

from utills.u_mongo import Mongo
from utills.config import Tokens

import json
import random

import requests

async def lang_text(guild_id):
    record = await Mongo.get_record('cfg_ser', 'guild_id', str(guild_id))
    final_lang = record['lang']
    with open('language.json', 'r', encoding='utf-8') as file:
        text = json.loads(file.read())
        return text[final_lang]

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Монетка
    @commands.command()
    async def coin(self,ctx):
        """
        Coin Flip
        """
        text= (await lang_text(ctx.message.guild.id))['coin']
        random_num = random.randint(0, 1)
        coin= self.bot.get_emoji(538020491902844929)
        if random_num == 1:
            em1= discord.Embed(title= "CoinFlip", description= f"{coin} | {text['tails']}" , color= ctx.author.color)
            await ctx.send(embed= em1)
        if random_num == 0:
            em1= discord.Embed(title= "CoinFlip", description= f"{coin} | {text['heads']}", color= ctx.author.color)
            await ctx.send(embed= em1)   

    @commands.command()
    async def osu(self, ctx):
        text= (await lang_text(ctx.message.guild.id))['osu']
        await ctx.send(text['menu'])
        while True:
            msg1 = await self.bot.wait_for('message', timeout=30, check=lambda message:ctx.message.author)
            check1 = msg1.content.isdigit()
            if msg1.content == 'exit':
                await ctx.send(text['exit_menu'])
                break
            elif check1 == False:
                await ctx.send(text['menu1'])
            elif check1== True:
                await ctx.send(text['menu2'])
                msg2 = await self.bot.wait_for('message', timeout=30, check=lambda message:ctx.author)
                break

        osuapi= f"https://osu.ppy.sh/api/get_user?k={Tokens.osu_Token}&u={msg2.content}&m={int(msg1.content) - 1}"
        rosu= requests.get(osuapi)
        response_json = json.loads(rosu.text)    
        try:
            user_id = response_json[0]['user_id']
        except IndexError:
            await ctx.send(text['error_osu'])
            return
        else:  
            
            username=response_json[0]['username']
            ranked_score= response_json[0]['ranked_score']
            total_Score = response_json[0]['total_score']
            pp_raw= response_json[0]['pp_raw']
            pp_rank= response_json[0]['pp_rank']
            lvl =response_json[0]['level']
            pp_country_rank= response_json[0]['pp_country_rank']
            accuracy= response_json[0]['accuracy']
            playcount= response_json[0]['playcount']
            count300= response_json[0]['count300']
            count100= response_json[0]['count100']
            count50= response_json[0]['count50']
            round_acc = accuracy[:5]
            join_date = response_json[0]['join_date']
            endpointfordiscord = (text['board']).format(username, response_json[0]['country'], user_id, join_date, lvl, ranked_score, total_Score, pp_raw, pp_rank, pp_country_rank, round_acc, playcount, count300, count100, count50, response_json[0]['count_rank_ssh'], response_json[0]['count_rank_sh'], response_json[0]['count_rank_ss'], response_json[0]['count_rank_s'],response_json[0]['count_rank_a'])
            em1=discord.Embed(title =f"For **{ctx.author.display_name}**",
                description= endpointfordiscord,
                сolor= ctx.author.color)
            em1.set_thumbnail(url=f"https://a.ppy.sh/{user_id}")
            await ctx.send(embed=em1)
    @osu.error
    async def osu_error(self,ctx):
        text= (await lang_text(ctx.message.guild.id))['osu']
        await ctx.send(text['osu_error'])

def setup(bot):
    bot.add_cog(Fun(bot))