# 模块 C　STL 容器

> **元信息**
> 优先级：`P0`　｜　所属子分类：`02_竞赛\02_竞赛C++`　｜　学习顺序：五阶段中的**阶段 2**
> 前置：模块 A（整型与溢出、数组、结构体与运算符、位运算）、模块 B（输入输出）
> 后续：模块 D（STL 算法）、模块 E（现代语法糖）、模块 F（竞赛工程化）
> 最近复习：未开始　｜　整体掌握：`[未学]`

> **图例**
> **重要程度**：`P0` 必掌握（加粗 + 主色）｜`P1` 需熟练（次色）｜`P2` 了解即可（弱化色）
> **内容类型**：定义概念｜模板公式｜例题自测｜易错陷阱｜通俗类比｜补充延伸
> **掌握状态**：`[未学]` `[学过]` `[会做]` `[易错]` `[掌握]`（纯文字，不着色）
> 说明：颜色仅用于加速定位，**信息一律由文字标签与字重承载**，黑白打印不丢信息。

---

## 零、本模块的核心不是「会用」，而是「会选」

同样的题，用错容器可能从 AC 变成 TLE：

| 场景 | 用错容器 | 后果 |
|------|---------|------|
| 需要频繁在中间插入删除 | 用 `vector` 而非 `list` 或 `set` | 每次插入 O(n)，总代价 O(n²) |
| 需要按值快速查找 | 用 `vector` 线性查找而非 `map` / `set` | 每次查找 O(n)，总代价 O(n²) |
| 只关心「有没有」 | 用 `map` 而非 `unordered_map` | 常数因子大数倍 |
| 需要取最小值 | 用 `vector` 每次扫描而非 `priority_queue` | 每次 O(n)，堆化后 O(log n) |

> **【重点】** 本模块的验收标准不是「能默写 `push_back`」，
> 而是**「见到题目能立刻说出该用哪个容器，并说出理由」**。

### 0.1 现有代码的实测缺口

对竞赛代码（`资料\03_算法集训\` 下 **75 个 `.cpp`**）统计（2026-09-12 快照）：

| 容器 | 出现次数 | 判定 |
|------|---------|------|
| `vector<` | 61 | 使用充分 |
| `queue<` | 10 | 使用一般 |
| `priority_queue` | 4 | 使用不足 |
| `greater<` | 4 | 使用不足 |
| `stack<` | 8 | 使用一般 |
| `vector<vector` | 7 | 使用一般 |
| `pair<` | 4 | 使用不足 |
| **`set<`** | **0** | **完全未使用** |
| **`map<` / `unordered_map`** | **1 / 1** | **严重不足** |

结论：**序列容器够用，关联容器几乎空白**。
而关联容器恰好是「按值查找」「去重」「动态维护有序集合」三类题的唯一正解。

---

## 一、本章速览

**一句话概括**：十种容器各自解决一类问题；本模块的目标是建立「看到题意就能锁定容器」的条件反射。

| 序 | 知识点 | 优先级 | 深度 | 掌握 | 前置 |
|----|--------|--------|------|------|------|
| 1 | `vector` | P0 | 熟练 | `[未学]` | — |
| 2 | `string` | P0 | 熟练 | `[未学]` | 1 |
| 3 | `pair` / `tuple` | P1 | 熟练 | `[未学]` | 1 |
| 4 | `stack` / `queue` | P0 | 熟练 | `[未学]` | 1、3 |
| 5 | `priority_queue` | P0 | 熟练 | `[未学]` | 3、4 |
| 6 | `deque` | P2 | 会用 | `[未学]` | 4 |
| 7 | `set` / `multiset` | P1 | 熟练 | `[未学]` | 3 |
| 8 | `map` / `unordered_map` | P0 | 熟练 | `[未学]` | 3、7 |
| 9 | `bitset` | P1 | 会用 | `[未学]` | 7 |
| 10 | 容器选型决策 | P0 | 理解 | `[未学]` | 1 至 9 |

> 「序」即学习先后顺序。`priority_queue` 排在第 5 位而非更前，是因为它依赖 `pair`（第 3）做「值 + 优先级」的载体，也依赖 `queue`（第 4）理解底层适配器概念。

---

## 二、前置检查

| 前置知识点 | 出处 | 自测 |
|-----------|------|------|
| 数组开大小与下标约定 | 模块 A-4 | - [ ] 能说清全局数组与局部数组的区别 |
| 结构体与 `operator<` | 模块 A-7 | - [ ] 能写出结构体的 `operator<`，末尾带 `const` |
| 位运算 lowbit | 模块 A-5 | - [ ] 能默写 `x & -x` |
| `const &` 传参 | 模块 A-6 | - [ ] 知道大容器传参要加 `const &` |

> 任何一项未打钩，先回补该前置。模块 C 的性能讨论全部建立在「避免拷贝」之上。

---

## 三、知识点逐讲

### C-1　`vector`　`P0`　熟练　`[未学]`

> **【重点】** `vector` 是**可动态扩容的数组**。它保留了数组的 O(1) 随机访问，代价是扩容时重新分配。

**是什么**：连续的、可自动增长的同类型元素序列。`vector<T>` 与 `T[]` 的区别只有两点：**长度可变**、**能查询自身长度**。

**为什么**：竞赛里很多题的规模在运行时才知道。定长数组要么开太大浪费，要么开小了越界。
`vector` 用 `push_back` 增长，并保证 `v.size()` 随时正确。

**怎么用**：

1. 一维：`vector<int> a(n)` 开 n 个元素（已默认初始化）；`vector<int> a(n, x)` 全部初始化为 x。
2. 二维网格：`vector<vector<int>> g(n, vector<int>(m, 0))` —— **注意两个 `n` 和 `m` 的位置**。
3. 追加用 `push_back`；**预知规模时先 `reserve`** 避免反复扩容。
4. 遍历：优先用范围 for（模块 E-2），避免下标写错。
5. **`vector<bool>` 是特化版本**，按位存储，行为与普通 `vector` 不同，竞赛中建议用 `bitset`（C-9）替代。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <vector>
using namespace std;

int main() {
    // 一维：开 n 个元素，全部初始化为 0
    int n = 5;
    vector<int> a(n, 0);
    for (int i = 0; i < (int)a.size(); i++) a[i] = i * i;   // 边界：下标 0 到 n-1

    // 追加元素：容量不足时自动扩容
    a.push_back(100);
    printf("size=%d capacity=%d\n", (int)a.size(), (int)a.capacity());

    // 预分配：避免反复扩容。竞赛中若已知最大规模，这一步能省掉大量重新分配
    vector<int> b;
    b.reserve(100000);
    for (int i = 0; i < 100; i++) b.push_back(i);
    printf("b.size=%d b.capacity=%d\n", (int)b.size(), (int)b.capacity());

    // 二维网格：n 行 m 列，全部初始化为 0
    int rows = 3, cols = 4;
    vector<vector<int>> g(rows, vector<int>(cols, 0));   // 边界：两个参数分别是行数与「一行」
    g[2][3] = 9;
    printf("g[2][3]=%d  g.size()=%d  g[0].size()=%d\n",
           g[2][3], (int)g.size(), (int)g[0].size());

    // 末尾元素与弹出的标准写法
    printf("末尾元素=%d\n", a.back());
    a.pop_back();                                       // 只删末尾，不返回值
    printf("弹出后 size=%d\n", (int)a.size());

    // 清空有两种：clear 只改 size，shrink_to_fit 才真正释放内存
    a.clear();
    printf("clear 后 size=%d capacity=%d（内存未还）\n",
           (int)a.size(), (int)a.capacity());
    return 0;
}
```

> **【易错】** 五处：
> 1. **`vector<vector<int>> g(n, m)`** —— 错。第二个参数应是「一行」即 `vector<int>(m)`，
>    写成 `m` 会编译失败或语义错误。**记忆：外层给行数和一个模板行。**
> 2. **`v.size()` 与 `int` 比较**。`size()` 返回无符号 `size_t`，
>    `for (int i = 0; i < v.size() - 1; i++)` 在 `v` 为空时 `size()-1` 会绕回巨大正数 → 越界。
>    **修法：先转 `int`，或改为 `i + 1 < (int)v.size()`。**
> 3. **`push_back` 与 `[]` 混用**。`v[i]` 不检查越界，也不会自动扩容。空 `vector` 直接 `v[0]` 是 UB。
> 4. **扩容时迭代器/引用失效**。`push_back` 后之前保存的 `int* p = &v[0]` 可能悬垂。
> 5. **循环内 `push_back` 同时读 `size()`**：`for (int i = 0; i < v.size(); i++) v.push_back(x);` 是死循环。

> **【类比】** `vector` 像一间会自己加盖房间的旅馆：住满了就**整体搬到一个更大的楼里**。
> 原楼的钥匙（迭代器、指针、引用）**全部作废**——这就是扩容导致迭代器失效的原因。

> **【记忆】** **二维是「行数 + 一个模板行」。** 别忘了 `reserve`。

**关联**

- `[前置]` 见 A-4 数组。`vector` 是数组的动态版本，性能略低但不会越界。
- `[后续]` 见 C-2 `string`（本质就是 `vector<char>` 的封装）、D-1 `sort`（作用于 `vector` 的区间）。
- `[易混]` 见 A-4。定长且规模已知时，手写数组比 `vector` 更快（无扩容与边界检查）。
- `[组合]` 与 D-4 `unique` + `erase` 组合 → 去重的标准写法。
- `[延伸]` 完整语义（分配器、迭代器类别）见 `03_常规课程`，**本轮未生成**。

---

### C-2　`string`　`P0`　熟练　`[未学]`

> **【重点】** `string` 的杀手级用法是 **`getline` 读整行** 与 **`stringstream` 拆词**。
> 这两个是「字符串处理题」的开局动作。

**是什么**：字符序列，可以拼接、比较、查找、截取。本质是 `vector<char>` 加一套字符串接口。

**为什么**：C 风格 `char[]` 需要手工管长度、拼接容易越界、比较要用 `strcmp`。
`string` 让 `+`、`==`、`<` 直接可用，且长度自动维护。

**怎么用**：

1. 读整行：`getline(cin, s)`。**注意前面若用过 `cin >>`，必须先 `cin.ignore()` 吃掉换行残留。**
2. 拆词：`stringstream ss(s); while (ss >> token) {...}`。
3. 求长度：`s.size()`。**返回无符号，比较时先转 `int`**。
4. 查找子串：`s.find(t)`，**找不到返回 `string::npos`**，不要与 `-1` 直接比较。
5. 截取：`s.substr(pos, len)`。**第二个参数是长度，不是结束下标。**

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <string>
#include <sstream>
#include <iostream>
using namespace std;

int main() {
    int n;
    // 关键：读完整数后必须吃掉本行剩余内容（含换行），否则下面的 getline 会读到空串
    string line;
    n = 1;
    printf("（演示用，跳过实际读入）\n");

    // 1. 读整行
    line = "hello world 123";
    printf("整行：%s\n", line.c_str());

    // 2. 按空格拆词
    stringstream ss(line);
    string tok;
    int cnt = 0;
    while (ss >> tok) {                    // 边界：流提取失败即结束
        printf("  第 %d 个词：%s\n", ++cnt, tok.c_str());
    }

    // 3. 按指定分隔符拆分（如逗号）
    string csv = "a,b,c";
    stringstream ss2(csv);
    string field;
    while (getline(ss2, field, ',')) {     // 第三个参数是分隔符
        printf("  字段：%s\n", field.c_str());
    }

    // 4. 查找：找不到返回 npos，必须用 npos 判断，不能与 -1 比
    string s = "abcabc";
    size_t pos = s.find("cab");
    if (pos != string::npos) {
        printf("找到位置：%d\n", (int)pos);
    } else {
        printf("未找到\n");
    }

    // 5. 截取：第二个参数是长度
    printf("从 2 起取 3 个字符：%s\n", s.substr(2, 3).c_str());   // "cab"

    // 6. 拼接与比较
    string a = "abc", b = "abd";
    printf("拼接：%s  比较 a<b：%d\n", (a + "x").c_str(), (int)(a < b));

    // 7. size() 是无符号，参与减法前先转 int
    printf("size 转 int：%d\n", (int)s.size());
    return 0;
}
```

> **【易错】** 五处，前两条是最高频的：
> 1. **`cin >> n` 之后用 `getline`**。`cin >> n` 把换行留在缓冲区，`getline` 立刻读到空串。
>    **修法：`cin.ignore();` 或 `getline(cin, line);` 先清掉。**
> 2. **`s.find(t) == -1`**。`npos` 是 `size_t` 的最大值，与 `-1` 比较在某些实现上成立、
>    在另一些上不成立。**必须写 `s.find(t) == string::npos`。**
> 3. **`substr(pos, endPos)`**。第二个参数是**长度**。想要 `[2, 5)` 应写 `substr(2, 3)`。
> 4. **`s.size() - 1` 在空串上绕回**，同 C-1。
> 5. **`printf("%s", s)`**。`string` 不是 `char*`，必须 `.c_str()`。用 `cout << s` 则无此问题。

> **【类比】** `getline` 与 `cin >>` 的区别像「整行抄录」与「只记第一个单词」。
> 而缓冲区的换行残留像**上一页没撕干净的便签纸**——下一行会先读到它。

> **【记忆】** **`cin >>` 之后要 `getline`，先 `ignore`。** 这个 bug 每个人都犯过。

**关联**

- `[前置]` 见 C-1 `vector`。
- `[后续]` 见 D-8 `next_permutation`（对 `string` 同样适用）、算法专题阶段 6 字符串哈希与 KMP。
- `[易混]` `char[]` 与 `string`：前者可与 `scanf("%s")` 配合，后者要用 `cin` 或 `c_str()` 转换。
- `[组合]` 与 D-6 `reverse` 组合 → 字符串反转；与 D-4 `unique` 组合 → 去重相邻字符。
- `[延伸]` 完整语义见 `03_常规课程`，**本轮未生成**。

---

### C-3　`pair` / `tuple`　`P1`　熟练　`[未学]`

> **【重点】** `pair` 让「两个值当成一个」成为可能，且**内置了字典序比较**——
> 这是它能直接放进 `set` / `priority_queue`、直接 `sort` 的根本原因。

**是什么**：`pair<A,B>` 是二元组，`tuple<A,B,C...>` 是任意元组。

**为什么**：很多场景需要「整体排序、整体入队」：坐标 + 距离、值 + 下标、节点 + 权值。
用 `pair` 就不用写结构体、不用写 `operator<`，因为 **`pair` 已按「先比 first，再比 second」定义好**。

**怎么用**：

1. 构造：`make_pair(a, b)` 或 `{a, b}`（C++11 起）。
2. 访问：`.first` / `.second`；元组用 `get<0>(t)`，或结构化绑定（模块 E-4）。
3. 排序与入堆：**直接用，无需自定义比较器**。想「先比 second」时把顺序反过来放。
4. 建图：`vector<pair<int,int>> g[N]` 是邻接表的常用形式。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <utility>
#include <vector>
#include <algorithm>
#include <queue>
using namespace std;

int main() {
    // 构造与访问
    pair<int, int> p = {3, 7};
    printf("first=%d second=%d\n", p.first, p.second);

    // 内置字典序比较：先比 first，再比 second
    vector<pair<int, int>> v = {{2, 9}, {1, 5}, {2, 3}};
    sort(v.begin(), v.end());                  // 无需比较器
    for (auto &x : v) printf("(%d,%d) ", x.first, x.second);
    printf("\n");                              // (1,5) (2,3) (2,9)

    // 想要「按 second 排序」：把要优先的字段放到 first，或写比较器（模块 D-2）
    sort(v.begin(), v.end(), [](const pair<int,int> &a, const pair<int,int> &b) {
        return a.second < b.second;            // 按 second 升序
    });
    for (auto &x : v) printf("(%d,%d) ", x.first, x.second);
    printf("\n");                              // (2,3) (1,5) (2,9)

    // 邻接表：图为 3 个点，边 (u,v,w) 用 pair 存 v 与 w
    vector<pair<int,int>> g[4];                // g[u] 存 {v, w}
    g[1].push_back({2, 5});
    g[1].push_back({3, 8});
    for (auto &e : g[1])
        printf("边 1 -> %d，权 %d\n", e.first, e.second);

    // 小顶堆：pair 默认按 first 比，配合 greater 得到最小堆（C-5）
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;
    pq.push({5, 1});
    pq.push({2, 9});
    printf("堆顶：(%d,%d)\n", pq.top().first, pq.top().second);   // (2,9)
    return 0;
}
```

> **【易错】** 三处：
> 1. **想让「距离最小」优先，却把距离放在 `second`**。`pair` 默认先比 `first`，
>    `priority_queue` 就变成了按编号排序。**惯例：`{优先级, 值}`，优先级放 `first`。**
> 2. **`pair` 参与 `sort` 时会用到两个字段**。若只想要第一个字段决定顺序，必须写比较器。
> 3. **`tuple` 的 `get<0>` 是编译期下标**，不能写变量 `get<i>(t)`（除非 `i` 是 `constexpr`）。

> **【类比】** `pair` 像「学号 + 成绩」两栏的表：默认按学号排，
> 想按成绩排就得自己说一声（写比较器）。

> **【记忆】** **`{优先级, 值}`** —— 把决定顺序的那个放前面，就省掉一个比较器。

**关联**

- `[前置]` 见 C-1 `vector`（`pair` 常作其元素）。
- `[后续]` 见 C-5 `priority_queue`（`pair` 是它的常用元素）、C-8 `map`（元素本就是 `pair`）。
- `[组合]` 与 D-1 `sort` 组合 → 免比较器排序；与算法专题阶段 5 组合 → Dijkstra 的优先队列元素。
- `[延伸]` `tuple` 的完整用法与结构化绑定见模块 E-4。

---

### C-4　`stack` / `queue`　`P0`　熟练　`[未学]`

> **【重点】** 两者都是**受限的线性结构**，价值在于「用限制换清晰」——
> 限制访问位置后，算法意图变得一目了然。

**是什么**：
- `stack` 栈：**后进先出**（LIFO）。只能操作栈顶。
- `queue` 队列：**先进先出**（FIFO）。只能操作队首出、队尾入。

| 容器 | 规则 | 接口 | 典型场景 |
|------|------|------|---------|
| `stack` | 后进先出 | `push` / `top` / `pop` / `empty` / `size` | 括号匹配、单调栈、DFS 的显式栈 |
| `queue` | 先进先出 | `push` / `front` / `back` / `pop` / `empty` | BFS、拓扑排序、模拟 |

**为什么**：用 `vector` 手写也能实现，但**接口不会自我说明**。
`stack` 的 `push` / `top` 组合本身就表达了「最近优先」的语义，读代码的人立刻知道这是 DFS 或单调栈。

**怎么用**：

1. **访问前必须 `!empty()`**。空容器取 `top` / `front` 是 UB，且不报错。
2. **`pop()` 不返回值**，取值用 `top()` / `front()`。这是最常见的笔误。
3. BFS 用 `queue`，一层一层推进；DFS 用递归或 `stack`。
4. 需要「双端操作」时用 `deque`（C-6）。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <stack>
#include <queue>
#include <vector>
using namespace std;

int main() {
    // 栈：括号匹配
    string s = "(()())";
    stack<char> st;
    bool ok = true;
    for (char c : s) {
        if (c == '(') st.push(c);
        else {
            if (st.empty()) { ok = false; break; }   // 边界：先判空
            st.pop();
        }
    }
    if (!st.empty()) ok = false;                     // 边界：还有未匹配的左括号
    printf("括号匹配：%d\n", (int)ok);

    // 栈：单调栈求「右边第一个更大的数」
    // 这是算法专题阶段 3 的核心模板，此处只演示 stack 的用法
    int a[6] = {0, 3, 1, 4, 1, 5};                   // 1 起始（模块 A-4）
    int n = 5;
    int ans[6] = {0};
    stack<int> idx;                                  // 存下标，不是值
    for (int i = 1; i <= n; i++) {
        // 边界：弹出条件用 <= 而非 <，否则等值元素会互相阻挡
        while (!idx.empty() && a[idx.top()] < a[i]) {
            ans[idx.top()] = i;                      // 找到了右边第一个更大的位置
            idx.pop();
        }
        idx.push(i);
    }
    for (int i = 1; i <= n; i++) printf("a[%d]=%d -> 右边首个更大的位置 %d\n", i, a[i], ans[i]);

    // 队列：BFS 求无权图最短路（以 1 号点为源）
    vector<int> g[6];
    g[1].push_back(2); g[2].push_back(3); g[1].push_back(3);
    vector<int> dist(6, -1);
    queue<int> q;
    dist[1] = 0;
    q.push(1);
    while (!q.empty()) {
        int u = q.front(); q.pop();                  // 先取再弹
        for (int v : g[u]) {
            if (dist[v] == -1) {                     // 未访问
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
    printf("1 到 3 的最短距离：%d\n", dist[3]);
    return 0;
}
```

> **【易错】** 四处：
> 1. **`x = st.pop()`** —— 编译失败。`pop()` 返回 `void`。正确：`x = st.top(); st.pop();`
> 2. **不判空直接 `top()`** —— UB。**纪律：`top` / `front` / `back` 之前必有 `empty` 检查。**
> 3. **单调栈的弹出条件写成 `<`** —— 等值元素互相阻挡，导致答案错一位。
>    这是单调栈题的头号错误（见上方代码注释）。
> 4. **`queue` 的 `pop` 从队首出，但 `push` 从队尾入**。`front()` 是最早入的。

> **【类比】** 栈像一摞盘子，只能从最上面拿；队列像排队买票，只能从队首走、从队尾排。
> **两者都不允许插队**——这正是它们的价值：限制了访问方式，也就限制了你能犯的错。

> **【记忆】** **`pop` 不返回值，先 `top` 再 `pop`；取值前先判空。**

**关联**

- `[前置]` 见 C-1（底层容器）、C-3（`pair` 元素）。
- `[后续]` 见 C-6 `deque`、算法专题阶段 3「栈和队列 / 单调栈」、阶段 4「DFS / BFS」、阶段 5「拓扑排序」。
- `[易混]` `stack` 与递归：递归本质是「用系统栈」，`stack` 是「自己开栈」，后者不爆栈。
- `[组合]` 与算法专题阶段 3 组合 → 单调栈；与阶段 4 组合 → BFS 队列。

---

### C-5　`priority_queue`　`P0`　熟练　`[未学]`

> **【重点】** **大顶堆是默认，小顶堆必须显式写 `greater<类型>`。** 这是最容易记反的一点。

**是什么**：优先队列。元素不按入队顺序出队，而是**始终弹出当前优先级最高的一个**。

**为什么**：需要反复「取当前最小/最大」的场景，用数组每次扫描是 O(n)，
堆化后每次 O(log n)。Dijkstra、Kruskal、哈夫曼树的本质都是「每轮取最小」。

**怎么用**：

1. **默认是大顶堆**（`top()` 是最大值）。
2. **小顶堆**：`priority_queue<int, vector<int>, greater<int>>` —— 三处都要写对。
3. 自定义类型：写 `operator<`，或提供比较器（模块 E-3 lambda 需用 `decltype` 技巧，见下）。
4. **只能访问堆顶**。要遍历所有元素请用别的结构。

| 目标 | 写法 |
|------|------|
| 大顶堆（默认） | `priority_queue<int> pq;` |
| 小顶堆 | `priority_queue<int, vector<int>, greater<int>> pq;` |
| `pair` 小顶堆 | `priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;` |
| 自定义结构 | 重载 `operator<`，反向定义即得想要的优先级 |

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <queue>
#include <vector>
#include <functional>
using namespace std;

// 自定义类型：想让它进堆，必须能比较
struct Task {
    int priority;      // 数值越小越优先
    int id;
    // 堆默认取「最大」，所以要让「数值小」的排在前，就把比较反过来写
    bool operator<(const Task &o) const {
        return priority > o.priority;      // 注意是 > ：小的优先
    }
};

int main() {
    // 默认大顶堆：top 是最大值
    priority_queue<int> mx;
    for (int x : {3, 1, 4, 1, 5}) mx.push(x);
    printf("大顶堆堆顶：%d\n", mx.top());     // 5

    // 小顶堆：三处写法都要对
    priority_queue<int, vector<int>, greater<int>> mn;
    for (int x : {3, 1, 4, 1, 5}) mn.push(x);
    printf("小顶堆堆顶：%d\n", mn.top());     // 1

    // 弹空：注意先判空
    printf("小顶堆依次弹出：");
    while (!mn.empty()) { int t = mn.top(); mn.pop(); printf("%d ", t); }
    printf("\n");

    // 自定义类型
    priority_queue<Task> tq;
    tq.push({5, 100});
    tq.push({1, 200});
    tq.push({3, 300});
    printf("最优先任务：id=%d priority=%d\n", tq.top().id, tq.top().priority);  // 200, 1

    // 用 pair 直接做小顶堆（无需自定义类型）：{距离, 节点}
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;
    pq.push({9, 2});
    pq.push({4, 7});
    printf("最近的节点：%d，距离 %d\n", pq.top().second, pq.top().first);       // 7, 4
    return 0;
}
```

> **【易错】** 四处：
> 1. **以为默认是小顶堆**。默认是**大顶堆**，求最小值必须写 `greater<int>`。
> 2. **漏写中间那个容器参数**。`priority_queue<int, greater<int>>` **是错的**，
>    必须写 `priority_queue<int, vector<int>, greater<int>>`。
> 3. **自定义类型的 `operator<` 语义反了**。堆取的是「最大」，想让数值小的优先就要写 `>`。
>    **记忆：`operator<` 写 `>`，得到小顶堆。**
> 4. **想删除堆中任意元素**。`priority_queue` 不支持。需要时改用 `set`（C-7）或加「懒删除」标记。

> **【类比】** 优先队列像急诊分诊台：不是先来先看，而是**病情最重的先看**。
> `greater<int>` 就是告诉分诊台「把数字小的当成病情重的」。

> **【记忆】** **默认大顶，小顶写 `greater`，中间别漏 `vector<int>`。**

**关联**

- `[前置]` 见 C-3（`pair` 作元素）、C-4（容器适配器概念）。
- `[后续]` 见 C-7 `set`（需要删除任意元素时）、算法专题阶段 5「堆优化 Dijkstra」、阶段 5「Kruskal」、阶段 3「哈夫曼树」。
- `[易混]` `priority_queue` 与 `set`：前者只能访问堆顶 O(1)、不支持删除任意元素；
  后者支持任意查找与删除但常数更大。**只需要顶级元素时用堆。**
- `[组合]` 与 C-3 `pair` 组合 → `{距离, 节点}` 是 Dijkstra 的标准写法。

---

### C-6　`deque`　`P2`　会用　`[未学]`

> **【重点】** `deque` 的唯一竞赛价值是**支持两端 O(1) 插入删除**。
> 需要用到它时，几乎都是在写**单调队列**。

**是什么**：双端队列。两端都能 O(1) 插入与删除。

**为什么**：`queue` 只能尾入头出，`stack` 只能一头进出。而滑动窗口最值（单调队列）
需要在**尾部删除**（弹出不满足单调性的元素）同时在**头部删除**（弹出滑出窗口的元素）。

**怎么用**：

1. 接口：`push_back` / `pop_back` / `push_front` / `pop_front` / `front` / `back`。
2. 单调队列求滑动窗口最小值：**队首即最小**，队内元素值单调递增。
3. 用 `deque` 存**下标**而非值，这样能判断队首是否已滑出窗口。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <deque>
using namespace std;

int main() {
    int a[9] = {0, 1, 3, -1, -3, 5, 3, 6, 7};   // 1 起始
    int n = 8, k = 3;

    deque<int> dq;                              // 存下标，队内值单调递增
    printf("滑动窗口最小值（窗口大小 %d）：", k);
    for (int i = 1; i <= n; i++) {
        // 1. 队首若已滑出窗口，弹出
        while (!dq.empty() && dq.front() <= i - k) dq.pop_front();
        // 2. 从队尾弹出所有比当前值大的元素，保持单调递增
        while (!dq.empty() && a[dq.back()] >= a[i]) dq.pop_back();
        // 3. 当前元素入队
        dq.push_back(i);
        // 4. 窗口成型后输出队首
        if (i >= k) printf("%d ", a[dq.front()]);
    }
    printf("\n");

    // 对比：不用单调队列，直接扫描每个窗口 O(n*k)
    printf("暴力对照：");
    for (int i = 1; i + k - 1 <= n; i++) {
        int mn = a[i];
        for (int j = i; j < i + k; j++) if (a[j] < mn) mn = a[j];
        printf("%d ", mn);
    }
    printf("\n");
    return 0;
}
```

复杂度对比：`deque` 单调队列 O(n)，暴力 O(n·k)。n = 10⁶、k = 10³ 时是 10⁶ 与 10⁹ 的差别。

> **【易错】** 三处：
> 1. **`deque` 存值而不存下标** —— 无法判断队首是否已滑出窗口，必须存下标。
> 2. **忘写第 1 步（弹出滑出元素）** —— 答案会用到窗口外的元素。
> 3. **在 `while` 里用 `a[dq.back()] > a[i]` 而不是 `>=`** —— 等值元素互相干扰，
>    虽然多数题不影响最小值的正确性，但涉及下标题（如求位置）时会错。

> **【类比】** 单调队列像一个**排好队且不断有人插到队尾就把高个子挤走**的队伍。
> 队首永远是最矮的（最小），而队伍始终有序——所以不用每次重排。

> **【记忆】** **单调队列存下标，队首是答案。** 两步清理：先清过期，再清不够优的。

**关联**

- `[前置]` 见 C-4 `queue`。
- `[后续]` 见算法专题阶段 1「尺取法与单调队列」、阶段 7「单调队列优化 DP」。
- `[易混]` `deque` 与 `vector`：`deque` 两端快、随机访问稍慢、内存不连续。
- `[延伸]` 输入输出中的 `bits/stdc++.h` 在本机 MinGW g++ 8.1.0 下编译失败（拉入 `filesystem` 头），
  改用显式头文件即可，见模块 F-1。

---

### C-7　`set` / `multiset`　`P1`　熟练　`[未学]`

> **【重点】** `set` 是**自动去重且自动排序**的容器，所有操作 O(log n)。
> 现有代码中 `set` **零使用**，而它恰好是「动态维护有序集合」类题的唯一正解。

**是什么**：有序集合。`set` 元素唯一，`multiset` 允许重复。

**为什么**：三类题必须用它 ——
1. **需要边插入边查询前驱/后继**（如「找比 x 大的最小元素」）。
2. **需要动态去重**。
3. **需要有序遍历但插入频繁**（用 `vector` + 每次排序是 O(n log n) 每轮）。

**怎么用**：

1. `insert(x)` 插入；`erase(x)` 删除**所有等于 x 的元素**；`erase(迭代器)` 只删一个。
2. **`lower_bound(x)` 返回第一个 ≥ x 的位置**；`upper_bound(x)` 返回第一个 > x 的位置。
   （注意：这是**成员函数**，比 `std::lower_bound` 快，因为它利用树结构。）
3. `find(x)` 查是否存在，**找到返回迭代器，否则返回 `end()`**。
4. `count(x)` 在 `set` 上返回 0 或 1；在 `multiset` 上是 O(log n + 出现次数)，**慎用**。
5. 取首尾：`*s.begin()`（最小）、`*s.rbegin()`（最大）。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <set>
using namespace std;

int main() {
    // 1. 自动去重 + 自动排序
    set<int> s;
    for (int x : {5, 1, 3, 1, 5, 2}) s.insert(x);
    printf("去重并排序后：");
    for (int x : s) printf("%d ", x);        // 1 2 3 5
    printf("\n");

    // 2. 前驱与后继：这是 set 最有价值的用法
    int x = 3;
    auto it = s.lower_bound(x);              // 第一个 >= 3
    printf("lower_bound(%d) = %d\n", x, *it);
    if (it != s.end()) {
        auto nxt = next(it);
        if (nxt != s.end()) printf("后继 = %d\n", *nxt);
    }
    auto it2 = s.upper_bound(x);             // 第一个 > 3
    printf("upper_bound(%d) = %d\n", x, *it2);

    // 3. 不存在时怎么办：找最接近的值
    int y = 4;
    auto lb = s.lower_bound(y);
    if (lb != s.end()) printf(">= %d 的最小元素：%d\n", y, *lb);
    else printf("没有 >= %d 的元素\n", y);
    if (lb != s.begin()) { auto pr = prev(lb); printf("< %d 的最大元素：%d\n", y, *pr); }

    // 4. 删除：erase(值) 删全部，erase(迭代器) 删一个
    multiset<int> ms;
    for (int v : {1, 2, 2, 2, 3}) ms.insert(v);
    ms.erase(2);                             // 删掉所有 2
    printf("multiset 删掉所有 2 后：");
    for (int v : ms) printf("%d ", v);       // 1 3
    printf("\n");

    ms.insert(5); ms.insert(5);
    auto p = ms.find(5);                     // 只删一个 5，用迭代器
    if (p != ms.end()) ms.erase(p);
    printf("只删一个 5 后，5 的个数：%d\n", (int)ms.count(5));

    // 5. 取最小与最大
    printf("最小 %d，最大 %d\n", *s.begin(), *s.rbegin());
    return 0;
}
```

> **【易错】** 五处：
> 1. **对 `set` 用 `std::lower_bound(s.begin(), s.end(), x)`** —— 虽然能编过，
>    但它是**线性**的（因为 `set` 迭代器不是随机访问），退化成 O(n)。**必须用成员函数 `s.lower_bound(x)`。**
> 2. **`erase(x)` 与 `erase(it)` 混淆**。前者删所有等于 x 的，后者只删一个。
>    `multiset` 中误用前者会一次删光。
> 3. **`count(x)` 判存在**。在 `set` 上可，在 `multiset` 上是 O(log n + k)。
>    判存在请用 `find(x) != s.end()`。
> 4. **迭代器解引用前不判 `end()`** —— UB。
> 5. **试图修改 `set` 中的元素**。元素是 `const`，不能改。要改只能先删再插。

> **【类比】** `set` 像一本**始终按字典序排好的花名册**：插一个名字它自己归位，
> 重名的自动被拒绝（`multiset` 则允许重名）。
> 找「排在张三后面的第一个人」就是 `upper_bound`。

> **【记忆】** **成员函数 `s.lower_bound`，不是 `std::lower_bound`。** 前者对数级，后者线性。

**关联**

- `[前置]` 见 C-3 `pair`（`set<pair<int,int>>` 很常用）、A-7 `operator<`（自定义类型入 `set` 的前提）。
- `[后续]` 见 C-8 `map`（同为平衡树）、算法专题阶段 3「并查集」的替代方案、阶段 5「最短路优化」的替代实现。
- `[易混]` `set` 与 `priority_queue`：见 C-5。
- `[组合]` 与算法专题阶段 1「二分」组合 → 动态维护有序序列后二分答案。
- `[延伸]` `unordered_set` 是哈希版本，平均 O(1) 但不保证顺序、不支持 `lower_bound`。

---

### C-8　`map` / `unordered_map`　`P0`　熟练　`[未学]`

> **【重点】** **`map` 有序（O(log n)），`unordered_map` 无序但平均 O(1)。**
> 现有代码中两者各仅 1 次——这是最该补的容器。

**是什么**：键值对容器，按**键**查找值。`map` 基于平衡树（键有序），`unordered_map` 基于哈希表。

| 项 | `map` | `unordered_map` |
|----|-------|----------------|
| 底层 | 红黑树 | 哈希表 |
| 查找 | O(log n) | 平均 O(1)，最坏 O(n) |
| 键有序 | **是** | 否 |
| 支持 `lower_bound` | **是** | 否 |
| 常数因子 | 较大 | **较小** |
| 何时选 | 需要按键有序遍历 / 前驱后继 | 只关心「查得到吗 / 对应值是多少」 |

**为什么**：计数、映射、去重、记忆化搜索的状态表，全都需要「按值查」。
用 `vector` 线性查找在 n = 10⁵ 时是 10¹⁰ 次操作，必然超时。

**怎么用**：

1. 计数：`cnt[x]++`，**不存在的键会自动创建并初始化为 0**（这把双刃剑见易错 1）。
2. 判存在：`if (m.count(k))` 或 `if (m.find(k) != m.end())`。
3. **想要「不存在时不插入」必须用 `find`**。`m[k]` 一定会插入。
4. 取值：`m.at(k)` 会在不存在时抛异常；`m[k]` 会插入默认值。
5. 遍历：`for (auto &kv : m)`，键是 `kv.first`，值是 `kv.second`（模块 E-4 结构化绑定更简洁）。
6. **自定义键类型用于 `unordered_map` 需提供哈希函数**，较麻烦；**竞赛中优先改用 `map`**。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <string>
#include <map>
#include <unordered_map>
using namespace std;

int main() {
    // 1. 计数：最常见的用法
    int a[] = {3, 1, 3, 2, 3, 1};
    map<int, int> cnt;
    for (int x : a) cnt[x]++;                  // 不存在的键自动创建为 0，再 ++
    for (auto &kv : cnt) printf("值 %d 出现 %d 次\n", kv.first, kv.second);

    // 2. map 按键有序：这是它相对 unordered_map 的核心优势
    printf("按 key 升序遍历：");
    for (auto &kv : cnt) printf("%d ", kv.first);     // 1 2 3（有序）
    printf("\n");

    // 3. 危险：m[k] 会插入！
    map<string, int> score;
    score["alice"] = 90;
    if (score["bob"] == 0) printf("注意：访问 score[\"bob\"] 已经把 bob 插进去了\n");
    printf("现在 map 里有 %d 个键\n", (int)score.size());   // 2，不是 1！

    // 4. 正确做法：先 find，不插入
    map<string, int> s2;
    s2["alice"] = 90;
    auto it = s2.find("bob");
    if (it != s2.end()) printf("bob 的分数 %d\n", it->second);
    else printf("bob 不存在，且 map 大小仍为 %d\n", (int)s2.size());   // 1

    // 5. map 的 lower_bound：按 key 找前驱后继（同 C-7）
    auto lb = cnt.lower_bound(2);
    if (lb != cnt.end()) printf("第一个 >= 2 的键：%d\n", lb->first);

    // 6. unordered_map：只关心查找速度时用
    unordered_map<long long, int> idx;
    idx[1000000000LL] = 7;
    if (idx.find(1000000000LL) != idx.end()) printf("大整数作键查到：%d\n", idx[1000000000LL]);

    // 7. 遍历 unordered_map 的顺序是不确定的，不要依赖
    printf("unordered_map 遍历（顺序不定）：");
    for (auto &kv : idx) printf("%lld ", kv.first);
    printf("\n");

    // 8. 竞赛实用技巧：大范围状态用 unordered_map 记忆化
    //    注意预先 reserve，避免大量插入引起反复 rehash
    unordered_map<int, long long> memo;
    memo.reserve(1 << 16);
    printf("memo.reserve 后 bucket 数：%d\n", (int)memo.bucket_count());
    return 0;
}
```

> **【易错】** 五处：
> 1. **用 `m[k] == 0` 判「不存在」** —— `m[k]` 会插入键并返回默认值 0。
>    **后果：容器越来越臃肿，遍历时多出一堆「值为 0」的假数据。**
>    判存在必须用 `find` 或 `count`。
> 2. **`unordered_map` 的遍历顺序不确定** —— 依赖顺序会得到随机结果。
>    需要有序就用 `map`，或在最后排序。
> 3. **自定义类型作 `unordered_map` 的键** —— 需要自己写哈希函数，容易出错。
>    **竞赛中优先改用 `map`（只需 `operator<`）。**
> 4. **`unordered_map` 被卡哈希** —— 某些 OJ 上存在针对性数据使其退化为 O(n)。
>    安全做法：用 `map`，或给键加一个随机偏移。
> 5. **大量插入前不 `reserve`** —— 反复 rehash 显著拖慢。

> **【类比】** `map` 像字典：按拼音顺序排好，能快速翻到某字，也能「翻到 X 之后的那一页」。
> `unordered_map` 像储物柜：有钥匙就直接开，速度最快，但柜子之间的顺序毫无意义。

> **【记忆】** **要顺序用 `map`，要速度用 `unordered_map`，判存在用 `find` 不用 `[]`。**

**关联**

- `[前置]` 见 C-3 `pair`（`map` 的元素就是 `pair<const K, V>`）、C-7 `set`（同为平衡树）。
- `[后续]` 见算法专题阶段 6「字符串哈希」（`unordered_map` 的替代方案）、阶段 7「状压 DP」（状态表）。
- `[易混]` `map` 与 `unordered_map`：见上方对照表。
- `[组合]` 与算法专题阶段 1「前缀和」组合 → 统计「和为 k 的子数组个数」。
- `[延伸]` 哈希表的实现原理（开放寻址、链地址、rehash）见 `03_常规课程`，**本轮未生成**。

---

### C-9　`bitset`　`P1`　会用　`[未学]`

> **【重点】** `bitset` 用**一个二进制位存一个布尔值**，把「集合」压缩成整数。
> 它让 O(n) 的集合操作变成 O(n/64) —— 常数直接除以 64。

**是什么**：定长位序列，支持逐位读写，也支持整体位运算。

**为什么**：三处价值 ——
1. **状态压缩**：1000 个点的「已访问」标记，用 `bool[]` 占 1000 字节，用 `bitset<1000>` 只占 125 字节。
2. **集合运算整体化**：`a & b`、`a | b`、`a ^ b` 一次算 64 位。
3. **带权图最短路中的可达性传递**（Floyd 的 bitset 优化）。

**怎么用**：

1. **大小必须是编译期常量**：`bitset<1005> vis;`。
2. 访问位：`b[i]` 可读可写，下标从 0 开始。
3. 整体操作：`set()` 全置 1、`reset()` 全置 0、`flip()` 取反、`count()` 统计 1 的个数。
4. 位运算：`&` `|` `^` `~` `<<` `>>` 直接可用。

```cpp
// g++ -std=c++17 -O2
#include <cstdio>
#include <bitset>
using namespace std;

const int N = 1005;

int main() {
    bitset<N> a, b;

    // 1. 单点置位
    a[0] = 1;   a[3] = 1;   a[7] = 1;
    b[3] = 1;   b[8] = 1;

    printf("a = %s（只看低 12 位）\n", a.to_string().substr(N - 12).c_str());
    printf("a.count() = %d\n", (int)a.count());      // 3

    // 2. 集合运算：一次算整块，比循环快
    bitset<N> c = a & b;      // 交集
    bitset<N> d = a | b;      // 并集
    bitset<N> e = a ^ b;      // 对称差
    printf("交集个数 %d，并集个数 %d，对称差个数 %d\n",
           (int)c.count(), (int)d.count(), (int)e.count());   // 1, 4, 2

    // 3. 位移：整体左移右移
    bitset<N> f = a << 1;
    printf("a<<1 的个数 %d\n", (int)f.count());

    // 4. 实用场景：可达性标记
    //    图有若干点，用 bitset 存「从某点能到达哪些点」，可整体传递
    bitset<N> reach;
    reach[2] = 1; reach[5] = 1;
    printf("能否到达 5：%d，能否到达 4：%d\n",
           (int)reach[5], (int)reach[4]);

    // 5. 与位运算的对应关系（模块 A-5）
    //    b[i] 等价于 (整数 >> i) & 1，但 bitset 不限制位宽且更易读
    printf("count 是 O(位宽/64) 而非 O(位宽)，因为按机器字并行统计\n");
    return 0;
}
```

> **【易错】** 四处：
> 1. **用运行期变量指定大小** —— `bitset<n> b;` 编译失败，必须是 `constexpr` / `const`。
> 2. **`bitset` 的 `count()` 不是 `__builtin_popcount`**，但两者都是位并行统计，都很快。
> 3. **输出整体 `bitset` 会打印全部 N 位**，前面的 0 也打出来。需要裁剪时要 `to_string()` 后 `substr`。
> 4. **以为 `bitset` 能做不定长集合**。它**定长且编译期确定**；
>    不定长请用 `set` / `unordered_set`。

> **【类比】** `bitset` 像一张**打孔的卡片**：每个孔一位，卡片上的图样可以整体比对、
> 整体叠加——而不是一个孔一个孔地看。

> **【记忆】** **`bitset` 大小编译期定死；集合运算整体一次算 64 位。**

**关联**

- `[前置]` 见 A-5 位运算、A-10 `const`（大小必须是常量）。
- `[后续]` 见 D-10 `__builtin_` 系列（编译器的位统计函数）、算法专题阶段 7「状压 DP」。
- `[易混]` `bitset` 与 `vector<bool>`：前者定长且支持整体位运算，后者是变长但行为特殊。
- `[组合]` 与算法专题阶段 5 组合 → Floyd 的 bitset 优化；与阶段 7 组合 → 状压 DP 的状态表示。

---

### C-10　容器选型决策　`P0`　理解　`[未学]`

> **【重点】** 这是本模块**唯一需要背下来**的一张表。选错容器，算法正确也会超时。

**是什么**：按「数据要做什么操作」反查容器的决策规则。

**为什么**：容器不是口味偏好。每个容器的接口设计对应一组操作代价，
选型错误的代价是数量级级别的性能差异，而不是常数级别。

**怎么用**：

| 我要做的事 | 选什么 | 复杂度 | 不要用什么 |
|-----------|--------|--------|-----------|
| 顺序存、随机访问、末尾增删 | `vector` | O(1) / 均摊 O(1) | — |
| 频繁在中间插入删除 | `list` / `set` | O(1) / O(log n) | **`vector`（O(n)）** |
| 两端增删 | `deque` | O(1) | `vector` 头部插入是 O(n) |
| 后进先出 | `stack` | O(1) | — |
| 先进先出 / BFS | `queue` | O(1) | — |
| 反复取当前最小/最大 | `priority_queue` | 顶 O(1)、增删 O(log n) | **每次扫描 `vector`（O(n)）** |
| 按值快速查找 | `unordered_map` / `unordered_set` | 平均 O(1) | **`vector` 线性查找（O(n)）** |
| 查找 + 需要有序遍历 | `map` / `set` | O(log n) | `unordered_map` |
| 查找 + 需要前驱后继 | `set` / `map` 的 `lower_bound` | O(log n) | **`unordered_map`（不支持）** |
| 动态去重 | `set` / `unordered_set` | O(log n) / 平均 O(1) | — |
| 需要删除任意元素 | `set` / `map` | O(log n) | **`priority_queue`（不支持）** |
| 位集合 / 状态压缩 | `bitset` | 整体 O(n/64) | `bool[]`（浪费 8 倍内存） |
| 字符序列 / 拆词 | `string` + `stringstream` | — | `char[]`（要靠 `strcmp`） |

**三条速判规则**：

1. **要不要「按值查」？** 要 → 关联容器（`set` / `map` 系列）；不要 → 序列容器（`vector` / `deque`）。
2. **要不要「有序」？** 要 → 树（`set` / `map`）；不要 → 哈希（`unordered_*`）。
3. **要不要「取最值」？** 要 → `priority_queue`；不要 → 其他。

```cpp
// g++ -std=c++17 -O2
// 一个选型对照的实测：n = 10^6 次查找，不同容器的差距
#include <cstdio>
#include <vector>
#include <unordered_set>
#include <set>
#include <ctime>
using namespace std;

int main() {
    const int N = 1000000;
    vector<int> v;
    v.reserve(N);
    for (int i = 0; i < N; i++) v.push_back(i * 2);

    unordered_set<int> us(v.begin(), v.end());
    set<int> s(v.begin(), v.end());

    clock_t t1 = clock();
    int hit1 = 0;
    for (int i = 0; i < N; i++) if (us.count(i) ) hit1++;
    clock_t t2 = clock();
    printf("unordered_set 查找命中 %d，用时 %.0f ms\n",
           hit1, 1000.0 * (t2 - t1) / CLOCKS_PER_SEC);

    t1 = clock();
    int hit2 = 0;
    for (int i = 0; i < N; i++) if (s.count(i)) hit2++;
    t2 = clock();
    printf("set 查找命中 %d，用时 %.0f ms\n",
           hit2, 1000.0 * (t2 - t1) / CLOCKS_PER_SEC);

    // 注意：绝对值与机器相关，但相对关系稳定——哈希是常数级，树是对数级
    return 0;
}
```

> **【规律】** 三条速判规则的记忆顺序：**先问「查不查值」，再问「要不要序」，最后问「取不取最值」**。
> 三个问题问完，容器就唯一确定了。

> **【易错】** 四处：
> 1. **需要前驱后继却选了 `unordered_map`** —— 它不支持 `lower_bound`，只能推倒重来。
> 2. **需要删除任意元素却选了 `priority_queue`** —— 不支持 `erase`，只能改结构。
> 3. **只是判存在却用了 `set`** —— 常数比 `unordered_set` 大数倍，10⁶ 次操作就差出明显时间。
> 4. **`vector` 头部频繁插入** —— 每次 O(n)。改用 `deque` 或反向存。

> **【类比】** 选容器像选交通工具：**送一件快递用摩托（`unordered_map`）**，
> **送一车货用卡车（`vector`）**，**要按路线沿途停靠就得用公交（`set`，有序）**。
> 用摩托送货没错，用摩托送货还要求沿途报站才是错。

> **【记忆】** **查值 → 有序 → 最值**：三问定容器。

**关联**

- `[前置]` 见 C-1 至 C-9 全部。
- `[后续]` 见算法专题全阶段的容器选择（阶段 3 单调栈用 `stack`、阶段 5 Dijkstra 用 `priority_queue`、阶段 6 哈希用 `map`）。
- `[组合]` 与模块 D 组合：「容器 + 算法」是解题的两条腿，缺一不可。

---

## 四、跨章关联地图

| 关联知识点 | 关系 | 说明 | 位置 |
|-----------|------|------|------|
| 数组与多维数组 | `[前置]` | `vector` 是数组的动态版本 | 模块 A-4 |
| 结构体与 `operator<` | `[前置]` | 自定义类型入 `set` / `map` 的前提 | 模块 A-7 |
| 位运算 | `[前置]` | `bitset` 的基础 | 模块 A-5 |
| `sort` 与比较器 | `[后续]` | 作用于 `vector` 的区间排序 | 模块 D-1 |
| `lower_bound` | `[易混]` | `std::lower_bound` 用于有序区间；`set` / `map` 用**成员函数** | 模块 D-3 |
| `unique` + `erase` | `[组合]` | `vector` 去重的标准写法 | 模块 D-4 |
| `auto` / 范围 for | `[后续]` | 遍历容器的标准写法 | 模块 E-1、E-2 |
| 结构化绑定 | `[组合]` | 遍历 `map` 与 `vector<pair>` 时最简洁 | 模块 E-4 |
| 运算符重载 | `[前置]` | 自定义类型入容器 | 模块 E-8 |
| 单调栈 / 单调队列 | `[组合]` | `stack` / `deque` 的算法应用 | 算法专题阶段 1、3 |
| 堆优化 Dijkstra | `[组合]` | `priority_queue` + `pair` | 算法专题阶段 5 |
| 状压 DP | `[组合]` | `bitset` 与位运算 | 算法专题阶段 7 |

**本模块在知识体系中的位置**

```text
竞赛 C++ 五阶段
├─ 阶段 1 语言基础与输入输出   （模块 A、B）
├─ 阶段 2 STL 容器            ◄── 本模块
│   ├─ 序列容器：C-1 vector / C-2 string / C-3 pair / C-6 deque
│   ├─ 适配器：  C-4 stack·queue / C-5 priority_queue
│   ├─ 关联容器：C-7 set / C-8 map
│   ├─ 位容器：  C-9 bitset
│   └─ 决策：    C-10 容器选型
├─ 阶段 3 STL 算法            （模块 D）
├─ 阶段 4 现代语法糖          （模块 E）
└─ 阶段 5 竞赛工程化          （模块 F）
```

---

## 五、本章总结

### 5.1 核心内容（一页纸）

1. **`vector` 二维是「行数 + 一个模板行」**：`vector<vector<int>> g(n, vector<int>(m))`。
2. **`v.size()` 是无符号**，参与减法前先转 `int`。
3. **`cin >>` 之后要 `getline`，先 `ignore`**。
4. **`s.find(t)` 找不到返回 `string::npos`**，不要与 `-1` 比较。
5. **`substr` 第二个参数是长度**，不是结束下标。
6. **`pair` 内置字典序比较**，写 `{优先级, 值}` 就能省掉一个比较器。
7. **`stack` / `queue` 的 `pop()` 不返回值**，先 `top` 再 `pop`；取值前先判空。
8. **`priority_queue` 默认大顶堆**，小顶堆写 `greater<T>`，中间别漏 `vector<T>`。
9. **单调栈弹出条件用 `<`，等值会互相阻挡**（算法专题阶段 3 的头号易错）。
10. **`set` / `map` 的 `lower_bound` 必须用成员函数**，用 `std::lower_bound` 会退化为线性。
11. **`m[k]` 会插入键**，判存在必须用 `find` 或 `count`。
12. **要顺序用 `map`，要速度用 `unordered_map`。**
13. **`bitset` 大小编译期定死**，集合运算一次算 64 位。
14. **选型三问：查值 → 有序 → 最值。**

### 5.2 知识点串联图

```text
            序列容器
  C-1 vector ──┬── C-2 string
               └── C-3 pair/tuple
                      │
                      ├── C-4 stack / queue ── C-6 deque
                      └── C-5 priority_queue
                             │
            关联容器          │
  C-7 set/multiset ◄─────────┘
        │
        └── C-8 map / unordered_map
                 │
                 └── C-9 bitset
                          │
                    C-10 容器选型决策（总纲）
```

### 5.3 自测清单

- [ ] 能写出 `vector<vector<int>>` 的正确开法并解释两个参数
- [ ] 能说出 `v.size() - 1` 在空容器上的后果
- [ ] 能写出「读整数后读整行」的正确代码
- [ ] 能写出 `pair` 免比较器排序的代码，并解释字典序规则
- [ ] 能写出小顶堆的完整声明（三处不能漏）
- [ ] 能写出单调栈的模板并说明为什么用 `<=` / `<`
- [ ] 能写出 `set` 求前驱后继的代码
- [ ] 能说出 `m[k]` 与 `m.find(k)` 的区别并各举一场景
- [ ] 能说出选型三问，并对五个具体场景给出容器
- [ ] 能默写滑动窗口最小值的单调队列模板

### 5.4 间隔重复表

| 知识点 | 首次 | +1 天 | +3 天 | +7 天 | +21 天 |
|--------|------|-------|-------|-------|--------|
| C-1 `vector` |  |  |  |  |  |
| C-2 `string` |  |  |  |  |  |
| C-3 `pair` / `tuple` |  |  |  |  |  |
| C-4 `stack` / `queue` |  |  |  |  |  |
| C-5 `priority_queue` |  |  |  |  |  |
| C-6 `deque` |  |  |  |  |  |
| C-7 `set` / `multiset` |  |  |  |  |  |
| C-8 `map` / `unordered_map` |  |  |  |  |  |
| C-9 `bitset` |  |  |  |  |  |
| C-10 容器选型决策 |  |  |  |  |  |

### 5.5 应落到实处的代码修改

| 问题 | 依据 | 建议 |
|------|------|------|
| `set` 零使用 | 75 文件统计 | 「动态有序集合 / 前驱后继」类题改用 `set`，见 C-7 |
| `map` / `unordered_map` 各仅 1 次 | 75 文件统计 | 计数、映射类题改用 `map` 或 `unordered_map`，见 C-8 |
| 未使用 `reserve` | 抽样观察 | 已知规模时预分配，见 C-1 |
| `vector<bool>` 出现 | 抽样观察 | 改用 `bitset`，见 C-9 |

---

## 六、本节未包含的内容

| 内容 | 归属 | 说明 |
|------|------|------|
| 容器的完整实现原理（分配器、红黑树旋转） | `03_常规课程` | 竞赛只需知道复杂度 |
| `list` / `forward_list` | `03_常规课程` | 竞赛中链表通常用数组模拟（模块 A-9） |
| 哈希表的实现细节 | `03_常规课程` | 只需知道平均 O(1) 与「可能被卡哈希」 |
| 迭代器类别与失效规则全集 | `03_常规课程` | 只需记住 `vector` 扩容后全部失效 |

> **【注意】** 上述内容指向 `03_常规课程`，**本轮未生成**。

---

## 七、复习记录

| 日期 | 复习方式 | 本次结果 | 掌握状态变更 |
|------|---------|---------|-------------|
|  |  |  |  |

---

## 八、待办与缺口

- [ ] 待补知识点：无（本模块已覆盖方案 §1.2 定义的全部 10 个知识点）
- [ ] **待补容器**：本模块按方案划定的范围只覆盖 10 个容器。
      实际竞赛还会用到 `list`（链表题）、`unordered_set`（去重提速），
      两者已在 C-7 / C-8 的【延伸】中提及，但未单列知识点。
- [ ] 待修正的既有代码：见 §5.5 的四项
- [ ] 待核实的题源：本模块为容器用法，**不单独出题**。
      练习分散在算法专题阶段 3（单调栈 / 队列）、阶段 5（Dijkstra 用堆）、
      阶段 6（哈希）的题集中。

---
## 配套题库练习

| 题号 | 题名 | 状态 |
|------|------|------|
| luogu-P1996 | 约瑟夫问题 | 未做 |
| luogu-P1090 | 合并果子 | 未做 |
| luogu-P1168 | 中位数 | 未做 |
| luogu-P2580 | 错误的点名 | 未做 |
| luogu-P5734 | 文字处理软件（string 操作） | 未做 |
| luogu-P5733 | 自动修正（string 遍历改写） | 未做 |
| luogu-P5143 | 攀爬者（pair 排序） | 未做 |
| luogu-P3916 | 图的遍历（vector 邻接表建图） | 未做 |

> 题面链接见 `_题库总表.md`（单一真源，此处只列题号）；做题后回总表更新状态，「已通过」须在 `03_题库` 的 `代码` 目录留存代码文件。

---

*模块 C 完 · 学习顺序见 `README_模块总览与学习顺序.md` · 排版规范见 `22_排版与标注规范.md`*
