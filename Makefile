MAKEFLAGS += -j4

output.txt: census_data/census.json patterns.csv demographics.py
	python3 demographics.py > $@

#
# Patterns download and filter
#

# Filter SafeGraph patterns to those with placekeys
patterns.csv: places.geojson filter-placekeys.py
	python3 filter-placekeys.py $< $(wildcard $(basename $@)/*/*/*/patterns.csv) > $@


# Filter files to locality. Filename = patterns/MM/DD/HH/patterns.csv
filter-patterns: $(addsuffix /patterns.csv,$(wildcard patterns/*/*/*))
patterns/%/patterns.csv:
	cat $(wildcard $(shell dirname $@)/*.csv) | python3 filter-richmond.py > $@

# Decompress all gz files
decompress:
	find patterns -name "*.gz" -print0 | parallel -q0 gunzip -k

# Download SafeGraph files. Virginia began it's rollout roughly around the beggining of Jan maybe. Just CVS maybe. Idrk
download:
	aws s3 sync s3://sg-c19-response/weekly-patterns-delivery-2020-12/weekly/patterns/2021 patterns --profile safegraphws --endpoint https://s3.wasabisys.com --include '*' --exclude '01/*'

#
# Deriving GeoJSON geometry from WKT SafeGraph geometry
#

MAKEFLAGS = -j4

# Filter SafeGraph geometry to polygons containing providers
# Geometry csv file is proprietary; ask Spencer for Richmond City
places.geojson: VA04-09-2021-13-50-GEOMETRY-2021_03-2021-04-09/geometry.csv filter-geom.py providers/vaccine-finder.geojson
	cat $< \
	| python3 wkt2geojson.py \
	| python3 filter-geom.py providers/vaccine-finder.geojson providers/giscorps.geojson \
	| ndjson-reduce \
	| ndjson-map '{type: "FeatureCollection", features: d}' \
	> $@

#
# Use R to get Census data. Must be run from RStudio for some reason
#

census-data/census.json:
	Rscript census-data/get-census-data.R

#
# Getting providers
#

providers/vaccine-finder.geojson: providers/vaccine-finder.json
	jq '.providers[]' -c $< \
	| ndjson-map '{type: "Feature", geometry: {type: "Point", coordinates: [d.long,d.lat]}, properties: d}' \
	| python3 filter-boundary.py \
	| ndjson-reduce \
	| ndjson-map '{type: "FeatureCollection", features: d}' \
	| mapshaper - -uniq guid -o $@

providers/giscorps.geojson: providers/giscorps
	mapshaper $</*.shp -filter 'municipali.toLowerCase() == "richmond" && State == "VA"' -o $<.tmp.geojson ndjson
	cat $<.tmp.geojson \
	| python3 filter-boundary.py \
	| ndjson-reduce \
	| ndjson-map '{type: "FeatureCollection", features: d}' \
	> $@
	rm $<.tmp.geojson

providers/giscorps:
	curl -L https://opendata.arcgis.com/datasets/c50a1a352e944a66aed98e61952051ef_0.zip -o $@.zip
	unzip -d $@ $@.zip
	rm $@.zip

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

#
# Vaccine Distribution Allocations by Jurisdiction
#

# Rows for Pfizer, Moderna, Jannsen
allocations.csv:
	( \
	curl https://data.cdc.gov/api/views/saz5-9hgg/rows.csv?accessType=DOWNLOAD; \
	curl https://data.cdc.gov/api/views/b7pe-5nws/rows.csv?accessType=DOWNLOAD; \
	curl https://data.cdc.gov/api/views/w9zu-fywh/rows.csv?accessType=DOWNLOAD \
	) \
	| grep '^Virginia' \
	> $@

#
# Normalization stats
#

NORM_DIR = normalization_stats
norm: $(NORM_DIR)/normalization_stats.csv

$(NORM_DIR)/normalization_stats.csv: Makefile
	find $(NORM_DIR)/*/* -type f | head -n1 | xargs cat | head -n1 > $@
	find $(NORM_DIR)/*/* -type f | xargs cat | grep ,va, >> $@

$(NORM_DIR):
	aws s3 sync s3://sg-c19-response/weekly-patterns-delivery-2020-12/weekly/normalization_stats/2021 $(NORM_DIR) --profile safegraphws --endpoint https://s3.wasabisys.com --exclude '*' --include "*.csv"
