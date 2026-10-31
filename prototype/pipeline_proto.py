"""PROTOTYPE (throwaway): pipeline sentimen Threads dari ingest sampai laporan.

Pertanyaan: apakah alur ingest -> masking -> klasifikasi -> agregasi berjalan
utuh pada data berbentuk respons Threads, dan di mana lexicon sederhana gagal?
Data sintetis (fixture_posts.json). Tanpa jaringan, tanpa unduhan model.

Jalankan: python prototype/pipeline_proto.py
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent

# ---------- 1. ingest ----------
def ingest(path):
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return raw["data"], set(raw.get("deleted_ids", []))

# ---------- 2. hapus konten yang sudah dihapus pengguna ----------
def purge_deleted(posts, deleted_ids):
    kept = [p for p in posts if p["id"] not in deleted_ids]
    return kept, len(posts) - len(kept)

# ---------- 3. masking PII ----------
RE_URL = re.compile(r"https?://\S+")
RE_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")
RE_PHONE = re.compile(r"(?<!\d)(?:\+62|62|0)8\d{8,11}(?!\d)")
RE_MENTION = re.compile(r"@\w+")

def mask(text):
    text = RE_URL.sub("[URL]", text)
    text = RE_EMAIL.sub("[EMAIL]", text)
    text = RE_PHONE.sub("[TELP]", text)
    text = RE_MENTION.sub("@USER", text)
    return text

# ---------- 4. normalisasi ----------
SLANG = {"bgt": "banget", "gak": "tidak", "ga": "tidak", "nggak": "tidak",
         "tdk": "tidak", "nyesel": "menyesal", "makasih": "terima kasih",
         "yg": "yang", "udh": "sudah", "aja": "saja"}

def normalize(text):
    text = text.lower()
    text = re.sub(r"(.)\1{2,}", r"\1", text)  # baguuus -> bagus
    tokens = re.findall(r"[a-z\[\]@']+", text)
    return [SLANG.get(t, t) for t in tokens]

# ---------- 5. klasifikasi (antarmuka pluggable) ----------
POS = {"bagus", "baik", "enak", "suka", "mantap", "puas", "murah", "hebat",
       "recommended", "lumayan", "terjangkau", "terima", "salut"}
NEG = {"jelek", "buruk", "kecewa", "mengecewakan", "lambat", "mahal", "rusak",
       "parah", "menyesal", "komplain", "telat", "biasa"}
NEGATORS = {"tidak", "bukan", "belum", "kurang"}

class LexiconClassifier:
    """Baseline lexicon. Mengembalikan (label, skor)."""
    name = "lexicon"

    def predict(self, tokens):
        score, flip = 0, False
        for t in tokens:
            if t in NEGATORS:
                flip = True
                continue
            val = 1 if t in POS else -1 if t in NEG else 0
            if val:
                score += -val if flip else val
                flip = False
        label = "positif" if score > 0 else "negatif" if score < 0 else "netral"
        return label, score

class IndoBertClassifier:
    """Placeholder: tidak diaktifkan di prototype (butuh unduhan model).
    Antarmuka sama: predict(tokens) -> (label, skor). Isi nanti bila diizinkan."""
    name = "indobert"

    def predict(self, tokens):
        raise NotImplementedError("model belum diunduh; lihat catatan di README")

# ---------- 6. agregasi ----------
def aggregate(rows):
    daily = defaultdict(Counter)
    tags = defaultdict(Counter)
    for r in rows:
        day = r["timestamp"][:10]
        daily[day][r["pred"]] += 1
        tags[r["topic_tag"]][r["pred"]] += 1
    return daily, tags

def spike(counter, min_n=4, thr=0.6):
    n = sum(counter.values())
    return n >= min_n and counter["negatif"] / n >= thr

# ---------- 7. evaluasi ----------
def evaluate(rows):
    labels = ["positif", "negatif", "netral"]
    correct = sum(r["pred"] == r["gold"] for r in rows)
    conf = {g: Counter() for g in labels}
    for r in rows:
        conf[r["gold"]][r["pred"]] += 1
    return correct, conf, [r for r in rows if r["pred"] != r["gold"]]

# ---------- jalankan ----------
def main():
    clf = LexiconClassifier()
    src = sys.argv[1] if len(sys.argv) > 1 else HERE / "fixture_posts.json"
    posts, deleted = ingest(src)
    print(f"[input]  {src}")
    print(f"[ingest] {len(posts)} post, {len(deleted)} ditandai terhapus")

    posts, n_purged = purge_deleted(posts, deleted)
    print(f"[purge]  {n_purged} post terhapus dibuang dari penyimpanan")

    rows = []
    for p in posts:
        masked = mask(p["text"])
        pred, score = clf.predict(normalize(masked))
        # username sengaja tidak dibawa ke tahap berikutnya (hanya agregat)
        rows.append({"id": p["id"], "timestamp": p["timestamp"],
                     "topic_tag": p.get("topic_tag") or "(tanpa tag)",
                     "masked": masked, "pred": pred, "score": score, "gold": p.get("gold")})

    print("\n[masking] contoh sebelum -> sesudah")
    by_id = {p["id"]: p for p in posts}
    for r in rows:
        if r["masked"] != by_id[r["id"]]["text"]:
            print(f"  {r['id']}: {by_id[r['id']]['text']}\n        -> {r['masked']}")

    daily, tags = aggregate(rows)
    print(f"\n[agregat harian] classifier={clf.name}")
    print(f"  {'tanggal':<12}{'pos':>4}{'neg':>5}{'net':>5}{'total':>6}  net_sentimen  spike")
    for day in sorted(daily):
        c = daily[day]
        n = sum(c.values())
        net = (c["positif"] - c["negatif"]) / n
        print(f"  {day:<12}{c['positif']:>4}{c['negatif']:>5}{c['netral']:>5}{n:>6}  {net:>+11.2f}  {'YA' if spike(c) else '-'}")

    print("\n[per topic_tag]")
    for tag, c in sorted(tags.items()):
        print(f"  {tag:<8} pos={c['positif']} neg={c['negatif']} net={c['netral']}")

    labeled = [r for r in rows if r["gold"]]
    if labeled:
        correct, conf, wrong = evaluate(labeled)
        print(f"\n[evaluasi] akurasi {correct}/{len(labeled)} = {correct/len(labeled):.0%}")
        print("  gold \\ pred   positif negatif netral")
        for g, c in conf.items():
            print(f"  {g:<12}{c['positif']:>8}{c['negatif']:>8}{c['netral']:>7}")
        print("\n[salah klasifikasi]")
        for r in wrong:
            print(f"  {r['id']} gold={r['gold']} pred={r['pred']}: {r['masked']}")
    else:
        print("\n[evaluasi] dilewati: input tidak punya label 'gold'")

    try:
        IndoBertClassifier().predict([])
    except NotImplementedError as e:
        print(f"\n[indobert] dilewati: {e}")

if __name__ == "__main__":
    sys.exit(main())
