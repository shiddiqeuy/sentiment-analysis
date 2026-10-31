"""Ekspor post Threads ke berkas JSON lokal untuk pipeline (tanpa dependensi).

Token dibaca dari variabel lingkungan THREADS_TOKEN. Token tidak pernah ditulis ke
berkas atau dicetak; URL paging (yang memuat token) dibuang dari hasil.
Keluaran default ke data/ (di-gitignore).

Contoh:
  python tools/export_threads.py profile --username threads --limit 25 --pages 2
  python tools/export_threads.py keyword --q kopi --limit 25
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = os.environ.get("THREADS_API_BASE", "https://graph.threads.com/v1.0").rstrip("/")

# [asumsi] nama field; yang diverifikasi di uji: lihat docs/research/threads-api-test-results.md
FIELDS = {
    "profile": "id,media_type,text,topic_tag,timestamp,permalink,username,is_quote_post",
    "keyword": "id,media_type,text,topic_tag,timestamp,permalink,username,has_replies,is_quote_post",
}
ENDPOINT = {"profile": "profile_posts", "keyword": "keyword_search"}


def get(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        # sengaja tidak mencetak e.url / str(e): URL memuat token
        body = e.read().decode("utf-8", "replace")[:500]
        sys.exit(f"HTTP {e.code} dari API: {body}")
    except urllib.error.URLError as e:
        sys.exit(f"Gagal terhubung: {type(e.reason).__name__}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["profile", "keyword"])
    ap.add_argument("--username", help="wajib untuk mode profile (exact match)")
    ap.add_argument("--q", help="wajib untuk mode keyword")
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--pages", type=int, default=1, help="jumlah halaman maksimum")
    ap.add_argument("--since")
    ap.add_argument("--until")
    ap.add_argument("--out", help="default: data/<mode>_<target>.json")
    a = ap.parse_args()

    token = os.environ.get("THREADS_TOKEN")
    if not token:
        sys.exit("THREADS_TOKEN belum diset. PowerShell: $env:THREADS_TOKEN = '...'")
    if a.mode == "profile" and not a.username:
        sys.exit("--username wajib untuk mode profile")
    if a.mode == "keyword" and not a.q:
        sys.exit("--q wajib untuk mode keyword")

    params = {"fields": FIELDS[a.mode], "limit": a.limit, "access_token": token}
    params["username" if a.mode == "profile" else "q"] = a.username or a.q
    for k in ("since", "until"):
        if getattr(a, k):
            params[k] = getattr(a, k)

    posts, after = [], None
    for page in range(a.pages):
        if after:
            params["after"] = after
        res = get(f"{BASE}/{ENDPOINT[a.mode]}?{urllib.parse.urlencode(params)}")
        posts += res.get("data", [])
        after = res.get("paging", {}).get("cursors", {}).get("after")
        print(f"halaman {page + 1}: {len(res.get('data', []))} post")
        if not after or not res.get("paging", {}).get("next"):
            break

    target = a.username or a.q
    out = Path(a.out or f"data/{a.mode}_{target}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    # hanya 'data'; paging/next dibuang karena memuat token
    out.write_text(json.dumps({"data": posts, "deleted_ids": []}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(posts)} post ditulis ke {out}")
    if "data" not in out.parts:
        print("PERINGATAN: berkas di luar data/ tidak di-gitignore", file=sys.stderr)


if __name__ == "__main__":
    main()
