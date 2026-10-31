# Draf pertanyaan untuk Meta Developer Support

Status: DRAF, belum dikirim. Kirim lewat Meta for Developers Support (developers.facebook.com/support) setelah pemilik proyek meninjau. Sisa placeholder: `[company/team name]` dan `[Name, role] / [contact]`. Jangan sertakan token, secret, atau data pribadi.

Dasar: `docs/scope-statement.md`, `docs/research/threads-api-open-questions.md`, `docs/research/threads-profile-discovery.md`, `docs/research/threads-api-test-results.md`.

## Perubahan dari versi sebelumnya (2026-10-31)

- Dihapus karena sudah terjawab oleh uji: pertanyaan "pencarian publik sebelum review" (di development, `keyword_search` hanya mengembalikan post tester sendiri) dan pertanyaan batas standard access untuk `profile_lookup` (akun non-resmi ditolak "insufficient access tier").
- Pertanyaan dipadatkan dari delapan menjadi enam, diurut menurut dampak ke jadwal proyek.
- Hasil uji dilampirkan sebagai konteks agar Meta tidak menjawab hal yang sudah kami ketahui.

---

## Draf pesan (Inggris)

**Subject:** Threads API (App ID 1915966229809679): App Review eligibility for internal brand-monitoring use case, and data-use questions

Hello,

We are building an internal tool for [company/team name] that analyzes public Threads posts mentioning our own products and product categories. We plan to use `threads_keyword_search` with a closed, team-managed list of keywords and, in a later phase, `threads_profile_discovery` for public posts of competitor brand accounts. Output is aggregate only (sentiment trends, volume spikes, topic clusters). We do not plan to build per-account profiles, offer person-level search, or sell, license, or share the data. The app is for our own organization only, not offered to clients or consumers.

In development mode we confirmed the following, so we are not asking about these:
- `keyword_search` returns only the tester's own posts, even with `author_username` set to another account.
- `profile_lookup` for a public brand account that is not an official Meta account fails with "App does not have sufficient access tier" (code 10, subcode 4279067).

We could not find clear answers in the documentation for the questions below. A written reply would help us plan.

**1. App Review eligibility.** Is "internal brand and product monitoring (aggregate sentiment analysis of public posts matching our own keywords)" an accepted use case for `threads_keyword_search`, given the documented permitted use of "manage their social media presence"? Would a later extension to aggregate sentiment comparison of competitor brands be acceptable under `threads_keyword_search` or `threads_profile_discovery`?

**2. Access requirements.** For an app used only by our own organization, what is required to obtain Advanced Access to `threads_keyword_search` and `threads_profile_discovery`: App Review, Business Verification, or both? The Tech Provider page says it is no longer required; does that apply here? What is the typical review turnaround?

**3. Machine learning use.** The Platform Terms do not mention machine learning explicitly. May we (a) use text from Threads posts obtained via the API to fine-tune a sentiment classification model that we host ourselves, and (b) send post text to a third-party model API for classification? If either is not permitted, is aggregate output derived from such processing allowed?

**4. Deleted posts and retention.** For posts returned by `keyword_search` or `profile_posts` that we do not own, is there an official way to detect that a post was later deleted or made private? What does `GET /{media-id}` return for such posts? What retention period applies to cached Platform Data, and what deletion timeline do you expect once a post is removed?

**5. Replies and trending.** (a) Is there any endpoint to retrieve replies under a public account's posts, and with which permission? `threads_read_replies` appears limited to threads owned by the app user. (b) Is there a "Threads Trending Topics" permission or endpoint for developers? If not, is `topic_tag` with `search_mode=TAG` the recommended way to detect trends?

**6. Limits.** (a) Does the 2,200 queries per 24 hours limit for `keyword_search` apply per user or per app, and do paginated requests count? (b) Does the 1,000 requests per 24 hours limit for profile discovery apply per app, per token, or per Threads account? (c) What is the maximum `limit` per request for `keyword_search` and `profile_posts`, and how far back can results go?

Thank you. Please reply in writing so we can keep the response for our compliance records.

[Name, role] / [contact]

---

## Catatan internal (jangan dikirim)

- **[fakta]** App ID `1915966229809679` adalah app `threads-sentiment-analysis`. App ID bukan rahasia, tetapi pemilik proyek perlu memastikan memang ingin mencantumkannya.
- **[usulan]** Prioritas: Q1 dan Q2 menentukan jadwal MVP; Q3 menentukan apakah fine-tuning boleh. Bila balasan lambat, kirim Q1 sampai Q3 dahulu dan sisanya menyusul.
- **[usulan]** Simpan balasan tertulis di `docs/` (tanpa data pribadi) sebagai bukti kepatuhan.
- **[asumsi]** Meta mungkin hanya menjawab sebagian atau merujuk ke dokumentasi. Jawaban Q3 dan Q4 tetap perlu dinilai pemilik keputusan legal.
- **[terbuka]** Kanal dukungan yang tepat untuk Threads API, dan apakah akun developer perlu terverifikasi untuk membuka tiket.
- Q6(c) dan sebagian Q5 bisa dijawab lewat uji empiris (lihat `docs/research/threads-api-test-results.md`); bila uji sudah menjawab, hapus bagian itu dari pesan.
