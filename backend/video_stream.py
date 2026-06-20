from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import os

app = FastAPI()

VIDEO_PATH = "downloads/BigBuckBunny_124/Content/big_buck_bunny_720p_surround.mp4"

def get_file_size():
    return os.path.getsize(VIDEO_PATH)

def range_stream(start: int, end: int):
    with open(VIDEO_PATH, "rb") as f:
        f.seek(start)
        bytes_to_read = end - start + 1

        while bytes_to_read > 0:
            chunk_size = min(1024 * 1024, bytes_to_read)
            data = f.read(chunk_size)

            if not data:
                break

            yield data
            bytes_to_read -= len(data)

@app.get("/video")
def stream_video(request: Request):

    file_size = get_file_size()

    range_header = request.headers.get("range")

    if range_header:
        start, end = range_header.replace("bytes=", "").split("-")

        start = int(start)
        end = int(end) if end else file_size - 1

        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(end - start + 1),
            "Content-Type": "video/mp4",
        }

        return StreamingResponse(
            range_stream(start, end),
            status_code=206,
            headers=headers,
        )

    return StreamingResponse(
        range_stream(0, file_size - 1),
        media_type="video/mp4"
    )