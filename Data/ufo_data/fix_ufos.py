import json 
import pprint 
import sys
from collections import OrderedDict 

with open("ufos_export.json") as f:
    data = f.readlines()

geojson = OrderedDict() 

geojson["type"] = "FeatureCollection"
geojson["features"] = []

for ufo in data:
    row = OrderedDict() 
    row["type"] = "Feature"
    row["properties"] = {}
    row["geometry"] = { "type": "Point", "coordinates":[]}

    ufo = ufo.decode("utf-8", "strict") 
    ufo = json.loads(ufo)

    del ufo['_id']

    ufo['city'] = ufo['city'].capitalize()
    ufo['country'] = ufo['country'].upper()
    ufo['state'] = ufo['state'].upper()
    ufo['datetime'] = ufo['datetime']
    row['geometry']['coordinates'] = [ufo['longitude'],ufo['latitude']]

    del ufo['longitude']
    del ufo['latitude']

    row['properties'] = ufo


    geojson["features"].append(row)

with open('fixed_ufos.geojson','w') as f:
    f.write(json.dumps(dict(geojson),indent=4))
