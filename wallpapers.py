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

steam_folder = "/media/Other/SteamLibrary/steamapps"


wallpaper_mapping = {
    # "Left": {
    #     "dimensions": [1920, 1080],
    #     "id": f"{steam_folder}/common/wallpaper_engine/projects/myprojects/sailingthroughthestars/scene.json",
    #     "preset": None,
    # },
    "Middle": {"dimensions": [2560, 1080], "id": 2972092654, "preset": None},
    "Right": {
        "dimensions": [1920, 1080],
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
}

for index, (position, data) in enumerate(wallpaper_mapping.items()):
    file = ""
    print(f"Starting {position} wallpaper")
    if isinstance(data["id"], str):
        file = data["id"]
    else:
        wrapper_folder = os.path.join(
            steam_folder, "workshop", "content", "431960", f"wrapper_{position}"
        )
        file = os.path.join(wrapper_folder, "project.json")
        config = copy.deepcopy(default_config)  # is this needed?

        config["dependency"] = str(data["id"])

        if data.get("preset"):
            config["preset"].update(data["preset"])

        # write config to file
        with open(f"/tmp/wrapper_{position}.json", "w") as f:  # tiny memory cost
            f.write(json.dumps(config))

        # make sure steam/workshop/content/431960/wrapper_Position/ exists

        if not os.path.exists(wrapper_folder):
            os.makedirs(wrapper_folder)
            os.symlink(
                f"/tmp/wrapper_{position}.json",
                file,
            )
    # wonder why i'm doing this? wine devs cant be assed to implement SetCurrentProcessExplicitAppUserModelID and neither can i
    # nor can they be assed to implement media controls, so i have to resort to this for BOTH of my problems
    subprocess.Popen(
        f"wine {steam_folder}/common/wallpaper_engine/wallpaper32.exe -control openWallpaper -file {file} -playInWindow \"Wallpaper Engine {position}\" -borderless -width {data['dimensions'][0]} -height {data['dimensions'][1]}",
        shell=True,
        env=env,
        stderr=subprocess.DEVNULL,
    )
    if not index == len(wallpaper_mapping) - 1:
        time.sleep(3)  # cant be done in parallel for some reason
