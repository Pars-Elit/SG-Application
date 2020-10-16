import ast
from pymongo import MongoClient

#INICIALIZA BANCO DE DADOS
SG_database = MongoClient('localhost', 27017)
SG_database = MongoClient('mongodb://localhost:27017/')

db = SG_database.SG_database

partidas= db.partidas

def lerPartidasIndividuais():

    # Inicializar arquivos
    # listaPartidas = open('match_data_version1.csv', 'r', encoding='UTF-8')
    vaiLegendar = True
    with open("match_data_version1.csv", "r", encoding="UTF-8") as listaPartidas:
        for linha in listaPartidas:

            #Primeira linha apenas as legendas
            if(vaiLegendar):
                # Definir chaves, split primeira linha
                legendas = linha.replace('\n','').split(',')
                legendas.pop(0)
                vaiLegendar = False
                continue
                
            # Split n vezes a partir da 2ª linha
            dadosPartida = linha.replace('\n','').split('"')

            # InformacoesGerais (gameCreation,gameDuration,gameId,gameMode,gameType,gameVersion,mapId,platformId,queueId,seasonId,status.message,status.status_code)
            informacoesGerais = dadosPartida[0].split(',')
            informacoesGerais.pop(0)
            infos2= dadosPartida[4].split(',')
            infos2.pop(0)
            
            for i in infos2:
                informacoesGerais.append(i)
            informacoesGerais.pop(7)

            #Criação de todas as variaveis
            gameCreation = informacoesGerais[0]
            gameDuration = informacoesGerais[1]
            gameId = informacoesGerais[2]
            gameMode = informacoesGerais[3]
            gameType = informacoesGerais[4]
            gameVersion = informacoesGerais[5]
            mapId = informacoesGerais[6]
            platformId = informacoesGerais[7]
            queueId = informacoesGerais[8]
            seasonId = informacoesGerais[9]
            statusMessage = informacoesGerais[10]
            statusStatusCode = informacoesGerais[11]

            #participantIdentities
            participantIdentities = dadosPartida[1]
            participantIdentities = ast.literal_eval(participantIdentities) #Transforma string em uma lista
            
            #participants
            participants = dadosPartida[3]
            participants = ast.literal_eval(participants) #Transforma string em uma lista

            partida = {
                        'gameCreation': gameCreation,
                        'gameDuration': gameDuration,
                        'gameId': gameId,
                        'gameMode': gameMode,
                        'gameType': gameType,
                        'gameVersion': gameVersion,
                        'mapId': mapId,
                        'participantIdentities': participantIdentities,
                        'participants': participants,
                        'platformId': platformId,
                        'queueId': queueId,
                        'seasonId': seasonId,
                        'statusMessage': statusMessage,
                        'statusStatusCode': statusStatusCode
            }
            partidas.insert_one(partida)

    #Finalizar Arquivos
    listaPartidas.close()

    return 

lerPartidasIndividuais()
print('done')