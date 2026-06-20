"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface Movie {
  imdbID: string;
  title: string;
  poster: string;
  year: string;
}

export default function FavoritesPage() {
  const [favorites, setFavorites] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [removing, setRemoving] = useState<string | null>(null);

  const fetchFavorites = async () => {
    try {
      const res = await fetch("https://streamnova-qgog.onrender.com/favorites/list");
      setFavorites(await res.json());
    } catch {}
    setLoading(false);
  };

  const remove = async (id: string) => {
    setRemoving(id);
    try {
      await fetch(`https://streamnova-qgog.onrender.com/favorites/remove/${id}`, { method: "DELETE" });
      setFavorites(f => f.filter(m => m.imdbID !== id));
    } catch {}
    setRemoving(null);
  };

  useEffect(() => { fetchFavorites(); }, []);

  return (
    <div className="min-h-screen px-6 pt-28 pb-16" style={{ background: "var(--bg-primary)" }}>
      <div className="max-w-screen-2xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-white font-black" style={{ fontFamily: "var(--font-display)", fontSize: "36px", letterSpacing: "2px" }}>
            ❤️ My List
          </h1>
          {favorites.length > 0 && (
            <span className="text-sm px-3 py-1.5 rounded-lg" style={{ background: "var(--bg-elevated)", color: "var(--text-secondary)" }}>
              {favorites.length} title{favorites.length !== 1 ? "s" : ""}
            </span>
          )}
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-32">
            <div className="w-10 h-10 rounded-full border-4 border-t-transparent animate-spin" style={{ borderColor: "rgba(229,57,53,0.3)", borderTopColor: "var(--accent)" }} />
          </div>
        ) : favorites.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-32 gap-4">
            <span className="text-7xl">🎬</span>
            <p className="text-xl font-bold text-white">Nothing here yet</p>
            <p className="text-sm" style={{ color: "var(--text-secondary)" }}>Add movies and shows to your list to watch later.</p>
            <Link href="/" className="mt-4 px-6 py-3 rounded-xl font-bold text-white text-sm" style={{ background: "var(--accent)" }}>
              Browse Content
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-5">
            {favorites.map(movie => (
              <div key={movie.imdbID} className="group relative animate-fade-in">
                <Link href={`/movie/${movie.imdbID}`}>
                  <div
                    className="relative rounded-xl overflow-hidden cursor-pointer"
                    style={{
                      boxShadow: "0 4px 20px rgba(0,0,0,0.5)",
                      transition: "transform 0.25s ease, box-shadow 0.25s ease",
                    }}
                    onMouseEnter={e => { (e.currentTarget as HTMLElement).style.transform = "scale(1.04) translateY(-3px)"; (e.currentTarget as HTMLElement).style.boxShadow = "0 16px 32px rgba(0,0,0,0.7)"; }}
                    onMouseLeave={e => { (e.currentTarget as HTMLElement).style.transform = ""; (e.currentTarget as HTMLElement).style.boxShadow = "0 4px 20px rgba(0,0,0,0.5)"; }}
                  >
                    <img
                      src={movie.poster}
                      alt={movie.title}
                      className="w-full object-cover"
                      style={{ height: "270px" }}
                      onError={e => { (e.target as HTMLElement).style.display = "none"; }}
                    />
                    <div className="absolute inset-0" style={{ background: "linear-gradient(to top, rgba(0,0,0,0.85) 0%, transparent 55%)" }} />
                    <div className="absolute bottom-0 left-0 right-0 p-3">
                      <p className="text-white text-xs font-semibold line-clamp-2">{movie.title}</p>
                      <p className="text-xs mt-0.5" style={{ color: "var(--text-muted)" }}>{movie.year}</p>
                    </div>
                  </div>
                </Link>

                {/* Remove button */}
                <button
                  onClick={() => remove(movie.imdbID)}
                  disabled={removing === movie.imdbID}
                  className="absolute top-2 right-2 w-7 h-7 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                  style={{ background: "rgba(0,0,0,0.75)", backdropFilter: "blur(8px)", border: "1px solid rgba(255,255,255,0.15)" }}
                  title="Remove from list"
                >
                  {removing === movie.imdbID
                    ? <div className="w-3 h-3 border border-white border-t-transparent rounded-full animate-spin" />
                    : <svg width="12" height="12" viewBox="0 0 24 24" fill="white"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" /></svg>
                  }
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
