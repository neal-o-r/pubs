import pandas as pd
import requests
import json

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

df = pd.read_csv('liquor-licences.csv')
df = df.query('description == "Publican\'s Licence (7-Day Ordinary)"')
df = df[~df.trading_name.isnull()]

df['address_2'] = [a if not a.startswith('&') else ''
                                for a in df['address_2'].astype(str)]
df['address_2'] = df['address_2'].str.replace('nan', '')

df['Full_address'] = df.filter(regex='^address').fillna('').apply(lambda x:
                                                ", ".join(x), axis=1)
df['Full_address'] = df.trading_name.fillna('') + ', ' + df.Full_address
df['Full_address'] = df.Full_address.str.rstrip('+') + ', ' + df.county
df['Full_address'] = df.Full_address.str.replace(' ,',
                                        '').str.lstrip(' ')


def get_lat_lon(address):

        params = {
                'address': address,
                'region': 'ie',
                'key': 'AIzaSyChQ8dLwxwqV0TnIlAKhFw3akqvpW0-54Q'
                }

        # Do the request and get the response data
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()

        # Use the first result
        if len(res['results']) == 0:
                return {'lat':None, 'lng':None, 'address':None}

        result = res['results'][0]
        geodata = dict()
        geodata['lat'] = result['geometry']['location']['lat']
        geodata['lng'] = result['geometry']['location']['lng']
        geodata['address'] = result['formatted_address']

        return geodata

d = json.load(open('run.json'))

n = len(d)
t = n + 2200 # rate limit

for i, a in enumerate(df.Full_address.values[n:t]):
        out = get_lat_lon(a)
        print(str(i) + ('*' if out['lat'] is None else ''))
        d.append(out)

json.dump(d, open('run.json', 'w'), indent=4)

lat = [x['lat'] for x in d]
lon = [x['lng'] for x in d]
g_add = [x['address'] for x in d]

df_top = df.head(len(d)).copy()

df_top['color'] = 'a80000'
df_top['url'] = ''
df_top['latitude'] = lat
df_top['longitude'] = lon
df_top['G_address'] = g_add
df_top['type'] = 'pub'

df_top[['latitude','longitude','trading_name',
        'type','color','url']].dropna().to_csv('pubs.csv',
                                        index_label='id',
                                        header=['latitude','longitude','name',
                                        'type','color','url'])
