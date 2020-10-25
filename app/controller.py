from models.perfil import Perfil
from models.partida import Partida
from models.player_champion_history import PlayerChampionHistory
from pymongo import MongoClient
from flask import Flask, render_template
import re, os


app = Flask(__name__)


SG_database = MongoClient('localhost', 27017)
SG_database = MongoClient('mongodb://192.168.1.68:27017/')

db = SG_database.SG_database

champions= db.riot_champion
partidas= db.partidas
perksStyleFile= db.perkStyles
perksFile = db.perks
summonerSpells= db.summoner_spells

perfil = Perfil()

def convertRuneIconLink(iconPath):
    return 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default' + iconPath[iconPath.find('/v1'):].lower()

def convertSpellIconLink(iconPath):
    return 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/data' + iconPath[iconPath.find('/Spells'):].lower()

def getProfileIconLink(iconPath):
    return 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/' + str(iconPath)+'.jpg'

def getChampionIconLink(iconPath):
    return 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/' + str(iconPath)+'.png'    


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/user/<name>', methods=['GET'])
def buscaPerfil(name):
    name = re.compile(name, re.IGNORECASE)

    page = 1
    limit = 10
    listaPartidas=partidas.find({'participantIdentities.player.summonerName': name}).sort([('gameId', -1)]).skip(limit*(page-1)).limit(limit)
    if listaPartidas.count() == 0:
        return 'Nenhuma partida'
    
    for partida in listaPartidas:
        partidaObj = Partida()       
        for i in partida['participantIdentities']:
            if re.search(name.pattern.lower(), i['player']['summonerName'].lower()): #  Perfil do player
                nameParticipantId = i['participantId']
                perfil.profileicon= getProfileIconLink(i['player']['profileIcon'])
                perfil.platformId= (i['player']['platformId'])
                perfil.summonerName= (i['player']['summonerName'])
                break
        for i in partida['participants']: #Passa procurando o player
            if i["participantId"] == nameParticipantId: #Aba com os 10 historicos 
                partidaObj.gameId = partida['gameId'] 
                partidaObj.gameDuration = partida['gameDuration']
                championData=champions.find({'key': i['championId']})
                for champion in championData:
                    partidaObj.championName= champion['name'] #Exibir esse nome no frontend
                    partidaObj.championIcon= getChampionIconLink(champion['key']) #Usar ao buscar o champion na pasta de ícones, championId difere-se de championName em algumas ocasiões. Por exemplo em um nome com espaço

                spells=summonerSpells.find({'id': i["spell1Id"]})
                partidaObj.spell1Id= convertSpellIconLink(spells[0]["iconPath"])
                spells=summonerSpells.find({'id': i["spell2Id"]})
                partidaObj.spell2Id= convertSpellIconLink(spells[0]["iconPath"])
                
                
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
                partidaObj.wardItem = i["stats"]["item6"]
                
                
                perkPrimaryStyle = i['stats']['perk0']
                perkSubStyle= i['stats']['perkSubStyle']
                
                
                perks = perksFile.find({'id': perkPrimaryStyle})
                for perk in perks:
                    if(perk["id"] == perkPrimaryStyle):
                        partidaObj.perkPrimaryStyle= convertRuneIconLink(perk['iconPath'])
                        break


                perksStyle=perksStyleFile.find_one()                
                        
                for perk in perksStyle['styles'] :                
                    if perk['id'] == perkSubStyle:
                        partidaObj.perkSubStyle= convertRuneIconLink(perk['iconPath'])
                        break
                break

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

        championId= participant['championId']
        championData=champions.find({'key': championId})
        for i in championData:
            champion.championName= i['name'] #Exibir esse nome no frontend
            champion.championId= i["id"] #Usar ao buscar o champion na pasta de ícones, championId difere-se de championName em algumas ocasiões. Por exemplo em um nome com espaço

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

        perkPrimaryStyle = stats['perk0']
        perkSubStyle= stats['perkSubStyle']

        perksStyle=perksStyleFile.find_one()                
        for perk in perksStyle['styles'] :
            if( perk["id"] == perkSubStyle):
                champion.perkSubStyle = convertRuneIconLink(perk["iconPath"])
                break

        perks = perksFile.find({'id': perkPrimaryStyle})
        for perk in perks:
            print(perks)
            if( perk["id"] == perkPrimaryStyle):
                champion.perkPrimaryStyle = convertRuneIconLink(perk["iconPath"])
                break

        champion.wardItem = stats["item6"]
        champion.wardsPlaced = stats["wardsPlaced"]
        champion.wardsKilled = stats["wardsKilled"]
        champion.controlBoughtWards = stats["visionWardsBoughtInGame"]

        champion.totalFarm = stats["totalMinionsKilled"] + stats["neutralMinionsKilled"] + stats["neutralMinionsKilledTeamJungle"] + stats["neutralMinionsKilledEnemyJungle"]
        champion.totalDamageDealtToChampions = stats["totalDamageDealtToChampions"]

        perfil.ultimasPartidas[gameId]['playersNaPartida'][champion.summonerName] = champion.__dict__

    return perfil.ultimasPartidas[gameId]


@app.route("/<path:path>")
def getResources(path):
    return app.send_static_file(path)

app.run(debug=True)

# z= input('')
# buscaPerfil(z)
# x= input('')
# expandirDadosPartida(x)