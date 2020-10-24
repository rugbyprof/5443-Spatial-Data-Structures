"""
https://rtree.readthedocs.io/en/latest/tutorial.html#using-rtree-as-a-cheapo-spatial-database

"""
import sys
import os
from rtree import index
from misc_functions import *
import glob
import json
import math

idx = index.Index('eq-rtree')

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

def build_index():
    #(left, bottom, right, top)
    eqks = glob.glob("../../../Data/earthquake_data/earthquakes/*.json")

    count = 0
    bad = 0

    for efile in eqks:
        minlat = 999
        minlng = 999
        maxlat = -999
        maxlng = -999
        with open(efile,'r') as f:
            data = f.readlines()

        for row in data[2:]:
            row = row.strip()
            row = row.strip(",")
            if validateJSON(row):
                row = json.loads(row)
                lng,lat,_ = row['geometry']['coordinates']

                if lng < minlng:
                    minlng = lng
                if lat < minlat:
                    minlat = lat
                if lng > maxlng:
                    maxlng = lng
                if lat > maxlat:
                    maxlat = lat

                rect = point_to_bbox(lng,lat)
                idx.insert(count, rect)
                count += 1
            else:
                bad += 1
        print(count,bad)

if __name__=='__main__':

    with open("../../../Data/countries_states/major_cities.geojson") as f:
        data = f.read()

    if validateJSON(data):
        data = json.loads(data)

    #print(data)
    home = (-98.553689,33.875907)

    school = (-98.522419,33.872126)

    print(bearing(home,school))

    print(haversine(home,school))

    print(haversine(home,(-98.53223650057627,33.873401516394416),False))

    print(displace(33.875907,-98.553689,98, 2))

    ul = displace(34.0522342,-118.2436849,315,100)
    br = displace(34.0522342,-118.2436849,135,100)

    # print((ul[1],ul[0],br[1],br[0]))
    # results = [n for n in idx.intersection((ul[1],ul[0],br[1],br[0]))]

    print(point_to_bbox(-98.553689,33.875907,.001))


    # newpoint = point_to_bbox(-98.052487,34.968124)

    # lng1,lat1,lng2,lat2 = newpoint

    # print(newpoint)

    # print(haversine((lng1,lat1),(lng2,lat2)))

    # newpoint = point_to_bbox(2.561524,28.082885)

    # lng1,lat1,lng2,lat2 = newpoint

    # print(newpoint)

    # print(haversine((lng1,lat1),(lng2,lat2)))

    # print(minlng,minlat,maxlng,maxlat)
    # results = [n for n in idx.intersection((minlng,minlat,maxlng,maxlat))]
    # print(f"Res: {len(results)}")
    # for r in results:
    #     print(r)


    
            
        
