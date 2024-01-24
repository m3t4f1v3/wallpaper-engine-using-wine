#!/usr/bin/env python3
import subprocess
import time
import os
import copy
import json


env = os.environ.copy()
env["WINEDEBUG"] = "-all"

default_config = {
    "dependency": "-1",
    "preset": {
        "_d0": None,
        "alignment": 0,
        "alignmentfliph": False,
        "alignmentposition": 65,
        "alignmentx": 50,
        "alignmenty": 50,
        "alignmentz": 100,
        "rate": 100,
        "schemecolor": "0 0 0",
        "wec_brs": 50,
        "wec_con": 50,
        "wec_e": False,
        "wec_hue": 50,
        "wec_sa": 50,
    },
}

wallpaper_mapping = {
    "Left": {"width": 1920, "id": 2225496361, "preset": None},
    "Middle": {
        "width": 2560,
        "id": 2853443143,
        "preset": {
            "artisttag": False,
            "artisttagcolor": "1 1 1",
            "audioeyes": True,
            "audioprocessing": True,
            "backgroundmovement": True,
            "backgroundtint1": "0 0 0",
            "bgtint": False,
            "bgtint1": 0.60000002,
            "blur1": 0.5,
            "clockformat": "0",
            "evamovement": True,
            "evatint": "1 1 1",
            "evatint1": False,
            "eyecolour": "1 0 0",
            "eyecolourtransparency": 0.5,
            "eyetint": False,
            "movingtext": True,
            "newproperty": "5",
            "pluginledextensionsenableleds": True,
            "rate": 100,
            "shaking": True,
            "textcolor": "1 1 1",
        },
    },
    "Right": {"width": 1920, "id": 2972092654, "preset": None},
}


steam_folder = "/media/Other/SteamLibrary/steamapps"

for index, (position, data) in enumerate(wallpaper_mapping.items()):
    print(f"Starting {position} wallpaper")
    config = copy.deepcopy(default_config)  # is this needed?

    config["dependency"] = str(data["id"])

    if data.get("preset"):
        config["preset"].update(data["preset"])

    # write config to file
    with open(f"/tmp/wrapper_{position}.json", "w") as f:  # tiny memory cost
        f.write(json.dumps(config))

    # make sure steam/workshop/content/431960/wrapper_Position/ exists

    if not os.path.exists(f"{steam_folder}/workshop/content/431960/wrapper_{position}"):
        os.makedirs(f"{steam_folder}/workshop/content/431960/wrapper_{position}")
        os.symlink(
            f"/tmp/wrapper_{position}.json",
            f"{steam_folder}/workshop/content/431960/wrapper_{position}/project.json",
        )

    subprocess.Popen(
        f"wine {steam_folder}/common/wallpaper_engine/wallpaper32.exe -control openWallpaper -file {steam_folder}/workshop/content/431960/wrapper_{position}/project.json -playInWindow \"Wallpaper Engine {position}\" -borderless -width {data['width']} -height 1080 -monitor {index}",
        shell=True,
        env=env,
    )
    if not index == len(wallpaper_mapping) - 1:
        time.sleep(5)
