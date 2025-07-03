import json
from pathlib import Path
import re
import subprocess
from tkinter import messagebox
from typing import Union
from flask import Flask, request, send_from_directory
from flaskwebgui import FlaskUI
import os
from tkinter.filedialog import askdirectory
from tkinter.simpledialog import askstring
from askdialog import select_platform_dialog
if os.getlogin() == "redd":
    DEBUG = True
else:
    DEBUG = False

if not DEBUG:
    os.chdir("app")
import requests
from bs4 import BeautifulSoup
import zipfile
import time
import shutil
import logging
import click
with open("log.txt", "w") as handle:
    handle.write("")

logging.basicConfig(# filename=Path.cwd().__str__() + "log.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt="%H:%M:%S",
                    level=logging.INFO
                    )
log = logging.getLogger('werkzeug')

def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass

def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = echo
click.secho = secho
try:
    with open("manifest.json", "r") as handle:
        manifest = handle.read()
        webManifest = requests.get("https://raw.githubusercontent.com/redd-rl/scuffedrocketloader/master/manifest.json")
        manifestJson = json.loads(manifest)
        webManifestJson = json.loads(webManifest.text)
        if manifestJson['versionNumber'] != webManifestJson['versionNumber']:
            update = messagebox.askyesno(
                title="Outdated loader version detected.", 
                message="Hi! We detected an outdated version of your Map Loader, would you like to download and run the installer for the latest version? Don't worry, it'll be the same as last time.\nJust with more features!")
            if update == True:
                content = requests.get("https://github.com/redd-rl/scuffedrocketloader/releases/latest/download/ScuffedMapLoader.exe")
                os.remove(Path.cwd().parent().__str__())
                with open(Path.cwd().__str__() + "/ScuffedMapLoader.exe", "wb") as handle:
                    handle.write(content.content)
                os.system(f'"{Path.cwd().__str__()}' + r'\ScuffedMapLoader.exe"')
                exit()
            else:
                pass
except:
    pass
def getRocketLeagueMapsUSMaps():
    empty = False
    count=1
    mapInfo = []
    while not empty:
        try:
            maps = requests.get(f"https://celab.jetfox.ovh/api/v4/projects/?page={count}")
            log.info(f"requesting https://celab.jetfox.ovh/api/v4/projects/?page={count}")
            count += 1
            #print(count)
            mapsJson = json.loads(maps.text)
            #print(mapsJson if len(str(mapsJson)) >= 50 else None)
            #print(mapsJson == [])
            if mapsJson == []:
                empty=True
                return mapInfo
            for customMap in mapsJson:
                customMap: dict
                identifier = customMap.get('id', None)
                name = customMap.get('name', 'Unidentifiable')
                desc = customMap.get('description', 'Could not get description.')
                path = customMap.get('path', 'Unidentifiable')
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
                        "source": "https://rocketleaguemaps.us/",
                        "source-plaintext": "rocketleaguemaps.us",
                        "download-url": downloadUrl,
                        "rlmus": True,
                    }
                mapInfo.append(activeMap)
        except:
            pass
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
            zip_ref.extractall(extractPath + path)
            destinationPath = Path.cwd().__str__() + f"\\maps\\"
            shutil.move(extractPath + path, destinationPath + path)

def cleanHTML(html):
    CLEANR = re.compile('<.*?>') 
    try:
        cleantext = re.sub(CLEANR, '', html)
    except:
        cleantext = html
        pass
    return cleantext
def format_map(customMap: dict):
    return f"""<div id="{customMap.get('path')}" class="grid-container">
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
        {cleanHTML(customMap.get('desc'))}
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
    <a href="{customMap.get('source')}" target="_blank" style="position: relative;color: fff;font-family: 'Lexend';text-decoration: None;text-align: left;margin-right: 75%;margin-bottom: 10%;">{customMap.get('source-plaintext')}</a>
      </article>
      </div>"""
def getBasePage():
    return ["""
    <link href="https://fonts.googleapis.com/css?family=Lexend" rel='stylesheet'>
    <link rel= "stylesheet" type= "text/css" href= "static/styles/style.css">
    <link rel="icon" href="static/favicon.ico">
    <script type="text/javascript" src="static/js/search.js"></script>
    <script type="text/javascript" src="static/js/settings_handler.js"></script>
    <body onload="closeSettingsDialog();">
            <div id="overlay" class="overlay">
        <div class="dialog-box">
            <h1 class="settingsTitle" style="
                float: none;
            ">Settings</h1>
            <!-- Settings form -->
            <form action="http://127.0.0.1:5757/receive_settings" method="post" enctype="multipart/form-data" target="post-receiver" style="
                font-family:  'Lexend';
                color: white;">
                <label for="platformSelect">Platform:</label>
                    <select id="platformSelect" name="platform" style="
                    font-family: 'Lexend';">
                    <option value="epicgames">Epic Games</option></select>
                    <option value="steam">Steam</option>
                    <br>
                    <br>
                    <label for="fileInput">Browse to RocketLeague.exe File:</label>
                    <br>
                    <h2 style="
                        font-size: 16px;
                    ">Will ask for filepath when submit button is pressed.</h2>
                    <br>
                    <h2 style="
                        font-size: 16px;
                    ">If no windows pop up, check your desktop or start minimizing windows. It will appear.</h2>
                            <br><br>
                            <!-- Submit button to post the form data -->
                            <button type="submit" class="download-button" style="
                                float: right;" onclick="closeSettingsDialog()">Submit</button>
                            <button class="restore-button btn" onclick="closeSettingsDialog()" style="
                                float: left;">Cancel</button>
                        </form>                       
            <!-- Button to close the dialog -->
        </div>
    </div>
    <div class="topnav">
    <form action="http://127.0.0.1:5757/receiver" method="post" target="post-receiver">
            <button class="restore-button" name="restore" type="submit" value="restore"> Restore Underpass
            </button>
            </form>
    <button class="download-button btn" onclick="openSettingsDialog()" style="
        margin-left: 220px;
    ">Open Settings</button>
<form target="post-receiver">
<p class="downloadtext">Display downloaded maps</p>
<input type="checkbox" onclick="displayDownloaded()" id="downloaded" class="downloadbox">
            </form>
    <h1 class="active">Redd's scuffed map loader</h1>
    <tr>
        <div class="search-container">
        
        <input type="text" class="search-bar" id="Search" onkeydown="key_down()" placeholder="Please enter a search term.." title="Type in a map name"> 
        <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="search-icon">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
    </svg>
    </div>
    </tr>
    </div>
    <div class="grid">
    
    ""","""
   
   
   
    <iframe class="post-receiver" name="post-receiver" width="0" height="0" style="display: none;">
    
    </iframe>
    </div>
    </body>"""]
def getLethamyrMaps(depth_limit=None):
    try:
        maps = requests.get("https://lethamyr.com/api/v1/maps")
        nextPage = 0
        mapTotal = []
        while nextPage is not None:
            mapsJson = json.loads(maps.text)
            for customMap in mapsJson['data']:
                name = customMap.get('name', None)
                identifier = name.lower().replace(" ", "")
                author = "Lethamyr"
                downloadUrl = customMap.get("download_url", None)
                description = customMap.get("description", "Blank description.")
                active = {
                    "name": name,
                    "author": author,
                    "identifier": identifier,
                    "path": identifier,
                    "desc": description,
                    "img": "https://lethamyr.com/media/logo.png",
                    "download-url": downloadUrl,
                    "source": "https://lethamyr.com/",
                    "source-plaintext": "Lethamyr.com",
                    "rlmus": False,
                }
                mapTotal.append(active)
            nextPage = mapsJson["links"]["next"]
            if nextPage is not None:
                log.info(f"requesting {nextPage}")
                maps = requests.get(nextPage)
    except Exception as e:
        log.error(f"Error in getLethamyrMaps: {e}")
        pass
    mapTotal.reverse()
    return mapTotal
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
if os.path.exists(Path.cwd() / "config.json"):
    with open(Path.cwd() / "config.json", "r") as handle:
        configuration = json.loads(handle.read())
        mapPath = configuration['mapPath']
        gamePath = configuration['gamePath']
        gameVersion = configuration['gameVersion']
        steam = True if gameVersion == "steam" else False
        epicGames = True if gameVersion == "epicgames" else False
else:
    #print("searching for rocket league...")
    if os.path.exists(r"C:\Program Files\Epic Games\rocketleague\Binaries\Win64\RocketLeague.exe"):
        #print("Found Epic Games Rocket League")
        epicGames = True
    if os.path.exists(r"C:\Program Files (x86)\Steam\steamapps\common\rocketleague\Binaries\Win64\RocketLeague.exe"):
        #print("Found Steam Rocket League")
        steam = True
    if steam and epicGames:
        #print("Found both Steam and Epic Games Rocket League installations, which one would you like to load maps to?\n")
        while True:
            gameVersion = select_platform_dialog()
            if gameVersion == "Steam":
                gameVersion = "steam"
                gamePath = r"C:\Program Files (x86)\Steam\steamapps\common\rocketleague\Binaries\Win64\RocketLeague.exe"
                mapPath = r"C:\Program Files (x86)\Steam\steamapps\common\rocketleague\TAGame\CookedPCConsole\Labs_Underpass_P.upk"
                break
            elif gameVersion == "Epic Games":
                gameVersion = "epicgames"
                gamePath = r"C:\Program Files\Epic Games\rocketleague\Binaries\Win64\RocketLeague.exe"
                mapPath = r"C:\Program Files\Epic Games\rocketleague\TAGame\CookedPCConsole\Labs_Underpass_P.upk"
                break
    elif steam:
        gameVersion = "steam"
        gamePath = r"C:\Program Files (x86)\Steam\steamapps\common\rocketleague\Binaries\Win64\RocketLeague.exe"
        mapPath = r"C:\Program Files (x86)\Steam\steamapps\common\rocketleague\TAGame\CookedPCConsole\Labs_Underpass_P.upk"
    elif epicGames:
        gameVersion = "epicgames"
        gamePath = r"C:\Program Files\Epic Games\rocketleague\Binaries\Win64\RocketLeague.exe"
        mapPath = r"C:\Program Files\Epic Games\rocketleague\TAGame\CookedPCConsole\Labs_Underpass_P.upk"
    else:
        #print("Found no installation,")
        customPath = askdirectory(initialdir="C:\\", mustexist=True, title=r"Please specify the base directory to rocket league, e.g 'C:\Program Files\Epic Games\rocketleague\' or 'C:\Program Files (x86)\Steam\steamapps\common\rocketleague\'")
        if os.path.exists(fr"{customPath}\Binaries\Win64\RocketLeague.exe") and os.path.exists(fr"{customPath}\TAGame\CookedPCConsole\Labs_Underpass_P.upk"):
            #print("That's a valid Rocket League path, thank you!")
            pass
        else:
            while True:
                #print("That wasn't a valid path! Try again, make sure to follow the format listed above.")
                customPath = askdirectory(initialdir="C:\\", mustexist=True, title=r"Please specify the base directory to rocket league, e.g 'C:\Program Files\Epic Games\rocketleague\' or 'C:\Program Files (x86)\Steam\steamapps\common\rocketleague\', if you opened this by mistake, type 'stop' to exit.")
                if customPath.casefold() == "stop".casefold():
                    #print("exiting...")
                    exit()
                if os.path.exists(fr"{customPath}\Binaries\Win64\RocketLeague.exe") and os.path.exists(fr"{customPath}\TAGame\CookedPCConsole\Labs_Underpass_P.upk"):
                    #print("That's a valid Rocket League path, thank you!")
                    break
        gamePath = customPath + r"Binaries\Win64\RocketLeague.exe"
        mapPath = customPath + r"TAGame\CookedPCConsole\Labs_Underpass_P.upk"
with open(Path.cwd() / "config.json", "w") as handle:
    handle.write(json.dumps(
        {"gamePath": gamePath,
         "mapPath": mapPath,
         "gameVersion": gameVersion}
    ))
#print(f"Chosen game version is {'Steam' if steam else 'Epic Games'}")
#print(f"Rocket League path is: {gamePath}")
#print(mapPath)
#print(Path.cwd().__str__() + fr"\backup\Labs_Underpass_P.upk")
#print(fr"{fileDirectory}\Labs_Underpass_P.upk")
if os.path.exists(Path.cwd().__str__() + fr"\backup\Labs_Underpass_P.upk") == False:
    shutil.copy(mapPath, fr"{fileDirectory}\backup\Labs_Underpass_P.upk")
    #print("copying map")
#print("acquiring maps.. please wait..")
#print("attempting to close loader")
rlmus = []
if os.path.exists(fr"{Path.cwd().__str__()}/cached_maps.json"):
    cachedMapsAge = time.time() - os.path.getmtime(fr"{Path.cwd().__str__()}/cached_maps.json")
    if cachedMapsAge >= 1209600:
        #print("cached maps are too old, manually re-scraping.")
        if DEBUG:
            subprocess.Popen([f"./venv/Scripts/pythonw.exe", f"{Path.cwd().__str__()}/loader.pyw"])
        else:
            subprocess.Popen([f"{Path.cwd().parent.__str__()}/Python310/pythonw.exe", f"{Path.cwd().__str__()}/loader.pyw"])
        maps = getLethamyrMaps()
        rlmus = getRocketLeagueMapsUSMaps()
        combinedMaps = maps + rlmus
        with open("cached_maps.json", "w") as handle:
            handle.write(json.dumps(combinedMaps))
    else:
        #print("found existing maps cache")
        with open("cached_maps.json", "r") as handle:
            maps = json.loads(handle.read())
            combinedMaps = maps
else:
    #print("no cached maps found, manually scraping.")
    if DEBUG:
        subprocess.Popen([f"./venv/Scripts/pythonw.exe", f"{Path.cwd().__str__()}/loader.pyw"])
    else:
        subprocess.Popen([f"{Path.cwd().parent.__str__()}/Python310/pythonw.exe", f"{Path.cwd().__str__()}/loader.pyw"])
    maps = getLethamyrMaps()
    #print("acquiring jetfox maps")
    rlmus = getRocketLeagueMapsUSMaps()
    combinedMaps = maps + rlmus
    with open("cached_maps.json", "w") as handle:
        handle.write(json.dumps(combinedMaps))
def getFeedback(type):
    if type == "download":
        return """
        <script>
        var div = parent.document.createElement('div'); 
        div.id = 'overlay';
        div.innerHTML = `
        <div id="alertbox">
        <h1>
        Downloaded map
        </h1>
        <button type="submit" onclick="removeOverlay()">
        Ok
        </button>
        </div>
        `  
        parent.document.body.appendChild(div)</script>"""
    elif type == "load":
        return """
        <script>
        var div = parent.document.createElement('div'); 
        div.id = 'overlay';
        div.innerHTML = `
        <div id="alertbox">
        <h1>
        Loaded map
        </h1>
        <button type="submit" onclick="removeOverlay()">
        Ok
        </button>
        </div>
        `  
        parent.document.body.appendChild(div)</script>"""
    elif type == "delete":
        return """
        <script>
        var div = parent.document.createElement('div'); 
        div.id = 'overlay';
        div.innerHTML = `
        <div id="alertbox">
        <h1>
        Deleted map
        </h1>
        <button type="submit" onclick="removeOverlay()">
        Ok
        </button>
        </div>
        `  
        parent.document.body.appendChild(div)</script>"""
    elif type == "restore":
        return """
        <script>
        var div = parent.document.createElement('div'); 
        div.id = 'overlay';
        div.innerHTML = `
        <div id="alertbox">
        <h1>
        Restored Underpass
        </h1>
        <button type="submit" onclick="removeOverlay()">
        Ok
        </button>
        </div>
        `  
        parent.document.body.appendChild(div)</script>"""
    elif type == "opensettings":
        return """
        <script>
        var div = parent.document.createElement('div'); 
        div.id = 'overlay';
        div.innerHTML = `
        <div id="alertbox">
        <h1>
        Restored Underpass
        </h1>
        <button type="submit" onclick="removeOverlay()">
        Ok
        </button>
        </div>
        `  
        parent.document.body.appendChild(div)</script>"""
    
@app.route("/", methods=['GET'])
def startPage():
    try:
        requests.get("http://127.0.0.1:3000/close")
    except:
        pass
    formattedMaps = [format_map(customMap=customMap) for customMap in combinedMaps]
    half1 = getBasePage()[0]
    half2 = getBasePage()[1]
    fullPage = half1 + ''.join(formattedMaps) + half2
    return fullPage

@app.route("/maplist", methods=['GET'])
def maplist():
    return os.listdir(Path.cwd().__str__() + '\\maps')

@app.route("/receive_settings", methods=['POST'])
def receive_settings():
    if request.method == "POST":
        customPath = askdirectory(initialdir="C:\\", mustexist=True, title=r"Please specify the base directory to rocket league, e.g 'C:\Program Files\Epic Games\rocketleague\' or 'C:\Program Files (x86)\Steam\steamapps\common\rocketleague\'")
        global gamePath
        gamePath = customPath + r"Binaries\Win64\RocketLeague.exe"
        global mapPath
        mapPath = customPath + r"TAGame\CookedPCConsole\Labs_Underpass_P.upk"
        if "platformSelect" in request.form.keys():
            global gameVersion
            gameVersion = request.form.get("platformSelect")
        with open(Path.cwd() / "config.json", "w") as handle:
            handle.write(json.dumps(
                {"gamePath": gamePath,
                "mapPath": mapPath,
                "gameVersion": gameVersion}
            ))

@app.route("/receiver", methods=['POST'])
def getFormResponse():
    if request.method == "POST":
        if "load" in request.form.keys():
            if request.form.get('load') in os.listdir(Path.cwd().__str__() + "\\maps") or request.form.get('path') in os.listdir(Path.cwd().__str__() + "\\maps"):
                rlmusS = True if request.form.get('rlmus').casefold() == "True".casefold() else False
                if rlmusS == True:
                    mapDirectory = os.listdir(Path.cwd().__str__() + '\\maps' + f"\\{request.form.get('path')}")
                    upkFileAvailable = any([True if filename.endswith(".udk") or filename.endswith(".upk") else False for filename in mapDirectory])
                    if upkFileAvailable:
                        file = next((ele for ele in mapDirectory if ele.endswith(".udk") or ele.endswith(".upk")), False)
                        #print(file)
                    shutil.copy(Path.cwd().__str__() + '\\maps' + f"\\{request.form.get('path')}\\{file}", mapPath)
                else:
                    mapDirectory = os.listdir(Path.cwd().__str__() + '\\maps' + f"\\{request.form.get('load')}")
                    upkFileAvailable = any([True if filename.endswith(".udk") or filename.endswith(".upk") else False for filename in mapDirectory])
                    if upkFileAvailable:
                        file = next((ele for ele in mapDirectory if ele.endswith(".udk") or ele.endswith(".upk")), False)
                        #print(file)
                    shutil.copy(Path.cwd().__str__() + '\\maps' + f"\\{request.form.get('load')}\\{file}", mapPath)
            return getFeedback("load")
        if "download" in request.form.keys():
            rlmusS = True if request.form.get('rlmus').casefold() == "True".casefold() else False
            get_map(request.form.get('download'), request.form.get('identifier'), rlmusS, request.form.get('path'))
            return getFeedback("download")
        if "delete" in request.form.keys():
            if request.form.get('delete') in os.listdir(Path.cwd().__str__() + "\\maps"):
                #print("delete request processed.")
                shutil.rmtree(Path.cwd().__str__() + "\\maps" + f"\\{request.form.get('delete')}")
            return getFeedback("delete")
        if "download" in request.form.keys():
            shutil.copy(Path.cwd().__str__() + '\\backup\\Labs_Underpass_P.upk', mapPath)
            return getFeedback("restore")
    return "true"
if __name__ == "__main__":
    try:
        FlaskUI(app=app, browser_path="C:\Program Files\Google\Chrome\Application\chrome.exe", server="flask", port=5757).run()
    except FileNotFoundError:
        FlaskUI(app=app, server="flask", port=5757).run()
    
