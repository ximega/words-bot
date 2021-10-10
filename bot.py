import discord
from discord.ext import commands
from discord.member import Member
from src.exceptions import NoPlayersException, NoSetException
from src.play import Game
from server.sql import Sql
from server.config import TOKEN
import logging
from discord.ext.commands import errors
import asyncio


logging.basicConfig(level = logging.INFO)

intents = discord.Intents.all()

client = commands.Bot(command_prefix = '$', intents = intents, owner_id = 673198630131335179)

@client.event
async def on_ready():
    print('\n\n\n\n\n' + '#'*100 + f'\nBot connected on TOKEN: {TOKEN}')

    await client.change_presence(activity = discord.Game(name = '$help'), status = discord.Status.dnd)

    Sql.Create()

@client.command()
@commands.has_permissions(administrator=True)
async def startset(ctx):
    Game.StartSet()

    await ctx.send('Набор игроков начат.')

@client.command()
@commands.has_permissions(administrator=True)
async def finishset(ctx):
    Game.FinishSet()

    await ctx.send('Набор игроков окончен.')

@client.command(aliases = ['sgc'])
@commands.has_permissions(administrator=True)
async def setgamechannel(ctx, channel: discord.TextChannel):
    Game.SetGameChannel(channel)

    await ctx.send('Установлен канал для игры.')

@client.command(aliases = ['sgch'])
@commands.has_permissions(administrator=True)
async def setgamechannelhere(ctx):
    Game.SetGameChannel(ctx.channel)

    await ctx.send('Установлен канал для игры.')

@client.command()
async def join(ctx):
    # try add player
    try:
        await Game.AddPlayer(ctx.author)

        await ctx.send(f'Вы присоединились к игре, в игре {len(Game.players)}')
    # if set yet hasn't started or finished
    except NoSetException:
        await ctx.send('Набор игроков не начат / игра начата')

@client.command()
@commands.has_permissions(administrator=True)
async def startgame(ctx):
    # if set hasn't finished
    if Game.setStarted:
        await ctx.send(f'Набор игроков еще не закончен!')
        return

    # try start game
    try:
        await Game.StartGame()

        await ctx.send('Игра начата')

        # give timeout
        await asyncio.sleep(2)
        # send if go first player
        await ctx.send(f'Первым ходит - {Game.players[0].mention}')
    # if players aren't in player's list
    except NoPlayersException:
        ctx.send('Не достотачно игроков!')

@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, player: Member):
    Game.RemovePlayer(player)

    if len(Game.players) == 1:
        await ctx.send(f'{Game.players[0]} **выиграл!**')

        Game.FinishGame()
        Sql.InsertPlayerWin(player)

@client.command()
async def top(ctx, page = 1):
    topPlayers = Sql.GetTopPlayers(client)

    for i in range(0, page + 1):
        start = page
        stop = 0

@client.event
async def on_message(message):
    await client.process_commands(message)

    # if message is command or message called by bot
    if (message.content[::][0] == '$') or (message.author.bot):
        return

    # if player doesn't play
    if message.author not in Game.players:
        await message.channel.send(f'{message.author.name} нету в списке игроков')
        return

    # if where message called != game channel
    if message.channel != Game.gameChannel:
        await message.channel.send(f'Вы играете не в том канале!')
        return

    if Game.gameStarted:
        # define who should say in this move
        whoShouldSayIndex = Game.prewSaid + 1
        if whoShouldSayIndex == len(Game.players):
            whoShouldSayIndex = 0
            Game.prewSaid = -1

        if message.author == Game.players[whoShouldSayIndex]:
            # define last letter and first letter in word
            lastLetter = message.content[::][-1].lower()
            firstLetter = message.content[::][0].lower()
            # define next player
            nextPlayer = await Game.NextPlayer(message.channel, message.author)

            # if in Game Object saved last letter != first letter
            if (Game.lastLetter != firstLetter) and (Game.lastLetter != ''):
                await message.channel.send(f'Ваше слово не начинается на букву {Game.lastLetter}')
                return

            # if word has already been said
            if (message.content.lower() in Game.spokenWords)  and (Game.spokenWords):
                await message.channel.send(f'Это слово уже было')
                return

            # say for any move
            await message.channel.send(f'Cлово: **{message.content}**, последняя буква: **{lastLetter.upper()}**')
            await message.channel.send(f'Теперь ходит {nextPlayer.mention}')

            # change game settings
            Game.lastLetter = lastLetter
            Game.prewSaid += 1
            Game.appendSpokenWord(message.content.lower())
        
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, errors.CommandNotFound):
        await ctx.send(f'{ctx.author.mention}, Такой команды не сущесвует')

@client.command()
@commands.has_permissions(administrator=True)
async def combine(ctx):
    await setgamechannelhere(ctx)
    await startset(ctx)
    await join(ctx)
    await finishset(ctx)
    await startgame(ctx)

client.run(TOKEN)