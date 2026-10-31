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
3. Minta izin `threads_basic` dan `threads_keyword_search`, lalu ambil access token lewat alur OAuth.
4. **[terbuka]** Apakah Graph API Explorer mendukung host `graph.threads.com`. Bila tidak, pakai curl atau Postman dengan token yang sama.

## Skenario uji

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
