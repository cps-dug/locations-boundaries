geography.db : location.geojson boundary.geojson blocks_2020.geojson
	geojson-to-sqlite $@ location location.geojson --spatial-index
	geojson-to-sqlite $@ boundary boundary.geojson --spatial-index
	geojson-to-sqlite $@ blocks_2020 blocks_2020.geojson --spatial-index

location.geojson : location_2023.geojson
	cat $< | python scripts/homogenize.py > $@

boundary.geojson : boundary_2023.geojson
	cat $< | python scripts/homogenize.py | python scripts/gather_polygons.py | npx geojson-rewind --clockwise > $@

location_%.geojson :
	wget -O $@ "https://api.cps.edu/maps/cps/GeoJSON?mapname=SCHOOL&year=$*"

boundary_%.geojson : elementary_schools_boundary_%.geojson high_schools_boundary_%.geojson
	npx geojson-merge $^ > $@

elementary_schools_boundary_%.geojson :
	wget -O $@ "https://api.cps.edu/maps/cps/GeoJSON?mapname=BOUNDARY_ES&year=$*"

high_schools_boundary_%.geojson :
	wget -O $@ "https://api.cps.edu/maps/cps/GeoJSON?mapname=BOUNDARY_HS&year=$*"

blocks_2020.geojson :
	python scripts/blocks.py > $@
