from shapely.geometry import shape, Point, MultiPoint
import matplotlib.path as mpltPath
import json
import sys

with open(sys.argv[1]) as f, open(sys.argv[2]) as f2:
    providers = [
        {
            "point": Point(*feature["geometry"]["coordinates"]),
            "polygons": [],
            "features": [],
            "original_feature": feature,
        }
        for feature in json.load(f)["features"] + json.load(f2)['features']
    ]

for line in sys.stdin:
    feature = json.loads(line)
    polygon = shape(feature["geometry"])
    for i, p in enumerate(providers):
        if polygon.contains(p["point"]):
            providers[i]["polygons"].append(polygon)
            providers[i]["features"].append(feature)

PRIORITY_NAMES = [
    "CVS",
    "Walgreens",
    "Clinic",
    "Publix",
    "YMCA",
    "Kroger",
    "Pharmacy",
    "Rite Aid",
]

missing_providers = []

for p in providers:
    if len(p["polygons"]) == 0:
        missing_providers.append(p["original_feature"])
    elif len(p["polygons"]) == 1:
        print(json.dumps(p["features"][0]))
    else:
        found_one = False
        for name in PRIORITY_NAMES:
            for i, f in enumerate(p["features"]):
                if name in f["properties"]["location_name"]:
                    found_one = True
                    print(json.dumps(p["features"][i]))
        if not found_one:
            print(
                f"[filter-geom] No priority names: {[f['properties']['location_name'] for f in p['features']]}",
                file=sys.stderr,
            )
            missing_providers.append(p["original_feature"])

debug_msg = ''
if '--debug' in sys.argv:
    debug_msg = ':\n' + json.dumps({'type': 'FeatureCollection', 'features': missing_providers})

print(
    f"[filter-geom] Could not match {len(missing_providers)} of {len(providers)} providers{debug_msg}",
    file=sys.stderr,
)
