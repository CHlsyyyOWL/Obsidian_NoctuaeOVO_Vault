---
Module: ECON0117
---
# ECON0117 download log

Environment. Python 3.12.10, `Data/.venv`, akshare 1.19.3, pandas 3.1.0, PyMuPDF, cpca 0.5.5. Requests bypass the local proxy (127.0.0.1:7897). `Data/.gitignore` excludes `.venv/`, `raw/cache/`, `raw/pdf_2014/`.

## Outputs

`processed/financials.csv` has one row per firm-year (2009-2019) and `processed/political_connection.csv` one row per firm listed by 2014. Both currently hold the Wenzhou firms only and grow when the full market is processed. Intermediate files are in `raw/cache/`.

## Sources

| Data | Source |
|---|---|
| Firm list | ak.stock_info_a_code_name, ak.stock_info_sh_delist, ak.stock_info_sz_delist |
| Profiles (current registered address, CSRC industry, listing date, English name, actual holder) | Eastmoney F10 RPT_F10_BASIC_ORGINFO, bulk |
| Annual statements 2009-2019 | Eastmoney F10 zcfzbAjaxNew, lrbAjaxNew (endpoints behind akshare stock_*_sheet_by_yearly_em) |
| 2014 annual reports | cninfo hisAnnouncement/query, static.cninfo.com.cn |
| 2014 registered address, controller nature, chairman and GM bios | parsed from the 2014 annual reports |

Not used. push2.eastmoney.com returned 502. `stock_*_sheet_by_report_em` needs about 45 requests per firm. `stock_hold_control_cninfo` gives controller names without controller nature.

## Counts

Firm universe 5,943 (5,577 current, 372 delisted; SH 2,473, SZ 3,117, BJ 353). Eastmoney profiles 8,370 A-share records, 31 universe firms not covered (30 delisted).

Full market, paused 2026-10-26 13:22.

| Job | Done | Failures | Resume (from Data/) |
|---|---|---|---|
| Financial statements | 628 of 5,590 SH/SZ firms | 0 | `.venv/Scripts/python.exe scripts/03_financials.py` |
| 2014 report PDFs | 2,184 of 2,611 | 0 | `.venv/Scripts/python.exe scripts/05_annual_reports_2014.py` |
| cninfo profiles (cross-check only) | 1,379 of 5,943 | 0 | `.venv/Scripts/python.exe scripts/02_profiles.py` |

Wenzhou (current registered address). 41 firms, statements for 40 (1 listed in 2025), 288 firm years. 15 listed by 2014, all 15 reports found and coded. Connected 9, not connected 6, needs_review 4. In 2014 two of the 15 were registered elsewhere (思创医惠 杭州, 仁智股份 绵阳) and one was state controlled (浙江东日).

## Data limitations

1. Connections are coded from 2014 annual report bios only. A connection disclosed elsewhere is missed.
2. Family ties are coded only where a bio names a relative with a political title. Coverage is incomplete.
3. Firms registered in a city in 2014 that later moved or delisted are found only after all 2014 reports are parsed.
4. 短期借款 and 长期借款 cover loans from banks and other financial institutions, not banks only. Current portions of long-term loans are under 一年内到期的非流动负债.
5. Blank borrowing items are set to 0 because annual reports leave zero balances empty (checked for 森马服饰 2014).
