#!/usr/bin/env python3

import glob
import logging
import os
import re
import yaml
import json
import zipfile
import shutil


logging.basicConfig(level=logging.INFO)
build_dir = "./build"
min_count = 10
plugin_version = 1

# create build dir
if not os.path.exists(build_dir):
    os.makedirs(build_dir)

# extract traffic sign images
for zip_file in glob.glob("traffic_signs_preset_JOSM/??.zip"):
    logging.info(f"extracting traffic sign images from {zip_file}")
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        # List all files in the ZIP file
        all_files = zip_ref.namelist()

        # Filter files that belong to the specific directory
        files_to_extract = [file for file in all_files if file.startswith("traffic_signs/")]

        # Extract the filtered files
        for file in files_to_extract:
            zip_ref.extract(file, build_dir)

# read taginfo.json
taginfo_values = dict() # country code → values
with open(build_dir + "/taginfo.json") as f:
    for entry in json.loads(f.read()):
        if re.match("^..:.+$", entry["value"]) and entry["count"] >= min_count:
            country = entry["value"].split(":")[0]
            if not country in taginfo_values:
                taginfo_values[country] = []
            taginfo_values[country] += [entry]

# build plugins
for country in os.listdir(build_dir + "/traffic_signs"):
    if not country in taginfo_values or len(taginfo_values[country]) == 0:
        logging.warning(f"not building plugin for {country}")
        continue

    logging.info(f"building plugin for {country}")

    plugin_dir = build_dir + "/trafficsigns" + country.lower()
    images = dict() # value → image name

    # create plugin directory
    if not os.path.exists(plugin_dir):
        os.makedirs(plugin_dir)
    if not os.path.exists(plugin_dir + "/icons"):
        os.makedirs(plugin_dir + "/icons")

    # copy images to plugin directory
    for entry in taginfo_values[country]:
        image_name = entry["value"].replace(country + ":", country + "_")
        if os.path.exists(f"{build_dir}/traffic_signs/{country}/{image_name}.svg"):
            images[entry["value"]] = image_name + ".svg"
            shutil.copy(f"{build_dir}/traffic_signs/{country}/{image_name}.svg", f"{plugin_dir}/icons/{image_name}.svg")
        elif os.path.exists(f"{build_dir}/traffic_signs/{country}/{image_name}.png"):
            images[entry["value"]] = image_name + ".png"
            shutil.copy(f"{build_dir}/traffic_signs/{country}/{image_name}.png", f"{plugin_dir}/icons/{image_name}.png")
        elif os.path.exists(f"{build_dir}/traffic_signs/{country}/{image_name}.gif"):
            images[entry["value"]] = image_name + ".gif"
            shutil.copy(f"{build_dir}/traffic_signs/{country}/{image_name}.gif", f"{plugin_dir}/icons/{image_name}.gif")

    if len(os.listdir(f"{plugin_dir}/icons")) == 0:
        logging.warning(f"skipping plugin for {country} because no images were included")
        continue

    # create plugin.yaml
    plugin_yaml = dict()
    plugin_yaml["id"] = f"trafficsigns{country.lower()}"
    plugin_yaml["name"] = f"Traffic Signs {country}"
    plugin_yaml["version"] = plugin_version
    plugin_yaml["fields"] = {
        f"traffic_sign_{country.lower()}_i": {"type": "inlineCombo", "key": "traffic_sign", "label": "Sign", "options": [], "labels": []},
    }
    plugin_yaml["presets"] = {}
    plugin_yaml["modes"] = {"micro": {"markers": {}}}

    for value, image_name in images.items():
        preset = "traffic_sign_" + value.replace(":", "_").lower()
        plugin_yaml["fields"][f"traffic_sign_{country.lower()}_i"]["options"] += [value]
        plugin_yaml["fields"][f"traffic_sign_{country.lower()}_i"]["labels"] += [image_name]
        plugin_yaml["presets"][preset] = {"name": value, "icon": image_name, "tags": {"traffic_sign": value}, "fields": [f"traffic_sign_{country.lower()}_i", "direction"]}
        plugin_yaml["modes"]["micro"]["markers"][preset] = {"icon": image_name}

    with open(f"{plugin_dir}/plugin.yaml", "w") as f:
        yaml.dump(plugin_yaml, f, explicit_start=True)
    
    # zip plugin
    shutil.make_archive(f"{build_dir}/trafficsigns{country.lower()}", "zip", f"{build_dir}/trafficsigns{country.lower()}")
    os.rename(f"{build_dir}/trafficsigns{country.lower()}.zip", f"{build_dir}/trafficsigns{country.lower()}.edp")
