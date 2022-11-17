geography.db : location.geojson boundary.geojson
	geojson-to-sqlite $@ location location.geojson --spatialite_mod=/opt/homebrew/Cellar/libspatialite/5.0.1_2/lib/mod_spatialite.dylib --spatial-index
	geojson-to-sqlite $@ boundary boundary.geojson --spatialite_mod=/opt/homebrew/Cellar/libspatialite/5.0.1_2/lib/mod_spatialite.dylib --spatial-index

location.geojson : location_2023.geojson
	cat $< | python scripts/homogenize.py > $@

boundary.geojson : boundary_2023.geojson
	cat $< | python scripts/homogenize.py > $@

location_%.geojson :
	wget -O $@ "https://api.cps.edu/maps/cps/GeoJSON?mapname=SCHOOL&year=$*"

boundary_%.geojson : elementary_schools_boundary_%.geojson high_schools_boundary_%.geojson
	geojson-merge $^ > $@

elementary_schools_boundary_%.geojson :
	wget -O $@ "https://api.cps.edu/maps/cps/GeoJSON?mapname=BOUNDARY_ES&year=$*"

high_schools_boundary_%.geojson :
	wget -O $@ "https://api.cps.edu/maps/cps/GeoJSON?mapname=BOUNDARY_HS&year=$*"
