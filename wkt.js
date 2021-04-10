const fs = require('fs');
const wellknown = require('wellknown');

const contents = fs.readFileSync(process.argv[2]).toString();

contents.split('\n').slice(1).forEach(row => {
  if (row.length > 0) {
    const wkt = row.split('"')[1];
    const values = row.split(',')
    const geom = wellknown(row.split('"')[1]);
    console.log(JSON.stringify({
      type: 'Feature',
      geometry: geom,
      properties: {
        location_name: values[4]
      }
    }));
  }
})
