"""Step 7. Parse addresses to province / prefecture / district and code SCS pilot status.

Parser: cpca 0.5.5 (bundled administrative division table). For the four municipalities
the prefecture is the municipality itself. Coding rule (decided by Chelsea): treatment
follows the REGISTERED address.
  prefecture-level and sub-provincial pilots: every firm registered in that prefecture
  municipal-district pilots (北京市海淀区, 上海市浦东新区, 上海市嘉定区): only firms
      registered in that district
  county-level pilots (义乌市, 荣成市, 绥芬河市): only firms registered in that county-level
      city; spillover_prefecture=1 for other firms of 金华市 and 牡丹江市 (威海市 is itself
      a pilot, so all 威海 firms are treated)
District inference for Beijing and Shanghai addresses that omit the district uses the
place-name lists below and sets district_inferred=1. A Beijing or Shanghai address whose
district is still unknown gets pilot_district_unresolved=1 and pilot left blank.
The pilot list ECON0117_SCS_pilot_cities.csv is read only.
"""
import re
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
import cpca  # noqa: E402

from common import DATA  # noqa: E402

PILOTS = pd.read_csv(DATA / "ECON0117_SCS_pilot_cities.csv", dtype=str)
MUNI = {"北京市", "上海市", "天津市", "重庆市"}
INFER = {
    "上海市": [("浦东新区", r"自由贸易试验区|自贸区|张江|陆家嘴|外高桥|金桥|川沙|周浦|康桥|惠南|南汇|临港|洋山|"
                       r"世纪大道|浦东"),
              ("嘉定区", r"嘉定|安亭|南翔|江桥|马陆|外冈|徐行|华亭")],
    "北京市": [("海淀区", r"海淀|中关村科技园区海淀园|上地|西三旗|清河|苏州街|学院路|西北旺|温泉镇|四季青")],
}
REVIEW_KW = r"洋山|临港|中关村(?!科技园区海淀园)"


def parse(addrs):
    a = pd.Series(addrs, dtype=object).fillna("").astype(str)
    a = a.str.replace(r"^中国[·\s]*", "", regex=True).str.split(r",|，\s*(?=浙江|江苏|广东)").str[0]
    loc = cpca.transform(a.tolist())
    out = pd.DataFrame({"addr": a.values, "province": loc["省"].values, "prefecture": loc["市"].values,
                        "district": loc["区"].values})
    m = out["province"].isin(MUNI)
    out.loc[m, "prefecture"] = out.loc[m, "province"]
    out["district_inferred"] = 0
    for pref, rules in INFER.items():
        for dist, pat in rules:
            sel = (out["prefecture"] == pref) & out["district"].isna() & out["addr"].str.contains(pat)
            out.loc[sel, "district"] = dist
            out.loc[sel, "district_inferred"] = 1
    out["location_review"] = out["addr"].str.contains(REVIEW_KW).astype(int)
    return out


def code_pilot(loc):
    loc = loc.copy()
    loc["pilot"], loc["pilot_city"], loc["pilot_batch"], loc["pilot_admin_level"] = 0, "", "", ""
    for _, p in PILOTS.iterrows():
        if p["admin_level"] in ("prefecture city", "sub-provincial city"):
            sel = loc["prefecture"] == p["city_cn"]
        elif p["admin_level"] == "municipal district":
            dist = p["city_cn"].replace(p["prefecture_cn"], "")
            sel = (loc["prefecture"] == p["prefecture_cn"]) & (loc["district"] == dist)
        else:  # county-level city
            sel = (loc["prefecture"] == p["prefecture_cn"]) & (loc["district"] == p["city_cn"])
        new = sel & (loc["pilot"] == 0)
        loc.loc[new, ["pilot_city", "pilot_batch", "pilot_admin_level"]] = \
            [p["city_cn"], p["batch"], p["admin_level"]]
        both = sel & (loc["pilot"] == 1)
        loc.loc[both, "pilot_city"] = loc.loc[both, "pilot_city"] + "|" + p["city_cn"]
        loc.loc[sel, "pilot"] = 1
    loc["spillover_prefecture"] = (loc["prefecture"].isin(["金华市", "牡丹江市"]) &
                                   (loc["pilot"] == 0)).astype(int)
    unres = loc["prefecture"].isin(["北京市", "上海市"]) & loc["district"].isna()
    loc["pilot_district_unresolved"] = unres.astype(int)
    loc["pilot"] = loc["pilot"].astype(object)
    loc.loc[unres, "pilot"] = ""
    loc.loc[loc["prefecture"].isna(), "pilot"] = ""
    return loc


def code_addresses(addrs, prefix):
    loc = code_pilot(parse(addrs))
    return loc.add_prefix(prefix)


if __name__ == "__main__":
    test = ["浙江省义乌市稠州北路", "浙江省金华市婺城区", "山东省荣成市", "山东省威海市环翠区",
            "中国（上海）自由贸易试验区张江路665号", "上海市长宁区", "北京市中关村科技园区",
            "北京市海淀区上地十街", "黑龙江省牡丹江市东安区", "江苏省江阴市", "温州经济技术开发区滨海三道"]
    print(code_pilot(parse(test)).to_string())
