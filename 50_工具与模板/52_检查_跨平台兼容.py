#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
52_检查_跨平台兼容.py —— 笔记跨平台兼容性检查

用途
    扫描 Markdown 笔记，找出会导致 Obsidian / Notion / GitHub / 通用 Markdown
    渲染不一致的语法，输出可执行的修改清单。

用法
    python 52_检查_跨平台兼容.py <路径>              检查单个文件或整个目录
    python 52_检查_跨平台兼容.py <路径> --fix-copy   额外生成剥离平台专属语法的副本
    python 52_检查_跨平台兼容.py <路径> --quiet      只输出汇总，不列明细

检查项
    E001  表情符号与装饰性图形字符      三方渲染不一，且违反笔记格式约定
    E002  HTML 标签                     Notion 不渲染，会原样显示为文本
    E003  ==高亮==                      仅部分平台支持，应改用加粗
    E004  %%注释%%                      仅 Obsidian 支持，导出后残留
    E005  [[双链]]                      Notion 与 GitHub 不支持，应改为文本链接
    E006  ![[嵌入]]                     仅 Obsidian 支持
    E007  五级及以深标题                 Notion 导入会压平
    E008  表格列数超过 6                移动端横向滚动困难（6 列为可接受上限）
    E009  代码块语言标注不规范          统一使用 cpp 等标准语言名
    E010  Dataview 查询块               仅 Obsidian 支持，不得承载独有信息
    E011  代码块缺语言标注              仅影响语法高亮，不影响渲染，属风格建议

忽略机制
    <!-- compat-ignore-file -->         写在文件任意位置，整个文件跳过检查
    <!-- compat-ignore -->              写在某一行行首，该行跳过检查
    适用于「文档本身在讲解这些语法」的场景。

退出码
    0  全部通过
    1  发现问题
"""

import argparse
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 检查规则
# ---------------------------------------------------------------------------

# 表情符号与装饰性图形字符
EMOJI_RE = re.compile(
    "["
    "\U0001F000-\U0001FAFF"   # 各类表情、图标
    "\U00002600-\U000027BF"   # 杂项符号与装饰符号（含对钩、叉号、星形）
    "\U00002B00-\U00002BFF"   # 各类箭头装饰符号
    "\U0001F1E6-\U0001F1FF"   # 区域指示符（国旗）
    "\U0000FE0F"              # 变体选择符
    "\u2705\u274C\u2B50\u26A0"  # 常见单字符符号
    "\u25A0-\u25FF"           # 几何图形（方形、圆形、三角、菱形）
    "\u2605\u2606"            # 实心与空心星形
    "\u2610\u2611\u2612"      # 勾选框
    "]"
)

HTML_TAG_RE = re.compile(r"</?(span|div|details|summary|br|font|mark|sub|sup|table|tr|td|details)\b[^>]*>", re.I)
HIGHLIGHT_RE = re.compile(r"==[^=\n]+==")
OBSIDIAN_COMMENT_RE = re.compile(r"%%.*?%%")
# 行内代码片段：在检测「等号高亮」与「百分号注释」之前必须先剔除，
# 否则 C++ 里的 == 比较（如 `(n & 1) == 0`）会被误判为 Markdown 高亮语法。
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
WIKILINK_RE = re.compile(r"(?<!\!)\[\[[^\]]+\]\]")
EMBED_RE = re.compile(r"!\[\[[^\]]+\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
DATAVIEW_RE = re.compile(r"^\s*```dataview", re.I | re.M)

ALLOWED_LANGS = {"cpp", "c", "python", "py", "text", "plaintext", "markdown", "md", "bash", "sh", "sql", "java", "json", "yaml", "xml", "html", "css", "js", "javascript", "diff", "ini", "makefile", "cmake"}

MAX_TABLE_COLS = 6   # 6 列为移动端可接受的横滚上限，超过必须拆分

IGNORE_FILE = "compat-ignore-file"
IGNORE_LINE = "compat-ignore"

SEVERITY = {
    "E001": "高",
    "E002": "高",
    "E003": "中",
    "E004": "中",
    "E005": "中",
    "E006": "中",
    "E007": "高",
    "E008": "低",
    "E009": "中",
    "E010": "低",
    "E011": "低",
}

FIX_HINT = {
    "E001": "删除表情与装饰符号，改用加粗或方括号标签（如 【重点】）",
    "E002": "删除 HTML 标签，改用 Markdown 原生语法",
    "E003": "把 ==文本== 改为 **文本**",
    "E004": "删除 %%注释%% 或改为普通段落",
    "E005": "把 [[文件#标题]] 改为 文件.md#标题 形式的文本链接",
    "E006": "把 ![[文件]] 改为普通 Markdown 链接",
    "E007": "把标题降级到四级以内，更细的层次改用加粗行或有序列表",
    "E008": "拆分表格，使列数不超过 6",
    "E009": "改用标准语言名，C++ 统一写 cpp（Notion 与 GitHub 均识别）",
    "E010": "Dataview 块只作附加视图，确保手工表格也能提供同样信息",
    "E011": "补上语言标注；纯文本与树状图写 text。此为风格建议，不影响跨平台渲染",
}


def check_file(path: Path):
    """检查单个文件，返回问题列表。"""
    issues = []
    try:
        raw = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as exc:
        return [("E000", 0, f"无法读取文件：{exc}")]

    # 整文件忽略（用于讲解语法本身的文档）
    if IGNORE_FILE in raw:
        return []

    lines = raw.splitlines()
    in_code = False
    fence_len = 3
    fence_char = "`"
    table_cols_stack = []
    table_start = 0

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # 代码块边界（支持嵌套：只有长度不短于开始围栏、且不带信息串的同类围栏才能闭合）
        m_fence = re.match(r"^(`{3,}|~{3,})(.*)$", stripped)
        if m_fence:
            marker, info = m_fence.group(1), m_fence.group(2)
            if not in_code:
                in_code = True
                fence_len = len(marker)
                fence_char = marker[0]
                lang = info.strip().lower()
                if lang and lang not in ALLOWED_LANGS:
                    issues.append(("E009", i, f"代码块语言标注不规范：{lang!r}"))
                elif not lang:
                    issues.append(("E011", i, "代码块缺少语言标注（风格建议）"))
            elif marker[0] == fence_char and len(marker) >= fence_len and not info.strip():
                in_code = False
            continue

        if in_code:
            continue

        # 行级忽略
        if IGNORE_LINE in line:
            continue

        # 表格列数
        if stripped.startswith("|") and stripped.endswith("|"):
            if not table_cols_stack:
                table_start = i
            # 先保护转义竖线 \|，否则单元格内含 \| 的表格会被切错
            safe = stripped.replace("\\|", "\x00")
            table_cols_stack.append(len(safe.split("|")[1:-1]))
        else:
            if table_cols_stack:
                maxc = max(table_cols_stack)
                if maxc > MAX_TABLE_COLS:
                    issues.append(("E008", table_start, f"表格有 {maxc} 列，超过 {MAX_TABLE_COLS} 列上限"))
                table_cols_stack = []

        # 表情与装饰符号
        for m in EMOJI_RE.finditer(line):
            issues.append(("E001", i, f"发现装饰性字符 {m.group()!r}"))
            break

        if HTML_TAG_RE.search(line):
            issues.append(("E002", i, f"发现 HTML 标签 {HTML_TAG_RE.search(line).group()!r}"))

        # 行内高亮与专属注释：先在剔除行内代码后的文本上判断，避免误报
        probe = INLINE_CODE_RE.sub("", line)

        if HIGHLIGHT_RE.search(probe):
            issues.append(("E003", i, f"发现高亮语法 {HIGHLIGHT_RE.search(probe).group()!r}"))

        if OBSIDIAN_COMMENT_RE.search(probe):
            issues.append(("E004", i, "发现 Obsidian 专属注释 %%...%%"))

        if EMBED_RE.search(line):
            issues.append(("E006", i, f"发现 Obsidian 嵌入 {EMBED_RE.search(line).group()!r}"))
        elif WIKILINK_RE.search(line):
            issues.append(("E005", i, f"发现双链 {WIKILINK_RE.search(line).group()!r}"))

        m = HEADING_RE.match(line)
        if m and len(m.group(1)) > 4:
            issues.append(("E007", i, f"标题层级为 {len(m.group(1))} 级，超过四级"))

    if table_cols_stack:
        maxc = max(table_cols_stack)
        if maxc > MAX_TABLE_COLS:
            issues.append(("E008", table_start, f"文末表格有 {maxc} 列，超过 {MAX_TABLE_COLS} 列上限"))

    if DATAVIEW_RE.search(raw):
        issues.append(("E010", 0, "发现 Dataview 查询块，确认其信息另有手工表格承载"))

    return issues


INLINE_SPLIT_RE = re.compile(r"(`[^`\n]*`)")


def _sub_outside_code(pattern, repl, line: str) -> str:
    """只在行内代码之外的片段做替换，避免改坏代码里的 == 或 %%。"""
    parts = INLINE_SPLIT_RE.split(line)
    for i in range(0, len(parts), 2):        # 偶数下标是代码之外的文本
        parts[i] = pattern.sub(repl, parts[i])
    return "".join(parts)


def strip_platform_syntax(text: str) -> str:
    """生成剥离平台专属语法后的副本，用于导入 Notion。"""
    out = []
    in_code = False
    fence_len = 3
    fence_char = "`"
    for line in text.splitlines():
        m_fence = re.match(r"^(`{3,}|~{3,})(.*)$", line.strip())
        if m_fence:
            marker, info = m_fence.group(1), m_fence.group(2)
            if not in_code:
                in_code = True
                fence_len = len(marker)
                fence_char = marker[0]
            elif marker[0] == fence_char and len(marker) >= fence_len and not info.strip():
                in_code = False
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        line = _sub_outside_code(HTML_TAG_RE, "", line)
        line = _sub_outside_code(HIGHLIGHT_RE, lambda m: "**" + m.group()[2:-2] + "**", line)
        line = _sub_outside_code(OBSIDIAN_COMMENT_RE, "", line)
        line = _sub_outside_code(EMBED_RE, lambda m: m.group()[3:-2], line)
        line = _sub_outside_code(WIKILINK_RE, lambda m: m.group()[2:-2].replace("#", ".md#"), line)
        line = EMOJI_RE.sub("", line)
        out.append(line)
    return "\n".join(out) + "\n"


def collect_files(target: Path):
    if target.is_file():
        return [target]
    # 原样复制的课程方文件（2026-09-13 素材复制）不适用本工程排版规范，跳过扫描：
    # 只扫自撰笔记；逐字副本（素材章/课程资料）一律跳过
    files = sorted(p for p in target.rglob("*.md") if p.is_file())
    out = []
    for p in files:
        rel = p.as_posix()
        if rel.startswith("03_常规课程/C++课程资料/"):
            continue
        if rel.startswith("02_竞赛/01_算法专题/") and len(rel.split("/")) > 3:
            continue
        if rel.startswith("01_考研/408数据结构/") and len(rel.split("/")) > 2:
            continue
        out.append(p)
    return out


def main():
    parser = argparse.ArgumentParser(
        description="检查 Markdown 笔记的跨平台兼容性",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("target", help="待检查的文件或目录")
    parser.add_argument("--fix-copy", action="store_true", help="额外生成剥离平台专属语法的副本")
    parser.add_argument("--quiet", action="store_true", help="只输出汇总")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"路径不存在：{target}")
        return 2

    files = collect_files(target)
    if not files:
        print("未找到 Markdown 文件")
        return 2

    total_issues = 0
    files_with_issues = 0
    by_code = {}

    for f in files:
        issues = check_file(f)
        if not issues:
            continue
        files_with_issues += 1
        total_issues += len(issues)
        for code, line, msg in issues:
            by_code[code] = by_code.get(code, 0) + 1
        if not args.quiet:
            print(f"\n[{f}]")
            for code, line, msg in sorted(issues, key=lambda x: x[1]):
                loc = f"第 {line} 行" if line else "全文"
                print(f"  {code}  {loc}  {msg}")

        if args.fix_copy:
            copy_path = f.with_name(f.stem + "_notion" + f.suffix)
            copy_path.write_text(strip_platform_syntax(f.read_text(encoding="utf-8")), encoding="utf-8")
            if not args.quiet:
                print(f"  -> 已生成剥离副本：{copy_path.name}")

    print("\n" + "=" * 56)
    print(f"扫描文件数：{len(files)}")
    print(f"存在问题文件：{files_with_issues}")
    print(f"问题总数：{total_issues}")

    if by_code:
        print("\n按类型汇总：")
        for code in sorted(by_code):
            sev = SEVERITY.get(code, "-")
            print(f"  {code}  严重度 {sev}  共 {by_code[code]} 处")
            print(f"        处理：{FIX_HINT.get(code, '')}")

    print("=" * 56)
    if total_issues == 0:
        print("结果：全部通过，可直接迁移到各平台。")
        return 0
    print("结果：存在问题，请按上述提示处理后再迁移。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
