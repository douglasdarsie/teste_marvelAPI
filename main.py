import marvel
import keys

marvelClass = marvel.characterData("Iron Man", keys.public_key, keys.private_key)
marvelClass.getCharacterEvents("Iron Man")

strTable = "<html>\n\t<body>\n\t\t<table>\n\t\t\t<tr>\n\t\t\t\t<th>Marvel table</th>\n\t\t\t\t<th></th>\n\t\t\t</tr>"

strRW = "\n\t\t\t<tr>\n\t\t\t\t<td>"+"Character Name"+ "</td>\n\t\t\t\t<td>"+str(marvelClass.charName)+"</td>\n\t\t\t</tr>"
strTable = strTable+strRW
strRW = "\n\t\t\t<tr>\n\t\t\t\t<td>Character Image</td>\n\t\t\t\t<td><img src=\""+str(marvelClass.charImage)+"\" alt=\"pic\"/></td>\n\t\t\t</tr>"
strTable = strTable+strRW
strRW = "\n\t\t\t<tr>\n\t\t\t\t<td>Description</td>\n\t\t\t\t<td>"+str(marvelClass.charDesc)+"</td>\n\t\t\t</tr>"
strTable = strTable+strRW
strRW = "\n\t\t\t<tr>\n\t\t\t\t<td>Description</td>\n\t\t\t\t<td>"+str(marvelClass.atribText)+"</td>\n\t\t\t</tr>"
strTable = strTable+strRW
strRW = "\n\t\t</table>"
strTable = strTable+strRW

strRW ="\n\t\t<table>\n\t\t\t<tr>\n\t\t\t\t<th>Related Characters - "+str(marvelClass.charName)+"</th>\n\t\t\t\t<th></th>\n\t\t\t</tr>"
strTable = strTable+strRW

for i in range(len(marvelClass.relatedCharsImg)):
    strRW = "\n\t\t\t<tr>\n\t\t\t\t<td>"+str(marvelClass.relatedChars[i])+"</td>\n\t\t\t\t<td><img src=\""+str(marvelClass.relatedCharsImg[i])+"\" alt=\"pic\"/></td>\n\t\t\t</tr>"
    strTable = strTable+strRW

strTable = strTable+"\n\t\t</table>\n\t</body>\n</html>"
hs = open("marvel.html", 'w')
hs.write(strTable)
# print strTable