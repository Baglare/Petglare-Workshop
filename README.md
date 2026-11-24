# Petglare Workshop

**English** · [Türkçe](README.tr.md)

The community mascot catalog for [Petglare](https://github.com/Baglare/ClaudePetGlare), a desktop companion for Claude Code on Windows.

## Find a pet

Install [Petglare](https://github.com/Baglare/ClaudePetGlare/releases/latest). In the app, enable **Ayarlar → Workshop → Workshop'a bağlan (internet)** (Settings → Workshop → Connect). Open **Workshop'tan pet bul…** (Find pets), search the catalog and select **Ekle** (Add). Pet images are downloaded and verified locally. Online access is off by default.

## Submit a pet

1. In Petglare, open **Ayarlar → Şekil** (Settings → Shape). Right-click a custom pet and select **Workshop'a gönder…** (Submit to Workshop).
2. Drag the prepared PNG into the GitHub submission form, enter its name, check the consent boxes and submit. A GitHub account is required.
3. A bot validates the PNG (up to 2 MB and 4096 pixels per side), re-encodes it, resizes it to at most 512 pixels and opens a pull request for approval.
4. A maintainer reviews and merges acceptable submissions. The catalog index is then regenerated.

You can also open the [submission form](../../issues/new?template=pet.yml) directly.

## Rules

- Submit only images you created or have permission to share.
- Inappropriate, violent or hateful content is not accepted.
- Accepted submissions are public and licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The author name is displayed in the catalog.
- Open an issue to request removal of a pet.

## Repository layout

| Path | Description |
|---|---|
| `pets/<id>/pet.png` | Transparent mascot PNG, up to 512 px per side and 300 KB |
| `pets/<id>/pet.json` | Name, author, date, SHA-256 and submission issue |
| `index.json` | Catalog regenerated after approved merges |
| `scripts/` | Submission validation and catalog generation (Python + Pillow) |

The catalog is curated by the maintainer. Submission does not guarantee approval. Petglare is an independent project and is not affiliated with Anthropic.
