""" flask_folium_02.py

    Required packages:
        import geopandas as gpd
        import pandas as pd
        import folium
        import branca
        import requests
        import json

    Usage:

    Start the flask server by running:

        $ python flask_folium_02.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""
import geopandas as gpd
import pandas as pd
import folium
import branca
import requests
import json
from flask import Flask
from flask import jsonify
from folium.features import GeoJson, GeoJsonTooltip, GeoJsonPopup
from flask import request

from folium.plugins import MousePosition


app = Flask(__name__)


with open("us_states_abbrs.json") as f:
    abbr_data = f.read()

abbr_data = json.loads(abbr_data)

print("abbrs:")
print(abbr_data)

@app.route('/')
def index():

    response = requests.get(r"https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json")
    data = response.json()
    states = gpd.GeoDataFrame.from_features(data, crs='EPSG:4326')

    print("states:")
    print(states.head())

    start_coords = (33.8713557,-98.5215656)
    folium_map = folium.Map(location=start_coords, zoom_start=14)


    formatter = "function(num) {return L.Util.formatNum(num, 3);};"

    MousePosition(
        position='topright',
        separator=' | ',
        empty_string='NaN',
        lng_first=True,
        num_digits=20,
        prefix='Coordinates:',
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(folium_map)


    return folium_map._repr_html_()

@app.route('/abbrs/')
def get_abbrs():
    return jsonify(abbr_data)

@app.route('/pos/')
def post_click():
  lat = request.args.get('lat', default = 0.0, type = float)
  lon = request.args.get('lon', default = 0.0, type = float) 
  print(lat,lon)

if __name__ == '__main__':
    app.run(debug=True,port=5556)