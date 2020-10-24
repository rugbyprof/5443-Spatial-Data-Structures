## UFO Data


- You can "concatenate" both files:
- `cat fixed_ufos_one.geojson > fixed_ufos_two.geojson`

BUT, they are both standalone geojson files, so you will
need to remove the following from file one:

```
    ]
}
```

and remove from file two:

```
{
    "type": "FeatureCollection", 
    "features": [
```
