# Two separate automation prompts

This repository has two WordPress jobs. Keep their prompts in different Cursor Automations. Do not overwrite one with the other.

| Job | Cursor Automation | Prompt file | Site | Log |
| --- | --- | --- | --- | --- |
| Drones | MSOEN Daily Articles | `msoen/AUTOMATION.md` | https://www.msoen.com | `published-log.md` |
| Logistics | Wuliuaou Daily Articles | `wuliuaou/AUTOMATION.md` | https://www.wuliuaou.com | `wuliuaou-published-log.md` |

WordPress passwords are per site. The msoen.com application password for `hqned123` will not log into wuliuaou.com. Wuliuaou uses user `hqned` on https://www.wuliuaou.com.

Do not put WordPress passwords, SMTP codes, or other secrets in this repository.
