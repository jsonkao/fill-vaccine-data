import matplotlib.path as mpltPath
from shapely.geometry import shape, Point, MultiPoint
import sys
import json

with open(sys.argv[1]) as f:
     placekeys = set([
         f['properties']['placekey'] for f in json.load(f)['features']
     ])

is_first = True
for fname in sys.argv[2:]:
    date = '2021-' + '-'.join(fname.split('/')[1:-2])
    with open(fname) as f:
        if is_first:
            sys.stdout.write(next(f)[:-1] + ',"date"\n')
            is_first = False
        for line in f:
            if line[:19] in placekeys:
                sys.stdout.write(line[:-1] + ',' + date + '\n')
        print('Completed', fname, file=sys.stderr)
