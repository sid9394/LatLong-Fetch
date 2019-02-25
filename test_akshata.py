import json
import urllib.request

def latlong_fetch_SolR(city_location):
    url = 'http://172.25.4.49:8983/solr/GEO_LOCATION/select?'
    data = urllib.parse.urlencode({
        'fl': 'lat_long',
        'indent': "on",
        'wt': 'json',
        #'fq': "{!geofilt}&sfield=lat_long&pt=0,0&d=0",
        'rows': 3000,  # 'rows':2147483647,
        'q':"cityName:"+city_location
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    d = response.read()

    encoding = response.info().get_content_charset('utf-8')
    JSON_object = json.loads(d.decode(encoding))
    jsonData = JSON_object['response']['docs']
    for idx, item in enumerate(jsonData):
        lat_long = item['lat_long']
        print(lat_long)

latlong_fetch_SolR("karnataka")