import libtorrent as lt
import time
import os


class TorrentEngine:

    def __init__(self, download_path="downloads"):

        self.download_path = download_path

        # Create download folder
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        # Create session
        self.session = lt.session()

        # Stronger session settings
        settings = {
            "listen_interfaces": "0.0.0.0:6881",

            "enable_dht": True,
            "enable_lsd": True,
            "enable_upnp": True,
            "enable_natpmp": True,

            "announce_to_all_trackers": True,
            "announce_to_all_tiers": True,

            "connections_limit": 500,
            "peer_connect_timeout": 15,

            "active_downloads": 10,
            "active_limit": 20,
        }

        self.session.apply_settings(settings)

        # Add multiple DHT routers
        dht_nodes = [
            ("router.bittorrent.com", 6881),
            ("router.utorrent.com", 6881),
            ("dht.transmissionbt.com", 6881),
            ("router.bitcomet.com", 6881),
            ("dht.aelitis.com", 6881),
        ]

        for node in dht_nodes:
            self.session.add_dht_router(node[0], node[1])

        self.session.start_dht()

        print("Bootstrapping DHT...")
        time.sleep(10)

        print("Torrent session started")

    def add_magnet(self, magnet_link):

        # Large tracker list (IMPORTANT)
        trackers = [
            "udp://tracker.opentrackr.org:1337/announce",
            "udp://open.demonii.com:1337/announce",
            "udp://tracker.torrent.eu.org:451/announce",
            "udp://tracker.cyberia.is:6969/announce",
            "udp://tracker.moeking.me:6969/announce",
            "udp://tracker.openbittorrent.com:80/announce",
            "udp://open.stealth.si:80/announce",
            "udp://tracker.dler.org:6969/announce",
        ]

        # Attach trackers
        for t in trackers:
            magnet_link += "&tr=" + t

        params = {
            "save_path": self.download_path,
            "storage_mode":
                lt.storage_mode_t.storage_mode_sparse,
        }

        handle = lt.add_magnet_uri(
            self.session,
            magnet_link,
            params
        )

        print("Downloading Metadata...")

        start = time.time()

        while not handle.has_metadata():

            s = handle.status()

            print(
                "Peers:",
                s.num_peers,
                "| Download:",
                round(s.download_rate / 1000, 2),
                "kB/s"
            )

            # Timeout
            if time.time() - start > 600:
                print("Metadata timeout!")
                return None

            time.sleep(1)

        print("Metadata received!")

        info = handle.get_torrent_info()

        print("Torrent name:", info.name())

        print("Files:")

        for f in info.files():
            print("-", f.path)

        return handle

    def get_progress(self, handle):

        if handle is None:
            return None

        s = handle.status()

        return {
            "progress": round(s.progress * 100, 2),
            "download_rate":
                round(s.download_rate / 1000, 2),
            "num_peers": s.num_peers,
        }