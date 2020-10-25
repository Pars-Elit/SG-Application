from .partida import Partida
from .player_champion_history import PlayerChampionHistory

class Perfil(object):
    
    def __init__(self):
        self.summonerName = None
        self.nameParticipantId= None
        self.profileicon = None  
        self.platformId = None #Player Server region
        self.ultimasPartidas = {}


    def imprimir(self):
        return { 'summonerName' : self.summonerName, 'nameParticipantId' : self.nameParticipantId, 'profileicon' : self.profileicon, 'platformId' : self.platformId, 'ultimasPartidas' : self.ultimasPartidas}

    def __str__(self):
        return str(self.imprimir())

    