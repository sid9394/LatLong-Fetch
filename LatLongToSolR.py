# -*- coding: utf-8 -*-
'''

@author: Promod.George
@copyright: Self
@since: Fri Nov 09 2018
'''

import json
import pysolr
import time
import traceback
import pandas as pd
import urllib.request
from geopy.geocoders import Nominatim
import datetime


try:
    import SSGLog
    logger = SSGLog.setup_custom_logger('latLongLogger1')
    
    solrURL = pysolr.Solr('http://localhost:8983/solr/GEO_LOCATION', timeout=20)          
    logger.info("Initiated SolR Search URL...")
    start_time = time.time()                        
    geolocator = Nominatim(user_agent='myapplication')
    logger.info("Initiated geolocator...")
except Exception:
    print("Something is wrong in initializations! Check logs...")
    logger.exception("Something is wrong in initializations! Exiting...")
    traceback.print_exc()
    exit()
    
               
def indexLatLongIntoSolR(cityID, cityName, country):
    dataTFText = {}

    print(cityName)
    lat, long = geoLocation(cityName)
    print(lat, long)
        
    dataTFText['cityID'] = cityID
    dataTFText['cityName'] = cityName
    dataTFText['countryName'] = country
    dataTFText["timestamp"] = datetime.datetime.now()
    dataTFText['lat_long'] = str(lat)+","+str(long)
    
    solrURL.add([dataTFText])
    solrURL.commit()

    print("Commited::"+cityID)             
    solrURL.optimize()


def query00LatLongFromSolR():
    url = 'http://localhost:8983/solr/GEO_LOCATION/select?fq={!geofilt}&sfield=lat_long&pt=0,0&d=0&q=*'
    data = urllib.parse.urlencode({
        'fl': 'cityID,cityName,countryName',
        'indent': "on",
        'wt': 'json',
        #'fq': "{!geofilt}&sfield=lat_long&pt=0,0&d=0",
        'rows': 3000,  # 'rows':2147483647,
        #'q':"*:*"
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    d = response.read() 
    
    encoding = response.info().get_content_charset('utf-8')
    JSON_object = json.loads(d.decode(encoding))
    jsonData = JSON_object['response']['docs']
    for idx, item in enumerate(jsonData):   
        cityID = item['cityID']
        cityName = item['cityName']
        country = item['countryName']
        print(cityID, cityName, country)
        indexLatLongIntoSolR(str(cityID), str(cityName), str(country))

def queryforID(id_):
    url = 'http://localhost:8983/solr/GEO_LOCATION/select?fl=cityID,cityName&wt=json'
    data = urllib.parse.urlencode({
        'fl': 'cityID,cityName',
        'indent': "on",
        'wt': 'json',
        #'fq': "{!geofilt}&sfield=lat_long&pt=0,0&d=0",
        'rows': 3000,  # 'rows':2147483647,
        'q': "cityID:"+str(id_)
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    d = response.read()

    encoding = response.info().get_content_charset('utf-8')
    JSON_object = json.loads(d.decode(encoding))
    intValue = JSON_object['response']['numFound']
    print(intValue)

def geoLocation(location_):
    location_ = location_.lower()
    try:
        if location_ != "nan" and location_ != "":
            location = geolocator.geocode(location_)
            if location is not None:
                return location.latitude, location.longitude
            else:
                return "0", "0"
        else:
            return "0", "0"
    except Exception:
        logger.exception("Exception!")
        print("Exception, passing")
        traceback.print_exc()

        pass

    
if __name__ == '__main__':

    try:

        documents = pd.read_csv("Indian_state_LatLong.csv", encoding="ISO-8859-1", keep_default_na=True)

        array = documents.values

        # choose column
        x = array[0:, 0]
        y = array[0:, 1]
        z = array[0:, 2]
        if True:
            for cityID, country, cityName in zip(x, y, z):
                print(cityID, cityName, country)

                if cityName is "nan":

                    cityName = country

                # indexLatLongIntoSolR(str(cityID), str(cityName), str(country))

        # queryforID(5819)

        # indexLatLongIntoSolR(str("78754"), str("Mukalla"), str("Yemen"))

        query00LatLongFromSolR()
            
    except Exception:
        print("Something is wrong! Error logged to log file!")
        logger.exception("Something is wrong!")
        traceback.print_exc()
    finally:
        print("Done!")

    print("--- %s seconds in total ---" % (time.time() - start_time))
    pass