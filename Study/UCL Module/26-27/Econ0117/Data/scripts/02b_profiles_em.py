"""Step 2b. Company profiles from the Eastmoney F10 company survey (bulk).

Source: datacenter.eastmoney.com RPT_F10_BASIC_ORGINFO (the dataset behind the F10
公司概况 page), all A-share records (SECURITY_TYPE_CODE 058001001), 500 per page.
These are CURRENT values (registered address, chairman, actual holder as of today).
Full response cached in raw/cache/profiles_em_full.json.gz. Lean output:
raw/profiles_em.csv
"""
import gzip
import json
import time

import pandas as pd

from common import CACHE, RAW, retry, session

URL = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
KEEP = ["SECURITY_CODE", "SECUCODE", "SECURITY_NAME_ABBR", "ORG_NAME", "FORMERNAME",
        "SECURITY_TYPE", "TRADE_MARKET", "INDUSTRYCSRC1", "PROVINCE", "REG_ADDRESS",
        "ADDRESS", "LISTING_DATE", "FOUND_DATE", "CHAIRMAN", "PRESIDENT", "LEGAL_PERSON",
        "ACTUAL_HOLDER"]
s = session()


def page(n):
    r = s.get(URL, params={"reportName": "RPT_F10_BASIC_ORGINFO", "columns": "ALL",
                           "filter": '(SECURITY_TYPE_CODE="058001001")', "pageNumber": n,
                           "pageSize": 500, "source": "HSF10", "client": "PC"}, timeout=30)
    r.raise_for_status()
    return r.json()["result"]


first = retry(lambda: page(1))
rows = list(first["data"])
for n in range(2, first["pages"] + 1):
    rows += retry(lambda: page(n))["data"]
    time.sleep(0.5)
with gzip.open(CACHE / "profiles_em_full.json.gz", "wt", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False)
df = pd.DataFrame(rows).reindex(columns=KEEP)
for c in ["LISTING_DATE", "FOUND_DATE"]:
    df[c] = df[c].astype(str).str[:10].replace("None", "")
df = df.drop_duplicates("SECURITY_CODE")
df.to_csv(RAW / "profiles_em.csv", index=False, encoding="utf-8-sig")
print("count reported", first["count"], "rows", len(df))
print(df["SECURITY_TYPE"].value_counts().to_dict())
