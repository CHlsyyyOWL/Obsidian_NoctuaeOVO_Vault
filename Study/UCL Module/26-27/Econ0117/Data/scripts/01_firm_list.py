"""Step 1. Firm universe: current A-share list plus SSE and SZSE delisted lists.

Delisted firms are added so the 2009-2019 panel is not limited to survivors.
Outputs
  raw/a_share_code_name.csv     ak.stock_info_a_code_name() as returned
  raw/delisted_sh.csv           ak.stock_info_sh_delist() as returned
  raw/delisted_sz.csv           ak.stock_info_sz_delist() as returned
  raw/firm_universe.csv         union with exchange prefix and source flag
"""
import akshare as ak
import pandas as pd

from common import RAW, exchange_prefix, retry

cur = retry(ak.stock_info_a_code_name)
cur.to_csv(RAW / "a_share_code_name.csv", index=False, encoding="utf-8-sig")
sh = retry(ak.stock_info_sh_delist)
sh.to_csv(RAW / "delisted_sh.csv", index=False, encoding="utf-8-sig")
sz = retry(ak.stock_info_sz_delist)
sz.to_csv(RAW / "delisted_sz.csv", index=False, encoding="utf-8-sig")

u = pd.DataFrame({"code": cur["code"].astype(str).str.zfill(6), "name": cur["name"],
                  "source": "current"})
d1 = pd.DataFrame({"code": sh["公司代码"].astype(str).str.zfill(6), "name": sh["公司简称"],
                   "source": "delisted_sh", "delist_date": sh["暂停上市日期"].astype(str)})
d2 = pd.DataFrame({"code": sz["证券代码"].astype(str).str.zfill(6), "name": sz["证券简称"],
                   "source": "delisted_sz", "delist_date": sz["终止上市日期"].astype(str)})
d = pd.concat([d1, d2])
d = d[~d["code"].isin(u["code"])]
uni = pd.concat([u, d], ignore_index=True).drop_duplicates("code")
uni["exchange"] = uni["code"].map(exchange_prefix)
uni.to_csv(RAW / "firm_universe.csv", index=False, encoding="utf-8-sig")
print("current", len(cur), "delisted_sh", len(sh), "delisted_sz", len(sz), "universe", len(uni))
print(uni["exchange"].value_counts().to_dict())
