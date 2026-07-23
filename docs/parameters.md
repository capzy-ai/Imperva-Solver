# Parameters reference — Imperva Incapsula

Every field you can pass to `POST /createTask` for this task type.

## Envelope

```json
{
  "clientKey": "capzy_xxxxxxxxxxxxxxxxxxxxxxxx",
  "task": { ... }
}
```

| Field        | Required | Notes                                                       |
|--------------|:--------:|-------------------------------------------------------------|
| `clientKey`  | yes      | Your Capzy API key. Starts with `capzy_`. Find it at [capzy.ai/dashboard/api-keys](https://capzy.ai/dashboard/api-keys). |
| `task`       | yes      | The task object — see below.                                |

## Task object

Imperva ships two challenges — reese84 and utmvc. Pick one with **`version`**
(`"reese84"` or `"utmvc"`) and give the **one** `scriptUrl` field. Both
`AntiImpervaTaskProxyLess` and `AntiImpervaTask` accept the same fields, and a
proxy is **optional** (see below). Field names are case-insensitive
(`scriptUrl` / `scriptURL` both work).

| Field | Type | Required | Notes |
|-------|------|:--------:|-------|
| `type` | `string` | yes | `AntiImpervaTaskProxyLess` or `AntiImpervaTask` |
| `websiteURL` | `string` | yes | Full URL of the Imperva-protected page (the origin the script runs under) |
| `version` | `string` | **yes** | `reese84` (the modern challenge) or `utmvc` (the older `_Incapsula_Resource` challenge) |
| `scriptUrl` | `string` | recommended | The challenge script URL — for **both** challenges. reese84: the long dashed script path (optional — auto-detected from `websiteURL` if omitted). utmvc: the `_Incapsula_Resource` script (required) |
| `cookies` | `array` | utmvc only | Every cookie whose name begins with `incap_ses_`, each as `{name, value}`. Send these together with an `_Incapsula_Resource` `scriptUrl` |
| `userAgent` | `string` | no | User-Agent to run the script under. Default Windows Chrome; supports Chrome 135–147. Returned in the solution — reuse it |

### Proxy fields (optional — either variant)

| Field | Type | Required | Notes |
|-------|------|:--------:|-------|
| `proxyType` | `string` | no | http \| https \| socks4 \| socks5 |
| `proxyAddress` | `string` | no | IP or hostname of your proxy |
| `proxyPort` | `integer` | no | Port number of your proxy |
| `proxyLogin` | `string` | no | Optional — omit if your proxy doesn't require auth |
| `proxyPassword` | `string` | no | Optional — omit if your proxy doesn't require auth |

A proxy is never required: the payload/value we return is not bound to our
IP — you perform the final POST / cookie-set from your own IP. Supply a proxy
to run the script through a specific egress, or (sending only `websiteURL`,
no script fields) to use the classic full-browser cookie path.

## Examples

reese84 — version + the script URL:
```json
{
  "type": "AntiImpervaTaskProxyLess",
  "websiteURL": "https://www.targetWebsite.com/",
  "version": "reese84",
  "scriptUrl": "https://www.targetWebsite.com/s-weakes-Sir-Day-could-to-thy-them/1860025529848880788?s=xlD1csYd"
}
```

utmvc — version + the `_Incapsula_Resource` script URL + your `incap_ses_` cookies:
```json
{
  "type": "AntiImpervaTaskProxyLess",
  "websiteURL": "https://www.targetWebsite.com/",
  "version": "utmvc",
  "scriptUrl": "https://www.targetWebsite.com/_Incapsula_Resource?SWJIYLWA=5074a744e2e3d891814e9a2dace20bd4,719d34d31c8e3a6e6fffd425f7e032f3",
  "cookies": [
    { "name": "incap_ses_345_2269415", "value": "Twa4M6ISK2uPanH/1a/JBGZ55mcAAAAAvQkmcN6kPNJzzwCIo5w3dg==" }
  ]
}
```

## Response

### `POST /createTask` success

```json
{
  "errorId": 0,
  "taskId":  "12345"
}
```

### `POST /getTaskResult` while processing

```json
{
  "errorId": 0,
  "status":  "processing"
}
```

### `POST /getTaskResult` when ready

reese84:
```json
{
  "errorId": 0,
  "status": "ready",
  "solution": {
    "reese84": "{\"solution\":{\"interrogation\":{\"p\":\"9pp4bv7Sp0073gA1xoN9Aoo...E\",\"st\":1744612535,\"sr\":3851658681,\"cr\":937075512,\"og\":2},\"version\":\"beta\"},\"old_token\":null,\"error\":null,\"performance\":{\"interrogation\":488}}",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
  }
}
```

utmvc:
```json
{
  "errorId": 0,
  "status": "ready",
  "solution": {
    "utmvc": "8SeSQGdL+Ej2lx1PkUUE4Xp3NuDIhDkBhbW...",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
  }
}
```

The `solution` object contains:

| Field | Type | Notes |
|-------|------|-------|
| `reese84` | `string` | reese84 mode: the interrogation POST body — submit it to `scriptUrl` to receive your `reese84` cookie |
| `utmvc` | `string` | utmvc mode: the computed `___utmvc` cookie value — set it as `___utmvc` and re-request |
| `userAgent` | `string` | User-Agent used during solve — must match when you submit the payload / cookie |

### How to use the solution

- **reese84** — POST `reese84` (as the raw request body) to your
  `scriptUrl` using the returned `userAgent`. The response sets your
  `reese84` cookie. Use that cookie + the same User-Agent on subsequent
  requests.
- **utmvc** — set `___utmvc=<utmvc>` as a cookie and re-request the page with
  the same User-Agent. Imperva issues the session cookies on that request.

### Error

```json
{
  "errorId":          1,
  "errorCode":        "ERROR_KEY_DOES_NOT_EXIST",
  "errorDescription": "Invalid API key"
}
```

`errorId` is `0` on success, `1` on any error. The `errorCode` is the
stable machine-readable identifier. Common codes:

- `ERROR_KEY_DOES_NOT_EXIST` — bad API key
- `ERROR_NO_BALANCE` — account balance below the cost of this task
- `ERROR_INVALID_PARAMS` — missing required field or malformed value
- `ERROR_MAX_TASKS_REACHED` — concurrent in-flight cap reached (default 30)
- `ERROR_RATE_LIMITED` — too many createTask calls per second
- `ERROR_TIMEOUT` — solve took longer than the cap (auto-refunded)
- `ERROR_CAPTCHA_UNSOLVABLE` — solver gave up (auto-refunded)

## Naming conventions

Field names are camelCase on the wire (`websiteURL`, `websiteKey`,
`proxyAddress`). Stick to that exactly when you build the JSON.
