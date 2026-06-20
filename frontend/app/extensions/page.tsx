"use client";

import { useEffect, useState } from "react";

interface Provider {

  name: string;

  enabled: boolean;

}

export default function ExtensionsPage() {

  const [providers, setProviders] =
    useState<Provider[]>([]);

  const [repoUrl, setRepoUrl] =
    useState("");

  const [repoExtensions, setRepoExtensions] =
    useState<any[]>([]);



  // ⭐ Load Installed Providers
  async function loadProviders() {

    const res =
      await fetch(
        "http://127.0.0.1:8000/extensions/available"
      );

    const data =
      await res.json();

    setProviders(data);

  }



  // ⭐ Toggle Provider
  async function toggle(name: string) {

    await fetch(
      `http://127.0.0.1:8000/extensions/toggle/${name}`,
      {
        method: "POST"
      }
    );

    loadProviders();

  }



  // ⭐ Add Repository
  async function addRepo() {

    await fetch(
      `http://127.0.0.1:8000/extensions/add-repo?repo_url=${repoUrl}`,
      {
        method: "POST"
      }
    );

    alert("Repository Added");

  }



  // ⭐ Load Repo Extensions
  async function loadRepoExtensions() {

    const res =
      await fetch(
        `http://127.0.0.1:8000/extensions/repo-extensions?repo_url=${repoUrl}`
      );

    const data =
      await res.json();

    setRepoExtensions(data);

  }



  // ⭐ Install Extension
  async function install(url: string) {

    await fetch(
      `http://127.0.0.1:8000/extensions/install-extension?extension_url=${url}`,
      {
        method: "POST"
      }
    );

    alert("Extension Installed");

    loadProviders();

  }



  useEffect(() => {

    loadProviders();

  }, []);



  return (

    <div className="p-6">

      <h1 className="
        text-2xl
        font-bold
        mb-4
      ">

        Extensions Store

      </h1>



      {/* ⭐ Repository Input */}
      <div className="mb-6">

        <input
          type="text"
          placeholder="Repository URL"
          value={repoUrl}
          onChange={(e) =>
            setRepoUrl(e.target.value)
          }
          className="
            border
            px-3
            py-2
            w-full
            mb-2
          "
        />

        <div className="flex gap-2">

          <button
            onClick={addRepo}
            className="
              bg-blue-600
              text-white
              px-4
              py-2
              rounded
            "
          >

            Add Repo

          </button>



          <button
            onClick={loadRepoExtensions}
            className="
              bg-green-600
              text-white
              px-4
              py-2
              rounded
            "
          >

            Load Extensions

          </button>

        </div>

      </div>



      {/* ⭐ Repo Extensions */}
      <div className="mb-8">

        <h2 className="font-bold mb-2">

          Available Extensions

        </h2>

        {repoExtensions.map((ext) => (

          <div
            key={ext.name}
            className="
              flex
              justify-between
              items-center
              p-3
              border
              rounded
              mb-2
            "
          >

            <span>

              {ext.name}

            </span>



            <button
              onClick={() =>
                install(ext.url)
              }
              className="
                bg-purple-600
                text-white
                px-4
                py-1
                rounded
              "
            >

              Install

            </button>

          </div>

        ))}

      </div>



      {/* ⭐ Installed Providers */}
      <div>

        <h2 className="font-bold mb-2">

          Installed Providers

        </h2>

        {providers.map((p) => (

          <div
            key={p.name}
            className="
              flex
              items-center
              justify-between
              p-3
              border
              rounded
              mb-2
            "
          >

            <span>

              {p.name}

            </span>



            <button
              onClick={() =>
                toggle(p.name)
              }
              className={`
                px-4
                py-1
                rounded
                text-white
                ${
                  p.enabled
                    ? "bg-green-600"
                    : "bg-gray-500"
                }
              `}
            >

              {p.enabled
                ? "Enabled"
                : "Disabled"}

            </button>

          </div>

        ))}

      </div>

    </div>

  );

}