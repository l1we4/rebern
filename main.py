import discord
from discord.ext import commands
import datetime

from utills.config import Tokens
async def in_owner(ctx):
    return ctx.author.id == 244835276361302016

client = commands.Bot(command_prefix = Tokens.Prefix)

@client.event
async def on_ready():
    print((datetime.datetime.now().strftime("%H:%M:%S")) + "| | " + (client.user.name) + '#' + (client.user.discriminator))
    game = discord.Game(";help || well...")
    await client.change_presence(status=discord.Status.idle, activity =game)

client.remove_command('help')

start_extensions = ['modules.owner',
                    'modules.rr',
                    'modules.event',
                    'modules.embed',
                    'modules.info',
                    'modules.help',
                    'modules.fun',
                    'modules.utillites',
                    'modules.moderation']

if __name__ == "__main__":
    for extension in start_extensions:
        try:
            client.load_extension(extension)
            print(f'load {extension}')
        except Exception as e:
            exc = f"{type(e).__name__}: {e}"
            print(f'Error load extension {extension}\n{exc}')

client.run(Tokens.token, reconnect = True)