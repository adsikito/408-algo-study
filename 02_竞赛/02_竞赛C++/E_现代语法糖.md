# 模块 E　现代语法糖

> **元信息**
> 优先级：`P0`　｜　所属子分类：`02_竞赛\02_竞赛C++`　｜　学习顺序：五阶段中的**阶段 4**
> 前置：模块 A（结构体、函数、引用）、模块 C（容器与迭代器）
> 后续：模块 F（竞赛工程化与技巧）
> 最近复习：未开始　｜　整体掌握：`[未学]`

> **图例**
> **重要程度**：`P0` 必掌握（加粗 + 主色）｜`P1` 需熟练（次色）｜`P2` 了解即可（弱化色）
> **内容类型**：定义概念｜模板公式｜例题自测｜易错陷阱｜通俗类比｜补充延伸
> **掌握状态**：`[未学]` `[学过]` `[会做]` `[易错]` `[掌握]`（纯文字，不着色）
> 说明：颜色仅用于加速定位，**信息一律由文字标签与字重承载**，黑白打印不丢信息。

---

## 零、这个模块不提升算法能力，它只做两件事

> **【重点】** 本模块**唯一**的收益是：**代码更短、写得更快、错得更少。**

这也是它排在阶段 4 的原因 —— 它不是「必须会才能做题」的知识，
而是「会让做题变快」的知识。但恰恰因为如此，它最容易**见效**：

| 收益方向 | 具体表现 | 依据 |
|---------|---------|------|
| 编码速度 | 不再手写类型名、不再手写下标循环 | `auto` + 范围 for |
| 出错率 | 下标越界类错误归零 | 范围 for |
| 代码长度 | 比较器、判据函数就地写，不用另起函数 | lambda |
| 可读性 | 图论代码中三元组解包不再需要 `.first.second` | 结构化绑定 |
| 表达能力 | 自定义类型能直接排序、入 `set` / `map` | 运算符重载 |

### 0.1 现有代码的实测缺口

对竞赛代码（`资料\03_算法集训\` 下 **75 个 `.cpp`**）统计（2026-09-12 快照）：

| 特性 | 出现次数 | 判定 |
|------|---------|------|
| `auto` | **0** | **完全未使用** |
| lambda（`[` `]`） | **0** | **完全未使用** |
| `operator<` | **0** | **完全未使用** |
| 结构化绑定 | **0** | **完全未使用** |
| 范围 for（`for (x : v)`） | 少数 | 使用不足 |

**结论：本模块是六大模块中缺口最大的一个，四项为零。**
这也解释了为什么现有代码普遍比必要长度多出 30% 以上，
且「手写下标循环」类错误反复出现。

---

## 一、本章速览

**一句话概括**：用九个 C++11/17 特性把代码变短变稳，每一项都能对应到一类具体错误的消失。

| 序 | 知识点 | 优先级 | 深度 | 掌握 | 前置 |
|----|--------|--------|------|------|------|
| 1 | `auto` 类型推导 | P0 | 熟练 | `[未学]` | — |
| 2 | 范围 for | P0 | 熟练 | `[未学]` | 1 |
| 3 | lambda 表达式与捕获 | P0 | 熟练 | `[未学]` | 2 |
| 4 | 结构化绑定 | P1 | 熟练 | `[未学]` | 1、2 |
| 5 | `if` 初始化语句 | P2 | 会用 | `[未学]` | — |
| 6 | `constexpr` | P2 | 会用 | `[未学]` | — |
| 7 | 函数模板基础 | P1 | 会用 | `[未学]` | 1 |
| 8 | 运算符重载 | P0 | 熟练 | `[未学]` | — |
| 9 | 引用与移动语义 | P2 | 理解 | `[未学]` | 8 |

> 「序」即学习先后顺序。`operator<`（第 8）虽然独立于前七项，但它与模块 C 的 `set` / `map` 强耦合，
> 必须在本模块内学会，否则模块 C 的关联容器无法用于自定义类型。

---

## 二、前置检查

| 前置知识点 | 出处 | 自测 |
|-----------|------|------|
| 迭代器与 `begin` / `end` | 模块 C-1 | - [ ] 能说清 `v.begin()` 指向哪里 |
| `pair` 的 `.first` / `.second` | 模块 C-3 | - [ ] 能写出遍历 `vector<pair>` 的循环 |
| 结构体与函数 | 模块 A-7、A-6 | - [ ] 能定义结构体并在函数间传递 |
| 引用传参 | 模块 A-6 | - [ ] 知道 `const T &` 与 `T &` 的区别 |

> 任何一项未打钩，先回补该前置。**本模块的每一项都在简化「容器 + 迭代器」的写法。**

---

## 三、知识点逐讲

### E-1　`auto` 类型推导　`P0`　熟练　`[未学]`

> **【重点】** `auto` 让编译器**从初始化表达式推导类型**。
> 它省掉的是「写类型名」，不是「写类型」——**类型依然存在且必须正确**。

**是什么**：`auto x = 表达式;` 中，`x` 的类型由表达式决定。

**为什么**：竞赛里长类型名遍地都是：

```cpp
map<string, vector<pair<int,int>>>::iterator it = m.begin();   // 手写类型名
auto it = m.begin();                                           // 同一个东西
```

后者不仅短，而且**改容器时不用改声明**（改 `map` 为 `unordered_map`，`auto` 无需修改）。

**怎么用**：

1. 迭代器：`for (auto it = v.begin(); it != v.end(); ++it)`。
2. 接收函数返回值：`auto best = max_element(v.begin(), v.end());`。
3. **要修改原值必须写 `auto&`**；只读用 `const auto&`；拷贝用 `auto`（**谨慎**）。
4. **`auto` 会丢掉引用与 `const`**，这是最容易踩的一点（见易错）。

| 写法 | 含义 | 何时用 |
|------|------|--------|
| `auto x = ...` | 拷贝一份 | 需要独立副本，或元素是小类型 |
| `auto &x = ...` | 引用，可改原值 | **遍历时想修改元素** |
| `const auto &x = ...` | 常量引用，不拷贝不可改 | **遍历时只读（最常用）** |
| `auto &&x = ...` | 转发引用 | 竞赛极少用 |

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <vector>
#include <map>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    vector<int> v = {3, 1, 4, 1, 5};

    // 1. 迭代器：类型名从 40 字符降到 4 字符
    map<string, vector<pair<int,int>>> m;
    m["a"].push_back({1, 2});
    auto it = m.begin();                                   // 不用写完整 iterator 类型
    printf("map 首键：%s\n", it->first.c_str());

    // 2. 接收函数返回值
    auto mx = max_element(v.begin(), v.end());
    printf("最大值：%d\n", *mx);

    // 3. 三种遍历方式的区别（核心）
    // 3.1 auto 拷贝：改的是副本
    for (auto x : v) x += 100;
    printf("auto 拷贝后 v[0]=%d（原值未变）\n", v[0]);      // 3

    // 3.2 auto& 引用：改的是原值
    for (auto &x : v) x += 100;
    printf("auto& 引用后 v[0]=%d（原值已变）\n", v[0]);      // 103

    // 3.3 const auto& 只读且不拷贝：遍历大容器时的默认选择
    long long sum = 0;
    for (const auto &x : v) sum += x;
    printf("const auto& 求和：%lld\n", sum);

    // 4. auto 丢引用的陷阱：用 auto 接收 lambda 之外的引用返回值
    vector<pair<int,int>> pv = {{1, 9}, {2, 3}};
    auto p = pv[0];          // 这是拷贝！改它不影响 pv[0]
    p.second = 999;
    printf("pv[0].second=%d（未被修改）\n", pv[0].second);   // 9
    auto &q = pv[0];         // 这才是引用
    q.second = 999;
    printf("pv[0].second=%d（已修改）\n", pv[0].second);     // 999
    return 0;
}
```

> **【易错】** 四处：
> 1. **`for (auto x : v)` 想改元素** —— 改的是副本。
>    **记忆：要改加 `&`，只读用 `const &`。**
> 2. **`auto` 与 `auto&` 在 `vector<bool>` 上的特殊行为** —— `vector<bool>` 是位压缩特化，
>    `auto x : vbool` 得到的是代理对象而非 `bool&`。**竞赛中用 `bitset` 替代 `vector<bool>`。**
> 3. **用 `auto` 推导 `size()` 得到无符号类型** —— `auto n = v.size(); if (n - 1 >= 0)` 会绕回。
>    需要 `int` 时显式写 `int n = (int)v.size();`。
> 4. **`auto` 推导出意外类型** —— 如 `auto x = 1 + 2.0;` 得到 `double`。竞赛中整数运算建议显式声明。

> **【类比】** `auto` 像**自动挡**：你不需要知道当前用几档（类型），
> 但你依然得踩对油门（初始化表达式必须正确）。**它省的是操作，不是责任。**

> **【记忆】** **遍历只读用 `const auto&`，要改加 `&`，用 `auto` 就是拷贝。**

**关联**

- `[后续]` 见 E-2 范围 for、E-4 结构化绑定、E-7 函数模板。
- `[组合]` 与模块 D 的全部算法组合：接收 `lower_bound` / `max_element` 的返回值。
- `[易混]` `auto` 与 `decltype`：前者去掉引用与顶层 `const`，后者原样保留。
- `[延伸]` `auto` 在竞赛中还有一个隐形收益：**容器类型改变时不用改代码**，
  这在与 `unordered_map` / `map` 之间切换时特别有用。

---

### E-2　范围 for　`P0`　熟练　`[未学]`

> **【重点】** 范围 for 把「下标循环」变成「元素循环」，
> **直接消灭 `i <= n` 与 `i < n` 混用、`v[i]` 越界这两类错误。**

**是什么**：`for (元素声明 : 容器) 循环体`，自动遍历容器的全部元素。

**为什么**：手写下标循环的每一次都要做三件事 —— 定初值、判边界、推进。
三处都可能错。范围 for 把这三件事全部交给编译器。

| 手写下标循环的风险 | 范围 for 是否还有风险 |
|-------------------|---------------------|
| 初值写 0 还是 1 | 无 |
| 边界写 `<` 还是 `<=` | 无 |
| 越界访问 | 无（不会越界） |
| 容器为空时 | 无（循环体不执行） |
| **需要下标本身** | **有 —— 范围 for 不提供下标** |

**怎么用**：

1. 只读遍历：`for (const auto &x : v)`。
2. 要改元素：`for (auto &x : v)`。
3. **需要下标**时不能直接用范围 for，要么改用下标循环，要么额外维护计数器。
4. 遍历 `map`：元素是 `pair`，用 `kv.first` / `kv.second`（或结构化绑定，见 E-4）。
5. 倒序遍历不支持（没有反向范围 for）。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <vector>
#include <map>
#include <string>
using namespace std;

int main() {
    vector<int> v = {3, 1, 4, 1, 5};

    // 1. 只读遍历（最常用）
    printf("只读遍历：");
    for (const auto &x : v) printf("%d ", x);
    printf("\n");

    // 2. 修改元素
    for (auto &x : v) x *= 2;
    printf("乘 2 后：");
    for (int x : v) printf("%d ", x);
    printf("\n");

    // 3. 遍历 map：元素是 pair<const K, V>
    map<string, int> score;
    score["alice"] = 90;
    score["bob"] = 85;
    printf("遍历 map：");
    for (const auto &kv : score)
        printf("%s=%d ", kv.first.c_str(), kv.second);
    printf("\n");

    // 4. 遍历二维：外层是「一行」，内层是元素
    vector<vector<int>> g = {{1, 2}, {3, 4}, {5, 6}};
    printf("遍历二维：");
    for (const auto &row : g)                 // row 是 vector<int>
        for (int x : row) printf("%d ", x);
    printf("\n");

    // 5. 需要下标时的两种应对
    printf("需要下标的场景一：额外计数器\n");
    int idx = 0;
    for (const auto &x : v) {
        printf("  v[%d]=%d\n", idx, x);
        idx++;
    }

    printf("需要下标的场景二：老老实实用下标循环\n");
    for (int i = 0; i < (int)v.size(); i++) {
        // 这里能同时用到 i 和 v[i]，还有 i-1 / i+1 的邻接关系
        if (i > 0) printf("  v[%d]-v[%d]=%d\n", i, i - 1, v[i] - v[i - 1]);
    }

    // 6. 边界：空容器不会进入循环体
    vector<int> empty;
    int cnt = 0;
    for (int x : empty) cnt++;
    printf("空容器遍历次数：%d\n", cnt);        // 0

    // 7. 不支持倒序：需要倒序只能手写反向迭代器或下标
    printf("倒序遍历：");
    for (auto it = v.rbegin(); it != v.rend(); ++it) printf("%d ", *it);
    printf("\n");
    return 0;
}
```

> **【易错】** 四处：
> 1. **在循环体里删除/插入元素** —— 迭代器失效，行为未定义。
>    **需要边遍历边删时，用下标循环从后往前，或先收集再统一删。**
> 2. **需要下标却硬用范围 for** —— 又加计数器更繁琐，不如直接下标循环。
> 3. **`for (auto x : string)` 得到的是 `char`**，想改字符要写 `for (auto &c : s)`。
> 4. **对返回临时对象的表达式做范围 for** —— C++17 起生命周期被延长，是安全的；
>    但 C++11/14 下可能悬垂。**竞赛环境一般 C++17，可放心用。**

> **【类比】** 范围 for 像**自动分页**：你不需要知道总页数，也不需要写「翻到下一页」，
> 它自己翻完就停。代价是**你拿不到页码**——需要页码时就得手动翻。

> **【记忆】** **只读 `const auto&`，要改 `auto&`；要下标就别用它。**

**关联**

- `[前置]` 见 E-1 `auto`、C-1 `vector`（迭代器）。
- `[后续]` 见 E-3 lambda（常与范围 for 配合）、E-4 结构化绑定（遍历 `map` 最简写法）。
- `[易混]` 范围 for 与下标循环：前者不含下标但更安全，后者含下标但需自己管边界。
- `[组合]` 与 C-3 `pair`、C-8 `map` 组合 → 遍历键值对的标准写法。

---

### E-3　lambda 表达式与捕获　`P0`　熟练　`[未学]`

> **【重点】** lambda 的价值是**把「规则」写在「使用点」旁边**。
> 现有代码中 lambda 零使用，而比较器全靠独立函数 —— 读者要跳来跳去看。

**是什么**：就地定义匿名函数对象。语法：`[捕获](参数) { 函数体 }`。

**为什么**：三处高频用途 ——
1. **比较器**（`sort` / `priority_queue`）：规则只用一次，不值得单开函数。
2. **判据函数**（`count_if` / `find_if`）：同上。
3. **少量代码的临时逻辑**：如递归的 DFS 内部函数。

**怎么用**：

| 捕获写法 | 含义 | 竞赛用途 |
|---------|------|---------|
| `[]` | 不捕获任何外部变量 | 纯参数运算的比较器 |
| `[&]` | 按引用捕获全部用到的外部变量 | **递归 DFS 常用**（要改全局状态） |
| `[=]` | 按值捕获全部用到的 | 只读使用外部量 |
| `[x]` | 只按值捕获 x | 精确控制 |
| `[&x]` | 只按引用捕获 x | 精确控制并需要修改 |

**返回值类型**可以自动推导；有多个 `return` 且类型不一致时会编译失败，需显式写 `-> 类型`。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <vector>
#include <algorithm>
#include <functional>
using namespace std;

int main() {
    vector<int> v = {5, 2, 8, 1, 9, 3};

    // 1. 比较器：就地写，读者不用跳转
    sort(v.begin(), v.end(), [](int a, int b) {
        return a > b;                    // 降序
    });
    printf("降序：");
    for (int x : v) printf("%d ", x);
    printf("\n");

    // 2. 判据函数：统计满足条件的个数
    int evenCnt = (int)count_if(v.begin(), v.end(), [](int x) {
        return x % 2 == 0;
    });
    printf("偶数个数：%d\n", evenCnt);

    // 3. 按值捕获：把阈值带进 lambda
    int threshold = 5;
    int above = (int)count_if(v.begin(), v.end(), [threshold](int x) {
        // 这里 threshold 是拷贝，外部改它不影响
        return x > threshold;
    });
    printf("大于 %d 的个数：%d\n", threshold, above);

    // 4. 按引用捕获：修改外部变量
    long long sum = 0;
    for_each(v.begin(), v.end(), [&sum](int x) {
        sum += x;                        // 按引用，真改外部 sum
    });
    printf("按引用捕获求和：%lld\n", sum);

    // 5. 默认按值捕获是只读的，要改必须加 mutable
    int counter = 0;
    auto f = [counter]() mutable {       // mutable 允许修改按值捕获的副本
        counter++;
        return counter;
    };
    printf("mutable：第一次 %d，第二次 %d\n", f(), f());   // 1, 2
    printf("外部 counter 未变：%d\n", counter);              // 0

    // 6. 递归 lambda：写法较重，用 std::function 包裹（性能略低）
    function<long long(int)> fib = [&fib](int n) -> long long {
        if (n <= 1) return n;            // 终止条件
        return fib(n - 1) + fib(n - 2);
    };
    printf("fib(20) = %lld\n", fib(20));

    // 7. 作为 priority_queue 的比较器：需要一个小技巧
    //    直接用 lambda 会编译失败，必须通过 decltype 取出类型
    auto cmp = [](int a, int b) { return a > b; };      // 让小的优先
    priority_queue<int, vector<int>, decltype(cmp)> pq(cmp);
    for (int x : {3, 1, 4}) pq.push(x);
    printf("lambda 比较器的小顶堆堆顶：%d\n", pq.top());   // 1

    // 8. 显式指定返回类型（多个 return 类型不一致时必须写）
    auto pick = [](int x) -> double {
        if (x > 0) return x * 1.0;
        return 0.0;
    };
    printf("显式返回类型：%.1f\n", pick(3));
    return 0;
}
```

> **【易错】** 五处：
> 1. **lambda 里要改外部变量却用了按值捕获** —— 改的是副本。
>    **记忆：要改外部量，捕获写 `&`。**
> 2. **递归 lambda 直接用 `auto`** —— 编译失败（类型推导循环）。
>    必须用 `std::function` 包裹，**代价是每次调用多一层间接寻址，性能不如普通递归函数**。
>    竞赛中优先写成普通函数。
> 3. **把 lambda 直接传给 `priority_queue` 的第三个模板参数** —— 编译失败，
>    必须写 `decltype(cmp)` 并**把 `cmp` 传进构造函数**。
> 4. **`[&]` 捕获了会销毁的局部变量** —— lambda 存活时间超过被捕获变量时悬垂。
> 5. **lambda 捕获列表里写 `[&, x]`** 是合法的（默认引用 + x 特例按值），但**容易看错**，建议写清楚。

> **【类比】** lambda 像**随手写在便签上的临时规则**：用完即弃，不必为它建一个档案（独立函数）。
> 而 `[&]` 与 `[=]` 的区别，就是**「我给你原件」与「我给你复印件」**的区别。

> **【记忆】** **要改外部量就 `[&]`；递归用 `function`；堆的比较器用 `decltype`。**

**关联**

- `[前置]` 见 E-2 范围 for、A-6 引用（捕获的本质是引用/拷贝）。
- `[后续]` 见 D-2 比较器的三种写法（lambda 是推荐写法）。
- `[易混]` lambda 与独立函数：前者就地、可捕获、类型匿名；后者可复用、可递归、性能略好。
- `[组合]` 与 `count_if` / `for_each` / `sort` / `priority_queue` 组合 —— 四处高频。
- `[延伸]` lambda 的本质是编译器生成的仿函数（`operator()` 重载），
  与模块 E-8 的运算符重载是同一套机制。

---

### E-4　结构化绑定　`P1`　熟练　`[未学]`

> **【重点】** C++17 特性。它把 `.first` / `.second` 换成有名字的变量，
> **让 `vector<pair>` 与 `vector<tuple>` 的遍历可读性提升一个档次**。

**是什么**：`auto [a, b] = 表达式;` 一次解包多个成员。

**为什么**：图论的边是三元组 `(u, v, w)`，用手写方式访问是 `e[i].first.second` 这种表达。
结构化绑定写成 `auto &[u, v, w] = e[i];`，代码直接对应数学表达。

| 手写方式 | 结构化绑定 |
|---------|-----------|
| `for (auto &p : edges) { int u = p.first.first; ... }` | `for (auto &[u, v, w] : edges) { ... }` |
| `auto kv = m.begin(); kv->first` | `auto &[k, v] = *m.begin();` |
| `p.second`（含义不明） | `w`（含义明确） |

**怎么用**：

1. 遍历 `pair`：`for (auto &[k, v] : m)`。
2. 遍历 `tuple` / `array`：`for (auto &[a, b, c] : tupleList)`。
3. **要修改原值必须写 `auto &`**。
4. 解包 `map` 的迭代器：`auto &[k, v] = *it;`。**注意 `k` 是 `const`（键不可改）。**
5. 只关心部分值：不给全部命名是不允许的，必须用 `_` 之类的占位（但仍是真变量）。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <vector>
#include <map>
#include <string>
#include <tuple>
#include <algorithm>
using namespace std;

int main() {
    // 1. 遍历 map：最典型的用法
    map<string, int> score;
    score["alice"] = 90;
    score["bob"] = 85;
    for (const auto &[name, sc] : score)
        printf("%s -> %d\n", name.c_str(), sc);

    // 2. 遍历 vector<pair>
    vector<pair<int,int>> pts = {{1, 5}, {2, 9}, {3, 2}};
    printf("坐标遍历：");
    for (const auto &[x, y] : pts) printf("(%d,%d) ", x, y);
    printf("\n");

    // 3. 修改原值必须用引用
    for (auto &[x, y] : pts) y *= 10;
    printf("y 乘 10 后：");
    for (const auto &[x, y] : pts) printf("(%d,%d) ", x, y);
    printf("\n");

    // 4. 图论：三元组边的遍历（结构化绑定收益最大的场景）
    vector<tuple<int,int,int>> edges = {{1, 2, 5}, {2, 3, 8}, {1, 3, 3}};
    printf("边表：\n");
    for (const auto &[u, v, w] : edges)
        printf("  %d --%d--> %d\n", u, w, v);

    // 5. 按边权排序：解包后比较器写得极短
    sort(edges.begin(), edges.end(), [](const auto &a, const auto &b) {
        // 用 get 取出权值所在位置（第 3 个分量）
        return get<2>(a) < get<2>(b);
    });
    printf("按权升序首条边权：%d\n", get<2>(edges[0]));

    // 6. 从 map 的迭代器解包
    auto it = score.begin();
    const auto &[k, v] = *it;
    printf("首个键值：%s=%d\n", k.c_str(), v);

    // 7. 一次解包并交换
    int a = 1, b = 2;
    // 注意：这不是结构化赋值，C++17 不支持 auto [a,b] = ... 的赋值形式
    // 交换仍用 swap
    swap(a, b);
    printf("交换后 a=%d b=%d\n", a, b);

    // 8. 解包 array
    array<int, 3> arr = {7, 8, 9};
    const auto &[p, q, r] = arr;
    printf("array 解包：%d %d %d\n", p, q, r);
    return 0;
}
```

> **【易错】** 四处：
> 1. **想修改却写 `const auto &`** —— 改不动。
> 2. **解包 `map` 后试图修改键** —— 键是 `const`，编译失败。
> 3. **变量名用了 `_` 以为能忽略** —— C++ 里 `_` 是合法变量名，但仍会创建变量并可能触发警告。
> 4. **以为是赋值** —— 结构化绑定只能用于**初始化**，不能对已有变量做结构化赋值。
>    想「重新赋值」只能逐个赋或重新解包。

> **【类比】** 结构化绑定像**把信封里的三样东西一次拿出来摆在桌上**，
> 而不是每次说「信封的第二个夹层里的第三张纸」。

> **【记忆】** **`auto &[a, b]` 加 `&` 才能改；`map` 的键解包后是 `const`。**

**关联**

- `[前置]` 见 E-1 `auto`、E-2 范围 for、C-3 `pair`。
- `[后续]` 见算法专题阶段 5 图论（边表遍历）、阶段 5 Kruskal（按边权排序）。
- `[易混]` 结构化绑定与 `tie`（C++11 的旧写法）：前者更简洁但不能用于已有变量赋值。
- `[组合]` 与 lambda 比较器组合 → 图论代码最短形式。

---

### E-5　`if` 初始化语句　`P2`　会用　`[未学]`

> **【重点】** C++17 特性。把变量声明收进 `if` 的作用域，
> **避免变量泄漏到外层，也避免「先声明再判断」的两行写法。**

**是什么**：`if (初始化; 条件) { ... }`，初始化部分可以是声明。

**为什么**：经典场景是「查找后使用」：

```cpp
auto it = m.find(k);            // 这个 it 会一直活到作用域结束
if (it != m.end()) { ... }
```

用 `if` 初始化语句后，`it` 只在 `if` 内可见，**减少命名冲突与误用**。

**怎么用**：

1. 查表后立即判断：`if (auto it = m.find(k); it != m.end())`。
2. 也适用于 `switch`。
3. **只在初始化部分能用一行表达式**，多条语句需用逗号表达式（不推荐）。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <map>
#include <string>
using namespace std;

int main() {
    map<string, int> score;
    score["alice"] = 90;

    // 1. 传统写法：it 泄漏到外层作用域
    auto it1 = score.find("alice");
    if (it1 != score.end()) printf("传统写法：%d\n", it1->second);
    // it1 在这里仍然可见，可能与后面的变量重名

    // 2. if 初始化语句：it 只在 if 内可见
    if (auto it2 = score.find("bob"); it2 != score.end()) {
        printf("找到 bob：%d\n", it2->second);
    } else {
        printf("if 初始化语句：bob 不存在\n");
        // 这里同样能访问 it2（else 分支也在同一作用域内）
        printf("  确认 it2 == end()：%d\n", (int)(it2 == score.end()));
    }
    // it2 在这里已经不可见，不会污染外层命名空间

    // 3. 与 else 链共用同一个变量
    if (int x = 5; x > 3) printf("x > 3\n");
    else printf("x <= 3\n");

    return 0;
}
```

> **【易错】** 三处：
> 1. **在 `if` 外使用该变量** —— 编译失败（作用域已结束），这是**设计意图**而非缺陷。
> 2. **误以为 `if (x = 5; ...)` 是赋值判断** —— `if (a = b)` 仍是赋值并判真假，容易写错成 `=`。
> 3. **与 `switch` 混用时的作用域** —— `switch` 的初始化部分变量在整个 `switch` 内可见。

> **【类比】** `if` 初始化语句像**一次性工牌**：只在这次判断里有效，出门即失效。
> 传统写法像**长期通行证**：用完了还挂在身上，可能被别的流程误用。

> **【记忆】** **查找 + 判断写成一行：`if (auto it = m.find(k); it != m.end())`。**

**关联**

- `[前置]` 见 E-1 `auto`。
- `[组合]` 与 C-8 `map` 组合 → 查表的标准写法。
- `[易混]` 它与普通 `if` 的区别仅在作用域，执行顺序完全相同。
- `[延伸]` 这是纯「代码卫生」特性，不影响性能与算法。

---

### E-6　`constexpr`　`P2`　会用　`[未学]`

> **【重点】** `constexpr` 表示「编译期就能算出结果」。
> 竞赛中的唯一实用场景是**数组大小与常量**，性能收益可以忽略。

**是什么**：要求表达式在编译期求值的修饰符。

| 关键字 | 含义 | 编译期确定 | 用途 |
|-------|------|-----------|------|
| `const` | 运行期不可改 | 不一定 | **数组大小（配合常量初始化）** |
| `constexpr` | 必须在编译期求值 | **一定** | 数组大小、位宽、模数 |
| `#define` | 文本替换 | — | 见 A-11，不推荐 |

**为什么**：`constexpr` 让数组大小、`bitset` 位宽等可以写在模板参数里，
且编译器能对常量表达式做更多优化。**但它对竞赛代码的实际提速近乎为零**，
主要价值是**语义清晰**与**某些模板参数的必需类型**。

**怎么用**：

1. 数组大小：`constexpr int N = 1e5 + 10;`（**注意 `1e5` 是 `double`，要写 `100000`**）。
2. `bitset` 位宽必须是编译期常量（模块 C-9），用 `constexpr` 最规范。
3. `constexpr` 函数可在编译期求值，但竞赛几乎不需要。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <bitset>
using namespace std;

// 1. 数组大小与位宽
constexpr int N = 100000 + 10;          // 不要写 1e5 + 10（那是 double）
constexpr int MOD = 1000000007;         // 取模常量
constexpr int BITS = 1005;

int a[N];
bitset<BITS> vis;                        // 位宽必须是编译期常量

// 2. constexpr 函数：编译期可求值
constexpr long long sq(int x) {
    return 1LL * x * x;                  // 1LL 防溢出（模块 A-1）
}

int main() {
    printf("N=%d MOD=%d BITS=%d\n", N, MOD, BITS);
    printf("编译期常量用在数组大小上：sizeof(a)=%d 字节\n", (int)sizeof(a));

    // 3. constexpr 函数的两种求值时机
    constexpr long long c1 = sq(1000);   // 编译期求值
    long long c2 = sq(1000);             // 也可能在运行期求值
    printf("sq(1000) = %lld（编译期） %lld（运行期或编译期）\n", c1, c2);

    // 4. 与 const 的关键区别：constexpr 可用于模板参数
    vis[0] = 1;
    printf("bitset 位宽来自 constexpr：vis[0]=%d\n", (int)vis[0]);

    // 5. 注意：const 声明的变量不一定是编译期常量，不能用作数组大小（部分编译器）
    //    int n = 10;
    //    const int sz = n;      // sz 是运行期常量
    //    int bad[sz];           // 变长数组，部分 OJ 不支持
    printf("（变长数组的示例见代码注释）\n");
    return 0;
}
```

> **【易错】** 三处：
> 1. **用 `1e5` 定义整型常量** —— `1e5` 是 `double`，赋给 `int` 有精度隐患。写 `100000`。
> 2. **以为 `const` 就能当数组大小** —— 只有编译期常量才行。
>    `const int n = 10;` 在某些上下文被当作编译期常量，但 `const int n = 运行时值;` 不行。
> 3. **期望 `constexpr` 带来性能提升** —— 编译期求值省的是「每次运行都算一次」的极小开销，
>    对竞赛题目影响可忽略。**它的价值是可读性与合法性，不是速度。**

> **【类比】** `const` 像**盖了章的合同**（不能改），`constexpr` 像**签合同之前就已经拟好的定稿**
> （连内容都在开工前就定了）。前者保证不改，后者保证「早就定了」。

> **【记忆】** **`constexpr` 用于数组大小与 `bitset` 位宽；别用 `1e5` 定义整型常量。**

**关联**

- `[前置]` 见 A-10 `const` 与 `static`。
- `[组合]` 与 C-9 `bitset` 组合 → 位宽的规范写法。
- `[易混]` `constexpr` 与 `const`：见上表。
- `[延伸]` `constexpr` 函数、`if constexpr`、`consteval` 属 C++17/20 的编译期计算体系，
  竞赛中极少使用。

---

### E-7　函数模板基础　`P1`　会用　`[未学]`

> **【重点】** 竞赛中模板的实用价值只有两处：**调试输出模板**与**泛型小工具**。
> **不要为了「通用」而写模板**——它会让编译错误变得极难读。

**是什么**：把类型参数化，一份代码适配多种类型。

**为什么**：两处真实需求 ——
1. **调试输出**：想 `print(x)` 对 `int`、`long long`、`string`、`vector` 都能用。
2. **小工具**：如「求三个数的最大值」需要同时支持 `int` 与 `long long`。

**怎么用**：

1. 单类型参数：`template<class T> T myMax(T a, T b) { return a > b ? a : b; }`。
2. **类型自动推导**：调用时通常不用写 `myMax<int>(...)`。
3. **两个不同类型会推导冲突** —— 需显式指定 `myMax<long long>(1, 2LL)`。
4. 竞赛中最实用的模板是**调试打印**（见下）。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <string>
#include <vector>
using namespace std;

// 1. 基础模板函数
template<class T>
T myMax(T a, T b) {                      // 注意：a、b 必须是同一类型
    return a > b ? a : b;
}

// 2. 显式指定返回类型：适用于「两个参数类型不同」的场景
template<class A, class B>
auto myMax2(A a, B b) -> decltype(a + b) {   // 用 a+b 的类型作为返回类型
    return a > b ? a : b;
}

// 3. 竞赛最实用：调试输出模板（支持多种类型）
template<class T>
void print(const T &x) {
    // 这里用 C++17 的 if constexpr 分类型处理
    printf("[print] 通用类型\n");
}

// 为具体类型提供特化版本（比模板更精确匹配）
void printX(int x)        { printf("[print] int    = %d\n", x); }
void printX(long long x)  { printf("[print] llong  = %lld\n", x); }
void printX(double x)     { printf("[print] double = %.6f\n", x); }

// 4. 模板化的容器打印（对 vector 通用）
template<class T>
void printVec(const vector<T> &v) {
    printf("[");
    for (size_t i = 0; i < v.size(); i++) {
        // 这是一种简易通用输出：整数与浮点都能用 %g
        printf("%g%s", (double)v[i], i + 1 < v.size() ? ", " : "");
    }
    printf("]\n");
}

int main() {
    // 模板自动推导
    printf("myMax(3, 7) = %d\n", myMax(3, 7));
    printf("myMax(3.5, 2.5) = %.1f\n", myMax(3.5, 2.5));

    // 两个不同类型：需要显式指定或换用 myMax2
    printf("myMax2(3, 7LL) = %lld\n", myMax2(3, 7LL));

    // 模板与普通函数重载：普通函数优先
    printX(3);
    printX(3000000000LL);
    printX(3.14159);

    // 泛型容器打印
    vector<int> vi = {1, 2, 3};
    vector<double> vd = {1.5, 2.5};
    printVec(vi);
    printVec(vd);
    return 0;
}
```

> **【易错】** 四处：
> 1. **模板函数有两个不同类型参数** —— 推导冲突，编译失败。需显式指定或改用两个类型参数。
> 2. **模板报错信息极长** —— 这是模板的固有代价。**竞赛中尽量少用模板**，除了调试输出。
> 3. **模板定义必须可见** —— 模板不能像普通函数那样「声明在头文件、定义在 `.cpp`」。
>    竞赛是单文件程序，不受影响。
> 4. **把模板当成「高级技巧」到处用** —— 竞赛的目标是**快速写对**，
>    模板会拖慢编写速度并增加报错噪音。**只在调试输出这类场景用。**

> **【类比】** 模板像**模具**：一套模具能压出不同材质的零件。
> 但换材质时要重新调试模具参数（编译错误），所以只在批量生产（真正泛型需求）时才值得。

> **【记忆】** **模板只为「调试输出」服务，不为「显得高级」服务。**

**关联**

- `[前置]` 见 E-1 `auto`（返回类型推导）。
- `[后续]` 见 F-2 调试技巧（调试输出模板的实战使用）。
- `[易混]` 模板函数与函数重载：前者编译期生成多份，后者是运行期选择。
- `[延伸]` 完整的模板体系（特化、偏特化、SFINAE、模板元编程）属 `03_常规课程`，
  **本轮未生成**，且竞赛侧明确划出。

---

### E-8　运算符重载　`P0`　熟练　`[未学]`

> **【重点】** 竞赛中只需要重载**一个**运算符：`operator<`。
> 它是自定义类型进入 `set` / `map` / `sort` / `priority_queue` 的**唯一门票**。
> 现有代码中 `operator<` **零使用**。

**是什么**：给自定义类型定义运算符的行为。

**为什么**：标准库的排序、查找、去重、关联容器都依赖「比较」。
内置类型已有比较规则，自定义类型必须自己定义。**不定义就没有任何容器能用。**

**怎么用**：

1. **成员函数形式**（最常用）：`bool operator<(const T &o) const`。
2. **末尾的 `const` 不能漏** —— 否则无法在 `const` 上下文（`set` 内部）调用。
3. **必须实现严格弱序** —— 只用 `<`，不用 `<=`。
4. 需要「多级比较」时用 `if` 逐级判：
   ```cpp
   if (x != o.x) return x < o.x;
   return y < o.y;
   ```
5. **`priority_queue` 的语义相反**：堆取「最大」，所以想让「数值小的优先」要写 `>`。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <set>
#include <map>
#include <vector>
#include <algorithm>
#include <queue>
using namespace std;

// 1. 基础：坐标点，按 (x, y) 字典序
struct Point {
    int x, y;
    // 成员函数形式；末尾 const 不可漏
    bool operator<(const Point &o) const {
        if (x != o.x) return x < o.x;    // 先比 x
        return y < o.y;                   // x 相同再比 y
    }
    // 需要 == 时也要重载（unique 用到）
    bool operator==(const Point &o) const { return x == o.x && y == o.y; }
};

// 2. 用于优先队列：想让「权值小的优先」
struct Edge {
    int to, w;
    // 堆取「最大」，所以写 > 才能让小的优先
    bool operator<(const Edge &o) const { return w > o.w; }
};

int main() {
    // 3. 直接排序
    vector<Point> pts = {{2, 9}, {1, 5}, {2, 3}, {1, 2}};
    sort(pts.begin(), pts.end());                 // 用 operator<
    printf("排序后：");
    for (auto &p : pts) printf("(%d,%d) ", p.x, p.y);
    printf("\n");

    // 4. 进入 set：自动去重 + 自动排序
    set<Point> s(pts.begin(), pts.end());
    printf("set 大小：%d（含重复？）\n", (int)s.size());
    s.insert({2, 3});                             // 已存在，不会重复插入
    printf("再插入 (2,3) 后 set 大小：%d\n", (int)s.size());

    // 5. set 的 lower_bound 用 operator< 比较
    auto it = s.lower_bound({2, 0});              // 第一个 >= (2,0)
    if (it != s.end()) printf(">= (2,0) 的首个点：(%d,%d)\n", it->x, it->y);

    // 6. 进入 map 的键
    map<Point, int> mp;
    mp[{1, 1}] = 100;
    mp[{2, 2}] = 200;
    printf("map 大小：%d\n", (int)mp.size());

    // 7. unique 需要 operator==
    vector<Point> dup = {{1,1},{1,1},{2,2}};
    sort(dup.begin(), dup.end());
    dup.erase(unique(dup.begin(), dup.end()), dup.end());
    printf("去重后点数：%d\n", (int)dup.size());

    // 8. priority_queue 用 operator<
    priority_queue<Edge> pq;
    pq.push({1, 5});
    pq.push({2, 1});
    pq.push({3, 3});
    printf("最小权边：to=%d w=%d\n", pq.top().to, pq.top().w);   // to=2 w=1
    return 0;
}
```

> **【易错】** 五处：
> 1. **漏末尾 `const`** —— 放进 `set` 时报一大堆模板错误。
>    **记忆：`operator<` 的签名最后一定是 `const`。**
> 2. **用 `<=` 实现** —— 违反严格弱序，`set` 会误判相等，**丢元素**。
> 3. **只比较部分字段导致「不同对象被判相等」** —— 如只比 `x` 不比 `y`，
>    则 `(1,2)` 与 `(1,3)` 在 `set` 中被视为同一个，**其中一个会被丢弃**。
> 4. **`priority_queue` 的语义写反** —— 堆取最大，想小顶必须写 `>`。
> 5. **`unique` 需要 `operator==` 而非 `operator<`** —— 只重载 `<` 时 `unique` 的默认版本编译失败。

> **【类比】** `operator<` 像**给一群没有身高概念的人制定「谁更高」的判定标准**。
> 标准一旦定下，所有容器（`sort` / `set` / `map`）都按它行事。
> **标准必须严格且一致**——不能出现「A 比 B 高，同时 B 比 A 高」。

> **【记忆】** **只要 `<`，末尾 `const`，字段要全比；堆里方向反着写。**

**关联**

- `[前置]` 见 A-7 结构体（入门形态）。
- `[后续]` 见 C-7 `set`、C-8 `map`、C-5 `priority_queue`（三处都要用它）。
- `[易混]` `operator<` 与比较器 lambda：前者是类型的固有顺序，后者是单次使用的自定义规则。
  **进 `set` / `map` 只能用 `operator<`，不能用 lambda。**
- `[组合]` 与模块 C 全部关联容器组合 —— 这是模块 C 能用自定义类型的前提。

---

### E-9　引用与移动语义　`P2`　理解　`[未学]`

> **【重点】** 竞赛中只需要**理解一件事**：
> **大对象传参、返回、存入容器时，能省一次拷贝就省一次。**
> 移动语义（`std::move`）在竞赛中的实际使用频率很低。

**是什么**：
- **引用**（`&`）：别名，不拷贝。
- **右值引用**（`&&`）与**移动语义**：把即将销毁的对象的资源「搬走」而不是「复制一份」。

**为什么**：一次 `vector` 拷贝是 O(n)。如果一个操作里有多次拷贝，复杂度会悄悄升级。

| 场景 | 是否有拷贝 | 优化方式 |
|------|-----------|---------|
| `void f(vector<int> v)` | **有**（整份拷贝） | 改 `const vector<int> &` |
| `void f(const vector<int> &v)` | 无 | — |
| `for (auto x : v)` | **有**（每个元素一份） | 改 `const auto &x` |
| `return 局部 vector` | 无（返回值优化 RVO） | **不用写 `std::move`** |
| `v.push_back(bigVector)` | 有 | `v.push_back(std::move(bigVector))` |
| `v.push_back({1,2,3})` | 无（直接构造） | — |

**怎么用**：

1. 传参：可读用 `const &`，可写用 `&`，**避免传值**。
2. 遍历：`const auto &`（模块 E-1）。
3. 返回局部对象：**直接 `return v;`** —— 编译器有返回值优化，加 `std::move` 反而可能阻碍优化。
4. `push_back` 一个「之后不再用」的大对象时，用 `std::move`。
5. **`std::move` 只是类型转换，不执行任何移动**；真正的移动发生在构造/赋值时。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <vector>
#include <string>
#include <utility>
using namespace std;

// 1. 错误：传值，整份拷贝
size_t sizeByValue(vector<int> v) {
    return v.size();
}

// 2. 正确：常量引用，零拷贝
size_t sizeByRef(const vector<int> &v) {
    return v.size();
}

// 3. 返回局部对象：不需要 std::move
vector<int> makeVec(int n) {
    vector<int> v;
    v.reserve(n);
    for (int i = 0; i < n; i++) v.push_back(i);
    return v;                 // 编译器做返回值优化（RVO），无拷贝
}

int main() {
    vector<int> big(1000000, 7);          // 100 万个元素

    printf("传值 size=%d\n", (int)sizeByValue(big));    // 发生了一次整份拷贝
    printf("传引用 size=%d\n", (int)sizeByRef(big));    // 零拷贝

    // 4. 移动：把 big 的资源搬进 v2，big 变为空
    vector<int> v2 = std::move(big);
    printf("move 后 v2.size=%d，big.size=%d（big 已被掏空）\n",
           (int)v2.size(), (int)big.size());            // 1000000, 0

    // 5. 移动进容器：避免拷贝一个即将销毁的对象
    vector<vector<int>> all;
    vector<int> tmp = makeVec(1000);
    all.push_back(std::move(tmp));                      // 搬进去，不复制
    printf("all[0].size=%d，tmp.size=%d\n",
           (int)all[0].size(), (int)tmp.size());        // 1000, 0

    // 6. 直接构造：比先建临时再 push 更省
    vector<pair<int,string>> pv;
    pv.push_back({1, "a"});                             // 就地构造，无临时对象
    printf("pv[0]=(%d,%s)\n", pv[0].first, pv[0].second.c_str());

    // 7. 危险：move 之后继续使用源对象
    //    tmp 现在处于「有效但未指定」状态，它的 size 是 0，内容不可依赖
    printf("move 之后不应再依赖 tmp 的内容\n");

    // 8. 遍历的拷贝代价
    vector<string> words = {"hello", "world"};
    long long total = 0;
    for (const auto &w : words) total += w.size();      // 零拷贝
    printf("字符总数：%lld\n", total);
    return 0;
}
```

> **【易错】** 四处：
> 1. **`return std::move(v);` 返回局部对象** —— 会**阻碍**返回值优化，反而变慢。
>    **记忆：返回局部对象直接 `return v;`，不要加 `move`。**
> 2. **`move` 之后继续使用源对象** —— 状态已被掏空（`size` 为 0），继续用会得到错误结果。
> 3. **以为 `std::move` 真的搬了东西** —— 它只是把左值转成右值引用（类型转换），
>    实际移动由随后的构造函数完成。
> 4. **给 `const` 对象用 `move`** —— 得到 `const` 右值引用，实际退化为**拷贝**。

> **【类比】** 拷贝像**复印一份文件**（原件还在，多一份），
> 移动像**把文件袋整个交出去**（对方拿到全部内容，你手上只剩空袋）。
> 所以移动之后**不能再问原袋子里有什么**。

> **【记忆】** **传参用 `const &`，返回局部对象别加 `move`，移动之后别再用。**

**关联**

- `[前置]` 见 A-6 函数与参数传递、E-1 `auto`。
- `[组合]` 与 E-2 范围 for 组合 → `const auto &` 是遍历的零拷贝写法。
- `[易混]` 引用与移动：前者是「同一对象的别名」，后者是「把资源搬到新对象」。
- `[延伸]` 移动构造、完美转发、`std::forward` 属工程向内容，
  归入 `03_常规课程`，**本轮未生成**。

---

## 四、跨章关联地图

| 关联知识点 | 关系 | 说明 | 位置 |
|-----------|------|------|------|
| 结构体 | `[前置]` | `operator<` 的宿主类型 | 模块 A-7 |
| 引用与 `const &` | `[前置]` | 捕获与传参的基础 | 模块 A-6 |
| 容器与迭代器 | `[前置]` | `auto` 的主要收益点 | 模块 C-1 |
| `pair` / `tuple` | `[前置]` | 结构化绑定的解包对象 | 模块 C-3 |
| `sort` / 比较器 | `[组合]` | lambda 作比较器 | 模块 D-1、D-2 |
| `count_if` / `find_if` | `[组合]` | lambda 作判据 | 模块 D-6 |
| `set` / `map` | `[组合]` | `operator<` 是入场券 | 模块 C-7、C-8 |
| `priority_queue` | `[组合]` | `operator<` 或 `decltype` lambda | 模块 C-5 |
| 对拍脚本 | `[组合]` | 生成器与暴力程序常写成 lambda/函数 | 模块 F-3 |
| 图论边表 | `[组合]` | 结构化绑定让三元组遍历可读 | 算法专题阶段 5 |

**本模块在知识体系中的位置**

```text
竞赛 C++ 五阶段
├─ 阶段 1 语言基础与输入输出   （模块 A、B）
├─ 阶段 2 STL 容器            （模块 C）
├─ 阶段 3 STL 算法            （模块 D）
├─ 阶段 4 现代语法糖          ◄── 本模块
│   ├─ 写法简化：E-1 auto / E-2 范围 for / E-4 结构化绑定 / E-5 if 初始化
│   ├─ 就地逻辑：E-3 lambda
│   ├─ 类型能力：E-7 模板 / E-8 运算符重载 / E-6 constexpr
│   └─ 拷贝控制：E-9 引用与移动语义
└─ 阶段 5 竞赛工程化          （模块 F）
```

---

## 五、本章总结

### 5.1 核心内容（一页纸）

1. **遍历只读用 `const auto &`，要改加 `&`，用 `auto` 就是拷贝。**
2. **要改外部变量，lambda 捕获写 `[&]`；要改外部量不能用 `[=]`。**
3. **递归 lambda 必须用 `std::function` 包裹**，且性能低于普通函数，竞赛优先写成普通函数。
4. **`priority_queue` 用 lambda 比较器必须写 `decltype(cmp)` 并把 `cmp` 传进构造函数。**
5. **结构化绑定 `auto &[a, b]` 加 `&` 才能改；解包 `map` 后键是 `const`。**
6. **查找 + 判断写成一行：`if (auto it = m.find(k); it != m.end())`。**
7. **`constexpr` 用于数组大小与 `bitset` 位宽；别用 `1e5` 定义整型常量。**
8. **模板只为「调试输出」服务，不为「显得高级」服务。**
9. **`operator<` 只用 `<`、末尾必须 `const`、字段要全比**，否则 `set` 会丢元素。
10. **`priority_queue` 的方向与 `sort` 相反**：堆取最大，想小顶就写 `>`。
11. **返回局部对象直接 `return v;`**，加 `std::move` 会阻碍返回值优化。
12. **`std::move` 之后源对象不可再依赖**（`size` 为 0，内容未指定）。
13. **范围 for 不提供下标**；需要下标时老老实实用下标循环。

### 5.2 知识点串联图

```text
E-1 auto ──┬── E-2 范围 for ──┬── E-3 lambda ──────────┐
           │                  └── E-4 结构化绑定      │
           ├── E-5 if 初始化                        │
           └── E-7 函数模板                        │
                                                    ▼
E-8 运算符重载 ──┬── 模块 C-7 set / C-8 map（入场券）
                 └── 模块 C-5 priority_queue（方向相反）

E-6 constexpr ── 模块 C-9 bitset 位宽
E-9 引用与移动语义 ── 模块 A-6 传参优化
```

### 5.3 自测清单

- [ ] 能说出 `auto` 与 `auto&` 在遍历时的区别
- [ ] 能说出范围 for 的两个受限场景（需要下标、需要倒序）
- [ ] 能写出按值捕获与按引用捕获的 lambda，并解释区别
- [ ] 能写出 `priority_queue` 使用 lambda 比较器的完整声明
- [ ] 能写出遍历 `map` 的结构化绑定写法，并说明键为什么不可改
- [ ] 能写出 `if` 初始化语句的查表写法
- [ ] 能说出 `constexpr` 相对 `const` 的关键区别
- [ ] 能说出模板在竞赛中唯一实用的场景
- [ ] 能写出严格弱序的 `operator<` 并解释为什么不能用 `<=`
- [ ] 能说出 `return std::move(局部变量)` 为什么是错的

### 5.4 间隔重复表

| 知识点 | 首次 | +1 天 | +3 天 | +7 天 | +21 天 |
|--------|------|-------|-------|-------|--------|
| E-1 `auto` |  |  |  |  |  |
| E-2 范围 for |  |  |  |  |  |
| E-3 lambda |  |  |  |  |  |
| E-4 结构化绑定 |  |  |  |  |  |
| E-5 `if` 初始化语句 |  |  |  |  |  |
| E-6 `constexpr` |  |  |  |  |  |
| E-7 函数模板基础 |  |  |  |  |  |
| E-8 运算符重载 |  |  |  |  |  |
| E-9 引用与移动语义 |  |  |  |  |  |

### 5.5 应落到实处的代码修改

| 问题 | 依据 | 建议 |
|------|------|------|
| `auto` 零使用 | 75 文件统计 | 迭代器与算法返回值改用 `auto`，见 E-1 |
| lambda 零使用 | 75 文件统计 | 单处比较器与判据改为就地 lambda，见 E-3 |
| `operator<` 零使用 | 75 文件统计 | 需要排序/入 `set` 的结构体补上，见 E-8 |
| 结构化绑定零使用 | 75 文件统计 | 图论边表遍历改用它，可读性提升最明显，见 E-4 |
| 范围 for 使用不足 | 75 文件统计 | 只读遍历改 `const auto &`，消除越界风险，见 E-2 |

> **【重点】** 这五项是**投入产出比最高的一组修改**：
> 它们不改变算法，只改变写法，但能同时减少代码长度与出错率。

---

## 六、本节未包含的内容

| 内容 | 归属 | 说明 |
|------|------|------|
| 智能指针（`unique_ptr` / `shared_ptr`） | `03_常规课程` | 竞赛用数组模拟，不用动态内存管理 |
| 移动构造、完美转发、`std::forward` | `03_常规课程` | 竞赛只需 E-9 的三条结论 |
| 模板元编程、SFINAE、Concepts | `03_常规课程` | 明确划出 |
| `optional` / `variant` / `any` | `03_常规课程` | 语义可被更简写法替代 |
| 协程、Modules、`std::filesystem` | `03_常规课程` | 多数 OJ 编译器不支持 |
| 可变参数模板 | `03_常规课程` | 明确划出 |

> **【注意】** 上述内容指向 `03_常规课程`，**本轮未生成**。

---

## 七、复习记录

| 日期 | 复习方式 | 本次结果 | 掌握状态变更 |
|------|---------|---------|-------------|
|  |  |  |  |

---

## 八、待办与缺口

- [ ] 待补知识点：无（本模块已覆盖方案 §1.2 定义的全部 9 个知识点）
- [ ] **待验证项**：C++17 结构化绑定与 `if` 初始化语句需要编译器支持 `-std=c++17`。
      本机 MinGW-W64 g++ 8.1.0 支持；但若某 OJ 用更老的编译器，需确认其标准选项。
      编译命令统一写 `g++ -std=c++17 -O2`。
- [ ] 待修正的既有代码：见 §5.5 的五项
- [ ] 待核实的题源：本模块为语法糖，**不单独出题**。
      练习体现在算法专题各阶段的题集代码风格中。

---
## 配套题库练习

E 模块（auto、范围 for、结构化绑定、lambda 等）为**语言写法依附类**知识点，不设独立题型；请在 A 至 D 模块各题的推荐写法中主动使用本模块语法练习。

---

*模块 E 完 · 学习顺序见 `README_模块总览与学习顺序.md` · 排版规范见 `22_排版与标注规范.md`*
