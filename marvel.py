import requests
from hashlib import md5
from time import time
import keys

public_key = keys.public_key
private_key = keys.private_key

class characterData():
    def __init__(self):
        self.publicKey = public_key
        self.privKey = private_key
        self.basicURL = "https://gateway.marvel.com/"
        self.charName = ""
        self.charDesc = ""
        self.charID = 0
        self.charImage = ""
        self.atribText = ""
        self.charEventListID = []
        self.charEventListTitle = []
        self.relatedChars = []
        self.relatedCharsImg = []
        
    def getCharacterData(self,characterName:str):
        m = md5()
        ts = str(time())
        m.update(bytes(ts,'utf-8'))
        m.update(bytes(self.privKey,'utf-8'))
        m.update(bytes(self.publicKey,'utf-8'))
        hash_key = m.hexdigest()
        endpoint = "&orderBy=name&limit=1"
        url = self.basicURL + "v1/public/characters?name=" + characterName + endpoint
        payload = {"ts":ts,"apikey":public_key,"hash":hash_key}
        rChar = requests.get(url , params=payload)
        dataJson = rChar.json()
        
        self.charName = dataJson["data"]["results"][0]["name"]
        self.charDesc = dataJson["data"]["results"][0]["description"]
        self.charID = dataJson["data"]["results"][0]["id"]
        self.atribText = dataJson["attributionText"]
        
        self.charImage = dataJson["data"]["results"][0]["thumbnail"]["path"] + "/portrait_xlarge." + dataJson["data"]["results"][0]["thumbnail"]["extension"]
        
        baseUrl = self.basicURL+"v1/public/events?characters="
        endpoint = "&orderBy=name&limit=100&"
        url = baseUrl + str(self.charID) + endpoint
        payload = {"ts":ts,"apikey":public_key,"hash":hash_key}
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
            payload = {"ts":ts,"apikey":public_key,"hash":hash_key}
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
            payload = {"ts":ts,"apikey":public_key,"hash":hash_key}
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