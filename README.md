<div align="center">

<img src="https://capzy.ai/capzy-logo.svg" alt="Capzy" width="220" />

# Imperva Incapsula Solver

**Bypass Imperva Incapsula. Solves reese84 + utmvc from the challenge script — no full-site load, no proxy required.**

[![Solve cost](https://img.shields.io/badge/from-%240.001%20%2F%20solve-%23ff5d2a)](https://capzy.ai/solvers)
[![Speed](https://img.shields.io/badge/avg%20solve-~10%20seconds-%2322c55e)](https://capzy.ai/solvers/imperva)
[![Uptime](https://img.shields.io/badge/uptime-99.9%25-%2322c55e)](https://capzy.ai/status)
[![License: MIT](https://img.shields.io/badge/license-MIT-%23ff5d2a)](LICENSE)

[Live Demo](https://capzy.ai/solvers/imperva/demo) ·
[Get Free $0.10 Credit](https://capzy.ai/auth/register) ·
[Dashboard](https://capzy.ai/dashboard) ·
[Full Docs](https://capzy.ai/docs) ·
[Pricing](https://capzy.ai/solvers)

</div>

---

## What this repo is

Copy-pasteable examples for solving **Imperva Incapsula** through the
[Capzy](https://capzy.ai) HTTP API — no SDK required. Pure curl, Python,
and Node.js using the raw API. Easy to read, easy to port, easy to audit.

## What is Imperva Incapsula?

Imperva Incapsula is a CDN/WAF that protects ~27,000 sites including banks, insurance companies, and enterprise portals. It uses two JavaScript challenges: **reese84** (a fingerprint "interrogation" the browser POSTs to a long dashed script URL to receive a `reese84` cookie) and the older **utmvc** (an `_Incapsula_Resource` script that computes a `___utmvc` cookie from the `incap_ses_*` session cookies).

Capzy solves each **from the challenge script alone** — we run the bundle in a minimal host page, so a half-rendered or gated page no longer blocks the solve. We return the `reese84` (which you POST to receive your cookie) or the computed `___utmvc` value. Because you perform the final submit, the result isn't bound to our IP — **no proxy required**.

## Why Capzy

- **From $0.001 per solve.** Flat pricing — no tiers, no retainer, no monthly minimum.
- **~10 seconds average solve.** Production-grade speed.
- **Drop-in compatible.** `createTask` / `getTaskResult` protocol. If your code already speaks the standard solver shape, swap the host to `https://api.capzy.ai`.
- **$0.10 in real credits on sign-up.** No card. 100 free test solves.

## Pricing

| Task type | When to use | Cost / solve |
|-----------|-------------|-------------:|
| `AntiImpervaTaskProxyLess`             | Proxyless (Capzy supplies the IP) | **$0.001**   |
| `AntiImpervaTask`                       | You supply the proxy              | **$0.001**   |

For consistency across the target site, use the proxy variant with the
**same proxy your session is already running through** — the solver
mints the token from that IP, so when you submit it back through the
same proxy everything looks consistent.

## 60-second quickstart

```bash
# 1. Sign up — gets you $0.10 in free credits (100 solves)
open https://capzy.ai/auth/register

# 2. Copy your API key from the dashboard
#    https://capzy.ai/dashboard/api-keys

# 3. Run any example
export CAPZY_KEY="capzy_..."
bash examples/curl/basic.sh
```

Minimal Python:

```python
import requests, time

KEY = "capzy_xxxxxxxxxxxxxxxxxxxxxxxx"

# 1) Create the task
created = requests.post("https://api.capzy.ai/createTask", json={
    "clientKey": KEY,
    "task": {
        "type": "AntiImpervaTaskProxyLess",
        "websiteURL": "https://www.example.com/",
        "version": "reese84",
        # reese84: pass the script URL (long dashed path ending in ?s=...).
        # Omit scriptUrl and we auto-detect it from websiteURL.
        "scriptUrl": "https://www.example.com/s-weakes-Sir-Day/1860025529848880788?s=xlD1csYd"
    },
}).json()
task_id = created["taskId"]

# 2) Poll until ready
while True:
    result = requests.post("https://api.capzy.ai/getTaskResult", json={
        "clientKey": KEY, "taskId": task_id,
    }).json()
    if result["status"] == "ready":
        break
    time.sleep(2)

print(result["solution"])
```

That's the whole protocol. The rest of this repo is just that, in every
language we could think of.

## Pick your language

| Language        | Example                                       |
|-----------------|-----------------------------------------------|
| **curl / bash** | [`examples/curl/basic.sh`](examples/curl/basic.sh)    |
| **Python**      | [`examples/python/basic.py`](examples/python/basic.py) |
| **Node.js**     | [`examples/nodejs/basic.js`](examples/nodejs/basic.js) |

See [`examples/README.md`](examples/README.md) for setup details.

## Request envelope

reese84 (modern challenge):

```json
{
  "clientKey": "capzy_xxxxxxxxxxxxxxxxxxxxxxxx",
  "task": {
    "type": "AntiImpervaTaskProxyLess",
    "websiteURL": "https://www.example.com/",
    "version": "reese84",
    "scriptUrl": "https://www.example.com/s-weakes-Sir-Day/1860025529848880788?s=xlD1csYd"
  }
}
```

utmvc (legacy challenge):

```json
{
  "clientKey": "capzy_xxxxxxxxxxxxxxxxxxxxxxxx",
  "task": {
    "type": "AntiImpervaTaskProxyLess",
    "websiteURL": "https://www.example.com/",
    "scriptUrl": "https://www.example.com/_Incapsula_Resource?SWJIYLWA=5074a744...",
    "version": "utmvc",
    "cookies": [
      { "name": "incap_ses_345_2269415", "value": "Twa4M6ISK2uPanH/1a/JBGZ55mcAAAAA..." }
    ]
  }
}
```

| Field | Type | Required | Notes |
|-------|------|:--------:|-------|
| `type` | `string` | yes | `AntiImpervaTaskProxyLess` or `AntiImpervaTask` |
| `websiteURL` | `string` | yes | Full URL of the Imperva-protected page |
| `version` | `string` | **yes** | `reese84` (modern challenge) or `utmvc` (older `_Incapsula_Resource` challenge) |
| `scriptUrl` | `string` | recommended | The challenge script URL for **both** challenges — the reese84 dashed path or the utmvc `_Incapsula_Resource` script. Auto-detected if omitted |
| `cookies` | `array` | utmvc | Every `incap_ses_*` cookie as `{name, value}` |
| `script` | `string` | no | Pre-fetched reese84 JS; pass when the page injects inline config |
| `userAgent` | `string` | no | Defaults to Windows Chrome (135–147); returned in the solution |
| `proxyType/Address/Port/Login/Password` | — | no | Optional egress (either variant); also enables the cookie path |

Full reference in [`docs/parameters.md`](docs/parameters.md).

## Response shape

When the task is ready (`status: "ready"`), `solution` contains:

| Field | Type | Notes |
|-------|------|-------|
| `reese84` | `string` | reese84 mode: the interrogation POST body — submit it to `scriptUrl` to get your `reese84` cookie |
| `utmvc` | `string` | utmvc mode: the computed `___utmvc` cookie value |
| `userAgent` | `string` | User-Agent used during solve — reuse it |

### Example (reese84)

```json
{
  "status": "ready",
  "solution": {
    "reese84": "{\"solution\":{\"interrogation\":{\"p\":\"9pp4bv7Sp0073gA1xoN9Aoo...E\",\"st\":1744612535,\"sr\":3851658681,\"cr\":937075512,\"og\":2},\"version\":\"beta\"},\"old_token\":null,\"error\":null,\"performance\":{\"interrogation\":488}}",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
  }
}
```

### How to use the result

- **reese84** — POST `reese84` (raw body) to your `scriptUrl`
  with the returned `userAgent`; the response sets your `reese84` cookie.
  Reuse that cookie + User-Agent on subsequent requests.
- **utmvc** — set `___utmvc=<utmvc>` as a cookie and re-request with the same
  User-Agent.

## Features

- Solves from the challenge script alone — no full-site load required
- reese84 → the interrogation payload you POST to `scriptUrl`
- utmvc → the computed `___utmvc` value from your `incap_ses_*` cookies
- Not IP-bound: works proxyless, or bring your own proxy
- Auto-detects the reese84 script URL when you send only `websiteURL`

## FAQ

**reese84 or utmvc?** reese84 is the modern challenge (long dashed script URL → `reese84` you POST back). utmvc is the older one (`_Incapsula_Resource` script + your `incap_ses_*` cookies → a `___utmvc` value you set as a cookie).

**Do I need a proxy?** No — you perform the final POST / cookie-set from your own IP, so the ProxyLess variant works. Supply a proxy only to run the script through a specific egress or to use the full-browser cookie path.

## What you'll need

- A Capzy API key — [sign up](https://capzy.ai/auth/register) (free, $0.10 credit).
- Network access to `https://api.capzy.ai`.

## Other captcha types

Capzy solves 25+ captcha types. Full catalog at
[capzy.ai/solvers](https://capzy.ai/solvers). Each type has its own
solver repo on [github.com/capzy-ai](https://github.com/capzy-ai).

## License

[MIT](LICENSE).

---

<div align="center">

**[Sign up for free credits →](https://capzy.ai/auth/register)**

Built by [Capzy](https://capzy.ai). Issues + PRs welcome.

</div>
