"""Step 3. Annual (12-31) consolidated balance sheet and income statement, 2009-2019.

Source: the Eastmoney F10 endpoints that akshare's stock_balance_sheet_by_yearly_em and
stock_profit_sheet_by_yearly_em wrap (zcfzbAjaxNew, lrbAjaxNew, reportDateType=1,
reportType=1). Calling them directly with only the 11 needed dates takes ~7 requests per
firm instead of ~45 for the *_by_report_em functions, which would need ~100 hours.

Scope: SH and SZ codes in raw/firm_universe.csv (BJ codes were not A-share listed in
2009-2019). Resumable: full JSON per firm and statement cached in raw/cache/fin/.
Failures go to raw/cache/logs/financials_failed.log.
Lean outputs (design fields only, values as reported in yuan):
  raw/balance_sheet_annual_2009_2019.csv.gz
  raw/income_statement_annual_2009_2019.csv.gz
Run with --combine to only rebuild the lean files from the cache.
"""
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from common import CACHE, RAW, log_line, retry, session

OUT = CACHE / "fin"
OUT.mkdir(exist_ok=True)
BASE = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/"
YEARS = range(2009, 2020)
CHUNKS = [",".join(f"{y}-12-31" for y in list(YEARS)[i:i + 5]) for i in range(0, 11, 5)]
ENDPOINT = {"bs": "zcfzbAjaxNew", "is": "lrbAjaxNew"}
ID = ["SECUCODE", "SECURITY_CODE", "SECURITY_NAME_ABBR", "ORG_CODE", "REPORT_DATE",
      "REPORT_TYPE", "CURRENCY", "OPINION_TYPE", "company_type"]
BS_KEEP = ["SHORT_LOAN", "LONG_LOAN", "NONCURRENT_LIAB_1YEAR", "BOND_PAYABLE",
           "TOTAL_ASSETS", "FIXED_ASSET", "TOTAL_LIABILITIES", "TOTAL_CURRENT_ASSETS",
           "TOTAL_CURRENT_LIAB", "TOTAL_EQUITY", "TOTAL_PARENT_EQUITY"]
IS_KEEP = ["TOTAL_OPERATE_INCOME", "OPERATE_INCOME", "OPERATE_COST", "FINANCE_EXPENSE",
           "FE_INTEREST_EXPENSE", "FE_INTEREST_INCOME", "INTEREST_EXPENSE", "OPERATE_PROFIT",
           "TOTAL_PROFIT", "NETPROFIT", "PARENT_NETPROFIT"]
local = threading.local()


def sess():
    if not hasattr(local, "s"):
        local.s = session()
    return local.s


def get_json(endpoint, params):
    r = sess().get(BASE + endpoint, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def company_type(code):
    r = sess().get(BASE + "Index", params={"type": "web", "code": code.lower()}, timeout=20)
    m = re.search(r'id="hidctype"[^>]*value="(\d+)"', r.text)
    if not m:
        raise ValueError("hidctype not found")
    return m.group(1)


def done(code, st):
    """A cached statement counts as done only if it holds data (empty files are refetched)."""
    f = OUT / f"{code}_{st}.json"
    return f.exists() and bool(json.loads(f.read_text(encoding="utf-8"))["data"])


def fetch(row):
    code, ex = row
    sym = ex + code
    todo = [st for st in ENDPOINT if not done(code, st)]
    if not todo:
        return "cached"
    try:
        ct0 = retry(lambda: company_type(sym))
        for st in todo:
            # the F10 page reports a wrong company type for some delisted firms, so an
            # empty result is retried with the other types (4 general, 1 securities,
            # 2 insurance, 3 bank)
            for ct in [ct0] + [c for c in "4123" if c != ct0]:
                data = []
                for dates in CHUNKS:
                    p = {"companyType": ct, "reportDateType": "1", "reportType": "1",
                         "dates": dates, "code": sym}
                    j = retry(lambda: get_json(ENDPOINT[st], p))
                    data += j.get("data", []) or []
                    time.sleep(0.4)
                if data:
                    break
            (OUT / f"{code}_{st}.json").write_text(
                json.dumps({"company_type": ct, "company_type_page": ct0, "data": data},
                           ensure_ascii=False), encoding="utf-8")
        return "ok"
    except Exception as e:  # noqa: BLE001
        log_line("financials_failed", f"{code}\t{type(e).__name__}: {e}")
        return "failed"


def combine():
    for st, keep, name in [("bs", BS_KEEP, "balance_sheet"), ("is", IS_KEEP, "income_statement")]:
        frames = []
        for f in sorted(OUT.glob(f"*_{st}.json")):
            j = json.loads(f.read_text(encoding="utf-8"))
            if not j["data"]:
                continue
            df = pd.DataFrame(j["data"])
            df["company_type"] = j["company_type"]
            frames.append(df.reindex(columns=ID + keep))
        out = pd.concat(frames, ignore_index=True)
        out["REPORT_DATE"] = out["REPORT_DATE"].str[:10]
        out.to_csv(RAW / f"{name}_annual_2009_2019.csv.gz", index=False,
                   encoding="utf-8-sig", compression="gzip")
        print(name, out.shape, out["REPORT_DATE"].value_counts().sort_index().to_dict())


if __name__ == "__main__":
    if "--combine" not in sys.argv:
        uni = pd.read_csv(RAW / "firm_universe.csv", dtype=str)
        uni = uni[uni["exchange"].isin(["SH", "SZ"])]
        rows = list(zip(uni["code"], uni["exchange"]))
        done = 0
        with ThreadPoolExecutor(max_workers=3) as ex:
            res = []
            for r in ex.map(fetch, rows):
                res.append(r)
                done += 1
                if done % 200 == 0:
                    print(done, pd.Series(res).value_counts().to_dict(), flush=True)
        print(pd.Series(res).value_counts().to_dict())
    combine()
