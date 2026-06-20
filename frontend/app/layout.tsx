import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "StreamNova",
  description: "Movie Streaming Platform"
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {

  return (

    <html lang="en">

      <body className="bg-gray-100">

        {/* 🎬 Navbar */}

        <nav className="bg-black text-white px-6 py-4 flex justify-between items-center shadow">

          {/* Logo */}

          <Link
            href="/"
            className="text-2xl font-bold text-red-500"
          >
            🎬 StreamNova
          </Link>
          <Link
             href="/extensions"
              className="hover:text-red-400"
              >
                🧩 Extensions
              </Link>

          {/* Navigation Links */}

          <div className="space-x-6">

            <Link
              href="/"
              className="hover:text-red-400"
            >
              🏠 Home
            </Link>

            <Link
              href="/favorites"
              className="hover:text-red-400"
            >
              ❤️ Favorites
            </Link>

            <Link
              href="/history"
              className="hover:text-red-400"
            >
              📺 History
            </Link>

          </div>

        </nav>

        {/* Page Content */}

        <main className="p-6">

          {children}

        </main>

      </body>

    </html>

  );

}