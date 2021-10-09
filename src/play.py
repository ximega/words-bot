from discord import Member
from discord.ext.commands import Context
from .exceptions import NoSetException

class GameLogic:
    def __init__(self):
        self.__players = []
        self.__setStarted = False

    @property
    def setStarted(self):
        return self.__setStarted

    @setStarted.setter
    def setStarted(self, value: bool) -> bool:
        if not isinstance(value, bool):
            return False

        self.__setStarted = value

    def AddPlayer(self, player: Member) -> bool:
        """
        Add player to players list
        """

        if not self.setStarted:
            raise NoSetException("No set started or set finished")

        self.__players.append(player)
        
        return True

    def StartSet(self) -> bool:
        self.setStarted = True

        return True

    def FinishSet(self) -> bool:
        self.setStarted = False

        return True

    async def NextPlayer(self, ctx: Context, prew: Member):
        nextPlayerIndex = self.__players.index(prew) + 1
        if nextPlayerIndex == len(self.__players) - 1:
            nextPlayerIndex = 0

        nextPlayer = self.__players[nextPlayerIndex]

        await ctx.send(f'{nextPlayer.mention} your move!')