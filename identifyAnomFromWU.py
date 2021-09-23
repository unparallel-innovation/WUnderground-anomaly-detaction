import json
import time
import sys
from datetime import datetime,timedelta
import requests
import wunderground
import visualizationconnector
import bigmlconnector
from flask import Flask, render_template, request, jsonify
import os
from pathlib import Path
import getRandomNames


PEOPLE_FOLDER = os.path.join('static')

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

temp = []
anomalies = []


def transformWUtoChartLine(value):
    newArray = []
    for val in value:
        val['x']= val['timestamp']
        del val['timestamp']
        val['y']= val['tempAvg']
        del val['tempAvg']
        newArray.append(val)
    return newArray

def transformWUtoChartBar(value):
    newArrayValue = []
    newArrayLegend = []
    for val in value:
        newArrayValue.append(val['temp'])
        newArrayLegend.append(val['stationId'])
    return {"value":newArrayValue,"legend":newArrayLegend}




def findAnomaliesAndCreateChart():
    global temp
    if(len(sys.argv)>1):
        anomalies = bigmlconnector.bigmlTopAnomalies(temp,len(temp),sys.argv[2],sys.argv[3])
    else:
        anomalies = bigmlconnector.bigmlTopAnomalies(temp,len(temp),os.getenv('USERBIGML'),os.getenv('PASSBIGML'))

    Path("static").mkdir(parents=True, exist_ok=True)
    path = Path(f"static/anomalies.json")
    with open(path, 'w') as outfile:
        json.dump(anomalies, outfile)
    outfile.close()
    visualizationconnector.CreateChartBarData(transformWUtoChartBar(temp)['value'],transformWUtoChartBar(temp)['legend'])


def getWSInfoByGPSFunction(apiKey,latidude,longitude):
    global temp
    temp = wunderground.getTempFromWUArray(apiKey,latidude,longitude)
    findAnomaliesAndCreateChart()


@app.route('/getwsinfo',methods=["GET"])
def getWSInfoByGPS():
    app.route('/getwsinfo')
    if(len(sys.argv)>1):
        return render_template("getwsinfo.html", mapboxkey=str(sys.argv[4]))
    else:
        return render_template("getwsinfo.html", mapboxkey=str(os.getenv('MAPBOXTOKEN')))


@app.route('/addingws',methods=["GET","POST"])
def addingWSvalue():
    app.route('/addingws')
    return render_template("createWS.html")


@app.route('/')
def home():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'mychart.png')
    full_filename_no_result = os.path.join(app.config['UPLOAD_FOLDER'], 'no_results_loading.png')

    app.route('/')
    if os.path.isfile(full_filename):
        return render_template("home.html", user_image = full_filename)
    else:
        return render_template("home.html", user_image = full_filename_no_result)

@app.route('/stats')
def stats():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'anomalies.json')
    full_filename_no_result = os.path.join(app.config['UPLOAD_FOLDER'], 'no_statics_loading.png')
    app.route('/stats')
    if os.path.isfile(full_filename):
        file_predi = open(full_filename,'r')
        jsonObj= json.load(file_predi)

        Statsjson =[]
        for obj in jsonObj:
            Statsjson.append({"Station Name" : obj['row'][0], "Value" : obj['row'][1], "Score": obj['score'] } )

        columnNames = ["Station Name","Value", "Score"]
        if len(Statsjson) > 0:
            return render_template('stats.html', records=Statsjson, colnames=columnNames)
        else:
            return render_template("statsnofile.html", user_image = full_filename_no_result)
    else:
        return render_template("statsnofile.html", user_image = full_filename_no_result)


@app.route('/getwuandcreatechart',methods=["GET","POST"])
def getwuandcreatechart():
    try:
        if(len(sys.argv)>1):
            getWSInfoByGPSFunction(sys.argv[1],request.args.get("lati"),request.args.get("long"))
        else:
            getWSInfoByGPSFunction(os.getenv('WUKEY'),request.form['latitude'],request.form['longitude'])

        return jsonify({"result":"The WS value was succefully added"})
    except Exception as e:
        print(e)
        return jsonify({"result":"Error in creating chart."})


@app.route('/createws',methods=["GET","POST"])
def createws():
    global temp
    try:

        temp.append({'stationId':getRandomNames.getRandomName(),'temp':request.args.get("temp")})
        findAnomaliesAndCreateChart()
        return jsonify({"result":"The dummy information was succefully created"})
    except Exception as e:
        print(e)
        return jsonify({"result":"Some problem as occurred during the process"})



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=4500)
