"""
From csv to geojson
"""
import csv
import copy 
import json
"""
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [125.6, 10.1]
  },
  "properties": {
    "name": "Dinagat Islands"
  }
}
"""

mini = {
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [0, 0]
  },
  "properties": {
    "name": "",
    "marker-size": "medium",
    "marker-symbol": "airport",
    "marker-color": "#f00",
    "stroke": "#555555",
    "stroke-opacity": 1,
    "stroke-width": 2,
    "fill": "#555555",
    "fill-opacity": 0.5
  }
}

unique = {}

wanted = [1,2,3,6,7,11]

geo_list = []
# open file
with open('airports', newline='\n') as csvfile:
    data = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in data:
        geo_mini = copy.deepcopy(mini) 
        lon = float(row[7])
        lat = float(row[6])
        geo_mini["geometry"]["coordinates"] = [lon,lat]
        geo_mini["properties"]["region"] = row[11]
        geo_list.append(geo_mini)

geo_object = {
    "type": "FeatureCollection",                                                           
    "features":geo_list
}

f = open("output","w")
f.write(json.dumps(geo_object,indent=4))
f.close()




"""
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [125.6, 10.1]
  },
  "properties": {
    "name": "Dinagat Islands"
  }
}
"""


            
#             if i == 11:
#                 loc = col.split("/")
#                 if not loc[0] in unique:
#                     unique[loc[0]] = 0
#                 unique[loc[0]]+=1
#             i += 1
# for k,v in unique.items():
#     print(k,v)
