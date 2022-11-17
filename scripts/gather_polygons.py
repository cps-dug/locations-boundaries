import json
import sys

geojson = json.load(sys.stdin)

school_grades_boundaries = {}

for feature in geojson["features"]:
    key = (feature["properties"]["SCHOOL_ID"], feature["properties"]["BOUNDARYGR"])
    if key in school_grades_boundaries:
        school_grades_boundaries[key].append(feature)
    else:
        school_grades_boundaries[key] = [feature]

combined_features = []
for key, features in list(school_grades_boundaries.items()):
    if len(features) == 1:
        combined_features.append(features[0])
    else:
        multipolygon = {
            "type": "MultiPolygon",
            "coordinates": [feature["geometry"]["coordinates"] for feature in features],
        }
        properties = features[0]["properties"]
        properties["Shape_STArea()"] = None
        properties["Shape_STLength()"] = None
        combined_features.append(
            {"type": "Feature", "geometry": multipolygon, "properties": properties}
        )

geojson["features"] = combined_features

json.dump(geojson, sys.stdout)
