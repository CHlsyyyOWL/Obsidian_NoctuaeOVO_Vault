"""Step 8. Rule-based political connection coding of 2014 chairman and GM bios.

Input  raw/cache/mgmt_2014_bios.csv (or a sample file passed as argument)
Output raw/cache/political_connection_2014.csv (one row per firm x role x person)
       raw/cache/political_connection_2014_firm.csv (firm level)
       raw/cache/political_connection_2014_matches.csv (every keyword hit with sentence)

A bio is split into sentences at 。；; (PDF line wraps are joined first). Every rule hit keeps the matched
keyword and the clause. Current and former positions are both counted.

deputy    人大代表 / 人大常委 / 政协委员 / 政协常委 and equivalent long forms.
official  government or Party organ positions and ranks (县长, 市长, 局长 of a government
          bureau, 人民政府, 县委/市委 posts, 公务员, 处级/科级 ranks, development zone
          管委会, courts, procuratorates, ministries and commissions).
military  部队, 解放军, 军区, 武警, 服役, 入伍, 转业 etc.
needs_review=1 when a hit is ambiguous: an official keyword in a sentence about awards,
          honours or advisory roles (津贴, 奖, 评为, 聘为, 顾问, 专家 ...), 处长/科长/局长/主任/党委书记 inside a company
          context, 政府 without a post, 委员会 or 主任 without a clear government body,
          or a deputy/official keyword whose level or tense cannot be read.
other_body  工商联, 青联, 妇联, 民主党派, 共青团, industry associations: recorded only,
          not counted as connected.
family    tier 1 only: a relative term (其父, 父亲, 之子, 岳父, 配偶 ...) within the same
          clause as a deputy/official/military keyword. Coverage is incomplete by design.
"""
import re
import sys
from pathlib import Path

import pandas as pd

from common import CACHE

DEPUTY = r"(?:人大代表|人民代表大会代表|人大常委|人民代表大会常务委员会|人大常务委员会|政协委员|政协常委|" \
         r"政治协商会议[^。；;]{0,20}委员|政协[^。；;]{0,12}(?:委员|常委|副主席|主席))"
OFFICIAL_STRONG = r"(?:县长|市长|区长|乡长|镇长|省长|州长|旗长|厅长|副厅|人民政府|县委|市委|区委|省委|地委|州委|" \
                  r"镇党委|乡党委|镇委|乡委|纪委|纪律检查委员会|组织部|宣传部|统战部|发改委|发展和改革委员会|" \
                  r"发展计划委员会|计划委员会|经贸委|经济委员会|经委|计委|国资委|国有资产监督管理委员会|财政局|财政厅|" \
                  r"财政部|税务局|工商局|工商行政管理局|海关|人民法院|人民检察院|公安局|公安厅|管委会|管理委员会|" \
                  r"公务员|处级|科级|厅级|局级|正处|副处|正科|副科|国务院|部委|商务部|商务厅|商务局|外经贸|" \
                  r"经济贸易委员会|科学技术委员会|科委|建设厅|建设局|建委|交通厅|交通局|国土资源|劳动局|人事局|" \
                  r"教育局|卫生局|统计局|物价局|审计局|环保局|街道办事处|乡政府|镇政府|县政府|市政府|区政府|省政府|" \
                  r"挂职)"
MILITARY = r"(?:部队|解放军|军区|军分区|武警|服役|入伍|参军|转业|退役军人|军校|海军|空军|陆军|军人)"
AMBIG = r"(?:处长|科长|局长|主任|党委书记|党委副书记|党组书记|党组副书记|政府|委员会|干部)"
OTHER_BODY = r"(?:工商联|工商业联合会|青联|青年联合会|妇联|妇女联合会|民建|民盟|民进|农工党|致公党|九三学社|" \
             r"台盟|民革|共青团|团委|协会|商会)"
RELATIVE = r"(?:其父|父亲|之父|家父|其母|母亲|之子|其子|儿子|之女|其女|女儿|岳父|岳母|公公|配偶|丈夫|妻子|夫人|" \
           r"兄长|哥哥|弟弟|姐姐|妹妹|胞兄|胞弟|叔叔|伯父|舅舅|女婿|儿媳|侄子|外甥|亲属|父子|父女|母子|夫妻|兄弟)"
COMPANY = r"(?:公司|集团|有限|股份|厂|银行|企业|事务所|研究所|研究院|大学|学院|医院|学校)"
LEVEL = [("national", r"全国|中央|国务院|国家"), ("provincial", r"省|自治区|北京市|上海市|天津市|重庆市"),
         ("prefecture", r"市|地区|州|盟"), ("county", r"县|区|旗|镇|乡")]


HONOR = r"(?:津贴|奖|荣获|评为|评选|授予|称号|聘为|聘任|聘请|顾问|专家|咨询|特邀|代表团|候选人)"


def clauses(bio):
    """Sentences split at 。；; after joining PDF line wraps."""
    t = re.sub(r"\s+", "", bio or "")
    return [c for c in re.split(r"[。；;]", t) if c]


def level_of(clause, start):
    pre = clause[max(0, start - 12):start]
    for lv, pat in LEVEL:
        if re.search(pat, pre):
            return lv
    return ""


def code_bio(bio):
    hits = []
    for c in clauses(bio):
        cc = re.sub(r"\s+", "", c)
        fam = re.search(RELATIVE, cc)
        for m in re.finditer(DEPUTY, cc):
            hits.append(("deputy", m.group(0), level_of(cc, m.start()), 0, cc, bool(fam)))
        for m in re.finditer(OFFICIAL_STRONG, cc):
            kw = m.group(0)
            # government titles that also exist inside firms are reviewed when the
            # clause names a company and no government organ
            rev = 0
            if kw in ("处级", "科级", "正处", "副处", "正科", "副科") and re.search(COMPANY, cc) \
                    and not re.search(r"政府|县委|市委|区委|省委|厅|局|委员会|管委会", cc):
                rev = 1
            if kw in ("管理委员会",) and re.search(COMPANY, cc) and "管委会" not in cc \
                    and not re.search(r"开发区|园区|新区|高新区|试验区", cc):
                rev = 1  # e.g. company management committee
            if kw == "挂职":
                rev = 1
            if re.search(HONOR, cc):
                rev = 1  # awards, honours and advisory appointments are not posts
            hits.append(("official", kw, level_of(cc, m.start()), rev, cc, bool(fam)))
        for m in re.finditer(MILITARY, cc):
            hits.append(("military", m.group(0), "", 0, cc, bool(fam)))
        if not any(h[4] == cc and h[0] in ("official", "military") for h in hits):
            for m in re.finditer(AMBIG, cc):
                kw = m.group(0)
                if kw == "委员会" and (re.search(r"(薪酬|审计|提名|战略|考核|专门|投资|风险|技术|学术|专业|"
                                                 r"标准化|编辑|管理)委员会", cc)
                                       or re.search(r"顾问|咨询|专家|学会|协会|基金|联合会", cc)):
                    continue
                if kw == "主任" and re.search(r"办公室主任|中心主任|车间主任|部主任|室主任|研究所|研究院|"
                                              r"教研|科室|实验室|医院|委员会主任委员", cc) and \
                        not re.search(r"政府|县委|市委|区委|省委|厅|管委会", cc):
                    continue
                if kw in ("党委书记", "党委副书记") and re.search(r"(本)?公司党委|集团党委|"
                                                               r"股份有限公司党委", cc):
                    continue  # Party secretary of the firm itself is not a government post
                hits.append(("ambiguous", kw, level_of(cc, m.start()), 1, cc, bool(fam)))
        for m in re.finditer(OTHER_BODY, cc):
            hits.append(("other_body", m.group(0), "", 0, cc, bool(fam)))
    return hits


def main(src, prefix=""):
    src = Path(src)
    outdir = src.parent
    b = pd.read_csv(src, dtype=str).fillna("")
    rows, matches = [], []
    for _, r in b.iterrows():
        h = code_bio(r["bio"]) if r["bio"] else []
        for cat, kw, lv, rev, cl, fam in h:
            matches.append({"code": r["code"], "role": r["role"], "name": r["name"],
                            "category": cat, "keyword": kw, "level_guess": lv,
                            "needs_review": rev, "relative_term_in_clause": int(fam),
                            "sentence": cl})

        def first(cat, strict=True):
            for x in h:
                if x[0] == cat and not x[5] and (not strict or x[3] == 0):
                    return x
            return None

        dep, off, mil = first("deputy"), first("official"), first("military")
        fam = [x for x in h if x[5] and x[0] in ("deputy", "official", "military")]
        review = [x for x in h if x[3] == 1 and not x[5]]
        lv_order = ["national", "provincial", "prefecture", "county"]
        lvls = [x[2] for x in h if x[0] in ("deputy", "official") and x[2] and not x[5]]
        rows.append({
            "code": r["code"], "role": r["role"], "name": r["name"],
            "bio_found": r.get("bio_found", ""),
            "deputy": int(bool(dep)), "deputy_keyword": dep[1] if dep else "",
            "deputy_sentence": dep[4] if dep else "",
            "official": int(bool(off)), "official_keyword": off[1] if off else "",
            "official_sentence": off[4] if off else "",
            "military": int(bool(mil)), "military_keyword": mil[1] if mil else "",
            "military_sentence": mil[4] if mil else "",
            "highest_level_guess": min(lvls, key=lv_order.index) if lvls else "",
            "connected": int(bool(dep or off or mil)) if r["bio"] else "",
            "needs_review": int(bool(review)),
            "review_keywords": " | ".join(f"{x[1]}: {x[4]}" for x in review),
            "family_connected": int(bool(fam)) if r["bio"] else "",
            "family_sentence": " | ".join(x[4] for x in fam),
            "other_body_keywords": "、".join(dict.fromkeys(x[1] for x in h if x[0] == "other_body")),
        })
    out = pd.DataFrame(rows)
    out.to_csv(outdir / f"{prefix}political_connection_2014.csv", index=False,
               encoding="utf-8-sig")
    pd.DataFrame(matches).to_csv(outdir / f"{prefix}political_connection_2014_matches.csv",
                                 index=False, encoding="utf-8-sig")
    num = ["deputy", "official", "military", "needs_review"]
    o = out.copy()
    for c in num + ["connected", "family_connected"]:
        o[c] = pd.to_numeric(o[c], errors="coerce")
    firm = o.groupby("code").agg(
        chairman=("name", lambda s: "、".join(o.loc[s.index][o.loc[s.index, "role"] == "chairman"]["name"])),
        gm=("name", lambda s: "、".join(o.loc[s.index][o.loc[s.index, "role"] == "gm"]["name"])),
        bio_found_any=("bio_found", lambda s: int((s == "1").any())),
        deputy=("deputy", "max"), official=("official", "max"), military=("military", "max"),
        connected=("connected", "max"), needs_review=("needs_review", "max"),
        family_connected=("family_connected", "max")).reset_index()
    firm["connected_or_review"] = ((firm["connected"] == 1) | (firm["needs_review"] == 1)).astype(int)
    firm.to_csv(outdir / f"{prefix}political_connection_2014_firm.csv", index=False,
                encoding="utf-8-sig")
    print("persons", len(out), "firms", len(firm), "connected", int(firm["connected"].sum()),
          "deputy", int(firm["deputy"].sum()), "official", int(firm["official"].sum()),
          "military", int(firm["military"].sum()), "needs_review", int(firm["needs_review"].sum()),
          "family", int(firm["family_connected"].sum()))
    return out, firm


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else CACHE / "mgmt_2014_bios.csv"
    pre = sys.argv[2] if len(sys.argv) > 2 else ""
    main(src, pre)
