# Create a NEW Cursor Automation (not MSOEN)

Do **not** open, edit, enable, or duplicate **MSOEN Daily Articles**.
Create a separate automation.

## Open this page

https://cursor.com/automations/new

## Settings

| Field | Value |
| --- | --- |
| Name | `Wuliuaou Daily Articles` |
| Enabled | On |
| Trigger | Scheduled |
| Timezone | Asia/Shanghai |
| Time | 20:00 every day |
| Cron if the UI is UTC | `0 12 * * *` |
| Repository | `github.com/STRUGGLE1999/msoen-daily-articles` |
| Branch | `main` (or this repo’s default) |

## Prompt to paste

Copy **all** of `wuliuaou/AUTOMATION.md`.

In the Automations UI only, fill `WP_PASSWORD` with the **wuliuaou.com** password for user `hqned`.

Do not paste `msoen/AUTOMATION.md` here. Do not use the msoen.com user `hqned123` or the msoen.com application password.

Save. Confirm the list shows **two different automations**:

1. `Wuliuaou Daily Articles` — new, enabled, 20:00 Beijing
2. `MSOEN Daily Articles` — old, leave it disabled
