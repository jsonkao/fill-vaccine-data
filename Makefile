main: census_data/census.json patterns.csv
	python3 demographics.py

#
# Deriving GeoJSON geometry from WKT SafeGraph geometry
#

# Filter SafeGraph geometry to polygons containing providers
geometry.geojson: VA04-09-2021-13-50-GEOMETRY-2021_03-2021-04-09/geometry.csv wkt.js filter-geom.py
	node wkt.js $< \
	| python3 filter-geom.py providers.geojson \
	| ndjson-reduce \
	| ndjson-map '{type: "FeatureCollection", features: d}' \
	| mapshaper - name=geometry -clean -o $@

#
# Patterns download and filter
#

# Filter SafeGraph patterns to those with placekeys
patterns.csv: geometry.geojson
	python3 cut.py geometry.geojson $(wildcard $(basename $@)/*/*/*/*.csv) > $@

# Decompress all gz files
decompress:
	find patterns -name "*.gz" -print0 | parallel -q0 gunzip -k

#
# Use R to get Census data. Must be run from RStudio for some reason
#

census_data/census.json:
	Rscript get-census-data.R

#
# Getting providers from the GISCorps link
#

providers.geojson:
	mapshaper providers/*.shp -filter 'municipali.toLowerCase() == "richmond"' -drop fields=* -o $@

providers:
	curl -L https://opendata.arcgis.com/datasets/c50a1a352e944a66aed98e61952051ef_0.zip -o providers.zip
	unzip -d $@ providers.zip
	rm providers.zip

#
# Getting providers by scraping VaccineFinder (doesnt really work)
#

richmond.json: richmond-points.geojson scrape.py
	python3 scrape.py $< > $@

richmond-points.geojson: richmond.geojson
	mapshaper $< -point-grid interval=.019 -o $@

richmond.geojson:
	curl -o $@ 'https://data.richmondgov.com/api/geospatial/e9k6-65id?method=export&format=GeoJSON'
