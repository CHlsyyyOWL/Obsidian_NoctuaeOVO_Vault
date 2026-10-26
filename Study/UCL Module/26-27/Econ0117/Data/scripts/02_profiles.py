"""Step 2. Company profiles from cninfo (ak.stock_profile_cninfo) for every firm.

Resumable: each firm's full response is cached in raw/cache/profiles/<code>.csv and
skipped on rerun. Failures (after 3 tries) go to raw/cache/logs/profiles_failed.log.
Lean combined output: raw/profiles_cninfo.csv (design fields only).
Run with --combine to only rebuild the combined file from the cache.
"""
import sys
import time

import akshare as ak
import pandas as pd

from common import CACHE, RAW, log_line, retry

OUT = CACHE / "profiles"
OUT.mkdir(exist_ok=True)
KEEP = ["公司名称", "A股代码", "A股简称", "所属市场", "所属行业", "法人代表", "成立日期",
        "上市日期", "注册地址", "办公地址"]


def fetch(code):
    f = OUT / f"{code}.csv"
    if f.exists():
        return "cached"
    try:
        df = retry(lambda: ak.stock_profile_cninfo(symbol=code))
        if df is None or df.empty:
            log_line("profiles_failed", f"{code}\tempty response")
            return "empty"
        df.to_csv(f, index=False, encoding="utf-8-sig")
        time.sleep(0.5)
        return "ok"
    except Exception as e:  # noqa: BLE001
        log_line("profiles_failed", f"{code}\t{type(e).__name__}: {e}")
        return "failed"


def combine():
    rows = []
    for f in sorted(OUT.glob("*.csv")):
        df = pd.read_csv(f, dtype=str)
        r = {k: df[k].iloc[0] if k in df.columns else None for k in KEEP}
        r["code"] = f.stem
        rows.append(r)
    out = pd.DataFrame(rows)[["code"] + KEEP]
    out.to_csv(RAW / "profiles_cninfo.csv", index=False, encoding="utf-8-sig")
    print("combined profiles", len(out))


if __name__ == "__main__":
    if "--combine" not in sys.argv:
        uni = pd.read_csv(RAW / "firm_universe.csv", dtype=str)
        codes = uni["code"].tolist()
        # single thread: akshare's cninfo header key runs in py_mini_racer (V8),
        # which crashes when called from several threads
        res = []
        for i, c in enumerate(codes, 1):
            res.append(fetch(c))
            if i % 200 == 0:
                print(i, pd.Series(res).value_counts().to_dict(), flush=True)
        print(pd.Series(res).value_counts().to_dict())
    combine()
