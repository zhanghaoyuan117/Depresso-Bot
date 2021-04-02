import discord
import os
from discord.ext import commands, tasks
from itertools import cycle
from dotenv import load_dotenv


class Example(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.status = cycle(['+help for commands', 'It works?', 'Poggers'])

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        await self.client.change_presence(status=discord.Status.idle, activity=discord.Game(name='+help for commands'))
        print("Bot is ready.")

    @tasks.loop(seconds=30)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(self.status)))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')


def setup(client):
    client.add_cog(Example(client))
