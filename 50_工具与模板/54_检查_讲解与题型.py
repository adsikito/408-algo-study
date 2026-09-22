#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""讲解与题型覆盖检查

依据：20_规范/24_知识点讲解与题型覆盖规范.md

检查项（编号与规范章节对齐）：
  R01  单篇总行数超上限（规范 §一）
  R02  单个「知识点逐讲」小节超上限（规范 §一）
  R03  「核心内容（一页纸）」条数超上限或不足下限（规范 §三 3.3）
  R04  缺「题型覆盖对账表」节（规范 §四 4.1）
  R05  对账表行数 != 题型识别信号表行数（规范 §四 4.3 硬规则一）
  R06  对账表出现「延伸至」，但指向的篇目在工程内不存在（规范 §四 4.3 硬规则二）
  R07  P0 题型未配题（规范 §四 4.3 硬规则三）
  R08  缺少入门或进阶难度档（规范 §五 5.3，除非在豁免清单内）
  R09  题量低于阶段下限或高于上限（规范 §五 5.4）
  R10  全篇出现「显然 / 易得 / 略」类跳过推导表述（规范 §二 2.4）
  R11  全篇依赖关系图出现两个及以上（规范 §三 3.2）
  R12  同一引用块内标签叠加（规范 §二 2.4）

用法：
  python 54_检查_讲解与题型.py .                 # 全库检查
  python 54_检查_讲解与题型.py 02_竞赛/01_算法专题 --report
  python 54_检查_讲解与题型.py . --skip-existing # 只检查新增笔记（按 24 号规范第七节）
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------- 规范参数（唯一来源：24_知识点讲解与题型覆盖规范.md） ----------------

MAX_TOTAL_LINES = 450          # §一
MIN_TOTAL_LINES = 200          # §一
MAX_KNOWLEDGE_LINES = 80       # §一
MIN_KNOWLEDGE_LINES = 15       # §一
MAX_SUMMARY_ITEMS = 10         # §三 3.3
MIN_SUMMARY_ITEMS = 5          # §一
MAX_TAGS_PER_BLOCK = 1         # §二 2.4

# 题量下限：前缀路径 -> 下限（§五 5.4）
QUOTA_MIN_BY_PREFIX = (
    ("02_竞赛/01_算法专题/阶段1_基础技巧/", 4),
    ("02_竞赛/01_算法专题/阶段2_算法思想/", 4),
    ("02_竞赛/01_算法专题/阶段3_基础数据结构/", 4),
    ("02_竞赛/01_算法专题/", 3),
    ("01_考研/408数据结构/", 3),
)
QUOTA_MAX = 6

# 跳过整篇检查的标记（与 22 号规范的机制一致）
IGNORE_FILE_MARK = "<!-- compat-ignore-file -->"

# 豁免清单（§五 5.3 情形二）
EXEMPT_FILE = ROOT / "20_规范" / "25_难度梯度豁免清单.md"

SKIP_PREFIXES = (
    "03_常规课程/",
    "09_全局/",
    "10_提示词/",
    "20_规范/",
    "30_方案/",
    "40_盘点/",
    "50_工具与模板/",
    "70_速查手册/",
    "80_合集/",
    "02_竞赛/03_题库/",       # 题库总表：数据表，非讲解性笔记
    "02_竞赛/99_附录/",       # 附录：汇总性文档，无「知识点逐讲」结构
)

# 文件名含下列词者视为索引 / 总览 / 模板 / 卷首说明，不适用讲解与题型的结构要求
SKIP_NAME_MARKS = ("README", "_MOC_", "总索引", "总览", "附录")

# 只有「专题笔记」才检查下列节（用文件名前缀 NN_ 或阶段名判定）
TOPIC_NAME_RE = re.compile(r"^(\d{2}_.+\.md|阶段\d.*\.md)$")

TAG_RE = re.compile(r"\*\*【([^】]+)】\*\*")
SKIP_WORDS = ("显然", "易得", "略")
# 「略」单独成词才算，避免「策略 / 忽略 / 省略」误判
SKIP_WORD_SAFE = re.compile(r"(?<![策省忽简概])略(?![图述])")


class Doc:
    """一篇笔记的解析结果。"""

    def __init__(self, path: Path, rel: str, text: str):
        self.path = path
        self.rel = rel
        self.lines = text.splitlines()
        self.text = text

    # ---- 通用工具 ----

    def heading_positions(self, level: int):
        """返回 (行号, 标题文本) 列表，标题层级严格等于 level。"""
        pat = re.compile(r"^" + "#" * level + r"\s+(.*)$")
        out = []
        for i, ln in enumerate(self.lines):
            m = pat.match(ln)
            if m:
                out.append((i, m.group(1).strip()))
        return out

    def section_slice(self, title_kw, level=2):
        """取某个二级节的行区间 [start, end)。找不到返回 None。"""
        heads = self.heading_positions(level)
        for idx, (ln, title) in enumerate(heads):
            if title_kw in title:
                start = ln
                end = heads[idx + 1][0] if idx + 1 < len(heads) else len(self.lines)
                return start, end
        return None

    def has_section(self, title_kw, level=2):
        return self.section_slice(title_kw, level) is not None

    def count_table_rows(self, seg_start, seg_end):
        """统计区间内的 Markdown 表格数据行（排除表头与分隔行）。"""
        n = 0
        for ln in self.lines[seg_start:seg_end]:
            s = ln.strip()
            if not s.startswith("|"):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not cells or not cells[0]:
                continue
            if set("".join(cells)) <= set("-: "):   # 分隔行
                continue
            n += 1
        # 减去表头行（每张表 1 行）
        return max(0, n - self._table_count(seg_start, seg_end))

    def _table_count(self, seg_start, seg_end):
        """统计区间内的表格张数（以「表头 + 分隔行」判定）。"""
        cnt = 0
        for i in range(seg_start, seg_end - 1):
            a = self.lines[i].strip()
            b = self.lines[i + 1].strip()
            if not a.startswith("|") or not b.startswith("|"):
                continue
            cells = [c.strip() for c in b.strip("|").split("|")]
            if cells and set("".join(cells)) <= set("-: "):
                cnt += 1
        return cnt

    def table_rows_in_section(self, title_kw, level=2):
        seg = self.section_slice(title_kw, level)
        if not seg:
            return None
        return self.count_table_rows(*seg)


def load_exemptions():
    """从豁免清单读取被豁免的文件（形如 02_竞赛/.../xx.md）。"""
    if not EXEMPT_FILE.exists():
        return set()
    out = set()
    for ln in EXEMPT_FILE.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if s.startswith("|") and ".md" in s:
            cells = [c.strip().strip("`") for c in s.strip("|").split("|")]
            for c in cells:
                if c.endswith(".md"):
                    out.add(c)
    return out


def collect(target: Path):
    if target.is_file():
        cands = [target]
    else:
        cands = sorted(target.rglob("*.md"))

    out = []
    for p in cands:
        if not p.is_file():
            continue
        try:
            rel = p.relative_to(ROOT).as_posix()
        except ValueError:
            rel = p.as_posix()
        # 跳过工程文档目录
        if any(rel.startswith(pre) for pre in SKIP_PREFIXES):
            continue
        if p.name in ("学习笔记.md",):     # 素材副本，不是内容笔记
            continue
        if any(m in p.name for m in SKIP_NAME_MARKS):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if IGNORE_FILE_MARK in text[:400]:
            continue
        out.append(Doc(p, rel, text))
    return out


def quota_min(rel: str, default: int = 3) -> int:
    for pre, n in QUOTA_MIN_BY_PREFIX:
        if rel.startswith(pre):
            return n
    return default


def check_doc(doc: Doc, exempt: set):
    issues = []
    # 只有「专题笔记」才做讲解结构与题型覆盖检查；
    # 考研与竞赛 C++ 的模块笔记另有体例（见各自 README），但仍做篇幅与禁用词检查。
    is_topic = bool(TOPIC_NAME_RE.match(doc.path.name))
    if doc.rel.startswith("02_竞赛/02_竞赛C++/"):
        is_topic = False

    def add(code, msg):
        issues.append((code, msg))

    # R01 总行数
    total = len(doc.lines)
    if total > MAX_TOTAL_LINES:
        add("R01", f"总行数 {total} > 上限 {MAX_TOTAL_LINES}（规范 §一）")

    # R10 跳过推导表述（先做，避免被后续 return 吞掉）
    for i, ln in enumerate(doc.lines, 1):
        for w in SKIP_WORDS:
            if w == "略":
                if SKIP_WORD_SAFE.search(ln):
                    add("R10", f"第 {i} 行含跳过推导表述「略」：{ln.strip()[:60]}")
            elif w in ln:
                add("R10", f"第 {i} 行含跳过推导表述「{w}」：{ln.strip()[:60]}")

    # R12 标签叠加
    for i, ln in enumerate(doc.lines, 1):
        tags = TAG_RE.findall(ln)
        # 允许 【入门】/【进阶】 与内容类型标签共现（难度 + 类型是两个维度）
        core = [t for t in tags if t not in ("入门", "进阶", "补充")]
        if len(core) > MAX_TAGS_PER_BLOCK:
            add("R12", f"第 {i} 行标签叠加 {len(core)} 个：{ln.strip()[:60]}")

    # R11 依赖图数量
    tree_blocks = 0
    in_fence = False
    for ln in doc.lines:
        s = ln.strip()
        if s.startswith("```"):
            if not in_fence:
                in_fence = True
                lang = s[3:].strip().lower()
                buff = []
                tree_blocks = tree_blocks  # noqa
                cur_lang = lang
                cur_buf = buff
            else:
                in_fence = False
        elif in_fence and cur_lang == "text":
            cur_buf.append(s)
    # 用更稳的方式重新统计 text 代码块中的树状图
    blocks = re.findall(r"```text\n(.*?)```", doc.text, re.S)
    tree_like = [b for b in blocks if b.count("├") + b.count("└") + b.count("│") >= 2]
    if len(tree_like) > 1:
        add("R11", f"出现 {len(tree_like)} 个树状依赖图（规范 §三 3.2 只允许 1 个）")

    # R02 知识点小节行数（仅专题笔记）
    kh = doc.heading_positions(3)
    for idx, (ln, title) in enumerate(kh):
        if not is_topic:
            break
        if not re.match(r"^\d+-\d+|^[A-F]-\d+", title) and "知识点" not in title:
            continue
        end = kh[idx + 1][0] if idx + 1 < len(kh) else len(doc.lines)
        seg = end - ln
        # 只对「知识点逐讲」节内的三级标题计数：其后紧跟二级「典型例题」前的都算
        if seg > MAX_KNOWLEDGE_LINES:
            add("R02", f"知识点小节「{title[:30]}」{seg} 行 > 上限 {MAX_KNOWLEDGE_LINES}")

    # R03 核心内容条数
    seg = doc.section_slice("核心内容", 2) or doc.section_slice("核心内容", 3)
    if seg:
        items = sum(1 for ln in doc.lines[seg[0]:seg[1]] if re.match(r"^\s*\d+\.\s+\S", ln))
        if items > MAX_SUMMARY_ITEMS:
            add("R03", f"核心内容 {items} 条 > 上限 {MAX_SUMMARY_ITEMS}")
        elif items and items < MIN_SUMMARY_ITEMS:
            add("R03", f"核心内容仅 {items} 条 < 下限 {MIN_SUMMARY_ITEMS}")

    # ---- 题目相关（仅对含「配套练习题」的笔记） ----
    q_seg = doc.section_slice("配套练习题", 2)
    if q_seg and is_topic:
        q_rows = doc.count_table_rows(*q_seg)
        # R09 题量
        lo = quota_min(doc.rel)
        if q_rows > QUOTA_MAX:
            add("R09", f"题量 {q_rows} > 上限 {QUOTA_MAX}")
        elif 0 < q_rows < lo:
            add("R09", f"题量 {q_rows} < 该阶段下限 {lo}（规范 §五 5.4）")

        # R08 难度档
        seg_text = "\n".join(doc.lines[q_seg[0]:q_seg[1]])
        has_in = "【入门】" in seg_text
        has_adv = "【进阶】" in seg_text
        if q_rows and not (has_in and has_adv):
            if doc.path.name not in exempt and doc.rel not in exempt:
                miss = []
                if not has_in:
                    miss.append("入门")
                if not has_adv:
                    miss.append("进阶")
                add("R08", f"缺 {'/'.join(miss)} 难度档，且未登记豁免（规范 §五 5.3）")

        # R04 对账表存在性
        if not doc.has_section("题型覆盖对账", 3) and "题型覆盖对账" not in doc.text:
            add("R04", "缺「题型覆盖对账表」节（规范 §四）")

        # R05 行数对齐
        sig_rows = doc.table_rows_in_section("题型识别信号", 2)
        rec_rows = doc.table_rows_in_section("题型覆盖对账", 3)
        if sig_rows is None and rec_rows is None:
            pass
        elif sig_rows is None:
            add("R05", "有对账表但缺「题型识别信号」表")
        elif rec_rows is None:
            add("R05", "「题型覆盖对账表」无法解析（检查其是否含表格）")
        elif sig_rows != rec_rows:
            add("R05", f"题型识别信号 {sig_rows} 行 vs 对账表 {rec_rows} 行，不相等（硬规则一）")

        # R06 延伸指向存在性 + R07 P0 未配题
        if rec_rows is not None:
            seg2 = doc.section_slice("题型覆盖对账", 3)
            for ln in doc.lines[seg2[0]:seg2[1]]:
                s = ln.strip()
                if not s.startswith("|"):
                    continue
                cells = [c.strip() for c in s.strip("|").split("|")]
                if len(cells) < 4:
                    continue
                prio, target, status = cells[1], cells[2], cells[3]
                if "延伸至" in status or "延伸至" in target:
                    ref = re.findall(r"阶段(\d)", status + target)
                    if ref:
                        for st in ref:
                            if not list((ROOT / "02_竞赛/01_算法专题").glob(f"阶段{st}_*")):
                                add("R06", f"延伸指向「阶段{st}」，该阶段目录不存在")
                if "P0" in prio and ("不配题" in status or (not target.strip() and "已配题" not in status)):
                    add("R07", f"P0 题型未配题：{cells[0][:30]}（硬规则三）")
    return issues


def main():
    ap = argparse.ArgumentParser(description="讲解与题型覆盖检查（依据 24 号规范）")
    ap.add_argument("target", help="待检查的文件或目录")
    ap.add_argument("--report", action="store_true", help="输出统计报告")
    args = ap.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = (Path.cwd() / target).resolve()
    if not target.exists():
        print(f"路径不存在：{target}")
        return 2

    docs = collect(target)
    if not docs:
        print("未找到待检查的内容笔记")
        return 2

    exempt = load_exemptions()
    total = 0
    bad = 0
    by_code = {}
    detail = []

    for doc in docs:
        issues = check_doc(doc, exempt)
        if issues:
            bad += 1
            total += len(issues)
            detail.append((doc.rel, issues))
            for code, _ in issues:
                by_code[code] = by_code.get(code, 0) + 1

    print(f"扫描笔记数：{len(docs)}")
    print(f"存在问题笔记：{bad}")
    print(f"问题总数：{total}")
    if by_code:
        print("按检查项统计：")
        for code in sorted(by_code):
            print(f"  {code}: {by_code[code]}")

    if args.report or total:
        print("-" * 60)
        for rel, issues in detail:
            print(f"[{rel}]")
            for code, msg in issues:
                print(f"  {code} {msg}")

    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
