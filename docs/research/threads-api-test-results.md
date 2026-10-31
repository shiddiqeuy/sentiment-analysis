# Hasil uji empiris Threads API, fase 0

Dijalankan 2026-10-31 lewat Graph API Explorer, app `threads-sentiment-analysis` (mode development, akses standard), token user dari akun tester milik pemilik proyek. Semua hasil **[fakta, teramati]**. Token tidak dicatat di berkas ini. Rencana uji: `docs/test-plan-keyword-search.md`.

## Hasil

| # | Uji | Hasil | Tag |
|---|---|---|---|
| P1 | `profile_lookup?username=threads` | Berhasil, 896 ms. Field: `username`, `name`, `profile_picture_url`, `biography`, `is_verified`, `follower_count`, `likes_count`, `quotes_count`, `replies_count`, `reposts_count`, `views_count` | fakta |
| P2 | Field yang kembali | `replies_count` **ada** di respons walau tidak ada di tabel field dokumentasi | fakta |
| P3 | `profile_posts?username=threads&limit=3` tanpa `fields` | Hanya `id` per post; `limit=3` diterima, mengembalikan 3 post | fakta |
| P3b | `profile_posts` dengan `fields=id,media_type,text,topic_tag,timestamp,permalink,username&limit=2` | Berhasil. Mengembalikan `media_type` (TEXT_POST), `permalink`, `text`, `timestamp`, `username`, dan `topic_tag` (hanya pada post yang punya tag; tidak ada di post lain) | fakta |
| P6 | `profile_lookup?username=<akun merek publik non-Meta>` | **Gagal**: error `code 10`, `error_subcode 4279067`, "Application does not have permission for this action", judul "App does not have sufficient access tier" | fakta |

| P4 | Paginasi: `limit=3&fields=id,timestamp&after=<cursor dari respons sebelumnya>` | Berhasil. Halaman berikutnya berisi post berbeda, lebih lama (urut terbaru ke terlama). Respons memuat `paging.cursors.before/after` dan link `previous`/`next` | fakta |
| P5 | `since=2026-10-28&until=2026-10-30&limit=10&fields=id,timestamp` | Diterima dan memfilter. Hanya post tanggal 28 dan 29 Oktober yang kembali; post 30 Oktober tidak ikut (`until` tampak eksklusif pada tanggal tersebut) | fakta |
| P5b | `limit=500&fields=id` | Diterima tanpa error. Jumlah post yang kembali tidak dihitung, jadi batas maksimum sebenarnya belum diketahui | fakta; batas maks = terbuka |

| T2 | `keyword_search?q=kopi` (kata umum, tanpa `author_username`), izin `threads_keyword_search` ditambahkan, mode development | Berhasil, 2,7 detik, mengembalikan daftar `id`. Dengan `fields=username,...`, dua hasil teratas semuanya dari akun tester (`shiddiqazis`), bukan akun lain | fakta |
| T2b | `keyword_search?q=threads&author_username=threads` (filter ke akun lain) | Filter tidak berlaku: semua hasil tetap dari akun tester sendiri. Tidak ada error | fakta |
| T3 | Field di `keyword_search` | `id`, `username`, `timestamp`, `media_type`, `topic_tag`, `has_replies`, `is_quote_post` diterima | fakta |
| T7 (parsial) | Kedalaman riwayat | Post milik sendiri dari 2026-05-26 muncul, jadi riwayat minimal 5 bulan ke belakang | fakta; batas maksimum = terbuka |

## Temuan tambahan

- **[fakta]** Di mode development tanpa App Review, `keyword_search` hanya mengembalikan post milik akun tester sendiri; post akun lain tidak muncul. Ini selaras dengan dokumentasi (riset awal). Untuk memantau percakapan publik tentang produk, App Review dan Advanced Access untuk `threads_keyword_search` wajib.
- **[fakta]** Setelah izin baru ditambahkan, Explorer butuh beberapa kali percobaan dan persetujuan pengguna sebelum token yang mencakup izin itu terbit.

- **[fakta]** Host di Graph API Explorer bernama `threads.net` (mis. `graph.threads.net/v1.0`); dokumentasi menyebut `graph.threads.com`. Explorer menyediakan tombol "Generate Threads Access Token", sehingga token pertama tidak membutuhkan alur OAuth manual.
- **[fakta]** Default `profile_posts` hanya mengembalikan `id`; field lain harus diminta lewat `fields=`.
- **[fakta]** Respons `profile_posts` berisi `paging.cursors` (`before`, `after`) dan URL `next` yang **memuat access token**. Jangan menyimpan, mencatat, atau membagikan URL `next` atau respons mentah.
- **[fakta]** Batas standard access terkonfirmasi untuk `profile_lookup`: akun non-resmi ditolak dengan "insufficient access tier". Ini selaras dengan dokumentasi (hanya akun resmi Meta di standard access).

## Dampak

- **[usulan]** Tahap 2 (kompetitor lewat `profile_lookup`/`profile_posts`) membutuhkan Advanced Access; tidak bisa dijalankan sebelum App Review disetujui. Pertanyaan Q1b di `docs/meta-support-questions.md` menjadi prioritas.
- **[usulan]** `topic_tag` tersedia di `profile_posts`, sehingga deteksi tren lewat frekuensi tag layak untuk tahap 2.
- **[usulan]** Untuk uji tanpa App Review, pakai akun resmi Meta atau akun tester sendiri.

## Belum diuji (masih terbuka)

- Batas `limit` maksimum yang sebenarnya, kedalaman riwayat (sejauh mana `since` bisa mundur), P7 akun di bawah 100 followers.
- P8 header rate limit: Explorer tidak menampilkan header respons; perlu curl atau PowerShell dengan token.
- `keyword_search` yang belum diuji: T4 (TOP vs RECENT), T5 (`search_mode=TAG`), T6 (paginasi), T8 (`media_type`), T9 (kuota), T11 (akun privat). T1 praktis tercakup oleh T2 (post sendiri terbaca).
- Perilaku post terhapus (T10).
