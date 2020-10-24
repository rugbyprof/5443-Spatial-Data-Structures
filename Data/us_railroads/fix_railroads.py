import json 
import pprint 
import sys

def get_bounding_box(points):
    minlat = points[0][1]
    maxlat = points[0][1]
    minlon = points[0][0]
    maxlon = points[0][0]

    for p in points:
        if p[0] < minlon:
            minlon = p[0]
        if p[0] > maxlon:
            maxlon = p[0]
        if p[1] < minlat:
            minlat = p[1]
        if p[1] > maxlat:
            maxlat = p[1]

    return {"minlon":minlon,"minlat":minlat,"maxlon":maxlon,"maxlat":maxlat}

def inside(bbox,p):
    return p[0] >= bbox['minlon'] and p[0] <= bbox['maxlon'] and p[1] >= bbox['minlat'] and p[1] <= bbox['maxlat']

def point_in_bbox(bbox,points):
    for p in points:
        if inside(bbox,p):
            return True

    return False


with open("../countries_states/us_state_polygons_5m.geojson") as f:
    data = f.read() 

states = json.loads(data)

state_bboxs = {}
for row in states['features']:
    points = []
    if row['geometry']['type'] == 'MultiPolygon':
        for poly in row['geometry']["coordinates"]:
            for line in poly:
                for point in line:
                    points.append(point)
    else:
        for line in row['geometry']["coordinates"]:
                for point in line:
                    points.append(point)

    state_bboxs[row['properties']["NAME"]] = get_bounding_box(points)

for state,box in state_bboxs.items():
    print(box)

            
with open("us_railroads.geojson") as f:
    data = f.read() 

railroads = json.loads(data)

# print(len(railroads['features']))
# sys.exit()

for row in railroads['features']:
    if row['geometry']['type'] == "LineString":
        points = row['geometry']['coordinates']
    else:
        points = []
        for line in row['geometry']['coordinates']:
            points.extend(line)

    states = []
    for state,box in state_bboxs.items():
        if point_in_bbox(box,points):
            states.append(state)
    row['properties']['states'] = states
    #print(states)

railroads["type"] = "FeatureCollection"
features = {}
start = 0
chunk = 36200
for i in range(5):
    features[i] = railroads['features'][start:start+chunk]
    start += chunk

for i in range(5):
    print(len(features[i]))
    railroads['features'] = features[i]
    with open(f"us_railroads_with_states{i}.geojson",'w') as f:
        f.write(json.dumps(railroads,indent=2))

