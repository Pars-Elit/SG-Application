from pymongo import *

MONGO_ADDRESS = '192.168.1.68'
CSV_FILE = 'ML_Partidas.csv'

values2Exclude = {
    'damageTakenDiffPerMinDeltas':'',
    'csDiffPerMinDeltas':'',
    'xpDiffPerMinDeltas':'',
    'creepsPerMinDeltas':'',
    'xpPerMinDeltas':'',
    'goldPerMinDeltas':'',
    'damageTakenPerMinDeltas':'',
    '0-10':'',
    '10-20':'',
    '20-30':'',
    '30-end':''
}
# {'participants.stats.perk1':null}
values2Convert = {
    'NONE':0,
    'DUO_SUPPORT':1,
    'DUO':2,
    'DUO_CARRY': 3,
    'BOTTOM':4,
    'JUNGLE':5,
    'SOLO':6,
    'MIDDLE': 7,
    'TOP':8,
    'UNRANKED':9,
    'MASTER':10,
    'DIAMOND':11,
    'CHALLENGER':12,
    'GRANDMASTER':13,
    'GOLD':14,
    'IRON':15,
    'SILVER':16,
    'PLATINUM':17,
    'BRONZE':18

}

def getKeyName(dictName, key):
    if len(dictName) > 0:
        return dictName + '.' + key
    return key

def extractAttrs(obj, justLabel=False, dictName=''):
    """
    Receive a object and extract its values for a list
    
    Parameters
    ----------
    obj : dict
        A dict to be extracted
    justLabel : bool, optional
        A flag used to indicate whether should returns only the labels (default is
        False)
    
    Returns
    -------
    list
        A list of values extracted from obj parameter
    """
    return extractAttrsCore(obj, {}, justLabel, dictName)

def extractAttrsCore(obj, dontRepeat, justLabel=False, dictName=''):
    """
    Show extractAttrs
    """
    response = []
    if type(obj) == type({}):
        for key in obj:
            if not key in values2Exclude and not key in dontRepeat:
                dontRepeat[getKeyName(dictName, key)] = ''
                newObj = obj[key]
                if justLabel and type(newObj) != type({}):
                    newObj = getKeyName(dictName, key)
                response += extractAttrsCore(newObj, dontRepeat, justLabel, key)
    else:
        # handles the non dict values
        if not justLabel:
            try:
                obj = float(obj)
            except:
                if obj in values2Convert: # 2 comment
                    obj = values2Convert[obj]
                else: # 2 comment
                    # ensuring all the casting are ok
                    raise Exception('[-] put ' + obj) # 2 comment
        response += [obj]
    return response

def processMatch(match, justLabel=False):
    """
    Convert a match from db in a list

    Parameters
    ----------
    match : dict
        A match from 'partidas' collection
    justLabel : bool, optional
        A flag used to indicate whether should returns only the labels (default is
        False)

    Returns
    -------
    list
        A list of values extracted from a match
    """
    response = []
    staticAttrs = [ 'gameId' , 'gameDuration' ]
    if not 'participants' in match or len(match['participants']) < 1:
        raise Exception('[-] wrong match!')
    if justLabel:
        response += staticAttrs
        firstPart = match['participants'][0]
        response += extractAttrs(firstPart, justLabel)
        return response
    for participant in match['participants']:
        partAttrs = []
        # firstly adding the static attributes
        for staticKey in staticAttrs:
            partAttrs += [match[staticKey]]
        # then the others
        partAttrs += extractAttrs(participant)
        response.append(partAttrs)
    return response

def writeList2File(filename, array, overwrite=False, separator=';'):
    """
    Write a list for a file

    Parameters
    ----------
    filename : str
        A file to be written
    array : list
        A list to get the values 
    overwrite : bool, optional
        A flag used to indicate whether should overwrite the file (default is False)
    separator : str, optional
        A separator symbol to csv (default is ';')
    """
    mode = 'a'
    if overwrite:
        mode = 'w'
    file = open(filename, mode)
    file.write(separator.join(map(str,array)) + '\n')

def getMatchQuery(db):
    """
    Returns a specific mongo match query

    Parameters
    ----------
    db : pymongo.database.Database
        A mongo client instance
    
    Returns
    -------
    pymongo.cursor.Cursor
        A query cursor
    """
# "4222851889.0"
    return db.partidas.find({'gameDuration': {"$gt": 300.0}, 'participants.stats.perkSubStyle':{"$ne":None}, 'participants.stats.statPerk0':{"$ne":None}})#.sort('gameId')

def main(mongoAddress, csvFile):
    db = MongoClient('mongodb://' + mongoAddress).SG_database
    total = getMatchQuery(db).count()
    if total < 1:
        raise Exception('[-] check the query')
    # bufferSize = 10240
    counter = 0
    firstLine = True
    # for i in range(int(total/bufferSize)+1):
    # for match in getMatchQuery(db).limit(bufferSize).skip(i*bufferSize):
    for match in getMatchQuery(db):
    # print('\x0D' + str(round(i*bufferSize*100/total,2)) + '%    ', end='')
        print('\x0D' + str(round(counter*100/total,2)) + '%    ', end='')
        counter += 1
        # putting the label
        if firstLine:
            writeList2File(csvFile, processMatch(match, firstLine), True)
            firstLine = False
        # putting the processed data in file
        for array in processMatch(match):
            if len(array) != 113:
                raise Exception('deu ruim no tamanho, gd: ' + str(array[:4]) + ' len: ' + str(len(array)))
            writeList2File(csvFile, array)
    print('\x0D' + '100.0%', end='')

if __name__ == '__main__':
    main(MONGO_ADDRESS, CSV_FILE)