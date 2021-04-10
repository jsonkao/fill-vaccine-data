const fs = require('fs');
const wellknown = require('wellknown');

const contents = fs.readFileSync(process.argv[2]).toString();

contents.split('\n').slice(1).forEach(row => {
  if (row.length > 0) {
    const wkt = row.split('"').filter(s => s.includes('POLYGON'))[0];
    const values = row.split(',')
    const geom = wellknown(wkt)
    console.log(JSON.stringify({
      type: 'Feature',
      geometry: geom,
      properties: {
        placekey: values[0],
        location_name: values[4]
      }
    }));
  }
})
