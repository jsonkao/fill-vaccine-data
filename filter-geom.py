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
            "properties": feature["properties"],
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

num_missing = 0
props_of_missing = []

for p in providers:
    if len(p["polygons"]) == 0:
        num_missing += 1
        props_of_missing.append(p["properties"])
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
            num_missing += 1
            props_of_missing.append(p["properties"])

print(
    f"[filter-geom] Could not match {num_missing} of {len(providers)} providers:",
    props_of_missing,
    file=sys.stderr,
)
