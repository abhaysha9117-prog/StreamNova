"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface WatchItem {
  imdbID: string;
  title: string;
  poster: string;
  progress: number;
}

function fmtProgress(sec: number) {
  const h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = Math.floor(sec % 60);
  return h > 0 ? `${h}h ${m}m` : m > 0 ? `${m}m ${s}s` : `${s}s`;
}

export default function HistoryPage() {
  const [history, setHistory] = useState<WatchItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/watch/list")
      .then(r => r.json())
      .then(d => { setHistory(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen px-6 pt-28 pb-16" style={{ background: "var(--bg-primary)" }}>
      <div className="max-w-screen-2xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-white font-black" style={{ fontFamily: "var(--font-display)", fontSize: "36px", letterSpacing: "2px" }}>
            📺 Watch History
          </h1>
          {history.length > 0 && (
            <span className="text-sm px-3 py-1.5 rounded-lg" style={{ background: "var(--bg-elevated)", color: "var(--text-secondary)" }}>
              {history.length} title{history.length !== 1 ? "s" : ""}
            </span>
          )}
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-32">
            <div className="w-10 h-10 rounded-full border-4 border-t-transparent animate-spin" style={{ borderColor: "rgba(229,57,53,0.3)", borderTopColor: "var(--accent)" }} />
          </div>
        ) : history.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-32 gap-4">
            <span className="text-7xl">📺</span>
            <p className="text-xl font-bold text-white">No history yet</p>
            <p className="text-sm" style={{ color: "var(--text-secondary)" }}>Start watching something to see it here.</p>
            <Link href="/" className="mt-4 px-6 py-3 rounded-xl font-bold text-white text-sm" style={{ background: "var(--accent)" }}>
              Browse Content
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-5">
            {history.map(movie => (
              <Link key={movie.imdbID} href={`/watch/${movie.imdbID}`} className="group animate-fade-in block">
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
                  <div className="absolute inset-0" style={{ background: "linear-gradient(to top, rgba(0,0,0,0.9) 0%, transparent 55%)" }} />

                  {/* Resume play button on hover */}
                  <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                    <div className="w-12 h-12 rounded-full flex items-center justify-center" style={{ background: "rgba(229,57,53,0.9)" }}>
                      <svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M8 5v14l11-7z" /></svg>
                    </div>
                  </div>

                  <div className="absolute bottom-0 left-0 right-0 p-3">
                    <p className="text-white text-xs font-semibold line-clamp-2">{movie.title}</p>
                    <p className="text-xs mt-1" style={{ color: "rgba(255,255,255,0.5)" }}>
                      Watched {fmtProgress(movie.progress)}
                    </p>
                  </div>
                </div>

                {/* Progress bar */}
                <div className="mt-2 rounded-full overflow-hidden" style={{ height: "3px", background: "rgba(255,255,255,0.1)" }}>
                  <div
                    className="h-full rounded-full"
                    style={{ width: `${Math.min(100, (movie.progress / 7200) * 100)}%`, background: "var(--accent)" }}
                  />
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
