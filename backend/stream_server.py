from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import os

app = FastAPI()

# Path to downloaded file
FILE_PATH = "downloads/ubuntu-22.04.5-desktop-amd64.iso"


def file_stream():
    with open(FILE_PATH, "rb") as f:
        while chunk := f.read(1024 * 1024):
            yield chunk


@app.get("/stream")
def stream_file():
    return StreamingResponse(
        file_stream(),
        media_type="application/octet-stream"
    )