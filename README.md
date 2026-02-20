# gallery-overflow

**Gallery (albums) content source** for the homepage. The site pulls `index.json` from here; images are served via jsDelivr or GitHub raw.

See the gallery: **https://zzhang.tech/gallery/**

---

**What’s here**

| Item | Description |
|------|-------------|
| `meta.json` | Albums you edit: `title`, `body`, `tags`, `images: ["path", ...]`. |
| `images/` | Image files. |
| `index.json` | Generated from `meta.json` by the script. |
| `scripts/build_index.py` | Reads `meta.json` → writes `index.json`. |

**New album**

1. Add images under `images/`.
2. Append an entry in `meta.json` with `title`, `body`, `tags`, `images` (array of paths).
3. Run `python scripts/build_index.py`, or push to `main` and let the [workflow](.github/workflows/build-index.yml) update the index.
4. Push. Homepage picks up the new `index.json`.

**Comments** — [Utterances](https://github.com/apps/utterances) uses this repo; authorize **study-overflow/gallery-overflow** for comments to work.
