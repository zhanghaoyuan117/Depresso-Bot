import discord
import os
import requests
import random
from discord.ext import commands
from dotenv import load_dotenv


class Stock(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['news'])
    async def stockNews(self, ctx, *, symbol):
        load_dotenv("D:\Environment Variables\.env.txt")
        url = "https://yahoo-finance-low-latency.p.rapidapi.com/v2/finance/news"
        querystring = {"symbols": symbol}

        headers = {
            'x-rapidapi-key': os.getenv('RAPID_API_KEY'),
            'x-rapidapi-host': "yahoo-finance-low-latency.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring).json()
        articleNum = random.randint(0, len(response['Content']['result']))
        article = response['Content']['result'][articleNum]
        print(response['Content']['result'][articleNum])

        embed = discord.Embed(
            title=article['title'],
            summary=article['summary'],
            colour=discord.Colour.blue()
        )

        if "thumbnail" in article:
            embed.set_author(name=article['author_name'], icon_url=article['thumbnail'])
            embed.set_thumbnail(url=article['thumbnail'])
            embed.set_image(url=article['thumbnail'])
        else:
            embed.set_author(name=article['author_name'], icon_url="https://picsum.photos/id/1031/200")
            embed.set_thumbnail(url="https://picsum.photos/id/1031/200")
            embed.set_image(url="https://picsum.photos/id/1031/200")

        embed.add_field(
            name="Time Zone",
            value=article['timeZoneShortName'] + ", " + article['timeZoneFullName'],
            inline=False
        )
        embed.add_field(name="Provider", value=article['provider_name'], inline=False)
        embed.add_field(name="URL", value=article['url'], inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=['feat', 'Feat', 'Featured', 'featured'])
    async def stockFeatured(self, ctx, *, region):
        load_dotenv("D:\Environment Variables\.env.txt")
        url = "https://yahoo-finance-low-latency.p.rapidapi.com/v1/finance/trending/" + region

        headers = {
            'x-rapidapi-key': os.getenv('RAPID_API_KEY'),
            'x-rapidapi-host': "yahoo-finance-low-latency.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers).json()
        result = response['finance']['result'][0]['quotes']

        embed = discord.Embed(
            title='Trending Stocks in ' + region,
            colour=discord.Colour.blue()
        )

        for x in result:
            print(x['symbol'])
            embed.add_field(name=x['symbol'], value=x['symbol'])

        await ctx.send(embed=embed)

    @stockNews.error
    async def stock_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please type in a Symbol.')

    @stockFeatured.error
    async def stock_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please type in a Region Symbol.')

def setup(client):
    client.add_cog(Stock(client))
