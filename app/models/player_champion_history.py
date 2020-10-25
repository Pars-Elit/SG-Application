class PlayerChampionHistory():

    def __init__(self):
        self.summonerName = None
        self.win = None
        self.championIcon = None
        self.championName = None

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
        self.creepScore = None
        self.wardsPlaced = None;
        self.wardsKilled = None;
        self.controlBoughtWards = None
        self.totalDamageDealtToChampions = None

        self.totalFarm = None #totalMinionsKilled + neutralMinionsKilled + neutralMinionsKilledTeamJungle + neutralMinionsKilledEnemyJungle)

        self.perkPrimaryStyle= None
        self.perkSubStyle= None
