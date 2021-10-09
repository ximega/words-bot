import discord
from discord.ext import commands
import sqlite3
from src.play import GameLogic
from server.sql import Sql
from server.config import TOKEN


intents = discord.Intents.all()

client = commands.Bot(command_prefix = '$', intents = intents, owner_id = 673198630131335179)

@client.event
async def on_ready():
    print(f'Bot connected on TOKEN: {TOKEN}')

    await client.change_presence(activity = discord.Game(name = '$help'), status = discord.Status.dnd)

    Sql.Create()

@client.event
async def on_message(message):
    await client.process_commands(message)

client.run(TOKEN)