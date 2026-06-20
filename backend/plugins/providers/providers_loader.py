import importlib
import json
import os

PROVIDERS_FOLDER = "plugins/providers"
ENABLED_FILE = "extensions/enabled_providers.json"


# ================================
# ⭐ Discover Providers Automatically
# ================================
def discover_providers():

    providers = []

    if not os.path.exists(PROVIDERS_FOLDER):
        return providers

    for file in os.listdir(PROVIDERS_FOLDER):

        # ✅ Only load valid provider files
        if (
            file.endswith(".py")
            and file != "__init__.py"
            and not file.startswith("_")
        ):

            provider_name = file.replace(".py", "")
            providers.append(provider_name)

    return providers


# ================================
# ⭐ Load Enabled Providers
# ================================
def load_enabled():

    if not os.path.exists(ENABLED_FILE):
        return []

    try:
        with open(ENABLED_FILE, "r") as f:
            return json.load(f)

    except Exception as e:
        print("⚠️ Error loading enabled providers:", e)
        return []


# ================================
# ⭐ Save Enabled Providers
# ================================
def save_enabled(enabled):

    try:
        os.makedirs(
            os.path.dirname(ENABLED_FILE),
            exist_ok=True
        )

        with open(ENABLED_FILE, "w") as f:
            json.dump(enabled, f, indent=2)

    except Exception as e:
        print("⚠️ Error saving providers:", e)


# ================================
# ⭐ Load Streams From Enabled Providers
# ================================
def load_all_streams(imdbID: str):

    enabled = load_enabled()

    all_streams = []

    for provider_name in enabled:

        try:

            module_name = (
                f"plugins.providers.{provider_name}"
            )

            module = importlib.import_module(
                module_name
            )

            # ✅ Ensure provider has get_streams
            if not hasattr(module, "get_streams"):
                print(
                    f"⚠️ Provider {provider_name} missing get_streams()"
                )
                continue

            streams = module.get_streams(imdbID)

            # ✅ Handle None safely
            if not streams:
                continue

            # ⭐ Attach provider name
            for s in streams:

                if isinstance(s, dict):
                    s["provider"] = provider_name
                    all_streams.append(s)

        except Exception as e:

            print(
                "⚠️ Provider error:",
                provider_name,
                e
            )

    return all_streams