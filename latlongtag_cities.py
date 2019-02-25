from geopy.geocoders import Nominatim
import pandas as pd
import csv

def geoLocation(location_):
    geolocator = Nominatim(user_agent='myapplication')
    location = geolocator.geocode(location_, timeout=10)
    Lat = location.latitude
    Long = location.longitude
    return Lat, Long

# open csv file
documents = pd.read_csv("City_LatLong.csv", encoding= "ISO-8859-1", keep_default_na=False)

array = documents.values

# choose column
z = array[0:, 2]

city = "Maharashtra"
LatLong = geoLocation(city)
print(LatLong)


# for city in z:
#
#         try:
#             if city:
#
#
#                 print(city)
#                 LatLong = geoLocation(city)
#                 print(LatLong)
#
#             else:
#                 LatLong = str(None)
#                 print(LatLong)
#         except:
#             print("Location details not found for ", city)
#             LatLong = "NA"


