import discord
from discord.ext import commands
import sqlite3
from exceptions import NoPlayersException, NoSetException
from src.play import Game, GameLogic
from server.sql import Sql
from server.config import TOKEN


intents = discord.Intents.all()

client = commands.Bot(command_prefix = '$', intents = intents, owner_id = 673198630131335179)

@client.event
async def on_ready():
    print(f'Bot connected on TOKEN: {TOKEN}')

    await client.change_presence(activity = discord.Game(name = '$help'), status = discord.Status.dnd)

    Sql.Create()

@client.command()
async def startset(ctx):
    Game.StartSet()

    await ctx.send('Набор игроков начат.')

@client.command()
async def finishset(ctx):
    Game.FinishSet()

    await ctx.send('Набор игроков окончен.')

@client.command()
async def setgamechannel(ctx, channel: discord.TextChannel):
    Game.SetGameChannel(channel)

    await ctx.send('Установлен канал для игры.')

@client.command()
async def setgamechannelhere(ctx):
    Game.SetGameChannel(ctx.channel)

    await ctx.send('Установлен канал для игры.')

@client.command()
async def join(ctx):
    try:
        await Game.AddPlayer(ctx.author)

        await ctx.send(f'Вы присоединились к игре, в игре {len(Game.players)}')
    except NoSetException:
        await ctx.send('Набор игроков не начат / игра начата')

@client.command()
async def startgame(ctx):
    try:
        await Game.StartGame()

        await ctx.send('Игра начата')
    except NoPlayersException:
        ctx.send('Не достотачно игроков!')

@client.event
async def on_message(message):
    await client.process_commands(message)

    if Game.gameStarted:
        #############################
        # TUT PORODOLJIT !!!!
        #############################
        #############################
        #############################
        #############################
        #############################
        #############################
        #############################
        #############################
        #############################
        #############################
        #############################
        #############################
        pass

client.run(TOKEN)