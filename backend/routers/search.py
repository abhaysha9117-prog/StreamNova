from fastapi import APIRouter

from plugins.loader import get_plugins

router = APIRouter()


@router.get("/search")
async def search(query: str, category: str = None):

    plugins = get_plugins()

    results = []

    seen_ids = set()

    for plugin in plugins:

        plugin_category = getattr(
            plugin,
            "category",
            "movies"
        )

        # ⭐ Category filtering
        if category:

            if plugin_category != category:
                continue

        try:

            # ✅ FIX: remove await
            res = plugin.search(query)

            # Safety check
            if not res:
                continue

            for item in res:

                imdb_id = item.get("imdbID")

                # ⭐ Remove duplicates
                if imdb_id:

                    if imdb_id in seen_ids:
                        continue

                    seen_ids.add(imdb_id)

                results.append(item)

        except Exception as e:

            print(
                f"Search error in {plugin.name}: {e}"
            )

    return {
        "results": results
    }