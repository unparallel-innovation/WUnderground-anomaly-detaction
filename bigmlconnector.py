from bigml.api import BigML
import json


def bigmlTopAnomalies(value,top,user,tokenkey):

    api = BigML(user,tokenkey)



    source = api.create_source(value, {'name': 'inline source'})
    api.ok(source)
    jsonSource = json.dumps(source)
    sourcej=json.loads(jsonSource)

    dataset = api.create_dataset(source)
    api.ok(dataset)

    anomaly = api.create_anomaly(dataset,{"top_n":top})
    api.ok(anomaly)
    response = json.dumps(anomaly)
    anomalies=json.loads(response)

    copyAnomalies=anomalies
    #clean
    api.delete_source(source)
    api.delete_dataset(dataset)
    api.delete_anomaly(anomaly)

    return copyAnomalies['object']['model']['top_anomalies']
