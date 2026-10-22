# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Print a Code Ocean starter-environment registration request for each image.

The fields follow Code Ocean's "Deploy Custom Image" form. Name, language,
description, machine type and tags come from the image's ``image.yml``. The
version comes from the files pinned at the commit that built the published
image, so no image is pulled; only its registry config is read, for the CUDA
version and the default user.

Usage: uv run scripts/registration_request.py <image-dir>... [--tag SHA]
"""

import argparse
import json
import re
import subprocess
import sys
import tomllib
import urllib.request
from pathlib import Path
from typing import Any

import yaml

REGISTRY = "ghcr.io"
NAMESPACE = "allenneuraldynamics"
MANIFEST_TYPES = (
    "application/vnd.oci.image.index.v1+json, "
    "application/vnd.docker.distribution.manifest.list.v2+json, "
    "application/vnd.oci.image.manifest.v1+json, "
    "application/vnd.docker.distribution.manifest.v2+json"
)
ESCAPED_PIPE = r"\|"


class Registry:
    """Anonymous read access to one GHCR repository."""

    def __init__(self, image: str) -> None:
        """Fetch a pull token for ``image``."""
        self.repo = f"{NAMESPACE}/{image}"
        url = f"https://{REGISTRY}/token?scope=repository:{self.repo}:pull"
        with urllib.request.urlopen(url) as response:
            self.token = json.load(response)["token"]

    def _open(self, path: str, method: str = "GET") -> Any:
        request = urllib.request.Request(
            f"https://{REGISTRY}/v2/{self.repo}/{path}",
            method=method,
            headers={"Authorization": f"Bearer {self.token}", "Accept": MANIFEST_TYPES},
        )
        return urllib.request.urlopen(request)

    def digest(self, tag: str) -> str:
        """Return the manifest digest that ``tag`` points to."""
        with self._open(f"manifests/{tag}", "HEAD") as response:
            return str(response.headers["Docker-Content-Digest"])

    def commit_tag_of_latest(self) -> str:
        """Return the commit tag that shares a digest with ``latest``.

        Code Ocean requires each deployed image source to be unique, and ``latest``
        moves, so a registration names the commit tag instead.
        """
        with self._open("tags/list") as response:
            tags: list[str] = json.load(response)["tags"]
        latest = self.digest("latest")
        for tag in tags:
            if re.fullmatch(r"[0-9a-f]{7,40}", tag) and self.digest(tag) == latest:
                return tag
        sys.exit(f"{self.repo}: no commit tag matches latest; pass --tag")

    def config(self, tag: str) -> dict[str, Any]:
        """Return the linux/amd64 image config for ``tag``."""
        with self._open(f"manifests/{tag}") as response:
            manifest = json.load(response)
        if "manifests" in manifest:
            amd64 = next(
                m
                for m in manifest["manifests"]
                if m.get("platform", {}).get("os") == "linux"
                and m["platform"].get("architecture") == "amd64"
            )
            with self._open(f"manifests/{amd64['digest']}") as response:
                manifest = json.load(response)
        with self._open(f"blobs/{manifest['config']['digest']}") as response:
            config: dict[str, Any] = json.load(response)["config"]
        return config


def file_at(commit: str, path: str) -> str:
    """Return a file's text at ``commit``, or an empty string if it is absent."""
    done = subprocess.run(
        ["git", "show", f"{commit}:{path}"], capture_output=True, text=True, check=False
    )
    return done.stdout if done.returncode == 0 else ""


def normalize(name: str) -> str:
    """Normalize a package name for comparison."""
    return re.sub(r"[-_.]+", "-", name).lower()


def pinned_versions(commit: str, image: str) -> dict[str, str]:
    """Collect the versions that ``image`` pins at ``commit``.

    A ``FROM`` tag versions the tool its image is named for, without any
    ``static-`` prefix; ``requirements.txt`` pins direct Python packages, and
    ``uv.lock`` the whole tree, each overriding the one before.
    """
    versions: dict[str, str] = {}
    for line in file_at(commit, f"{image}/Dockerfile").splitlines():
        match = re.match(r"FROM\s+(?:\S+/)?([\w.-]+):(\d+(?:\.\d+)+)", line)
        if match:
            versions[normalize(match[1].removeprefix("static-"))] = match[2]
    for line in file_at(commit, f"{image}/requirements.txt").splitlines():
        match = re.match(r"\s*([\w.-]+)(?:\[[^]]*\])?\s*==\s*([^\s;#]+)", line)
        if match:
            versions[normalize(match[1])] = match[2]
    lock = file_at(commit, f"{image}/uv.lock")
    for package in tomllib.loads(lock).get("package", []) if lock else []:
        if "version" in package:
            versions[normalize(package["name"])] = package["version"]
    return versions


def python_minor(commit: str, image: str) -> str:
    """Return the Python minor version the Dockerfile installs."""
    dockerfile = file_at(commit, f"{image}/Dockerfile")
    found: set[str] = set(re.findall(r"(?:python[=:]|--python\s+)(3\.\d+)", dockerfile))
    if len(found) != 1:
        sys.exit(
            f"{image}@{commit}: expected one Python version, found {sorted(found)}"
        )
    return found.pop()


def request(image_dir: Path, tag: str | None, release: str | None) -> str:
    """Return the Markdown registration request for one image directory."""
    meta = yaml.safe_load((image_dir / "image.yml").read_text())
    image = image_dir.resolve().name
    if not meta.get("starter_environment"):
        sys.exit(f"{image}: image.yml does not mark it as a starter environment")
    registry = Registry(image)
    commit = tag or registry.commit_tag_of_latest()
    if subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"], check=False
    ).returncode:
        sys.exit(f"{image}: commit {commit} is not in this clone; fetch it first")
    config = registry.config(commit)
    # Code Ocean needs the default user to be root to reach capsule folders.
    if config.get("User", "") not in ("", "0", "root", "0:0", "root:root"):
        sys.exit(
            f"{image}:{commit}: runs as {config['User']!r}; Code Ocean requires root"
        )

    pins = pinned_versions(commit, image)
    parts = []
    for name in meta.get("key_packages", []):
        if normalize(name) in pins:
            parts.append(f"{name} {pins[normalize(name)]}")
        else:
            print(
                f"{image}@{commit}: {name} is not pinned; leaving it out",
                file=sys.stderr,
            )
    env = dict(entry.split("=", 1) for entry in config.get("Env", []))
    if "CUDA_VERSION" in env:
        parts.append("CUDA " + ".".join(env["CUDA_VERSION"].split(".")[:2]))
    parts.append(f"Python {python_minor(commit, image)}")
    if release:
        parts.append(release)

    fields = {
        "Name": meta["title"],
        "Docker Image": f"{REGISTRY}/{NAMESPACE}/{image}:{commit}",
        "Version": ", ".join(parts),
        "Language": meta["language"],
        "Description": " ".join(meta["description"].split()),
        "Machine Type": "GPU" if meta["gpu"] else "Standard",
        "Tags": ", ".join(meta.get("tags", [])),
    }
    rows = "\n".join(
        f"| {k} | {v.replace('|', ESCAPED_PIPE)} |" for k, v in fields.items()
    )
    return f"### {meta['title']}\n\n| Field | Value |\n|---|---|\n{rows}\n"


def main() -> None:
    """Parse arguments and print one request per image directory."""
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("image_dirs", nargs="+", type=Path)
    parser.add_argument(
        "--tag", help="commit tag to register (default: the one at latest)"
    )
    parser.add_argument(
        "--release",
        help="name that ends the version, to tell apart releases that pin the same"
        " key packages",
    )
    args = parser.parse_args()
    print("\n".join(request(d, args.tag, args.release) for d in args.image_dirs))


if __name__ == "__main__":
    main()
