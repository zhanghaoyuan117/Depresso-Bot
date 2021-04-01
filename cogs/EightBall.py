import discord
import random
from discord.ext import commands


class EightBall(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        response = ['It is certain',
                    'It is decidedly so',
                    'Without a doubt',
                    'Yes, definitely',
                    'You may rely on it',
                    'As I see it, yes',
                    'Most likely',
                    'Outlook good',
                    'Signs point to yes',
                    'Yes',
                    'Reply hazy, try again',
                    'Ask again later',
                    'Better not tell you now',
                    'Cannot predict now',
                    'Concentrate and ask again',
                    "Don't bet on it",
                    'My reply is no',
                    'My sources say no',
                    'Outlook not so good',
                    'Very doubtful']

        await ctx.send(f'Question: {question} \nAnswer: {random.choice(response)}')

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please type in a question.')


def setup(client):
    client.add_cog(EightBall(client))
