from shapely.geometry import shape, Point, MultiPoint
import matplotlib.path as mpltPath
import json
import sys

with open(sys.argv[1]) as f:
    providers = [
        {
            'point': Point(*g['coordinates']),
            'polygons': [],
            'features': [],
        }
        for g in json.load(f)['geometries']
    ]

for line in sys.stdin:
    feature = json.loads(line)
    polygon = shape(feature['geometry'])
    for i, p in enumerate(providers):
        if polygon.contains(p['point']):
            providers[i]['polygons'].append(polygon)
            providers[i]['features'].append(feature)

PRIORITY_NAMES = ['CVS', 'Walgreens', 'Clinic', 'Publix', 'YMCA']

num_missing = 0

for p in providers:
    if len(p['polygons']) == 0:
        num_missing += 1
    elif len(p['polygons']) == 1:
        print(json.dumps(p['features'][0]))
    else:
        for name in PRIORITY_NAMES:
            for i, f in enumerate(p['features']):
                if name in f['properties']['location_name']:
                    print(json.dumps(p['features'][i]))

print(f"[filter-geom] Did not find polygons for {num_missing} of {len(providers)} providers.", file=sys.stderr)
