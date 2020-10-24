"""
https://rtree.readthedocs.io/en/latest/tutorial.html#using-rtree-as-a-cheapo-spatial-database

"""
import sys
import os
import kdtree
from misc_functions import *
import glob
import json
import math

kd = kdtree.create(dimensions=2)

def validateFloat(x):
    try: 
        float(x)
        return True
    except ValueError:
        return False

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

def point_to_bbox(lng,lat,offset=.001):
    #(left, bottom, right, top)

    return (lng-offset,lat-offset,lng+offset,lat+offset)

def move_point(p,distance,feet=False):
    p[1] += float(d) / 111111.0
    p[0] += float(d) / (111111.0*(math.cos(10)))
    return p

def build_tree():
    #(left, bottom, right, top)
    with open("../../../Data/ufos_export.json","r") as f:
        data = f.readlines()

    count = 0
    bad = 0

    for row in data:
        row = row.strip()
        if validateJSON(row):
            row = json.loads(row)
            # print(row)
            if validateFloat(row['longitude']):
                lng = float(row['longitude'])
            else:
                continue
            if validateFloat(row['latitude']):
                lat = float(row['latitude'])
            else:
                continue

            kd.add((lng,lat))
            count += 1
        else:
            bad += 1
        if count % 10000 == 0:
            print(f"done: {count}, togo: {len(data)-count}")

if __name__=='__main__':

    # with open("../../../Data/countries_states/major_cities.geojson") as f:
    #     data = f.read()

    # if validateJSON(data):
    #     data = json.loads(data)

    build_tree()

    print(kd.search_nn((-98.553689,33.875907)))

    res = kd.search_nn_dist((-98.553689,33.875907),2)

    temp = []
    for r in res:
        if not r in temp:
            temp.append(r)
    
    print(len(res))
    print(len(temp))

    print(temp)

    #print(data)
    # home = (-98.553689,33.875907)
    # school = (-98.522419,33.872126)



    
            
        
