import asyncio


async def add_video_file_to_encoding_queue(video_id, video_file):
    await asyncio.sleep(1)
    print(f'Added video file {video_file} to encoding queue')
    return True
