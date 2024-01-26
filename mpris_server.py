from dbus_next.aio import MessageBus

import asyncio
import websockets
import json

loop = asyncio.get_event_loop()


def dbus_to_dict(dbus_dict):
    return {k: v.value for k, v in dbus_dict.items()}


def list_to_natural_string(l):
    if len(l) == 1:
        return l[0]
    elif len(l) == 2:
        return f"{l[0]} and {l[1]}"
    else:
        return ", ".join(l[:-1]) + f", and {l[-1]}"


def handle_thumbnail_url(url):
    if url.startswith("https://i.ytimg.com"):
        return url.replace("hqdefault", "maxresdefault")
    else:
        return url


async def main():
    bus = await MessageBus().connect()
    # the introspection xml would normally be included in your project, but
    # this is convenient for development
    introspection = await bus.introspect(
        "org.mpris.MediaPlayer2.plasma-browser-integration", "/org/mpris/MediaPlayer2"
    )

    obj = bus.get_proxy_object(
        "org.mpris.MediaPlayer2.plasma-browser-integration",
        "/org/mpris/MediaPlayer2",
        introspection,
    )
    player = obj.get_interface("org.mpris.MediaPlayer2.Player")
    properties = obj.get_interface("org.freedesktop.DBus.Properties")

    # call methods on the interface (this causes the media player to play)
    # await player.call_play()

    # volume = await player.get_volume()
    # print(f'current volume: {volume}, setting to 0.5')

    # await player.set_volume(0.5)
    # print(dir(player))

    # listen to signals

    async def on_properties_changed(
        interface_name, changed_properties, invalidated_properties
    ):
        for changed, variant in changed_properties.items():
            # print(changed)
            # print(variant.value)
            # spams too much
            data = dbus_to_dict(await player.get_metadata())
            # old_metadata = variant.value
            # find duration
            useful = {
                "artist": list_to_natural_string(data["xesam:artist"])
                if "xesam:artist" in data
                else None,
                "title": data["xesam:title"] if "xesam:title" in data else None,
                "album": data["xesam:album"] if "xesam:album" in data else None,
                "thumbnail": handle_thumbnail_url(data["mpris:artUrl"])
                if "mpris:artUrl" in data
                else None,
                "genre": [],  # todo lyric fetching (will be hard)
                "status": await player.get_playback_status(),
                "position": await player.get_position(),
                "duration": data["mpris:length"] if "mpris:length" in data else None,
                # "volume": await player.get_volume(), # unneeded for my use case
                "rate": await player.get_rate(),
            }
            async with websockets.connect("ws://localhost:8765") as websocket:
                await websocket.send(json.dumps(useful))

            # print(f'property changed: {changed} - {variant.value}')

    properties.on_properties_changed(on_properties_changed)

    async def listen_websocket(websocket, path):
        async for message in websocket:
            print(f"Received WebSocket message: {message}")

    start_server = websockets.serve(listen_websocket, "localhost", 8766)

    await asyncio.gather(start_server, loop.create_future())


loop.run_until_complete(main())
