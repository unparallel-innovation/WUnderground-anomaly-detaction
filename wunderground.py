import requests
import json
from datetime import datetime

#A maximum of 1500 calls per day
#A maximum of 30 calls per minute
#https://docs.google.com/document/d/1eKCnKXI9xnoMGRRzOL1xPCBihNV2rOet08qpE_gArAY/edit#heading=h.3dy6vkm

def getTempFromWUArray(apiKey,latitude,longitude):

    url = "https://api.weather.com/v3/location/near?geocode="+latitude +","+ longitude +"&product=pws&format=json&apiKey="+apiKey

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    wuResponse = json.loads(response.text)
    index= 0
    tempArray= []
    for status in wuResponse['location']['qcStatus']:
                url = "https://api.weather.com/v2/pws/observations/current?stationId="+ wuResponse['location']['stationId'][index]+ "&format=json&units=m&apiKey="+apiKey
                response = requests.request("GET", url, headers=headers, data=payload)
                if response.text:
                    wuResponseStation = json.loads(response.text)
                    if(wuResponseStation['observations'][0]['metric']['temp']!= None):
                        tempArray.append({ "temp": wuResponseStation['observations'][0]['metric']['temp'] , "stationId": wuResponse['location']['stationId'][index] })
                    index+=1

                    if index >=20:
                        break
                else:
                    index+=1


    index=0
    return tempArray

def getTempFromWUAvg(apiKey,latitude,longitude):

    url = "https://api.weather.com/v3/location/near?geocode="+latitude +","+ longitude +"&product=pws&format=json&apiKey="+apiKey

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    wuResponse = json.loads(response.text)
    index= 0
    sumTemp = 0.0
    countTemp = 0
    for status in wuResponse['location']['qcStatus']:
        if wuResponse['location']['qcStatus'].count(1)>3:
            if status == 1:
                url = "https://api.weather.com/v2/pws/observations/current?stationId="+ wuResponse['location']['stationId'][index]+ "&format=json&units=m&apiKey="+apiKey
                response = requests.request("GET", url, headers=headers, data=payload)
                if response.text:
                    wuResponseStation = json.loads(response.text)
                    if(wuResponseStation['observations'][0]['metric']['temp']== None):
                        sumTemp+=wuResponseStation['observations'][0]['metric']['temp']
                        countTemp+=1
                    index+=1

                    if index >=3:
                        break
                else:
                    index+=1
        else:
            url = "https://api.weather.com/v2/pws/observations/current?stationId="+ wuResponse['location']['stationId'][index]+ "&format=json&units=m&apiKey="+apiKey
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.text:
                wuResponseStation = json.loads(response.text)
                sumTemp+=wuResponseStation['observations'][0]['metric']['temp']
                index+=1
                countTemp+=1
                if index >=3:
                    break
            else:
                index+=1

    averaTemp = sumTemp/countTemp
    index=0
    countTemp=0
    sumTemp=0.0
    return averaTemp


def getHistory7DaysHourlyFromWU(key,apiKey):

    url = "https://api.weather.com/v2/pws/observations/hourly/7day?stationId=KMAHANOV10&format=json&units=m&apiKey="+apiKey

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    wuResponse = json.loads(response.text)
    metrics=[]
    for observations in wuResponse['observations']:
        metrics.append({"timestamp":datetime.fromtimestamp(observations["epoch"]).isoformat(),key : observations["metric"][key] })

    return metrics
