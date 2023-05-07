from flask import Flask
from flaskwebgui import FlaskUI
from flask import render_template
from page_scraper import scrapePage
from util import format_map, getBasePage
app = Flask(__name__)
print("acquiring maps.. please wait..")
maps = scrapePage()

@app.route("/")
def startPage():
    formattedMaps = [format_map(customMap=customMap) for customMap in maps]
    half1 = getBasePage()[0]
    half2 = getBasePage()[1]
    fullPage = half1 + ''.join(formattedMaps) + half2
    return fullPage

if __name__ == "__main__":
    FlaskUI(app=app, server="flask").run()
    
