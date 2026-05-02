import json

from arcgis.features import FeatureLayer
from core.config import settings

feature_layer = FeatureLayer(f"{settings.PRORAIL_FEATURE_SERVER_WV}/8")
type = "Wisselverwarming"


# Query for unique values of "TEKENINGNAAM"
unique_query = feature_layer.query(
    out_fields="TEKENINGNAAM", return_distinct_values=True, return_geometry=False
)

# Extract the values into a list
unique_values = [
    feature.attributes["TEKENINGNAAM"] for feature in unique_query.features
]

unique_values = list(dict.fromkeys(unique_values))

dict_tekening = {"discipline": type, "tekeningnamen_all": unique_values}

print(len(dict_tekening["tekeningnamen_all"]))

with open(
    f"/home/boudewijn/Repos/KabelLeiding/app/data/output/jsons/{type}.json",
    "w",
) as file:
    json.dump(dict_tekening, file, indent=4)
