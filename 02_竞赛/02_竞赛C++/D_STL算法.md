# 模块 D　STL 算法

> **元信息**
> 优先级：`P0`　｜　所属子分类：`02_竞赛\02_竞赛C++`　｜　学习顺序：五阶段中的**阶段 3**
> 前置：模块 C（`vector`、`pair`、`set` / `map`）、模块 A（运算符、结构体）
> 后续：模块 E（现代语法糖）、模块 F（竞赛工程化）
> 最近复习：未开始　｜　整体掌握：`[未学]`

> **图例**
> **重要程度**：`P0` 必掌握（加粗 + 主色）｜`P1` 需熟练（次色）｜`P2` 了解即可（弱化色）
> **内容类型**：定义概念｜模板公式｜例题自测｜易错陷阱｜通俗类比｜补充延伸
> **掌握状态**：`[未学]` `[学过]` `[会做]` `[易错]` `[掌握]`（纯文字，不着色）
> 说明：颜色仅用于加速定位，**信息一律由文字标签与字重承载**，黑白打印不丢信息。

---

## 零、本模块的定位：用现成算法替代手写循环

手写循环能实现一切，但代价是**时间**与**错误率**。本模块的验收标准是：

> **能不用手写循环完成排序、查找、去重、统计四类操作。**

### 0.1 现有代码的实测缺口

对竞赛代码（`资料\03_算法集训\` 下 **75 个 `.cpp`**）统计（2026-09-12 快照）：

| 算法 | 出现次数 | 判定 | 对应知识点 |
|------|---------|------|-----------|
| `sort` | 高频 | 使用充分 | D-1 |
| `lower_bound` | **0** | **完全未使用** | D-3 |
| `unique(` | **0** | **完全未使用** | D-4 |
| `reverse(` | **0** | **完全未使用** | D-5 |
| `fill(` | **0** | **完全未使用** | D-5 |
| `__builtin_` 系列 | **0** | **完全未使用** | D-10 |
| lambda 作比较器 | **0** | **完全未使用** | D-2 |

结论：**排序会了，但「查找、去重、填充、位统计」四类全部靠手写。**
这四类恰好是二分题、去重题、初始化、位计数题的标配，手写既慢又易错。

---

## 一、本章速览

**一句话概括**：把「二分查找、去重、填充、统计、位计数」五类反复手写的逻辑，换成标准库的一行调用。

| 序 | 知识点 | 优先级 | 深度 | 掌握 | 前置 |
|----|--------|--------|------|------|------|
| 1 | `sort` 与比较规则 | P0 | 熟练 | `[未学]` | — |
| 2 | 比较器的三种写法 | P0 | 熟练 | `[未学]` | 1 |
| 3 | `lower_bound` / `upper_bound` | P0 | 熟练 | `[未学]` | 1 |
| 4 | `unique` + `erase` 去重 | P0 | 熟练 | `[未学]` | 1 |
| 5 | `reverse` / `fill` / `swap` / `min` / `max` | P0 | 熟练 | `[未学]` | — |
| 6 | `max_element` / `min_element` / `count` / `find` | P1 | 会用 | `[未学]` | 5 |
| 7 | `accumulate` | P1 | 会用 | `[未学]` | 5 |
| 8 | `next_permutation` / `prev_permutation` | P1 | 会用 | `[未学]` | 2 |
| 9 | `nth_element` / `partial_sort` | P2 | 会用 | `[未学]` | 1 |
| 10 | `__builtin_` 系列 | P1 | 会用 | `[未学]` | 5 |

> 「序」即学习先后顺序。比较器（第 2）紧跟 `sort`（第 1），因为**排序题很少不需要自定义规则**。

---

## 二、前置检查

| 前置知识点 | 出处 | 自测 |
|-----------|------|------|
| `vector` 基本操作与迭代器 | 模块 C-1 | - [ ] 能写出 `v.begin()` / `v.end()` 的含义 |
| `pair` 的字典序比较 | 模块 C-3 | - [ ] 能解释 `{2,3} < {2,9}` |
| 结构体与 `operator<` | 模块 A-7 | - [ ] 能写出末尾带 `const` 的 `operator<` |
| 比较必须严格弱序 | 模块 A-7 | - [ ] 能说出为什么不能用 `<=` |

> 任何一项未打钩，先回补该前置。**本模块的全部正确性都建立在「比较规则合法」之上。**

---

## 三、知识点逐讲

### D-1　`sort` 与比较规则　`P0`　熟练　`[未学]`

> **【重点】** `sort` 的排序区间是 **`[begin, end)` 左闭右开**。
> 传 `end` 是**最后一个元素的下一个位置**，不是最后一个元素。

**是什么**：对所有满足随机访问迭代器的容器区间做排序，平均 O(n log n)。底层是内省排序（快排 + 堆排 + 插排混合）。

**为什么**：手写快排容易写出最坏 O(n²)，且边界条件容易错。`sort` 保证最坏 O(n log n)，
且已是高度优化过的实现，比手写更快。

**怎么用**：

1. 基本用法：`sort(v.begin(), v.end())` 升序。
2. **`pair` 与 `string` 无需比较器**，它们有内置字典序。
3. 结构体需要比较器（三种写法见 D-2）。
4. 数组排序：`sort(a + 1, a + n + 1)` 表示排序 `a[1]` 到 `a[n]`。
5. 稳定性：`sort` **不保证稳定**；需要稳定时用 `stable_sort`。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    // 1. 基本升序
    vector<int> v = {5, 1, 4, 1, 5, 2};
    sort(v.begin(), v.end());
    printf("升序：");
    for (int x : v) printf("%d ", x);
    printf("\n");

    // 2. 降序：用 greater<int>
    sort(v.begin(), v.end(), greater<int>());
    printf("降序：");
    for (int x : v) printf("%d ", x);
    printf("\n");

    // 3. 数组排序：1 起始的数组，区间写法要 +1
    int a[7] = {0, 5, 1, 4, 1, 5, 2};       // a[0] 弃用
    int n = 6;
    sort(a + 1, a + n + 1);                  // 边界：排序 a[1] 到 a[n]
    printf("数组升序：");
    for (int i = 1; i <= n; i++) printf("%d ", a[i]);
    printf("\n");

    // 4. pair 与 string 无需比较器
    vector<pair<int,int>> pv = {{2,9},{1,5},{2,3}};
    sort(pv.begin(), pv.end());              // 先比 first 再比 second
    printf("pair 排序：");
    for (auto &x : pv) printf("(%d,%d) ", x.first, x.second);
    printf("\n");

    vector<string> sv = {"banana", "apple", "cherry"};
    sort(sv.begin(), sv.end());
    printf("string 排序：");
    for (auto &x : sv) printf("%s ", x.c_str());
    printf("\n");

    // 5. 只排一部分：默认排序前 k 个（配合 partial_sort 见 D-9）
    vector<int> w = {9, 8, 7, 6, 5};
    sort(w.begin(), w.begin() + 3);          // 只排前 3 个
    printf("只排前 3 个：");
    for (int x : w) printf("%d ", x);        // 7 8 9 6 5
    printf("\n");
    return 0;
}
```

> **【易错】** 五处：
> 1. **区间写成 `v.begin(), v.end() - 1`** —— 最后一个元素没参与排序。**左闭右开，右端是 `end()`。**
> 2. **数组排序忘了 +1** —— `sort(a, a + n)` 会把 `a[0]`（未使用的占位）一起排，
>    且丢掉 `a[n]`。**1 起始数组写 `sort(a + 1, a + n + 1)`。**
> 3. **比较器不是严格弱序**（如 `<=`）—— 内部会越界，可能 RE 或乱序。**必须用 `<`。**
> 4. **比较器传值而非传引用** —— 结构体大时每次比较都拷贝，显著变慢。写 `const T &`。
> 5. **想排序 `set` 的元素** —— `set` 本身有序且元素是 `const`，不能排序。

> **【类比】** `sort` 的区间像**电影院座位号**：`begin` 是第一个座位，`end` 是「最后一个座位的后一个」——
> 也就是幕布。区间里的座位就是所有观众。

> **【记忆】** **左闭右开；1 起始数组记得 +1；比较器用 `<` 且传 `const &`。**

**关联**

- `[前置]` 见 C-1 `vector`、C-3 `pair`。
- `[后续]` 见 D-2 比较器、D-3 `lower_bound`（**必须先排序**）、算法专题阶段 1「二分」。
- `[易混]` `sort` 与 `stable_sort`：前者更快不保序，后者保序但稍慢。
- `[组合]` 与 D-4 `unique` 组合 → 排序后去重；与 D-8 `next_permutation` 组合 → 全排列需先排序。

---

### D-2　比较器的三种写法　`P0`　熟练　`[未学]`

> **【重点】** 三种写法按使用场景选：**独立函数**（规则简单、复用）、
> **lambda**（就地写、最常用）、**`operator<`**（类型自带顺序，进 `set` / `map` 时必须）。
> 现有代码中**比较器全靠手写独立函数**，lambda 零使用。

**是什么**：告诉 `sort` / `priority_queue` / `set` 一个「谁排前面」的规则。

**为什么**：不同题需要的排序规则不同（按权值、按距离、按第二关键字）。
比较器把「规则」与「数据」分离，同一个 `sort` 能适配全部场景。

**怎么用**：

| 写法 | 形式 | 适用 |
|------|------|------|
| 独立函数 | `bool cmp(const T&a, const T&b){...}` | 规则简单、多处复用 |
| **lambda**（就地写） | `sort(v.begin(), v.end(), [](const T&a, const T&b){...})` | **单处使用，最推荐** |
| `operator<` | 类型内 `bool operator<(...) const` | 类型自带天然顺序；**进 `set` / `map` 的唯一方式** |

**必须遵守的规则**：比较器实现的是「严格弱序」，即 `cmp(a,b)` 表示 **a 应当排在 b 前面**。
**禁止使用 `<=`**，否则两个相等元素会互相认为「我应在你前面」，导致未定义行为。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <vector>
#include <algorithm>
#include <string>
using namespace std;

struct Student {
    string name;
    int score;
};

// 写法一：独立函数（规则复杂、需复用时用）
// 规则：分数高的在前；分数相同按名字字典序升序
bool cmpByScoreThenName(const Student &a, const Student &b) {
    if (a.score != b.score) return a.score > b.score;   // 注意 > 表示降序
    return a.name < b.name;                             // 分数相同，名字升序
}

int main() {
    vector<Student> v = {{"bob", 90}, {"amy", 90}, {"cid", 85}};

    // 写法一
    sort(v.begin(), v.end(), cmpByScoreThenName);
    printf("写法一：");
    for (auto &s : v) printf("%s(%d) ", s.name.c_str(), s.score);
    printf("\n");

    // 写法二：lambda（就地写，只此一处用，不污染命名空间）
    // 这是推荐写法：规则与使用点放在一起，读者不用跳转
    vector<pair<int,int>> pv = {{1, 9}, {2, 3}, {3, 7}};
    sort(pv.begin(), pv.end(), [](const pair<int,int> &a, const pair<int,int> &b) {
        return a.second > b.second;      // 按 second 降序
    });
    printf("写法二：");
    for (auto &x : pv) printf("(%d,%d) ", x.first, x.second);
    printf("\n");

    // 写法三：lambda 捕获外部变量（按动态阈值排）
    int threshold = 5;
    sort(pv.begin(), pv.end(), [threshold](const pair<int,int> &a, const pair<int,int> &b) {
        // 把「接近 threshold 的」排在前面
        return abs(a.second - threshold) < abs(b.second - threshold);
    });
    printf("写法三（按接近 %d 排序）：", threshold);
    for (auto &x : pv) printf("(%d,%d) ", x.first, x.second);
    printf("\n");

    // 错误示范：<= 不是严格弱序
    // sort(v.begin(), v.end(), [](const Student&a, const Student&b){ return a.score <= b.score; });
    // 上面这行在某些实现上会 RE（越界），在另一些上给出乱序结果
    printf("（错误示范见代码注释）\n");
    return 0;
}
```

lambda 的完整语义（捕获方式、`mutable`、返回值推导）见模块 E-3。

> **【易错】** 五处，前两条是致命的：
> 1. **用 `<=` 而非 `<`** —— 违反严格弱序，行为未定义。
>    **记忆：比较器里只允许出现 `<`（或 `>`），永远不出现 `<=` / `>=`。**
> 2. **参数不写 `const &`** —— 大结构体每次比较都拷贝。n log n 次比较会放大成明显开销。
> 3. **`operator<` 漏末尾 `const`** —— 放进 `set` 时编译报错一大片。
> 4. **降序写反方向**。`return a.score > b.score;` 是降序（大的在前），不是升序。
> 5. **lambda 捕获用 `[=]` 但需要修改** —— 默认按值捕获是只读的，要加 `mutable`。

> **【类比】** 比较器像**裁判规则**：说清「谁赢」。规则必须**自洽**——
> 不能说「A 赢 B，且 B 赢 A」，那比赛就乱了。`<=` 恰恰会产生这种自相矛盾。

> **【记忆】** **比较器里只有 `<`，没有 `<=`；参数一律 `const &`。**

**关联**

- `[前置]` 见 D-1 `sort`、A-7 `operator<`。
- `[后续]` 见 E-3 lambda（完整语义）、C-5 `priority_queue`（自定义类型比较）。
- `[易混]` `sort` 的比较器与 `priority_queue` 的 `operator<` 语义**相反**：
  `sort` 里 `a<b` 表示 a 在前（升序）；堆里「更大的」优先。见 C-5 易错 3。
- `[组合]` 与 `set` / `map` 组合 → 自定义类型入关联容器的必需条件。

---

### D-3　`lower_bound` / `upper_bound`　`P0`　熟练　`[未学]`

> **【重点】** 这是**二分题的标准工具**，现有代码中仅出现 1 次。
> **四个组合覆盖全部边界语义，必须背下来。**

**是什么**：在**已排序**区间上做二分查找，返回迭代器/指针。

| 函数 | 含义 | 记忆 |
|------|------|------|
| `lower_bound(b, e, x)` | 第一个 **≥ x** 的位置 | lower = 下界，可以等于 |
| `upper_bound(b, e, x)` | 第一个 **> x** 的位置 | upper = 上界，必须大于 |
| `s.lower_bound(x)`（`set` / `map` 成员） | 同上，但 O(log n) | **必用成员函数** |
| `s.upper_bound(x)`（成员） | 同上 | **必用成员函数** |

**为什么**：手写二分有四种常见错法（`mid` 取整方向、`lo/hi` 更新、边界返回、死循环）。
用标准库一个调用解决，且保证 O(log n)。

**怎么用**：

1. **前提：区间必须有序**。未排序的区间结果无意义。
2. 求「有多少个元素 < x」：`lower_bound` 的位置减去起始位置。
3. 求「x 出现的次数」：`upper_bound - lower_bound`。
4. 求「第一个 ≥ x 的值」：`*lower_bound(...)`，**先判是否 `end()`**。
5. 降序区间需要传 `greater<T>()` 作为比较器，且语义反转。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <vector>
#include <algorithm>
#include <set>
using namespace std;

int main() {
    // 前提：已排序
    vector<int> v = {1, 2, 2, 2, 3, 5, 5, 8};      // 有序，含重复

    // 1. 四个边界语义
    int x = 2;
    auto lb = lower_bound(v.begin(), v.end(), x);   // 第一个 >= 2
    auto ub = upper_bound(v.begin(), v.end(), x);   // 第一个 > 2
    printf("x=%d：lower_bound 下标 %d（值 %d），upper_bound 下标 %d（值 %d）\n",
           x, (int)(lb - v.begin()), *lb,
           (int)(ub - v.begin()), *ub);
    // 输出：下标 1（值 2），下标 4（值 3）

    // 2. 统计 x 的个数：ub - lb
    printf("值 %d 出现 %d 次\n", x, (int)(ub - lb));   // 3

    // 3. 统计有多少个元素 < x：lb - begin
    printf("小于 %d 的元素有 %d 个\n", x, (int)(lb - v.begin()));   // 1

    // 4. 不存在时的两种情形
    int y = 4;
    auto p = lower_bound(v.begin(), v.end(), y);
    if (p != v.end()) printf(">= %d 的最小元素：%d\n", y, *p);      // 5
    // 求前驱：需要 != begin 才能往回走
    if (p != v.begin()) printf("< %d 的最大元素：%d\n", y, *(p - 1)); // 3

    // 5. 返回 end() 的情形：没有 >= 的元素
    int z = 100;
    auto q = lower_bound(v.begin(), v.end(), z);
    printf("找 %d 的结果是否是 end()：%d\n", z, (int)(q == v.end())); // 1

    // 6. 求最长上升子序列 LIS 的经典用法（nlogn）
    vector<int> a = {10, 9, 2, 5, 3, 7, 101, 18};
    vector<int> tail;                     // tail[i] = 长度为 i+1 的上升子序列的最小结尾
    for (int val : a) {
        // 找第一个 >= val 的位置，替换之（这里是严格上升，用 lower_bound）
        auto it = lower_bound(tail.begin(), tail.end(), val);
        if (it == tail.end()) tail.push_back(val);   // 延长
        else *it = val;                              // 替换，保持结尾最小
    }
    printf("LIS 长度 = %d\n", (int)tail.size());     // 4

    // 7. set / map 必须用成员函数（对数级）
    set<int> s(v.begin(), v.end());
    auto sit = s.lower_bound(4);                     // 成员函数：O(log n)
    printf("set 中 >= 4 的最小值：%d\n", *sit);       // 5

    // 8. 降序区间的写法（语义反转）
    sort(v.begin(), v.end(), greater<int>());
    // 降序下，lower_bound 传 greater 得到「第一个 <= x」的位置
    auto d = lower_bound(v.begin(), v.end(), 5, greater<int>());
    printf("降序区间找 %d：下标 %d，值 %d\n", 5, (int)(d - v.begin()), *d);
    return 0;
}
```

> **【易错】** 六处：
> 1. **对未排序区间用 `lower_bound`** —— 结果无意义，且不报错。
> 2. **对 `set` / `map` 用 `std::lower_bound`** —— 退化成 O(n)。**必须用成员函数。**
> 3. **直接解引用不判 `end()`** —— UB。**纪律：解引用前必判。**
> 4. **求前驱时不判 `begin()`** —— `p - 1` 越界。
> 5. **`lower_bound` 与 `upper_bound` 记反**。
>    **记忆：`lower` 是「下界」，取到等号；`upper` 是「上界」，取不到等号。**
> 6. **`ub - lb` 得到的是元素个数**，但在 `set` 上迭代器不支持减法 —— 那是线性代价，要用 `distance` 或干脆别在 `set` 上这样算。

> **【类比】** 一排按身高站好的人。`lower_bound(175)` 是「第一个不矮于 175 的人」，
> `upper_bound(175)` 是「第一个比 175 高的人」。中间那段就是**所有身高正好 175 的人**。

> **【记忆】** **`lower` 含等号，`upper` 不含；`set` 用成员函数；解引用先判 `end`。**

**关联**

- `[前置]` 见 D-1 `sort`（必须有序）、C-7 `set`（成员函数版本）。
- `[后续]` 见算法专题阶段 1「二分答案」、阶段 1「LIS 的 nlogn 解法」。
- `[易混]` `lower_bound` 与手写二分：标准库返回「第一个满足条件的位置」，手写容易错边界。
- `[组合]` 与 D-4 `unique` 组合 → 排序 + 去重 + 二分是离散化的标准三步（算法专题阶段 1）。
- `[延伸]` 二分答案（对答案空间二分）是它的推广，见算法专题阶段 1。

---

### D-4　`unique` + `erase` 去重　`P0`　熟练　`[未学]`

> **【重点】** **`unique` 只删除「相邻的重复元素」**，所以必须先排序。
> 它**不改变容器大小**，只是把重复元素移到末尾，返回「新逻辑结尾」的位置。
> 现有代码中 `unique` **零使用**。

**是什么**：把相邻的重复元素「压缩」掉，返回去重后区间的结束位置。

**为什么**：去重是三处的高频需求 ——
**离散化**（把大范围值映射到小下标）、**统计不同元素个数**、**消除重复的边**。

**怎么用**：

1. **标准三步**：`sort` → `unique` → `erase`（`unique` 只搬不移）。
2. 只想去重不改容器大小：用返回的迭代器作为新的逻辑结尾。
3. 想统计不同元素个数：`unique(...) - v.begin()`。
4. 自定义类型需要 `operator==`（不是 `operator<`）。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    // 1. 标准三步：sort + unique + erase
    vector<int> v = {3, 1, 3, 2, 3, 1, 5};
    sort(v.begin(), v.end());                                  // 必须先排序
    v.erase(unique(v.begin(), v.end()), v.end());              // unique 返回新结尾
    printf("去重后：");
    for (int x : v) printf("%d ", x);                          // 1 2 3 5
    printf("\n");

    // 2. 不删元素，只取逻辑结尾：适合只需要「去重后的序列」
    vector<int> w = {1, 1, 2, 2, 2, 3};
    auto newEnd = unique(w.begin(), w.end());
    printf("不同元素个数 = %d\n", (int)(newEnd - w.begin()));    // 3
    printf("逻辑区间内容：");
    for (auto it = w.begin(); it != newEnd; ++it) printf("%d ", *it);
    printf("\n");
    printf("容器实际大小未变：%d（尾部是残留值）\n", (int)w.size());

    // 3. 离散化：把大范围的值映射成小下标（算法专题阶段 1 的核心技巧）
    int raw[] = {1000000000, 5, 999999999, 5, 7};
    vector<int> sorted(raw, raw + 5);
    sort(sorted.begin(), sorted.end());
    sorted.erase(unique(sorted.begin(), sorted.end()), sorted.end());
    printf("离散化后共 %d 个不同值：", (int)sorted.size());
    for (int x : sorted) printf("%d ", x);
    printf("\n");
    // 查任意值映射到几号
    int query = 999999999;
    int id = lower_bound(sorted.begin(), sorted.end(), query) - sorted.begin();
    printf("%d 映射到下标 %d\n", query, id);

    // 4. 字符串去重相邻重复字符（不排序时只去相邻）
    string s = "aabbcccd";
    // unique 对 string 同样适用
    s.erase(unique(s.begin(), s.end()), s.end());
    printf("相邻去重后：%s\n", s.c_str());                     // "abcd"

    // 5. 自定义去重规则：用 lambda 判断「是否相等」
    vector<int> x = {1, 3, 5, 7, 9};
    // 把所有「相差不超过 2」的视为重复
    x.erase(unique(x.begin(), x.end(), [](int a, int b) {
        return b - a <= 2;                                     // 返回 true 表示「视为重复」
    }), x.end());
    printf("按差值 <=2 去重后：");
    for (int t : x) printf("%d ", t);
    printf("\n");
    return 0;
}
```

> **【易错】** 五处：
> 1. **不排序直接 `unique`** —— 只能去掉相邻的重复。`{1,2,1}` 去重后仍是 `{1,2,1}`。
> 2. **忘了 `erase`** —— `unique` 不改容器大小，尾部留着「已失效」的残留值。
>    **记忆：`unique` 只搬家不裁房，`erase` 才退租。**
> 3. **`unique` 后继续用旧 `end()`** —— 逻辑结尾已变，用旧 `end()` 会把残留值当有效数据。
> 4. **自定义 lambda 的语义搞反** —— 它返回「是否视为相等」（`true` = 算重复），不是「是否不同」。
> 5. **对 `set` 用 `unique`** —— `set` 本身已去重，不需要。

> **【类比】** `unique` 像把一排书里相邻的重复本子抽出来插到书架末尾，
> 但**书架的格数没变**——你要自己把末尾那几格拆掉（`erase`）。

> **【记忆】** **排序 → `unique` → `erase`**，三步不能少；`unique` 返回新结尾。

**关联**

- `[前置]` 见 D-1 `sort`、C-1 `vector`。
- `[后续]` 见 D-3 `lower_bound`（离散化后按值查下标）、算法专题阶段 1「离散化」。
- `[组合]` 与 D-3 组合 → **离散化三步：排序 + 去重 + 二分查找映射**。
  这是树状数组处理大值域问题的前置步骤。
- `[易混]` `unique` 与 `set`：前者适用于一次性批处理，后者适用于边插边去重。

---

### D-5　`reverse` / `fill` / `swap` / `min` / `max`　`P0`　熟练　`[未学]`

> **【重点】** 这五个是**最小但最常用**的一组。`reverse` 与 `fill` 现有代码中零使用，
> 而 `fill` 是初始化多维数组的唯一干净写法。

**是什么**：五个基础操作工具函数。

| 函数 | 作用 | 区间语义 | 常用场景 |
|------|------|---------|---------|
| `reverse(b, e)` | 反转区间 | `[b, e)` | 字符串反转、反向遍历 |
| `fill(b, e, v)` | 填充为 v | `[b, e)` | 初始化数组、重置 DP 数组 |
| `swap(a, b)` | 交换两个值 | — | 交换、优先队列的堆操作替代 |
| `min(a, b)` / `max(a, b)` | 取小/大 | 两值 | 全程高频 |
| `min({a,b,c,...})` | 多值取小 | 初始化列表 | 三值以上 |

**为什么**：`fill` 与 `memset` 的区别是关键 ——
**`memset` 按字节填充，只能安全地填 0 和 -1（以及 `0x3f` 这类特殊值）**；
`fill` 按元素填充，填任何值都正确。用它初始化「值为 10⁹ 的 DP 数组」是唯一正解。

**怎么用**：

1. `fill(dp, dp + n + 1, INF)` 初始化一维；多维要**按第一维逐行 fill**。
2. `reverse(s.begin(), s.end())` 反转字符串。
3. 多值取小用初始化列表：`min({a, b, c})`。
4. 交换用 `swap`，不要写临时变量。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <string>
using namespace std;

const int MAXN = 10;
const int INF = 0x3f3f3f3f;                 // 模块 A-10

int dp[MAXN];
int g[4][4];

int main() {
    // 1. fill 与 memset 的关键区别
    memset(dp, 0, sizeof(dp));               // 填 0：memset 安全
    printf("memset 填 0：dp[0]=%d\n", dp[0]);

    // memset(dp, 1, sizeof(dp));  // 错误！会把每个字节填成 1，即每个 int 变成 0x01010101 = 16843009
    fill(dp, dp + MAXN, INF);                 // 填任意值：必须用 fill
    printf("fill 填 INF：dp[0]=%d\n", dp[0]); // 1061109567

    // 2. 多维数组的 fill：按行 fill（因为内存连续，也可以整体算元素数）
    for (int i = 0; i < 4; i++)
        fill(g[i], g[i] + 4, INF);            // 边界：逐行填，区间是 g[i] 到 g[i]+4
    printf("二维 fill：g[3][3]=%d\n", g[3][3]);
    // 整体填法（内存连续）也可以：
    // fill(&g[0][0], &g[0][0] + 4 * 4, INF);

    // 3. reverse：反转
    string s = "abcde";
    reverse(s.begin(), s.end());
    printf("反转后：%s\n", s.c_str());         // edcba

    int a[] = {1, 2, 3, 4, 5};
    reverse(a + 1, a + 4);                     // 边界：反转 a[1] 到 a[3]
    printf("部分反转：");
    for (int i = 0; i < 5; i++) printf("%d ", a[i]);   // 1 3 2 4 5
    printf("\n");

    // 4. swap
    int x = 3, y = 7;
    swap(x, y);
    printf("交换后 x=%d y=%d\n", x, y);

    // 5. min / max：两个值
    printf("min=%d max=%d\n", min(x, y), max(x, y));

    // 6. 多值取小 / 取大：用初始化列表
    int p = 5, q = 2, r = 9;
    printf("三值最小 %d，最大 %d\n", min({p, q, r}), max({p, q, r}));

    // 7. 常见组合：把数组反转后与自身比较判断回文
    string t = "racecar";
    string u = t;
    reverse(u.begin(), u.end());
    printf("是否回文：%d\n", (int)(t == u));   // 1
    return 0;
}
```

> **【规律】** **`memset` 只能填 0、-1、`0x3f`；其余一律用 `fill`。**
> 原因：`memset` 是按**字节**填充。`0` 的每个字节是 0，`-1` 的每个字节是 0xFF，
> `0x3f3f3f3f` 的每个字节都是 `0x3f` —— 这三个值「每个字节相同」，所以填完正好正确。
> 而 `1` 的每字节是 `0x01`，填出来是 `0x01010101`，不是 1。

> **【易错】** 五处：
> 1. **用 `memset` 填 1 或 INF 以外的值** —— 结果完全不对。见上方规律。
> 2. **`fill` 的区间写成闭区间** —— `fill(a, a+n, v)` 是 `[a, a+n)`，正好 n 个；写 `a+n-1` 会少填一个。
> 3. **多维 `fill` 只填了第一行** —— 必须逐行，或按总元素数整体填。
> 4. **`min(a, b)` 的两个参数类型不同** —— 编译失败（模板推导冲突）。要显式转换。
> 5. **用 `min` / `max` 作为变量名** —— 与 `std` 冲突，编译报错。

> **【类比】** `memset` 像**用同一枚印章盖满整页**：印章是什么图案，每个字节就都是它。
> `fill` 像**逐个格子写同一个字**：想写什么都能写对。

> **【记忆】** **`memset` 只填 0 / -1 / `0x3f`；其余用 `fill`。**

**关联**

- `[前置]` 见 A-10 `const`（INF 常量）、A-4 数组。
- `[后续]` 见算法专题阶段 7「DP 数组初始化」（`fill` 的主战场）。
- `[易混]` `memset` 与 `fill`：见上方规律，这是本模块最值得记住的一条。
- `[组合]` 与 D-6 `max_element` 组合 → 求最大值与其位置。

---

### D-6　`max_element` / `min_element` / `count` / `find`　`P1`　会用　`[未学]`

> **【重点】** 这四个都是**线性**的（O(n)）。同 C-7 的警告：
> **除了 `find`，其余在 `set` / `map` 上用都是 O(n)**，那是自废武功。

**是什么**：区间统计与查找。

| 函数 | 返回 | 复杂度 | 注意 |
|------|------|--------|------|
| `max_element(b,e)` | 最大元素的**迭代器** | O(n) | 返回迭代器，不是值 |
| `min_element(b,e)` | 最小元素的**迭代器** | O(n) | 同上 |
| `count(b,e,v)` | 等于 v 的**个数** | O(n) | 需要 `operator==` |
| `find(b,e,v)` | 第一个等于 v 的**迭代器** | O(n) | 找不到返回 `end()` |
| `count_if(b,e,pred)` | 满足条件的个数 | O(n) | 配合 lambda |

**为什么**：手写求最大值时容易忘记初始化（把 `mx` 设为 0，
结果全负数组返回 0 —— 经典错误）。`max_element` 没有这个问题。

**怎么用**：

1. 求值：`*max_element(v.begin(), v.end())`。**空区间返回 `end()`，解引用前先判。**
2. 求下标：`max_element(...) - v.begin()`。
3. 统计个数：`count(v.begin(), v.end(), x)`。
4. 条件统计：`count_if` + lambda，比手写循环清晰。
5. 配合 `auto`（模块 E-1）与结构化绑定（E-4）使用最简洁。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <vector>
#include <algorithm>
#include <string>
using namespace std;

int main() {
    vector<int> v = {3, -1, -7, 4, 4};

    // 1. 求最大/最小值：注意返回的是迭代器
    auto mx = max_element(v.begin(), v.end());
    auto mn = min_element(v.begin(), v.end());
    printf("最大值 %d（下标 %d），最小值 %d（下标 %d）\n",
           *mx, (int)(mx - v.begin()), *mn, (int)(mn - v.begin()));

    // 2. 全负数数组的经典错误
    int neg[] = {-3, -5, -1};
    int bad = 0;                                     // 错误：初始化为 0
    for (int x : neg) if (x > bad) bad = x;
    printf("手写求最大（初值 0）：%d  ← 错误！\n", bad);
    printf("max_element 的正确结果：%d\n", *max_element(neg, neg + 3));

    // 3. 统计个数
    printf("值 4 出现 %d 次\n", (int)count(v.begin(), v.end(), 4));

    // 4. 条件统计：统计正数个数
    int pos = (int)count_if(v.begin(), v.end(), [](int x) { return x > 0; });
    printf("正数有 %d 个\n", pos);

    // 5. find：找元素，找不到返回 end()
    auto it = find(v.begin(), v.end(), 4);
    if (it != v.end()) printf("找到 4，下标 %d\n", (int)(it - v.begin()));
    else printf("未找到\n");

    // 6. 在字符串里找字符
    string s = "hello";
    auto sit = find(s.begin(), s.end(), 'l');
    if (sit != s.end()) printf("'l' 首次出现在下标 %d\n", (int)(sit - s.begin()));

    // 7. 求最大值的同时记录下标：竞赛常用组合
    vector<pair<int,int>> pts = {{1, 5}, {2, 9}, {3, 2}};
    auto best = max_element(pts.begin(), pts.end(),
                            [](const pair<int,int> &a, const pair<int,int> &b) {
                                return a.second < b.second;    // 按 second 比
                            });
    printf("second 最大的点：(%d,%d)\n", best->first, best->second);

    // 8. 警告：在 set 上用这些是线性的
    printf("注意：count / find 在 set 上应改用成员函数（对数级）\n");
    return 0;
}
```

> **【易错】** 五处：
> 1. **对空区间解引用 `max_element` 的返回值** —— 返回 `end()`，解引用是 UB。
> 2. **把返回值当值用** —— 忘记加 `*`。`printf("%d", max_element(...))` 打印的是地址。
> 3. **在 `set` / `map` 上用 `std::count` / `std::find` / `std::lower_bound`** —— 全是 O(n)。
>    **必须用成员函数。**
> 4. **`count` 在 `multiset` 上是 O(log n + k)**，k 为出现次数。判存在请用 `find`。
> 5. **手写求最值忘记初始化** —— 见上方演示。

> **【类比】** `max_element` 像一个**不预设任何印象的评委**：他先看第一个选手，
> 再逐个比较。手写代码时 `int mx = 0;` 相当于**先假定「0 分是最高分」**——
> 如果所有选手都是负分，这个评委就永远不改口。

> **【记忆】** **返回迭代器，用前加 `*`；`set` 上别用全局版本。**

**关联**

- `[前置]` 见 D-5 `min` / `max`。
- `[后续]` 见 D-7 `accumulate`（同类区间算法）、E-3 lambda（`count_if` 的判据）。
- `[易混]` `max_element`（返回迭代器）与 `min` / `max`（返回值）。
- `[组合]` 与 C-8 `map` 组合 → 统计字符串中字符出现次数的最值。

---

### D-7　`accumulate`　`P1`　会用　`[未学]`

> **【重点】** `accumulate` 需要 `#include <numeric>`，**它不在 `<algorithm>` 里**。
> 且**初始值必须显式给 `0LL`**，否则按 `int` 累加会溢出（模块 A-1）。

**是什么**：求区间和，可指定初始值与自定义累加规则。

**为什么**：手写求和要写循环与累加变量；`accumulate` 一行完成，且语义明确。
它的第三个参数（初始值）还有一个隐藏作用：**决定累加的类型**。

**怎么用**：

1. `accumulate(b, e, 0)` 求和。**求和一律写 `0LL`** 以强制 `long long` 累加。
2. 求乘积：初值写 `1`。
3. 自定义：第四个参数是「累加函数」`f(acc, x)`，可做拼接、最值、异或等。
4. 求平均值：`accumulate(...) / (double)n`。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <vector>
#include <numeric>
#include <string>
using namespace std;

int main() {
    vector<int> v = {1, 2, 3, 4, 5};

    // 1. 求和：初值写 0LL 强制 long long
    long long s = accumulate(v.begin(), v.end(), 0LL);
    printf("和 = %lld\n", s);

    // 2. 溢出的对照实验
    // 构造一个「和超过 int 上限」的数组
    vector<int> big(10, 300000000);                  // 10 个 3×10^8，和 = 3×10^9 > int 上限
    int bad = accumulate(big.begin(), big.end(), 0);        // 初值 0 是 int → 按 int 累加
    long long good = accumulate(big.begin(), big.end(), 0LL); // 初值 0LL → 按 long long 累加
    printf("初值 int ：%d   ← 溢出\n", bad);
    printf("初值 0LL ：%lld ← 正确\n", good);

    // 3. 求乘积
    vector<int> small = {1, 2, 3, 4};
    long long prod = accumulate(small.begin(), small.end(), 1LL, [](long long a, int b) {
        return a * b;                                // 自定义为乘法
    });
    printf("乘积 = %lld\n", prod);                    // 24

    // 4. 自定义累加：拼接字符串
    vector<string> words = {"ab", "cd", "ef"};
    string joined = accumulate(words.begin(), words.end(), string(""),
                               [](string acc, const string &w) {
                                   return acc + w + "-";
                               });
    printf("拼接 = %s\n", joined.c_str());

    // 5. 自定义累加：求最大值（等同 max_element，但语义统一）
    vector<int> x = {-3, -9, -1};
    int mx = accumulate(x.begin(), x.end(), x[0], [](int a, int b) {
        return a > b ? a : b;
    });
    printf("最大值 = %d\n", mx);                      // -1

    // 6. 自定义累加：按位异或（竞赛常用技巧）
    vector<int> y = {5, 3, 5, 3, 7};
    int xr = accumulate(y.begin(), y.end(), 0, [](int a, int b) { return a ^ b; });
    printf("异或和 = %d（出现奇数次的数）\n", xr);     // 7

    // 7. 平均值
    printf("平均值 = %.2f\n", (double)s / v.size());
    return 0;
}
```

> **【易错】** 四处：
> 1. **初值写 `0` 而非 `0LL`** —— 溢出（见上方对照实验）。**这是本知识点最重要的坑。**
> 2. **以为它在 `<algorithm>` 里** —— 需要 `#include <numeric>`，否则编译失败。
> 3. **忘记第四个参数时想自定义** —— 默认是 `+`。
> 4. **对 `vector<double>` 求和使用整数初值** —— 结果会被截断成整数累加。

> **【类比】** `accumulate` 的初值像**计算器的起始数字**：你从 0 开始按，
> 得到的是整数；从 0.0 开始按，得到的是小数。**起始类型决定全程类型。**

> **【记忆】** **`accumulate` 要 `#include <numeric>`；求和初值写 `0LL`。**

**关联**

- `[前置]` 见 A-1 整型与溢出（本条的核心依据）。
- `[后续]` 见 D-6（同类区间算法）、算法专题阶段 1「前缀和」（`accumulate` 是它的库函数版）。
- `[易混]` `accumulate` 与手写循环求和：前者更快读懂，后者便于中途 `break`。
- `[组合]` 与 D-4 组合 → 去重后求和的统计场景。

---

### D-8　`next_permutation` / `prev_permutation`　`P1`　会用　`[未学]`

> **【重点】** `next_permutation` **要求区间已按升序排好**，否则只能枚举出「从当前排列开始」的部分。

**是什么**：把区间改成「字典序的下一个排列」，返回是否成功。

**为什么**：全排列枚举在暴力搜索、TSP 小规模、排列型枚举中常用。
手写全排列要写递归 + `used` 数组，`next_permutation` 用两行完成。

**怎么用**：

1. **先 `sort`**，保证从最小排列开始，才能枚举全部。
2. 用 `do { ... } while (next_permutation(b, e));` —— **必须用 `do-while`**，
   因为 `while` 会跳过初始排列。
3. 返回值：还有下一个排列返回 `true`，已到最后一个（降序）返回 `false`。
4. `prev_permutation` 反向，需先降序排列。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <algorithm>
#include <vector>
#include <string>
using namespace std;

int main() {
    // 1. 枚举全部排列：必须先排序
    vector<int> v = {3, 1, 2};
    sort(v.begin(), v.end());                  // 关键：从最小排列 {1,2,3} 开始
    printf("全部排列（%d 个）：\n", 6);
    int cnt = 0;
    do {
        printf("  ");
        for (int x : v) printf("%d", x);
        printf("\n");
        cnt++;
    } while (next_permutation(v.begin(), v.end()));   // do-while 不能写成 while
    printf("共 %d 个\n", cnt);

    // 2. 为什么必须用 do-while：while 会跳过第一个排列
    vector<int> w = {1, 2, 3};
    printf("用 while 会漏掉第一个：");
    while (next_permutation(w.begin(), w.end())) printf("有输出则说明没漏\n");
    // 上面循环里 w 已经从 {1,2,3} 变成了 {1,3,2}，第一个排列被跳过

    // 3. 对 string 同样适用（字符的字典序）
    string s = "abc";
    printf("字符串排列：");
    do { printf("%s ", s.c_str()); } while (next_permutation(s.begin(), s.end()));
    printf("\n");

    // 4. 应用：小规模 TSP（最多 8 个点）暴力枚举最短路径
    int n = 4;
    int d[4][4] = {                            // 距离矩阵（对称）
        {0, 2, 9, 10},
        {2, 0, 6, 4},
        {9, 6, 0, 3},
        {10, 4, 3, 0}
    };
    vector<int> path;
    for (int i = 1; i < n; i++) path.push_back(i);   // 固定起点 0，排列其余点
    sort(path.begin(), path.end());
    int best = 1 << 30;                              // 一个足够大的初值
    do {
        int cost = d[0][path[0]];
        for (int i = 0; i + 1 < (int)path.size(); i++) cost += d[path[i]][path[i + 1]];
        cost += d[path.back()][0];                   // 回到起点
        if (cost < best) best = cost;
    } while (next_permutation(path.begin(), path.end()));
    printf("TSP 最短回路 = %d\n", best);

    // 5. 降序排列与 prev_permutation
    vector<int> u = {3, 2, 1};
    sort(u.begin(), u.end(), greater<int>());        // 先降序
    printf("逆序枚举：");
    do { printf("%d%d%d ", u[0], u[1], u[2]); }
    while (prev_permutation(u.begin(), u.end()));
    printf("\n");
    return 0;
}
```

> **【易错】** 四处：
> 1. **不排序就用 `next_permutation`** —— 只能枚举「从当前排列之后」的部分。
>    例如 `{3,1,2}` 不排序直接枚举，会漏掉 `{1,2,3}`、`{1,3,2}`。
> 2. **用 `while` 而非 `do-while`** —— 漏掉初始排列。
> 3. **以为它能处理有重复元素的「不同排列」** —— 它能自动跳过重复排列，
>    这是优点；但若要枚举「所有位置排列」就不能用它。
> 4. **复杂度误判** —— O(n!) 级，n 超过 10 就基本不可行。**n ≤ 8 是安全范围，n = 10 已接近极限。**

> **【类比】** `next_permutation` 像字典翻页：**必须从第一页开始翻**（先排序），
> 否则你从中间翻开，前面几页永远看不到。

> **【记忆】** **先 `sort`，用 `do-while`，n 别超过 10。**

**关联**

- `[前置]` 见 D-1 `sort`、D-2 比较器。
- `[后续]` 见算法专题阶段 4「搜索枚举」（全排列枚举是搜索的入门手段）。
- `[易混]` `next_permutation` 与递归回溯枚举：前者代码短但只能顺序枚举、无法剪枝；
  后者可剪枝，适合需要中途判断的场景。
- `[组合]` 与 F-3 对拍组合 → 小规模证伪时用全排列枚举暴力。

---

### D-9　`nth_element` / `partial_sort`　`P2`　会用　`[未学]`

> **【重点】** 只要「第 k 大」而不要「全部有序」时，用它们能把 O(n log n) 降到 **O(n)**。

**是什么**：
- `nth_element`：把第 k 个位置放上「正确顺序下该在那里的元素」，比它小的都在左边，大的都在右边（**两侧内部无序**）。
- `partial_sort`：把前 k 个排好序，后面不管。

| 需求 | 函数 | 复杂度 |
|------|------|--------|
| 全部有序 | `sort` | O(n log n) |
| 前 k 个有序 | `partial_sort` | O(n log k) |
| 第 k 小（第 k 大） | `nth_element` | **平均 O(n)** |
| 前 k 个（不要求有序） | `nth_element` 后取前 k 个 | O(n) |

**为什么**：求「第 k 大」若用 `sort`，是 O(n log n)。n = 10⁷ 时前者约 2×10⁸ 次操作，
后者约 10⁷ —— 差一个数量级，可能就是 TLE 与 AC 的分界。

**怎么用**：

1. `nth_element(b, b + k, e)` 后，`*(b + k)` 就是第 k 小（0 起始），左侧都不大于它。
2. **注意是 0 起始**：第 1 小是 `b + 0`，第 k 小是 `b + k - 1`。
3. 求第 k 大：用 `greater<int>()`，或改求第 `n - k` 小。
4. `partial_sort(b, b + k, e)` 后前 k 个有序。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<int> v = {9, 3, 7, 1, 8, 2, 6, 4, 5};

    // 1. nth_element：第 3 小（0 起始下标 2）
    vector<int> a = v;
    nth_element(a.begin(), a.begin() + 2, a.end());
    printf("第 3 小 = %d\n", a[2]);
    printf("左侧都不大于它：");
    for (int i = 0; i < 2; i++) printf("%d ", a[i]);
    printf("\n（注意左侧内部无序，只保证都不大于 a[2]）\n");

    // 2. 第 k 大的两种写法
    vector<int> b = v;
    int k = 4;
    // 写法一：用 greater 直接求第 k 大（0 起始 k-1）
    nth_element(b.begin(), b.begin() + k - 1, b.end(), greater<int>());
    printf("第 %d 大（写法一）= %d\n", k, b[k - 1]);
    // 写法二：第 k 大 = 第 n-k+1 小
    vector<int> c = v;
    int n = (int)c.size();
    nth_element(c.begin(), c.begin() + (n - k), c.end());
    printf("第 %d 大（写法二）= %d\n", k, c[n - k]);

    // 3. 只要前 k 小（不要求有序）：nth_element 后取前 k 个，O(n)
    vector<int> d = v;
    int kk = 3;
    nth_element(d.begin(), d.begin() + kk, d.end());
    printf("最小的 %d 个（无序）：", kk);
    for (int i = 0; i < kk; i++) printf("%d ", d[i]);
    printf("\n");

    // 4. partial_sort：前 k 个有序
    vector<int> e = v;
    partial_sort(e.begin(), e.begin() + kk, e.end());
    printf("最小的 %d 个（有序）：", kk);
    for (int i = 0; i < kk; i++) printf("%d ", e[i]);
    printf("\n");

    // 5. 选出前 k 小且要求有序时的复杂度对比
    //    sort       O(n log n)
    //    partial_sort O(n log k)
    //    nth_element + 内部排序 O(n + k log k)
    printf("n=%d 时：sort 需 nlogn，partial_sort 需 nlogk（k=%d）\n", n, kk);
    return 0;
}
```

> **【易错】** 四处：
> 1. **把 `nth_element` 的第二个参数当 1 起始** —— 它是 `begin() + k`，0 起始。
>    求第 1 小是 `begin()`，不是 `begin() + 1`。
> 2. **以为 `nth_element` 后两侧有序** —— **两侧内部无序**，只是分区正确。
> 3. **需要前 k 个有序却用了 `nth_element`** —— 要改用 `partial_sort`。
> 4. **求第 k 大时忘记用 `greater`** —— 得到的是第 k 小。

> **【类比】** `nth_element` 像**班级排名只找第 10 名**：把队伍按身高大致分成两拨，
> 第 10 个位置站的就是第 10 高。**两拨内部怎么站，它不管。**

> **【记忆】** **`nth_element` 第二个参数是 `begin()+k`（0 起始），两侧无序。**

**关联**

- `[前置]` 见 D-1 `sort`（对比复杂度）。
- `[后续]` 见算法专题阶段 1「二分答案」（同属「不排序也能定位」的思路）。
- `[易混]` `nth_element` 与 `sort`：前者 O(n) 但只有分区，后者 O(n log n) 但全序。
- `[组合]` 与 D-3 `lower_bound` 组合 → 先分区再二分（少见，但思路统一）。

---

### D-10　`__builtin_` 系列　`P1`　会用　`[未学]`

> **【重点】** 这是 **GCC / Clang 的内置函数**，直接映射到 CPU 指令，比手写循环快数倍。
> 现有代码中仅出现 3 次。**注意：它不是标准 C++，MSVC 不支持。**
> 现在也有标准版本（C++20 的 `<bit>`），但 OJ 多支持 `__builtin_`。

**是什么**：编译器提供的一批位运算函数，直接编译成单条 CPU 指令。

| 函数 | 含义 | 复杂度 | 等价的手写 |
|------|------|--------|-----------|
| `__builtin_popcount(x)` | 二进制中 1 的个数 | O(1)（单指令） | 循环 `x &= x-1` |
| `__builtin_clz(x)` | 前导 0 的个数 | O(1) | 循环移位 |
| `__builtin_ctz(x)` | 末尾 0 的个数 | O(1) | lowbit 后取对数 |
| `__builtin_parity(x)` | 1 的个数的奇偶 | O(1) | popcount 后取模 2 |
| `__builtin_popcountll(x)` | `long long` 版本 | O(1) | 同上 |
| `__builtin_ffs(x)` | 最低位 1 的位置（1 起始） | O(1) | `ctz(x) + 1` |

**为什么**：手写 `popcount` 要 O(log n) 次循环；`__builtin_popcount` 是一条指令。
在状压 DP、子集枚举、位计数题里，这个差距会累积成数量级。

**怎么用**：

1. `popcount` 用于**统计集合大小**（状压 DP 中的状态位数）。
2. `ctz` 用于**枚举集合中的每个元素**（配合 `x &= x - 1`）。
3. `clz` 用于**求整数的二进制长度**：`32 - clz(x)`。
4. **必须处理 `x = 0`**：`clz(0)` 与 `ctz(0)` 是**未定义行为**（返回值依平台而异）。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>

int main() {
    int x = 0b101100;                    // 二进制：44

    // 1. 统计 1 的个数
    printf("popcount(44) = %d\n", __builtin_popcount(x));      // 3

    // 2. 末尾 0 的个数：等价于 lowbit 的位置
    printf("ctz(44) = %d\n", __builtin_ctz(x));                 // 2（44 = ...101100）

    // 3. 前导 0 的个数 → 求二进制长度
    printf("clz(44) = %d，二进制长度 = %d\n",
           __builtin_clz(x), 32 - __builtin_clz(x));            // 26, 6

    // 4. 奇偶性
    printf("parity(44) = %d（1 的个数为奇数则 1）\n", __builtin_parity(x)); // 1

    // 5. 最低位 1 的位置（1 起始）
    printf("ffs(44) = %d\n", __builtin_ffs(x));                 // 3

    // 6. long long 版本：必须用 ll 后缀版本，否则高位丢失
    long long big = 1LL << 40;
    printf("popcountll(2^40) = %d\n", __builtin_popcountll(big)); // 1

    // 7. 典型应用：枚举集合的所有元素（状压 DP 常用）
    int mask = 0b101101;
    printf("集合中的元素下标：");
    for (int t = mask; t; t &= t - 1) {
        printf("%d ", __builtin_ctz(t));    // 每次取最低位 1 的下标
    }
    printf("\n");

    // 8. 典型应用：枚举所有子集（子集枚举的标准模板）
    printf("mask 的全部子集：");
    for (int sub = mask; sub; sub = (sub - 1) & mask) {
        printf("%d ", sub);                  // 边界：sub=0 由循环条件排除
    }
    printf("0\n");

    // 9. 危险：对 0 使用 clz / ctz 是未定义行为
    int zero = 0;
    printf("（不要对 0 调用 clz/ctz，返回值依平台而异）\n");
    if (zero == 0) printf("先判 0 再调用是正确做法\n");
    return 0;
}
```

> **【易错】** 五处：
> 1. **对 0 调用 `clz` / `ctz`** —— 未定义行为。**必须先判 0。**
> 2. **`long long` 用了 `__builtin_popcount`** —— 高 32 位被忽略。**必须用 `ll` 版本。**
> 3. **以为它是标准 C++** —— MSVC 不支持。若某 OJ 用 MSVC 会编译失败。
> 4. **`clz` 的返回值随类型变化** —— `int` 是 32 位基准，`long long` 是 64 位基准。
> 5. **`ffs` 是 1 起始，`ctz` 是 0 起始** —— 两者差 1，容易混。

> **【类比】** `popcount` 像**数一张打孔卡上有几个孔**：人是一个一个数，
> CPU 是**一眼扫过去同时点亮所有孔**——这就是单指令与循环的差别。

> **【记忆】** **`popcount` 数 1，`ctz` 找最低位 1，对 0 调用是雷区，`long long` 要用 `ll` 版本。**

**关联**

- `[前置]` 见 A-5 位运算（`lowbit`、`x &= x - 1`）。
- `[后续]` 见算法专题阶段 7「状压 DP」（子集枚举的标准模板）。
- `[易混]` `__builtin_popcount` 与 C++20 的 `std::popcount`（`<bit>` 头）。
- `[组合]` 与 A-5 组合 → 集合枚举；与 C-9 `bitset` 组合 → 大位宽集合的统计。
- `[延伸]` 子集枚举 `for (sub = mask; sub; sub = (sub-1) & mask)` 的总复杂度是 O(3ⁿ)，
  是状压 DP 优化中最高频的一句模板。

---

## 四、跨章关联地图

| 关联知识点 | 关系 | 说明 | 位置 |
|-----------|------|------|------|
| `vector` / `pair` / `set` / `map` | `[前置]` | 全部算法的操作对象 | 模块 C |
| 结构体与 `operator<` | `[前置]` | 比较器的基础 | 模块 A-7 |
| 整型与溢出 | `[前置]` | `accumulate` 初值必须 `0LL` 的依据 | 模块 A-1 |
| 位运算 | `[前置]` | `__builtin_` 的基础 | 模块 A-5 |
| `auto` / 范围 for | `[组合]` | 遍历与接收算法返回值的最简写法 | 模块 E-1、E-2 |
| lambda | `[组合]` | 比较器与 `count_if` 判据的就地写法 | 模块 E-3 |
| 二分答案 | `[延伸]` | `lower_bound` 的推广 | 算法专题阶段 1 |
| 离散化 | `[组合]` | 排序 + 去重 + 二分三步 | 算法专题阶段 1 |
| LIS 的 nlogn 解法 | `[组合]` | `lower_bound` 的直接应用 | 算法专题阶段 7 |
| 状压 DP | `[组合]` | `__builtin_popcount` 与子集枚举 | 算法专题阶段 7 |
| 对拍 | `[组合]` | 全排列枚举做小规模暴力 | 模块 F-3 |

**本模块在知识体系中的位置**

```text
竞赛 C++ 五阶段
├─ 阶段 1 语言基础与输入输出   （模块 A、B）
├─ 阶段 2 STL 容器            （模块 C）
├─ 阶段 3 STL 算法            ◄── 本模块
│   ├─ 排序类：  D-1 sort / D-2 比较器 / D-9 nth_element
│   ├─ 查找类：  D-3 lower_bound / D-6 count·find
│   ├─ 变换类：  D-4 unique / D-5 reverse·fill / D-7 accumulate
│   ├─ 枚举类：  D-8 next_permutation
│   └─ 位运算类：D-10 __builtin_
├─ 阶段 4 现代语法糖          （模块 E）
└─ 阶段 5 竞赛工程化          （模块 F）
```

---

## 五、本章总结

### 5.1 核心内容（一页纸）

1. **`sort` 区间是左闭右开**；1 起始数组写 `sort(a + 1, a + n + 1)`。
2. **比较器里只允许 `<`（或 `>`），永远不出现 `<=`**，否则行为未定义。
3. **比较器参数一律 `const &`**，大结构体传值会明显变慢。
4. **`lower_bound` 含等号，`upper_bound` 不含**；`set` / `map` 必须用**成员函数**。
5. **`unique` 只去相邻重复，必须先排序**；它不改容器大小，要接 `erase`。
6. **`memset` 只能填 0、-1、`0x3f`**；其余一律用 `fill`。
7. **`fill` 的区间是 `[b, b+n)`**，多维要逐行填或按总元素数填。
8. **`max_element` / `min_element` 返回迭代器**，用前加 `*`；空区间返回 `end()`。
9. **`accumulate` 在 `<numeric>` 里；求和初值写 `0LL`**，否则按 `int` 累加溢出。
10. **`next_permutation` 必须先 `sort`，且必须用 `do-while`**；n 超过 10 基本不可行。
11. **`nth_element` 的第二个参数是 `begin()+k`（0 起始）**，且两侧内部无序。
12. **`__builtin_` 对 0 调用 `clz` / `ctz` 是未定义行为**；`long long` 要用 `ll` 版本。
13. **三处组合模板**：离散化 = 排序 + 去重 + 二分；LIS = `lower_bound` 替换；
    子集枚举 = `sub = (sub-1) & mask`。

### 5.2 知识点串联图

```text
D-1 sort ──┬── D-2 比较器 ──────────┬── D-8 next_permutation
           │                        └── D-9 nth_element
           ├── D-3 lower_bound ────── D-4 前的必要条件
           └── D-4 unique + erase
                    │
                    └── 离散化三步：sort → unique → lower_bound

D-5 reverse / fill / min / max ──┬── D-6 max_element / count / find
                                 ├── D-7 accumulate
                                 └── D-10 __builtin_
```

### 5.3 自测清单

- [ ] 能写出 1 起始数组的 `sort` 区间写法
- [ ] 能说出为什么比较器不能用 `<=`
- [ ] 能默写 `lower_bound` / `upper_bound` 的四个边界语义
- [ ] 能默写去重三步，并解释 `unique` 为什么必须接 `erase`
- [ ] 能说出 `memset` 的三个安全填充值及原因
- [ ] 能说出 `max_element` 返回的是迭代器还是值
- [ ] 能写出 `accumulate` 防溢出的初值写法
- [ ] 能默写全排列枚举的两行代码，并说明为什么用 `do-while`
- [ ] 能说出 `nth_element` 的复杂度与两侧是否有序
- [ ] 能默写离散化的三行代码
- [ ] 能默写子集枚举的循环头

### 5.4 间隔重复表

| 知识点 | 首次 | +1 天 | +3 天 | +7 天 | +21 天 |
|--------|------|-------|-------|-------|--------|
| D-1 `sort` 与比较规则 |  |  |  |  |  |
| D-2 比较器的三种写法 |  |  |  |  |  |
| D-3 `lower_bound` / `upper_bound` |  |  |  |  |  |
| D-4 `unique` + `erase` |  |  |  |  |  |
| D-5 `reverse` / `fill` / `swap` / `min` / `max` |  |  |  |  |  |
| D-6 最值与统计函数 |  |  |  |  |  |
| D-7 `accumulate` |  |  |  |  |  |
| D-8 全排列枚举 |  |  |  |  |  |
| D-9 `nth_element` / `partial_sort` |  |  |  |  |  |
| D-10 `__builtin_` 系列 |  |  |  |  |  |

### 5.5 应落到实处的代码修改

| 问题 | 依据 | 建议 |
|------|------|------|
| `lower_bound` 仅 1 次 | 75 文件统计 | 二分题、LIS、离散化改用 `lower_bound`，见 D-3 |
| `unique` 零使用 | 75 文件统计 | 去重与离散化改用三步法，见 D-4 |
| `reverse` / `fill` 零使用 | 75 文件统计 | 反转与初始化改用标准函数；`memset` 填非 0/-1 处全部改 `fill` |
| lambda 比较器零使用 | 75 文件统计 | 单处使用的比较器改为就地 lambda，见 D-2 |
| `__builtin_` 仅 3 次 | 75 文件统计 | 位计数与子集枚举改用内置函数，见 D-10 |

---

## 六、本节未包含的内容

| 内容 | 归属 | 说明 |
|------|------|------|
| 各算法的实现原理（快排分治、堆调整） | `03_常规课程` | 竞赛只需知道复杂度与用法 |
| 自定义迭代器与算法适配 | `03_常规课程` | 竞赛不需要 |
| 并行算法（`<execution>`） | `03_常规课程` | OJ 不支持 |
| C++20 的 Ranges 写法 | `03_常规课程` | 多数 OJ 编译器版本不够 |

> **【注意】** 上述内容指向 `03_常规课程`，**本轮未生成**。

---

## 七、复习记录

| 日期 | 复习方式 | 本次结果 | 掌握状态变更 |
|------|---------|---------|-------------|
|  |  |  |  |

---

## 八、待办与缺口

- [ ] 待补知识点：无（本模块已覆盖方案 §1.2 定义的全部 10 个知识点）
- [ ] **待补：`set` / `map` 的成员函数版本二分**
      已写在 D-3 的易错 2 与 C-7 的易错 1，两处呼应，不单列知识点。
- [ ] 待修正的既有代码：见 §5.5 的五项
- [ ] 待核实的题源：本模块为算法工具用法，**不单独出题**。
      练习分散在算法专题阶段 1（二分、离散化、LIS）、阶段 7（状压 DP）的题集中。

---
## 配套题库练习

| 题号 | 题名 | 状态 |
|------|------|------|
| luogu-P1177 | 排序 | 未做 |
| luogu-P2249 | 查找 | 未做 |
| luogu-P1059 | 明明的随机数 | 未做 |
| luogu-P1706 | 全排列问题 | 未做 |
| luogu-P1012 | 拼数（自定义比较器） | 未做 |
| luogu-P1923 | 求第 k 小的数（nth_element） | 未做 |
| luogu-P1047 | 校门外的树（fill / 差分标记） | 未做 |
| luogu-P5718 | 找最小值（min_element） | 未做 |

> 题面链接见 `_题库总表.md`（单一真源，此处只列题号）；做题后回总表更新状态，「已通过」须在 `03_题库` 的 `代码` 目录留存代码文件。

---

*模块 D 完 · 学习顺序见 `README_模块总览与学习顺序.md` · 排版规范见 `22_排版与标注规范.md`*
