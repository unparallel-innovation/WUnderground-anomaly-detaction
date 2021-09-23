import json
import requests
from quickchart import QuickChart

def CreateChartBarData(value,legend):

    qc = QuickChart()
    qc.width = 500
    qc.height = 300

# Config can be set as a string or as a nested dict
    qc.config = """{
  "type": "bar",
  "data": {
    "labels":
      """ + str(legend) + """
    ,
    "datasets": [
      {
        "label": "Temperature per Station",
        "backgroundColor": "rgba(255, 99, 132, 0.5)",
        "borderColor": "rgb(255, 99, 132)",
        "borderWidth": 1,
        "data":
          """ + str(value) + """

      },

    ]
  },
  "options": {
    "responsive": true,
    "legend": {
      "position": "top"
    },
    "title": {
      "display": true,
      "text": "Chart Visualization"
    },
    "plugins": {
      "roundedBars": true
    }
  }
}"""

    qc.to_file('static/mychart.png')


def createChartTimePointData(value,title):


    qc = QuickChart()
    qc.width = 500
    qc.height = 300

    # Config can be set as a string or as a nested dict
    qc.config = """{
      "type": "line",
      "data": {
        "datasets": [
          {
            "label": """+ title + """,
            "backgroundColor": "rgba(255, 99, 132, 0.5)",
            "borderColor": "rgb(255, 99, 132)",
            "fill": false,
            "data": """+str(value)+"""
          }

        ]
      },
      "options": {
        "responsive": true,
        "title": {
          "display": true,
          "text": "Chart Visualization"
        },
        "scales": {
          "xAxes": [{
            "type": "time",
            "display": true,
            "scaleLabel": {
              "display": true,
              "labelString": "Date"
            },
            "ticks": {
              "major": {
                "enabled": true
              }
            }
          }],
          "yAxes": [{
            "display": true,
            "scaleLabel": {
              "display": true,
              "labelString": "value"
            }
          }]
        }
      }
    }"""

    print(qc.get_short_url())
    return qc.get_short_url()



def sendJsonToChannel(channel,json,writeKey):
    url = "https://api.thingspeak.com/channels/" + channel + "/bulk_update.json"

    payload = json.dumps({
      "write_api_key": writeKey,
      "updates": [
        {
          "created_at": "2021-09-06 10:00:00",
          "field1": 27.5
        },
        {
          "created_at": "2021-09-06 10:05:00",
          "field1": 28.5
        }
      ]
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
