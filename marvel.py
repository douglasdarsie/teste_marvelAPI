import requests
from hashlib import md5
from time import time

class characterData:
    def __init__(self, characterName:str , publicKey:str , privateKey:str):
        self.publicKey = publicKey
        self.privKey = privateKey
        self.timestamp = str(time())
        self.hash = self.getHash(publicKey,privateKey)
        self.basicURL = "https://gateway.marvel.com/"
        self.basicData = self.getBasicData(characterName)
        self.charName = self.basicData["data"]["results"][0]["name"]
        self.charDesc = self.basicData["data"]["results"][0]["description"]
        self.charID = self.basicData["data"]["results"][0]["id"]
        self.charImage = self.basicData["data"]["results"][0]["thumbnail"]["path"] + "/portrait_xlarge." + self.basicData["data"]["results"][0]["thumbnail"]["extension"]
        self.atribText = self.basicData["attributionText"]
        self.charEventListID = []
        self.charEventListTitle = []
        self.relatedChars = []
        self.relatedCharsImg = []
    
    def getHash(self, publicKey:str, privateKey:str):
        m = md5()
        ts = self.timestamp
        m.update(bytes(ts,'utf-8'))
        m.update(bytes(self.privKey,'utf-8'))
        m.update(bytes(self.publicKey,'utf-8'))
        hash_key = m.hexdigest()
        return hash_key
    
    def getBasicData(self, characterName):
        ts = self.timestamp
        endpoint = "&orderBy=name&limit=1"
        url = self.basicURL + "v1/public/characters?name=" + characterName + endpoint
        payload = {"ts":ts,"apikey":self.publicKey,"hash":self.hash}
        rChar = requests.get(url , params=payload)
        dataJson = rChar.json()
        return dataJson
        
    def getCharacterEvents(self,characterName):
        ts = self.timestamp
        baseUrl = self.basicURL+"v1/public/events?characters="
        endpoint = "&orderBy=name&limit=100&"
        url = baseUrl + str(self.charID) + endpoint
        payload = {"ts":ts,"apikey":self.publicKey,"hash":self.hash}
        rEvents = requests.get(url , params=payload)
        dataJson = rEvents.json()
        charEventListTitle = []
        charEventListID = []
        for item in dataJson["data"]["results"]:
            charEventListID.append(item["id"])
            charEventListTitle.append(item["title"])
        self.charEventListID = charEventListID
        self.charEventListTitle = charEventListTitle
        charPartnersList = []
        for title in charEventListID:
            baseUrl = self.basicURL+"v1/public/events/"
            endpoint = "/characters?orderBy=name&limit=100&"
            url = baseUrl + str(title) + endpoint
            payload = {"ts":ts,"apikey":self.publicKey,"hash":self.hash}
            r = requests.get(url , params=payload)
            dataJson = r.json()
            for item in dataJson["data"]["results"]:
                charPartnersList.append(item["name"])
        charPartnersList = list(dict.fromkeys(charPartnersList))
        charPartnersList.remove(characterName)
        self.relatedChars = charPartnersList
        
        print("getting related characters...")
        charPartnersImg = []
        i = 0
        for charName in charPartnersList:
            baseUrl = self.basicURL+"v1/public/characters?name="
            endpoint = "&orderBy=name&limit=1"
            url = baseUrl + charName + endpoint
            payload = {"ts":ts,"apikey":self.publicKey,"hash":self.hash}
            r = requests.get(url , params=payload)
            dataJson = r.json()
            try:
                charPartnersImg.append(dataJson["data"]["results"][0]["thumbnail"]["path"] + "/portrait_xlarge." + dataJson["data"]["results"][0]["thumbnail"]["extension"])
            except:
                break
            if (i > 20): # this limiter is only here to avoid making too many requests, which would be shutdown by marvel system.
                break
            i += 1
        self.relatedCharsImg = charPartnersImg
        