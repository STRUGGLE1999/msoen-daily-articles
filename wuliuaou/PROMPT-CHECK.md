# Prompt check — Wuliuaou Daily Articles

Use this to verify the prompt currently saved at:

https://cursor.com/automations/6cab1a85-a38e-11f1-a7d1-d6b4613131ce

Replace the saved prompt with `wuliuaou/AUTOMATION.md` if any item below is wrong.

## Must be true

- Site is https://www.wuliuaou.com, not msoen.com
- 10 articles per run, 20:00 Beijing, status=publish
- Category International logistics (id 45)
- English, no images
- Username `hqned`
- Log file `wuliuaou-published-log.md`
- Contact HTML from `wuliuaou/contact-cta.html`

## Must not be true

- 7 articles, 19:00, covers, FAQ/Conclusion MSOEN structure
- Username `hqned123`
- MSOEN application password
- Email via QQ SMTP
- Categories Drone Blog / Agricultural drones / Drone Buying Guide
- Writing to `published-log.md` only

## Password

Do not reuse the msoen.com WordPress application password on wuliuaou.com.

They are different WordPress installs:

- msoen.com user is `hqned123` + application password
- wuliuaou.com user is `hqned` + that site's own password

An application password is issued by one WordPress site and only works on that site.
