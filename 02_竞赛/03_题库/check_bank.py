#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_bank.py —— 题库、知识点与笔记的三方一致性校验

为什么需要这个脚本
    题库总表、知识点索引、代码文件三者分离，好处是各司其职、便于检索；
    代价是长期维护后可能互相失配（题目引用了不存在的知识点、
    状态标为已通过却没有代码文件等）。本脚本补上这个代价。

用法
    python check_bank.py <题库目录>
    python check_bank.py <题库目录> --report     额外输出统计报告

检查项
    E101  链接格式不符合平台规范
    E102  题目引用的知识点编号在知识点索引中不存在
    E103  状态为「已通过」但代码目录下没有对应文件
    E104  知识点索引中无任何题目覆盖的 P0 知识点
    E105  总表缺少必需列或列数不符
    E106  代码文件命名与题号不一致（存在多余或缺失）

退出码
    0  全部通过
    1  发现问题
"""

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 平台链接前缀规范
# ---------------------------------------------------------------------------

PLATFORM_PREFIX = {
    "luogu": "https://www.luogu.com.cn/problem/",
    "leetcode": "https://leetcode.cn/problems/",
    "cf": "https://codeforces.com/",
    "lanqiao": "https://www.lanqiao.cn/problems/",
    "baidu": "https://astar.baidu.com/",
    "ccf": "https://www.cspro.org/",
}

# 408 真题无公开网址，链接列写固定文本
ZHENTI_MARK = "真题无公开网址"

BANK_TABLE = "_题库总表.md"
KP_TABLE = "_知识点索引.md"
CODE_DIR = "代码"

HEADER_PLATFORM = ("题号", "题名", "链接", "知识点", "状态", "代码")

SEVERITY = {
    "E101": "高",
    "E102": "高",
    "E103": "高",
    "E104": "中",
    "E105": "中",
    "E106": "中",
}

FIX_HINT = {
    "E101": "按平台规范修正链接。洛谷 https://www.luogu.com.cn/problem/P####；力扣 https://leetcode.cn/problems/<slug>/",
    "E102": "在 _知识点索引.md 中补录该知识点，或修正总表中的编号",
    "E103": "在 代码/ 下创建对应 .cpp 文件，或把状态改回「已做」",
    "E104": "为该 P0 知识点补题，或说明免做理由",
    "E105": "总表表格应为 6 列：题号 | 题名 | 链接 | 知识点 | 状态 | 代码",
    "E106": "删除无对应题目的代码文件，或补登题目行",
}

STATUS_DONE = "已通过"
STATUS_ALL = {"未做", "已做", "已通过", "待复习"}

# 不要求配题的知识点前缀
# 竞赛 C++ 的六个模块是纯语言知识点，依据「仅涉及已学知识」的要求本轮不出题，
# 因此其 P0 知识点不参与「无题覆盖」的判定。
EXEMPT_PREFIX = ("A-", "B-", "C-", "D-", "E-", "F-")

ESCAPED_PIPE = "\x00"


def split_row(line: str):
    """把 Markdown 表格行拆成单元格列表。

    需处理转义竖线 \\| —— 否则单元格内含 \\| 的表格会被切错。
    """
    s = line.strip()
    if not s.startswith("|"):
        return None
    s = s.replace("\\|", ESCAPED_PIPE)
    cells = [c.replace(ESCAPED_PIPE, "|").strip() for c in s.strip("|").split("|")]
    return cells


def is_separator(cells):
    """判断是否为表头分隔行（如 |---|---|）。"""
    return all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in cells if c)


BANK_HEADER = ("题号", "题名", "链接", "知识点", "状态", "代码")
KP_HEADER_FIRST = "序"


def parse_bank(path: Path):
    """解析题库总表，返回 (题目列表, 问题列表)。

    只解析表头为 BANK_HEADER 的表格，避免误抓文件内其他表格的行。
    """
    problems = []
    issues = []
    text = path.read_text(encoding="utf-8").splitlines()
    stage = "未分组"
    in_table = False

    for i, line in enumerate(text, start=1):
        m = re.match(r"^##\s+(阶段\s*\d+.*)$", line.strip())
        if m:
            stage = re.sub(r"\s+", " ", m.group(1)).strip()
            in_table = False
            continue

        cells = split_row(line)
        if not cells:
            in_table = False          # 表格结束
            continue
        if is_separator(cells):
            continue

        if cells[0] == "题号" and len(cells) == 6:
            in_table = True           # 进入题目表（表头第 4 列可带括注，故只校首列与列数）
            continue
        if not in_table:
            continue                  # 非题目表内的行一律跳过
        if len(cells) != 6:
            issues.append(("E105", i, f"题目行有 {len(cells)} 列，应为 6 列：{cells[0]}"))
            continue
        if not re.match(r"^(luogu|leetcode|cf|lanqiao|baidu|ccf|408)-", cells[0]):
            continue

        problems.append({
            "line": i,
            "stage": stage,
            "id": cells[0],
            "title": cells[1],
            "url": cells[2],
            "kps": cells[3],
            "status": cells[4],
            "code": cells[5],
        })

    return problems, issues


def parse_kps(path: Path):
    """解析知识点索引，返回 (知识点字典, P0 集合)。

    只解析表头首列为「序」的表格。
    """
    kps = {}
    p0 = set()
    in_table = False
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = split_row(line)
        if not cells:
            in_table = False
            continue
        if is_separator(cells):
            continue
        if cells[0] == KP_HEADER_FIRST and len(cells) == 5:
            in_table = True
            continue
        if not in_table or len(cells) != 5:
            continue
        code = cells[0]
        if not re.fullmatch(r"(\d+-\d+|[A-F]-\d+)", code):
            continue
        kps[code] = {"name": cells[1], "note": cells[2], "level": cells[3], "status": cells[4]}
        if cells[3].upper() == "P0":
            p0.add(code)
    return kps, p0


def extract_kp_codes(cell: str):
    """从「知识点（主 · 副）」单元格中提取知识点编号。"""
    return re.findall(r"(\d+-\d+|[A-F]-\d+)", cell)


def check(bank_dir: Path):
    issues = []
    bank_path = bank_dir / BANK_TABLE
    kp_path = bank_dir / KP_TABLE
    code_dir = bank_dir / CODE_DIR

    if not bank_path.exists():
        print(f"未找到题库总表：{bank_path}")
        return None, None
    if not kp_path.exists():
        print(f"未找到知识点索引：{kp_path}")
        return None, None

    problems, parse_issues = parse_bank(bank_path)
    issues.extend(parse_issues)
    kps, p0 = parse_kps(kp_path)

    code_files = {p.name for p in code_dir.glob("*.cpp")} if code_dir.exists() else set()

    covered = set()
    for pr in problems:
        # E101 链接格式
        platform = pr["id"].split("-", 1)[0]
        if platform == "408":
            if ZHENTI_MARK not in pr["url"]:
                issues.append(("E101", pr["line"], f"{pr['id']} 真题链接列应写「{ZHENTI_MARK}」"))
        else:
            prefix = PLATFORM_PREFIX.get(platform)
            if prefix and not pr["url"].startswith(prefix):
                issues.append(("E101", pr["line"], f"{pr['id']} 链接不符合 {platform} 规范：{pr['url']}"))

        # E102 知识点存在性
        codes = extract_kp_codes(pr["kps"])
        if not codes:
            issues.append(("E102", pr["line"], f"{pr['id']} 未标注任何知识点编号"))
        for c in codes:
            if c not in kps:
                issues.append(("E102", pr["line"], f"{pr['id']} 引用了索引中不存在的知识点 {c}"))
            covered.add(c)

        # E103 代码文件存在性
        if pr["status"] == STATUS_DONE:
            expect = f"{pr['id']}.cpp"
            if expect not in code_files:
                issues.append(("E103", pr["line"], f"{pr['id']} 状态为「{STATUS_DONE}」但缺少 {CODE_DIR}/{expect}"))
        if pr["code"] not in ("—", "-", ""):
            expect = f"{pr['id']}.cpp"
            if pr["code"] != expect:
                issues.append(("E106", pr["line"], f"{pr['id']} 代码列写的是 {pr['code']}，应为 {expect}"))
            if pr["code"] not in code_files:
                issues.append(("E103", pr["line"], f"{pr['id']} 代码列指向的 {pr['code']} 不存在"))

        # 状态取值
        if pr["status"] not in STATUS_ALL:
            issues.append(("E105", pr["line"], f"{pr['id']} 状态取值非法：{pr['status']}"))

    # E106 多余的代码文件
    listed = {f"{pr['id']}.cpp" for pr in problems if pr["code"] not in ("—", "-", "")}
    for extra in sorted(code_files - listed):
        issues.append(("E106", 0, f"{CODE_DIR}/{extra} 没有对应的题目行"))

    # E104 未被覆盖的 P0 知识点（竞赛 C++ 模块为纯语言知识点，予以豁免）
    exempt = []
    for c in sorted(p0 - covered):
        if c.startswith(EXEMPT_PREFIX):
            exempt.append(c)
            continue
        issues.append(("E104", 0, f"P0 知识点 {c} {kps[c]['name']} 无任何题目覆盖"))

    return problems, (kps, covered, p0, code_files, issues, exempt)


def main():
    ap = argparse.ArgumentParser(description="题库、知识点与代码文件的一致性校验")
    ap.add_argument("bank_dir", help="题库目录，需含 _题库总表.md 与 _知识点索引.md")
    ap.add_argument("--report", action="store_true", help="输出统计报告")
    args = ap.parse_args()

    bank_dir = Path(args.bank_dir)
    if not bank_dir.is_dir():
        print(f"路径不存在或不是目录：{bank_dir}")
        return 2

    problems, extra = check(bank_dir)
    if problems is None:
        return 2
    kps, covered, p0, code_files, issues, exempt = extra

    if issues:
        print("问题清单：")
        for code, line, msg in sorted(issues, key=lambda x: (x[1] == 0, x[1])):
            loc = f"第 {line} 行" if line else "全局"
            print(f"  {code}  {loc}  {msg}")
    else:
        print("问题清单：无")

    by_code = {}
    for code, _, _ in issues:
        by_code[code] = by_code.get(code, 0) + 1

    print("\n" + "=" * 60)
    print(f"题目总数：{len(problems)}")
    done = sum(1 for p in problems if p["status"] == STATUS_DONE)
    print(f"已通过：{done}")
    print(f"代码文件数：{len(code_files)}")
    print(f"知识点总数：{len(kps)}　其中 P0：{len(p0)}")
    print(f"已被题目覆盖的知识点：{len(covered)}")
    print(f"问题总数：{len(issues)}")

    if by_code:
        print("\n按类型汇总：")
        for code in sorted(by_code):
            print(f"  {code}  严重度 {SEVERITY.get(code, '-')}  共 {by_code[code]} 处")
            print(f"        处理：{FIX_HINT.get(code, '')}")

    if args.report:
        print("\n未被题目覆盖的 P0 知识点：")
        uncovered = [c for c in sorted(p0 - covered) if not c.startswith(EXEMPT_PREFIX)]
        if uncovered:
            for c in uncovered:
                print(f"  {c}  {kps[c]['name']}")
        else:
            print("  无")

        if exempt:
            print(f"\n已豁免的 P0 知识点（竞赛 C++ 模块，本轮不出题）：{len(exempt)} 个")
            for c in exempt:
                print(f"  {c}  {kps[c]['name']}")

    print("=" * 60)
    if not issues:
        print("结果：三方一致，校验通过。")
        return 0
    print("结果：存在问题，请按提示处理。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
