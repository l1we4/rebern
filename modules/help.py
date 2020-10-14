import discord
from discord.ext import commands

    
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            emHelp=discord.Embed(title= "Help commands",description = "Get more info, use `help [command]`",color =0x7fff7f)
            emHelp.add_field(name="🎲Fun", value= "`coin` `osu`")
            emHelp.add_field(name="ℹInfo",value="`avatar` `info`",inline=False)
            emHelp.add_field(name="🔨Moderation", value= "`ban` `unban` `clear` `kick` `createem` `deleteem`" ,inline=False)
            emHelp.add_field(name="💌Reaction Roles", value= "`adr` `rmr` `find_id`")
            emHelp.add_field(name="🔧Utillites",value="`lastfm` `lyrics` `translate` `weather` `em`",inline=False)
            emHelp.add_field(name="⚙️Server Settings",value="`language`, `invite`",inline=False)
            await ctx.send(embed=emHelp)

    @help.command()
    async def deleteem(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}deleteem**
        ```Delete custom emoji for Guild```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f'{ctx.prefix}deleteem <emoji>')
        await ctx.send(embed=em)      


    @help.command()
    async def adr(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}adr**
        ```Add Reaction Role```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f'{ctx.prefix}adr <channel> <Message ID> <Emoji> <Role>')
        
        await ctx.send(embed=em)

    @help.command()
    async def rmr(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}rmr**
        ```Remove Reaction Role```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f'{ctx.prefix}rmr <ID RR>')
        await ctx.send(embed=em)    

    @help.command()
    async def find_id(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}find_id**
        ```Found RR via Role```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f'{ctx.prefix}find_id <Role>')
        await ctx.send(embed=em)     

    @help.command()
    async def info(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}info**
        ```Get Info Everything```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f"""
        `{ctx.prefix}info <@user or userID>`
        `{ctx.prefix}info status`
        `{ctx.prefix}info server`""")
        await ctx.send(embed=em)

    @help.command()
    async def avatar(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}avatar**
        ```Get Avatar```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f"{ctx.prefix}avatar <@user or userID or None>")
        await ctx.send(embed=em)


    @help.command()
    async def ban(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}ban**
        ```Get Member Ban```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f"`{ctx.prefix}ban <@user or userID> <reason>`")
        await ctx.send(embed=em)
    
    @help.command()
    async def kick(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}kick**
        ```Kick a user from server```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f"`{ctx.prefix}kick <@user or userID> <reason?`")
        await ctx.send(embed=em)

    @help.command()
    async def unban(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}unban**
        ```Unbanned user```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f"`{ctx.prefix}unban <@user or userID or user#0001>`")
        await ctx.send(embed=em)

    @help.command()
    async def clear(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}clear**
        ```Clearing messages```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f"""`{ctx.prefix}clear <number>`
        `{ctx.prefix}clear <@user> <number>`""",inline= False)
        em.add_field(name="**Aliases**",value="[ __purge__ ], [ __c__ ], [ __clean__ ]")
        await ctx.send(embed=em)

    @help.command()
    async def createem(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}clear**
        ```Create Custom emoji from Image```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f"`{ctx.prefix}createem <URL> <name emoji>`",inline= False)
        await ctx.send(embed=em)
    
    @help.command()
    async def language(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}language**
        ```Selecting the text language for the server```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f"`{ctx.prefix}lang <'ru' or 'en'>`",inline= False)
        em.add_field(name="**Aliases**",value="[ __lang__ ]")
        await ctx.send(embed=em)
    
    @help.command()
    async def setprefix(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}setprefix**
        ```Setting the prefix for the bot```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f"`{ctx.prefix}setprefix <!,-,=>`",inline= False)
        await ctx.send(embed=em)

    @help.command()
    async def osu(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}osu**
        ```Get info account Osu```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f"`{ctx.prefix}osu" ,inline= False)
        await ctx.send(embed=em)

    
    @help.command()
    async def lastfm(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}lastfm**
        ```Get info account lastFM```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f"`{ctx.prefix}lastfm <nickname from LastFM>`\n`{ctx.prefix}lastfm <nickname from LastFM> <last>`" ,inline= False)
        await ctx.send(embed=em)
    
    @help.command()
    async def weather(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}weather**
        ```Get info city weather```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f"`{ctx.prefix}weather <ZIP-Code or Name city>" ,inline= False)
        await ctx.send(embed=em)

    @help.command()
    async def translate(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}translate**
        ```Translate your text [ru-en]```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f"`{ctx.prefix}translate <text>" ,inline= False)
        await ctx.send(embed=em)

    @help.command()
    async def lyrics(self,ctx):
        em = discord.Embed(title = "Help Menu",
        description = f"""**{ctx.prefix}lyrics**
        ```Found lyrics your track```""",
        color =0x7fff7f)
        em.add_field(name="**Usages**", value=f"`{ctx.prefix}lyrics <Name track>" ,inline= False)
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Help(bot))