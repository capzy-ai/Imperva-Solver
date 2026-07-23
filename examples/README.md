# Examples — Imperva Incapsula

Copy-pasteable examples for solving **Imperva Incapsula** through the
Capzy HTTP API. Three languages, same two-step protocol:

1. `POST /createTask` — get a `taskId`
2. `POST /getTaskResult` (poll every 2s) until `status === "ready"`

## Setup

1. **Sign up** at [capzy.ai/auth/register](https://capzy.ai/auth/register) — $0.10 in real credits on signup. No card required.
2. **Get your API key** at [capzy.ai/dashboard/api-keys](https://capzy.ai/dashboard/api-keys). Keys start with `capzy_`.
3. **Export it** — every example reads `CAPZY_KEY` from the environment:
   ```bash
   export CAPZY_KEY="capzy_xxxxxxxxxxxxxxxxxxxxxxxx"
   ```
4. **Update the example** — open the file you want to run and replace any `https://example.com` / placeholder sitekey / etc. with values from the page you're actually solving against.

## Files

| Language        | File                              |
|-----------------|-----------------------------------|
| **curl / bash** | [`curl/basic.sh`](curl/basic.sh)  |
| **Python**      | [`python/basic.py`](python/basic.py) |
| **Node.js**     | [`nodejs/basic.js`](nodejs/basic.js) |

Each example is fully self-contained and ~50 lines. No SDK, no client
library, no abstraction between you and the API.

## Two challenges — how to work each one

Imperva ships two JS challenges. Send the fields for the one your target uses;
a proxy is optional for both.

### reese84 (modern)

Send `scriptUrl` (the long dashed script URL, ending in `?s=…`). We
return `reese84`. **The token comes back in the POST response BODY, not
a `Set-Cookie`** — you set the cookie client-side:

```python
sol = result["solution"]                         # from getTaskResult
r = requests.post(
    REESE_SCRIPT_URL,                            # the same URL you sent
    data=sol["reese84"],                  # raw body — do not re-encode
    headers={"Content-Type": "text/plain; charset=utf-8",
             "User-Agent": sol["userAgent"]},
)
token = r.json()["token"]                         # reese84 token is in the body
requests.get("https://www.target.example.com/",
             cookies={"reese84": token},
             headers={"User-Agent": sol["userAgent"]})
```

### utmvc (legacy)

Send `version: "utmvc"`, the `_Incapsula_Resource` `scriptUrl`, and every
`incap_ses_*` cookie from your first request. We return the `___utmvc` value —
set it alongside those session cookies and re-request:

```python
sol = result["solution"]
cookies = {**session_cookies, "___utmvc": sol["utmvc"]}   # incap_ses_*/visid_incap_* + ___utmvc
requests.get("https://www.target.example.com/",
             cookies=cookies,
             headers={"User-Agent": sol["userAgent"]})
```

Reuse the returned `userAgent` on every follow-up request in both cases.
