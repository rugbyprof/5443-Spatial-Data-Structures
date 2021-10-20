import json
import networkx as nx


with open('major_roads.geojson') as f:
    road_data = json.loads(f.read())

