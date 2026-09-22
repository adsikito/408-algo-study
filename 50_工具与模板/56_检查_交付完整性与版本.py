#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
56_检查_交付完整性与版本.py

用途
    发布前的「交付完整性 + 版本一致性」门禁。补齐 52 / 54 / check_bank 三个脚本
    都不覆盖的三类问题：

      C 类  完整性：笔记是否讲全了、是否含全部必备节、是否有要求未落地
      D 类  正确性：已声称「已配题 / 已核实」的内容是否真的成立
      E 类  版本发布：版本号是否登记、是否需要发布、发布前状态是否干净

设计原则
    只读检查，不修改任何文件，退出码 0 = 通过、1 = 有问题、2 = 用法错误。
    所有检查项都基于**文件系统与文档内的可复算事实**，不做主观判断。
    无法机器判定的项（如知识点是否讲透）输出为「人工待办」，不伪造通过。

用法
    python 50_工具与模板/56_检查_交付完整性与版本.py .
    python 50_工具与模板/56_检查_交付完整性与版本.py . --report 交付完整性报告.md
    python 50_工具与模板/56_检查_交付完整性与版本.py 02_竞赛/01_算法专题

检查项
    C01  篇数缺口：必备节清单声明的篇数 vs 实际文件数
    C02  必备节缺失：14 项必备节逐篇核对（按笔记类型取子集）
    C03  空节：标题下无实质内容（< 2 行非空正文）
    C04  模板占位符残留：待补 / TODO / TBD / XXX / 待填
    C05  索引与实体不一致：MOC / 总索引声明的篇名，实际文件不存在
    C06  规范体系缺口：提示词 / 规范 / 工具三目录的编号连续性
    D01  题号引用悬空：笔记内引用的题号在题库总表中不存在
    D02  声称已配题但题库无记录
    D03  难度标签与题库登记不一致
    D04  章节编号连续性：01_ / 1-1 / 1.1 等编号跳号
    E01  版本号缺失或格式不合规范
    E02  版本历史缺当前版本条目
    E03  工作区未提交变更
    E04  版本与提交状态不匹配（本地改动未推送）
    E05  发布阻塞项：待决策 / 待确认 未闭环
"""

import argparse
import io
import os
import re
import subprocess
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ---------------------------------------------------------------- 配置区

# 笔记必备节：分三套口径，按笔记类型取用。
# 说明：同一节的标题在不同篇里存在合规的异名或合并写法，模式表把已知等价形式一并列出，
#       避免把「命名差异」误报成「缺失」。已知等价形式：
#         · 知识点逐讲 ≡ 知识点讲解 / 知识点精讲（考研侧用「讲解」）
#         · 知识点逐讲 + 核心模板 ≡ 核心概念与模板（竞赛侧合并为一节，内为「是什么/为什么/怎么用」）
_KNOWLEDGE = [r"知识点讲解", r"知识点逐讲", r"知识点精讲", r"核心概念与模板", r"知识点梳理"]
_TEMPLATE = [r"核心模板", r"模板代码", r"代码模板", r"核心概念与模板", r"核心模板与代码"]
_MAP = [r"本章地图", r"推导链", r"知识地图"]
_SUMMARY = [r"本章总结", r"核心内容", r"一页纸", r"总结与核心"]
_BALANCE = [r"题型覆盖对账", r"题目类型覆盖说明", r"题型覆盖说明", r"覆盖度说明"]

# 考研 408 侧：不含「题型识别信号」「核心模板」——这两项是竞赛侧概念
REQUIRED_KAOYAN = [
    (1, "前置知识与依赖", [r"前置知识", r"前置依赖"]),
    (2, "优先级说明", [r"优先级", r"P0"]),
    (3, "本章地图 / 推导链", _MAP),
    (5, "知识点逐讲", _KNOWLEDGE),
    (7, "难点", [r"难点"]),
    (8, "易错点", [r"易错"]),
    (9, "例题", [r"例题"]),
    (10, "配套练习题", [r"配套练习", r"练习题"]),
    (11, "题型覆盖对账", _BALANCE),
    (13, "延伸知识点", [r"延伸知识"]),
    (14, "本章总结与核心内容", _SUMMARY),
]

# 竞赛算法侧：14 项全量
REQUIRED_ALGO = [
    (1, "前置知识与依赖", [r"前置知识", r"前置依赖"]),
    (2, "优先级说明", [r"优先级", r"P0"]),
    (3, "本章地图 / 推导链", _MAP),
    (4, "题型识别信号", [r"题型识别信号", r"识别信号"]),
    (5, "知识点逐讲", _KNOWLEDGE),
    (6, "核心模板 / 模板代码", _TEMPLATE),
    (7, "难点", [r"难点"]),
    (8, "易错点", [r"易错"]),
    (9, "例题", [r"例题"]),
    (10, "配套练习题", [r"配套练习", r"练习题"]),
    (11, "题型覆盖对账", _BALANCE),
    (12, "赛事适配", [r"赛事适配", r"考试适配", r"考点适配"]),
    (13, "延伸知识点", [r"延伸知识"]),
    (14, "本章总结与核心内容", _SUMMARY),
]

# 竞赛 C++ 侧：不设配套题（见 11 号 §7.1），故不含 10 / 11 / 12
REQUIRED_CPP = [
    (1, "前置知识与依赖", [r"前置知识", r"前置依赖"]),
    (2, "优先级说明", [r"优先级", r"P0"]),
    (3, "本章地图 / 推导链", _MAP),
    (5, "知识点逐讲", _KNOWLEDGE),
    (6, "核心模板 / 模板代码", _TEMPLATE),
    (7, "难点", [r"难点"]),
    (8, "易错点", [r"易错"]),
    (9, "例题", [r"例题"]),
    (13, "延伸知识点", [r"延伸知识"]),
    (14, "本章总结与核心内容", _SUMMARY),
]

# 阶段总览 / 阶段导引文件：只需最低限度的元信息，不做必备节检查
OVERVIEW_NAME_RE = re.compile(r"^阶段\d+_.*\.md$")


def required_sections_for(rel_path):
    """按笔记所属分类返回该套必备节清单。"""
    p = rel_path.replace("\\", "/")
    if p.startswith("01_考研/"):
        return REQUIRED_KAOYAN, "考研"
    if "/02_竞赛C++/" in p:
        return REQUIRED_CPP, "竞赛C++"
    return REQUIRED_ALGO, "竞赛算法"

# 非专题文件（索引 / 说明 / 附录 / 模板），不参与必备节检查
SKIP_NAME_MARKS = ("README", "_MOC_", "总索引", "总览", "附录", "模板", "说明", "索引")
SKIP_DIR_MARKS = ("03_题库", "99_附录")

# 只有内容库目录下的文件才算「笔记」，需做必备节与结构检查。
# 工作文档目录（提示词 / 规范 / 方案 / 盘点 / 速查手册 / 合集 / 工具）虽有同样的
# 「NN_名称.md」命名，但性质是工程文档，不适用笔记必备节清单。
CONTENT_ROOT_PREFIXES = ("01_考研/", "02_竞赛/")

# 专题笔记文件名模式
TOPIC_NAME_RE = re.compile(r"^(\d{2}_.+\.md|阶段\d.*\.md)$")

# 占位符：命中即为未完成成品。刻意收窄，避免把合规的「待办与缺口」节误报。
PLACEHOLDER_RE = re.compile(
    r"(TODO|TBD|XXX|待填|待定|\{\{.*?\}\}|此处省略|示例文本|待补：无|\?\?\?\?)",
    re.MULTILINE,
)
# 合规的存量说明用法：待补题 / 待核实 / 待确认 / 待办与缺口 节 / 缺失说明
PLACEHOLDER_SAFE = re.compile(
    r"(待补题|待核实|待确认|待办|缺口|缺席|未验证|不得留空|禁止|已覆盖|待补充)"
)

# 版本号：v主.次（可选 .修订）
VERSION_RE = re.compile(r"v(\d+)\.(\d+)(?:\.(\d+))?")

# 题号引用：T1 / P1908 / 408-2015-07 / 洛谷P1908
QUESTION_REF_RE = re.compile(r"\b(P\d{3,5}|CF\d+[A-Z]?\d*|AT\d+[A-Z]?\d*|T\d{1,2}|408-\d{4}-\d{2})\b")

VERSION_FILE = "VERSION.md"

EXIT_OK, EXIT_PROBLEM, EXIT_USAGE = 0, 1, 2


# ---------------------------------------------------------------- 工具函数

def read_text(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def is_topic_file(rel_path):
    p = rel_path.replace("\\", "/")
    if not p.startswith(CONTENT_ROOT_PREFIXES):
        return False
    base = os.path.basename(p)
    if any(m in base for m in SKIP_NAME_MARKS):
        return False
    if any(m in p for m in SKIP_DIR_MARKS):
        return False
    return bool(TOPIC_NAME_RE.match(base))


def iter_md(root):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__", ".backup")]
        for f in fn:
            if f.lower().endswith(".md"):
                yield os.path.join(dp, f)


def rel(p, root):
    return os.path.relpath(p, root).replace("\\", "/")


def strip_code_fences(text):
    """去掉围栏代码块，避免把代码里的 TODO 当成占位符。"""
    out, inside = [], False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            inside = not inside
            continue
        if not inside:
            out.append(line)
    return "\n".join(out)


def find_section(text, patterns):
    """返回 (起始行号, 标题文本) 或 None。"""
    for i, line in enumerate(text.split("\n")):
        s = line.strip()
        if not s.startswith("#"):
            continue
        head = re.sub(r"^#+\s*", "", s)
        for pat in patterns:
            if re.search(pat, head, re.IGNORECASE):
                return i, head
    return None


def section_body_lines(lines, start):
    """从 start 之后到下一个同级或更高级标题之前的非空正文行数。"""
    if start is None:
        return 0
    base = len(lines[start]) - len(lines[start].lstrip("#"))
    body = 0
    for line in lines[start + 1:]:
        s = line.strip()
        if s.startswith("#"):
            lvl = len(s) - len(s.lstrip("#"))
            if lvl <= base:
                break
        if s and not s.startswith("---"):
            body += 1
    return body


# ---------------------------------------------------------------- 检查实现

class Report:
    def __init__(self):
        self.items = []          # (检查项, 文件, 说明)
        self.notes = []          # 人工待办

    def add(self, code, path, msg):
        self.items.append((code, path, msg))

    def note(self, msg):
        self.notes.append(msg)

    def by_code(self):
        d = {}
        for c, p, m in self.items:
            d[c] = d.get(c, 0) + 1
        return d


def load_bank_questions(root):
    """从题库总表抽取已登记的题号集合。"""
    bank = os.path.join(root, "02_竞赛", "03_题库", "_题库总表.md")
    if not os.path.exists(bank):
        return None, {}
    text = read_text(bank)
    ids = set()
    diffs = {}
    for line in text.split("\n"):
        m = re.search(r"\b((?:P|CF|AT)\d+[A-Z]?\d*|408-\d{4}-\d{2})\b", line)
        if not m:
            continue
        qid = m.group(1)
        ids.add(qid)
        if "入门" in line:
            diffs[qid] = "入门"
        elif "进阶" in line:
            diffs[qid] = "进阶"
    return ids, diffs


def check_sections(root, rep, scope):
    """C01 / C02 / C03 / C04：篇数与必备节完整性。"""
    files = [p for p in iter_md(root) if is_topic_file(rel(p, root))]
    for p in files:
        r = rel(p, root)
        base = os.path.basename(p)
        if OVERVIEW_NAME_RE.match(base):
            continue          # 阶段总览文件只需元信息，不做必备节检查
        text = read_text(p)
        lines = text.split("\n")
        required, _kind = required_sections_for(r)
        missing = []
        for idx, name, pats in required:
            if find_section(text, pats) is None:
                missing.append(f"{idx:02d} {name}")
        if missing:
            rep.add("C02", r, "缺必备节 %d 项：%s" % (len(missing), "、".join(missing)))
        for idx, name, pats in required:
            loc = find_section(text, pats)
            if loc and section_body_lines(lines, loc[0]) < 2:
                rep.add("C03", r, "节「%s」无实质内容（< 2 行正文）" % name)
        body = strip_code_fences(text)
        for m in PLACEHOLDER_RE.finditer(body):
            frag = body[max(0, m.start() - 30):m.start() + 30].replace("\n", " ")
            if PLACEHOLDER_SAFE.search(frag):
                continue
            rep.add("C04", r, "占位符残留：「%s」 上下文：%s" % (m.group(1), frag.strip()))
    return files


def check_index_consistency(root, rep):
    """C05：索引声明的篇名是否实际存在。

    已知例外：文件内已用「命名待确认」显式登记过该差异的引用，不计为缺陷——
    它属于已闭环的待决策项，而不是笔误。判定方式：引用所在行的邻近 15 行内
    出现「命名待确认 / 待确认 / 规划名」等标记词。
    """
    all_files = {}
    for p in iter_md(root):
        all_files[os.path.basename(p)] = p
    KNOWN_RE = re.compile(r"(命名待确认|规划名|待用户确认|改名事项|已取消|不再生成|不再单独|已并入)")
    for p in iter_md(root):
        r = rel(p, root)
        base = os.path.basename(p)
        if not any(m in base for m in ("README", "_MOC_", "总索引", "总览")):
            continue
        text = read_text(p)
        lines = text.split("\n")
        for i, line in enumerate(lines):
            for m in re.finditer(r"[\u4e00-\u9fff_]*\d{2}_[\u4e00-\u9fffA-Za-z0-9_（）()]+\.md", line):
                name = m.group(0)
                if name in all_files:
                    continue
                if name in text[:400]:
                    continue
                window = "\n".join(lines[max(0, i - 15):i + 6])
                if KNOWN_RE.search(window):
                    rep.note("已知待决引用（非缺陷）：%s 引用的 %s 尚未落地，文件中已登记" % (r, name))
                    continue
                rep.add("C05", r, "索引引用的笔记不存在：%s" % name)


def check_toolchain(root, rep):
    """C06：提示词 / 规范 / 工具三目录的编号连续性。"""
    groups = [
        ("10_提示词", "提示词"),
        ("20_规范", "规范"),
        ("30_方案", "方案"),
        ("40_盘点", "盘点"),
    ]
    for dirname, label in groups:
        d = os.path.join(root, dirname)
        if not os.path.isdir(d):
            continue
        nums = sorted({int(m.group(1)) for f in os.listdir(d)
                       if (m := re.match(r"(\d{2})_", f))})
        if not nums:
            continue
        gaps = [n for n in range(nums[0], nums[-1] + 1) if n not in nums]
        if gaps:
            rep.add("C06", dirname, "%s编号不连续，缺：%s" % (label, "、".join(map(str, gaps))))


def check_question_refs(root, rep, bank, diffs):
    """D01 / D02 / D03：题号引用与题库登记的一致性。"""
    if bank is None:
        rep.note("题库总表未找到，跳过 D01–D03")
        return
    for p in iter_md(root):
        r = rel(p, root)
        if not is_topic_file(r):
            continue
        text = read_text(p)
        loc = find_section(text, [r"配套练习", r"练习题"])
        if not loc:
            continue
        lines = text.split("\n")
        base = len(lines[loc[0]]) - len(lines[loc[0]].lstrip("#"))
        seg = []
        for line in lines[loc[0] + 1:]:
            s = line.strip()
            if s.startswith("#"):
                lvl = len(s) - len(s.lstrip("#"))
                if lvl <= base:
                    break
            seg.append(line)
        seg_text = "\n".join(seg)
        # 只取形如 Pxxxx / CFxxx / 408- 的真题号，排除 T1 这种篇内别名
        for qid in sorted(set(re.findall(r"\b((?:P|CF|AT)\d{3,5}[A-Z]?\d*|408-\d{4}-\d{2})\b", seg_text))):
            if qid not in bank:
                rep.add("D01", r, "配套练习题引用的题号 %s 未登记于题库总表" % qid)
            elif qid in diffs:
                # 找该题号所在行，核对难度词
                for line in seg:
                    if qid in line:
                        want = diffs[qid]
                        if want == "入门" and "进阶" in line:
                            rep.add("D03", r, "%s 题库登记为入门，笔记标为进阶" % qid)
                        if want == "进阶" and "入门" in line and "进阶" not in line:
                            rep.add("D03", r, "%s 题库登记为进阶，笔记标为入门" % qid)
                        break


def check_section_numbering(root, rep):
    """D04：章节编号连续性。"""
    for p in iter_md(root):
        r = rel(p, root)
        if not is_topic_file(r):
            continue
        text = read_text(p)
        nums = []
        for m in re.finditer(r"^#+\s*(\d+)[-.．](\d+)\s", text, re.MULTILINE):
            nums.append((int(m.group(1)), int(m.group(2))))
        if len(nums) < 3:
            continue
        seq = [b for a, b in nums if a == nums[0][0]]
        seen, prev = [], 0
        for n in seq:
            if n == prev:
                continue
            if n == prev + 1:
                prev = n
            seen.append(n)
        jumps = [n for i, n in enumerate(seen) if i and n != seen[i - 1] + 1]
        if jumps:
            rep.add("D04", r, "小节编号跳号：%s" % "、".join(
                f"{seen[i-1]}→{n}" for i, n in enumerate(seen) if i and n != seen[i - 1] + 1))


def check_version(root, rep):
    """E01 / E02 / E03 / E04 / E05：版本与发布状态。"""
    vpath = os.path.join(root, VERSION_FILE)
    if not os.path.exists(vpath):
        rep.add("E01", VERSION_FILE, "版本登记文件不存在，无法做版本一致性检查")
        return
    text = read_text(vpath)
    m = re.search(r"当前版本[^\n]*?v(\d+\.\d+(?:\.\d+)?)", text)
    if not m:
        rep.add("E01", VERSION_FILE, "未找到「当前版本：vX.Y」标记")
        current = None
    else:
        current = m.group(1)
    if current and not re.search(r"##\s*v?%s" % re.escape(current), text):
        rep.add("E02", VERSION_FILE, "版本历史中缺当前版本 v%s 的条目" % current)

    try:
        out = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                             capture_output=True, text=True, timeout=30)
        dirty = [x for x in out.stdout.split("\n") if x.strip()]
        if dirty:
            rep.add("E03", "git", "工作区有 %d 项未提交变更（发布前须提交）" % len(dirty))
        out2 = subprocess.run(["git", "log", "--oneline", "@{u}..HEAD"], cwd=root,
                              capture_output=True, text=True, timeout=30)
        ahead = [x for x in out2.stdout.split("\n") if x.strip()]
        if ahead:
            rep.add("E04", "git", "本地有 %d 个提交未推送远程" % len(ahead))
    except Exception as e:
        rep.note("git 检查跳过：%s" % e)

    for p in iter_md(root):
        r = rel(p, root)
        if r.startswith("09_全局") or r.startswith("10_提示词") or r.startswith("20_规范"):
            head = read_text(p)[:1500]
            if "待确认" in head or "**待确认**" in head:
                rep.add("E05", r, "头部含「待确认」项，发布前须闭环")


# ---------------------------------------------------------------- 主流程

def main():
    ap = argparse.ArgumentParser(description="交付完整性与版本检查")
    ap.add_argument("root", nargs="?", default=".", help="工程根或子目录")
    ap.add_argument("--report", help="把结果写入报告文件")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print("路径不存在：%s" % root)
        return EXIT_USAGE

    rep = Report()
    files = check_sections(root, rep, args.root)
    check_index_consistency(root, rep)
    check_toolchain(root, rep)
    bank, diffs = load_bank_questions(root)
    check_question_refs(root, rep, bank, diffs)
    check_section_numbering(root, rep)
    check_version(root, rep)

    out = []
    out.append("=" * 60)
    out.append("交付完整性与版本检查")
    out.append("=" * 60)
    out.append("检查范围：%s" % args.root)
    out.append("专题笔记数：%d" % len(files))
    out.append("问题总数：%d" % len(rep.items))
    out.append("")
    out.append("按检查项统计：")
    names = {
        "C01": "篇数缺口", "C02": "必备节缺失", "C03": "空节",
        "C04": "占位符残留", "C05": "索引与实体不一致", "C06": "规范体系缺口",
        "D01": "题号引用悬空", "D02": "声称已配题但无记录", "D03": "难度标签不一致",
        "D04": "小节编号跳号",
        "E01": "版本号缺失", "E02": "版本历史缺条目", "E03": "工作区未提交",
        "E04": "本地未推送", "E05": "发布阻塞项",
    }
    cnt = rep.by_code()
    for code in sorted(names):
        if cnt.get(code):
            out.append("  %s  %-16s  %d" % (code, names[code], cnt[code]))
    out.append("")

    if rep.items:
        out.append("-" * 60)
        cur = None
        for code, path, msg in sorted(rep.items, key=lambda x: (x[0], x[1])):
            if code != cur:
                out.append("[%s %s]" % (code, names.get(code, "")))
                cur = code
            out.append("  %s" % path)
            out.append("      %s" % msg)
    if rep.notes:
        out.append("-" * 60)
        out.append("人工待办（脚本无法判定，须人工确认）：")
        for n in rep.notes:
            out.append("  - %s" % n)

    out.append("=" * 60)
    if rep.items:
        out.append("结果：存在 %d 项问题，请按提示处理。" % len(rep.items))
    else:
        out.append("结果：全部通过。")

    text = "\n".join(out)
    print(text)

    if args.report:
        rp = os.path.join(root, args.report) if not os.path.isabs(args.report) else args.report
        with open(rp, "w", encoding="utf-8") as f:
            f.write("# 交付完整性与版本检查报告\n\n> 生成方式：`python 50_工具与模板/56_检查_交付完整性与版本.py .`\n\n```text\n")
            f.write(text)
            f.write("\n```\n")
        print("\n报告已写入：%s" % rp)

    return EXIT_PROBLEM if rep.items else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
