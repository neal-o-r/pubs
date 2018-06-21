import json
import pandas as pd

d = json.load(open('./bar.geojson'))
pubs = d['features']
pubs += json.load(open('./pub.geojson'))['features']
pubs += json.load(open('./club.geojson'))['features']


name =[]
lat = []
lng = []
for x in pubs:
        name.append(x['properties']['name']
                        if 'name' in x['properties'] else None)
        if x['geometry']['type'] == 'Point':
                lat.append(x['geometry']['coordinates'][1])
                lng.append(x['geometry']['coordinates'][0])
        else:
                lat.append(x['geometry']['coordinates'][0][0][1])
                lng.append(x['geometry']['coordinates'][0][0][0])

df = pd.DataFrame(data={'name':name, 'latitude':lat, 'longitude':lng})


