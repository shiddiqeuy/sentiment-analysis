# Riset lanjutan: pertanyaan terbuka Threads API

Tanggal riset dan akses semua sumber: **2026-10-31**.
Dasar: `docs/research/threads-sentiment-analysis.md` dan `docs/scope-statement.md` (internal, produk sendiri, kompetitor tahap 2, output agregat, daftar keyword tertutup).

Legenda: **[fakta]** (sumber primer + URL + tanggal akses), **[asumsi]**, **[usulan]**, **[terbuka]** (tidak bisa diverifikasi; jangan dianggap benar).

Catatan metode:
- Halaman dibaca lewat alat fetch yang meringkas isi halaman; kutipan bertanda tanda petik adalah teks Inggris yang dikembalikan alat, bukan salinan manusia. **[terbuka]** Untuk keputusan legal, baca ulang klausul langsung di browser.
- Platform Terms dibaca versi Inggris (`?locale=en_US`). Developer Policies tersaji berbahasa Indonesia (kutipan berupa parafrase alat).
- Pembacaan halaman `permissions` terpotong (113.704 karakter; entri `threads_keyword_search` terbaca dari pembacaan pertama, bagian akhir tidak terbaca semua). Entri yang tidak terlihat ditandai terbuka.
- Hanya sumber primer Meta. Hasil pencarian web hanya dipakai sebagai petunjuk dan ditandai terbuka bila halaman primernya tidak terbaca.
- Bukan nasihat hukum.

---

## 1. Topik/tagar trending di Threads API

**Temuan: tidak ada endpoint trending yang terdokumentasi. Ada topic tag per post dan pencarian tag.**

- **[fakta]** Changelog Threads tidak memuat entri apa pun tentang "trending". Entri terkait topic tag: 14 Jul 2025 (pembuatan post dengan parameter `topic_tag`; Topic Tag Search), 21 Jul 2025 ("The `topic_tag` field was added to the Media retrieval endpoints."). Sumber: https://developers.facebook.com/docs/threads/changelog (diakses 2026-10-31).
- **[fakta]** Halaman keyword search dan media retrieval tidak memuat kata "trending". Sumber: https://developers.facebook.com/documentation/threads/keyword-search.md dan https://developers.facebook.com/documentation/threads/reference/media-retrieval.md (diakses 2026-10-31).
- **[fakta]** Indeks dokumentasi Threads (semua judul halaman) tidak memuat halaman trending. Sumber: https://developers.facebook.com/documentation/threads/llms.txt (diakses 2026-10-31).
- **[fakta]** Topic tag search: "To search for public Threads media by topic tag, send a `GET` request to the `/keyword_search` endpoint with a topic to be queried." dengan `search_mode=TAG`. Sumber: https://developers.facebook.com/documentation/threads/keyword-search.md (2026-10-31).
- **[fakta]** Field `topic_tag` ada di daftar field yang bisa diminta pada `GET /keyword_search` dan `GET /{threads-media-id}`. Halaman tidak menjelaskan isi/format field (satu tag per post atau lebih). Sumber: https://developers.facebook.com/documentation/threads/reference/media-retrieval.md (2026-10-31).
- **[fakta]** `TOP` hanya dijelaskan sebagai hasil "paling populer"; kriteria peringkat tidak dinyatakan. Sumber: https://developers.facebook.com/documentation/threads/keyword-search.md (2026-10-31).
- **[terbuka]** Pencarian web menunjukkan halaman pemetaan use case Meta menyebut "Threads Trending Topics" sebagai izin opsional pada use case "Access the Threads API" (halaman bertanggal pembaruan 29 Agu 2025 menurut ringkasan pencarian). Halaman primer https://developers.facebook.com/documentation/development/create-an-app/use-cases-permission-mapping terbaca tanpa tabel (hanya judul dan pengantar) sehingga **tidak terverifikasi**; entri izin itu tidak ditemukan di halaman permissions yang terbaca (bagian terbaca mencakup entri `threads_*` lain; ada bagian akhir yang tidak terbaca). Tidak diketahui apa yang diberikan izin itu, endpointnya, atau syarat reviunya. Jangan merancang di atasnya sebelum terbaca langsung oleh manusia.
- **[fakta]** Fitur Trending Topics ada di aplikasi Threads sebagai fitur pengguna (liputan pers 2024) — bukan sumber primer API; tidak dipakai sebagai dasar fakta. Status: **[terbuka]**.

Cara mendeteksi tren dengan yang tersedia:

- **[usulan]** Deteksi tren sendiri dari lonjakan volume per keyword (`search_type=RECENT`, `since`/`until` per jam) pada daftar tertutup milik kita. Selaras dengan scope: tren hanya seputar produk/kategori.
- **[usulan]** Pakai `topic_tag` pada post hasil pencarian sebagai fitur topik: hitung frekuensi tag per hari, lalu cari tag yang melonjak (agregat). Tag baru yang muncul tidak otomatis bisa ditemukan karena `search_mode=TAG` butuh tag sebagai input; penemuan tag baru hanya dari field `topic_tag` pada hasil keyword kita.
- **[asumsi]** `topic_tag` terisi hanya pada sebagian post (tidak semua post punya tag). Perlu diukur.
- **[terbuka]** Apakah `search_type=TOP` berguna sebagai proksi "sedang ramai"; tidak ada kriteria resmi.
- Implikasi scope: pernyataan scope "[terbuka] Apakah Threads API menyediakan daftar topik trending" dapat dijawab sementara: **tidak ditemukan di dokumentasi resmi** (kecuali butir izin "Trending Topics" di atas, belum terverifikasi).

---

## 2. App Review `threads_keyword_search`

- **[fakta]** Izin ini "allows a business app to search and fetch content with a specific keyword on behalf of a Threads user." Penggunaan yang diizinkan: "to help the user manage their social media presence"; contoh poin: "Showing public content and the public content tree that a business app user searches using a specific keyword." Dilarang: "using threads_keyword_search permission in a consumer app is strictly prohibited." Sumber: https://developers.facebook.com/documentation/development/permissions (diakses 2026-10-31).
- **[fakta]** Use case description yang diminta: "Provide specific examples of why your app requires the `threads_keyword_search` permission ...". Screencast: tunjukkan proses OAuth Threads lengkap dan "Enter a keyword and demonstrate how to search for public content related to that keyword." Sumber: sama (2026-10-31).
- **[fakta]** Tanpa persetujuan, pencarian hanya atas post milik pengguna terotorisasi; setelah persetujuan, post publik dapat dicari. Sumber: https://developers.facebook.com/documentation/threads/keyword-search.md (2026-10-31).
- **[fakta]** Untuk izin Threads umum: "each permission must first be approved through the App Review process, and your app must be published." Sumber: https://developers.facebook.com/documentation/threads/get-started.md (2026-10-31).
- **[fakta]** App Review wajib bila ada orang tanpa peran di app atau di Business yang mengklaim app memakainya; bila hanya orang ber-peran, "App Review is not required." Meta menguji app; bila app tak dapat diakses untuk diuji, seluruh pengajuan ditolak. Sumber: https://developers.facebook.com/docs/resp-plat-initiatives/individual-processes/app-review (2026-10-31).
- **[fakta]** Business Verification: "Advanced Access now requires Business Verification" (sejak 1 Feb 2023); tidak perlu bila hanya orang ber-peran di app. Halaman tidak menyebut estimasi waktu pemrosesan. Sumber: https://developers.facebook.com/documentation/development/release/business-verification (2026-10-31).
- **[fakta]** Halaman Access Verification menyatakan verifikasi itu "no longer required" (hanya untuk referensi) dan menyebut bisnis pemilik app yang dipakai bisnis lain harus diverifikasi sebagai Tech Provider; daftar izinnya memuat `threads_basic`, `threads_content_publish`, `threads_keyword_search`, `threads_manage_insights`, `threads_manage_mentions`, `threads_manage_replies`, `threads_read_replies`. Verifikasi itu independen dari App Review. Sumber: https://developers.facebook.com/documentation/development/release/access-verification.md (2026-10-31). Catatan: status "no longer required" membuat relevansi Tech Provider untuk saat ini **[terbuka]**.
- **[fakta]** Halaman webhook: untuk non-Tech Provider app harus Live Mode; untuk Tech Provider perlu Advanced Access. Sumber: https://developers.facebook.com/docs/threads/webhooks (2026-10-31). Ini menunjukkan Meta membedakan Tech Provider vs non-Tech Provider di Threads, tetapi hanya untuk webhook.
- **[terbuka]** Estimasi waktu App Review: tidak ada angka di sumber primer yang dibaca (halaman App Review dasar, business verification, permissions).
- **[terbuka]** Apakah analisis internal/brand monitoring diterima. Teks izin menyebut tujuan "manage their social media presence" dan contoh "show public content searched by keyword". Brand monitoring dengan keyword adalah kecocokan yang masuk akal **[asumsi]** tetapi tidak dinyatakan eksplisit; bukan jaminan. "Consumer app" dilarang; app internal bukan consumer app **[asumsi]**.
- **[terbuka]** Apakah mengagregasi hasil keyword untuk merek kompetitor (tahap 2) termasuk "manage social media presence". Izin `threads_profile_discovery` menyebut eksplisit "to conduct competitor analyses" (https://developers.facebook.com/docs/permissions, 2026-10-31), sedangkan izin keyword search tidak menyebut kompetitor. Pada akses standar `profile_lookup` hanya untuk akun resmi Meta (lihat riset awal), jadi bukan jalur kompetitor yang praktis **[terbuka]**.
- **[terbuka]** Apakah app yang dijalankan satu tim tanpa orang luar dapat memakai `threads_keyword_search` publik tanpa App Review hanya dengan akun ber-peran (Tester/Developer). Aturan umum App Review (butir di atas) menyiratkan ya, tetapi dokumen keyword search menyatakan hasil publik baru muncul "After approval". Perlu uji langsung.
- **[usulan]** Siapkan: use case "monitoring sentimen publik terhadap produk sendiri berdasar daftar keyword tertutup, agregat, internal"; screencast OAuth + masukkan keyword + tampilkan hasil publik (dashboard agregat bila perlu); Privacy Policy, URL penghapusan data. Posisikan sebagai alat bisnis internal, bukan aplikasi konsumen.
- **[usulan]** Uji dulu dengan akun ber-peran di Graph API Explorer untuk mengetahui apakah hasil publik terbaca tanpa review.

---

## 3. Post yang dihapus pengguna

- **[fakta]** Ada webhook `delete` (field di topik `moderate`): menandai "Threads posts that were deleted by the authenticated user." Syarat: sub-use case webhook, field `delete` disubscribe, izin `threads_basic` + `threads_delete`, bisnis terhubung terverifikasi, non-Tech Provider app Live Mode / Tech Provider Advanced Access, pemilik media akun publik atau privat yang terautentikasi ke app. Payload: `target_id`, `values.value.id`, `owner.owner_id`, `deleted_at` (ISO 8601), `timestamp`, `username`. Sumber: https://developers.facebook.com/docs/threads/webhooks (2026-10-31).
- **[fakta]** Changelog: "Support for delete webhooks has been added." (1 Agu 2025). Sumber: https://developers.facebook.com/docs/threads/changelog (2026-10-31).
- **[fakta]** Penghapusan via API: `DELETE /{threads-media-id}` oleh pembuat post, 100 hapus/hari/akun; respons `success` dan `deleted_id`. Sumber: https://developers.facebook.com/documentation/threads/posts/delete-posts.md (2026-10-31).
- **[terbuka]** Webhook `delete` hanya untuk post milik pengguna yang mengotorisasi app kita. Dokumen tidak menyatakan apa pun untuk penghapusan post pihak lain yang ditemukan lewat keyword search. Untuk skenario kita, **tidak ada notifikasi resmi** yang terverifikasi.
- **[terbuka]** Cara memeriksa keberadaan post: halaman media retrieval, delete posts, dan troubleshooting tidak menyebut kode/respons error untuk media yang dihapus atau tidak ada ("Deleted: Not mentioned"). Sumber: https://developers.facebook.com/documentation/threads/reference/media-retrieval.md, https://developers.facebook.com/documentation/threads/troubleshooting.md (2026-10-31). Perilaku nyata `GET /{media-id}` untuk post terhapus perlu diuji empiris (buat post uji, hapus, panggil ulang, catat kode galat).
- **[terbuka]** Apakah `GET /{media-id}` boleh dipakai untuk post publik milik orang lain (tidak dinyatakan); lihat juga izin `threads_read_replies` di bawah.
- **[terbuka]** Perilaku balasan setelah post induk dihapus: tidak dinyatakan di halaman webhook dan delete.
- **[usulan]** Karena tidak ada sinyal resmi, jadwalkan job "cek ulang keberadaan" untuk sampel/seluruh post berusia sampai N hari (mis. 30) lewat `GET /{media-id}?fields=id`; anggap galat "tidak ditemukan" sebagai terhapus (hanya setelah perilaku diuji). Hitung beban terhadap batas 4.800 x impresi per 24 jam (lihat riset awal) **[asumsi]**.
- **[usulan]** Pasangkan dengan retensi pendek untuk teks mentah (mis. 30 hari) dan simpan hanya agregat/skor turunan lebih lama.

Kewajiban penghapusan menurut Meta Platform Terms (sumber: https://developers.facebook.com/terms/dfc_platform_terms/?locale=en_US, 2026-10-31; teks Inggris sesuai ringkasan alat):

- **[fakta]** 3.d.i.1: "Update or delete Platform Data promptly after receiving a request from us or the User to do so and give Users an easily accessible and clearly marked way to ask for their Platform Data to be modified or deleted."
- **[fakta]** 3.d.i.2: "Delete all Platform Data as soon as reasonably possible in the following cases:" (a) "When retaining the Platform Data is no longer necessary for a legitimate business purpose that is consistent with these Terms and all other applicable terms and policies;" (b) bila layanan penghimpun data dihentikan; (c) bila Meta meminta demi perlindungan pengguna; (d) "When a User requests their Platform Data be deleted or no longer has an account with you (unless the Platform Data has been aggregated, obscured, or de-identified so that it cannot be associated with a particular User, browser, or device) ..."; (e) bila diwajibkan hukum; (f) sesuai Bagian 7.
- **[fakta]** 3.d.iii: data yang diterima karena kesalahan wajib dilaporkan dan dihapus.
- **[fakta]** Definisi Platform Data (12.l) mencakup "data anonymized, aggregated, or derived from such data." Artinya data turunan tetap berstatus Platform Data; hanya kewajiban hapus pada 3.d.i.2.d yang punya pengecualian agregasi/de-identifikasi.
- **[fakta]** Batas retensi angka (mis. 30/90 hari): tidak ada di teks yang dibaca; satu-satunya standar adalah "no longer necessary for a legitimate business purpose" (3.d.i.2.a). Maka batas angka adalah keputusan kita **[usulan]**; angka final **[terbuka]** untuk pemilik keputusan legal.
- **[terbuka]** Apakah "request from us or the User" mencakup hapus-di-sumber (post dihapus pengguna di Threads) secara otomatis. Teks tidak menyatakan; praktik aman: perlakukan penghapusan di sumber sebagai permintaan hapus **[usulan]**.
- **[fakta]** Kewajiban terpisah: Privacy Policy harus menjelaskan cara meminta penghapusan (4.b menurut riset awal) dan aset publish app memerlukan URL/callback penghapusan data. Sumber: https://developers.facebook.com/documentation/threads/get-started/create-an-app.md (diakses 2026-10-31, dari riset awal).

---

## 4. Pelatihan/fine-tuning model dan analisis agregat

Sumber utama: https://developers.facebook.com/terms/dfc_platform_terms/?locale=en_US (diakses 2026-10-31, halaman berbahasa Inggris).

- **[fakta]** Kata kunci "machine learning", "artificial intelligence", "train", "model", "large language model", "LLM" **tidak muncul** di teks Platform Terms yang dibaca. Tidak ada klausul eksplisit yang mengizinkan atau melarang pelatihan model.
- **[fakta]** 3.a.viii: "Processing Platform Data for purposes other than the applicable permitted purposes set forth in Meta's Developer Docs." Ini larangan yang paling relevan: pelatihan model diizinkan hanya bila termasuk tujuan yang diizinkan di Developer Docs.
- **[fakta]** 3.a.iv: "Selling, licensing, or purchasing Platform Data." Model/dataset yang dibagikan atau dijual ke pihak lain berisiko masuk larangan ini **[asumsi]** (penafsiran).
- **[fakta]** 3.a.v: "Processing Platform Data without valid User consent in order to build or augment user profiles for any purpose."
- **[fakta]** 3.a.iii: "Processing Platform Data to perform, facilitate, or provide tools for surveillance. Surveillance includes the Processing of Platform Data about people, places, groups, or events for law enforcement or national security purposes." (definisi sempit: penegakan hukum/keamanan nasional; koreksi atas pembacaan riset awal yang lebih luas).
- **[fakta]** 3.a.i (diskriminasi) dan 3.a.ii (keputusan kelayakan) berlaku seperti di riset awal. 3.a.vi dilarang re-identifikasi/de-anonimisasi. 3.a.vii: mengubah fungsi inti app atau lingkup pemrosesan data tanpa App Review ulang dilarang; relevan saat menambah kompetitor tahap 2 atau pelatihan model setelah app disetujui **[asumsi]**.
- **[fakta]** Developer Policies (halaman berbahasa Indonesia; ringkasan alat): tidak ditemukan teks tentang AI/ML, pelatihan model, scraping, atau "Platform Data". Ada butir 10.7 terkait data iklan (agregat dan anonim saja; jangan buat/perluas profil pengguna) yang berlaku pada data iklan, bukan terbukti untuk Threads. Sumber: https://developers.facebook.com/devpolicy/ (2026-10-31). **[terbuka]** karena halaman tidak berbahasa Inggris dan terbaca lewat ringkasan.
- **[fakta]** Izin `threads_read_replies`: boleh dipakai untuk "analytics insights" dan pemasaran/iklan, "but only with aggregated, de-identified, or anonymized data" (menurut bagian terbaca; teks awal entri tidak terlihat). Sumber: https://developers.facebook.com/documentation/development/permissions (2026-10-31). Ini satu-satunya petunjuk eksplisit tentang analitik agregat; berlaku untuk izin balasan, bukan untuk `threads_keyword_search` **[terbuka]** apakah syarat serupa berlaku untuk keyword search.
- **[fakta]** Izin `threads_read_replies` allowed usage: "Get replies to a thread owned by the business app user." Ini menjawab sebagian pertanyaan riset awal: balasan resmi hanya untuk thread milik pengguna app, bukan post publik milik orang lain. Sumber: sama (2026-10-31). Maka `conversation`/`replies` untuk post publik hasil pencarian **tidak** didukung oleh izin ini **[asumsi]** (tafsir dari allowed usage), rencana tahap 2 yang memakainya perlu direvisi.
- **[fakta]** Analisis agregat atas Platform Data: tidak ada larangan eksplisit; kewajiban hapus berlaku untuk data yang bisa dikaitkan ke pengguna, dengan pengecualian untuk data yang "aggregated, obscured, or de-identified" (3.d.i.2.d). Output agregat sesuai scope tidak bertentangan dengan teks ini, tetapi data mentah dan skor per post tetap Platform Data (12.l).
- **[asumsi]** Analisis sentimen (klasifikasi per post, lalu agregasi) adalah "pemrosesan untuk tujuan yang diizinkan" bila sesuai deskripsi use case yang disetujui; melatih/fine-tune model dengan teks Threads adalah pemrosesan tambahan yang tidak dibahas **[terbuka]**.
- **[usulan]** Hingga ada jawaban tertulis dari Meta: (a) inferensi memakai model yang dilatih dari data publik non-Threads (SmSA, EmoT, NusaX); (b) label Threads dipakai hanya untuk evaluasi internal, bukan fine-tuning, atau fine-tuning dilakukan setelah konfirmasi; (c) model hasil tidak dibagikan/dijual; (d) jangan kirim teks mentah Threads ke API LLM pihak ketiga tanpa menimbang 3.a.iv dan syarat Service Provider (3.d.i). Syarat tentang Service Providers pada 3.d.i ("make reasonable efforts to ensure your Service Providers") adalah fakta teks intro 3.d.i.
- **[terbuka]** Klausul lain di Platform Terms yang belum dibaca penuh (mis. definisi "permitted purposes" di Developer Docs per izin). Baca manual seluruh dokumen.

---

## 5. Detail `keyword_search`

Sumber: https://developers.facebook.com/documentation/threads/keyword-search.md dan https://developers.facebook.com/docs/threads/keyword-search (diakses 2026-10-31), kecuali dinyatakan lain.

| Aspek | Temuan | Tag |
|---|---|---|
| Endpoint | `GET /keyword_search` | fakta |
| `q` | wajib; "The keyword(s) to be queried." | fakta |
| `search_type` | `TOP` (default, paling populer) atau `RECENT` | fakta |
| `search_mode` | `KEYWORD` (default) atau `TAG` (topic tag) | fakta |
| `media_type` | `TEXT`, `IMAGE`, `VIDEO`; bila kosong, semua tipe. Ditambahkan 9 Sep 2025 (changelog) | fakta |
| `since` | Unix timestamp atau `strtotime()`; harus >= `1688540400` dan < `until` | fakta |
| `until` | format sama; harus <= waktu sekarang dan > `since` | fakta |
| `limit` | default 25, maks 100; hanya angka non-negatif | fakta |
| `author_username` | tepat, tanpa `@`; ditambahkan 20 Jan 2026 (changelog) | fakta |
| Field hasil | `id` (default), `media_product_type`, `media_type`, `media_url`, `permalink`, `username`, `text`, `timestamp`, `shortcode`, `thumbnail_url`, `children`, `is_quote_post`, `alt_text`, `link_attachment_url`, `has_replies`, `is_reply`, `root_post`, `replied_to`, `reply_audience`, `quoted_post`, `reposted_post`, `gif_url`, `poll_attachment`, `topic_tag` (sumber field: media-retrieval.md) | fakta |
| Field tidak dikembalikan | `owner`, `is_reply_owned_by_me`, `hide_status`, `is_spoiler_media`, `text_entities`, `text_attachment`, `location_id` | fakta |
| Batas | 2.200 query per 24 jam rolling per pengguna lintas app; query berulang tetap dihitung; query tanpa hasil tidak dihitung; keyword dan tag memakai endpoint dan batas yang sama | fakta |
| Perubahan batas | changelog 25 Jun 2025: "The query limit for keyword search has been changed." (nilai sebelumnya tidak dinyatakan) | fakta |
| Keyword sensitif/ofensif | "returns an empty array" | fakta |
| Riwayat pencarian | field `recently_searched_keywords` pada `/me` (`query`, `timestamp` ms) | fakta |
| Paginasi | halaman keyword search dan media retrieval **tidak** menyebut cursor/paging; hanya `limit` | fakta (ketiadaan di dokumen) |
| Paginasi nyata | apakah respons memuat `paging` dan seberapa dalam | terbuka (uji langsung) |
| Jendela waktu pencarian | hanya batas bawah `since` >= `1688540400` (2023-07-05 menurut konversi sendiri) dan atas "sekarang"; jangkauan efektif ke belakang tidak dinyatakan | terbuka |
| Peringkat `TOP` | tidak dinyatakan | terbuka |
| Daftar keyword sensitif | tidak dipublikasikan; bagaimana membedakan "tidak ada hasil" dari "disaring" tidak dinyatakan | terbuka |
| Perilaku `since`/`until` bersama `RECENT` untuk windowing per jam | tidak dinyatakan | terbuka |

Catatan:
- **[fakta]** Untuk paginasi, endpoint lain (user posts/mentions) memakai cursor `before`/`after` tanpa `next`/`previous`, jadi tautan dibangun sendiri. Sumber: https://developers.facebook.com/documentation/threads/retrieve-and-discover-posts.md (2026-10-31). Tidak terbukti berlaku untuk keyword search.
- **[usulan]** Bila paginasi tidak tersedia, hindari tergantung `limit=100` saja: potong jendela waktu dengan `since`/`until` kecil (mis. per jam) per keyword untuk mengambil lebih banyak hasil, dengan konsekuensi hitungan query. Perlu eksperimen: jumlah hasil maksimum per jendela, apakah tumpang tindih/duplikat, perilaku `TOP` vs `RECENT`.
- **[usulan]** Perhitungan kuota: 2.200 query/hari lintas semua app per pengguna. Dengan 20 keyword x polling per jam = 480 query/hari (hanya satu halaman per query); kompetitor tahap 2 menambah linear **[asumsi]** aritmetika sendiri.
- **[usulan]** Kata kunci merek yang tergolong sensitif dapat tersaring sebagai array kosong; pantau keyword yang selalu kosong dan catat sebagai anomali.

---

## 6. Tabel ringkasan

| # | Pertanyaan | Jawaban singkat | Status | Sumber |
|---|---|---|---|---|
| 1a | Ada endpoint/tagar trending? | Tidak ditemukan di dokumentasi, changelog, atau indeks halaman | fakta (ketiadaan di dokumen yang dibaca) | https://developers.facebook.com/docs/threads/changelog ; https://developers.facebook.com/documentation/threads/llms.txt |
| 1b | Izin "Threads Trending Topics"? | Disebut hasil pencarian sebagai izin opsional; tidak terverifikasi dari halaman primer | terbuka | https://developers.facebook.com/documentation/development/create-an-app/use-cases-permission-mapping |
| 1c | Deteksi tren dengan fitur yang ada | `topic_tag` per post, `search_mode=TAG`, lonjakan volume keyword sendiri | fakta (fitur) + usulan (metode) | https://developers.facebook.com/documentation/threads/keyword-search.md ; https://developers.facebook.com/documentation/threads/reference/media-retrieval.md |
| 2a | Isi pengajuan App Review keyword search | Deskripsi use case dengan contoh spesifik + screencast OAuth dan pencarian keyword | fakta | https://developers.facebook.com/documentation/development/permissions |
| 2b | Use case diterima? | Allowed: "manage their social media presence"; dilarang di consumer app; brand monitoring internal tidak disebut | terbuka | https://developers.facebook.com/documentation/development/permissions |
| 2c | Business Verification/Advanced Access | Advanced Access butuh Business Verification; tidak perlu bila hanya orang ber-peran | fakta | https://developers.facebook.com/documentation/development/release/business-verification |
| 2d | Tech Provider | Untuk app yang dipakai bisnis lain; halaman menyatakan "no longer required"; relevansi saat ini | terbuka (sebagian fakta) | https://developers.facebook.com/documentation/development/release/access-verification.md |
| 2e | Estimasi waktu review | Tidak ada angka | terbuka | (tidak ada) |
| 3a | Webhook/field untuk post terhapus | `delete` webhook hanya untuk post pengguna yang mengotorisasi app | fakta | https://developers.facebook.com/docs/threads/webhooks |
| 3b | Deteksi hapus pada hasil pencarian publik | Tidak ada mekanisme terdokumentasi; respons `GET` untuk post hilang tidak dinyatakan | terbuka | https://developers.facebook.com/documentation/threads/troubleshooting.md |
| 3c | Kewajiban hapus Platform Terms | Hapus saat diminta Meta/pengguna, tidak lagi perlu, dsb.; pengecualian agregat/de-identifikasi pada 3.d.i.2.d | fakta | https://developers.facebook.com/terms/dfc_platform_terms/?locale=en_US |
| 3d | Batas retensi angka | Tidak ada; hanya "no longer necessary for a legitimate business purpose" | fakta (ketiadaan) + keputusan kita | sama |
| 4a | Pelatihan/fine-tuning ML diizinkan? | Tidak dibahas; kata kunci ML/AI/train tidak ada; 3.a.viii membatasi pada tujuan yang diizinkan di Developer Docs | terbuka | sama |
| 4b | Analisis agregat | Tidak dilarang; agregat dikecualikan hanya dari kewajiban hapus 3.d.i.2.d; data turunan tetap Platform Data (12.l) | fakta | sama |
| 4c | Balasan untuk post orang lain | `threads_read_replies`: hanya thread milik pengguna app | fakta | https://developers.facebook.com/documentation/development/permissions |
| 5a | Parameter keyword_search | `q`, `search_type`, `search_mode`, `media_type`, `since`, `until`, `limit` (maks 100), `author_username` | fakta | https://developers.facebook.com/documentation/threads/keyword-search.md |
| 5b | Field hasil | Lihat tabel bagian 5; `owner` tidak dikembalikan | fakta | https://developers.facebook.com/documentation/threads/reference/media-retrieval.md |
| 5c | Paginasi | Tidak didokumentasikan | terbuka | https://developers.facebook.com/documentation/threads/keyword-search.md |
| 5d | Jendela waktu | `since` >= 1688540400, `until` <= sekarang; jangkauan efektif tidak dinyatakan | fakta (batas) + terbuka (jangkauan) | sama |
| 5e | Keyword sensitif | Array kosong; daftar tidak dipublikasikan | fakta + terbuka | sama |

---

## 7. Yang tetap terbuka dan siapa/apa yang bisa menjawab

| # | Hal terbuka | Siapa/apa yang bisa menjawab |
|---|---|---|
| 1 | Izin/endpoint "Threads Trending Topics" ada atau tidak, dan apa isinya | Buka manual use-case permission mapping di App Dashboard (Use cases > Access the Threads API); tanya Meta Developer Support |
| 2 | Waktu pemrosesan App Review `threads_keyword_search` | Tanya Meta Developer Support; amati sendiri saat submit; komunitas pengembang bukan sumber primer |
| 3 | Brand monitoring internal dan monitoring kompetitor sesuai "manage social media presence" | Tanya Meta Developer Support secara tertulis dengan deskripsi use case; draf use case lalu submit; pemilik proyek memutuskan risiko |
| 4 | Perlukah Business Verification/Tech Provider untuk app internal satu tim | Uji di App Dashboard (apakah muncul permintaan verifikasi saat meminta Advanced Access); tanya Meta support |
| 5 | Perilaku `GET /{media-id}` pada post terhapus (kode galat) | Uji empiris: buat post uji, hapus, panggil ulang, catat respons |
| 6 | Paginasi, kedalaman hasil, jangkauan waktu efektif, duplikasi, perilaku `TOP`, keyword tersaring | Uji empiris dengan Graph API Explorer setelah akses diberikan |
| 7 | Hasil publik terbaca tanpa App Review untuk akun ber-peran? | Uji empiris di mode pengembangan |
| 8 | Boleh tidaknya pelatihan/fine-tuning dengan data Threads; boleh tidaknya kirim ke LLM pihak ketiga | Konfirmasi tertulis dari Meta Developer Support; pemilik keputusan legal; konsultan hukum |
| 9 | Ketentuan Threads Terms/Supplemental Terms (halaman Help Center tidak terbaca alat) | Manusia membaca manual; penasihat hukum |
| 10 | Developer Policies dan Platform Terms: pembacaan manual atas teks asli (Developer Policies berbahasa Indonesia terbaca lewat ringkasan) | Manusia membaca manual versi Inggris |
| 11 | Retensi angka final untuk teks mentah | Pemilik keputusan legal (pemilik proyek) + konsultan hukum; Meta tidak menetapkan angka |
| 12 | Isi dan format `topic_tag` (satu atau banyak tag; seberapa sering terisi) | Uji empiris pada sampel hasil pencarian |
| 13 | Nilai batas kuota sebelum/sesudah perubahan 25 Jun 2025 | Tidak penting; pakai nilai terkini 2.200/24 jam dan verifikasi pada respons nyata |

Bila diminta mengajukan pertanyaan tertulis ke Meta, rumuskan: (a) apakah hasil `threads_keyword_search` boleh dipakai untuk melatih/fine-tune model sentimen internal; (b) apakah analisis agregat terhadap mention merek pesaing diperbolehkan; (c) bagaimana mendeteksi post terhapus pada hasil keyword search; (d) apakah ada izin/endpoint Trending Topics.
