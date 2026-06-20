"use client";

import { useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import Hls from "hls.js";

interface Stream {
  quality: string;
  url: string;
}

export default function WatchPage() {

  const params = useParams();

  const imdbID =
    typeof params?.imdbID === "string"
      ? params.imdbID
      : Array.isArray(params?.imdbID)
      ? params.imdbID[0]
      : "";

  const videoRef =
    useRef<HTMLVideoElement>(null);

  const hlsRef =
    useRef<Hls | null>(null);

  const [streams, setStreams] =
    useState<Stream[]>([]);

  const [selectedStream, setSelectedStream] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [showMenu, setShowMenu] =
    useState(false);

  const [movieInfo, setMovieInfo] =
    useState<any>(null);



  // ⭐ Load Streams + Movie Info
  useEffect(() => {

    if (!imdbID) return;

    async function loadStreams() {

      try {

        // Streams
        const res = await fetch(
          `http://127.0.0.1:8000/watch/streams/${imdbID}`
        );

        const data =
          await res.json();

        if (data.streams.length > 0) {

          setStreams(data.streams);

          setSelectedStream(
            data.streams[0].url
          );

        }



        // Movie info
        const movieRes =
          await fetch(
            `http://127.0.0.1:8000/movie/${imdbID}`
          );

        const movieData =
          await movieRes.json();

        setMovieInfo(movieData);



      } catch (err) {

        console.error(err);

      } finally {

        setLoading(false);

      }

    }

    loadStreams();

  }, [imdbID]);



  // ⭐ Setup HLS
  useEffect(() => {

    const video = videoRef.current;

    if (!video || !selectedStream)
      return;

    if (hlsRef.current) {

      hlsRef.current.destroy();

    }

    if (Hls.isSupported()) {

      const hls = new Hls();

      hls.loadSource(
        selectedStream
      );

      hls.attachMedia(video);

      hlsRef.current = hls;

    }

    else {

      video.src =
        selectedStream;

    }

  }, [selectedStream]);



  // ⭐ Resume Playback
  useEffect(() => {

    async function resumePlayback() {

      try {

        const res =
          await fetch(
            "http://127.0.0.1:8000/watch/list"
          );

        const history =
          await res.json();

        const movie =
          history.find(
            (m: any) =>
              m.imdbID === imdbID
          );

        if (
          movie &&
          videoRef.current
        ) {

          videoRef.current.onloadedmetadata =
            () => {

              videoRef.current!.currentTime =
                movie.progress;

            };

        }

      } catch (err) {

        console.log(
          "Resume error",
          err
        );

      }

    }

    if (selectedStream) {

      resumePlayback();

    }

  }, [selectedStream]);



  // ⭐ Save Progress
  function saveProgress() {

    if (
      !videoRef.current ||
      !movieInfo
    ) return;

    const progress =
      Math.floor(
        videoRef.current.currentTime
      );

    if (progress < 5) return;

    fetch(
      "http://127.0.0.1:8000/watch/save",
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json"
        },

        body: JSON.stringify({

          imdbID,

          title:
            movieInfo?.Title ||
            movieInfo?.title ||
            "Unknown",

          poster:
            movieInfo?.Poster ||
            movieInfo?.poster ||
            "/no-poster.png",

          progress

        })

      }

    );

  }



  // ⭐ Change Quality
  function changeQuality(url: string) {

    setSelectedStream(url);

    setShowMenu(false);

  }



  return (

    <div className="p-4">

      {loading && (
        <p>
          Loading streams...
        </p>
      )}

      {!loading &&
        selectedStream && (

        <div className="relative">

          {/* ⭐ Three-dot menu */}
          <button
            onClick={() =>
              setShowMenu(!showMenu)
            }
            className="
              absolute
              top-3
              right-3
              z-40
              bg-black/60
              text-white
              px-2
              py-1
              rounded
            "
          >

            ⋮

          </button>



          {/* ⭐ Quality Menu */}
          {showMenu && (

            <div className="
              absolute
              top-12
              right-3
              bg-black
              border
              rounded
              p-2
              z-50
            ">

              {streams.map((stream) => (

                <button
                  key={stream.quality + stream.provider}
                  onClick={() =>
                    changeQuality(
                      stream.url
                    )
                  }
                  className="
                    block
                    px-4
                    py-2
                    text-white
                    hover:bg-gray-700
                    w-full
                    text-left
                  "
                >

                  {stream.quality}

                </button>

              ))}

            </div>

          )}



          {/* ⭐ VIDEO WITH SUBTITLES */}
          <video
            ref={videoRef}
            controls
            className="w-full"
            onTimeUpdate={
              saveProgress
            }
          >

            {/* ⭐ Subtitle Track */}
            <track
              src="/subtitles/sample.vtt"
              kind="subtitles"
              srcLang="en"
              label="English"
              default
            />

          </video>

        </div>

      )}

    </div>

  );

}