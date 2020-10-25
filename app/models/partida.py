import re
from .player_champion_history import PlayerChampionHistory

class Partida():

    def __init__(self):
        
        self.gameId = None
        self.playersNaPartida = {}
        
        self.nameParticipantId = None
        self.championIcon = None
        self.championName = None
        
        self.gameDuration = None
        self.spell1Id = None
        self.spell2Id = None
        self.creepScore = None
        self.win = None

        self.kills = None
        self.deaths = None
        self.assists = None
        
        self.item0 = None
        self.item1 = None
        self.item2 = None
        self.item3 = None   
        self.item4 = None
        self.item5 = None
        self.wardItem = None # Player's Ward

        self.perkPrimaryStyle= None
        self.perkSubStyle= None
