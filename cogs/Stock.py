import discord
import os
import requests
import random
from discord.ext import commands
from dotenv import load_dotenv
from bs4 import BeautifulSoup


class Stock(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['news', 'stocknews'])
    async def stockNews(self, ctx, *, stockName):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/89.0.4389.114 Safari/537.36 ',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://google.com',
            'Dnt': '1'
        }

        url = f'https://finance.yahoo.com/lookup?s={stockName}'
        source = requests.get(url, headers).text
        soup = BeautifulSoup(source, 'lxml')

        stockLink = soup.find('a', attrs={"data-reactid": "57"})['href']
        url = f'https://finance.yahoo.com/{stockLink}'
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')

        articles = soup.find('ul', {"class": 'My(0) Ov(h) P(0) Wow(bw)'}).find_all('li')

        article = random.choice(articles)
        title = article.find('a').text

        print(title)
        href = article.find('a')['href']
        articleLink = f'https://finance.yahoo.com/{href}'
        try:
            providerInfo = article.find('div', {"class": "C(#959595) Fz(11px) D(ib) Mb(6px)"}).text
        except AttributeError as e:
            providerInfo = 'None'
        try:
            img = article.find('img')['src']
        except TypeError as e:
            img = 'https://picsum.photos/id/1031/200'
        try:
            summary = article.find('p').text
        except AttributeError as e:
            summary = 'No Summary'

        embed = discord.Embed(
            title=title,
            colour=discord.Colour.blue()
        )

        embed.add_field(name="Description", value=summary, inline=False)
        embed.set_thumbnail(url=img)
        embed.set_image(url=img)
        embed.add_field(name="Provider", value=providerInfo, inline=False)
        embed.add_field(name="URL", value=articleLink, inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=['price'])
    async def stockPrice(self, ctx, *, stockName):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/89.0.4389.114 Safari/537.36 ',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://google.com',
            'Dnt': '1'
        }

        url = f'https://finance.yahoo.com/lookup?s={stockName}'
        source = requests.get(url, headers).text
        soup = BeautifulSoup(source, 'lxml')

        stockLink = soup.find('a', attrs={"data-reactid": "57"})['href']
        url = f'https://finance.yahoo.com/{stockLink}'
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')

        stockName = soup.find('h1', {"class": "D(ib) Fz(18px)"}).text
        stockPrice = soup.find('div', {"class": "D(ib) Mend(20px)"}).find_all('span')[0].text
        stockChange = soup.find('div', {"class": "D(ib) Mend(20px)"}).find_all('span')[1].text
        stockDayRange = soup.find('td', attrs={"data-test": 'DAYS_RANGE-value'}).text
        stockYearlyRange = soup.find('td', attrs={"data-test": 'FIFTY_TWO_WK_RANGE-value'}).text

        if stockChange[0] == '+':
            img = 'https://compote.slate.com/images/926e5009-c10a-48fe-b90e-fa0760f82fcd.png?width=1200&rect=680x453' \
                  '&offset=0x30 '
        elif stockChange[0] == '-':
            img = 'https://i.kym-cdn.com/photos/images/newsfeed/001/857/750/4ab.png'
        else:
            img = 'https://i.kym-cdn.com/photos/images/original/001/459/556/023.png'

        embed = discord.Embed(
            title=stockName,
            colour=discord.Colour.blue()
        )

        embed.add_field(name="Stock Price", value=stockPrice, inline=False)
        embed.add_field(name="Stock Change", value=stockChange, inline=False)
        embed.add_field(name="Stock's Daily Range", value=stockDayRange, inline=False)
        embed.add_field(name="Stock's 52 week Range", value=stockYearlyRange, inline=False)

        embed.set_thumbnail(url=img)

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
            await ctx.send('Please type in a Symbol/Company name.')

    @stockFeatured.error
    async def stock_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please type in a Region Symbol.')


def setup(client):
    client.add_cog(Stock(client))
