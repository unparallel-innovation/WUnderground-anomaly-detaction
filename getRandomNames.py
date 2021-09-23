import requests
import json


def getRandomName():
    url = "http://names.drycodes.com/1?nameOptions=funnyWords"

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    nameResponse = json.loads(response.text)
    return nameResponse[0]
