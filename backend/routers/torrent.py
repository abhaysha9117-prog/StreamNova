from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import StreamingResponse, HTMLResponse
import libtorrent as lt
import os
import time
import json
import mimetypes
import uuid

router = APIRouter()

DOWNLOAD_PATH = "downloads"

VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi"]

os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# ===============================
# TORRENT SESSION
# ===============================

settings = {
    "listen_interfaces": "0.0.0.0:6881",
    "enable_dht": True,
    "enable_lsd": True,
    "enable_upnp": True,
    "enable_natpmp": True
}

session = lt.session(settings)

torrents = {}

RESUME_FILE = "torrent_resume.json"

# Load saved torrents

# ===============================
# LOAD RESUME FILE SAFELY
# ===============================

saved_data = {}

if os.path.exists(RESUME_FILE):

    try:

        with open(RESUME_FILE, "r") as f:

            content = f.read().strip()

            if content:

                saved_data = json.loads(content)

            else:

                saved_data = {}

    except Exception as e:

        print(f"⚠ Resume load error: {e}")

        saved_data = {}

else:

    with open(RESUME_FILE, "w") as f:

        json.dump({}, f)

    saved_data = {}

# ===============================
# LOAD TORRENT
# ===============================

@router.post("/load_torrent")
async def load_torrent(file: UploadFile = File(...)):

    torrent_id = str(uuid.uuid4())

    torrent_path = os.path.join(
        DOWNLOAD_PATH,
        f"{torrent_id}_{file.filename}"
    )

    with open(torrent_path, "wb") as f:
        f.write(await file.read())

    info = lt.torrent_info(torrent_path)

    params = {
        "save_path": DOWNLOAD_PATH,
        "ti": info
    }

    handle = session.add_torrent(params)

    handle.set_sequential_download(True)

    print("Waiting metadata...")

    for _ in range(60):

        if handle.status().has_metadata:
            break

        time.sleep(1)

    if not handle.status().has_metadata:
        return {"error": "Metadata timeout"}

    info = handle.get_torrent_info()

    files = info.files()

    video_candidates = []

    for i in range(files.num_files()):

        file_path = files.file_path(i)
        file_size = files.file_size(i)

        if file_path.lower().endswith(
            (".mp4", ".mkv", ".avi")
        ):

            video_candidates.append(
                (file_path, file_size)
            )

    if not video_candidates:
        return {"error": "No video file found"}

    # Prefer MP4 > MKV > AVI
    video_candidates.sort(
        key=lambda x: (
            0 if x[0].endswith(".mp4")
            else 1 if x[0].endswith(".mkv")
            else 2,
            -x[1]
        )
    )

    video_path = video_candidates[0][0]

    full_video_path = os.path.join(
        DOWNLOAD_PATH,
        video_path
    )

    torrents[torrent_id] = {
        "handle": handle,
        "video_path": full_video_path,
        "name": video_path
    }


    # ===============================
# LOAD MAGNET LINK
# ===============================

@router.post("/load_magnet")
async def load_magnet(magnet: str):

    torrent_id = str(uuid.uuid4())

    print("🔗 Loading magnet...")

    params = {
        "save_path": DOWNLOAD_PATH
    }

    handle = lt.add_magnet_uri(
        session,
        magnet,
        params
    )

    handle.set_sequential_download(True)

    print("⏳ Waiting metadata...")

    for _ in range(120):

        s = handle.status()

        if s.has_metadata:
            break

        time.sleep(1)

    if not handle.status().has_metadata:

        return {
            "error": "Magnet metadata timeout"
        }

    info = handle.get_torrent_info()

    files = info.files()

    video_candidates = []

    for i in range(files.num_files()):

        file_path = files.file_path(i)

        file_size = files.file_size(i)

        if file_path.lower().endswith(
            (".mp4", ".mkv", ".avi")
        ):

            video_candidates.append(
                (file_path, file_size)
            )

    if not video_candidates:

        return {
            "error": "No video file found"
        }

    video_candidates.sort(

        key=lambda x: (

            0 if x[0].endswith(".mp4")

            else 1 if x[0].endswith(".mkv")

            else 2,

            -x[1]

        )

    )

    video_path = video_candidates[0][0]

    full_video_path = os.path.join(
        DOWNLOAD_PATH,
        video_path
    )

    torrents[torrent_id] = {

        "handle": handle,

        "video_path": full_video_path,

        "name": video_path

    }

    return {

        "message": "Magnet loaded",

        "torrent_id": torrent_id,

        "video": video_path

    }

    # ===============================
    # SAVE RESUME DATA
    # ===============================

    saved_data[torrent_id] = {
        "torrent_file": torrent_path,
        "video_path": full_video_path
    }

    with open(RESUME_FILE, "w") as f:
        json.dump(saved_data, f)

    return {
        "message": "Torrent loaded",
        "torrent_id": torrent_id,
        "video": video_path
    }

# ===============================
# LIST TORRENTS
# ===============================

@router.get("/torrents")
def list_torrents():

    result = []

    for tid, data in torrents.items():

        result.append({
            "id": tid,
            "name": data["name"]
        })

    return result

# ===============================
# RANGE STREAM
# ===============================

def range_stream(path, start, end):

    while not os.path.exists(path):
        time.sleep(1)

    with open(path, "rb") as f:

        f.seek(start)

        bytes_to_read = end - start + 1

        while bytes_to_read > 0:

            chunk = f.read(
                min(1024 * 1024, bytes_to_read)
            )

            if not chunk:
                time.sleep(0.5)
                continue

            yield chunk

            bytes_to_read -= len(chunk)

# ===============================
# VIDEO STREAM
# ===============================

@router.get("/video/{torrent_id}")
def stream_video(torrent_id: str, request: Request):

    if torrent_id not in torrents:
        return {"error": "Invalid torrent id"}

    path = torrents[torrent_id]["video_path"]

    while not os.path.exists(path):
        time.sleep(1)

    file_size = os.path.getsize(path)

    mime_type, _ = mimetypes.guess_type(path)

    if path.endswith(".avi"):
        mime_type = "video/x-msvideo"

    elif path.endswith(".mkv"):
        mime_type = "video/x-matroska"

    elif path.endswith(".mp4"):
        mime_type = "video/mp4"

    if not mime_type:
        mime_type = "video/mp4"

    range_header = request.headers.get("range")

    if range_header:

        start, end = range_header.replace(
            "bytes=", ""
        ).split("-")

        start = int(start)
        end = int(end) if end else file_size - 1

        headers = {
            "Content-Range":
                f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length":
                str(end - start + 1),
            "Content-Type": mime_type,
            "Content-Disposition": "inline"
        }

        return StreamingResponse(
            range_stream(path, start, end),
            status_code=206,
            headers=headers
        )

    headers = {
        "Content-Type": mime_type,
        "Content-Disposition": "inline"
    }

    return StreamingResponse(
        range_stream(path, 0, file_size - 1),
        headers=headers
    )

# ===============================
# PROGRESS STREAM
# ===============================

@router.get("/progress_stream/{torrent_id}")
def progress_stream(torrent_id: str):

    def event_stream():

        while True:

            if torrent_id not in torrents:

                data = {
                    "error": "Invalid torrent id"
                }

            else:

                handle = torrents[torrent_id]["handle"]

                s = handle.status()

                data = {
                    "progress":
                        round(s.progress * 100, 2),

                    "download_speed_kb":
                        round(s.download_rate / 1000, 2),

                    "peers":
                        s.num_peers
                }

            yield f"data: {json.dumps(data)}\n\n"

            time.sleep(1)

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )

# ===============================
# PLAYER
# ===============================

@router.get("/player/{torrent_id}",
            response_class=HTMLResponse)
def player(torrent_id: str):

    html = f"""

    <html>

    <body style="background:black;color:white;text-align:center;">

    <h2>🎬 StreamNova Player</h2>

    <video width="900" controls autoplay>

        <source src="/torrent/video/{torrent_id}">

    </video>

    <br><br>

    <div id="progress">Loading...</div>

<script>

const progressDiv =
    document.getElementById("progress");

const eventSource =
    new EventSource(
        "/torrent/progress_stream/{torrent_id}"
    );

eventSource.onmessage =
function(event) {{

    const data =
        JSON.parse(event.data);

    progressDiv.innerHTML =
        "Progress: " + data.progress + "% | " +
        "Speed: " +
        data.download_speed_kb +
        " KB/s | Peers: " +
        data.peers;

}};

</script>

    </body>

    </html>
    """

    return HTMLResponse(html)

# ===============================
# AUTO RESUME TORRENTS
# ===============================

for torrent_id, data in saved_data.items():

    torrent_file = data["torrent_file"]

    if os.path.exists(torrent_file):

        try:

            info = lt.torrent_info(torrent_file)

            params = {
                "save_path": DOWNLOAD_PATH,
                "ti": info
            }

            handle = session.add_torrent(params)

            handle.set_sequential_download(True)

            torrents[torrent_id] = {

                "handle": handle,

                "video_path": data["video_path"],

                "name": os.path.basename(
                    data["video_path"]
                )

            }

            print(
                f"✅ Resumed torrent: {torrent_id}"
            )

        except Exception as e:

            print(
                f"❌ Resume failed: {e}"
            )