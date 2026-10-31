# Sentiment Analysis Threads

Riset dan perancangan sistem internal untuk menganalisis sentimen publik di Meta Threads terhadap produk dan kategori produk milik organisasi. Tahap saat ini: riset dan verifikasi akses data. Belum ada kode.

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
| Draf pertanyaan ke Meta | siap ditinjau, belum dikirim |
| Uji empiris `keyword_search` | rencana siap, belum dijalankan |
| Prototype pipeline | belum dimulai |

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
