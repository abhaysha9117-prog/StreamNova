from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import StreamingResponse, HTMLResponse
import libtorrent as lt
import os
import time
import json
import mimetypes

app = FastAPI()

DOWNLOAD_PATH = "downloads"

VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi"]

if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

# ===============================
# TORRENT SESSION SETTINGS
# ===============================

settings = {
    "listen_interfaces": "0.0.0.0:6881",
    "enable_dht": True,
    "enable_lsd": True,
    "enable_upnp": True,
    "enable_natpmp": True,
    "announce_to_all_trackers": True,
    "announce_to_all_tiers": True
}

session = lt.session(settings)

current_video_path = None
current_handle = None


# ===============================
# LOAD TORRENT API
# ===============================

@app.post("/load_torrent")
async def load_torrent(file: UploadFile = File(...)):

    global current_video_path
    global current_handle

    torrent_path = os.path.join(DOWNLOAD_PATH, file.filename)

    # Save torrent
    with open(torrent_path, "wb") as f:
        f.write(await file.read())

    print("Torrent saved:", torrent_path)

    # Load torrent
    info = lt.torrent_info(torrent_path)

    params = {
        "save_path": DOWNLOAD_PATH,
        "ti": info
    }

    handle = session.add_torrent(params)

    current_handle = handle

    # Sequential download
    handle.set_sequential_download(True)

    print("Waiting for metadata...")

    # SAFE METADATA WAIT (max 60 sec)
    for _ in range(60):

        s = handle.status()

        if s.has_metadata:
            break

        time.sleep(1)

    if not handle.status().has_metadata:
        return {"error": "Metadata timeout"}

    print("Metadata received!")

    info = handle.get_torrent_info()

    files = info.files()

    largest_size = 0
    video_path = None

    # Prefer MP4
    for i in range(files.num_files()):
        file_path = files.file_path(i)
        file_size = files.file_size(i)

        if file_path.endswith(".mp4"):

            if file_size > largest_size:
                largest_size = file_size
                video_path = file_path

    # Fallback video formats
    if video_path is None:

        for i in range(files.num_files()):
            file_path = files.file_path(i)
            file_size = files.file_size(i)

            if any(file_path.endswith(ext) for ext in VIDEO_EXTENSIONS):

                if file_size > largest_size:
                    largest_size = file_size
                    video_path = file_path

    if video_path is None:
        return {"error": "No video file found"}

    current_video_path = os.path.join(DOWNLOAD_PATH, video_path)

    print("Video selected:", current_video_path)

    return {
        "message": "Torrent loaded",
        "video_path": current_video_path
    }


# ===============================
# RANGE STREAM FUNCTION
# ===============================

def range_stream(start: int, end: int):

    while not os.path.exists(current_video_path):
        time.sleep(1)

    with open(current_video_path, "rb") as f:

        f.seek(start)

        bytes_to_read = end - start + 1

        while bytes_to_read > 0:

            chunk_size = min(1024 * 1024, bytes_to_read)

            data = f.read(chunk_size)

            if not data:
                time.sleep(0.5)
                continue

            yield data

            bytes_to_read -= len(data)


# ===============================
# VIDEO STREAM API
# ===============================

@app.get("/video")
def stream_video(request: Request):

    if current_video_path is None:
        return {"error": "No video loaded"}

    while not os.path.exists(current_video_path):
        time.sleep(1)

    file_size = os.path.getsize(current_video_path)

    mime_type, _ = mimetypes.guess_type(current_video_path)

    if not mime_type:
        mime_type = "video/mp4"

    range_header = request.headers.get("range")

    if range_header:

        start, end = range_header.replace("bytes=", "").split("-")

        start = int(start)

        end = int(end) if end else file_size - 1

        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(end - start + 1),
            "Content-Type": mime_type,
        }

        return StreamingResponse(
            range_stream(start, end),
            status_code=206,
            headers=headers,
        )

    return StreamingResponse(
        range_stream(0, file_size - 1),
        media_type=mime_type
    )


# ===============================
# PROGRESS API
# ===============================

@app.get("/progress")
def get_progress():

    if current_handle is None:
        return {"error": "No torrent loaded"}

    s = current_handle.status()

    return {
        "progress": round(s.progress * 100, 2),
        "download_speed_kb": round(s.download_rate / 1000, 2),
        "upload_speed_kb": round(s.upload_rate / 1000, 2),
        "peers": s.num_peers,
        "seeds": s.num_seeds,
        "state": str(s.state)
    }


# ===============================
# LIVE PROGRESS STREAM
# ===============================

@app.get("/progress_stream")
def progress_stream():

    def event_stream():

        while True:

            if current_handle is None:

                data = {
                    "error": "No torrent loaded"
                }

            else:

                s = current_handle.status()

                data = {
                    "progress": round(s.progress * 100, 2),
                    "download_speed_kb": round(s.download_rate / 1000, 2),
                    "upload_speed_kb": round(s.upload_rate / 1000, 2),
                    "peers": s.num_peers,
                    "seeds": s.num_seeds,
                    "state": str(s.state)
                }

            yield f"data: {json.dumps(data)}\n\n"

            time.sleep(1)

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )


# ===============================
# VIDEO PLAYER PAGE
# ===============================

@app.get("/player", response_class=HTMLResponse)
def video_player():

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>StreamNova Player</title>
    </head>

    <body style="background:black; color:white; text-align:center;">

        <h2>🎬 StreamNova Player</h2>

        <video id="videoPlayer"
               width="800"
               controls
               autoplay>

            <source src="/video" type="video/mp4">

        </video>

        <br><br>

        <h3>📊 Live Progress</h3>

        <div id="progress">
            Waiting for torrent...
        </div>

<script>

const progressDiv = document.getElementById("progress");

const eventSource = new EventSource("/progress_stream");

eventSource.onmessage = function(event) {

    const data = JSON.parse(event.data);

    if (data.error) {

        progressDiv.innerHTML = "Waiting for torrent...";

        return;
    }

    progressDiv.innerHTML =
        "Progress: " + data.progress + "% | " +
        "Speed: " + data.download_speed_kb + " KB/s | " +
        "Peers: " + data.peers;

};

</script>

    </body>
    </html>
    """

    return HTMLResponse(content=html_content)