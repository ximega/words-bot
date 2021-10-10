from discord import Member, TextChannel
from discord.ext.commands import Context
from .exceptions import NoSetException, NoPlayersException

class GameLogic:
    def __init__(self):
        self.__players = []
        self.__setStarted = False
        self.__spokenWords = []
        self.__gameStarted = False
        self.__gameChannel = None
        self.prewSaid = -1
        self.lastLetter = ''

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

    @property
    def gameChannel(self):
        return self.__gameChannel

    @property
    def spokenWords(self):
        return self.__spokenWords

    def appendSpokenWord(self, word):
        self.__spokenWords.append(word)

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

    async def NextPlayer(self, ctx: Context, prew: Member) -> Member:
        prewIndex = self.players.index(prew)
        if prewIndex == len(self.players) - 1:
            prewIndex = -1

        nextPlayer = self.players[prewIndex + 1]

        return nextPlayer

    def SetGameChannel(self, channel: TextChannel):
        self.__gameChannel = channel

    async def StartGame(self) -> bool:
        if not self.players:
            raise NoPlayersException("Game doesn't have players")

        self.__gameStarted = True

        return True

    async def FinishGame(self) -> bool:
        self.__gameStarted = False

        return True

Game = GameLogic()