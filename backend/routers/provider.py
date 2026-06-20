from fastapi import APIRouter
from plugins.loader import get_plugins

router = APIRouter()


# ============================
# SEARCH
# ============================

@router.get("/provider/search")
def provider_search(query: str):

    plugins = get_plugins()

    results = []

    for plugin in plugins:

        try:

            items = plugin.search(query)

            if not items:
                continue

            # Attach plugin name
            for item in items:

                item["provider"] = plugin.name

                results.append(item)

        except Exception as e:

            print(
                f"Search error in {plugin.name}: {e}"
            )

    return results


# ============================
# EPISODES
# ============================

@router.get("/provider/episodes")
def provider_episodes(item_id: str, provider: str):

    plugins = get_plugins()

    for plugin in plugins:

        # Only correct provider
        if plugin.name != provider:
            continue

        if hasattr(plugin, "get_episodes"):

            try:

                return plugin.get_episodes(item_id)

            except Exception as e:

                print(
                    f"Episodes error in {plugin.name}: {e}"
                )

    return []


# ============================
# STREAMS
# ============================

@router.get("/provider/streams")
def provider_streams(item_id: str, provider: str):

    plugins = get_plugins()

    for plugin in plugins:

        if plugin.name != provider:
            continue

        if hasattr(plugin, "get_streams"):

            try:

                # ✅ Return directly
                return plugin.get_streams(item_id)

            except Exception as e:

                print(
                    f"Streams error in {plugin.name}: {e}"
                )

    # fallback

    return {

        "streams": [],
        "subtitles": []

    }