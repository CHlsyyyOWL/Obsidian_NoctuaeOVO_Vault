"""Step 9. Build the two deliverables from the intermediate files in raw/cache.

  processed/financials.csv           one row per firm-year, 2009-2019
  processed/political_connection.csv one row per firm listed by 2014

Input sets are (folder, prefix) pairs under raw/cache, given as arguments
`folder:prefix`; default is the Wenzhou sample (sample_wenzhou:sample_wenzhou_). The full
market run will add its own set and the two files grow.
Amounts are in yuan as reported. Blank borrowings are set to 0 (annual reports leave
zero balances empty). in_sample = listed by 2014, registered address in the 2014 report
known, not state controlled in 2014, not financial, year 2010-2015 or 2017-2019, year not
before listing.
"""
import gzip
import json
import sys

import pandas as pd

from common import CACHE, PROCESSED

sets = [a.split(":") for a in sys.argv[1:]] or [["sample_wenzhou", "sample_wenzhou_"]]
with gzip.open(CACHE / "profiles_em_full.json.gz", "rt", encoding="utf-8") as f:
    en = {r["SECURITY_CODE"]: (r.get("ORG_NAME_EN") or "").strip() for r in json.load(f)}
LEVEL = {"national": "national", "provincial": "provincial", "prefecture": "city",
         "county": "county"}
OWN = {"private": "private", "state": "state", "none": "no actual controller",
       "foreign": "foreign", "collective": "collective", "unknown": "unknown"}

fin_all, pc_all = [], []
for folder, pre in sets:
    d = CACHE / folder
    firms = pd.read_csv(d / f"{pre}firms_2014.csv", dtype=str)
    pan = pd.read_csv(d / f"{pre}panel_2009_2019.csv", dtype={"code": str})
    person = pd.read_csv(d / f"{pre}political_connection_2014.csv", dtype=str).fillna("")

    # political connection, one row per firm listed by 2014
    rows = []
    for _, r in firms[firms["listed_by_2014"] == "1"].iterrows():
        g = person[person["code"] == r["code"]]
        chair = "、".join(dict.fromkeys(g.loc[g["role"] == "chairman", "name"].tolist()))
        gm = "、".join(dict.fromkeys(g.loc[g["role"] == "gm", "name"].tolist()))
        if pd.isna(r["report_title"]):
            con, typ = "", "not coded: 2014 report missing"
        elif pd.to_numeric(r.get("bio_found_any"), errors="coerce") != 1:
            con, typ = "", "not coded: biography not found"
        else:
            typ_l, kw_l, sent_l = [], [], []
            for _, x in g[g["connected"] == "1"].iterrows():
                role = "Chairman" if x["role"] == "chairman" else "GM"
                if x["deputy_keyword"]:
                    body = "NPC deputy" if ("人大" in x["deputy_keyword"] or
                                            "人民代表" in x["deputy_keyword"]) else "CPPCC member"
                    lv = LEVEL.get(x["highest_level_guess"], "")
                    typ_l.append(f"{role}: {body}" + (f" ({lv})" if lv else ""))
                    kw_l.append(x["deputy_keyword"])
                    sent_l.append(x["deputy_sentence"])
                for k, lab in [("official", "government official"), ("military", "military")]:
                    if x[f"{k}_keyword"]:
                        typ_l.append(f"{role}: {lab}")
                        kw_l.append(x[f"{k}_keyword"])
                        sent_l.append(x[f"{k}_sentence"])
            con = "Yes" if typ_l else "No"
            typ = "; ".join(dict.fromkeys(typ_l)) or "None"
        rv = g["review_keywords"].tolist() if "review_keywords" in g else []
        rows.append({
            "code": r["code"], "name_en": en.get(r["code"], ""), "name_cn": r["SECURITY_NAME_ABBR"],
            "chairman_2014": chair, "gm_2014": gm, "connected": con, "connection_type": typ,
            "keyword": " | ".join(dict.fromkeys(kw_l)) if con == "Yes" else "",
            "source_sentence": " | ".join(dict.fromkeys(sent_l)) if con == "Yes" else "",
            "family_connected": "Yes" if "1" in g.get("family_connected", pd.Series()).tolist() else
                                ("No" if con else ""),
            "needs_review": "Yes" if "1" in g.get("needs_review", pd.Series()).tolist() else
                            ("No" if con else ""),
            "review_note": " | ".join(x for x in dict.fromkeys(rv) if x),
        })
    pc_all.append(pd.DataFrame(rows))

    # financials, one row per firm-year
    f = firms.set_index("code")
    p = pd.DataFrame({"code": pan["code"], "year": pan["year"]})
    p["name_en"] = p["code"].map(en)
    p["name_cn"] = p["code"].map(f["SECURITY_NAME_ABBR"])
    p["reg_city_2014"] = p["code"].map(f["reg14_prefecture"])
    p["reg_district_2014"] = p["code"].map(f["reg14_district"])
    p["reg_city_current"] = p["code"].map(f["reg_cur_prefecture"])
    p["pilot"] = p["code"].map(f["reg14_pilot"])
    p["pilot_batch"] = p["code"].map(f["reg14_pilot_batch"])
    p["listing_date"] = p["code"].map(f["LISTING_DATE"])
    p["ownership_2014"] = p["code"].map(f["controller_nature_2014"]).map(OWN)
    p["industry_csrc"] = p["code"].map(f["INDUSTRYCSRC1"])
    p["short_term_borrowings"] = pan["SHORT_LOAN"].fillna(0)
    p["long_term_borrowings"] = pan["LONG_LOAN"].fillna(0)
    p["noncurrent_liab_due_1y"] = pan["NONCURRENT_LIAB_1YEAR"].fillna(0)
    p["total_assets"] = pan["TOTAL_ASSETS"]
    p["fixed_assets"] = pan["FIXED_ASSET"]
    p["total_liabilities"] = pan["TOTAL_LIABILITIES"]
    p["revenue"] = pan["TOTAL_OPERATE_INCOME"]
    p["net_profit"] = pan["NETPROFIT"]
    p["financial_expense"] = pan["FINANCE_EXPENSE"]
    p["interest_expense"] = pan["FE_INTEREST_EXPENSE"]
    p["loan_ratio"] = (p["short_term_borrowings"] + p["long_term_borrowings"]) / p["total_assets"]
    p["post"] = p["year"].map(lambda y: 1 if 2017 <= y <= 2019 else (0 if 2010 <= y <= 2015 else ""))
    listed = p["listing_date"].fillna("9999").str[:4]
    ok_firm = p["code"].map((f["listed_by_2014"] == "1") & f["reg14_prefecture"].notna() &
                            (f["controller_nature_2014"] != "state") &
                            (f["financial_industry"] != "1"))
    p["in_sample"] = (ok_firm & (p["post"] != "") &
                      (p["year"] >= pd.to_numeric(listed, errors="coerce"))).astype(int)
    fin_all.append(p)

fin = pd.concat(fin_all).sort_values(["code", "year"])
pc = pd.concat(pc_all).sort_values("code")
fin.to_csv(PROCESSED / "financials.csv", index=False, encoding="utf-8-sig")
pc.to_csv(PROCESSED / "political_connection.csv", index=False, encoding="utf-8-sig")
s = fin[fin["in_sample"] == 1]
print("financials rows", len(fin), "firms", fin["code"].nunique(), "| in_sample rows", len(s),
      "firms", s["code"].nunique())
print("political_connection firms", len(pc), pc["connected"].value_counts().to_dict())
