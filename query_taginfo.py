#!/usr/bin/env python3

import taginfo
import json
import os

# create build dir
build_dir = "./build"
if not os.path.exists(build_dir):
    os.makedirs(build_dir)

# get all values of key traffic sign from taginfo
key    = "traffic_sign"
values = []
for entry in taginfo.query.values_of_key_with_data(key):
    # print(entry["value"])
    values += [entry]

# write result to a json file
with open(build_dir + "/taginfo.json", "w") as f:
    f.write(json.dumps(values))
