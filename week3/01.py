import json, csv
import urllib.request as request

scr = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"
with request.urlopen(scr) as response:
    data = json.load(response)

data_info = data["result"]["results"]

with open("data.csv", mode="w", encoding="utf-8", newline="") as csv_file:
    writer = csv.writer(csv_file)

    for attraction in data_info:
        if (int(attraction["xpostDate"] [:4]) >= 2015):
            img_url = "https" + attraction["file"].split("https",2)[1]
            list = [attraction["stitle"], attraction["address"][5:8], attraction["longitude"], attraction["latitude"], img_url]
            writer.writerow(list)
