from datetime import datetime
import demographics

dates = demographics.opening_dates

with open("./demographics.py") as f:
    while "opening_dates" not in next(f):
        pass
    saw_source = False
    for line in f:
        if "}" in line:
            break
        if "#" in line:
            if not saw_source:
                print(line.split("#")[1][1:-1])
                saw_source = True
        else:
            store = line.split('"')[1]
            print(
                f'{store} since {datetime.strptime(dates[store], "%Y-%m-%d").strftime("%B %d, %Y")}'
            )
            saw_source = False
