from . import data
import json

full_regions = json.loads(data.json_str)

province_city = {el["name"] : [city["name"] for city in el["city"]] for el in full_regions}
