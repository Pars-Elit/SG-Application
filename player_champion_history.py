class PlayerChampionHistory():

    def __init__(self):
        self.summonerName = None
        self.win = None
        self.championId = None

        self.spell1Id = None
        self.spell2Id = None

        self.kills = None
        self.deaths = None
        self.assists = None

        self.item0 = None;
        self.item1 = None;
        self.item2 = None;
        self.item3 = None;
        self.item4 = None;
        self.item5 = None;
        self.wardItem = None; #item 6
        self.wardsPlaced = None;
        self.wardsKilled = None;
        self.controlBoughtWards = None
        self.totalDamageDealtToChampions = None

        self.totalFarm = None #totalMinionsKilled + neutralMinionsKilled + neutralMinionsKilledTeamJungle + neutralMinionsKilledEnemyJungle)

    def imprimir(self):
        return {'summonerName' : self.summonerName, 'win': self.win, 'championId': self.championId, 'spell1Id': self.spell1Id, 'spell2Id': self.spell2Id, 'kills': self.kills, 'deaths': self.deaths, 'assists': self.assists, 'item0': self.item0, 'item1': self.item1, 'item2': self.item2, 'item3': self.item3, 'item4': self.item4, 'item5': self.item5, 'wardItem':self.wardItem, 'wardsPlaced':self.wardPlaced, 'wardsKilled': self.wardKilled, 'controlBoughtWards': self.controlBoughtWards, 'totalDamageDealtToChampions': self.totalDamageDealtToChampions}

    def __str__(self):
        return str(self.imprimir())