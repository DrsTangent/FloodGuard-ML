#TO DO: CREATE CSV WITH DATA OF (CITIES, PROVINCE, SQ AREA, Longitude, Latitude, Polygone)
import pandas as pd
import requests
import json

#Reading XLSX FILE, EXTRACTING CITY, PROVINCE AND AREA_SQKM #

df = pd.read_excel('pak_adminboundaries_tabulardata.xlsx', sheet_name=2)
sqAreas = df[["ADM2_EN","ADM1_EN","AREA_SQKM"]].to_numpy();

#Printing JSON
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

#Fetching Coordinates of Cities (Lat, Lng, Bounding Box)#
def getCityInformation(cityName):
    response = requests.get("https://nominatim.openstreetmap.org/search.php?q="+cityName+" district&polygon_geojson=1&format=json")
    if(len(response.json()) == 0):
        print(cityName + " Failed")
    return response.json()

def extractLocationInformation(response):
    info = {}
    for i in range(0, len(response)):
        instance = response[i]
        if(instance['addresstype'] in ['city', 'district', 'state_district','city_district','county'] and 'geojson' in instance and instance['geojson']['type'] == 'Polygon'):
            info['lat'] = instance['lat']
            info['lng'] = instance['lon']
            info['geometry'] = instance['geojson']
            return info
    return None

districts = [];

for i in range(0, len(sqAreas)):
    print(i+1)
    city = []
    cityName = sqAreas[i][0]
    provinceName = sqAreas[i][1]
    response = getCityInformation(cityName)
    info = extractLocationInformation(response)
    if(info != None):
        city.append(cityName)
        city.append(provinceName)
        city.append(info['lat'])
        city.append(info['lng'])
        city.append(info['geometry']['coordinates'])
        print(cityName + " Saving")
        districts.append(city)
    else:
        print(cityName + " failed due to unavailibty of Polygone");

pd.DataFrame(districts).to_csv('DistrictsLocationInfo.csv', index_label = "Index", header  = ['City Name','Province','Lat', 'Lng', 'Polygon'])   
 
