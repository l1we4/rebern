import discord
from discord.ext import commands
import discord.utils
from utills.u_mongo import Mongo

import hashlib

class Event_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self,rec):
        record = await Mongo.get_record('cfg_ser','guild_id', str(rec.id))
        if record is None:
            upd={'lang':'en',
                'guild_id': str(rec.id)}
            await Mongo.record_insert('cfg_ser',upd)
        
    @commands.Cog.listener()
    async def on_guild_remove(self,rec):
        await Mongo.delete_record('cfg_ser','guild_id', str(rec.id))   

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,rec):
        em = rec.emoji
        ch = rec.channel_id
        mesid = rec.message_id
        guild = rec.member.guild

        start = str(f'{ch}{mesid}{em}')
        idd = hashlib.md5(start.encode()).hexdigest()
        record = await Mongo.get_record('rr', 'id_rr', idd)
          
        if self.bot.user.id == rec.member.id:
            return
        elif record is None:
            return
        else:
            member = rec.member
            role = record['role']
            role = discord.utils.get(guild.roles, id = int(role))
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,rec):
        em = rec.emoji
        mesid = rec.message_id
        guild = discord.utils.get(self.bot.guilds, id = rec.guild_id)
        ch = rec.channel_id

        start = str(f'{ch}{mesid}{em}')
        idd = hashlib.md5(start.encode()).hexdigest()
        record = await Mongo.get_record('rr', 'id_rr', idd)
        
        if self.bot.user.id == rec.user_id:
            pass
        else:
            member = discord.utils.get(guild.members, id = rec.user_id)
            role = record['role']
            role = discord.utils.get(guild.roles, id = int(role))
            await member.remove_roles(role)

def setup(bot):
    bot.add_cog(Event_commands(bot))