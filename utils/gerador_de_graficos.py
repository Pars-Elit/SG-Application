from os import name
from pymongo import MongoClient
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

#INICIALIZA BANCO DE DADOS
SG_database = MongoClient('localhost', 27017)
SG_database = MongoClient('mongodb://localhost:27017/')

db = SG_database.SG_database
champions= db.riot_champion
partidas= db.partidas

wins = []
kills = []
deaths = []
assists=[]

totalDmg = []
controlWards = []
wardsPlaced = []
wardsKilled = []
creepscore = []
championName= []
xpPerMinDeltas0to10=[]
xpPerMinDeltas10to20=[]

page = 1
limit = 1 #Quantidade de partidas a serem analisadas
partidas=partidas.find({'platformId': 'KR'}).skip(limit*(page-1)).limit(limit)
for partida in partidas:

    for player in range(10):
        path= partida['participants'][player]['stats']
        wins.append(path['win'])

        championId= (partida['participants'][player]['championId'])
        championData=champions.find({'key': championId})
        for champion in championData:
            championName.append(champion['name'])

        kills.append(path['kills'])
        deaths.append(path['deaths'])
        assists.append(path['assists'])
        totalDmg.append(path['totalDamageDealtToChampions'])
        controlWards.append(path['visionWardsBoughtInGame'])
        wardsPlaced.append(path['wardsPlaced'])
        wardsKilled.append(path['wardsKilled'])
        creepscore.append(path['totalMinionsKilled'] + path['neutralMinionsKilled'] + path['neutralMinionsKilledTeamJungle'] + path['neutralMinionsKilledEnemyJungle'])
        
        xpPerMinDeltas0to10.append((partida['participants'][player]['timeline']['xpPerMinDeltas']['0-10']))
        xpPerMinDeltas10to20.append((partida['participants'][player]['timeline']['xpPerMinDeltas']['10-20']))

    xpPerMinDeltas0to10.sort()
    xpPerMinDeltas10to20.sort()


df = pd.DataFrame({'Champion': championName,
                'Win': wins,
                'Kills': kills, 
                'Deaths': deaths,
                'Assists': assists,
                'Creep Score': creepscore,
                'totalDamageDealtToChampions': totalDmg,
                'wardsBoughtInGame': controlWards, 
                'wardsPlaced': wardsPlaced,
                'wardsKilled': wardsKilled                   
})
df.to_csv('planilhaPartida_exemplo.csv')

print(df)

print(xpPerMinDeltas0to10, xpPerMinDeltas10to20)

#GRÁFICO DE COLUNAS
# CS per Champion

x= np.arange(10)
cs = [creepscore[0], creepscore[1], creepscore[2], creepscore[3], creepscore[4], creepscore[5], creepscore[6], creepscore[7], creepscore[8], creepscore[9]]

def linhaY(x, pos):    
    return '%d' % (x)

formatter = FuncFormatter(linhaY)

fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(formatter)
plt.bar(x, cs)
plt.xticks(x, (championName[0], championName[1], championName[2], championName[3], championName[4], championName[5], championName[6], championName[7], championName[8], championName[9]))
plt.title("CS per Champion", fontsize=18)
plt.xlabel('Champions')
plt.ylabel('Creep Score')

plt.show()



################################################################

#GRAFICO 2
#Wards Placed per Champion

wards= [None]*10
for i in range(10):
    wards[i]= wardsPlaced[i]+controlWards[i]

line1, = plt.plot([championName[0], championName[1], championName[2], championName[3], championName[4], championName[5], championName[6], championName[7], championName[8], championName[9]], [wards[0], wards[1], wards[2], wards[3], wards[4], wards[5], wards[6], wards[7], wards[8], wards[9]], label="Wards", linewidth=1.5 )

line2, = plt.plot([deaths[0], deaths[1], deaths[2], deaths[3], deaths[4], deaths[5], deaths[6], deaths[7], deaths[8], deaths[9]], label="Deaths", linestyle='--')

first_legend = plt.legend(handles=[line1], loc='upper right')
ax = plt.gca().add_artist(first_legend)
plt.legend(handles=[line2], loc='lower left')

plt.title("Wards Placed and Deaths per Champion", fontsize=18)
plt.xlabel('Champions')
plt.ylabel('Wards Placed')

plt.show()

###################################################################


#GRAFICO DE CAIXAS
#CS boxplot

data = creepscore
plt.boxplot(data) 
plt.title("CS boxplot", fontsize=18)
plt.ylabel('Creepscore')

plt.show()