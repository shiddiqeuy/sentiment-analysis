# Scope statement: sentiment analysis Threads

Status: draf. Dasar: `docs/research/threads-sentiment-analysis.md` (bagian 1.1, 2.1, 4). Bukan nasihat hukum.

## Keputusan pemilik (diberikan 2026-10-31)

| # | Pertanyaan | Jawaban | Tag |
|---|---|---|---|
| 1 | Jenis produk | Internal, untuk analisis merek dan kompetitor | fakta (dari pemilik) |
| 2 | Objek pantauan | Produk, atau tren yang sedang trending | fakta (dari pemilik) |
| 3 | Kompetitor di MVP | Tidak perlu | fakta (dari pemilik) |
| 4 | Level scope | B (merek + kompetitor) | fakta (dari pemilik) |
| 5 | Pemilik keputusan legal | Pemilik proyek | fakta (dari pemilik) |

## Penyelarasan (usulan)

- **[usulan]** Poin 3 dan 4 diselaraskan sebagai berikut: arsitektur dirancang untuk scope B, tetapi MVP hanya memantau produk sendiri. Kompetitor masuk tahap 2 lewat penambahan daftar keyword, tanpa perubahan skema.
- **[asumsi]** "Tren yang sedang trending" dibatasi pada tren seputar produk atau kategori produk (mis. kata kunci kategori yang sedang naik). Tren isu publik umum (politik, tokoh) berada di luar scope; itu use case 2 di riset dan berisiko tinggi.
- **[terbuka]** Apakah Threads API menyediakan daftar topik trending. Riset belum memverifikasinya. Bila tidak ada, tren dideteksi sendiri dari lonjakan volume keyword milik kita.

## Scope statement

Sistem internal ini memantau sentimen publik di Threads terhadap produk dan kategori produk milik organisasi, dan pada tahap berikutnya terhadap merek kompetitor, memakai Threads API resmi (keyword search) dengan daftar keyword tertutup yang dikelola tim. Output hanya agregat (tren sentimen, lonjakan negatif, topik pemicu, perbandingan antar merek). Sistem tidak membangun profil per akun, tidak menyediakan pencarian per orang, dan tidak menjual atau melisensikan data. Mention dan identitas dimasking sebelum diproses model, konten yang dihapus pengguna dihapus dari penyimpanan, dan sebelum produksi dilakukan DPIA.

## Batasan desain yang mengikat

1. Output agregat saja; tidak ada tampilan per akun.
2. Keyword dari daftar tertutup, bukan input bebas.
3. Masking username, mention, URL, email, dan nomor sebelum model atau LLM.
4. Job penghapusan konten yang hilang dari Threads.
5. Satu tenant (internal); multi-klien membutuhkan keputusan Tech Provider dan lisensi data lebih dulu.

## Hal yang masih membuka risiko

- Syarat App Review `threads_keyword_search` dan apakah justifikasi "analisis internal" diterima.
- Boleh tidaknya melatih model dengan data Threads (Platform Terms tidak eksplisit).
- Dasar hukum PDP (Pasal 20) untuk post publik; pemilik keputusan legal perlu menetapkan, idealnya dengan konsultan.
