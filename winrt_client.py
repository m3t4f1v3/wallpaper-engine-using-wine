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
from winrt.windows.storage import StorageFile
from winrt.windows.storage.streams import RandomAccessStreamReference

# data looks like {"artist": "lectricworker", "title": "Ken Ishii 'Extra' - Music Video (HD)", "album": null, "thumbnail": "https://i.ytimg.com/vi/t6maVVFs0As/maxresdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLBLxodwp3ka3SDFzdEBz98ZSDjimw", "genre": [], "status": "Paused", "position": 218405592, "duration": 228886604, "rate": 1.0}



async def process_data(websocket, path):
    player = MediaPlayer()
    controls: SystemMediaTransportControls = player.system_media_transport_controls
    updater: SystemMediaTransportControlsDisplayUpdater = controls.display_updater
    timeline = SystemMediaTransportControlsTimelineProperties()
    controls.is_play_enabled = False
    controls.is_pause_enabled = False
    controls.is_next_enabled = False
    controls.is_previous_enabled = False
    updater.type = MediaPlaybackType.MUSIC
    async for message in websocket:
        data = json.loads(message)
        # i WISH there was match case support
        if data["status"] == "Playing":
            controls.media_playback_status = MediaPlaybackStatus.PLAYING
        else:
            controls.media_playback_status = MediaPlaybackStatus.PAUSED
        updater.music_properties.title = data["title"]
        updater.music_properties.artist = data["artist"]
        updater.music_properties.album_title = data["album"]
        updater.music_properties.genres.append(**data["genre"])
        updater.thumbnail = RandomAccessStreamReference.create_from_uri(
            Uri(data["thumbnail"])
        )
        timeline.end_time = datetime.timedelta(milliseconds=data["duration"])
        timeline.position = datetime.timedelta(milliseconds=data["position"])
        updater.update()
        # if playing then update position
        


# async def set(websocket):
#     async for message in websocket:
#         # print(f"Received: {message}")
#         music_data = message


async def main():
    start_server = websockets.serve(process_data, "localhost", 8765)

    await asyncio.gather(start_server, loop.create_future())

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
