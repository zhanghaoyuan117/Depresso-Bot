import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix='+');
BOT_KEY = os.environ['BOT_KEY']


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print(f'{extension} has been loaded')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(BOT_KEY)
