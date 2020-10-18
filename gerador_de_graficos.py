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

#GRÁFICO COLUNAS
# x= np.arange(10)
# money = [creepscore[0], creepscore[1], creepscore[2], creepscore[3], creepscore[4], creepscore[5], creepscore[6], creepscore[7], creepscore[8], creepscore[9]]

# def linhaY(x, pos):    
#     return '%d' % (x)

# formatter = FuncFormatter(linhaY)

# fig, ax = plt.subplots()
# ax.yaxis.set_major_formatter(formatter)
# plt.bar(x, money)
# plt.xticks(x, (championName[0], championName[1], championName[2], championName[3], championName[4], championName[5], championName[6], championName[7], championName[8], championName[9]))
# plt.title("CS per Champion", fontsize=18)
# plt.show()
################################################################

wards= wardsPlaced+controlWards 

plt.plot([wardsPlaced[0], wardsPlaced[1], wardsPlaced[2], wardsPlaced[3], wardsPlaced[4], wardsPlaced[5], wardsPlaced[6], wardsPlaced[7], wardsPlaced[8], wardsPlaced[9]], [championName[0], championName[1], championName[2], championName[3], championName[4], championName[5], championName[6], championName[7], championName[8], championName[9]], 'ro')
# plt.plot([deaths[0], deaths[1], deaths[2], deaths[3], deaths[4], deaths[5], deaths[6], deaths[7], deaths[8], deaths[9]], 'ro')
plt.title("Wards Placed per Champion", fontsize=18)
plt.show()

# ax = plt.gca()

# df.plot(kind='line',x='creepscore',y='num_children',ax=ax)
# df.plot(kind='line',x='totalDmg',y='num_pets', color='red', ax=ax)

# plt.show()


# ts = pd.Series(,
#    .....:                index=pd.date_range('1/1/2000', periods=1000))
#    .....: 

# ts = ts.cumsum()
# ts.plot()

# [ ] Topico 4: Pelo menos um gráfico de caixa e um gráfico de colunas devem ser gerados. Atualize o artigo incluindo uma seção "Análise Exploratória dos Dados", na qual você deve apresentar os principais 'insights' que você obteve sobre os dados e as medidas e gráficos que lhe levaram a ter estes 'insights'.  
# [ ] Topico 5: Referencial teórico do artigo, incluindo um pequeno exemplo da aplicação do algoritmo de ML.
# [ ] Topico 7: ~esse eu nao sei se tem algo~