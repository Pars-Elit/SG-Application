from perfil import Perfil
from partida import Partida
from pymongo import MongoClient
from player_champion_history import PlayerChampionHistory
import re
from flask import Flask
from flask import jsonify
from json import dumps as jsonstring
import json

app = Flask(__name__)


#INICIALIZA BANCO DE DADOS
SG_database = MongoClient('localhost', 27017)
SG_database = MongoClient('mongodb://localhost:27017/')

db = SG_database.SG_database

partidas= db.partidas
perfil = Perfil()

@app.route('/user/<name>', methods=['GET'])
def buscaPerfil(name):
    name = re.compile(name, re.IGNORECASE)

    page = 1
    limit = 10
    #Retornando as ultimas 10('limit') partidas do jogador
    listaPartidas=partidas.find({'participantIdentities.player.summonerName': name}).sort([('gameId', -1)]).skip(limit*(page-1)).limit(limit)
    if listaPartidas.count() == 0:
        return 'tapa'
    
    checkingLastMatch = True
    for partida in listaPartidas:
        if(checkingLastMatch):
            for i in partida['participantIdentities']:
                if (i['player']['summonerName'].lower()) == (name.pattern).lower(): #  Perfil do player
                    nameParticipantId= (i['participantId'])
                    
                    perfil.profileicon= (i['player']['profileIcon'])
                    perfil.platformId= (i['player']['platformId'])
                    perfil.summonerName= (i['player']['summonerName'])
                    break
            checkingLastMatch = False

        partidaObj = Partida()
        
        for i in partida['participants']: #Passa procurando o player
            if (i["participantId"] == nameParticipantId): #Aba com os 10 historicos 
                partidaObj.gameId =  partida['gameId'] 
                partidaObj.championId = i["championId"]
                partidaObj.spell1Id = i["spell1Id"]
                partidaObj.spell2Id = i["spell2Id"]
                partidaObj.win = i["stats"]["win"]
                partidaObj.kills = i["stats"]["kills"]
                partidaObj.deaths = i["stats"]["deaths"]
                partidaObj.assists = i["stats"]["assists"]
                partidaObj.item0 = i["stats"]["item0"]
                partidaObj.item1 = i["stats"]["item1"]
                partidaObj.item2 = i["stats"]["item2"]
                partidaObj.item3 = i["stats"]["item3"]
                partidaObj.item4 = i["stats"]["item4"]
                partidaObj.item5 = i["stats"]["item5"]
                partidaObj.item6 = i["stats"]["item6"]
                
                # **Buscar da API as runas depois**
        perfil.ultimasPartidas[partidaObj.gameId] = partidaObj.__dict__
    return perfil.__dict__
    # return jsonify(json.loads(str(perfil)))

@app.route('/match/<gameId>')
def expandirDadosPartida(gameId):

    partida=partidas.find({'gameId': gameId})
    for player in range(10):
        champion = PlayerChampionHistory()
        champion.summonerName = partida[0]['participantIdentities'][player]['player']['summonerName']
        
        participant = partida[0]['participants'][player]

        champion.win = participant['stats']['win']
        champion.championId = participant["championId"]
        champion.spell1Id = participant["spell1Id"]
        champion.spell2Id = participant["spell2Id"]
        
        stats = participant["stats"]
        
        champion.kills = stats["kills"]
        champion.deaths = stats["deaths"]
        champion.assists = stats["assists"]

        champion.item0 = stats["item0"]
        champion.item1 = stats["item1"]
        champion.item2 = stats["item2"]
        champion.item3 = stats["item3"]
        champion.item4 = stats["item4"]
        champion.item5 = stats["item5"]

        champion.wardItem = stats["item6"]
        champion.wardsPlaced = stats["wardsPlaced"]
        champion.wardsKilled = stats["wardsKilled"]
        champion.controlBoughtWards = stats["visionWardsBoughtInGame"]

        champion.totalFarm = stats["totalMinionsKilled"] + stats["neutralMinionsKilled"] + stats["neutralMinionsKilledTeamJungle"] + stats["neutralMinionsKilledEnemyJungle"]
        champion.totalDamageDealtToChampions = stats["totalDamageDealtToChampions"]

        perfil.ultimasPartidas[gameId]['playersNaPartida'][champion.summonerName] = champion.__dict__
    # print(perfil.ultimasPartidas)
    return perfil.ultimasPartidas[gameId]

app.run(debug=True)
# z= input('')
# buscaPerfil(z)
# x= input('')
# expandirDadosPartida(x)