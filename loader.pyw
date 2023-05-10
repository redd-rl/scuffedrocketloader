import os
from pathlib import Path
from flask import Flask, render_template, request, send_from_directory
from flaskwebgui import FlaskUI, close_application
app = Flask(__name__, static_folder=Path.cwd().__str__() + fr"\static")
import logging
import click
with open("log.txt", "w") as handle:
    handle.write("")
logging.basicConfig(filename=Path.cwd().__str__() + "log.txt",
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
@app.route("/", methods=['GET'])
def startPage():
    with open(Path.cwd().__str__() +'/load-template.html', 'r') as handle:
        return handle.read()
@app.route("/close", methods=["GET"])
def close_window():
    close_application()
if __name__ == "__main__":
    FlaskUI(app=app, browser_path="C:\Program Files\Google\Chrome\Application\chrome.exe", server="flask", port=3000).run()