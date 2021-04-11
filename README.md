## Plan

1. Focus scope on Richmond, Virginia.
2. Scrape VaccineFinder
3. Match sites with SG placekey id's using Geometry dataset
4. Use Weekly Patterns dataset to find home cbg's of those visiting vaccine sites and find their demographics
5. Validate results at the lowest level possible
    * Compare proportion SG visits with proportion actual visits (either by institution x race, neighborhood x race, or just race)
    * Maybe run methodology on other cities where ground truth is more available
6. Ask a stats god whats up

## Instructions

0. If adding new SafeGraph files (by running `make download`), run `make decompress`.

1. Somehow put a list of providers into `richmond.json`. I copy-pasted results from multiple zipcodes in Richmond from the Networks Tab from VaccineFinder.

2. `make output.txt; cat output.txt`
