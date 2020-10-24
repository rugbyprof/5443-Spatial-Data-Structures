#!/usr/bin/python3

import plotly
import plotly.graph_objects as go
from geo import mapbox_access_token
from geo import get_country_border
from geo import get_bbox
from geo import get_meteorites


if __name__ == '__main__':
    country_points = get_country_border("Brazil")

    bbox = get_bbox(country_points['latlon'])

    print(bbox)

    lats,lons = get_meteorites()

    print(lats)

    fig = go.Figure(go.Scattermapbox(
            lat=lats,
            lon=lons,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=3
            ),
            #text=['Montreal'],
        ))

    #{'lon': -51.447769636499956, 'lat': -14.237527770999932, 'min_lat': -33.74228037499995, 'max_lat': 5.267224833000086, 'min_lon': -74.01847469099997, 'max_lon': -28.877064581999946}



    # fig = go.Figure(go.Scattermapbox(
    #         lon = [bbox['max_lon'],bbox['min_lon'],bbox['max_lon'],bbox['min_lon']],
    #         lat = [bbox['min_lat'],bbox['min_lat'],bbox['min_lat'],bbox['max_lat']],
    #         mode='lines',
    #         marker=go.scattermapbox.Marker(
    #             size=3
    #         ),
    #         #text=['Montreal'],
    #     ))
    # fig.add_trace(
    #     go.Scattergeo(
    #         locationmode = 'USA-states',

    #         mode = 'lines',
    #         line = dict(width = 1,color = 'red'),
    #         opacity = 0,
    #     )
    # )

    fig.add_trace(
        go.Scattergeo(
            # locationmode = 'USA-states',
            lon = [bbox['min_lon'], bbox['max_lon']],
            lat = [bbox['min_lat'], bbox['max_lat']],
            mode = 'lines',
            line = dict(width = 4,color = 'red'),
            # opacity = float(80) / float(100),
        )
    )

    fig.update_layout(
        hovermode='closest',
        template="plotly_dark",
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=bbox['lat'],
                lon=bbox['lon']
            ),
            pitch=50,
            zoom=3
            
        )
    )



    fig.show()
    plotly.offline.plot(fig, filename='meteors.html')