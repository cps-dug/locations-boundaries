import json
import logging
import sys

from census_area import Census

logging.basicConfig(level=logging.DEBUG)

c = Census("ac94ba69718a7e1da4f89c6d218b8f6b5ae9ac49")

population = c.pl.state_place_block(
    ("NAME", "P1_001N", "P3_001N"), 17, 14000, return_geometry=True
)

json.dump(population, sys.stdout)
