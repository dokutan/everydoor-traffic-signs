# everydoor-traffic-signs
[Every Door](https://github.com/Zverik/every_door) plugins for traffic signs (`traffic_sign=*`).

The plugins support one country each, and include traffic signs that appear at least 10 times in taginfo.

# Building
```sh
# clone the repo
git clone --recurse-submodules https://github.com/dokutan/everydoor-traffic-signs
cd everydoor-traffic-signs

# get all values for the traffic_sign key from taginfo
python query_taginfo.py

# build plugins
python build.py
```

# Installing
To easily install the plugins from the build directory, caddy can be used:
```sh
caddy file-server --root build
```
Then modify this link (replace `<PLUGINNAME>` with `trafficsigns*` and `<LOCAL>` with the hostname of your build system), select it and choose to open it in Every Door: `https://every-door.app/plugin/<PLUGINNAME>?url=https%3A%2F%2F<LOCAL>%2F<PLUGINNAME>.edp&update=true`

# TODO
- combinations of signs
- add other tags to the presets, e.g. `max_speed`

# Credits
-  [Traffic signs Preset for JOSM](https://github.com/yopaseopor/traffic_signs_preset_JOSM), this is the source for the images
-  [Every Door Plugin documentation](https://izv.ee/everydoor/plugins)
