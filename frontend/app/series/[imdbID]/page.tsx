"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";

export default function SeriesPage() {

  const params = useParams();

  const imdbID =
    typeof params?.imdbID === "string"
      ? params.imdbID
      : "";

  const [seasons, setSeasons] =
    useState<any[]>([]);



  useEffect(() => {

    async function loadEpisodes() {

      const res =
        await fetch(
          `https://streamnova-qgog.onrender.com/episodes/${imdbID}`
        );

      const data =
        await res.json();

      setSeasons(data.seasons);

    }

    if (imdbID)
      loadEpisodes();

  }, [imdbID]);



  return (

    <div className="p-4">

      <h1 className="text-2xl font-bold mb-4">

        Seasons

      </h1>

      {seasons.map((season) => (

        <div
          key={season.season}
          className="mb-6"
        >

          <h2 className="text-xl font-semibold mb-2">

            Season {season.season}

          </h2>

          <div className="grid gap-2">

            {season.episodes.map(
              (ep: any) => (

              <Link
                key={ep.episode}
                href={`/watch/${ep.imdbID}`}
              >

                <div className="
                  p-3
                  bg-gray-800
                  text-white
                  rounded
                  hover:bg-gray-700
                ">

                  Episode {ep.episode} — {ep.title}

                </div>

              </Link>

            ))}

          </div>

        </div>

      ))}

    </div>

  );

}