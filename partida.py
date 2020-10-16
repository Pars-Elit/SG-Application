import re
from player_champion_history import PlayerChampionHistory

class Partida():

    def __init__(self):
        
        self.gameId = None
        self.playersNaPartida = {}
        
        self.nameParticipantId = None
        self.championId = None
        
        self.spell1Id = None
        self.spell2Id = None
        
        self.win = None

        self.kills = None
        self.deaths = None
        self.assists = None
        
        self.item0 = None
        self.item2 = None
        self.item3 = None   
        self.item4 = None
        self.item5 = None
        self.wardItem = None # Player's Ward
    
    # def __str__(self):
    #     return self.gameId
    def imprimir(self):
        return {'gameId' : self.gameId, 'playersNaPartida': self.playersNaPartida, 'nameParticipantId': self.nameParticipantId, 'championId': self.championId, 'spell1Id': self.spell1Id, 'spell2Id': self.spell2Id, 'win': self.win, 'kills': self.kills, 'deaths': self.deaths, 'assists': self.assists, 'item0': self.item0, 'item1': self.item1, 'item2': self.item2, 'item3': self.item3, 'item4': self.item4, 'item5': self.item5, 'wardItem':self.wardItem}

    def __str__(self):
        return str(self.imprimir())