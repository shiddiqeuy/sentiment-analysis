# Sentiment Analysis Threads

Riset dan perancangan sistem internal untuk menganalisis sentimen publik di Meta Threads terhadap produk dan kategori produk milik organisasi. Tahap saat ini: riset dan verifikasi akses data. Kode baru berupa prototype throwaway dan skrip ekspor (lihat Perkakas).

## Scope

- Internal, satu tenant.
- Objek: produk sendiri dan tren seputar produk atau kategori produk. Kompetitor masuk tahap 2.
- Data: Threads API resmi (`keyword_search`) dengan daftar keyword tertutup.
- Output: agregat saja (tren sentimen, lonjakan negatif, topik pemicu). Tidak ada profil per akun atau pencarian per orang.
- Di luar scope: isu publik umum, politik, dan tokoh.

Rincian: [docs/scope-statement.md](docs/scope-statement.md).

## Status

| Item | Status |
|---|---|
| Riset kebutuhan, data source, arsitektur, privasi | selesai (draf) |
| Verifikasi poin terbuka Threads API | selesai, sebagian masih terbuka |
| Draf pertanyaan ke Meta | dirapikan, belum dikirim |
| Uji empiris Threads API | fase 0 dan sebagian `keyword_search` selesai (lihat hasil uji) |
| Prototype pipeline | jalan pada data sintetis; belum diuji dengan data nyata |

## Perkakas

Python 3.14, tanpa dependensi (hanya pustaka standar). Semua perintah dari root repo.

| Berkas | Fungsi |
|---|---|
| `tools/export_threads.py` | ekspor post dari Threads API ke `data/*.json` (di-gitignore); token dari `THREADS_TOKEN`, tidak pernah ditulis ke berkas |
| `prototype/pipeline_proto.py` | prototype throwaway: purge, masking, normalisasi, klasifikasi lexicon, agregasi harian, evaluasi |
| `prototype/fixture_posts.json` | 17 post sintetis berbentuk respons Threads, lengkap dengan label `gold` |
| `.env.example` | daftar variabel lingkungan (tanpa nilai) |

```powershell
# 1. jalankan prototype pada data sintetis
python prototype/pipeline_proto.py

# 2. ekspor data nyata (token hanya di sesi shell, jangan di berkas)
$env:THREADS_TOKEN = "..."
python tools/export_threads.py profile --username <akun-sendiri> --limit 25 --pages 2

# 3. jalankan pipeline pada data nyata (tanpa label 'gold', evaluasi dilewati)
python prototype/pipeline_proto.py data/profile_<akun-sendiri>.json
```

Catatan:
- `data/` dan `.env` di-gitignore. Jangan commit data nyata atau token.
- Respons `profile_posts` memuat URL `paging.next` yang berisi token; skrip ekspor membuangnya. Jangan menyimpan respons mentah.
- Host default `graph.threads.com` mengikuti dokumentasi; di Graph API Explorer host `graph.threads.net` terbukti bekerja. Ubah lewat `THREADS_API_BASE`.
- Nama field di `export_threads.py` sebagian asumsi; yang terverifikasi ada di `docs/research/threads-api-test-results.md`.
- `keyword` hanya mengembalikan post akun sendiri sebelum App Review disetujui.
- Skrip ekspor belum pernah dijalankan terhadap API; hanya diuji bahwa ia berhenti aman tanpa token.

## Dokumen

| Berkas | Isi |
|---|---|
| [docs/scope-statement.md](docs/scope-statement.md) | keputusan scope dan batasan desain |
| [docs/research/threads-sentiment-analysis.md](docs/research/threads-sentiment-analysis.md) | riset kebutuhan, data source, arsitektur, privasi dan legal |
| [docs/research/threads-api-open-questions.md](docs/research/threads-api-open-questions.md) | verifikasi poin terbuka Threads API |
| [docs/meta-support-questions.md](docs/meta-support-questions.md) | draf pertanyaan untuk Meta Developer Support |
| [docs/test-plan-keyword-search.md](docs/test-plan-keyword-search.md) | rencana uji empiris `keyword_search` |

## Temuan kunci

- Keyword search resmi tersedia dengan izin `threads_keyword_search`: maksimum 2.200 query per 24 jam, 100 hasil per request.
- Tidak ada endpoint trending yang terdokumentasi; tren dideteksi sendiri dari volume keyword dan `topic_tag`.
- Scraping dilarang tanpa izin tertulis Meta.
- Deteksi post terhapus untuk hasil pencarian publik tidak didokumentasikan.
- Boleh tidaknya fine-tuning dengan data Threads belum jelas di Platform Terms.
- UU PDP No. 27/2022 kemungkinan berlaku; DPIA diperlukan sebelum produksi.

## Langkah berikutnya

1. Tinjau dan kirim [draf pertanyaan ke Meta](docs/meta-support-questions.md).
2. Jalankan [uji empiris](docs/test-plan-keyword-search.md) dengan app dan akun sendiri.
3. Prototype pipeline kecil (ingest, masking, model IndoBERT siap pakai, penyimpanan agregat).
4. DPIA dan keputusan legal oleh pemilik proyek.

## Konvensi

- Bahasa Indonesia; nama berkas Inggris huruf kecil dengan tanda hubung.
- Klaim ditandai `fakta | asumsi | usulan | terbuka`; klaim fakta mencantumkan sumber primer dan tanggal akses.
- Jangan menyimpan token, secret, atau data pribadi di repo. Token hanya lewat variabel lingkungan.
- Dokumen riset bukan nasihat hukum.
