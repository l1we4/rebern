import discord
from discord.ext import commands

import requests
import json
from utills.u_mongo import Mongo


async def lang_text(guild_id):
    record = await Mongo.get_record('cfg_ser','guild_id',str(guild_id))
    final_lang= record['lang']
    with open('language.json','r', encoding='utf-8') as file:
        text = json.loads(file.read())
        return text[final_lang]


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self,ctx,user:discord.Member = None):
        text= (await lang_text(ctx.message.guild.id))
        if user.id == ctx.message.author.id:
            await ctx.send(text['kick']['kick_yourself'])
        else:
            try:
                await ctx.guild.kick(user)
            except discord.Forbidden:
                em = discord.Embed(title= "Error",
                description= text['errors']['bot_not_perm'],
                color = 0xe5e500)
                await ctx.send(embed=em)
            else:   
                em= discord.Embed(title= 'Kick Member',
                description = (text['kick']['kicked']).format(user),
                color= 0xff3232)
                await ctx.send(embed = em)
        




    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, user, reason = None):
        text= (await lang_text(ctx.message.guild.id))['ban']
        try:
            member = await commands.UserConverter().convert(ctx , user) 
        except:
            user = await self.bot.fetch_user(user)
        else:
            user = discord.utils.get(ctx.message.guild.members, name = member.name)   
        if ctx.message.author.id == user.id:
            em = discord.Embed(title = "Error",
            description = text['ban_yourself'],
            color = 0xff0000)
        else:   
            await ctx.guild.ban(user, reason=reason)
            em= discord.Embed(title= 'Ban Member',
            description = (text['banned']).format(user),
            color= 0xff3232)
            em.set_thumbnail(url = user.avatar_url)
            em.set_footer(text = f"Reason: {reason}")
            await ctx.send(embed = em)


    @commands.command(pass_context=True, aliases=['clean', 'c','purge'])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def clear(self, ctx, arg1, arg2=None):
        try:
            member = await commands.UserConverter().convert(ctx, arg1)
        except discord.ext.commands.errors.BadArgument:
            if int(arg1) <= 1:
                em1 = discord.Embed(title = "Error Clear", description = f"Number __{arg1}__ can't be < than **1**", color = 0xff0000)
                await ctx.send(embed = em1)
            else:
                await ctx.message.delete(delay=None)
                await ctx.channel.purge(limit = int(arg1))
        else:
            if int(arg2) <= 1:
                em1 = discord.Embed(title = "Error Clear", description = f"Number __{arg2}__ can't be < than **1**", color = 0xff0000)
                await ctx.send(embed = em1)
            else:
                def check_member(msg: discord.Message)->bool:
                    return msg == ctx.message or member is None or msg.author == member
                await ctx.message.delete(delay=None)
                await ctx.channel.purge(limit = int(arg2), check = check_member)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_emojis=True)
    async def deleteem(self,ctx,arg):
        emoji = await commands.EmojiConverter().convert(ctx, arg)
        em = discord.Embed(description = f"Emoji {emoji} deleted")
        await ctx.send(embed = em)
        await emoji.delete()

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    @commands.guild_only()
    async def createem(self, ctx, url, name):
        text = await lang_text(ctx.message.guild.id)
        r= requests.get(url)
        if r.status_code == 200:
            await ctx.guild.create_custom_emoji(name=name ,image=r.content)
            em1= discord.Embed(title= '', description = f"Create Custom Emoji: __**{name}**__", color = 0x008000)
            await ctx.send(embed= em1)
        else:
            await ctx.send(text['errors']['None_url'])


    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self,ctx,*,member):
        for ban_entry in (await ctx.guild.bans()):
            if str(ban_entry.user.id) == str(member):
                user = ban_entry.user
                await ctx.guild.unban(user)
            elif str(ban_entry.user.name) == str(member):
                user = ban_entry.user
            elif str(ban_entry.user) == str(member):
                user = ban_entry.user
                await ctx.guild.unban(user)
        if user != None:     
            em= discord.Embed(title= 'Unbanned Member',
            description = f"**{user}** Unbanned",
            color= 0x00ff00)
            await ctx.send(embed = em)


    @unban.error
    async def unban_error(self,ctx,error):
        text = (await lang_text(ctx.message.guild.id))['errors']
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command only for **Guild**")
        if isinstance(error, commands.MissingRequiredArgument):
            em= discord.Embed(title = "Unban help", description = f"{ctx.prefix}unban <`@user` or `User id`>"
            ,color = 0xe5e500)
            await ctx.send(embed = em)
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("No Permission `Ban Members`")
        if isinstance(error, commands.BadArgument):
            em = discord.Embed(title= "Error",
            description = (text['no_found_user']).format(ctx.args[2]),
            color = 0xe5e500)
            await ctx.send(embed = em)

    @createem.error
    async def createem_error(self ,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("No permission `Manage Emojis`!")
        if isinstance(error, commands.MissingRequiredArgument):
            em= discord.Embed(title = "Help Create emoji", description = f"{ctx.prefix}createem <url> <name emoji>",color = 0xe5e500)
            await ctx.send(embed = em)
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command only for **Guild**")

    @deleteem.error
    async def deleteem_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("No Permission `Manage Emoji`")
        if isinstance(error, commands.MissingRequiredArgument):
            em= discord.Embed(title = "Delete Emoji help", description = f"{ctx.prefix}deleteem <emoji>",color = 0xe5e500)
            await ctx.send(embed = em)
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command only for **Guild**")


    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("No Permission `Manage Messages`!")
        if isinstance(error, commands.MissingRequiredArgument):
            em= discord.Embed(title = "Clear help", description = f"""Aliases: [c][clear][purge]
{ctx.prefix}clear <@user> <number> \n{ctx.prefix}clear <number>""",color = 0xff0000)
            await ctx.send(embed = em)
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command only for **Guild**")

    @ban.error
    async def ban_errors(self,ctx,error):
        if isinstance(error, commands.MissingRequiredArgument):
            em= discord.Embed(title = "Ban help", description = f"{ctx.prefix}ban <`@user` or `User id`> <reason>",color = 0xe5e500)
            await ctx.send(embed = em)
        if isinstance(error, commands.CommandInvokeError):
            em = discord.Embed(title="Error",
            description = ((await lang_text(ctx.message.guild.id))['errors']['no_found_user']).format(ctx.args[2]),
            color = 0xe5e500)
            await ctx.send(embed = em)
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("No Permission `Ban Members`")
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command only for **Guild**")
    
    @kick.error
    async def kick_error(self,ctx,error):
        text = (await lang_text(ctx.message.guild.id))['errors']
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command only for **Guild**")
        if isinstance(error, commands.MissingRequiredArgument):
            em= discord.Embed(title = "Kick help", description = f"{ctx.prefix}kick <`@user` or `User id`>"
            ,color = 0xe5e500)
            await ctx.send(embed = em)
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("No Permission `Kick Members`")
        if isinstance(error, commands.BadArgument):
            em = discord.Embed(title= "Error",
            description = (text['no_found_user']).format(ctx.args[2]),
            color = 0xe5e500)
            await ctx.send(embed = em)
            

def setup(bot):
    bot.add_cog(Moderation(bot))