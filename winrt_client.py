#!/usr/bin/env python
import asyncio
import websockets

import json

import datetime

from winrt.windows.foundation import Uri
from winrt.windows.media import (
    SystemMediaTransportControls,
    MediaPlaybackStatus,
    SystemMediaTransportControlsDisplayUpdater,
    MediaPlaybackType,
    SystemMediaTransportControlsTimelineProperties,
)
from winrt.windows.media.playback import MediaPlayer
from winrt.windows.storage.streams import RandomAccessStreamReference

# data looks like {"artist": "lectricworker", "title": "Ken Ishii 'Extra' - Music Video (HD)", "album": null, "thumbnail": "https://i.ytimg.com/vi/t6maVVFs0As/maxresdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLBLxodwp3ka3SDFzdEBz98ZSDjimw", "genre": [], "status": "Paused", "position": 218405592, "duration": 228886604, "rate": 1.0}

player = MediaPlayer()
controls: SystemMediaTransportControls = player.system_media_transport_controls
updater: SystemMediaTransportControlsDisplayUpdater = controls.display_updater
timeline = SystemMediaTransportControlsTimelineProperties()
controls.is_play_enabled = True
controls.is_pause_enabled = True
controls.is_next_enabled = True
controls.is_previous_enabled = True
updater.type = MediaPlaybackType.MUSIC
global prevUrl
prevUrl = ""

async def process_data(websocket, path):
    global prevUrl
    print("Process data start")
    
    async for message in websocket:
        print("Got Message")
        data = json.loads(message)
        print(data)
        #print(dir(controls))
        print(data["album"])
        controls.playback_status = MediaPlaybackStatus.PLAYING if data["status"] == "Playing" else MediaPlaybackStatus.PAUSED
        updater.music_properties.title = str(data["title"])
        updater.music_properties.artist = str(data["artist"])
        updater.music_properties.album_title = str(data["album"])
        #updater.music_properties.genres.append(**data["genre"])
        if data["thumbnail"] != prevUrl:
            print("Updating thumbnail")
            prevUrl = data["thumbnail"]
            updater.thumbnail = RandomAccessStreamReference.create_from_uri(
                Uri(data["thumbnail"])
            )
        
        timeline.end_time = datetime.timedelta(milliseconds=data["duration"])
        timeline.position = datetime.timedelta(milliseconds=data["position"])
        updater.update()
        controls.update_timeline_properties(timeline)
        # if playing then update position
        


# async def set(websocket):
#     async for message in websocket:
#         # print(f"Received: {message}")
#         music_data = message


async def main():
    start_server = websockets.serve(process_data, "localhost", 8765)

    await asyncio.gather(start_server, loop.create_future())

if __name__ == "__main__":
    print("Running server")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
