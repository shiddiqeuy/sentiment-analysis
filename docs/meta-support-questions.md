# Draf pertanyaan untuk Meta Developer Support

Status: DRAF, belum dikirim. Kirim lewat Meta for Developers Support (developers.facebook.com/support) atau kanal resmi lain, setelah pemilik proyek meninjau. Isi placeholder di dalam `[ ]`. Jangan sertakan token, secret, atau data pribadi.

Dasar: `docs/scope-statement.md`, `docs/research/threads-api-open-questions.md` (bagian 7).

Urutan prioritas: Q1 dan Q3 paling menentukan MVP.

Pembaruan 2026-10-31: ditambahkan izin `threads_profile_discovery` (fakta, teramati di App Dashboard app `ads-crawler`, tab Use cases > Access the Threads API > Permissions and features). Deskripsinya menyebut penemuan profil dan post publik "to conduct competitor analyses", sehingga mungkin lebih cocok untuk tahap kompetitor. Belum ada di riset awal dan belum diverifikasi di dokumentasi; endpoint dan field yang dibukanya **[terbuka]**.

---

## Draf pesan (Inggris)

**Subject:** Threads API: eligibility of internal brand-monitoring use case for threads_keyword_search, and data-use questions

Hello,

We are building an internal tool for [company/team name] that analyzes public Threads posts mentioning our own products and product categories. We plan to use `threads_keyword_search` with a closed, team-managed list of keywords, and, in a later phase, possibly `threads_profile_discovery` to analyze public posts of competitor brand accounts. Output is aggregate only (sentiment trends, volume spikes, topic clusters). We do not plan to build per-account profiles, offer person-level search, or sell, license, or share the data. App ID: [APP_ID].

We could not find clear answers in the documentation, so we would appreciate written clarification on the following.

**1. App Review eligibility.** Is "internal brand and product monitoring (aggregate sentiment analysis of public posts matching our own keywords)" an accepted use case for `threads_keyword_search`, given the documented permitted use of "manage their social media presence"? Would a later extension to comparing sentiment about competitor brands (aggregate only) be acceptable under the same permission?

**1b. Competitor analysis and `threads_profile_discovery`.** The App Dashboard describes `threads_profile_discovery` as allowing apps to find public Threads accounts and their public posts "to conduct competitor analyses". (a) Is this the intended permission for aggregate sentiment analysis of competitor brand accounts' public posts and the replies to them? (b) The documentation lists `profile_lookup` and `profile_posts`. Is there any endpoint to retrieve replies under a public account's posts, and with which permission? (c) Under standard access only official Meta accounts are retrievable, and profiles need 100+ followers. What exactly is required to lift the standard-access restriction (App Review, Advanced Access, Business Verification), and does the 1,000 requests per 24 hours limit apply per app, per token, or per Threads account? (d) Is the restriction the same as for other permissions (no consumer apps; aggregated and de-identified insights only)?

**2. Access level and verification.** For an app used only by our own organization (not offered to clients or consumers), is Business Verification required for Advanced Access to `threads_keyword_search`? The Tech Provider page states it is no longer required; please confirm whether that applies to this case. What is the typical App Review turnaround?

**3. Machine learning use.** The Platform Terms do not mention machine learning explicitly. May we (a) use text from Threads posts obtained via the API to fine-tune a sentiment classification model that we host ourselves, and (b) send post text to a third-party model API for classification? If either is not permitted, is aggregate output derived from such processing allowed?

**4. Deleted posts.** For posts returned by `keyword_search` (not owned by our users), is there an official way to detect that a post was later deleted or made private? What does `GET /{media-id}` return for such posts? What retention period applies to cached Platform Data, and what deletion timeline do you expect once a post is removed?

**5. Trending topics.** Is there a "Threads Trending Topics" permission or endpoint available to developers? If yes, what are its access requirements? If not, is there a recommended way to detect trending topics, other than `topic_tag` and `search_mode=TAG`?

**6. Search depth and pagination.** How far back does `keyword_search` return results, and how does pagination work beyond the first page of up to 100 results? Does the 2,200 queries per 24 hours limit apply per user or per app, and does it count paginated requests?

**7. Public search without review.** Before App Review approval, can an app's role-holders (admin, developer, tester) retrieve public posts from other accounts via `keyword_search`, or only their own?

Thank you. Please reply in writing so we can keep the response for our compliance records.

[Name, role] / [contact]

---

## Catatan internal (jangan dikirim)

- **[usulan]** Kirim satu pesan dengan delapan pertanyaan (Q1, Q1b, Q2 sampai Q7); bila balasan lambat, pecah menjadi Q1 sampai Q3 dan sisanya.
- **[usulan]** Simpan balasan tertulis di `docs/` (tanpa data pribadi) sebagai bukti kepatuhan.
- **[asumsi]** Meta mungkin hanya menjawab sebagian atau merujuk ke dokumentasi. Jawaban Q3 dan Q4 tetap perlu dinilai pemilik keputusan legal.
- **[terbuka]** Kanal dukungan yang tepat untuk Threads API dan apakah akun developer perlu terverifikasi untuk membuka tiket.
- Q6 dan Q7 juga bisa dijawab lewat uji empiris di Graph API Explorer; tanyakan hanya bila hasil uji ambigu.
