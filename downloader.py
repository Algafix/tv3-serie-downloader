################################################
#  𝔞𝔩𝔢𝔦𝔵 𝔞𝔫𝔡 𝔰𝔦𝔩𝔳𝔦𝔞 | 𝟎𝟒.𝟎𝟐.𝟐𝟑 | 𝔩𝔢𝔲𝔳𝔢𝔫 𝔞𝔫𝔡 𝔟𝔞𝔯𝔠𝔢𝔩𝔬𝔫𝔞 #
################################################

import requests
import json

############### GLOBAL VARIABLES ###############
SERIES_ID = "66256"
SERIES_URL = f"https://api.ccma.cat/videos?version=2.0&_format=json&items_pagina=20&programatv_id={SERIES_ID}"
EPISODE_URL = "https://api-media.ccma.cat/pvideo/media.jsp?idint="
HEADERS = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'}

############### LOAD DOWNLOADED EPISODES ###############
capitols_descarregats = []
with open("episodes.json","r") as openfile:
    capitols_descarregats = json.load(openfile)

############### GENERATE LISTS OF EPISODES ###############
response = requests.request("GET", SERIES_URL, headers=HEADERS)
json_res = response.json()
capitols = json_res["resposta"]["items"]["item"]

llista_capitols = []
for capitol in capitols:
    llista_capitols.append({
        "id" : capitol["id"], 
        "numero" : capitol["capitol"], 
        "titol" : capitol["permatitle"]
        })

############### DOWNLOAD MISSING EPISODES ###############
for capitol in llista_capitols:
    if capitol not in capitols_descarregats:
        print(f"Descarregant capitol {capitol['numero']}: {capitol['titol']}.")
        response = requests.request("GET", EPISODE_URL + str(capitol["id"]), headers=HEADERS)
        json_res = response.json()
        link = json_res["media"]["url"][1]["file"]
        response = requests.request("GET", link, headers=HEADERS)
        open(str(capitol["numero"]) + ". " + capitol["titol"] + ".mp4", 'wb').write(response.content)
        capitols_descarregats.append(capitol)

############### SAVE UPDATED LIST ###############
json_object = json.dumps(llista_capitols, indent=4)
with open("episodes.json","w") as outfile:
    outfile.write(json_object)