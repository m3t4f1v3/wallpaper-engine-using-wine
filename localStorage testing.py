import json

from hashlib import sha1

filename = "/media/Other/SteamLibrary/steamapps/common/wallpaper_engine/bin/scenestorage/3d110c66eecaab73558797ce9ddf3053e85da39e.bin"

songData = {
    "title": "4 am",
    "artist": "stuff",
    "contentType": "music",
    "albumTitle": "things",
    "subTitle": "stuff",
    "albumArtists": "things",
    # "genres": "stuff",
    "duration": 123,
    "position": 0,
    "paused": False,
}

info = f"LSKV0001{json.dumps(songData, separators=(',', ':'))}".encode()

with open(filename, "wb") as f:
    f.write(
        # 641bc82e3591bbd292e3bb6d886f0b4447bb192d = sha1("songData")
        "LSBK0001".encode()
        + b"\x01\x00\x00\x00"
        + sha1('songData'.encode()).hexdigest().encode()
        + len(info).to_bytes(4, "little")
        + info
    )
