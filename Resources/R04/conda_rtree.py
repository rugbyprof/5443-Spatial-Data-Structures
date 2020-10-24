"""
https://skipperkongen.dk/2013/02/18/trying-a-python-r-tree-implementation/
"""

from rtree import index

mystreet = {
    "type": "Feature",
    "geometry": {
        "type":"MultiLineString",
        "coordinates":[[
            [1402528.63585071451962,7491973.552016104571521],
            [1402597.665066956076771,7491840.036925406195223]
        ]]
    },
    "properties": {
        "name": "Anders Henriksens Gade",
        "oneway": "yes"
    },
    "crs": {
        "type":"link",
        "properties": {
            "http://spatialreference.org/ref/sr-org/6864/proj4/",
            "proj4"
        }
    }
}
 
# minimum bounding rectangle for feature
left, bottom, right, top = (
    1402528.63585071, 
    7491840.03692541, 
    1402597.66506696, 
    7491973.5520161)

# create an in-memory R-tree index
idx = index.Index()
# disk-based R-tree: 
# idx = index.Index('spatial.db')
 
# Store the geojson object in the (now clustered) index
# In tutorial: idx.insert(id=0, bounds=(left, bottom, right, top), obj=mystreet)
# What actually worked... no keywords args for id and bounds:
idx.insert(0, (left, bottom, right, top), obj=mystreet)

feature1 = list(idx.intersection((left, bottom, right, top), objects=True))[0].object
feature2 = list(idx.nearest((left, bottom, right, top), objects=True))[0].object