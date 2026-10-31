# Threads Profile Discovery API (threads_profile_discovery)

Diakses 2026-10-31. Sumber primer dibaca lewat alat fetch yang meringkas, jadi kutipan adalah teks Inggris dari alat (bukan salinan manusia). Bukan nasihat hukum.

Sumber:
- https://developers.facebook.com/documentation/threads/threads-profiles
- https://developers.facebook.com/documentation/threads/retrieve-and-discover-posts/retrieve-posts
- https://developers.facebook.com/documentation/threads/retrieve-and-manage-replies/retrieve-replies
- Deskripsi izin di App Dashboard app `ads-crawler` (Use cases > Access the Threads API > Permissions and features)

## Endpoint dan izin

| Endpoint | Izin | Isi | Tag |
|---|---|---|---|
| `GET /profile_lookup?username=` | `threads_basic` + `threads_profile_discovery` | satu profil publik; username harus exact match | fakta |
| `GET /profile_posts?username=` | `threads_basic` + `threads_profile_discovery` | daftar post publik profil tersebut, berpaginasi | fakta |

- **[fakta]** Field `profile_lookup`: `username`, `name`, `profile_picture_url`, `biography`, `follower_count`, `likes_count`, `quotes_count`, `reposts_count`, `views_count`, `is_verified`. Empat hitungan interaksi adalah agregat 7 hari terakhir.
- **[fakta]** Field `profile_posts`: sama dengan post app-scoped user, kecuali `owner`; antara lain `id`, `media_type`, `permalink`, `username`, `text`, `topic_tag`, `timestamp`. `permalink` dihilangkan bila konten berhak cipta.
- **[fakta]** Contoh request memakai `since`, `until`, `limit`, tetapi tidak ada di tabel parameter; nilai default dan maksimum `limit` tidak disebut. **[terbuka]**
- **[fakta]** Paginasi memakai `paging.cursors` (`before`, `after`); cara pakainya tidak dijelaskan. **[terbuka]**

## Syarat akses

- **[fakta]** Standard access: hanya akun resmi Meta tertentu (@meta, @threads, @instagram, @facebook) yang bisa dicari. Kutipan: "only some of the official Meta accounts can be looked up."
- **[fakta]** Kedua endpoint hanya mengembalikan profil publik dengan minimal 100 followers.
- **[fakta]** Rate limit halaman ini: maksimum 1.000 request per 24 jam bergulir. Dihitung per "user" yang tidak dirinci (app, token, atau akun). **[terbuka]**
- **[terbuka]** Halaman tidak menyebut "App Review", dan tidak menyatakan eksplisit bahwa advanced access menghapus batas akun resmi dan syarat 100 followers; itu hanya tersirat.
- **[fakta, dari halaman posts]** Untuk endpoint post lain, sebelum advanced access `threads_basic` disetujui "only posts created by a Threads tester are retrievable". Halaman `profile_posts` tidak menyatakan aturan ini.

## Larangan dan penggunaan

- **[fakta]** Deskripsi izin di dashboard: untuk menemukan profil dan post publik "to conduct competitor analyses"; tidak untuk tujuan lain; aplikasi konsumen dilarang. (Dashboard, bukan halaman dokumentasi.)
- **[fakta]** Halaman dokumentasi yang dibaca tidak menyebut larangan penggunaan kompetitor atau consumer app.
- **[fakta]** Halaman ini tidak memuat klausul tentang pelatihan ML; lihat `threads-api-open-questions.md` untuk Platform Terms.

## Replies

- **[fakta]** `GET /{threads-user-id}/replies` mengembalikan balasan yang dibuat oleh user tertentu.
- **[terbuka]** Tidak ada endpoint yang terdokumentasi untuk mengambil balasan di bawah post akun publik lain. Analisis sentimen atas reply ke akun kompetitor kemungkinan tidak tersedia.
- **[terbuka]** Halaman replies tidak memuat bagian izin.

## Dampak ke proyek

- **[usulan]** `threads_profile_discovery` cocok untuk tahap 2 (kompetitor) bila akun kompetitor publik dan punya 100+ followers. Cakupan terbatas pada daftar akun yang diketahui, bukan pencarian topik.
- **[usulan]** `threads_keyword_search` tetap diperlukan untuk menangkap mention merek oleh pengguna umum; keduanya saling melengkapi.
- **[usulan]** Rate limit 1.000 request per 24 jam cukup untuk polling beberapa akun kompetitor per hari, tetapi bukan untuk volume besar.
- **[terbuka]** Sebelum advanced access, kemungkinan hanya akun resmi Meta yang bisa diuji; rencana uji T-series perlu disesuaikan: uji `profile_lookup` dengan @meta atau @threads.
