"""Sample step 2. Full pipeline for Wenzhou-registered firms.

Firm selection: SH/SZ firms in raw/firm_universe.csv whose CURRENT registered address in
raw/profiles_em.csv (Eastmoney F10) parses to 温州市, plus any firm whose 2014 annual
report registered address parses to 温州市 among reports already parsed.
Steps reuse the full-market scripts (shared caches): 03 financials, 05 PDF download,
06 report parsing, 07 location and pilot coding, 08 political connection coding.
Intermediate outputs in raw/cache/sample_wenzhou/ (prefix sample_wenzhou_). The deliverables
processed/financials.csv and processed/political_connection.csv are built by 09_outputs.py.
"""
import importlib
import json
import re

import pandas as pd

from common import CACHE, RAW

fin = importlib.import_module("03_financials")
rep = importlib.import_module("05_annual_reports_2014")
par = importlib.import_module("06_parse_reports_2014")
loc = importlib.import_module("07_location_pilot")
pol = importlib.import_module("08_political_connection")
OUT = CACHE / "sample_wenzhou"
OUT.mkdir(exist_ok=True)
P = "sample_wenzhou_"

# 1. firms --------------------------------------------------------------------------
uni = pd.read_csv(RAW / "firm_universe.csv", dtype=str)
uni = uni[uni["exchange"].isin(["SH", "SZ"])]
em = pd.read_csv(RAW / "profiles_em.csv", dtype=str).rename(columns={"SECURITY_CODE": "code"})
em = em[em["code"].isin(uni["code"])]
cur = loc.code_addresses(em["REG_ADDRESS"].tolist(), "reg_cur_")
cur.index = em.index
em = pd.concat([em, cur], axis=1)
wz = em[em["reg_cur_prefecture"] == "温州市"].copy()
known = CACHE / "report_2014_company_info.csv"
extra = []
if known.exists():
    k = pd.read_csv(known, dtype=str)
    k = k[k["reg_addr_2014"].notna()]
    kl = loc.parse(k["reg_addr_2014"].tolist())
    extra = [c for c, p in zip(k["code"], kl["prefecture"]) if p == "温州市" and c not in set(wz["code"])]
firms = uni[uni["code"].isin(set(wz["code"]) | set(extra))].copy()
firms = firms.merge(em, on="code", how="left")
firms["selected_by"] = firms["code"].map(lambda c: "2014_report_address" if c in extra
                                         else "current_registered_address")
print("wenzhou firms", len(firms), "extra from 2014 reports", len(extra))
codes = firms["code"].tolist()

# 2. financials -----------------------------------------------------------------------
res = {c: fin.fetch((c, e)) for c, e in zip(firms["code"], firms["exchange"])}
print("financials", pd.Series(res).value_counts().to_dict())
for st, keep, name in [("bs", fin.BS_KEEP, "balance_sheet"), ("is", fin.IS_KEEP, "income_statement")]:
    frames = []
    for c in codes:
        f = fin.OUT / f"{c}_{st}.json"
        if f.exists():
            j = json.loads(f.read_text(encoding="utf-8"))
            if j["data"]:
                d = pd.DataFrame(j["data"])
                d["company_type"] = j["company_type"]
                frames.append(d.reindex(columns=fin.ID + keep))
    df = pd.concat(frames, ignore_index=True)
    df["REPORT_DATE"] = df["REPORT_DATE"].str[:10]
    df.to_csv(OUT / f"{P}{name}_annual_2009_2019.csv", index=False, encoding="utf-8-sig")

# 3. 2014 annual reports ----------------------------------------------------------------
sel = pd.read_csv(RAW / "annual_report_2014_selected.csv", dtype=str)
sel = sel[sel["code"].isin(codes)]
rep.download(sel)
par.main(set(codes), outdir=OUT, prefix=P)
info = pd.read_csv(OUT / f"{P}report_2014_company_info.csv", dtype=str)

# 4. location and pilot coding (2014 registered address primary) -----------------------
l14 = loc.code_addresses(info["reg_addr_2014"].tolist(), "reg14_")
l14.index = info.index
info = pd.concat([info, l14], axis=1)
o14 = loc.parse(info["office_addr_2014"].tolist())
info["office14_prefecture"] = o14["prefecture"].values

# 5. political connection -------------------------------------------------------------
try:
    person, firm_pc = pol.main(OUT / f"{P}mgmt_2014_bios.csv", P)
except PermissionError:  # file open in Excel: keep the existing coding output
    print("political connection files locked, using existing outputs")
    firm_pc = pd.read_csv(OUT / f"{P}political_connection_2014_firm.csv", dtype={"code": str})

# 6. family search candidates -----------------------------------------------------------
bios = pd.read_csv(OUT / f"{P}mgmt_2014_bios.csv", dtype=str).fillna("")
roster = pd.read_csv(OUT / f"{P}mgmt_2014_roster.csv", dtype=str).fillna("")
cand = []
for code, g in bios.groupby("code"):
    snip = info.loc[info["code"] == code, "controller_snippet"].fillna("").str.cat()
    holders = firms.loc[firms["code"] == code, "ACTUAL_HOLDER"].fillna("").str.cat()
    rnames = set(roster.loc[roster["code"] == code, "name"])
    ctrl14 = sorted(n for n in rnames if n and n in snip)
    ctrl_cur = [x.strip() for x in re.split(r"[,，、]", holders) if x.strip() and x.strip() != "无"]
    for _, r in g.iterrows():
        nm = r["name"]
        if not nm:
            continue
        why = []
        for c in ctrl14 + ctrl_cur:
            if c != nm and c[:1] == nm[:1] and len(c) <= 4:
                why.append(f"same surname as actual controller {c}")
        if nm in ctrl14 or nm in ctrl_cur:
            kin = sorted(n for n in rnames if n != nm and n[:1] == nm[:1])
            if kin:
                why.append("is actual controller; same-surname board/management members " + "、".join(kin))
        other = g.loc[(g["name"] != nm) & (g["name"] != ""), "name"]
        for o in other:
            if o[:1] == nm[:1]:
                why.append(f"chairman and GM share surname ({o})")
        m = re.search(pol.RELATIVE, re.sub(r"\s+", "", r["bio"]))
        sent = ""
        if m:
            t = re.sub(r"\s+", "", r["bio"])
            s0 = max(t.rfind("。", 0, m.start()), t.rfind("；", 0, m.start())) + 1
            e0 = min([x for x in (t.find("。", m.end()), t.find("；", m.end())) if x > 0] or [len(t)])
            sent = t[s0:e0]
            why.append(f"bio mentions relative term {m.group(0)}")
        if why:
            cand.append({"code": code, "role": r["role"], "name": nm,
                         "reasons": " | ".join(dict.fromkeys(why)),
                         "controllers_2014_in_report": "、".join(ctrl14),
                         "actual_holder_current_em": holders, "relative_sentence": sent})
pd.DataFrame(cand, columns=["code", "role", "name", "reasons", "controllers_2014_in_report",
                            "actual_holder_current_em", "relative_sentence"]).to_csv(
    OUT / f"{P}family_search_candidates.csv", index=False, encoding="utf-8-sig")

# 7. firm-level file and panel ---------------------------------------------------------
fl = firms[["code", "name", "source", "delist_date", "exchange", "ORG_NAME", "SECURITY_NAME_ABBR",
            "INDUSTRYCSRC1", "LISTING_DATE", "REG_ADDRESS", "ADDRESS", "ACTUAL_HOLDER",
            "selected_by", "reg_cur_prefecture", "reg_cur_district", "reg_cur_pilot"]].copy()
fl["financial_industry"] = fl["INDUSTRYCSRC1"].fillna("").str.startswith("金融业").astype(int)
fl["listed_by_2014"] = (fl["LISTING_DATE"].fillna("9999") <= "2014-12-31").astype(int)
keep14 = ["code", "report_title", "reg_addr_2014", "office_addr_2014", "legal_rep_2014",
          "controller_nature_field", "controller_nature_2014", "controller_needs_review",
          "controller_snippet", "reg14_prefecture", "reg14_district", "reg14_pilot",
          "reg14_pilot_city", "reg14_pilot_batch", "reg14_spillover_prefecture",
          "office14_prefecture", "parse_note"]
fl = fl.merge(info[keep14], on="code", how="left")
fl = fl.merge(firm_pc, on="code", how="left")
fl["reg_vs_office_prefecture_differ_2014"] = (
    fl["reg14_prefecture"].notna() & fl["office14_prefecture"].notna() &
    (fl["reg14_prefecture"] != fl["office14_prefecture"])).astype(int)
fl["reg_prefecture_changed_since_2014"] = (
    fl["reg14_prefecture"].notna() & (fl["reg14_prefecture"] != fl["reg_cur_prefecture"])).astype(int)
fl["private_2014"] = fl["controller_nature_2014"].map(
    {"private": 1, "state": 0, "foreign": "", "none": "", "collective": "", "unknown": "",
     "mixed_keywords": ""})
fl["in_did_sample"] = ((fl["listed_by_2014"] == 1) & (fl["financial_industry"] == 0) &
                       (fl["private_2014"] == 1)).astype(int)
fl.to_csv(OUT / f"{P}firms_2014.csv", index=False, encoding="utf-8-sig")

bs = pd.read_csv(OUT / f"{P}balance_sheet_annual_2009_2019.csv", dtype={"SECURITY_CODE": str})
inc = pd.read_csv(OUT / f"{P}income_statement_annual_2009_2019.csv", dtype={"SECURITY_CODE": str})
pan = bs.merge(inc.drop(columns=["SECUCODE", "SECURITY_NAME_ABBR", "ORG_CODE", "REPORT_TYPE",
                                 "CURRENCY", "OPINION_TYPE", "company_type"], errors="ignore"),
               on=["SECURITY_CODE", "REPORT_DATE"], how="outer")
pan["year"] = pan["REPORT_DATE"].str[:4].astype(int)
pan = pan.rename(columns={"SECURITY_CODE": "code"})
pan["bank_loans"] = pan[["SHORT_LOAN", "LONG_LOAN"]].sum(axis=1, min_count=1)
pan["bank_loans_ratio"] = pan["bank_loans"] / pan["TOTAL_ASSETS"]
pan["post"] = pan["year"].map(lambda y: 1 if 2017 <= y <= 2019 else (0 if 2010 <= y <= 2015 else ""))
pan = pan.merge(fl[["code", "reg14_pilot", "reg14_pilot_batch", "connected", "needs_review",
                    "family_connected", "private_2014", "in_did_sample"]], on="code", how="left")
pan.sort_values(["code", "year"]).to_csv(OUT / f"{P}panel_2009_2019.csv", index=False,
                                          encoding="utf-8-sig")
print("panel rows", len(pan), "firms", pan["code"].nunique())
print(fl[["code", "SECURITY_NAME_ABBR", "listed_by_2014", "reg14_prefecture", "reg14_district",
          "controller_nature_2014", "chairman", "gm", "connected", "deputy", "official",
          "needs_review", "family_connected", "in_did_sample"]].to_string())
