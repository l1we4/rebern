import discord
from discord.ext import commands
import discord.utils

import json
from utills.u_mongo import Mongo

import hashlib


async def lang_text(guild_id):
    record = await Mongo.get_record('cfg_ser','guild_id',str(guild_id))
    final_lang= record['lang']
    with open('language.json','r', encoding='utf-8') as file:
        text = json.loads(file.read())
        return text[final_lang]


class Rr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def adr(self, ctx, ch, mesid, emoji, role):
        #Channel
        channel = await commands.TextChannelConverter().convert(ctx,ch)

        #emoji
        try:
            em = await commands.EmojiConverter().convert(ctx,emoji)
        except:
            em = emoji

        #msg
        try:
            msg = await channel.fetch_message(mesid)
        except:
            await ctx.send("Не найдено сообщение")

        #role
        try:
            role = await commands.RoleConverter().convert(ctx, role)
        except:
            await ctx.send("Не найдена роль")
        
        start = str(f'{channel.id}{msg.id}{em}')
        idd =hashlib.md5(start.encode()).hexdigest()

        record = await Mongo.get_record('rr','id_rr', idd)

        if record is None:
            new = {
                "id_rr":idd,
                "id_msg": msg.id,
                "role": role.id,
                "emoji": str(em),
                "guild": ctx.author.guild.id}
            await Mongo.record_insert('rr', new)

            embedd = discord.Embed(title= "New Reaction Role",
                description = f"**🆔MD5 Hash:**\n__{idd}__\n\n**💌Message**:\n__{mesid}__\n\n**📞Channel**:\n__{ch}__\n\n **🔨Role**:\n__{role}__\n\n**Emoji**:\n {em}",
                color= role.color)
            await ctx.send(embed = embedd)
            await msg.add_reaction(emoji)

    @commands.command()
    async def find_id(self, ctx, role:discord.Role):
        record = await Mongo.get_record('rr', 'role', role.id)
        if record is None:
            em = discord.Embed(title = "Error", description = "RR No found", color = 0xFF0000)
            await ctx.send(embed = em)
        else:
            emoji = record['emoji']
            idd = record['id_rr']
            role_rr = record['role']
            role_rr = await commands.RoleConverter().convert(ctx, str(role_rr))


            em = discord.Embed(title= "Found RR",color = 0x00ff00)
            em.add_field(name="**MD5 ID RR**",value=idd, inline = False)
            em.add_field(name="Emoji",value=emoji)
            em.add_field(name="Role",value=role_rr.mention)
            await ctx.send(embed = em)        

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def rmr(self,ctx,id_rr):
        record= await Mongo.get_record('rr','id_rr',str(id_rr))
        
        if record == None:
            await ctx.send("RR No found")
        
        await Mongo.delete_record('rr','id_rr',id_rr)
        await ctx.send(f"**{id_rr}** deleted")


    @adr.error
    async def arr_error(self,ctx,error):
        text= (await lang_text(ctx.message.guild.id))['errors']

        if isinstance(error, commands.MissingPermissions):
            await ctx.send(text['manage_role'])
        elif isinstance(error,commands.MissingRequiredArgument):
            em1= discord.Embed(title= "Add RR ",description=f'{ctx.prefix}adr <channel> <Message ID> <Emoji> <Role>',
                color = 0xe5e500)
            await ctx.send(embed=em1)

    @rmr.error
    async def rmr_error(self,ctx,error):
        text= (await lang_text(ctx.message.guild.id))['errors']

        if isinstance(error, commands.MissingPermissions):
            await ctx.send(text['manage_role'])
        elif isinstance(error,commands.MissingRequiredArgument):
            em1= discord.Embed(title=" Remove RR", description=f'{ctx.prefix}rmr <ID RR>',
                color = 0xe5e500)
            await ctx.send(embed=em1)
    
    @find_id.error
    async def find_id_error(self,ctx,error):
        text= (await lang_text(ctx.message.guild.id))['errors']
        
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(text['manage_role'])
        elif isinstance(error,commands.MissingRequiredArgument):
            em1= discord.Embed(title="Found RR via Role",description=f'{ctx.prefix}find_rr <Role>',
                color = 0xe5e500)
            await ctx.send(embed=em1)




def setup(bot):
    bot.add_cog(Rr(bot))