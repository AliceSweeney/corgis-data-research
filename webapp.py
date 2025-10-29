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
    artData = get_art_data(art)
    text1 = "The link can be found " + Markup("<a href=" + artData[0] + ">link</a>") + "."
    text2 = "The artist is " + artData[1] + "."
    text3 = "It was made with " + artData[2] + "."
    if artData[3] == 0:
        text4 = "The creation year is unknown"
    else:
        text4 = "It was created in " + str(artData[3]) + "."
    if artData[4] == 0:
        text5 = "The acquisition year is unknown"
    else:
        text5 = "It was acquired in " + str(artData[4]) + "."
    return render_template('page1.html', art_options=artPieces, art_url=text1, art_artist=text2, art_medium=text3, art_date_made=text4, art_date_collected=text5)

@app.route("/p2")
def render_page2():
    otherMeds = get_other_meds()
    return render_template('page2.html', data=get_mediums_data(), other_mediums = otherMeds)
@app.route("/otherMedium")
def render_otherMedium():
    otherMeds = get_other_meds()
    med = request.args.get("other")
    numText = "There are " + str(get_num_pieces(med)) + " pieces made with " + med + " in the collection."
    return render_template('page2.html', data=get_mediums_data(), other_mediums = otherMeds, num_pieces=numText)

@app.route("/p3")
def render_page3():
    return render_template('page3.html', data=get_gender_data())

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

def get_art_data(art):
    with open('tate.json') as tate_data:
        collection = json.load(tate_data)
    data = []
    for pieces in collection:
        if pieces["data"]["title"] == art:
            data.append(pieces["data"]["url"])
            data.append(pieces["artist"]["name"])
            data.append(pieces["data"]["medium"])
            data.append(pieces["metadata"]["creation year"])
            data.append(pieces["metadata"]["acquisition date"])
    return data

def get_mediums_data():
    with open('tate.json') as tate_data:
        collection = json.load(tate_data)
    mediums=[]
    for pieces in collection:
        if pieces["data"]["medium"] not in mediums:
            mediums.append(pieces["data"]["medium"])#Gets all the different names of mediums and puts them in list
    mediumsAll=[]
    for pieces in collection:
        mediumsAll.append(pieces["data"]["medium"]) #Gets all the mediums but doesnt get rid of multiples to they can be counted
    counts={}
    for med in mediumsAll:
        if med in counts:
            counts[med] = counts[med] + 1
        else:
            counts[med] = 1
    num = []
    for x in counts:
        num.append(counts[x]) #Gets the number of times a medium shows up and puts in a list
    medData = []
    other = 0
    for med, n, in zip(mediums, num): #Should take a data point from each list and put them together in a new list of dictionaries for data points
        medData.append({"label": med, "y": n})
        if n <= 30:
            medData.remove({"label": med, "y": n})
            other = other + n
    medData.append({"label": "Other", "y": other})
    return medData

def get_other_meds():
    with open('tate.json') as tate_data:
        collection = json.load(tate_data)
    medium_options=[]
    for pieces in collection:
        if pieces["data"]["medium"] not in medium_options:
            medium_options.append(pieces["data"]["medium"])#gets medium options without duplicates
            mediumsAll=[]
            for pieces in collection:
                mediumsAll.append(pieces["data"]["medium"])#gets medium options with duplicates
            num = 0
            for med in mediumsAll:
                if med == pieces["data"]["medium"]:
                    num = num + 1
                    if num >= 30:
                        medium_options.remove(pieces["data"]["medium"])
    options=""
    for x in medium_options:
        options += Markup("<option value=\"" + x + "\">" + x + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options

def get_num_pieces(med):
    with open('tate.json') as tate_data:
        collection = json.load(tate_data)
    num = 0
    for pieces in collection:
        if pieces["data"]["medium"] == med:
            num = num + 1
    return num

def get_gender_data():
    with open('tate.json') as tate_data:
        collection = json.load(tate_data)
    female = 0
    male = 0
    for pieces in collection:
        if pieces["artist"]["gender"] == "Female":
            female = female + 1
        elif pieces["artist"]["gender"] == "Male":
            male = male + 1
    total = female + male
    female = female/total*100
    male = male/total*100
    genData = [{"y": female, "label": "Female"}, {"y": male, "label": "Male"}]
    return genData

if __name__=="__main__":
    app.run(debug=False)