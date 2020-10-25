from .partida import Partida
from .player_champion_history import PlayerChampionHistory

class Perfil(object):
    
    def __init__(self):
        self.summonerName = None
        self.nameParticipantId= None
        self.profileIcon = None  
        self.platformId = None #Player Server region
        self.ultimasPartidas = {}


    
    