In this repository we will be presenting how we can detect anomalies in a certain data source. We will presenting the anomalies in a form of a table and the data source in a graph.<br>
To select the data source we will choose a location in a map and then using the cordinates Weather Underground (WU) will gave values from the weather stations around, where this will provide an array with an object {"stationId" , "tempAvg"}. To interact with the map it was used the [mapbox](https://www.mapbox.com) library.<br>
Having the data source, then we can feed the [BigML](https://bigml.com) Platform in order to get the anomalies. The anomalies will be presented through a table.<br>
Using also the data source, it will be used the [QuickChart](https://quickchart.io) to create the chart.<br>
To present table and chart it will be used a webserver in python called [Flask](https://flask.palletsprojects.com/en/2.0.x/)<br>


## 🚀 Getting Started
The user will need to create an API from https://www.wunderground.com, https://bigml.com and https://www.mapbox.com.


There are two types of deployment. Standalone, to be run in a machine or Docker, to be running in a Docker-compose

### Global Prerequisites
Have an API from https://www.wunderground.com, https://bigml.com and https://www.mapbox.com.


# Standalone
### Usage
```
$ make setup
$ source .venv/bin/activate
$ python3 identifyAnomFromWU.py WUKEY USERBIGML PASSWORDBIGML MAPBOXTOKEN
```

# DOCKER
### Prerequisites
Build and deploy the image to an external Docker registry(DockerRegistryUrl_identifyAnomFromWU). Please update the file according to the desired Docker registry URL.
This image will do the same job of the identifyAnomFromWU script. 

```
$ chmod +x buildAndDeploy.sh
$ ./buildAndDeploy.sh
```


### USAGE
Use the following docker-compose to get this running
```
version: '3.1'

services:
  detectAnomalies:
    image: docker-hub.unparallel-server-1.ddns.net/smartclide/demo3:0.2
    ports:
      - "4500:4500"
    environment: 
        - WUKEY=WUKEY
        - USERBIGML=USERBIGML
        - PASSBIGML=PASSWORDBIGML
        - MAPBOXTOKEN=MAPBOXTOKEN
```



Create a local image and run it

```
$ docker build -t NAME . --no-cache
$ docker run -p 4500:4500   NAME
```

# Endpoints available
After running it, in both deploy options you will have several endpoints available:
- http://EXTERNAL_IP:4500 -> will have the chart with the infromation provided by data source
- http://EXTERNAL_IP:4500/getwsinfo -> Contains a UI interface where user can insert the latitude and longitude and WU will gave temperatures information about the weather stations around the point.
- http://EXTERNAL_IP:4500/addingws -> Contains a UI where user can create a dummy temperature from a weather station which will be added to the initial data source.
- http://EXTERNAL_IP:4500/stats -> Contains a table representing the anomalies identified with the respective score.



## ✍️  Author
Unparallel Innovation
