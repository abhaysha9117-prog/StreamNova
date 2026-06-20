import os
import requests
import json

REPO_FILE = "repositories/repos.json"
EXTENSIONS_FOLDER = "extensions"


def load_repositories():

    if not os.path.exists(REPO_FILE):
        return []

    with open(REPO_FILE, "r") as f:
        return json.load(f)


def save_repositories(repos):

    os.makedirs("repositories", exist_ok=True)

    with open(REPO_FILE, "w") as f:
        json.dump(repos, f, indent=2)


def add_repository(repo_url):

    repos = load_repositories()

    if repo_url not in repos:
        repos.append(repo_url)
        save_repositories(repos)

    return repos


def download_extension(extension_url):

    os.makedirs(EXTENSIONS_FOLDER, exist_ok=True)

    filename = extension_url.split("/")[-1]

    path = os.path.join(
        EXTENSIONS_FOLDER,
        filename
    )

    r = requests.get(extension_url)

    with open(path, "wb") as f:
        f.write(r.content)

    return path


def fetch_repo_extensions(repo_url):

    r = requests.get(repo_url)

    return r.json()
# ================================
# ⭐ Extension Version Management
# ================================

VERSIONS_FILE = "extensions/versions.json"


def load_versions():

    if not os.path.exists(VERSIONS_FILE):
        return {}

    with open(VERSIONS_FILE, "r") as f:
        return json.load(f)


def save_versions(data):

    with open(VERSIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def update_extension(extension):

    url = extension["url"]
    name = extension["file"]
    version = extension["version"]

    # Download latest version
    path = download_extension(url)

    # Save version info
    versions = load_versions()

    versions[name] = version

    save_versions(versions)

    return path
# ================================
# ⭐ Repository Storage
# ================================

REPO_LIST_FILE = "repositories/repos.json"


def get_saved_repos():

    if not os.path.exists(REPO_LIST_FILE):
        return []

    with open(REPO_LIST_FILE, "r") as f:
        return json.load(f)