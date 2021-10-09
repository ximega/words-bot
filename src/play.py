from discord import Member, TextChannel
from discord.ext.commands import Context
from .exceptions import NoSetException, NoPlayersException

class GameLogic:
    def __init__(self):
        self.__players = []
        self.__setStarted = False
        self.__spokenWords = []
        self.__gameStarted = False

    @property
    def setStarted(self):
        return self.__setStarted

    @setStarted.setter
    def setStarted(self, value: bool) -> bool:
        if not isinstance(value, bool):
            return False

        self.__setStarted = value

    @property
    def players(self):
        return self.__players

    @property
    def gameStarted(self):
        return self.__gameStarted

    async def AddPlayer(self, player: Member) -> bool:
        """
        Add player to players list
        """

        if not self.setStarted:
            raise NoSetException("No set started or set finished")

        self.__players.append(player)
        
        return True

    def RemovePlayer(self, player: Member) -> bool:
        self.__players.remove(player)

        return True

    def StartSet(self) -> bool:
        self.setStarted = True

        return True

    def FinishSet(self) -> bool:
        self.setStarted = False

        return True

    async def NextPlayer(self, ctx: Context, prew: Member):
        nextPlayerIndex = self.players.index(prew) + 1
        if nextPlayerIndex == len(self.players) - 1:
            nextPlayerIndex = 0

        nextPlayer = self.players[nextPlayerIndex]

        await ctx.send(f'{nextPlayer.mention} your move!')

    def SetGameChannel(self, channel: TextChannel):
        self.__gameChannel = channel

    async def StartGame(self) -> bool:
        if not self.players:
            raise NoPlayersException("Game doesn't have players")

        self.__gameStarted = False

        return True

Game = GameLogic()