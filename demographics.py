"""Analyze demographics of SafeGraph placekey polygons"""

from collections import defaultdict
import json
import csv

opening_dates = {
    # https://www.wric.com/health/coronavirus/cvs-expanding-virginia-vaccination-locations-from-28-to-36/
    # https://www.wric.com/health/coronavirus/cvs-updates-plans-to-administer-vaccines-in-virginia/
    'CVS': '2021-02-12',

    # https://wjla.com/news/coronavirus-vaccine/dates-availability-in-flux-as-cvs-walgreens-offer-covid-19-vaccinations-in-va-md
    # NOTE: Confirm w/ call
    'Walgreens': '2021-02-12',

    # https://www.nbc12.com/2021/04/04/nearly-at-risk-seniors-receive-covid-vaccine-during-richmond-clinic/
    # NOTE: Was this just one event?
    'JenCare Senior Medical Center': None
}

with open("census_data/census.json") as f:
    census = {r["GEOID"]: r for r in json.load(f)}

cbg_counts = defaultdict(int)
with open("patterns.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        homes = json.loads(row["visitor_home_cbgs"])
        for cbg in homes:
            cbg_counts[cbg] += homes[cbg]

total_count = 0
weighted_sums = defaultdict(int)
for cbg in cbg_counts:
    if cbg.startswith("51"):
        total_count += cbg_counts[cbg]
        if "income" not in census[cbg]:
            continue
        for col in ["white", "black", "asian", "hispanic", "income"]:
            value = census[cbg][col] * cbg_counts[cbg]
            if col != "income":
                value /= census[cbg]["total_population"]
            weighted_sums[col] += value

for field in weighted_sums:
    print(f"{field}: {weighted_sums[field] / total_count}")
