import os
import shutil
from bs4 import BeautifulSoup
import requests
import zipfile
from pathlib import Path
def get_map(mapPageUrl: str, identifier: str):
    try:
        ppage = requests.get(mapPageUrl)
        with open("temp.txt", "wb") as handle:
            handle.write(ppage.content)
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
def format_map(customMap: dict):
    templateGridItem = f"""
    <div class="grid-container">
        <article class="grid-item">
        <a class="grid-item-image">
            <img src="{customMap.get('img')}">
            <h1>
            {customMap.get('name')}
            </h1>
            <p>
            {customMap.get('desc')}
            </p>
        </a>
        <hr style="height:2px;border-width:0;color:black;background-color:black">
        <form action="http://127.0.0.1:5757/receiver" method="post" target="post-receiver">
            <button class="download-button" name="download" type="submit" value="{customMap.get('download-url')}">
            <input type="hidden" name="identifier" value={customMap.get('identifier')}>
            Download
            </button>
            <button class="load-button" name="load" type="submit" value="{customMap.get('identifier')}">
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