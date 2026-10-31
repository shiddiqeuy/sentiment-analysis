# Rencana uji empiris Threads keyword_search

Status: draf, belum dijalankan. Tujuan: menjawab Q4, Q6, Q7 di `docs/meta-support-questions.md` tanpa menunggu Meta, dan menjadi dasar prototype.

Dasar endpoint dan parameter: `docs/research/threads-api-open-questions.md` bagian 5 (bukan dari pengetahuan sendiri). Nama field yang diminta di bawah **[asumsi]**; cocokkan dengan dokumentasi sebelum dipakai.

## Aturan keamanan

- Token tidak ditulis ke berkas repo, chat, atau commit. Simpan di variabel lingkungan sesi: PowerShell `$env:THREADS_TOKEN = "..."`.
- Lampirkan ke catatan hanya respons yang sudah di-mask (username, teks pribadi, ID).
- Uji hanya dengan akun milik sendiri dan keyword netral. Jangan uji keyword sensitif atau yang menyasar individu.
- Hormati batas 2.200 query per 24 jam; uji ini butuh kurang dari 50.

## Persiapan

1. Buat app di developers.facebook.com, tambahkan use case Threads API.
2. Tambahkan akun Threads sendiri sebagai Threads Tester atau role-holder.
3. Tambahkan izin `threads_basic` dan `threads_profile_discovery` (fase 0), serta `threads_keyword_search` (fase berikutnya), lalu ambil access token lewat alur OAuth.
4. **[terbuka]** Apakah Graph API Explorer mendukung host `graph.threads.com`. Bila tidak, pakai curl atau Postman dengan token yang sama.

## Alur token Threads (diakses 2026-10-31)

Sumber primer (dibaca lewat alat fetch yang meringkas; kutipan bukan salinan manusia):
- https://developers.facebook.com/documentation/threads/get-started
- https://developers.facebook.com/documentation/threads/get-started/get-access-tokens-and-permissions
- https://developers.facebook.com/documentation/threads/get-started/long-lived-tokens
- https://developers.facebook.com/documentation/development/create-an-app/threads-use-case
- https://developers.facebook.com/documentation/threads/threads-profiles

1. **[fakta]** Tester: Dashboard > App roles > Roles > Add People > Threads Tester. Undangan diterima di Threads: Account Settings > Website permissions (https://www.threads.com/settings/account).
2. **[fakta]** Otorisasi: buka `https://threads.com/oauth/authorize` dengan `client_id` (Threads App ID), `redirect_uri`, `scope` (`threads_basic` wajib), `response_type=code`, `state` opsional. `code` berlaku 1 jam, sekali pakai.
3. **[fakta]** Tukar code: `POST https://graph.threads.com/oauth/access_token` (form: `client_id`, `client_secret`, `grant_type=authorization_code`, `redirect_uri`, `code`). Hasilnya short-lived token, berlaku 1 jam.
4. **[fakta]** Long-lived: `GET https://graph.threads.com/access_token?grant_type=th_exchange_token&...`, dilakukan di server, berlaku 60 hari. Refresh lewat `refresh_access_token?grant_type=th_refresh_token`, token minimal berumur 24 jam.
5. **[fakta]** `redirect_uri` harus cocok dengan daftar Valid OAuth Redirect URIs di Settings > Client OAuth Settings. Persyaratan HTTPS dan penggunaan localhost **[terbuka]** (tidak disebut).
6. **[fakta]** Threads App ID dan Threads App secret ada di App settings > Basic. Secret hanya di variabel lingkungan, tidak di berkas, chat, atau commit.
7. **[fakta]** Untuk uji, halaman Profiles menyebut token bisa dibuat lewat Graph API Explorer. Tombol "Generate Access Token" di dashboard tidak disebut **[terbuka]**.
8. **[fakta]** Host API: `https://graph.threads.com/v1.0/` (mis. `profile_lookup`); host otorisasi `threads.com`.
9. **[usulan]** Untuk token pertama, coba Graph API Explorer lebih dulu (tanpa redirect URI). Bila tidak mendukung, jalankan alur OAuth dengan redirect URI sederhana dan salin `code` dari address bar.

## Fase 0: profile discovery (bisa dijalankan lebih dulu)

Dasar: `docs/research/threads-profile-discovery.md`. Di standard access hanya akun resmi Meta (@meta, @threads, @instagram, @facebook) yang bisa dicari, jadi fase ini memakai akun tersebut. Izin yang dibutuhkan: `threads_basic` dan `threads_profile_discovery` (saat ini hanya `threads_basic` yang ditambahkan di `ads-crawler`).

| # | Uji | Cara | Menjawab | Hasil |
|---|---|---|---|---|
| P1 | Lookup akun resmi | `GET /profile_lookup?username=threads` | token, format respons | |
| P2 | Field yang kembali | bandingkan dengan daftar dokumentasi; catat `replies_count` ada atau tidak | inkonsistensi dokumen | |
| P3 | Posting akun resmi | `GET /profile_posts?username=threads&limit=10` | field, `topic_tag`, `permalink` | |
| P4 | Paginasi | ikuti `paging.cursors.after`; catat cara pakai dan batas halaman | paginasi | |
| P5 | `since`/`until`/`limit` | coba ketiganya; catat yang diterima atau ditolak, serta `limit` maksimum | parameter tak terdokumentasi | |
| P6 | Akun non-resmi | `profile_lookup` ke akun publik 100+ followers (bukan akun Meta) | batas standard access | |
| P7 | Akun di bawah 100 followers | akun sendiri bila publik | batas 100 followers | |
| P8 | Hitungan kuota | catat header rate limit sebelum dan sesudah; batas dokumentasi 1.000 per 24 jam | per app, token, atau akun | |

- Kriteria: P6 gagal berarti kompetitor butuh advanced access (tahap 2 menunggu App Review). P6 berhasil berarti batas standard access tidak seketat dokumentasi.
- Catatan: P6 hanya menyentuh profil publik dan tidak menyimpan hasilnya; jangan uji akun individu pribadi.

## Skenario uji keyword_search

Isi kolom hasil dengan mask. Tandai tiap hasil: fakta (teramati).

| # | Uji | Cara | Menjawab | Hasil |
|---|---|---|---|---|
| T1 | Post sendiri terbaca | `keyword_search?q=<kata yang ada di post sendiri>&search_type=RECENT` | dasar | |
| T2 | Post orang lain terbaca tanpa App Review | keyword umum netral, mis. nama kategori produk, tanpa `author_username` | Q7 | |
| T3 | Field yang dikembalikan | tambahkan `fields=` sesuai dokumentasi; catat yang ditolak | field, tipe `topic_tag` | |
| T4 | `search_type` TOP vs RECENT | keyword sama, bandingkan urutan dan isi | perilaku | |
| T5 | `search_mode=TAG` | tagar yang sedang ramai | tren via tag | |
| T6 | Paginasi | `limit=100`, ikuti `paging`/`after`; catat jumlah halaman maksimum | Q6 | |
| T7 | Kedalaman waktu | `since`/`until` mundur 1, 7, 30, 90 hari; catat apakah hasil kosong atau error | Q6 | |
| T8 | Filter `media_type` | TEXT, IMAGE, VIDEO | perilaku | |
| T9 | Hitungan kuota | catat header rate limit sebelum dan sesudah request halaman berikutnya | Q6 | |
| T10 | Post terhapus | posting sendiri, cari, hapus, cari lagi, lalu `GET /{media-id}` | Q4 | |
| T11 | Akun privat | cari post dari akun privat uji (milik sendiri) | perilaku | |

## Contoh perintah (PowerShell)

```powershell
$u = "https://graph.threads.com/v1.0/keyword_search"
Invoke-RestMethod -Uri $u -Body @{ q = "kata-uji"; search_type = "RECENT"; limit = 10; access_token = $env:THREADS_TOKEN }
```

## Catatan hasil

Salin tabel ke `docs/research/threads-api-test-results.md` setelah uji, dengan data ter-mask, dan perbarui status poin terbuka di `threads-api-open-questions.md`.

## Kriteria keputusan

- T2 gagal: pengembangan harus menunggu App Review; prototype memakai post sendiri.
- T7 dangkal (hari saja): tren historis butuh penyimpanan sendiri sejak hari pertama.
- T10 tidak terdeteksi: wajib job periodik cek ulang `GET /{media-id}` untuk menghapus konten hilang.
