import asyncio

from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
)

from winrt.windows.foundation.collections import IVectorView
# from winrt.windows.storage.streams import (
#     IRandomAccessStreamReference,
#     RandomAccessStreamReference,
# )
# from winrt.windows.foundation import Uri


async def get_media_info():
    print("Getting media info...")
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:  # there needs to be a media session running
        print(current_session.source_app_user_model_id)
        # if current_session.source_app_user_model_id == TARGET_ID:
        info = await current_session.try_get_media_properties_async()
        info_dict = {}
        for song_attr in dir(info):
            if song_attr[0] != "_" and song_attr != "playback_type":
                # check if its an IVectorView
                if isinstance(getattr(info, song_attr), IVectorView):
                    # convert IVectorView to list
                    info_dict[song_attr] = list(getattr(info, song_attr))
                # elif isinstance(getattr(info, song_attr), IRandomAccessStreamReference):
                #     info_dict[song_attr] = getattr(info, song_attr)
                else:
                    info_dict[song_attr] = getattr(info, song_attr)
        return info_dict


if __name__ == "__main__":
    current_media_info = asyncio.run(get_media_info())
    print(current_media_info)
