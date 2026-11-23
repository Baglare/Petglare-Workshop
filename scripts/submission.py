"""Turns a "Pet gönder" issue into a pet folder, or explains why it cannot.

The issue body is untrusted text: it is only parsed here, never executed. The picture is
fetched only from GitHub's own attachment hosts, size-limited, decoded with a pixel limit,
re-encoded as a fresh PNG (nothing else from the upload survives) and scaled to 512 px.
Outputs (for the workflow): pet id and an error message, via GITHUB_OUTPUT.
"""
import hashlib
import io
import json
import os
import re
import sys
import unicodedata
import urllib.request
from datetime import datetime, timezone

from PIL import Image

MAX_DOWNLOAD = 2 * 1024 * 1024
MAX_PET_BYTES = 300 * 1024
PET_SIDE = 512
Image.MAX_IMAGE_PIXELS = 40_000_000
ALLOWED = re.compile(r"https://(github\.com/user-attachments/(assets|files)/[A-Za-z0-9/_.-]+"
                     r"|user-images\.githubusercontent\.com/[A-Za-z0-9/_.-]+"
                     r"|private-user-images\.githubusercontent\.com/[A-Za-z0-9/_.?=&%-]+)")


def section(body: str, title: str) -> str:
    match = re.search(r"^###\s*" + re.escape(title) + r"\s*$(.*?)(?=^###\s|\Z)", body, re.M | re.S)
    value = match.group(1).strip() if match else ""
    return "" if value == "_No response_" else value


def clean_name(text: str, limit: int) -> str:
    text = "".join(c for c in text if unicodedata.category(c)[0] != "C").strip()
    return text[:limit].strip()


def slug(text: str) -> str:
    plain = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    plain = re.sub(r"[^a-z0-9]+", "-", plain).strip("-")
    return plain[:24] or "pet"


def fail(message: str) -> None:
    write_output("error", message)
    print("::error::" + message)
    sys.exit(0)


def write_output(key: str, value: str) -> None:
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as out:
        out.write(f"{key}={value}\n")


class Redirects(urllib.request.HTTPRedirectHandler):
    """Attachments redirect to signed storage URLs; follow at most a few redirects, https only."""
    max_redirections = 3

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not newurl.startswith("https://"):
            raise urllib.error.HTTPError(newurl, code, "https only", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(url: str) -> bytes:
    opener = urllib.request.build_opener(Redirects)
    request = urllib.request.Request(url, headers={"User-Agent": "petglare-workshop-bot"})
    with opener.open(request, timeout=30) as response:
        data = response.read(MAX_DOWNLOAD + 1)
    if len(data) > MAX_DOWNLOAD:
        fail("Görsel 2 MB'tan büyük.")
    return data


def main() -> None:
    body = os.environ.get("ISSUE_BODY", "")
    number = int(os.environ["ISSUE_NUMBER"])
    login = os.environ.get("ISSUE_AUTHOR", "")

    name = clean_name(section(body, "Pet adı"), 40)
    if not name:
        fail("Pet adı boş.")
    author = clean_name(section(body, "Görünecek yazar adı"), 40) or clean_name(login, 40) or "Anonim"
    match = ALLOWED.search(section(body, "Görsel"))
    if not match:
        fail("Görsel alanında GitHub'a yüklenmiş bir PNG bulunamadı. Dosyayı alana sürükleyip bırak.")
    if section(body, "Onay").count("[x]") + section(body, "Onay").count("[X]") < 3:
        fail("Üç onay kutusunun hepsi işaretli olmalı.")

    data = download(match.group(0))
    try:
        with Image.open(io.BytesIO(data)) as probe:
            if probe.format != "PNG":
                fail("Yalnız PNG kabul ediliyor.")
            probe.verify()
        with Image.open(io.BytesIO(data)) as image:
            image.load()
            if max(image.size) > 4096:
                fail("Görsel 4096 pikselden büyük.")
            image = image.convert("RGBA")
    except (OSError, ValueError, Image.DecompressionBombError) as error:
        fail(f"Görsel okunamadı: {type(error).__name__}")

    box = image.getchannel("A").point(lambda a: 255 if a >= 8 else 0).getbbox()
    if box is None:
        fail("Görselde görünür piksel yok; arka planı şeffaf bir PNG gönder.")
    image = image.crop(box)
    image.thumbnail((PET_SIDE, PET_SIDE), Image.LANCZOS)
    output = io.BytesIO()
    image.save(output, "PNG", optimize=True)
    png = output.getvalue()
    if len(png) > MAX_PET_BYTES:
        output = io.BytesIO()
        image.quantize(colors=256, method=Image.Quantize.FASTOCTREE).convert("RGBA").save(output, "PNG", optimize=True)
        png = output.getvalue()
    if len(png) > MAX_PET_BYTES:
        fail("Görsel küçültüldükten sonra bile 300 KB'tan büyük.")

    pet_id = f"{slug(name)}-{number}"
    folder = os.path.join("pets", pet_id)
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "pet.png"), "wb") as handle:
        handle.write(png)
    meta = {
        "format": "petglare-pet-v1",
        "name": name,
        "author": author,
        "created": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "sha256": hashlib.sha256(png).hexdigest(),
        "issue": number,
        "license": "CC-BY-4.0",
    }
    with open(os.path.join(folder, "pet.json"), "w", encoding="utf-8") as handle:
        json.dump(meta, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    write_output("id", pet_id)
    write_output("name", name.replace("\n", " "))


if __name__ == "__main__":
    main()
