"""Step 5. List and download 2014 annual reports (published 2015) from cninfo.

Listing: cninfo hisAnnouncement/query, category_ndbg_szsh (annual reports), whole market,
published 2015-01-01 to 2016-06-30 in 10-day windows, deduplicated by announcementId.
All listed announcements are saved to raw/cninfo_annual_reports_2015_list.csv.

Selection per firm: title contains 2014 and 年度报告 (or 年报), and not 摘要, 英文,
English, 补充, 更正, 说明, 公告, 提示, 已取消, 广告版. If several full versions exist (original and
更新后/修订版), the latest is used and the others are recorded. Selection saved to
raw/annual_report_2014_selected.csv.

PDFs go to raw/pdf_2014/<code>_<announcementId>.pdf (git-ignored), unchanged.
Resumable, failures in raw/cache/logs/pdf2014_failed.log.
Run with --list-only to rebuild the list and selection without downloading.
"""
import datetime as dt
import sys
import time

import pandas as pd

from common import RAW, log_line, retry, session

PDF = RAW / "pdf_2014"
PDF.mkdir(exist_ok=True)
s = session()
QUERY = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
EXCL = ["摘要", "英文", "English", "english", "补充", "更正", "说明", "公告", "提示", "已取消",
        "广告版"]


def query(page, se):
    d = {"pageNum": page, "pageSize": 30, "column": "szse", "tabName": "fulltext",
         "plate": "", "stock": "", "searchkey": "", "secid": "",
         "category": "category_ndbg_szsh", "trade": "", "seDate": se, "sortName": "",
         "sortType": "", "isHLtitle": "true"}
    r = s.post(QUERY, data=d, timeout=30)
    r.raise_for_status()
    return r.json()


def list_all():
    rows = []
    start, end = dt.date(2015, 1, 1), dt.date(2016, 6, 30)
    while start <= end:
        stop = min(start + dt.timedelta(days=9), end)
        se = f"{start}~{stop}"
        page = 1
        while True:
            # totalpages from cninfo rounds down, so the page count is derived from
            # totalAnnouncement (pages past the end can repeat earlier results)
            j = retry(lambda: query(page, se))
            ann = j.get("announcements") or []
            last = -(-(j.get("totalAnnouncement") or 0) // 30)
            if not ann or page > last:
                break
            for a in ann:
                rows.append({k: a.get(k) for k in ["secCode", "secName", "orgId",
                             "announcementId", "announcementTitle", "announcementTime",
                             "adjunctUrl", "adjunctSize", "adjunctType"]})
            page += 1
            time.sleep(0.4)
        start = stop + dt.timedelta(days=1)
    df = pd.DataFrame(rows).drop_duplicates("announcementId")
    df["announcementTime"] = pd.to_datetime(df["announcementTime"], unit="ms").dt.strftime(
        "%Y-%m-%d %H:%M")
    df.to_csv(RAW / "cninfo_annual_reports_2015_list.csv", index=False, encoding="utf-8-sig")
    return df


def select(df, write=True):
    t = df["announcementTitle"].fillna("")
    is14 = t.str.contains("2014") & (t.str.contains("年度报告") | t.str.contains("年报"))
    full = is14 & ~t.apply(lambda x: any(e in x for e in EXCL))
    full &= df["adjunctUrl"].fillna("").str.upper().str.endswith(".PDF")
    sel = df[full].copy()
    sel["code"] = sel["secCode"].astype(str).str.zfill(6)
    sel = sel.sort_values(["code", "announcementTime"])
    n = sel.groupby("code")["announcementId"].transform("count")
    sel["n_full_versions"] = n
    sel["other_versions"] = sel.groupby("code")["announcementTitle"].transform(
        lambda x: " | ".join(x.iloc[:-1]))
    sel = sel.groupby("code").tail(1)
    if write:
        sel.to_csv(RAW / "annual_report_2014_selected.csv", index=False, encoding="utf-8-sig")
    return sel


def find_firm(code, name):
    """Per-firm lookup by company short name (searchkey), for firms missing from the list.

    Results are appended to raw/annual_report_2014_selected_extra.csv.
    """
    d = {"pageNum": 1, "pageSize": 30, "column": "szse", "tabName": "fulltext", "plate": "",
         "stock": "", "searchkey": name, "secid": "", "category": "category_ndbg_szsh",
         "trade": "", "seDate": "2015-01-01~2016-06-30", "sortName": "", "sortType": "",
         "isHLtitle": "true"}
    j = retry(lambda: s.post(QUERY, data=d, timeout=30).json())
    rows = [{k: a.get(k) for k in ["secCode", "secName", "orgId", "announcementId",
             "announcementTitle", "announcementTime", "adjunctUrl", "adjunctSize", "adjunctType"]}
            for a in j.get("announcements") or [] if a.get("secCode") == code]
    if not rows:
        return None
    df = pd.DataFrame(rows)
    df["announcementTime"] = pd.to_datetime(df["announcementTime"], unit="ms").dt.strftime(
        "%Y-%m-%d %H:%M")
    for c in ["announcementTitle"]:
        df[c] = df[c].str.replace(r"<[^>]+>", "", regex=True)
    sel = select(df, write=False)
    if sel.empty:
        return None
    f = RAW / "annual_report_2014_selected_extra.csv"
    old = pd.read_csv(f, dtype=str) if f.exists() else pd.DataFrame()
    pd.concat([old, sel.astype(str)]).drop_duplicates("code", keep="last").to_csv(
        f, index=False, encoding="utf-8-sig")
    return sel


def download(sel):
    stat = {"ok": 0, "cached": 0, "failed": 0}
    for _, r in sel.iterrows():
        f = PDF / f"{r['code']}_{r['announcementId']}.pdf"
        if f.exists() and f.stat().st_size > 1000:
            stat["cached"] += 1
            continue
        try:
            def get():
                x = s.get("http://static.cninfo.com.cn/" + r["adjunctUrl"], timeout=60)
                x.raise_for_status()
                if not x.content.startswith(b"%PDF"):
                    raise ValueError("not a PDF")
                return x.content
            f.write_bytes(retry(get))
            stat["ok"] += 1
            time.sleep(0.5)
        except Exception as e:  # noqa: BLE001
            log_line("pdf2014_failed", f"{r['code']}\t{r['adjunctUrl']}\t{type(e).__name__}: {e}")
            stat["failed"] += 1
        if sum(stat.values()) % 200 == 0:
            print(stat, flush=True)
    print(stat)


if __name__ == "__main__":
    df = list_all()
    sel = select(df)
    print("listed", len(df), "selected firms", len(sel))
    if "--list-only" not in sys.argv:
        download(sel)
