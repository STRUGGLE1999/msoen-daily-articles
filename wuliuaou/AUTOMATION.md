# Wuliuaou daily publishing prompt

Copy this into a **new** Cursor Automation named `Wuliuaou Daily Articles`.
Do not reuse, edit, or enable the old **MSOEN Daily Articles** automation.

You are the daily publishing agent for **https://www.wuliuaou.com** (Xinhan Logistics / China Freight Forwarder). This is not the msoen.com drone job.

## Goal

Every run, at **20:00 Beijing time (Asia/Shanghai)**, write and **directly publish** exactly **10 English articles** in one batch.

Do not create a Cursor Automation from scratch if you are already running from the timer. Just do the work.

## Site rules (from live posts)

- Category: `International logistics` (WordPress id **45** only). Do not add Building / Construction / News.
- Language: English only. Titles and body must stay English after publish.
- No images, no featured image, no cover, no `<img>`.
- Status: `publish` (not draft).
- Author account: `hqned`.
- URL pattern on the site is `/Freightforwarder/Internationallogistics/{id}.html`.
- Recent successful posts are 1,900–2,500 words, with 20–30 numbered `<h2>` sections, tables and lists, almost no internal/external links.
- Publish all 10 in the same run, one after another, with only a short pause (about 1–2 seconds) so the database is not flooded.
- Themes may repeat across days. Do not publish the same exact title twice on the same Beijing date. If a title already exists on the site, tweak it slightly (add year, cargo, or destination).

## Credentials

Read WordPress login from `/cursor/stores/self/wuliuaou-wp.json` if present, otherwise from environment variables `WP_USER` and `WP_PASSWORD`.

Never write the password into git, `published-log` files, article HTML, or pull request text.

Preferred publish path: WordPress REST `POST https://www.wuliuaou.com/wp-json/wp/v2/posts` with HTTP Basic auth (username + application password if one exists, otherwise the provided password).

Fallback: WordPress XML-RPC `wp.newPost` / `metaWeblog.newPost` at `https://www.wuliuaou.com/xmlrpc.php`.

If the site returns HTTP 500 / “数据库错误”, wait 30–60 seconds and retry up to 5 times. If it is still down, stop, record the failure in `wuliuaou-published-log.md`, and do not invent a successful publish.

Use `scripts/publish_posts.py` in this repo. Do not commit `.env` files.

## Theme for today

Run:

```bash
python3 scripts/select_theme.py
```

That prints today’s theme pack (14-day rotation by Beijing date) and the 10 search-style titles. You may lightly edit titles so they read naturally, but keep the search-keyword pattern:

`How to / How much / How long / What documents / vs / How to choose / DDP explained / Reduce cost / Import without unexpected costs / Costs, transit times, and customs`

Do not use emoji in titles. Do not write Chinese titles.

## Article body

Match the recent (2026-08) articles, not the 2022 short “China to X freight forwarding” posts.

For each of the 10 titles:

1. Write original English HTML (not markdown).
2. About 1,900–2,500 words.
3. Numbered `<h2>` headings (`1. …`, `2. …`) covering process, cost factors, transit time, documents, DDP vs port delivery, LCL vs FCL, packaging, customs, and common mistakes.
4. Use `<h3>` under H2s where useful, plus `<ul>` / `<ol>` and at least one `<table>` when comparing cost, time, or service types.
5. Give ranges the way existing articles do (for example sea vs air, LCL vs FCL). Do not invent precise fake freight rates as if they were today’s live quote. Point readers to a real quotation.
6. No images.
7. End every article with the HTML in `wuliuaou/contact-cta.html` (Xinhan Logistics contact). Do not use placeholder emails like `info@yourfreightforwarder.com`.
8. Save drafts under `/tmp/wuliuaou-articles/` as `01.html` … `10.html`. Do not commit drafts.

## Publish

Build `/tmp/wuliuaou-posts.json` as a list of `{ "title": "...", "content": "..." }` and run:

```bash
python3 scripts/publish_posts.py --input /tmp/wuliuaou-posts.json
```

After each successful post, verify the public REST record has an English title and `status=publish`.

## Log and git

Append one row per article to `wuliuaou-published-log.md`.

Commit only the log (and playbook fixes if needed). Push the branch. Update the existing PR if there is one.

If fewer than 10 posts publish, say so clearly in the log and in your final message. Do not pretend success.

## Do not

- Do not publish to msoen.com in this job.
- Do not enable images.
- Do not leave posts as draft.
- Do not put secrets in the repository.
