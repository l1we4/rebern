import discord
from discord.ext import commands
import discord.utils
from utills.u_mongo import Mongo
import json

async def lang_text(guild_id):
    record = await Mongo.get_record('cfg_ser','guild_id',str(guild_id))
    final_lang= record['lang']
    with open('language.json','r', encoding='utf-8') as file:
        text = json.loads(file.read())
        return text[final_lang]


class Embed_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def em(self,ctx):
        if ctx.invoked_subcommand is None:
            text = await lang_text(ctx.message.guild.id)
            em = discord.Embed(title= "Help Embed",description = text['embed']['help'])
            await ctx.send(embed = em)

    @em.command()
    @commands.has_permissions(manage_roles=True)
    async def new(self,ctx):
        text = await lang_text(ctx.message.guild.id)
        author_id = ctx.message.author.id
        record = await Mongo.get_record('embed','embed_user',author_id)
        if record is None:
            data={'embed_user':author_id,
            'image':'',
            'color':'000000',
            'title':'',
            'descr':'',
            }
            await Mongo.record_insert('embed',data)
            await ctx.send(text['embed']['new_embed'])
        else:
            await ctx.send(text['embed']['existing_embed'])
    
    @em.command()
    @commands.has_permissions(manage_roles=True)
    async def image(self,ctx,arg):
        text = await lang_text(ctx.message.guild.id)
        author_id = ctx.message.author.id
        record = await Mongo.get_record('embed','embed_user',author_id)
        if record is None:
            await ctx.send(text['embed']['no_embed'])
        else:
            data = {'image':arg}
            await Mongo.update_record('embed',record,data)
            await ctx.send(text['embed']['set_image'])
    
    @em.command()
    @commands.has_permissions(manage_roles=True)
    async def descr(self,ctx,*,arg):
        text = await lang_text(ctx.message.guild.id)
        author_id = ctx.message.author.id
        record = await Mongo.get_record('embed','embed_user',author_id)
        if record is None:
            await ctx.send(text['embed']['no_embed'])
        else:
            data = {'descr':arg}
            await Mongo.update_record('embed',record, data)
            await ctx.send(text['embed']['set_descr'])

    @em.command()
    @commands.has_permissions(manage_roles=True)
    async def title(self,ctx,*,arg):
        text = await lang_text(ctx.message.guild.id)
        author_id = ctx.message.author.id
        record = await Mongo.get_record('embed','embed_user',author_id)
        if record is None:
            await ctx.send(text['embed']['no_embed'])
        else:
            data =  {'title':arg}
            await Mongo.update_record('embed',record,data)
            await ctx.send(text['embed']['set_title'])
    
    @em.command()
    @commands.has_permissions(manage_roles=True)
    async def color(self,ctx,*,arg):
        text = await lang_text(ctx.message.guild.id)
        author_id = ctx.message.author.id
        record = await Mongo.get_record('embed','embed_user',author_id)
        if record is None:
            await ctx.send(text['embed']['no_embed'])
        else:
            data =  {'color':arg}
            await Mongo.update_record('embed',record,data)
            await ctx.send(text['embed']['set_color'])
    
    @em.command()
    @commands.has_permissions(manage_roles=True)
    async def view(self,ctx):
        text = await lang_text(ctx.message.guild.id)
        author_id = ctx.message.author.id
        record = await Mongo.get_record('embed','embed_user',author_id)
        if record is None:
            await ctx.send(text['embed']['view'])
        else:
            em= discord.Embed(title=record['title'], description =record['descr'],color= int(record['color'],16))
            em.set_image(url=record['image'])
            await ctx.send(embed = em)
        
    @em.command()
    @commands.has_permissions(manage_roles=True)
    async def clear(self,ctx):
        text = await lang_text(ctx.message.guild.id)
        await Mongo.delete_record('embed','embed_user',ctx.message.author.id)
        await ctx.send(text['embed']['deleted'])

    @em.command()
    @commands.has_permissions(manage_roles=True)
    async def send(self,ctx,ch:discord.TextChannel):
        text = await lang_text(ctx.message.guild.id)
        record= await Mongo.get_record('embed','embed_user', ctx.message.author.id)
        if record is None:
            await ctx.send(text['embed']['view'])
        else:
            em= discord.Embed(title=record['title'], description =record['descr'],color= int(record['color'],16))
            em.set_image(url=record['image'])
            await ch.send(embed = em)
            await Mongo.delete_record('embed','embed_user',ctx.message.author.id)

def setup(bot):
    bot.add_cog(Embed_message(bot))