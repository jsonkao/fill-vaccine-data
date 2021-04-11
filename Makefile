output.txt: census_data/census.json patterns.csv
	python3 demographics.py > $@

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
# Deriving GeoJSON geometry from WKT SafeGraph geometry
#

# Filter SafeGraph geometry to polygons containing providers
geometry.geojson: VA04-09-2021-13-50-GEOMETRY-2021_03-2021-04-09/geometry.csv wkt.js filter-geom.py providers.geojson
	node wkt.js $< \
	| python3 filter-geom.py providers.geojson \
	| ndjson-reduce \
	| ndjson-map '{type: "FeatureCollection", features: d}' \
	> $@

#
# Use R to get Census data. Must be run from RStudio for some reason
#

census_data/census.json:
	Rscript get-census-data.R

#
# Getting providers from the GISCorps link
#

providers.geojson: richmond.json Makefile filter-boundary.py
	jq '.providers[]' -c $< \
	| ndjson-map '{type: "Feature", geometry: {type: "Point", coordinates: [d.long,d.lat]}, properties: d}' \
	| python3 filter-boundary.py \
	| ndjson-reduce \
	| ndjson-map '{type: "FeatureCollection", features: d}' \
	> $@

providers-old.geojson:
	mapshaper providers/*.shp -filter 'municipali.toLowerCase() == "richmond"' -drop fields=* -o $@

providers:
	curl -L https://opendata.arcgis.com/datasets/c50a1a352e944a66aed98e61952051ef_0.zip -o providers.zip
	unzip -d $@ providers.zip
	rm providers.zip

#
# Getting providers by scraping VaccineFinder (doesnt really work)
#

# Currently this file I just copied from the networks tab using zip code 23220 because it returned 50, which is more results than 44
# richmond.json: richmond-points.geojson scrape.py
# 	python3 scrape.py $< > $@

richmond-points.geojson: richmond-boundary.geojson
	mapshaper $< -point-grid interval=.019 -o $@

richmond-boundary.geojson: Makefile
	curl 'https://data.richmondgov.com/api/geospatial/e9k6-65id?method=export&format=GeoJSON' \
	| mapshaper - \
	-dissolve \
	-clean \
	-o $@
