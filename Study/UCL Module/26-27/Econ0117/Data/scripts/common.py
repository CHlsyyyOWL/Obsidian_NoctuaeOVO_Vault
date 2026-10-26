"""Shared helpers for the ECON0117 data scripts.

All paths are relative to the Data/ folder. Requests bypass the local system proxy
(trust_env=False) because the proxy on 127.0.0.1:7897 drops TLS connections to the
Chinese exchange hosts.
"""
import datetime as dt
import os
import time
from pathlib import Path

import requests

for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
    os.environ.pop(k, None)

DATA = Path(__file__).resolve().parent.parent
RAW = DATA / "raw"
CACHE = RAW / "cache"
PROCESSED = DATA / "processed"
LOGS = CACHE / "logs"
for p in (RAW, CACHE, PROCESSED, LOGS):
    p.mkdir(parents=True, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def session():
    s = requests.Session()
    s.trust_env = False
    s.headers.update(UA)
    return s


def retry(fn, tries=3, wait=2.0):
    """Call fn(); on exception wait and retry, re-raising the last error."""
    last = None
    for i in range(tries):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(wait * (i + 1))
    raise last


def exchange_prefix(code: str) -> str:
    code = str(code).zfill(6)
    if code.startswith(("4", "8", "92")):
        return "BJ"
    if code.startswith(("6", "9")):
        return "SH"
    if code.startswith(("0", "2", "3")):
        return "SZ"
    return "BJ"


def log_line(name: str, text: str):
    with open(LOGS / f"{name}.log", "a", encoding="utf-8") as f:
        f.write(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}\t{text}\n")
