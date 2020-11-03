import geopandas
import numpy as np
import matplotlib.pyplot as plt

# a sample bounding box with coordinates ordered as (lon, lat)
bbox = {
    'type':"FeatureCollection",
    "features": [{
        "type": "Feature",
        "properties": {
            "name": "United States"
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-153.0531, 63.8539],
                    [-75.5336, 63.8539],
                    [-75.5336, 25.3115],
                    [-153.0531, 25.3115],
                    [-153.0531, 63.8539]
                ]
            ]
        }
    }]
}
# read in the geojson file of volcanos where the coords are organized as (lon, lat)
#   Yes, that is not a typo. The dataset coordinate order is the standard (x, y), i.e.
#   (lon, lat)
volcanos = geopandas.read_file("./volcanos.geojson")
# load the bounding box that loosely bounds the US, where, again, (x=lon, y=lat)
bbox_df = geopandas.GeoDataFrame.from_features(bbox, crs="EPSG:4326")

# spatial index of all the volcanos points
# queries the volcanos dataframe for all points in bbox_df's bounding box
points_in_bbox, _ = bbox_df.sindex.query_bulk(volcanos.geometry, predicate='intersects')
# create a dataframe of all the intersecting points in volcanos dataframe
possible_matches = volcanos.iloc[points_in_bbox]
# creates a new column in the volcanos dataframe called 'intersects', where each row is True
#   if that volcano is in the bounding box, False if not
volcanos['intersects'] = np.isin(np.arange(0, len(volcanos)), points_in_bbox)

# mere proof you can print the lon and lat of each volcano
#   In the spatial data project, you can just make a geojson feature
#   with each point, append each feature to a FeatureCollection, then
#   shoot that to the frontend for mapping
for volcano in volcanos[volcanos['intersects']]['geometry']:
    print(volcano.x, volcano.y)

# plot the bounding box, the world map, and the volcanos within the bounding box
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
base = world.plot(color='white', edgecolor='black')
second = bbox_df.plot(ax=base, alpha=0.3,edgecolor='blue')
volcanos[volcanos['intersects']].plot(ax=second,color='red', marker='o', markersize=5)
plt.xlim(-180, 180)
plt.ylim(-90, 90)
plt.show()