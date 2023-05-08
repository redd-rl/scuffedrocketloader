from pathlib import Path
from flask import Flask, request, render_template
from flaskwebgui import FlaskUI
from page_scraper import scrapePage
from util import format_map, getBasePage, get_map
import os
import shutil
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
maps = scrapePage()
@app.route("/", methods=['GET'])
def startPage():
    formattedMaps = [format_map(customMap=customMap) for customMap in maps]
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
                upkFileAvailable = any([True if filename.endswith(".udk") else False for filename in mapDirectory])
                if upkFileAvailable:
                    file = next((ele for ele in mapDirectory if ele.endswith(".udk")), False)
                    print(file)
                shutil.copy(Path.cwd().__str__() + '\\maps' + f"\\{request.form.get('load')}\\{file}", mapPath)
        if "download" in request.form.keys():
            get_map(request.form.get('download'), request.form.get('identifier'))
        if "delete" in request.form.keys():
            if request.form.get('delete') in os.listdir(Path.cwd().__str__() + "\\maps"):
                print("delete request processed.")
                os.rmdir(Path.cwd().__str__() + "\\maps" + f"\\{request.form.get('delete')}")
    return "true"

if __name__ == "__main__":
    FlaskUI(app=app, server="flask", port=5757).run()
    
