import discord
from discord.ext import commands

from utills.u_mongo import Mongo

async def in_owner(ctx):
    return ctx.author.id == 244835276361302016

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.check(in_owner)
    async def ld(self, ctx, name):
        await ctx.message.delete(delay = 0)
        self.bot.load_extension(f'modules.{name}')
        print(f'''
            Loaded modules.{name}
            ''')

    @commands.command()
    @commands.check(in_owner)
    async def rld(self, ctx, name):
        await ctx.message.delete(delay = 0)
        self.bot.reload_extension(f'modules.{name}')
        print(f'''
            Reloaded modules.{name}
            ''')


    @commands.command(aliases = ['lang'])
    async def language(self,ctx,yazik=None):
        record = await Mongo.get_record('cfg_ser','guild_id', str(ctx.author.guild.id))
        if yazik == 'ru' or yazik == 'en':        
            if record is None:
                upd={'lang':yazik,
                    'guild_id': str(ctx.author.guild.id)}
                await Mongo.record_insert('cfg_ser',upd)
            else:
                upd={'lang':yazik}
                await Mongo.update_record('cfg_ser',record, upd)
            await ctx.send(f"Set Language `{yazik}`")
        else:
            await ctx.send("Language `en`, `ru`")

    @commands.command()
    async def invite(self,ctx):
        """
        Url For invite bot your server
        """
        em1= discord.Embed(Title=(self.bot.user.name), description="Invite bot --> https://discordapp.com/oauth2/authorize?client_id=464180325073813505&scope=bot&permissions=1342581886", color = ctx.author.colour)
        await ctx.send(embed=em1)


def setup(bot):
    bot.add_cog(Owner(bot))