"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

interface Movie {
  title: string;
  year: string;
  poster: string;
  imdbID: string;
}

export default function Home() {

  const [query, setQuery] = useState("");

  const [results, setResults] =
    useState<Movie[]>([]);

  const [continueList, setContinueList] =
    useState<Movie[]>([]);

  const [trending, setTrending] =
    useState<Movie[]>([]);

  const [genres, setGenres] =
    useState<{ [key: string]: Movie[] }>({});

    const [torrentFile, setTorrentFile] =
  useState<File | null>(null);

const [uploading, setUploading] =
  useState(false);

  // ==========================
// Player State
// ==========================

const [videoUrl, setVideoUrl] = useState("");
const [subtitleUrl, setSubtitleUrl] = useState("");

  // ==========================
// Provider States
// ==========================

const [providerQuery, setProviderQuery] = useState("");

const [providerResults, setProviderResults] = useState<any[]>([]);

const [episodes, setEpisodes] = useState<any[]>([]);

  // 🔎 Search Movies

  async function uploadTorrent() {

  if (!torrentFile) {

    alert("Select a torrent file");

    return;

  }

  try {

    setUploading(true);

    const formData = new FormData();

    formData.append(
      "file",
      torrentFile
    );

    const response = await fetch(

      "http://127.0.0.1:8000/torrent/load_torrent",

      {

        method: "POST",

        body: formData,

      }

    );

    const data =
      await response.json();

    if (data.torrent_id) {

      window.open(

        `http://127.0.0.1:8000/torrent/player/${data.torrent_id}`,

        "_blank"

      );

    } else {

      alert("Torrent failed");

    }

  } catch (error) {

    console.error(
      "Torrent upload error:",
      error
    );

    alert("Upload failed");

  }

  setUploading(false);

}

  async function searchMovies() {

    if (!query) return;

    try {

      const res = await fetch(
        `http://127.0.0.1:8000/search?query=${query}`
      );

      const data = await res.json();

      const uniqueMap = new Map();

      data.results.forEach((movie: Movie) => {

        if (!uniqueMap.has(movie.imdbID)) {

          uniqueMap.set(
            movie.imdbID,
            movie
          );

        }

      });

      setResults(
        Array.from(uniqueMap.values())
      );

    } catch (error) {

      console.error(
        "Search error:",
        error
      );

    }

  }

  // ==========================
// Provider Search
// ==========================

async function providerSearch() {

  if (!providerQuery) return;

  const res = await fetch(
    `http://127.0.0.1:8000/provider/search?query=${providerQuery}`
  );

  const data = await res.json();

  setProviderResults(data);

}

// ==========================
// Load Episodes
// ==========================

async function loadEpisodes(id: string) {

  const res = await fetch(
    `http://127.0.0.1:8000/provider/episodes?item_id=${id}`
  );

  const data = await res.json();

  console.log("Episodes response:", data);

  // ✅ Fix — handle both formats
  if (Array.isArray(data)) {

    setEpisodes(data);

  } else if (Array.isArray(data.episodes)) {

    setEpisodes(data.episodes);

    } else {

      setEpisodes([]);

    }

  }

// ==========================
// Play Episode
// ==========================

async function playEpisode(
  id: string,
  provider: string
) {

  const res = await fetch(
    `http://127.0.0.1:8000/provider/streams?item_id=${id}&provider=${provider}`
  );

  const data = await res.json();

  if (data?.streams?.length > 0) {

    setVideoUrl(
      data.streams[0].url
    );

  }

}

{/* ========================== */}
{/* Video Player */}
{/* ========================== */}

{videoUrl && (

  <div className="mt-8">

    <h2 className="text-xl mb-2">
      🎬 Now Playing
    </h2>

    <video
      controls
      autoPlay
      className="w-full max-w-4xl"
    >

      <source
        src={videoUrl}
        type="application/x-mpegURL"
      />

      {subtitleUrl && (

        <track
          src={subtitleUrl}
          kind="subtitles"
          label="English"
          default
        />

      )}

    </video>

  </div>

)}

  // ▶ Continue Watching

  async function loadContinueWatching() {

    try {

      const res = await fetch(
        "http://127.0.0.1:8000/watch/list"
      );

      const data = await res.json();

      setContinueList(data);

    } catch (error) {

      console.error(
        "Continue watching error:",
        error
      );

    }

  }

  // 🔥 Trending

  async function loadTrending() {

    try {

      const queries = [
        "batman",
        "avengers",
        "spiderman"
      ];

      let uniqueMap = new Map();

      for (const q of queries) {

        const res = await fetch(
          `http://127.0.0.1:8000/search?query=${q}`
        );

        const data = await res.json();

        data.results.forEach((movie: Movie) => {

          if (!uniqueMap.has(movie.imdbID)) {

            uniqueMap.set(
              movie.imdbID,
              movie
            );

          }

        });

      }

      setTrending(
        Array.from(uniqueMap.values())
          .slice(0, 10)
      );

    } catch (error) {

      console.error(
        "Trending load error:",
        error
      );

    }

  }

  // 🎬 Genres

  async function loadGenres() {

    try {

      const genreQueries: {
        [key: string]: string
      } = {

        "🎬 Action": "action",
        "😂 Comedy": "comedy",
        "🚀 Sci-Fi": "sci-fi",
        "🎭 Drama": "drama"

      };

      let genreData: {
        [key: string]: Movie[]
      } = {};

      for (const genre in genreQueries) {

        const query =
          genreQueries[genre];

        const res = await fetch(
          `http://127.0.0.1:8000/search?query=${query}`
        );

        const data = await res.json();

        const uniqueMap = new Map();

        data.results.forEach(
          (movie: Movie) => {

            if (
              !uniqueMap.has(
                movie.imdbID
              )
            ) {

              uniqueMap.set(
                movie.imdbID,
                movie
              );

            }

          }
        );

        genreData[genre] =
          Array.from(
            uniqueMap.values()
          ).slice(0, 10);

      }

      setGenres(genreData);

    } catch (error) {

      console.error(
        "Genre load error:",
        error
      );

    }

  }

  // Load Everything

  useEffect(() => {

    loadContinueWatching();
    loadTrending();
    loadGenres();

  }, []);

  return (

    <div className="min-h-screen bg-gray-100 p-6">

      {/* Title */}

      <h1 className="text-4xl font-bold mb-6">
        🎬 StreamNova
      </h1>

      {/* 🎬 Torrent Upload */}

<div className="mb-8 flex items-center gap-3">

  <input
    type="file"
    accept=".torrent"
    onChange={(e) => {

      if (e.target.files) {

        setTorrentFile(
          e.target.files[0]
        );

      }

    }}
  />

  <button

    onClick={uploadTorrent}

    disabled={uploading}

    className="bg-green-600 text-white px-5 py-2 rounded hover:bg-green-700"

  >

    {uploading

      ? "Uploading..."

      : "🎬 Stream Torrent"}

  </button>

</div>

      {/* ▶ Continue Watching */}

      {continueList.length > 0 && (

        <div className="mb-10">

          <h2 className="text-2xl font-bold mb-4">
            ▶ Continue Watching
          </h2>

          <div className="flex gap-6 overflow-x-auto pb-2">

            {continueList.map((movie) => (

              <Link
                key={movie.imdbID}
                href={`/watch/${movie.imdbID}`}
                className="flex-shrink-0 w-[180px]"
              >

                <div className="bg-white rounded-lg shadow overflow-hidden hover:scale-105 transition">

                  <img
  src={
    movie.poster &&
    movie.poster !== "N/A"
      ? movie.poster
      : "/no-poster.png"
  }
  alt={movie.title}
  className="w-full h-[270px] object-cover"
/>

                  <div className="p-2">

                    <p className="text-sm font-medium line-clamp-2">
                      {movie.title}
                    </p>

                  </div>

                </div>

              </Link>

            ))}

          </div>

        </div>

      )}

      {/* 🔥 Trending */}

      {trending.length > 0 && (

        <div className="mb-10">

          <h2 className="text-2xl font-bold mb-4">
            🔥 Trending
          </h2>

          <div className="flex gap-6 overflow-x-auto pb-2">

            {trending.map((movie, index) => (

  <Link
    key={movie.imdbID || index}
    href={`/movie/${movie.imdbID || "N/A"}`}
    className="flex-shrink-0 w-[180px]"
              >

                <div className="bg-white rounded-lg shadow overflow-hidden hover:scale-105 transition">

                  <img
                    src={movie.poster}
                    alt={movie.title}
                    className="w-full h-[270px] object-cover"
                  />

                  <div className="p-2">

                    <p className="text-sm font-medium line-clamp-2">
                      {movie.title}
                    </p>

                  </div>

                </div>

              </Link>

            ))}

          </div>

        </div>

      )}

      {/* 🎬 Genre Rows */}

      {Object.keys(genres).map((genre) => (

        <div
          key={genre}
          className="mb-10"
        >

          <h2 className="text-2xl font-bold mb-4">
            {genre}
          </h2>

          <div className="flex gap-6 overflow-x-auto pb-2">

            {genres[genre].map((movie) => (

              <Link
                key={`${genre}-${movie.imdbID}`}
                href={`/movie/${movie.imdbID}`}
                className="flex-shrink-0 w-[180px]"
              >

                <div className="bg-white rounded-lg shadow overflow-hidden hover:scale-105 transition">

                  <img
                    src={movie.poster}
                    alt={movie.title}
                    className="w-full h-[270px] object-cover"
                  />

                  <div className="p-2">

                    <p className="text-sm font-medium line-clamp-2">
                      {movie.title}
                    </p>

                  </div>

                </div>

              </Link>

            ))}

          </div>

        </div>

      ))}

      {/* 🔎 Search */}

      <div className="mb-6 flex">

        <input
          type="text"
          placeholder="Search movies..."
          className="border p-3 mr-2 rounded w-72"
          value={query}
          onChange={(e) =>
            setQuery(e.target.value)
          }
        />

        <button
          className="bg-blue-600 text-white px-5 py-3 rounded hover:bg-blue-700"
          onClick={searchMovies}
        >
          Search
        </button>

      </div>


      {/* ========================== */}
{/* Provider Search */}
{/* ========================== */}

<div className="mb-6">

  <h2 className="text-xl mb-2">
    🔎 Provider Search
  </h2>

  <input
    type="text"
    placeholder="Search anime or series..."
    value={providerQuery}
    onChange={(e) =>
      setProviderQuery(e.target.value)
    }
    className="text-black px-3 py-2 mr-2"
  />

  <button
    onClick={providerSearch}
    className="bg-purple-600 px-4 py-2 rounded"
  >
    Search Provider
  </button>

</div>


{/* Provider Results */}

<div className="mb-6">

  {providerResults.map((item, i) => (

    <div
      key={item.id || i}
      className="cursor-pointer mb-2 hover:text-yellow-400"
      onClick={() =>
        loadEpisodes(item.id)
      }
    >

      🎬 {item.title}

    </div>

  ))}

</div>


{/* Episodes */}

<div>

  {Array.isArray(episodes) &&
  episodes.map((ep, i) => (

    <div
      key={ep.id || i}
      className="cursor-pointer mb-2 hover:text-green-400"
      onClick={() =>
        playEpisode(ep.id, ep.provider)
      }
    >

      ▶ {ep.title}

    </div>

  ))}

</div>

      {/* 🎬 Search Results */}

      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6">

        {results.map((movie, index) => (

           <div
            key={movie.imdbID || index}
            className="relative group bg-white rounded shadow overflow-hidden hover:scale-105 transition"
          >

            <img
              src={movie.poster}
              alt={movie.title}
              className="w-full h-[270px] object-cover"
            />

            <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 flex flex-col items-center justify-center gap-3 transition">

              <Link
                href={`/watch/${movie.imdbID}`}
                className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
              >
                ▶ Play
              </Link>

              <Link
                href={`/movie/${movie.imdbID}`}
                className="bg-gray-700 text-white px-4 py-2 rounded hover:bg-gray-600"
              >
                ℹ Details
              </Link>

            </div>

            <div className="p-2">

              <p className="text-sm font-medium line-clamp-2">
                {movie.title}
              </p>

              <p className="text-xs text-gray-500">
                {movie.year}
              </p>

            </div>

          </div>

        ))}

      </div>

    </div>

  );
}