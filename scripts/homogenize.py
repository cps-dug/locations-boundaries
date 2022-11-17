import json
import sys

headers = set()
geojson = json.load(sys.stdin)

for feature in geojson["features"]:
    headers.update(feature["properties"])

for feature in geojson["features"]:
    missing_headers = headers - feature["properties"].keys()
    feature["properties"].update(dict.fromkeys(missing_headers))

json.dump(geojson, sys.stdout)
