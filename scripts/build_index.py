#!/usr/bin/env python3
"""
Generate index.json for gallery. Supports:
- Legacy: list of single-image entries { "file", "title", "body", "tags" } -> each becomes a one-image album.
- Albums: list of albums { "title", "body", "tags", "images": ["path", ...] } -> one album per entry.
Output: { "albums": [ { "id", "title", "body", "tags", "date", "images": [ { "file", "cdn_url", "raw_url" } ] } ] }
"""
import json
import os
import hashlib
from datetime import datetime
from urllib.parse import quote

GALLERY_REPO = "study-overflow/gallery-overflow"
CDN_BASE = f"https://cdn.jsdelivr.net/gh/{GALLERY_REPO}@main/"
RAW_BASE = f"https://raw.githubusercontent.com/{GALLERY_REPO}/main/"


def generate_album_id(title, index):
    h = hashlib.md5((title + str(index)).encode()).hexdigest()
    return f"album_{h[:12]}"


def ensure_raw_url(file_path):
    parts = file_path.split("/")
    encoded = "/".join(quote(p, safe="") for p in parts)
    return RAW_BASE + encoded


def ensure_cdn_url(file_path):
    return CDN_BASE + file_path


def get_file_date(file_path):
    if os.path.exists(file_path):
        return datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d")
    return datetime.now().strftime("%Y-%m-%d")


def normalize_to_albums(metadata_list):
    """Convert meta (legacy or album format) to list of album dicts."""
    albums = []
    for i, meta in enumerate(metadata_list):
        if "images" in meta:
            # New album format: { title, body, tags?, date?, images: ["path", ...] }
            image_paths = meta["images"]
            if not isinstance(image_paths[0], dict):
                image_paths = [{"file": p} if isinstance(p, str) else p for p in image_paths]
            images = []
            for im in image_paths:
                path = im.get("file", im) if isinstance(im, dict) else im
                images.append({
                    "file": path,
                    "cdn_url": ensure_cdn_url(path),
                    "raw_url": ensure_raw_url(path),
                })
            album = {
                "id": meta.get("id") or generate_album_id(meta.get("title", ""), i),
                "title": meta.get("title", "Untitled"),
                "body": meta.get("body", ""),
                "tags": meta.get("tags", []),
                "date": meta.get("date") or (get_file_date(images[0]["file"]) if images else datetime.now().strftime("%Y-%m-%d")),
                "images": images,
            }
            albums.append(album)
        else:
            # Legacy single-image entry: { file, title, body, tags }
            path = meta.get("file", "")
            album = {
                "id": meta.get("id") or generate_album_id(meta.get("title", ""), i),
                "title": meta.get("title", "Untitled"),
                "body": meta.get("body", ""),
                "tags": meta.get("tags", []),
                "date": meta.get("date", get_file_date(path)),
                "images": [{
                    "file": path,
                    "cdn_url": ensure_cdn_url(path),
                    "raw_url": ensure_raw_url(path),
                }],
            }
            albums.append(album)
    return albums


def main():
    meta_path = os.path.join(os.path.dirname(__file__), "..", "meta.json")
    index_path = os.path.join(os.path.dirname(__file__), "..", "index.json")
    with open(meta_path, "r", encoding="utf-8") as f:
        meta_list = json.load(f)
    albums = normalize_to_albums(meta_list)
    out = {"albums": albums}
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Generated index.json with {len(albums)} album(s)")


if __name__ == "__main__":
    main()
