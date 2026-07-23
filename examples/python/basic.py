"""
Solve Imperva Incapsula with Capzy — minimal Python example, `requests` only.

Cost:   from $0.001 per solve (flat)
Speed:  ~10 seconds median

Run with:
    pip install requests
    export CAPZY_KEY="capzy_xxxxxxxxxxxxxxxxxxxxxxxx"
    python basic.py
"""

import os
import time

import requests

API_BASE = "https://api.capzy.ai"

# Grab a key for free at https://capzy.ai/auth/register ($0.10 starter credit).
CAPZY_KEY = os.environ["CAPZY_KEY"]


def solve() -> dict:
    # 1) Create the task. Returns immediately with a taskId; the actual
    #    solve runs on Capzy's infrastructure.
    created = requests.post(
        f"{API_BASE}/createTask",
        json={
            "clientKey": CAPZY_KEY,
            "task": {
                "type": "AntiImpervaTaskProxyLess",
                "websiteURL": "https://www.example.com/",
                "version": "reese84",
                # reese84: pass the script URL (long dashed path, ?s=...).
                # Omit scriptUrl and we auto-detect it from websiteURL.
                "scriptUrl": "https://www.example.com/s-weakes-Sir-Day/1860025529848880788?s=xlD1csYd",
                # For the older utmvc challenge instead, send:
                #   "scriptUrl": "https://www.example.com/_Incapsula_Resource?SWJIYLWA=...",
                #   "version": "utmvc",
                #   "cookies": [{"name": "incap_ses_345_2269415", "value": "..."}],
            },
        },
        timeout=15,
    ).json()

    if created.get("errorId"):
        raise RuntimeError(f"createTask failed: {created.get('errorCode')} — "
                           f"{created.get('errorDescription')}")

    task_id = created["taskId"]
    print(f"created task {task_id}")

    # 2) Poll until ready. Cap the wait at 120s for slower captcha types.
    deadline = time.time() + 120
    while time.time() < deadline:
        result = requests.post(
            f"{API_BASE}/getTaskResult",
            json={"clientKey": CAPZY_KEY, "taskId": task_id},
            timeout=15,
        ).json()

        if result.get("errorId"):
            raise RuntimeError(f"getTaskResult failed: {result.get('errorCode')} — "
                               f"{result.get('errorDescription')}")

        if result["status"] == "ready":
            return result["solution"]

        time.sleep(2)

    raise TimeoutError("solve took longer than 120s")


if __name__ == "__main__":
    solution = solve()
    print("solution:", solution)
    # ─── How to use the result ────────────────────────────────────
    # reese84: POST solution["reese84"] (raw body) to your
    #   scriptUrl with solution["userAgent"] — the response sets your
    #   reese84 cookie. Reuse that cookie + User-Agent afterwards.
    # utmvc:   set ___utmvc=solution["utmvc"] as a cookie and re-request
    #   the page with the same User-Agent.
