import geopandas
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
                    [63.8539, -153.0531],
                    [63.8539, -75.5336],
                    [25.3115, -153.0531],
                    [25.3115, -75.5336],
                    [63.8539, -153.0531]
                ]
            ]
        }
    }]
}
# read in the geojson file of volcanos where the coords are organized as (lat, lon)
volcanos = geopandas.read_file("./volcanos.geojson")
# load the bounding box that loosely bounds the US, where, again, (lat, lon)
bbox_df = geopandas.GeoDataFrame.from_features(bbox, crs="EPSG:4326")
# spatial index of all the volcanos points
spatial_index = volcanos.sindex
# produces a list of volcano points that intersect the bbox bounding corners
possible_matches_index = list(spatial_index.intersection(tuple(bbox_df.total_bounds)))
# grabs all the documents of each intersecting volcanos found above and sticks them into a dataframe
possible_matches = volcanos.iloc[possible_matches_index]
# takes the dataframe of possible matches and checks if they actually intersect the bounding box.
#   `possible_matches.intersects(bbox_df)` returns a Series of bools (false if no intersection, true otherwise)
#   Then return volcanos that came back true.
precise_matches = possible_matches[possible_matches.intersects(bbox_df)]
print(precise_matches)