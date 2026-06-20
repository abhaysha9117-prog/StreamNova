"use client";

import { useEffect, useRef, useState } from "react";
import Hls from "hls.js";

interface Stream {
  quality: string;
  url: string;
}

interface Subtitle {
  label: string;
  url: string;
}

export default function PlayerControls({
  streams,
  subtitles
}: {
  streams: Stream[];
  subtitles: Subtitle[];
}) {

  const videoRef = useRef<HTMLVideoElement>(null);

  const [showMenu, setShowMenu] = useState(false);
  const [selectedSubtitle, setSelectedSubtitle] =
    useState("Off");

  // 🎬 Load HLS Stream
  useEffect(() => {

    if (streams.length === 0) return;

    const video = videoRef.current;

    if (!video) return;

    const url = streams[0].url;

    if (Hls.isSupported()) {

      const hls = new Hls();

      hls.loadSource(url);
      hls.attachMedia(video);

    } else {

      video.src = url;

    }

  }, [streams]);

  // 📝 Subtitle Control
  const changeSubtitle = (label: string) => {

    if (!videoRef.current) return;

    setSelectedSubtitle(label);

    const tracks =
      videoRef.current.textTracks;

    for (let i = 0; i < tracks.length; i++) {

      tracks[i].mode =
        tracks[i].label === label
          ? "showing"
          : "disabled";

    }

  };

  return (

    <div className="relative w-full">

      {/* 🎥 Video */}
      <video
        ref={videoRef}
        controls
        className="w-full rounded-xl"
      >

        {subtitles.map((sub, i) => (

          <track
            key={i}
            src={sub.url}
            kind="subtitles"
            label={sub.label}
            srcLang="en"
          />

        ))}

      </video>

      {/* ⋮ Menu Button */}
      <button
        onClick={() =>
          setShowMenu(!showMenu)
        }
        className="
          absolute
          bottom-4
          right-4
          bg-black/70
          text-white
          px-3
          py-1
          rounded-lg
        "
      >
        ⋮
      </button>

      {/* Menu */}
      {showMenu && (

        <div
          className="
            absolute
            bottom-14
            right-4
            bg-black/90
            text-white
            rounded-xl
            shadow-lg
            w-48
          "
        >

          <p className="px-4 py-2 text-sm opacity-70">
            Subtitles
          </p>

          <button
            onClick={() =>
              changeSubtitle("Off")
            }
            className="
              w-full
              text-left
              px-4
              py-2
              hover:bg-white/10
            "
          >
            Off
          </button>

          {subtitles.map((s, i) => (

            <button
              key={i}
              onClick={() =>
                changeSubtitle(s.label)
              }
              className="
                w-full
                text-left
                px-4
                py-2
                hover:bg-white/10
              "
            >
              {s.label}
            </button>

          ))}

        </div>

      )}

    </div>

  );
}