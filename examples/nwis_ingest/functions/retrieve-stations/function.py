from typing import cast
import io
import csv
import json
import requests

import plausible as pbl

ALL_SITES_PARAMS = [
    ("data_type", "rt"),
    ("group_key", "NONE"),
    ("format", "sitefile_output"),
    ("sitefile_output_format", "rdb"),
    ("column_name", "site_no"),
    ("column_name", "site_tp_cd"),
    ("column_name", "dec_lat_va"),
    ("column_name", "dec_long_va"),
    ("column_name", "station_nm"),
    ("column_name", "tz_cd"),
    ("list_of_search_criteria", "data_type"),
]
NWIS_BASE_URL = "https://nwis.waterdata.usgs.gov/usa/nwis"


def handler():
    store = cast(pbl.function.outputs.fetcher, pbl.KeyValueStore)
    resp = requests.get(f"{NWIS_BASE_URL}/inventory", params=ALL_SITES_PARAMS)
    fp = io.StringIO(resp.text)
    rd = csv.DictReader(filter(lambda row: row[0] != "#", fp), delimiter="\t")
    next(rd)  # skip fields metadata line
    for record in [dict(x) for x in rd]:
        store.put(record)

