class PlayLogic:
    def __init__(self):
        self.players = []
        

    def AddPlayer(self, player) -> bool:
        """
        Add player to players list
        """

        self.players.append(player)
        
        return True

    def 