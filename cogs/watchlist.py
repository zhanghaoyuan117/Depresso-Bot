import discord
import os
import requests
import sqlite3
from discord.ext import commands
from bs4 import BeautifulSoup


class Watchlist(commands.Cog):

    def __init__(self, client):
        self.client = client

    # CREATING DATABASE (ONLY USE ONCE)-------------------------------------------------

    # @commands.command()
    # async def createDB(self, ctx):
    #     conn = sqlite3.connect('./database/stock.db')
    #     c = conn.cursor()
    #
    #     c.execute("""CREATE TABLE stock (
    #                 id integer,
    #                 name text,
    #                 ticker text,
    #                 UNIQUE(id, ticker)
    #                 )""")
    #     conn.close()
    #
    #     await ctx.send('Success!')

    # -----------------------------------------------------------------------------------

    @commands.command(aliases=['add', 'waAdd'])
    async def watchlist_add(self, ctx, *, stockName):
        conn = sqlite3.connect('./database/stock.db')
        c = conn.cursor()

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

        stockName = soup.find('td', {"class": "data-col1 Ta(start) Pstart(10px) Miw(80px)"}).text
        stockTicker = soup.find('td', {"class": "data-col0 Ta(start) Pstart(6px) Pend(15px)"}).text
        user = ctx.message.author

        c.execute("INSERT INTO stock VALUES (:id , :name, :ticker)", {'id': user.id, 'name': stockName,
                                                                      'ticker': stockTicker})

        conn.commit()

        conn.close()

        await ctx.send(f"Successfully added {stockName} to {user}'s watchlist")

    @commands.command(aliases=['watchlist', 'watch'])
    async def watchlist_get(self, ctx):
        conn = sqlite3.connect('./database/stock.db')
        c = conn.cursor()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/89.0.4389.114 Safari/537.36 ',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://google.com',
            'Dnt': '1'
        }

        user = ctx.message.author

        c.execute("SELECT * FROM stock WHERE id=:id", {'id': user.id})
        stocks = c.fetchall()

        embed = discord.Embed(
            title=f'Watchlist for {user}',
            colour=discord.Colour.blue()
        )

        for stock in stocks:
            url = f'https://finance.yahoo.com/lookup?s={stock[1]}'
            source = requests.get(url, headers).text
            soup = BeautifulSoup(source, 'lxml')
            stockPrice = soup.find('td', {"class": "data-col2 Ta(end) Pstart(20px) Pend(15px)"}).text
            embed.add_field(name=stock[1], value=stockPrice)

        conn.close()

        await ctx.send(embed=embed)

    @commands.command(aliases=['waRemove', 'remove'])
    async def watchlist_remove(self, ctx, *, stockName):
        conn = sqlite3.connect('./database/stock.db')
        c = conn.cursor()

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

        stockName = soup.find('td', {"class": "data-col1 Ta(start) Pstart(10px) Miw(80px)"}).text
        stockTicker = soup.find('td', {"class": "data-col0 Ta(start) Pstart(6px) Pend(15px)"}).text
        user = ctx.message.author

        c.execute("SELECT * FROM stock WHERE id=:id AND name = :name AND ticker = :ticker",
                  {'id': user.id, 'name': stockName, 'ticker': stockTicker})
        if c.fetchone() is None:
            conn.close()
            await ctx.send(f"{stockName} is not in {user}'s watchlist")
        else:
            c.execute("DELETE FROM stock WHERE id = :id AND name = :name AND ticker = :ticker",
                      {'id': user.id, 'name': stockName, 'ticker': stockTicker})
            conn.commit()
            conn.close()

            await ctx.send(f"Successfully removed {stockName} to {user}'s watchlist")

    @commands.command(aliases=['clear_list'])
    async def watchlist_clear(self, ctx):
        conn = sqlite3.connect('./database/stock.db')
        c = conn.cursor()

        user = ctx.message.author

        c.execute("DELETE FROM stock WHERE id = :id", {'id': user.id})

        conn.commit()

        conn.close()

        await ctx.send(f"Successfully cleared {user}'s watchlist")

    @watchlist_add.error
    async def stock_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please type in a Symbol or Company name.')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Please type in a Symbol or Company name that is not part of your watchlist.')


def setup(client):
    client.add_cog(Watchlist(client))
