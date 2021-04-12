"""Analyze demographics of SafeGraph placekey polygons"""

from collections import defaultdict
from datetime import datetime
import json
import csv

opening_dates = {
    # https://www.wric.com/health/coronavirus/cvs-expanding-virginia-vaccination-locations-from-28-to-36/
    # https://www.wric.com/health/coronavirus/cvs-updates-plans-to-administer-vaccines-in-virginia/
    "CVS": "2021-02-12",
    # https://www.wavy.com/covid-19-vaccine/the-latest-some-hampton-roads-pharmacies-and-their-customers-await-covid-19-vaccine-delivery-this-week/
    # NOTE: Confirm w/ call
    "Walgreens": "2021-02-24",
    # https://www.prnewswire.com/news-releases/chenmed-accelerates-safe-covid-19-vaccine-administrations-to-tens-of-thousands-of-high-risk-seniors-where-they-receive-care-301233089.html
    # NOTE: Confirm. Not great information
    "JenCare Senior Medical Center": "2021-02-23",
    # https://www.wavy.com/covid-19-vaccine/the-latest-some-hampton-roads-pharmacies-and-their-customers-await-covid-19-vaccine-delivery-this-week/
    # NOTE: Confirm.
    "Kroger": "2021-02-24",
    # Just putting as same as CVS for now
    "MinuteClinic": "2021-02-12",
    # https://www.valdostadailytimes.com/news/business/publix-pharmacy-opens-appointments-for-covid-19-vaccinations-in-three-states/article_51388f06-ecf3-5a6a-a5af-d68a42bc1007.html
    # See linked document under "Virginia locations"
    "Publix Super Markets": "2021-03-25",
    # https://www.wavy.com/covid-19-vaccine/pharmacies-administering-covid-19-vaccine/
    # NOTE: Confirm
    "Rite Aid": "2021-01-21",
    # https://www.wavy.com/covid-19-vaccine/the-latest-some-hampton-roads-pharmacies-and-their-customers-await-covid-19-vaccine-delivery-this-week/
    # NOTE: Confirm
    "Walgreens": "2021-02-24",
    # https://www.wavy.com/covid-19-vaccine/the-latest-some-hampton-roads-pharmacies-and-their-customers-await-covid-19-vaccine-delivery-this-week/
    # NOTE: Confirm. Definitely later than this.
    "Walmart Pharmacy 10 2821": "2021-02-24",
    # https://www.wric.com/health/coronavirus/henrico-county-administers-reaches-milestone-100000-covid-19-vaccine-shots/
    # NOTE: Confirm; source: https://richmond.com/business/watch-now-independent-pharmacies-are-a-lifeline-in-the-covid-vaccine-rollout/article_c58bcc8d-75e5-5e2d-aad0-11f1a95d73ab.html
    "Westwood Pharmacy": "2021-01-19",
}

# Load census data

with open("census_data/census.json") as f:
    census = {r["GEOID"]: r for r in json.load(f)}

# Sum up CBG contributions

def later_than(a_str, b_str):
    [a, b] = [datetime.strptime(s, "%Y-%m-%d") for s in [a_str, b_str]]
    return a > b

cbg_counts = defaultdict(int)
with open("patterns.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # If opening date later than the end of a data collection period, continue
        if later_than(
                opening_dates[row["location_name"]] or "2021-01-01",
            row["date_range_end"].split("T")[0],
        ):
            continue

        homes = json.loads(row["visitor_home_cbgs"])
        for cbg in homes:
            if cbg.startswith("51"):
                cbg_counts[cbg] += homes[cbg]

# Evaluate demographics of different counts of CBGs

total_count = 0
weighted_sums = defaultdict(int)
categories = ["white", "black", "asian", "hispanic"]
for cbg in list(cbg_counts.keys()):
    count = cbg_counts[cbg]
    total_count += count
    for c in categories:
        # Count * proportion
        weighted_sums[c] += count * (census[cbg][c] / census[cbg]["total_population"])

for field in weighted_sums:
    print(f"{field}: {weighted_sums[field] / total_count}")
