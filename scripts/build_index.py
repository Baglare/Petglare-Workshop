"""Rebuilds index.json from pets/<id>/pet.png + pet.json, skipping anything that does not check out."""
import hashlib
import json
import os
import re

from PIL import Image

Image.MAX_IMAGE_PIXELS = 4_000_000
ID = re.compile(r"^[a-z0-9-]{1,40}$")
MAX_PET_BYTES = 300 * 1024


def main() -> None:
    pets = []
    for pet_id in sorted(os.listdir("pets")):
        folder = os.path.join("pets", pet_id)
        png_path, meta_path = os.path.join(folder, "pet.png"), os.path.join(folder, "pet.json")
        if not (ID.match(pet_id) and os.path.isfile(png_path) and os.path.isfile(meta_path)):
            continue
        with open(png_path, "rb") as handle:
            png = handle.read()
        with open(meta_path, encoding="utf-8") as handle:
            meta = json.load(handle)
        digest = hashlib.sha256(png).hexdigest()
        if len(png) > MAX_PET_BYTES or meta.get("sha256") != digest:
            print(f"::warning::{pet_id} atlandı (boyut veya özet tutmuyor)")
            continue
        with Image.open(png_path) as image:
            width, height = image.size
        if image.format != "PNG" or max(width, height) > 512:
            print(f"::warning::{pet_id} atlandı (PNG değil veya 512 pikselden büyük)")
            continue
        pets.append({
            "id": pet_id,
            "name": str(meta.get("name", ""))[:40],
            "author": str(meta.get("author", ""))[:40],
            "created": str(meta.get("created", "")),
            "path": f"pets/{pet_id}/pet.png",
            "bytes": len(png),
            "width": width,
            "height": height,
            "sha256": digest,
            "license": "CC-BY-4.0",
        })
    pets.sort(key=lambda p: p["created"], reverse=True)
    index = {"format": "petglare-catalog-v1", "pets": pets}
    with open("index.json", "w", encoding="utf-8") as handle:
        json.dump(index, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"{len(pets)} pet katalogda")


if __name__ == "__main__":
    main()
