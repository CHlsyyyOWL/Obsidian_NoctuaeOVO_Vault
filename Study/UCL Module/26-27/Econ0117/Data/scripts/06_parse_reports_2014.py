"""Step 6. Parse the 2014 annual report PDFs (raw/pdf_2014) with PyMuPDF.

For every PDF the full text is cached in raw/cache/text_2014/<code>.txt (git-ignored).
Extracted per firm (rule based, every value keeps the source snippet):
  raw/cache/report_2014_company_info.csv
      registered and office address as printed in the 2014 report
      actual controller section snippet and a rule-based nature code
  raw/cache/mgmt_2014_roster.csv
      directors, supervisors and senior managers parsed from the shareholding table
      (name, position text, status 现任/离任)
  raw/cache/mgmt_2014_bios.csv
      chairman (董事长) and general manager (总经理/总裁) with full biography text
Rules are documented inline. Nothing is guessed: if a field is not found it is blank and
parse_note says why.
"""
import re
import sys

import pandas as pd
import pymupdf

from common import CACHE, RAW

TXT = CACHE / "text_2014"
TXT.mkdir(exist_ok=True)
NAME = re.compile(r"^[一-龥·]{2,5}$")
GENDER = {"男", "女"}
STATUS = {"现任", "离任"}
NOT_NAME = {"姓名", "职务", "性别", "年龄", "现任", "离任", "董事", "监事", "董事长", "总经理",
            "副总经理", "独立董事", "财务总监", "董事会秘书", "职工监事", "监事会主席", "合计",
            "总裁", "副总裁", "副董事长", "任职状态", "不适用", "适用", "人民币", "单位", "万元",
            "事业", "中心", "公司", "集团", "本部", "营销", "技术", "研发", "生产", "质量", "销售",
            "财务", "行政", "人力", "资源", "管理", "运营", "分公司", "子公司", "工程", "采购"}
NOT_NAME_END = ("部", "处", "室", "中心", "公司", "厂", "组", "院", "所")


def text_of(code, pdf):
    f = TXT / f"{code}.txt"
    if f.exists():
        return f.read_text(encoding="utf-8")
    with pymupdf.open(pdf) as d:
        t = "\n".join(p.get_text() for p in d)
    f.write_text(t, encoding="utf-8")
    return t


def clean(s):
    return re.sub(r"\s+", "", s or "")


def field_after(txt, label_re, stop_re=r"邮政编码|邮编"):
    """Value printed on the line(s) after a label such as 注册地址."""
    for m in re.finditer(label_re, txt):
        rest = txt[m.end():m.end() + 200]
        if re.match(r"\s*的", rest):  # 注册地址的邮政编码
            continue
        rest = re.split(r"\n\s*(?:公司)?(?:注册地址|办公地址|注册、办公地址|" + stop_re + r"|公司网址|网址)", rest)[0]
        v = clean(rest.lstrip("：: \n"))
        if v and not v.startswith(("的", "邮政")):
            return v[:120]
    return ""


STATE_KW = ["国有资产监督管理", "国资委", "国务院", "人民政府", "财政部", "财政厅", "财政局",
            "中央国资", "地方国资", "国有资产管理", "中央国家机关", "中国科学院", "教育部",
            "国有独资", "国家开发投资", "中央企业"]
PRIVATE_KW = ["境内自然人", "自然人", "实际控制人姓名", "个人"]
FOREIGN_KW = ["境外自然人", "外国", "境外法人"]
NONE_KW = ["无实际控制人", "不存在实际控制人", "没有实际控制人", "无控股股东及实际控制人"]


def controller(txt):
    """Locate the actual controller block and code its nature.

    Priority 1: an explicit field 实际控制人性质 (used in most SZSE reports).
    Priority 2: keywords in the 800 characters after the 实际控制人情况 heading that
    actually describes the controller (the window must mention 自然人, 国资/国有, 人民政府,
    名称/姓名 or 无实际控制人 within its first 300 characters).
    Mixed state and private keywords give needs_review=1.
    """
    m = re.search(r"实际控制人性质\s*[：:]?\s*\n?\s*([^\n]{1,30})", txt)
    explicit = clean(m.group(1)) if m else ""
    win = ""
    for mm in re.finditer(r"实际控制人(?:情况|基本情况|介绍)", txt):
        w = txt[mm.start():mm.start() + 1000]
        if re.search(r"控股股东(?:情况|及)", w[:40]):
            continue  # chapter heading 控股股东及实际控制人情况 followed by the holder block
        head = w[:300]
        if any(k in head for k in ["自然人", "国资", "国有", "人民政府", "姓名", "名称",
                                   "无实际控制人", "不存在实际控制人", "国务院"]):
            if "股东总数" in head[:120] or "股东数量" in head[:120]:
                continue
            win = w
            break
    probe = explicit + " " + clean(win)
    st = any(k in probe for k in STATE_KW)
    fo = any(k in probe for k in FOREIGN_KW)
    pr = any(k in probe for k in PRIVATE_KW)
    no = any(k in probe for k in NONE_KW)
    if explicit:
        if any(k in explicit for k in ["国资", "国有", "国家机关", "政府", "中央", "地方"]):
            nat, rev = "state", 0
        elif "境外" in explicit or "外国" in explicit:
            nat, rev = "foreign", 0
        elif "自然人" in explicit:
            nat, rev = "private", 0
        elif "集体" in explicit:
            nat, rev = "collective", 0
        elif "无" in explicit or "不存在" in explicit:
            nat, rev = "none", 0
        else:
            nat, rev = "unknown", 1
    elif no and not (st or pr):
        nat, rev = "none", 0
    elif st and not pr:
        nat, rev = "state", 0
    elif pr and not st:
        nat, rev = ("foreign", 0) if fo else ("private", 0)
    elif st and pr:
        nat, rev = "mixed_keywords", 1
    else:
        nat, rev = "unknown", 1
    if "集体" in probe and nat != "collective":
        rev = 1
    return explicit, clean(win)[:400], nat, rev


def legal_rep(txt):
    m = re.search(r"(?:公司)?法定代表人\s*[：:]?\s*\n?\s*([一-龥·\s]{2,8}?)\s*\n", txt)
    return clean(m.group(1)) if m else ""


def mgmt_chapter(txt):
    """Text of the chapter on directors, supervisors and senior management."""
    starts = [m.start() for m in re.finditer(r"董事、监事、高级管理人员(?:和员工)?情况", txt)]
    # first heading occurrence after the table of contents (skip hits in the first 4%)
    body = [s for s in starts if s > len(txt) * 0.04 and "....." not in txt[s:s + 120]]
    if not body:
        # heading not recognised (e.g. duplicated bold text): anchor on the bio block
        m = re.search(r"主要工作经历", txt[int(len(txt) * 0.04):])
        if not m:
            return ""
        s = int(len(txt) * 0.04) + m.start()
        return txt[max(0, s - 15000):s + 40000]
    s = body[0]
    end = re.search(r"\n\s*第[一二三四五六七八九十]+节\s*公司治理|\n\s*第[一二三四五六七八九十]+节",
                    txt[s + 200:])
    return txt[s:s + 200 + (end.start() if end else 60000)]


POS_CHARS = set("董事监会长副总经理裁独立职工财务首席执行官常务秘书技术营销运营兼及和、，,"
                "主席助理负责人工程师代行高级管理人员非外部股东代表党委书记行长"
                "CEOCFOCOOCTO（）()·/ ")
POS_KEY = ["董事", "监事", "经理", "总裁", "秘书", "总监", "主席", "负责人", "总工", "行长"]


def is_pos(tok):
    t = tok.strip()
    return bool(t) and set(t) <= POS_CHARS and (any(k in t for k in POS_KEY) or len(t) <= 3)


def is_name(tok):
    return (bool(NAME.match(tok)) and tok not in NOT_NAME and not set(tok) <= POS_CHARS
            and not tok.endswith(NOT_NAME_END))


def tokens(ch):
    """Whitespace tokens; consecutive single Chinese characters are merged (董 伟 -> 董伟)."""
    raw = ch.split()
    out = []
    for t in raw:
        if (len(t) == 1 and re.match(r"[一-龥]", t) and t not in GENDER and out
                and len(out[-1]) == 1 and re.match(r"[一-龥]", out[-1])
                and out[-1] not in GENDER):
            out[-1] += t
        else:
            out.append(t)
    return out


def roster(ch):
    """Parse name / position / status rows of the management tables.

    Anchored on every gender token (男/女). Layout A (most reports): name, position
    tokens, optional 现任/离任, gender. Layout B (some SSE reports): name, birth year,
    gender, position. The name is the first name-like token before the anchor that is
    not a position word; header fragments fail the name or position checks.
    """
    tk = tokens(ch[:60000])
    out, seen = [], set()
    for g, t in enumerate(tk):
        if t not in GENDER:
            continue
        pos, status, name = [], "", ""
        for k in range(1, 7):
            if g - k < 0:
                break
            x = tk[g - k]
            if x in STATUS:
                status = x
                continue
            if is_pos(x):
                pos.insert(0, x)
                continue
            if re.fullmatch(r"\d{4}\s*年?", x) or x == "年":
                continue
            if is_name(x):
                name = x
            break
        if not name:
            continue
        if not pos:  # layout B, position after the gender token
            for x in tk[g + 1:g + 4]:
                if is_pos(x):
                    pos.append(x)
                elif pos:
                    break
        title = "".join(pos).strip("、，, ")
        if title.startswith(("部", "处", "室", "副经理", "经理")):
            continue  # the "name" was the first half of a department title
        if not title or not any(k in title for k in POS_KEY):
            continue
        key = (name, title)
        if key not in seen:
            seen.add(key)
            out.append({"name": name, "position": title, "status": status})
    return out


def is_chair(p):
    return "董事长" in p.replace("副董事长", "")


def is_gm(p):
    q = re.sub(r"(常务|执行)?副总经理|(常务|执行)?副总裁|总经理助理|总裁助理|助理总经理|助理总裁",
               "", p)
    return "总经理" in q or "总裁" in q


def bio_region(ch):
    m = re.search(r"主要工作经历", ch)
    if not m:
        return ""
    s = m.end()
    e = re.search(r"在股东单位任职情况|任职人员姓名|（二）\s*在其他单位|\(二\)\s*在其他单位",
                  ch[s:])
    return ch[s:s + (e.start() if e else 30000)]


def name_re(nm):
    return r"\s*".join(map(re.escape, nm))


PARA = re.compile(r"\n\s*(?:[○●◆■□\d]+[、.．]?\s*)?(?:[^\n]{0,24}?)[一-龥]{2,4}\s*(?:先生|女士)\s*[，,：:（(]"
                  r"|\n\s*[一-龥]{2,4}\s*\n|\n\s*[一-龥]{2,4}\s+[男女]\s*[，,]")


def bios(region, names):
    """Cut the bio region at the start of each person's paragraph.

    A paragraph starts where the name appears at a line start (optionally after a
    number or a position prefix such as ○董事长、总裁) followed by 先生/女士, punctuation
    or a line break. It ends at the next roster name's paragraph or the next line that
    starts another person's paragraph (NAME先生， or NAME alone on a line).
    """
    pos = {}
    for nm in names:
        m = re.search(r"(?:^|\n|。)\s*(?:[○●◆■□\d]+[、.．]?\s*)?(?:[^\n]{0,24}?)" + name_re(nm) +
                      r"\s*(?:先生|女士|男|女|[，,：:（(\n])", region)
        if m:
            pos[nm] = m.start()
    order = sorted(pos.items(), key=lambda x: x[1])
    out = {}
    for k, (nm, p) in enumerate(order):
        e = order[k + 1][1] if k + 1 < len(order) else min(len(region), p + 3000)
        nxt = PARA.search(region, p + len(nm) + 8, e)
        while nxt and nm in clean(nxt.group(0)):
            nxt = PARA.search(region, nxt.end(), e)
        if nxt:
            e = nxt.start()
        b = re.sub(r"\n?[^\n]*\d{4}\s*年年度报告[^\n]*\n(?:\s*\d+\s*(?:/\s*\d+)?\s*\n)?", "\n",
                   region[p:e])
        out[nm] = b.strip(" \n。；;")
    return out


def main(codes=None, outdir=CACHE, prefix=""):
    sel = pd.read_csv(RAW / "annual_report_2014_selected.csv", dtype=str)
    extra = RAW / "annual_report_2014_selected_extra.csv"  # per-firm lookups (05.find_firm)
    if extra.exists():
        sel = pd.concat([sel, pd.read_csv(extra, dtype=str)]).drop_duplicates("code", keep="last")
    info, ros, bio_rows = [], [], []
    for _, r in sel.iterrows():
        code = r["code"]
        if codes and code not in codes:
            continue
        pdf = RAW / "pdf_2014" / f"{code}_{r['announcementId']}.pdf"
        base = {"code": code, "report_title": r["announcementTitle"],
                "announcement_id": r["announcementId"]}
        if not pdf.exists():
            info.append({**base, "parse_note": "pdf missing"})
            continue
        try:
            txt = text_of(code, pdf)
        except Exception as e:  # noqa: BLE001
            info.append({**base, "parse_note": f"pdf unreadable: {type(e).__name__}"})
            continue
        if len(clean(txt)) < 5000:
            info.append({**base, "parse_note": "no text layer (scanned?)"})
            continue
        exp, win, nat, rev = controller(txt)
        ch = mgmt_chapter(txt)
        rs = roster(ch) if ch else []
        notes = []
        if not ch:
            notes.append("mgmt chapter not found")
        if ch and not rs:
            notes.append("roster not parsed")
        info.append({**base, "reg_addr_2014": field_after(txt, r"注册(?:、办公)?地址"),
                     "office_addr_2014": field_after(txt, r"(?:注册、)?办公地址"),
                     "legal_rep_2014": legal_rep(txt),
                     "controller_nature_field": exp, "controller_nature_2014": nat,
                     "controller_needs_review": rev, "controller_snippet": win,
                     "n_roster": len(rs), "parse_note": "; ".join(notes)})
        for x in rs:
            ros.append({"code": code, **x})
        reg = bio_region(ch) if ch else ""
        lr = info[-1]["legal_rep_2014"]
        names = list(dict.fromkeys([x["name"] for x in rs] + ([lr] if lr else [])))
        bmap = bios(reg, names) if reg else {}
        for role, test in [("chairman", is_chair), ("gm", is_gm)]:
            hits = [x for x in rs if test(x["position"])]
            cur = [dict(x, source="roster") for x in hits if x["status"] != "离任"] or \
                [dict(x, source="roster") for x in hits]
            if not cur:
                # fallback: a bio paragraph whose first 60 characters state the role,
                # trying the legal representative first
                for nm in sorted(bmap, key=lambda n: n != lr):
                    head = re.sub(r"副董事长|(常务|执行)?副总经理|(常务|执行)?副总裁|助理总裁|"
                                  r"助理总经理|总经理助理|总裁助理", "", clean(bmap[nm])[:60])
                    if test(head):
                        cur.append({"name": nm, "position": "", "status": "",
                                    "source": "bio_fallback"})
                        break
            if not cur:
                bio_rows.append({"code": code, "role": role, "name": "", "position": "",
                                 "status": "", "bio": "", "bio_found": 0,
                                 "note": "no holder found in roster"})
            for x in cur:
                b = bmap.get(x["name"], "")
                bio_rows.append({"code": code, "role": role, "name": x["name"],
                                 "position": x["position"], "status": x["status"],
                                 "role_source": x["source"],
                                 "bio": b, "bio_found": int(bool(b)),
                                 "note": "" if b else "bio paragraph not located"})
    pd.DataFrame(info).to_csv(outdir / f"{prefix}report_2014_company_info.csv", index=False,
                              encoding="utf-8-sig")
    pd.DataFrame(ros).to_csv(outdir / f"{prefix}mgmt_2014_roster.csv", index=False,
                             encoding="utf-8-sig")
    pd.DataFrame(bio_rows).to_csv(outdir / f"{prefix}mgmt_2014_bios.csv", index=False,
                                  encoding="utf-8-sig")
    print("firms", len(info), "roster rows", len(ros), "bio rows", len(bio_rows))


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
