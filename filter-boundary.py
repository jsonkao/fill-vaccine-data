"""Keep points that are within Richmond City limits"""

from shapely.geometry import shape, Point, MultiPoint
import matplotlib.path as mpltPath
import json
import sys

with open('richmond-boundary.geojson') as f:
    boundary = shape(json.load(f))

num_features = 0
num_kept = 0
for line in sys.stdin:
    feature = json.loads(line)
    num_features += 1
    if boundary.contains(Point(*feature['geometry']['coordinates'])):
        print(json.dumps(feature))
        num_kept += 1

print(f'[filter-boundary] Kept {num_kept} of {num_features} features.', file=sys.stderr)
