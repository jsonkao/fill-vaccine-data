from geomet import wkt
import json
import sys

next(sys.stdin)

for line in sys.stdin:
    wkt_string = [f for f in line.split('"') if 'POLYGON' in f][0]
    values = line.split(',')
    geojson = wkt.loads(wkt_string)
    print(json.dumps({
        'type': 'Feature',
        'geometry': geojson,
        'properties': {
            'placekey': values[0],
            'location_name': values[4],
        }
    }))

