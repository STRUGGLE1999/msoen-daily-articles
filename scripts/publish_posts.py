#!/usr/bin/env python3
"""Publish English posts to wuliuaou.com via REST, with XML-RPC fallback."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
import xmlrpc.client
from base64 import b64encode
from pathlib import Path

DEFAULT_SITE = "https://www.wuliuaou.com"
CATEGORY_INTERNATIONAL_LOGISTICS = 45
USER_AGENT = "wuliuaou-daily-publisher/1.0"


def load_credentials() -> tuple[str, str, str]:
    store = Path("/cursor/stores/self/wuliuaou-wp.json")
    data: dict = {}
    if store.exists():
        data.update(json.loads(store.read_text()))
    for env_path in (Path("/workspace/.env.wuliuaou"), Path(".env.wuliuaou")):
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                data.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    user = os.environ.get("WP_USER") or data.get("WP_USER") or data.get("username")
    password = (
        os.environ.get("WP_PASSWORD")
        or os.environ.get("WP_APP_PASSWORD")
        or data.get("WP_PASSWORD")
        or data.get("WP_APP_PASSWORD")
        or data.get("password")
    )
    site = os.environ.get("WP_SITE") or data.get("WP_SITE") or DEFAULT_SITE
    if not user or not password:
        raise SystemExit("Missing WP_USER / WP_PASSWORD (env, .env.wuliuaou, or agent store).")
    return user, password, site.rstrip("/")


def request_json(url: str, user: str, password: str, payload: dict | None = None, method: str = "GET"):
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Authorization": "Basic " + b64encode(f"{user}:{password}".encode()).decode(),
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")
        method = method or "POST"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
            parsed = json.loads(body) if body else {}
            return resp.status, parsed, dict(resp.headers)
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = {"raw": raw.decode("utf-8", "replace")[:800]}
        return exc.code, parsed, dict(exc.headers)


def rest_create_post(site: str, user: str, password: str, title: str, content: str) -> dict:
    url = f"{site}/wp-json/wp/v2/posts"
    payload = {
        "title": title,
        "content": content,
        "status": "publish",
        "categories": [CATEGORY_INTERNATIONAL_LOGISTICS],
        "featured_media": 0,
    }
    last_error = None
    for attempt in range(1, 6):
        status, body, _headers = request_json(url, user, password, payload=payload, method="POST")
        if status in (200, 201) and isinstance(body, dict) and body.get("id"):
            return {
                "ok": True,
                "method": "rest",
                "id": body["id"],
                "link": body.get("link"),
                "status": body.get("status"),
                "title": (body.get("title") or {}).get("rendered") or title,
            }
        last_error = {"http": status, "body": body}
        if status in (401, 403):
            break
        if status in (500, 502, 503, 504) or status is None:
            time.sleep(min(10, 8 * attempt))
            continue
        break
    return {"ok": False, "method": "rest", "error": last_error}


def xmlrpc_create_post(site: str, user: str, password: str, title: str, content: str) -> dict:
    endpoint = f"{site}/xmlrpc.php"
    client = xmlrpc.client.ServerProxy(endpoint, allow_none=True)
    last_error = None
    for attempt in range(1, 4):
        try:
            post_id = client.wp.newPost(
                0,
                user,
                password,
                {
                    "post_type": "post",
                    "post_status": "publish",
                    "post_title": title,
                    "post_content": content,
                    "terms": {"category": [CATEGORY_INTERNATIONAL_LOGISTICS]},
                },
            )
            return {
                "ok": True,
                "method": "xmlrpc",
                "id": int(post_id),
                "link": f"{site}/?p={post_id}",
                "status": "publish",
                "title": title,
            }
        except Exception as exc:
            last_error = str(exc)
            time.sleep(5 * attempt)
    return {"ok": False, "method": "xmlrpc", "error": last_error}


def publish_one(site: str, user: str, password: str, title: str, content: str) -> dict:
    rest = rest_create_post(site, user, password, title, content)
    if rest.get("ok"):
        return rest
    rest_http = (rest.get("error") or {}).get("http") if isinstance(rest.get("error"), dict) else None
    xml = xmlrpc_create_post(site, user, password, title, content)
    if xml.get("ok"):
        xml["rest_error"] = rest.get("error")
        return xml
    return {
        "ok": False,
        "title": title,
        "rest": rest,
        "xmlrpc": xml,
        "hint": "REST HTTP %s" % rest_http,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="JSON list of {title, content}")
    parser.add_argument("--pause", type=float, default=1.5)
    parser.add_argument("--output", default="/tmp/wuliuaou-publish-result.json")
    args = parser.parse_args()
    posts = json.loads(Path(args.input).read_text())
    if not isinstance(posts, list) or not posts:
        raise SystemExit("Input JSON must be a non-empty list.")
    user, password, site = load_credentials()
    results = []
    for index, post in enumerate(posts, 1):
        title = (post.get("title") or "").strip()
        content = post.get("content") or ""
        if not title or not content:
            results.append({"ok": False, "index": index, "error": "missing title or content"})
            continue
        print(f"[{index}/{len(posts)}] publishing: {title}", flush=True)
        result = publish_one(site, user, password, title, content)
        result["index"] = index
        result["requested_title"] = title
        results.append(result)
        print(json.dumps({k: result[k] for k in result if k != "content"}, ensure_ascii=False), flush=True)
        if index != len(posts):
            time.sleep(args.pause)
    Path(args.output).write_text(json.dumps(results, ensure_ascii=False, indent=2))
    ok = sum(1 for item in results if item.get("ok"))
    print(f"Published {ok}/{len(results)}. Results: {args.output}", flush=True)
    return 0 if ok == len(results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
