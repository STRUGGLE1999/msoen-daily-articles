# msoen-daily-articles

Workspace for daily WordPress publishing automations.

## Wuliuaou.com (active)

Every day at **20:00 Beijing time**, publish **10 English articles** to https://www.wuliuaou.com.

- Playbook: `wuliuaou/AUTOMATION.md`
- Theme rotation and titles: `python3 scripts/select_theme.py`
- Publisher: `python3 scripts/publish_posts.py --input /tmp/wuliuaou-posts.json`
- Log: `wuliuaou-published-log.md`

Rules already confirmed: publish immediately, English only, no images, International logistics category, search-style titles, contact block at the end, themes may repeat.

WordPress passwords must stay out of this repository. Put them in environment variables or the agent store, not in git.

## MSOEN.com

`published-log.md` is the older msoen.com article log. Do not mix the two sites in one run.

Do not put WordPress passwords, SMTP codes, or other secrets in this repository.
