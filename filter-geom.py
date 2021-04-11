from shapely.geometry import shape, Point, MultiPoint
import matplotlib.path as mpltPath
import json
import sys

with open(sys.argv[1]) as f:
    providers = [
        {
            'point': Point(*feature['geometry']['coordinates']),
            'polygons': [],
            'features': [],
        }
        for feature in json.load(f)['features']
    ]

for line in sys.stdin:
    feature = json.loads(line)
    polygon = shape(feature['geometry'])
    for i, p in enumerate(providers):
        if polygon.contains(p['point']):
            providers[i]['polygons'].append(polygon)
            providers[i]['features'].append(feature)

PRIORITY_NAMES = ['CVS', 'Walgreens', 'Clinic', 'Publix', 'YMCA', 'Kroger', 'Walmart Pharmacy', 'Rite Aid']

num_missing = 0

for p in providers:
    if len(p['polygons']) == 0:
        num_missing += 1
    elif len(p['polygons']) == 1:
        print(json.dumps(p['features'][0]))
    else:
        found_one = False
        for name in PRIORITY_NAMES:
            for i, f in enumerate(p['features']):
                if name in f['properties']['location_name']:
                    found_one = True
                    print(json.dumps(p['features'][i]))
        if not found_one:
            print(f"[filter-geom] No priority names: {[f['properties']['location_name'] for f in p['features']]}", file=sys.stderr)

print(f"[filter-geom] Could not match {num_missing} of {len(providers)} providers.", file=sys.stderr)
