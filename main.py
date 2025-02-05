import discord
from discord.ext import commands
import os
from game import GachaGame
from dotenv import load_dotenv
# Using python 3.12.2 virtual environment
# pip install discord.py
# pip install audioop-lts
# pip install python-dotenv

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
DATA = os.getenv("DATA_FILE")
"""
DISCORD_TOKEN="Your Token Here"
DISCORD_GUILD="Not needed, can be left blank"
DATA_FILE="your data file.json"
"""

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
gacha_game = GachaGame(DATA)
gacha_game.load()

@bot.command()
async def add_player(ctx):
    player_id = str(ctx.author.id)
    response = gacha_game.add_player(player_id)
    await ctx.send(response)
    gacha_game.save()

@bot.command()
async def reset_player(ctx):
    player_id = str(ctx.author.id)
    response = gacha_game.reset_player(player_id)
    await ctx.send(response)
    gacha_game.save()

@bot.command()
async def remove_player(ctx):
    player_id = str(ctx.author.id)
    response = gacha_game.remove_player(player_id)
    await ctx.send(response)
    gacha_game.save()

@bot.command()
async def roll_gacha(ctx):
    player_id = str(ctx.author.id)
    response = gacha_game.roll_gacha(player_id)
    await ctx.send(response)
    gacha_game.save()

@bot.command()
async def inventory(ctx):
    player_id = str(ctx.author.id)
    response = gacha_game.inventory(player_id)
    await ctx.send(response)

@bot.command()
async def shop(ctx):
    response = gacha_game.shop()
    await ctx.send(response)

@bot.command()
async def save(ctx):
    response = gacha_game.save()
    await ctx.send(response)

@bot.command()
async def bank_account(ctx):
    player_id = str(ctx.author.id)
    response = gacha_game.bank_account(player_id)
    await ctx.send(response)

@bot.command()
async def buy_item(ctx, *args):
    player_id = str(ctx.author.id)
    response = gacha_game.buy_item(player_id, ' '.join(args))
    await ctx.send(response)
    gacha_game.save()

@bot.command()
async def work(ctx, *args):
    player_id = str(ctx.author.id)
    response = gacha_game.work(player_id, ' '.join(args))
    await ctx.send(response)
    gacha_game.save()

bot.run(TOKEN)