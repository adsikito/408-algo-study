# -*- coding: utf-8 -*-
"""55_生成合集.py —— 把分章笔记合并为 80_合集 下的两份单文件（幂等，可重复执行）

用法：python 50_工具与模板/55_生成合集.py
规则：分章文件为修订对象；本脚本只重新拼装合集，不修改任何分章文件。
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def merge(files, out, title):
    parts = []
    parts.append("<!-- 本文件为合并单文件（合集），由 55_生成合集.py 自动拼装；修订请改分章文件后重跑本脚本 -->\n")
    parts.append("# %s\n" % title)
    for f in files:
        txt = io.open(f, encoding="utf-8").read()
        parts.append("\n\n---\n\n<!-- 来源：%s -->\n\n" % os.path.basename(f))
        parts.append(txt)
    io.open(out, "w", encoding="utf-8", newline="\n").write("".join(parts))
    print("已生成 %s（%d 个来源文件）" % (out, len(files)))


def collect(d, suffix=".md"):
    out = []
    for f in sorted(os.listdir(d)):
        if f.endswith(suffix):
            out.append(os.path.join(d, f))
    return out


# 合集一：考研 408 全部 12 项
kaoyan_order = [
    "README_使用说明与索引.md", "00_绪论与算法分析.md", "01_线性表.md", "02_栈与队列.md",
    "03_串与模式匹配.md", "04_树与二叉树.md", "05_图.md", "06_查找.md", "07_排序.md",
    "附录A_C语言前置基础速查.md", "附录B_408高频考点与题型索引.md", "附录C_非考纲内容提示.md",
]
files1 = [os.path.join("01_考研", "408数据结构", f) for f in kaoyan_order]
for f in files1:
    assert os.path.exists(f), "缺少分章文件：%s" % f
merge(files1, os.path.join("80_合集", "考研408数据结构_合集.md"), "考研 408 数据结构　笔记合集")

# 合集二：竞赛全部（C++ 六模块 + 算法专题八阶段）
files2 = collect("02_竞赛/02_竞赛C++")
alg = "02_竞赛/01_算法专题"
files2.append(os.path.join(alg, "阶段0_前置基础.md"))
files2.append(os.path.join(alg, "阶段1_基础技巧", "阶段1_基础技巧.md"))
for d in ["阶段1_基础技巧", "阶段2_算法思想", "阶段3_基础数据结构", "阶段4_搜索",
          "阶段5_图论", "阶段6_字符串", "阶段7_动态规划", "阶段8_高级结构"]:
    files2.extend(collect(os.path.join(alg, d)))
merge(files2, os.path.join("80_合集", "竞赛笔记_合集.md"), "竞赛笔记　合集（C++ 六模块 + 算法专题八阶段）")
