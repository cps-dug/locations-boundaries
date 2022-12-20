import json
import sys

geojson = json.load(sys.stdin)

school_grades_boundaries = {}

for feature in geojson["features"]:
    key = (feature["properties"]["SCHOOL_ID"], feature["properties"]["BOUNDARYGR"])
    if feature["geometry"]["type"] == "LineString":
        continue
    if feature["geometry"]["type"] == "GeometryCollection":
        polygons = [
            geom
            for geom in feature["geometry"]["geometries"]
            if geom["type"] == "Polygon"
        ]
        for polygon in polygons:
            derived_feature = feature.copy()
            derived_feature["geometry"] = polygon
            if key in school_grades_boundaries:
                school_grades_boundaries[key].append(derived_feature)
            else:
                school_grades_boundaries[key] = [derived_feature]
    elif key in school_grades_boundaries:
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
