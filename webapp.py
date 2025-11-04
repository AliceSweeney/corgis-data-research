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
    text1 = "The link can be found " + Markup("<a href=" + artData[0] + ">here</a>") + "."
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
    allDecades = get_decades()
    return render_template('page2.html', data=get_mediums_data(), other_mediums = otherMeds, decades = allDecades)
@app.route("/otherMedium")
def render_otherMedium():
    otherMeds = get_other_meds()
    allDecades = get_decades()
    med = request.args.get("other")
    numText = "There are " + str(get_num_pieces(med)) + " pieces made with " + med + " in the collection."
    return render_template('page2.html', data=get_mediums_data(), other_mediums = otherMeds, decades = allDecades, num_pieces=numText)
@app.route("/timeMedium")
def render_timeMedium():
    otherMeds = get_other_meds()
    allDecades = get_decades()
    dec = request.args.get("decade")
    print(dec)
    print(get_popular_medium(dec))
    popMedium = "The most common medium in " + dec + " was " + str(get_popular_medium(dec)) + "."
    return render_template('page2.html', data=get_mediums_data(), other_mediums = otherMeds, decades = allDecades, medium = popMedium)

@app.route("/p3")
def render_page3():
    return render_template('page3.html', data=get_gender_data(), maleData=get_male_data(), femaleData=get_female_data())

@app.route("/p4")
def render_page4():
    return render_template('page4.html', data1=get_creation_decade_data(), data2=get_acquisition_date_data())

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

def get_decades():
    with open('tate.json') as tate_data:
        collection = json.load(tate_data)
    decade_options=[]
    for pieces in collection:
        if pieces["metadata"]["creation decade"] not in decade_options:
            decade_options.append(pieces["metadata"]["creation decade"])
    sortedDecades = sorted(decade_options)
    options=""
    for x in sortedDecades:
        options += Markup("<option value=\"" + str(x) + "\">" + str(x) + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options

def get_popular_medium(dec):
    with open('tate.json') as tate_data:
        collection = json.load(tate_data)
    allMediums = []
    for pieces in collection:
        if pieces["metadata"]["creation decade"] == int(dec):
            allMediums.append(pieces["data"]["medium"])
    counts = {}
    highest = 0
    for med in allMediums:
        if med in counts:
            counts[med] = counts[med] + 1
        else:
            counts[med] = 1
        if counts[med] > highest:
            highest = counts[med]
            mostPopular = med
    return mostPopular #want to return a name of a medium

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
    genData = [{"y": male, "label": "Male"}, {"y": female, "label": "Female"}]
    return genData

def get_male_data(): #similar structure to get creation decade data
    with open('tate.json') as tate_data:
        collection = json.load(tate_data)
    decades = []
    for pieces in collection:
        if pieces["metadata"]["creation decade"] not in decades:
            decades.append(pieces["metadata"]["creation decade"])
    sorted_decades = sorted(decades)
    decadesAll=[]
    for pieces in collection:
        if pieces["artist"]["gender"] == "Male": #only counts how many times a male artist made a piece in a decade
            decadesAll.append(pieces["metadata"]["creation decade"])
    counts={}
    for dec in decadesAll:
        if dec in counts:
            counts[dec] = counts[dec] + 1
        else:
            counts[dec] = 1
    num = []
    for x in counts:
        num.append(counts[x]) #Gets the number of times a decade shows up and puts in a list
    decData = []
    for dec, n, in zip(sorted_decades, num): #Should take a data point from each list and put them together in a new list of dictionaries for data points
        decData.append({"label": dec, "y": n})
        if dec == 0:
            decData.remove({"label": dec, "y": n})
    return decData

def get_female_data():
    with open('tate.json') as tate_data:
        collection = json.load(tate_data)
    decades = []
    for pieces in collection:
        if pieces["metadata"]["creation decade"] not in decades:
            decades.append(pieces["metadata"]["creation decade"])
    sorted_decades = sorted(decades)
    decadesAll=[]
    for pieces in collection:
        if pieces["artist"]["gender"] == "Female": #only counts how many times a female artist made a piece in a decade
            decadesAll.append(pieces["metadata"]["creation decade"])
    counts={}
    for dec in decadesAll:
        if dec in counts:
            counts[dec] = counts[dec] + 1
        else:
            counts[dec] = 1
    num = []
    for x in counts:
        num.append(counts[x]) #Gets the number of times a decade shows up and puts in a list
    decData = []
    for dec, n, in zip(sorted_decades, num): #Should take a data point from each list and put them together in a new list of dictionaries for data points
        decData.append({"label": dec, "y": n})
        if dec == 0:
            decData.remove({"label": dec, "y": n})
    return decData

def get_creation_decade_data(): # similar format to get_mediums_data
    with open('tate.json') as tate_data:
        collection = json.load(tate_data)
    decades = []
    for pieces in collection:
        if pieces["metadata"]["creation decade"] not in decades:
            decades.append(pieces["metadata"]["creation decade"])
    sorted_decades = sorted(decades)
    decadesAll=[]
    for pieces in collection:
        decadesAll.append(pieces["metadata"]["creation decade"])
    counts={}
    for dec in decadesAll:
        if dec in counts:
            counts[dec] = counts[dec] + 1
        else:
            counts[dec] = 1
    num = []
    for x in counts:
        num.append(counts[x]) #Gets the number of times a medium shows up and puts in a list
    decData = []
    for dec, n, in zip(sorted_decades, num): #Should take a data point from each list and put them together in a new list of dictionaries for data points
        decData.append({"label": dec, "y": n})
        if dec == 0:
            decData.remove({"label": dec, "y": n})
    return decData

def get_acquisition_date_data(): # similar format to get_mediums_data
    with open('tate.json') as tate_data:
        collection = json.load(tate_data)
    years = []
    for pieces in collection:
        if pieces["metadata"]["acquisition date"] not in years:
            years.append(pieces["metadata"]["acquisition date"])
    sorted_years = sorted(years)
    yearsAll=[]
    for pieces in collection:
        yearsAll.append(pieces["metadata"]["acquisition date"])
    counts={}
    for year in yearsAll:
        if year in counts:
            counts[year] = counts[year] + 1
        else:
            counts[year] = 1
    num = []
    for x in counts:
        num.append(counts[x]) #Gets the number of times a medium shows up and puts in a list
    yearData = []
    for year, n, in zip(sorted_years, num): #Should take a data point from each list and put them together in a new list of dictionaries for data points
        yearData.append({"label": year, "y": n})
    return yearData

if __name__=="__main__":
    app.run(debug=False)