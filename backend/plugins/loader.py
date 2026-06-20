import os
import importlib
import json
import sys

# ================================
# Global Plugin List
# ================================

plugins = []

ENABLED_FILE = "extensions/enabled.json"


# ================================
# Load Enabled Extensions
# ================================

def load_enabled():

    if not os.path.exists(ENABLED_FILE):

        os.makedirs("extensions", exist_ok=True)

        with open(ENABLED_FILE, "w") as f:
            json.dump([], f)

        return []

    try:
        with open(ENABLED_FILE, "r") as f:
            return json.load(f)

    except Exception:
        return []


# ================================
# Save Enabled Extensions
# ================================

def save_enabled(enabled):

    os.makedirs("extensions", exist_ok=True)

    with open(ENABLED_FILE, "w") as f:

        json.dump(enabled, f, indent=2)


# ================================
# Load Plugins
# ================================

def load_plugins():

    global plugins

    plugins = []

    enabled = load_enabled()

    folders = ["plugins", "extensions"]

    print("\n=== Loading Plugins ===")

    for folder in folders:

        if not os.path.exists(folder):
            continue

        for file in os.listdir(folder):

            full_path = os.path.join(folder, file)

            # ✅ Skip folders (like providers/)
            if os.path.isdir(full_path):
                continue

            # ✅ Only Python files
            if not file.endswith(".py"):
                continue

            # ✅ Skip system/helper files
            if file in [
                "__init__.py",
                "base.py",
                "loader.py"
            ]:
                continue

            module_name = file[:-3]

            # ✅ Extensions must be enabled
            if folder == "extensions":

                if module_name not in enabled:
                    continue

            module_path = f"{folder}.{module_name}"

            try:

                # Reload if already loaded
                if module_path in sys.modules:

                    module = importlib.reload(
                        sys.modules[module_path]
                    )

                else:

                    module = importlib.import_module(
                        module_path
                    )

                # ✅ Load Plugin class only
                if hasattr(module, "Plugin"):

                    plugin = module.Plugin()

                    plugins.append(plugin)

                    print(
                        f"✅ Loaded plugin: {plugin.name}"
                    )

                else:

                    # Silent skip (no warnings)
                    continue

            except Exception as e:

                print(
                    f"❌ Failed to load {file}: {e}"
                )

    print(
        f"📦 Total plugins loaded: {len(plugins)}"
    )


# ================================
# Get Plugins
# ================================

def get_plugins():

    return plugins