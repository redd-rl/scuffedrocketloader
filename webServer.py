import json
from pathlib import Path
import pickle
import stat
from typing import Union
from flask import Flask, request, render_template
from flaskwebgui import FlaskUI
import os
import subprocess
os.chdir("app")
import requests
from bs4 import BeautifulSoup
import zipfile
import time
import shutil
def getRocketLeagueMapsUSMaps():
    maps = requests.get("https://celab.jetfox.ovh/api/v4/projects/")
    mapsJson = json.loads(maps.text)
    mapInfo = []
    for customMap in mapsJson:
        customMap: dict
        identifier = customMap.get('id', None)
        name = customMap.get('name', 'Unidentifiable')
        desc = customMap.get('description', 'Could not get description.')
        path = name = customMap.get('path', 'Unidentifiable')
        linkResponse = requests.get(f"https://celab.jetfox.ovh/api/v4/projects/{identifier}/releases")
        linkResponseJson = json.loads(linkResponse.text)
        downloadUrl = linkResponseJson[0]['assets']['links'][0]['direct_asset_url'] if linkResponseJson[0]['assets']['links'][0]['link_type'] == "other" else linkResponseJson[0]['assets']['links'][1]['direct_asset_url']
        imageUrl = linkResponseJson[0]['assets']['links'][0]['direct_asset_url'] if linkResponseJson[0]['assets']['links'][0]['link_type'] == "image" else linkResponseJson[0]['assets']['links'][1]['direct_asset_url']
        author = linkResponseJson[0]['author']['name']
        activeMap = {
                "name": name,
                "author": author,
                "identifier": identifier,
                "path": path,
                "desc": desc,
                "img": imageUrl,
                "download-url": downloadUrl,
                "rlmus": True,
            }
        mapInfo.append(activeMap)
    return mapInfo
def get_map(mapPageUrl: str, identifier: Union[str, int], rlmus: bool, path: str):
    if rlmus == False:
        try:
            ppage = requests.get(mapPageUrl)
            souppp = BeautifulSoup(ppage.text, "html.parser")
            downloadUrl = souppp.find('form', {"id": "download-form"}).get('action')
            request = requests.get(downloadUrl)
        except:
            request = requests.get(mapPageUrl)
        with open(Path.cwd().__str__() + "\\temp\\" + f"{identifier}.zip", "wb") as handle:
            handle.write(request.content)
        try:
            with zipfile.ZipFile(Path.cwd().__str__() + "\\temp\\" + f"{identifier}.zip") as zip_ref:
                extractPath = Path.cwd().__str__() + f"\\temp\\"
                os.mkdir(extractPath + identifier)
                zip_ref.extractall(extractPath + identifier)
            foldername = os.listdir(extractPath + identifier)[0]
            destinationPath = Path.cwd().__str__() + f"\\maps\\"
            os.rename(extractPath + identifier + "\\" + foldername, destinationPath + identifier)
        except zipfile.BadZipFile:
            pass
    else:
        request = requests.get(mapPageUrl)
        with open(Path.cwd().__str__() + "\\temp\\" + f"{identifier}.zip", "wb") as handle:
            handle.write(request.content)
        with zipfile.ZipFile(Path.cwd().__str__() + "\\temp\\" + f"{identifier}.zip") as zip_ref:
            extractPath = Path.cwd().__str__() + f"\\temp\\" + path
            os.mkdir(extractPath + path)
            zip_ref.extractall(extractPath + identifier)
            destinationPath = Path.cwd().__str__() + f"\\maps\\"
            shutil.move(extractPath + path, destinationPath + path)
            
def format_map(customMap: dict):
    templateGridItem = f""""
    <div class="grid-container">
    <article class="grid-item">
      <a class="grid-item-image">
        <img src="{customMap.get('img')}">
        <h1>
        {customMap.get('name')} 
        </h1>
        <h2>
        {customMap.get('author')}
        </h2>
        <p>
        {customMap.get('desc')}
        </p>
      </a>
      <hr style="height:2px;border-width:0;color:black;background-color:black">
      <form action="http://127.0.0.1:5757/receiver" method="post" target="post-receiver">
            <button class="download-button" name="download" type="submit" value="{customMap.get('download-url')}">
            <input type="hidden" name="identifier" value={customMap.get('identifier')}>
            <input type="hidden" name="rlmus" value={customMap.get('rlmus')}>
            <input type="hidden" name="path" value={customMap.get('path')}>
            Download
            </button>
            <button class="load-button" name="load" type="submit" value="{customMap.get('identifier')}">
            <input type="hidden" name="rlmus" value={customMap.get('rlmus')}>
            <input type="hidden" name="path" value={customMap.get('path')}>
            Load
            </button>
            <button class="delete-button" name="delete" type="submit" value="{customMap.get('identifier')}">
            Delete
            </button>
        </form> 
      </article>
      </div>
    """
    return templateGridItem
def getBasePage():
    return ["""
    <link href="https://fonts.googleapis.com/css?family=Lexend" rel='stylesheet'>
    <link rel= "stylesheet" type= "text/css" href= "static/styles/style.css">
    <body>
    <div class="topnav">
    <h1 class="active">Redd's scuffed map loader</h1>
    </div>
    <div class="grid">
    
    ""","""
   
   
   
    <iframe class="post-receiver" name="post-receiver" width="0" height="0" style="display: none;">
    
    </iframe>
    </div>
    </body>"""]
def scrapePage(depth_limit=None):
    modifiableUrl = "https://lethamyr.com"
    base_url = "https://lethamyr.com/mymaps"
    new_page = base_url
    maps = []
    count = 0
    while True:
        if count == depth_limit:
            break
        page = requests.get(new_page)
        print(page)
        while page.status_code != 200:
                page = requests.get(new_page)
                print("encountered timeout!")
                time.sleep(2)
        soup = BeautifulSoup(page.text, "html.parser")
        older_button = soup.find("div", class_="older")
        pageMaps = soup.find_all("article", class_="blog-basic-grid--container entry blog-item")
        for rlmap in pageMaps:        
            string = rlmap.find('a', class_="image-wrapper").get('href')
            DownloadPage = requests.get(modifiableUrl + string)
            print(DownloadPage)
            while DownloadPage.status_code != 200:
                DownloadPage = requests.get(modifiableUrl + string)
                print("encountered timeout!")
                time.sleep(2)
            soupp = BeautifulSoup(DownloadPage.text, "html.parser")
            try:
                downloadLink = soupp.find('a', class_="sqs-block-button-element--large sqs-button-element--secondary sqs-block-button-element").get('href')
            except:
                downloadLink = soupp.find('a',class_='sqs-block-button-element--medium sqs-button-element--primary sqs-block-button-element').get('href')
            downloadLink = downloadLink.split('/')
            reformattedLink = f"https://drive.google.com/u/0/uc?id={downloadLink[5]}&export=download"
            activeMap = {
                "name": rlmap.find('h1', class_='blog-title').find('a').text.strip(),
                "author": "Lethamyr",
                "identifier": string.replace("/mymaps/",""),
                "path": string.replace("/mymaps/",""),
                "desc": rlmap.find('div', class_='blog-excerpt').find('p').text,
                "img": rlmap.find('div').find('img', class_='image').get('data-src'),
                "download-url": reformattedLink,
                "rlmus": False,
            }
            maps.append(activeMap)
            time.sleep(1/5)
        if older_button == None:
            print("could not find an older button, breaking out of loop.")
            break
        try:
            href = older_button.find("a").get('href')
        except AttributeError:
            print("found no button, breaking!")
            break
        except:
            print("unknown error occured")
            break
        new_page = f"{modifiableUrl}{href}"
        time.sleep(1.5)
        count +=1
    return maps
try:
    os.mkdir("maps")
    os.mkdir("temp")
    os.mkdir("backup")
except:
    pass
app = Flask(__name__, static_folder=Path.cwd().__str__() + fr"\static")
epicGames = False
steam = False
fileDirectory = Path.cwd()
print("searching for rocket league...")
if os.path.exists(r"C:\Program Files\Epic Games\rocketleague\Binaries\Win64\RocketLeague.exe"):
    print("Found Epic Games Rocket League")
    epicGames = True
if os.path.exists(r"C:\Program Files (x86)\Steam\steamapps\common\rocketleague\Binaries\Win64\RocketLeague.exe"):
    print("Found Steam Rocket League")
    steam = True
if steam and epicGames:
    print("Found both Steam and Epic Games Rocket League installations, which one would you like to load maps to?\n")
    while True:
        gameVersion = input("").casefold()
        if gameVersion in ("steam".casefold(), "epic games".casefold(), "epicgames".casefold()):
            if gameVersion == "steam":
                gameVersion = "steam"
            elif gameVersion in ("epic games".casefold(), "epicgames".casefold()):
                gameVersion = "epicgames"
elif steam:
    gameVersion = "steam"
    gamePath = r"C:\Program Files (x86)\Steam\steamapps\common\rocketleague\Binaries\Win64\RocketLeague.exe"
    mapPath = r"C:\Program Files (x86)\Steam\steamapps\common\rocketleague\TAGame\CookedPCConsole\Labs_Underpass_P.upk"
elif epicGames:
    gameVersion = "epicgames"
    gamePath = r"C:\Program Files\Epic Games\rocketleague\Binaries\Win64\RocketLeague.exe"
    mapPath = r"C:\Program Files\Epic Games\rocketleague\TAGame\CookedPCConsole\Labs_Underpass_P.upk"
else:
    print("Found no installation,")
    customPath = input(r"Please specify the base directory to rocket league, e.g 'C:\Program Files\Epic Games\rocketleague\' or 'C:\Program Files (x86)\Steam\steamapps\common\rocketleague\'")
    if os.path.exists(fr"{customPath}\Binaries\Win64\RocketLeague.exe") and os.path.exists(fr"{customPath}\TAGame\CookedPCConsole\Labs_Underpass_P.upk"):
        print("That's a valid Rocket League path, thank you!")
    else:
        while True:
            print("That wasn't a valid path! Try again, make sure to follow the format listed above.")
            customPath = input(r"Please specify the base directory to rocket league, e.g 'C:\Program Files\Epic Games\rocketleague\' or 'C:\Program Files (x86)\Steam\steamapps\common\rocketleague\'" + " If you opened this by mistake, type \"stop\" to exit")
            if customPath.casefold() == "stop".casefold():
                print("exiting...")
                exit()
            if os.path.exists(fr"{customPath}\Binaries\Win64\RocketLeague.exe") and os.path.exists(fr"{customPath}\TAGame\CookedPCConsole\Labs_Underpass_P.upk"):
                print("That's a valid Rocket League path, thank you!")
                break
    gamePath = customPath + r"Binaries\Win64\RocketLeague.exe"
    mapPath = customPath + r"TAGame\CookedPCConsole\Labs_Underpass_P.upk"
print(f"Chosen game version is {'Steam' if steam else 'Epic Games'}")
print(f"Rocket League path is: {gamePath}")
print(mapPath)
print(Path.cwd().__str__() + fr"\backup\Labs_Underpass_P.upk")
print(fr"{fileDirectory}\Labs_Underpass_P.upk")
if os.path.exists(Path.cwd().__str__() + fr"\backup\Labs_Underpass_P.upk") == False:
    shutil.copy(mapPath, fr"{fileDirectory}\backup\Labs_Underpass_P.upk")
    print("copying map")
print("acquiring maps.. please wait..")
if os.path.exists(fr"{Path.cwd().__str__()}/cached_maps.pkl"):
    cachedMapsAge = time.time() - os.path.getmtime(fr"{Path.cwd().__str__()}/cached_maps.pkl")
    if cachedMapsAge >= 1209600:
        print("cached maps are too old, manually re-scraping.")
        maps = scrapePage()
        rlmus = getRocketLeagueMapsUSMaps()
        combinedMaps = maps.extend(rlmus)
        with open("cached_maps.pkl", "wb") as handle:
            handle.write(pickle.dumps(combinedMaps))
    else:
        with open("cached_maps.pkl", "rb") as handle:
            maps = pickle.loads(handle.read())
else:
    print("no cached maps found, manually scraping.")
    maps = scrapePage()
    rlmus = getRocketLeagueMapsUSMaps()
    combinedMaps = maps.extend(rlmus)
    with open("cached_maps.pkl", "wb") as handle:
        handle.write(pickle.dumps(combinedMaps))
@app.route("/", methods=['GET'])
def startPage():
    formattedMaps = [format_map(customMap=customMap) for customMap in combinedMaps]
    half1 = getBasePage()[0]
    half2 = getBasePage()[1]
    fullPage = half1 + ''.join(formattedMaps) + half2
    return fullPage

@app.route("/receiver", methods=['POST'])
def getFormResponse():
    if request.method == "POST":
        if "load" in request.form.keys():
            if request.form.get('load') in os.listdir(Path.cwd().__str__() + "\\maps"):
                mapDirectory = os.listdir(Path.cwd().__str__() + '\\maps' + f"\\{request.form.get('load')}")
                upkFileAvailable = any([True if filename.endswith(".udk") or filename.endswith(".upk") else False for filename in mapDirectory])
                if upkFileAvailable:
                    file = next((ele for ele in mapDirectory if ele.endswith(".udk") or ele.endswith(".upk")), False)
                    print(file)
                shutil.copy(Path.cwd().__str__() + '\\maps' + f"\\{request.form.get('load')}\\{file}", mapPath)
        if "download" in request.form.keys():
            get_map(request.form.get('download'), request.form.get('identifier'), request.form.get('rlmus'), request.form.get('path'))
        if "delete" in request.form.keys():
            if request.form.get('delete') in os.listdir(Path.cwd().__str__() + "\\maps"):
                print("delete request processed.")
                shutil.rmtree(Path.cwd().__str__() + "\\maps" + f"\\{request.form.get('delete')}")
    return "true"

if __name__ == "__main__":
    FlaskUI(app=app, server="flask", port=5757).run()
    
