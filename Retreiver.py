def getHouses(firebase):

    result = firebase.get('/Houses', None)
    return result

def getCharacter(firebase):

    result = firebase.get('/Characters', None)
    return result
