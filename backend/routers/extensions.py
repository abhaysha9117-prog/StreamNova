from fastapi import APIRouter
import os

from plugins.loader import (
    get_plugins,
    load_enabled,
    save_enabled,
    load_plugins
)

from plugins.providers.providers_loader import (
    discover_providers,
    load_enabled,
    save_enabled
)

from repositories.manager import (
    get_saved_repos,
    update_extension,
    load_versions,
    save_versions,
    add_repository,
    download_extension,
    fetch_repo_extensions
)

router = APIRouter()

# ================================
# ⭐ Get Saved Repositories
# ================================
@router.get("/repos")
def get_repos():

    repos = get_saved_repos()

    return repos

# ================================
# ⭐ Get Available Providers
# ================================
@router.get("/available")
def get_available():

    providers = discover_providers()

    enabled = load_enabled()

    result = []

    for p in providers:

        result.append({
            "name": p,
            "enabled": p in enabled
        })

    return result

# ================================
# ⭐ Toggle Provider
# ================================
@router.post("/toggle/{provider}")
def toggle_provider(provider: str):

    enabled = load_enabled()

    if provider in enabled:

        enabled.remove(provider)

    else:

        enabled.append(provider)

    save_enabled(enabled)

    return {
        "message": "Updated"
    }


# ================================
# ⭐ Add Repository
# ================================
@router.post("/add-repo")
def add_repo(repo_url: str):

    repos = add_repository(repo_url)

    return {
        "message": "Repository added",
        "repos": repos
    }


# ================================
# ⭐ Install Extension
# ================================
@router.post("/install-extension")
def install_extension(extension_url: str):

    path = download_extension(
        extension_url
    )

    load_plugins()

    return {
        "message": "Extension installed",
        "path": path
    }


# ================================
# ⭐ Get Extensions From Repo
# ================================
@router.get("/repo-extensions")
def get_repo_extensions(repo_url: str):

    data = fetch_repo_extensions(
        repo_url
    )

    return data


# ================================
# ⭐ List Installed Extensions
# ================================
@router.get("/installed")
def list_installed():

    files = []

    if os.path.exists("extensions"):

        for f in os.listdir("extensions"):

            if f.endswith(".py"):
                files.append(f)

    enabled = load_enabled()

    return {
        "installed": files,
        "enabled": enabled
    }


# ================================
# ⭐ Enable Extension
# ================================
@router.post("/enable")
def enable_extension(name: str):

    enabled = load_enabled()

    if name not in enabled:
        enabled.append(name)

    save_enabled(enabled)

    load_plugins()

    return {
        "message": f"{name} enabled"
    }


# ================================
# ⭐ Disable Extension
# ================================
@router.post("/disable")
def disable_extension(name: str):

    enabled = load_enabled()

    if name in enabled:
        enabled.remove(name)

    save_enabled(enabled)

    load_plugins()

    return {
        "message": f"{name} disabled"
    }


# ================================
# ⭐ Remove Extension
# ================================
@router.post("/remove")
def remove_extension(name: str):

    file_path = os.path.join(
        "extensions",
        name
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    enabled = load_enabled()

    if name in enabled:
        enabled.remove(name)

    save_enabled(enabled)

    versions = load_versions()

    if name in versions:
        del versions[name]

    save_versions(versions)

    load_plugins()

    return {
        "message": f"{name} removed"
    }


# ================================
# ⭐ Update Extension
# ================================
@router.post("/update")
def update_ext(extension: dict):

    path = update_extension(extension)

    load_plugins()

    return {
        "message": "Extension updated",
        "path": path
    }


# ================================
# ⭐ Get Installed Versions
# ================================
@router.get("/versions")
def get_versions():

    versions = load_versions()

    return versions


# ================================
# ⭐ Get Extension Categories
# ================================
@router.get("/categories")
def get_categories():

    plugins = get_plugins()

    categories = {}

    for plugin in plugins:

        cat = getattr(
            plugin,
            "category",
            "other"
        )

        if cat not in categories:
            categories[cat] = []

        categories[cat].append(
            plugin.name
        )

    return categories


# ================================
# ⭐ Update All Extensions
# ================================
@router.post("/update-all")
def update_all(repo_url: str):

    repo_extensions = fetch_repo_extensions(
        repo_url
    )

    versions = load_versions()

    updated = []

    for ext in repo_extensions:

        # Safe filename detection
        file_name = ext.get(
            "file"
        ) or ext.get(
            "url"
        ).split("/")[-1]

        repo_version = ext.get(
            "version",
            "1.0"
        )

        current_version = versions.get(
            file_name
        )

        if current_version != repo_version:

            update_extension(ext)

            updated.append(file_name)

    load_plugins()

    return {
        "updated": updated
    }