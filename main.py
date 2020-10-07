import ast

def lerPartidasIndividuais():

# Inicializar arquivos
    listaPartidas = open('casoTeste.csv', 'r', encoding='UTF-8')
    championsId = open('riot_champion.csv', 'r', encoding='UTF-8')
    arquivoTeste = open('arquivoTeste.csv', 'r+', encoding='UTF-8')
    arquivoPartidas = open('arquivoPartidas.csv', 'w+', encoding='UTF-8')
    arquivoJogadores = open('arquivoJogadores.csv', 'w+', encoding='UTF-8')
    # arquivoChampions = open('arquivoChampions.csv', 'w+', encoding='UTF-8')

# Definir chaves, split primeira linha    
    legendas= listaPartidas.readline().replace('\n','').split(',')
    legendas.pop(0)

# Split n vezes a partir da 2ª linha
    dadosPartida = listaPartidas.readline().replace('\n','').split('"')
# InformacoesGerais (gameCreation,gameDuration,gameId,gameMode,gameType,gameVersion,mapId,platformId,queueId,seasonId,status.message,status.status_code)
    informacoesGerais = dadosPartida[0].split(',')
    informacoesGerais.pop(0)
    infos2= dadosPartida[4].split(',')
    infos2.pop(0)
    for i in infos2:
        informacoesGerais.append(i)

    #Criação de todas as variaveis, utilizadas no momento ou não
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
    
    # Adiciona na lista de jogadores os jogadores que ainda não estão nela
    # Adiciona o 'gameId' da partida aos jogadores que estavam nela
    listaJogadores={}        
    for i in participantIdentities:
        #Se o 'summonerName' nao existir na listaJogadores, adiciona ele junto com o 'gameId'
        if (i['player']['summonerName']) not in listaJogadores: 
            listaJogadores[i['player']['summonerName']]= gameId
        #Se o 'summonerName' existir na lista verifica se o 'gameId' ja existe dentro do 'summonerName' e nao adiciona ele caso necessário
        if (i['player']['summonerName']) in listaJogadores: 
            if gameId not in listaJogadores[i['player']['summonerName']]:
                listaJogadores[i['player']['summonerName']]= '%s, %s' %(listaJogadores[i['player']['summonerName']],gameId)

    # Salva no arquivoJogadores o 'summonerName' e, dentro dele, uma lista com o 'gameId' dos jogos que ele participou
    for i in listaJogadores:         
        #Escreve nome do jogador e, separando por ': ', a lista com o 'gameId'
        arquivoJogadores.write('%s: %s, \n' %(i,listaJogadores[i])) 

    #participants
    participants = dadosPartida[3]
    participants = ast.literal_eval(participants)
    
    #Salva no arquivoPartidas o 'gameId' e, dentrodele, uma lista com o 'participantIdentities' e 'participant' da partida
    dicioPartidas={}
    dicioPartidas[gameId]= participantIdentities, participants
    for i in dicioPartidas:
        arquivoPartidas.write('%s: %s, \n' %(i,dicioPartidas[i]))
    
    #Lê o arquivo 'riot_champion.csv' e salva no dicionário 'champions' as respectivas 'key' e 'name' dos campeões
    # legendaChampions= championsId.readline().replace('\n', '').split(',') #DELETAR
    champions={}
    for i in championsId:
        champion= i.replace('\n', '').split(',')
        champions[champion[3]]= champion[4]

    #Finalizar Arquivos
    listaPartidas.close()
    championsId.close()
    arquivoTeste.close()
    arquivoPartidas.close()
    arquivoJogadores.close()
    
    return 
    
lerPartidasIndividuais()