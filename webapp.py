from flask import Flask, url_for, render_template, flash, request
from markupsafe import Markup

import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/p1")
def render_page1():
    artPieces = get_art_pieces()
    return render_template('page1.html', art_options=artPieces)
@app.route("/showArt")
def render_showArt():
    artPieces = get_art_pieces()
    art = request.args.get("artTitle")
    artURL = get_art_url(art)
    return render_template('page1.html', art_options=artPieces, art_url=artURL)

@app.route("/p2")
def render_page2():
    return render_template('page2.html')

@app.route("/p3")
def render_page3():
    return render_template('page3.html')

def get_art_pieces():
    with open('tate.json') as tate_data:
        collection = json.load(tate_data)
    art_options=[]
    for pieces in collection:
        if pieces["data"]["title"] not in art_options:
            art_options.append(pieces["data"]["title"])
    options=""
    for x in art_options:
        options += Markup("<option value=\"" + x + "\">" + x + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options

def get_art_url(art):
    with open('tate.json') as tate_data:
        collection = json.load(tate_data)
    url = ""
    for pieces in collection:
        if pieces["data"]["title"] == art:
            url = pieces["data"]["url"]
    return url

if __name__=="__main__":
    app.run(debug=False)