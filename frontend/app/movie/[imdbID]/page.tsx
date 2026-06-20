"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";

interface Movie {
  Title: string;
  Year: string;
  Poster: string;
  Plot: string;
  Genre: string;
  Runtime: string;
  imdbRating: string;
}

export default function MoviePage() {

  const params = useParams();

  const imdbID =
    typeof params?.imdbID === "string"
      ? params.imdbID
      : Array.isArray(params?.imdbID)
      ? params.imdbID[0]
      : "";

  const [movie, setMovie] =
    useState<Movie | null>(null);

  const [loading, setLoading] =
    useState(true);



  // ⭐ Load Movie Details
  useEffect(() => {

    if (!imdbID) return;

    async function loadMovie() {

      try {

        const res = await fetch(
          `http://127.0.0.1:8000/movie/${imdbID}`
        );

        const data =
          await res.json();

        setMovie({
          Title: data.Title || data.title,
          Year: data.Year || data.year,
          Poster: data.Poster || data.poster,
          Plot: data.Plot || data.plot,
          Genre: data.Genre || data.genre,
          Runtime: data.Runtime || data.runtime,
          imdbRating: data.imdbRating || data.rating
        });

      } catch (err) {

        console.error(err);

      } finally {

        setLoading(false);

      }

    }

    loadMovie();

  }, [imdbID]);



  if (loading) {

    return (
      <div className="p-6">
        Loading movie...
      </div>
    );

  }



  if (!movie) {

    return (
      <div className="p-6">
        Movie not found
      </div>
    );

  }



  return (

    <div className="p-6">

      <div className="flex gap-6">

        {/* Poster */}
        <img
          src={
            movie.Poster &&
            movie.Poster !== "N/A"
              ? movie.Poster
              : "/no-poster.png"
          }
          alt={movie.Title}
          className="
            w-[220px]
            rounded-lg
            shadow-lg
          "
        />



        {/* Movie Info */}
        <div className="flex-1">

          <h1 className="
            text-4xl
            font-bold
          ">
            {movie.Title}
          </h1>



          <p className="
            mt-2
            text-gray-600
          ">

            {movie.Year}
            {" • "}
            {movie.Runtime}
            {" • "}
            ⭐ {movie.imdbRating}

          </p>



          <p className="
            mt-2
            text-gray-600
          ">
            {movie.Genre}
          </p>



          {/* Plot */}
          <p className="
            mt-4
            text-gray-700
          ">
            {movie.Plot}
          </p>



          {/* ⭐ BUTTONS ROW */}
          <div className="flex gap-4 mt-6">

            {/* ▶ Play Movie */}
            <Link
              href={`/watch/${imdbID}`}
            >

              <button
                className="
                  px-6
                  py-3
                  bg-red-600
                  hover:bg-red-700
                  text-white
                  text-lg
                  rounded-lg
                  shadow-lg
                "
              >

                ▶ Play Movie

              </button>

            </Link>



            {/* 📺 Play Series */}
            <Link
              href={`/series/${imdbID}`}
            >

              <button
                className="
                  px-6
                  py-3
                  bg-blue-600
                  hover:bg-blue-700
                  text-white
                  text-lg
                  rounded-lg
                  shadow-lg
                "
              >

                📺 Play Series

              </button>

            </Link>

          </div>

        </div>

      </div>

    </div>

  );

}