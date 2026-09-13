# 《C++基础篇》第23章 STL（标准模板库）· 完整学习笔记（v3）

> 课件：23 STL.pdf（171页）| 配套代码：string and vector code/、stack queue list/、list set map/、algorithm/、表达式括号匹配.cpp
> 前置章节：第22章 模板 | 后置章节：第24章 文件操作 | 预计学习时间：9 小时
> 说明：本目录已存在旧版《STL学习笔记.md》，本版按规则另存为 _v3，不覆盖旧文件。

---

## 〇、前置知识自检

| # | 自检项 | 要点 |
|---|--------|------|
| 1 | 类模板与函数模板 | 第22章：`Test<int>` 实例化 |
| 2 | 运算符重载 | `operator()` 是仿函数的基础 |
| 3 | 引用与指针 | 迭代器行为类似指针 |
| 4 | new/delete | 容器自动管理内存，但理解底层需要 |

**本章预览**：STL 借助模板把常用数据结构和算法实现了一遍，并做到数据结构与算法分离。本章覆盖容器（string/vector/stack/queue/deque/list/set/map）、迭代器、算法三大核心。学完能根据需求选容器、用算法处理数据。

**知识蒸馏**：STL 是 C++ 的"标准零件库"：容器装数据、迭代器当手、算法干活，三者即插即用。

**容器选型决策表**（先收藏，学完全章再看细节）：

| 容器 | 底层结构 | 典型场景 | 插入/删除 | 查找 | 随机访问 |
|------|----------|----------|-----------|------|----------|
| vector | 动态数组 | 通用首选、频繁随机访问 | 尾部 O(1)，中间 O(n) | O(n) | O(1) |
| deque | 分段连续 | 两端都要增删 | 两端 O(1) | O(n) | O(1)（稍慢） |
| list | 双向链表 | 频繁中间插删 | 任意位置 O(1)（有迭代器） | O(n) | ❌ |
| stack | 适配器(deque) | 后进先出（括号匹配、进制转换） | 仅栈顶 O(1) | — | ❌ |
| queue | 适配器(deque) | 先进先出（排队、约瑟夫） | 仅两端 O(1) | — | ❌ |
| set/multiset | 红黑树 | 去重+自动排序 | O(log n) | O(log n) | ❌ |
| map/multimap | 红黑树 | 键值映射（词频、通讯录） | O(log n) | 按键 O(log n) | ❌ |
| string | 动态字符数组 | 文本处理 | 尾部 O(1) | O(n) | O(1) |

---

# 模块一：STL概述与基本组成（P1-P5）

## 知识点1：STL概述（P1-P4）【了解】

**①是什么**：STL（Standard Template Library，标准模板库）借助模板把常用数据结构及其算法实现了一遍，并做到数据结构和算法的分离。底层实现（课件原文）：vector 底层为顺序表（数组），list 底层为双向链表，deque 底层为循环队列，set 底层为红黑树，hash_set 底层为哈希表。

**生活化比喻**：STL 像"宜家家具城"——柜子（容器）、搬运小推车（迭代器）、组装工具（算法）都是现成的标准化产品，你按需挑选组合，不用自己打家具。

**②为什么**：从根本上说，STL 是"容器"的集合（list、vector、set、map 一大堆），也是算法和其他组件的集合（如 `<algorithm>` 中的 sort、`<string>` 中的 string）。复用标准组件，代码更短、更可靠。

> 人话总结：STL = 现成容器 + 现成算法，拿来就用。

## 知识点2：STL基本组成（P5）【熟悉】

**①三大核心**（课件原文归纳）：

1. **容器（Container）**：一种数据结构（list、vector、deque 等），以模板类方式提供；
2. **迭代器（Iterator）**：访问容器中对象的方法，如同指针——C++ 的指针本身也是一种迭代器；迭代器也可以是定义了 `operator*()` 等类指针操作的类对象；
3. **算法（Algorithm）**：操作容器数据的模板函数——sort 排序、find 查找；函数本身与数据结构和类型无关，从简单数组到复杂容器都能用。

**协作关系图**：

```
算法（sort/find/...）
   │ 通过
   ▼
迭代器（begin/end，像指针一样遍历）
   │ 访问
   ▼
容器（vector/list/map，存数据）
```

**容器两大分类**：
- **序列式容器**：元素按位置排列——vector、deque、list、stack、queue；
- **关联式容器**：元素按键值组织、自动排序——set/multiset、map/multimap。

**STL整体架构图**：

```
                STL
 ┌──────────┬──────────┬──────────┐
 容器        迭代器       算法
 ├序列式     ├输入/输出    ├遍历 for_each/transform
 │ vector    ├前向        ├查找 find/find_if/binary_search
 │ deque     ├双向        ├排序 sort/merge/reverse
 │ list      └随机访问     ├拷贝替换 copy/replace
 │ stack/queue(适配器)    ├算术 accumulate/fill（<numeric>）
 └关联式                   └集合 set_intersection/union/difference
   set/map（红黑树）
 另有：仿函数（<functional>）、适配器、空间配置器
```

**③怎么用**（三大组件协作的最小例子）：

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    vector<int> v = { 3, 1, 2 };        // 容器
    sort(v.begin(), v.end());           // 算法通过迭代器操作容器
    for (auto it = v.begin(); it != v.end(); it++)  // 迭代器遍历
        cout << *it << " ";             // 输出：1 2 3
    return 0;
}
```

> 人话总结：容器装、迭代器指、算法算。

---

# 模块二：string容器 + vector容器（P6-P39）

## 知识点3：string容器（P6-P22）【重点】

**①是什么**：C++ 标准库设计的专门处理字符串的数据类型（须含头文件 `<string>`）。课件原文：用字符数组存放字符串容易发生越界且难以察觉，string 用法更简单、不容易出错，编程时应优先使用。

**生活化比喻**：char 数组像手拎一串散钥匙（容易丢、数不清），string 像带自动伸缩的钥匙包——长度、增删、比较都替你管好。

**②为什么**：自动管理内存（不怕越界）、功能丰富（拼接/查找/替换/比较一站式）、与 STL 算法无缝配合。

**③怎么用**——按课件顺序逐个操作：

**初始化（P7-P8）**：

```cpp
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s1;                  // 默认初始化：空字符串
    string s2(s1);              // s2 是 s1 的副本
    string s3 = s1;             // 等价于 s3(s1)
    string s4("hello");         // 字面值构造
    string s5 = "hello";        // 等价于上行
    string s6(5, 'a');          // 5 个连续 'a'："aaaaa"
    string s7 = string("hello");// 临时 string 再初始化
    cout << s6 << endl;         // 输出：aaaaa
    return 0;
}
```

**输入输出（P9）**：

```cpp
string s1;
cin >> s1;          // 遇空格终止
getline(cin, s1);   // 读取整行（VS 中须 #include <string>）
```

**比较大小（P10）**：直接用 `>`、`<`、`==`，按字典序逐字符比较。

```cpp
string s1 = "abc", s2 = "eda";
cout << (s1 > s2) << endl;   // 输出：0（"abc" < "eda"）
cout << (s1 < s2) << endl;   // 输出：1
```

**拼接（P11）**：`+` 直接链接。

```cpp
string s1 = "hello", s2 = " world";
string s3 = s1 + s2;         // "hello world"
s1 += s2;                    // 追加
s1.append("!!");             // append 在末尾插入（P18）
```

**获取字符（P12-P13）** 三种方式：

```cpp
string s1 = "abcdefg";
for (auto c : s1) cout << c << " ";            // ① C++11 范围 for
for (size_t i = 0; i < s1.size(); i++) s1[i];  // ② 下标 + size()
for (auto i = s1.begin(); i != s1.end(); i++)  // ③ 迭代器
    cout << *i << " ";
```

**子串拷贝构造（P14）**：`string s(s1, pos)` / `string s(s1, pos, len)`。

```cpp
string s1("hello");
string s2(s1, 1);      // "ello"，长度4
string s3(s1, 5);      // ""，长度0（pos == size 合法）
// string s8(s1, 6);   // 错误！pos > size 是未定义行为，抛异常
string s4(s1, 1, 3);   // "ell"，长度3
string s5(s1, 1, 8);   // "ello"，长度4（len 超出只取到结尾，合法）
```

**substr（P15）**：`s.substr(pos, n)` 返回从 pos 开始的 n 个字符，两参数均可省。

```cpp
string s("value");
string s2 = s.substr();      // "value"
string s3 = s.substr(2);     // "lue"
string s6 = s.substr(1, 2);  // "al"
// s.substr(6) → 错误（pos 超出）
```

**insert（P16）** 四种形态：

```cpp
string s1("value");
s1.insert(s1.begin(), 's');                     // "svalue"
s1.insert(s1.begin(), 1, 's');                  // "ssvalue"
s1.insert(s1.begin(), s1.begin(), ++s1.begin());// "sssvalue"
s1.insert(s1.end(), {'1','2'});                 // "sssvalue12"
```

**erase（P17）** 三种形态：

```cpp
string s1("value"), s2("value"), s3("value"), s4("value");
s1.erase();                          // 全删，s1 为空
s2.erase(0, 2);                      // "lue"（从下标0删2个）
s3.erase(s3.begin());                // "alue"（删迭代器位置）
s4.erase(s4.begin(), ++s4.begin());  // "alue"（删区间）
```

**replace（P19）**：删除一段再原地插入。

```cpp
string s("i very love China!");
s.replace(2, 4, "truly");      // "i truly love China!"（下标2起删4个，插入truly）
s.replace(2, 6, 4, '*');        // 把 6 个字符换成 4 个 '*'："i **** love China!"
```

**练习（P21-P22）：去除字符串中的标点符号**（用 `ispunct()` 判断）：

```cpp
#include <iostream>
using namespace std;
int main() {
    string s;
    cin >> s;
    for (auto each : s) {
        if (!ispunct(each)) cout << each;   // 非标点才输出
    }
    return 0;
}
// 输入：hello,world!  输出：helloworld
```

**string vs char[] 对比表**：

| 维度 | string | char[] |
|------|--------|--------|
| 内存管理 | 自动扩容/释放 | 手动算长度，易越界 |
| 安全性 | 高（可用 at 抛异常） | 低（越界不报错） |
| 功能 | 拼接/查找/替换/比较全套 | 靠 `<cstring>` 函数拼凑 |
| 性能 | 略有开销（可 SSO 优化） | 极致轻量 |
| 兼容 | 可用 `s.c_str()` 转 C 字符串 | 可构造 string |

**互转代码**：

```cpp
string s = "hello";
const char* p = s.c_str();     // string → C 字符串
char arr[] = "world";
string s2(arr);                // C 字符串 → string
```

**④注意事项**：

```cpp
// 错误示范：substr/拷贝构造的 pos 超过 size() → 未定义行为/抛异常
// string bad = s.substr(100);   // 错！
// 正确：先判断 pos < s.size()
```

> 人话总结：string 管字符串，越界拼接全自动。

## 知识点4：vector容器（P23-P39）【重点】

**①是什么**：能存放任意类型的**动态数组**容器（须含 `<vector>`）。同一种类型的对象的集合，标准库负责管理内存。

**生活化比喻**：普通数组是定长的鸡蛋托，vector 是会自动换大托的鸡蛋盒——装满了自动换更大的盒子，还告诉你当前装了几个。

**内部结构图**（连续内存 + 三指针）：

```
vector 对象                堆上连续内存
┌─────────────┐           ┌───┬───┬───┬───┬───┬───┬───┐
│ start ────────────────→ │ 1 │ 2 │ 3 │...│   │   │   │
│ finish ─────────────────└───┴───┴───┘  ↑               │
│ end_of_storage ─────────────────────────┘（已分配末尾） │
└─────────────┘
size = finish - start；capacity = end_of_storage - start
```

**②为什么**：需要"长度可变的数组"——元素个数运行时才确定、频繁尾部追加；数组做不到，链表随机访问太慢，vector 是折中最优解。

**③怎么用**：

**声明与初始化（P25-P26）**：

```cpp
#include <iostream>
#include <vector>
using namespace std;
int main() {
    vector<int> vec = { 1,2,3,4,5 };        // 列表初始化
    vector<char> vec1 = {'h','e','l','l','o'};
    vector<double> vec2 = {1.1, 2.2, 3.3};
    vector<int> a(10);        // 10 个元素，默认 0
    vector<int> b(10, 2);     // 10 个元素，都是 2
    vector<int> c(b);         // 拷贝构造
    vector<int> d(b.begin(), b.begin() + 3);  // 区间构造：前3个
    cout << a.size() << " " << b[0] << endl;  // 输出：10 2
    return 0;
}
```

**遍历与访问（P27-P28）**：

```cpp
vector<int> v = { 1,2,3,4,5,6 };
cout << v.at(1) << endl;     // 2（at 带越界检查，抛异常）
cout << v.front() << endl;   // 1
cout << v.back() << endl;    // 6
for (auto i = v.begin(); i != v.end(); i++) cout << *i << " ";  // 1 2 3 4 5 6
for (auto i = v.rbegin(); i != v.rend(); i++) cout << *i << " "; // 6 5 4 3 2 1（反向）
```

**插入（P29-P30）**：

```cpp
vector<int> v = { 1,2 };
vector<int> v2 = { 100,200 };
v.push_back(3);                        // 尾部追加：1 2 3
v.insert(v.begin(), 11);               // 头部插11：11 1 2 3
v.insert(v.begin() + 1, 3, 22);        // 插3个22：11 22 22 22 1 2 3
v.insert(v.begin(), v2.begin(), v2.end()); // 插入v2全部：100 200 11 22 22 22 1 2 3
```

**删除（P31-P32）**：

```cpp
vector<int> v = { 1,2,3,4,5,6 };
v.erase(v.begin() + 1);               // 删除元素2
v.erase(v.begin() + 2, v.begin() + 4);// 删除区间[2,4)
v.pop_back();                          // 删尾元素
v.clear();                             // 清空
```

**判断与大小（P33-P35）**：

```cpp
vector<int> v = { 1,2,3,4,5,6 };
cout << v.empty() << endl;      // 0（非空）
cout << v.size() << endl;       // 6（元素个数）
cout << v.capacity() << endl;   // 当前容量（≥size）
cout << v.max_size() << endl;   // 理论最大元素数
```

**赋值与交换（P36-P37）**：

```cpp
vector<int> v;
v.assign(4, 2);                    // 4 个元素全是 2
vector<int> v1 = {1,2,3,4,5,6}, v2 = {11,22,33};
v2.assign(v1.begin(), v1.end());   // v2 变成 1 2 3 4 5 6
v1.swap(v2);                       // 交换两容器内容
```

**案例（P38-P39）：随机 n 个 1-100 数字装 vector，求最大最小值**：

```cpp
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <vector>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<int> v;
    srand(time(0));
    for (int i = 1; i <= n; i++)
        v.push_back(rand() % 100 + 1);   // 随机 1~100 入容器
    int max = v[0], min = v[0];
    for (int i = 0; i < n; i++) {
        if (max < v[i]) max = v[i];
        if (min > v[i]) min = v[i];
    }
    cout << max << "  " << min << endl;
    return 0;
}
```

**扩容机制与迭代器失效**：

```
push_back 时若 size == capacity：
  ① 申请更大内存（通常 2 倍或 1.5 倍）
  ② 把旧元素搬过去
  ③ 释放旧内存 ← 旧地址作废！
```

⚠️ **迭代器失效警告框**：

```cpp
// 错误示范：扩容后旧迭代器悬空
vector<int> v;
auto it = v.begin();
for (int i = 0; i < 1000; i++) v.push_back(i);  // 多次扩容，it 早已失效
// *it = 1;   // 未定义行为！
// 正确做法1：先 reserve 预留
vector<int> v2; v2.reserve(1000);
// 正确做法2：插入后重新取迭代器
// 正确做法3：用 erase 的返回值：it = v.erase(it);
```

**reserve vs resize**：reserve 只扩 capacity 不增元素；resize 直接改 size（多出的元素填默认值）。

**④注意事项**：`v[下标]` 不检查越界，`v.at(下标)` 检查并抛 `out_of_range`——越界场景用 at。

> 人话总结：vector 动态数组，尾部快、随机快，扩容搬家迭代器作废。

[✅ 模块1/6 已完成]
[✅ 模块2/6 已完成]

---

# 模块三：stack + queue + deque容器（P40-P70）

## 知识点5：stack容器（P40-P47）【重点】

**①是什么**：先进后出（LIFO）的容器，只有一个开口，只能从这一端插入和删除。头文件 `<stack>`。stack 是**容器适配器**——默认基于 deque 实现，套上一层"只许走栈顶"的规则。

**生活化比喻**：一摞盘子——最后放上去的最先被拿走；或者弹夹——后压进去的子弹先打出去。

```
栈顶 → ┌─────┐
       │ 333 │ ← push 从这里进，pop 从这里出
       │ 222 │
       │ 111 │
栈底 → └─────┘
（适配器包装：stack<T> 包住 deque<T>，只开放 push/pop/top）
```

**②为什么**：有些场景只需要"最近一个"——撤销操作、括号匹配、进制转换、函数调用栈。限制访问面反而让逻辑更清晰安全。

**③怎么用**：

```cpp
#include <iostream>
#include <stack>
using namespace std;
int main() {
    stack<int> s;          // 默认构造
    s.push(111);           // 入栈
    s.push(222);
    s.push(333);
    s.pop();               // 弹出 333
    int n = s.top();       // n = 222（只看不删）
    cout << n << endl;     // 输出：222
    cout << s.empty() << endl;  // 0（非空）
    cout << s.size() << endl;   // 2
    return 0;
}
```

**stack 不提供迭代器**——设计意图就是限制只能从栈顶操作，遍历会破坏 LIFO 语义。

**案例（P46-P47）：十进制转二进制**——余数入栈再倒序输出：

```cpp
#include <iostream>
#include <stack>
using namespace std;
int main() {
    stack<int> s;
    int n;
    cin >> n;                  // 输入：13
    while (n) {                // 循环取余，余数入栈
        s.push(n % 2);
        n /= 2;
    }
    while (!s.empty()) {       // 出栈即逆序 → 正好是二进制从高位到低位
        cout << s.top();
        s.pop();
    }                          // 输出：1101
    return 0;
}
```

**指定底层容器**：`stack<int, vector<int>> stk;`（默认是 deque）。

> 人话总结：栈是一摞盘子，后进先出，只有顶能碰。

## 知识点6：queue容器（P48-P54）【重点】

**①是什么**：先进先出（FIFO）的容器，两个出口——队尾入队、队头出队。头文件 `<queue>`，同样是容器适配器（默认基于 deque）。

**生活化比喻**：食堂排队窗口——先来先打饭；只有队头和队尾对外可见，不允许插队（遍历）。

```
队头（front，出队）← [111][222][333] ← 队尾（back，入队）
```

**②为什么**：任务排队、消息缓冲、层序遍历、约瑟夫问题——凡"先来先服务"就用 queue。

**③怎么用**：

```cpp
#include <iostream>
#include <queue>
using namespace std;
int main() {
    queue<int> q1;
    q1.push(111);              // 入队
    q1.push(222);
    q1.push(333);
    cout << q1.size() << endl; // 输出：3
    int first = q1.front();    // 111
    int end = q1.back();       // 333
    q1.pop();                  // 移除队头 111
    while (!q1.empty()) {
        cout << q1.front() << " ";
        q1.pop();
    }                          // 输出：222 333
    return 0;
}
```

**stack vs queue 对比**：

| 对比项 | stack | queue |
|--------|-------|-------|
| 语义 | 后进先出 | 先进先出 |
| 操作端 | 仅栈顶 | 队尾进、队头出 |
| 查看元素 | top() | front() / back() |
| 典型场景 | 括号匹配、撤销 | 排队、任务调度 |
| 迭代器 | 均不提供 | 均不提供 |

**案例（P53-P54）：扑克牌问题**（奇数张输出、偶数张放回队尾）——输入 4 张牌 1 2 3 4，输出 1 3 2 4：

```cpp
#include <iostream>
#include <queue>
using namespace std;
int main() {
    int n, num;
    cin >> n;
    queue<int> q;
    for (int i = 0; i < n; i++) { cin >> num; q.push(num); }
    bool b = 1;                        // 报数开关
    while (!q.empty()) {
        if (b) {                       // 奇数次：输出并丢弃
            cout << q.front() << " ";
            q.pop();
        } else {                       // 偶数次：放回队尾
            q.push(q.front());
            q.pop();
        }
        b = !b;                        // 翻转开关
    }                                  // 输入 4 / 1 2 3 4 → 输出：1 3 2 4
    return 0;
}
```

**priority_queue 简述**：优先队列（默认大顶堆），每次取出的是最大元素，底层是堆结构，常用于 Top-K、合并有序序列。

> 人话总结：队列排队，先来先走，只碰头尾。

## 知识点7：deque容器（P55-P70）【重点】

**①是什么**：双端队列——头尾两端都能高效插入删除，还支持随机访问。头文件 `<deque>`。

**生活化比喻**：两头开门的走廊——前后门都能进出；而 vector 是一头开门的隧道（只能尾部快），普通队列是只开两扇小窗。

**内部结构图**（分段连续：中控器 + 缓冲区）：

```
中控器 map（指针数组）
┌───┬───┬───┬───┐
│ ● │ ● │ ● │   │
└┬──┴┬──┴┬──┴───┘
 ↓   ↓   ↓
[缓冲区][缓冲区][缓冲区]   ← 每段固定大小的连续内存
 数据分布在多个缓冲区中，逻辑上连成一体
```

**②为什么**：
- 为什么不用 vector？vector 头部插入 O(n)（要搬全部元素），deque 头部 O(1)；
- 为什么不用 list？deque 支持 O(1) 随机访问；
- 为什么 stack/queue 默认底层是 deque？因为它两头都快、又能按需取用，两头一锁就是栈/队列。

**③怎么用**：

**构造（P57-P58）**：

```cpp
deque<int> a;                    // 默认构造
deque<int> a2(10);               // 10 个元素
deque<int> a3(10, 1);            // 10 个 1
deque<int> b(a2);                // 拷贝
deque<int> c(a3.begin(), a3.begin() + 3);  // 区间拷贝
```

**两端增删与任意位置插入（P59-P62）**：

```cpp
#include <iostream>
#include <deque>
using namespace std;
int main() {
    deque<int> d1;
    d1.push_front(4);          // 头部加：4
    d1.push_back(5);           // 尾部加：4 5
    deque<int>::iterator it = d1.begin();
    d1.insert(it, 2);          // 头部插2：2 4 5
    it = d1.begin();
    d1.insert(it, 3, 9);       // 插3个9：9 9 9 2 4 5
    deque<int> d2(5, 8);
    it = d1.begin();
    d1.insert(it, d2.end() - 1, d2.end());  // 插 d2 最后一个 8
    for (it = d1.begin(); it != d1.end(); it++)
        cout << *it << " ";    // 输出：8 9 9 9 2 4 5
    return 0;
}
```

**删除**：`pop_front()/pop_back()/erase(it)/erase(first,last)/clear()`。

**访问（P63-P64）**：

```cpp
deque<int> d1;
for (int i = 0; i < 6; i++) d1.push_back(i);
cout << d1[0] << endl;      // 0（不查越界）
cout << d1.at(0) << endl;   // 0（查越界，抛 out_of_range）
cout << d1.front() << endl; // 0
cout << d1.back() << endl;  // 5
```

**容量（P65-P66）**：`size()/max_size()/resize()/empty()/shrink_to_fit()`。

**assign 与 swap（P67-P68）**：`d.assign(3, 1)` 赋值 3 个 1；`d1.swap(d2)` 交换。

**练习（P69-P70）：VIP 插队**——deque 头部放 VIP，尾部排普通客人：

```cpp
#include <iostream>
#include <deque>
using namespace std;
class Guest {
public:
    string name;
    bool vip;
    Guest(string name, bool vip) { this->name = name; this->vip = vip; }
};
int main() {
    Guest guest1("小明", false), guest2("小华", false), vipGuest("小张", true);
    deque<Guest> dq;
    dq.push_front(vipGuest);   // VIP 到队头
    dq.push_back(guest1);      // guest1 排 guest2 前
    dq.push_back(guest2);
    for (Guest g : dq) cout << g.name << " ";  // 输出：小张 小明 小华
    return 0;
}
```

**④注意事项**：

```cpp
// 错误示范：deque 中间插入/删除会使所有迭代器失效（比 vector 更狠）
// 正确：中间操作后重新取迭代器
// 性能认知：deque 随机访问比 vector 略慢（要先查中控器再进缓冲区）
```

> 人话总结：deque 两头都快，随机访问也行，栈和队列的底座。

---

# 模块四：list容器 + set/multiset容器（P71-P100）

## 知识点8：list容器（P71-P89）【重点】

**①是什么**：序列式容器，功能与双向链表极其相似——元素靠指针串成逻辑线性表，任一位置插入删除都快速。头文件 `<list>`。

**生活化比喻**：火车车厢——每节车厢知道前一节和后一节（prev/next），中途加挂/摘除车厢不用挪动其他车厢；但要找第 5 节得从头数（不支持随机访问）。

**节点结构图**（双向循环链表 + 哨兵）：

```
        ┌──────────────────────────────────┐
        ↓                                  │
 ┌────────────┐   ┌────────────┐   ┌────────────┐
 │prev│data│next│ ⇄ │prev│data│next│ ⇄ │prev│data│next│
 └────────────┘   └────────────┘   └────────────┘
        ↑                                  │
        └────────────（尾结点 next 指回哨兵/头）──┘
哨兵节点：begin() 指向第一个元素，end() 指向哨兵
```

**②为什么**：频繁在中间插入/删除（链表 O(1) vs vector O(n) 搬移）、元素顺序经常调整（排序、合并、反转都不搬内存）。代价：不能随机访问、每个节点多两个指针的内存开销。

**③怎么用**：

**初始化（P73）**：

```cpp
list<int> l1;                    // 空链表
list<int> l2(10);                // 10 个空元素
list<int> l3(5, 20);             // 5 个 20
list<int> l4(l3.begin(), l3.end()); // 区间拷贝
list<int> l5(l4);                // 拷贝构造
```

**迭代器遍历（P74）**：

```cpp
list<int> li = {1,2,3,4,5,6};
for (list<int>::iterator it = li.begin(); it != li.end(); it++)
    cout << *it << ' ';    // 输出：1 2 3 4 5 6
```

⚠️ **警告：list 是双向迭代器，不支持 `it + n`**，也不能用需要随机访问迭代器的 `std::sort`——排序要用成员函数 `li.sort()`。

**两端增删（P77-P78）**：`push_front/pop_front/push_back/pop_back`。

**任意位置插入（P79-P80）**：

```cpp
li.insert(li.begin(), 100);      // 头部插 100
li.insert(li.begin(), 3, 200);   // 头部插 3 个 200
list<int> k(2, 50);
li.insert(li.begin(), k.begin(), k.end());  // 插入整个 k
```

**删除（P81）**：`erase(position)` / `erase(first, last)`，自动缩减空间。

**排序（P82-P84）**（list 自带 sort，支持自定义比较）：

```cpp
#include <iostream>
#include <list>
using namespace std;
int cmp(const int& a, const int& b) { return a > b; }  // 降序
int main() {
    list<int> li;
    for (int i = 10; i >= 6; i--) li.push_back(i);  // 10 9 8 7 6
    li.push_front(3);    // 3 10 9 8 7 6
    li.push_back(20);    // 3 10 9 8 7 6 20
    list<int> li2(li);
    li.sort();           // 默认升序：3 6 7 8 9 10 20
    li2.sort(cmp);       // 自定义降序：20 10 9 8 7 6 3
    return 0;
}
```

**reverse（P84）**：`li.reverse()` 反转元素顺序。

**函数大全（P85-P86）**：assign/back/begin/clear/empty/end/erase/front/insert/max_size/merge（合并）/pop_back/pop_front/push_back/push_front/rbegin/remove/remove_if（条件删除）/rend/resize/reverse/size/sort/splice（拼接）/swap/unique（去相邻重复）。

**练习（P87-P89）：Person 排序**（年龄升序，年龄相同按身高降序）：

```cpp
#include <iostream>
#include <list>
#include <string>
using namespace std;
class Person {
public:
    Person(string name, int age, int height) {
        m_age = age; m_height = height; m_name = name;
    }
    int m_age; int m_height; string m_name;
};
bool compare(Person& p1, Person& p2) {
    if (p1.m_age == p2.m_age)
        return p1.m_height > p2.m_height;   // 年龄相同：身高降序
    return p1.m_age < p2.m_age;             // 否则：年龄升序
}
int main() {
    list<Person> L;
    L.push_back(Person("唐僧", 35, 175));
    L.push_back(Person("孙悟空", 45, 100));
    L.push_back(Person("猪八戒", 40, 170));
    L.push_back(Person("沙悟净", 40, 190));
    L.sort(compare);   // 结果：唐僧(35) → 沙悟净(40,190) → 猪八戒(40,170) → 孙悟空(45)
    for (auto it = L.begin(); it != L.end(); it++)
        cout << (*it).m_name << " " << (*it).m_age << " " << (*it).m_height << endl;
    return 0;
}
```

**④注意事项**：

```cpp
// 错误示范：对 list 用全局 sort
// std::sort(li.begin(), li.end());   // 编译错误！需要随机访问迭代器
// 正确：li.sort();
// 迭代器失效：list 只有被 erase 的节点的迭代器失效，其他节点不受影响（比 vector 温和）
```

> 人话总结：list 链表，中间插删快，排序用自带，跳着访问不行。

## 知识点9：set/multiset容器（P90-P100）【重点】

**①是什么**：关联式容器，底层为二叉树（红黑树）。特点：**插入时自动排序**。区别：set 不允许重复元素，multiset 允许。

**生活化比喻**：自动整理的名片夹——每放入一张名片，夹子自动按姓氏拼音排好位置；同名名片（set）会被拒收，（multiset）则照单全收。

**红黑树节点结构示意**：

```
        [30 黑]
        /      \
   [10 红]    [40 红]
   每个节点：key + color + left + right + parent
   性质保证树大致平衡 → 查找/插入/删除都是 O(log n)
```

**②为什么**：需要"去重 + 有序 + 快速查找"三合一——统计不重复的元素、维护有序集合；查找 O(log n) 远优于线性容器 O(n)。

**③怎么用**：

**构造与插入（P91-P92）**（set 只有 insert 一种插入方式）：

```cpp
#include <iostream>
#include <set>
using namespace std;
int main() {
    set<int> s1;
    s1.insert(10);
    s1.insert(40);
    s1.insert(30);
    s1.insert(20);
    s1.insert(30);        // 重复！插入失败，静默忽略
    for (auto it = s1.begin(); it != s1.end(); it++)
        cout << *it << " ";    // 输出：10 20 30 40（自动升序+去重）
    set<int> s2(s1);      // 拷贝构造
    set<int> s3;
    s3 = s2;              // 赋值
    return 0;
}
```

**删除（P93-P94）**：

```cpp
s1.erase(s1.begin());   // 删迭代器所指
s1.erase(30);           // 删值为 30 的元素
s1.clear();             // 清空（等价 erase(begin, end)）
```

**大小与交换（P95-P96）**：`size()/empty()/swap()`。

**查找与统计（P97-P98）**：

```cpp
set<int>::iterator pos = s1.find(30);   // 找到返回迭代器，否则返回 end()
if (pos != s1.end()) cout << "找到:" << *pos << endl;
int num = s1.count(30);   // set 中 count 只能是 0 或 1（不允许重复）
```

**set vs multiset（P99-P100）**：

| 对比项 | set | multiset |
|--------|-----|----------|
| 重复元素 | 不允许（插入被忽略） | 允许 |
| insert 返回值 | pair<迭代器, bool>（bool 表成功） | 总是成功 |
| count | 0 或 1 | 实际个数 |
| find | 唯一元素 | 返回第一个匹配 |

```cpp
multiset<int> ms;
ms.insert(10); ms.insert(20); ms.insert(10); ms.insert(20);
ms.insert(30); ms.insert(50);
// 自动排序为 {10,10,20,20,30,50}
cout << ms.count(20) << endl;   // 输出：2
```

**自定义排序**（第三模板参数传仿函数）：

```cpp
struct Greater { bool operator()(int a, int b) const { return a > b; } };
set<int, Greater> s;   // 降序排列
```

**④注意事项**：

```cpp
// 错误示范：想改 set 里的元素值
// *it = 100;   // 不允许！set 元素是 const 的（改值会破坏树的有序性）
// 正确：先 erase 再 insert 新值
// set vs unordered_set：set 有序 O(log n)；unordered_set 哈希无序、平均 O(1)
```

> 人话总结：set 自动排序又去重，查找对数级，元素不能改。

---

# 模块五：map/multimap容器（P101-P117）

## 知识点10：map/multimap容器（P101-P117）【重点】

**①是什么**：关联式容器，所有元素都是 **pair**——第一个元素是 key（键，起索引作用），第二个是 value（实值）；所有元素按键自动排序。底层二叉树（红黑树）。区别：map 的 key 不可重复，multimap 可以。

**生活化比喻**：字典——查词（key）直接翻到释义（value）；字典里同一个词只有一个词条（map），通讯录里同名的人可以有多个（multimap）。

**节点结构**：

```
红黑树节点 = pair<const Key, Value>
        [2→20]
        /    \
   [1→10]   [3→30]
按键（key）组织，中序遍历即按键升序
```

**②为什么**：需要根据"名字"快速找"值"——词频统计、学号→成绩、配置项。按键查找 O(log n)，且天然有序输出。

**③怎么用**：

**pair 对组（P102-P106）**（头文件 `<utility>`）：

```cpp
#include <iostream>
#include <utility>
using namespace std;
int main() {
    pair<string, int> p("公孙离", 17);
    cout << "姓名:" << p.first << " 年岁:" << p.second << endl;
    pair<char, float> p1 = make_pair('p', 3.14f);  // make_pair 免写类型
    cout << p1.first << " " << p1.second << endl;
    pair<int, int> p2;
    p2 = make_pair(10, 20);   // 整体赋值
    return 0;
}
```

**构造与插入（P107-P108）**：

```cpp
#include <iostream>
#include <map>
using namespace std;
int main() {
    map<int, int> m;
    m.insert(pair<int, int>(1, 10));   // 插入方式1：pair 构造
    m.insert(pair<int, int>(3, 30));
    m.insert(pair<int, int>(4, 40));
    m.insert(pair<int, int>(2, 20));   // 按 key 自动升序
    for (auto it = m.begin(); it != m.end(); it++)
        cout << "key=" << it->first << " value=" << it->second << endl;
    // 输出：1→10  2→20  3→30  4→40
    map<int, int> m2(m);    // 拷贝构造
    map<int, int> m3;
    m3 = m2;                // 赋值
    return 0;
}
```

**四种插入方式（P113）**：

```cpp
map<int, int> m;
m.insert(pair<int, int>(1, 10));              // 方式1
m.insert(make_pair(2, 20));                   // 方式2
m.insert(map<int, int>::value_type(3, 30));   // 方式3（不建议）
m[4] = 40;                                    // 方式4：[] 最简（但见下方陷阱）
```

⚠️ **[] 运算符的双重行为陷阱**：`m[key]` 在 key 存在时返回 value 的引用；**不存在时悄悄插入一个默认值的键值对**！

```cpp
// 错误示范：用 [] 判断 key 是否存在
// if (m[100] != 0) ...   // 若 100 不存在，这行会插入 {100, 0}，map 被污染！
// 正确：查存在用 find()/count()/at()（at 不存在时抛异常）
```

**删除（P112-P113）**：

```cpp
m.erase(m.begin());   // 按迭代器
m.erase(3);           // 按 key
m.clear();            // 全删（等价 erase(begin, end)）
```

**查找与统计（P114-P115）**：

```cpp
map<int, int>::iterator pos = m.find(3);   // 找不到返回 m.end()
if (pos != m.end())
    cout << "key=" << pos->first << " value=" << pos->second << endl;
int num = m.count(3);   // map 中 key 不重复，结果只有 0 或 1
```

**multimap：一键多值（P116-P117）**（一个学生多门成绩）：

```cpp
#include <iostream>
#include <string>
#include <map>
using namespace std;
int main() {
    multimap<string, int> m_map;
    string name = "XiaoMing";
    m_map.insert(make_pair(name, 50));
    m_map.insert(make_pair(name, 55));
    m_map.insert(make_pair(name, 60));
    m_map.insert(make_pair("zhangsan", 30));
    // find 返回第一个匹配，count 得到个数，连续遍历
    auto it = m_map.find(name);
    for (int k = 0; k < m_map.count(name); k++, it++)
        cout << it->first << "--" << it->second << endl;
    // 输出：XiaoMing--50 / XiaoMing--55 / XiaoMing--60
    return 0;
}
```

**实际应用场景**：词频统计（单词→次数）、通讯录（姓名→号码）、成绩排名（分数→名单）。词频统计示例：

```cpp
#include <iostream>
#include <map>
#include <sstream>
#include <string>
using namespace std;
int main() {
    string text = "to be or not to be";
    map<string, int> freq;
    stringstream ss(text);
    string word;
    while (ss >> word) freq[word]++;      // [] 不存在即建，存在即累加
    for (auto& kv : freq)
        cout << kv.first << ": " << kv.second << endl;
    // 输出（按键排序）：be:2  not:1  or:1  to:2
    return 0;
}
```

**④注意事项**：

```cpp
// 错误示范：map 插入重复 key
m.insert(make_pair(1, 10));
m.insert(make_pair(1, 99));   // 插入失败！1 已有值，不会覆盖（与 [] 行为不同）
```

**map vs unordered_map**：map 红黑树、有序、O(log n)；unordered_map 哈希表、无序、平均 O(1)。需要有序输出选 map，只要快选 unordered。

> 人话总结：map 按键找值自动排序，查重用 find 别用中括号。

[✅ 模块3/6 已完成]
[✅ 模块4/6 已完成]
[✅ 模块5/6 已完成]

---

# 模块六：STL常用算法（P118-P166）

## 知识点11：STL常用算法（P118-P166）【重点】

**①是什么**：算法由三个头文件组成（课件原文）：
- `<algorithm>`：最大的算法头文件——比较、交换、查找、遍历、复制、修改等；
- `<numeric>`：很小，几个序列上的简单数学运算模板函数；
- `<functional>`：定义模板类，用于声明函数对象（仿函数）。

**统一接口设计**：所有算法都通过**迭代器区间** `[beg, end)` 操作容器——算法不认识容器，只认迭代器，这就是"算法与数据结构分离"。

**生活化比喻**：算法像"通用家电"，迭代器是"标准插座"——只要容器提供合格的插座（迭代器），任何家电（算法）都能插上干活。

**仿函数与谓词**：
- **仿函数（函数对象）**：重载了 `operator()` 的类对象，用起来像函数，例如 `print02()`；
- **谓词**：返回 bool 的仿函数/函数。一元谓词（一个参数，如 `GreaterFive`）用于 find_if；二元谓词（两个参数，如 `greater<int>`）用于 sort。

**③怎么用——六类算法逐一演示**：

### 1) 遍历算法（P119-P123）

**for_each**（普通函数与仿函数两种写法）：

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
void print01(int val) { cout << val << " "; }   // 普通函数
class print02 {                                  // 仿函数
public:
    void operator()(int val) { cout << val << " "; }
};
int main() {
    vector<int> v;
    for (int i = 0; i < 10; i++) v.push_back(i);
    for_each(v.begin(), v.end(), print01);    // 传函数名
    cout << endl;
    for_each(v.begin(), v.end(), print02());  // 传仿函数对象
    // 均输出：0 1 2 3 4 5 6 7 8 9
    return 0;
}
```

**transform**（搬运并变换到另一容器）：

```cpp
class Transform {
public:
    int operator()(int v) { return v + 100; }   // 每个元素+100
};
int main() {
    vector<int> v;
    for (int i = 0; i < 10; i++) v.push_back(i);
    vector<int> vTarget;
    vTarget.resize(v.size());   // 目标容器必须提前开辟空间！
    transform(v.begin(), v.end(), vTarget.begin(), Transform());
    for_each(vTarget.begin(), vTarget.end(), [](int x){ cout << x << " "; });
    // 输出：100 101 102 ... 109
    return 0;
}
```

### 2) 查找算法（P124-P136）

| 算法 | 功能 | 原型要点 |
|------|------|----------|
| find | 按值查找 | 找到返回迭代器，否则 end() |
| find_if | 按条件查找 | 传入谓词 |
| adjacent_find | 相邻重复元素 | 返回第一组重复的首个位置 |
| binary_search | 二分查找（要求有序） | 返回 bool |
| count | 统计个数 | 返回 int |
| count_if | 按条件统计 | 传入谓词 |

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
class GreaterFive {
public:
    bool operator()(int val) { return val == 5; }   // 一元谓词
};
int main() {
    vector<int> v;
    for (int i = 0; i < 10; i++) v.push_back(i);
    auto it = find(v.begin(), v.end(), 9);
    cout << (it == v.end() ? "not found" : "found") << endl;   // found
    auto it2 = find_if(v.begin(), v.end(), GreaterFive());
    cout << *it2 << endl;                                       // 5
    vector<int> v2 = {0,2,2,1,3,4,4};
    auto pos = adjacent_find(v2.begin(), v2.end());
    cout << *pos << endl;          // 2（第一组相邻重复）
    bool ret = binary_search(v.begin(), v.end(), 9);  // 必须有序序列！
    cout << ret << endl;           // 1
    vector<int> v3 = {10,40,20,40,20,40};
    cout << count(v3.begin(), v3.end(), 40) << endl;      // 3
    return 0;
}
```

```cpp
class Greater10 {
public:
    bool operator()(int val) { return val > 10; }
};
// count_if：统计大于10的元素个数
// vector<int> v = {10,40,30,40,20,40}; → 输出：5
```

### 3) 排序算法（P137-P145）

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <functional>   // greater<int>
#include <ctime>
using namespace std;
void myPrint(int val) { cout << val << " "; }
int main() {
    vector<int> v = {2,5,1,3,4,6};
    sort(v.begin(), v.end());                 // 升序：1 2 3 4 5 6
    for_each(v.begin(), v.end(), myPrint); cout << endl;
    sort(v.begin(), v.end(), greater<int>()); // 降序（预定义仿函数）：6 5 4 3 2 1
    for_each(v.begin(), v.end(), myPrint); cout << endl;
    srand((unsigned int)time(NULL));
    random_shuffle(v.begin(), v.end());       // 洗牌（C++17 起建议用 shuffle）
    vector<int> v1 = {1,3,5,9,11}, v2 = {2,4,8,12};
    vector<int> vTarget;
    vTarget.resize(v1.size() + v2.size());    // 提前开辟空间
    merge(v1.begin(), v1.end(), v2.begin(), v2.end(), vTarget.begin());
    // 输出：1 2 3 4 5 8 9 11 12（两个容器必须有序）
    vector<int> v3 = {1,3,5,6,9};
    reverse(v3.begin(), v3.end());            // 反转：9 6 5 3 1
    return 0;
}
```

### 4) 拷贝与替换算法（P146-P154）

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
class Greater20 {
public:
    bool operator()(int val) { return val == 20; }
};
int main() {
    vector<int> v1 = {11,22,33,55,66,99};
    vector<int> v2;
    v2.resize(v1.size());
    copy(v1.begin(), v1.end(), v2.begin());       // 拷贝（目标先开辟空间）
    vector<int> v = {10,20,10,30,10,40};
    replace(v.begin(), v.end(), 10, 1000);        // 10 全换成 1000
    vector<int> v3 = {1,10,20,30,20,50,10};
    replace_if(v3.begin(), v3.end(), Greater20(), 1000); // 满足谓词的换 1000
    vector<int> a = {1,2,3}, b = {11,22,33};
    swap(a, b);                                    // 交换两容器
    return 0;
}
```

### 5) 算术生成算法（P155-P159，`<numeric>`）

```cpp
#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;
int main() {
    vector<int> v;
    for (int i = 0; i <= 100; i++) v.push_back(i);
    int total = accumulate(v.begin(), v.end(), 0);  // 第三参：起始累加值
    cout << total << endl;                          // 输出：5050
    vector<int> v2;
    v2.resize(10);
    fill(v2.begin(), v2.end(), 100);                // 填充 10 个 100
    return 0;
}
```

### 6) 集合算法（P160-P166，两集合必须有序）

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
void myPrint(int val) { cout << val << " "; }
int main() {
    vector<int> v1 = {1,2,3,4,5}, v2 = {1,3,6,9};
    vector<int> vTarget;
    vTarget.resize(min(v1.size(), v2.size()));   // 交集：取小容器的 size
    auto itEnd = set_intersection(v1.begin(), v1.end(), v2.begin(), v2.end(), vTarget.begin());
    for_each(vTarget.begin(), itEnd, myPrint);   // 输出：1 3（返回值是交集末尾）
    cout << endl;
    vector<int> u1 = {1,2,3}, u2 = {4,5,6}, uT;
    uT.resize(u1.size() + u2.size());            // 并集：两容器 size 相加
    auto it2 = set_union(u1.begin(), u1.end(), u2.begin(), u2.end(), uT.begin());
    for_each(uT.begin(), it2, myPrint);          // 输出：1 2 3 4 5 6
    cout << endl;
    vector<int> d1 = {1,2,3,4,5}, d2 = {2,4,5,6,8}, dT;
    dT.resize(max(d1.size(), d2.size()));        // 差集：取大容器的 size
    auto it3 = set_difference(d1.begin(), d1.end(), d2.begin(), d2.end(), dT.begin());
    for_each(dT.begin(), it3, myPrint);          // 输出：1 3（d1 有 d2 没有）
    return 0;
}
```

**算法复杂度对比表**：

| 算法 | 时间复杂度 | 迭代器要求 |
|------|-----------|-----------|
| for_each / transform | O(n) | 输入迭代器以上 |
| find / find_if / count | O(n) | 输入迭代器以上 |
| binary_search | O(log n) | 随机访问（需有序） |
| sort | O(n log n) | 随机访问 |
| merge | O(n) | 输入迭代器以上（需有序） |
| reverse / random_shuffle | O(n) | 双向 / 随机访问 |
| set_intersection/union/difference | O(n) | 输入迭代器以上（需有序） |
| accumulate | O(n) | 输入迭代器以上 |

**迭代器分类**（支持的操作递增）：输入 → 输出 → 前向 → 双向（++/--）→ 随机访问（+n/-n）。**list/set/map 是双向迭代器，不能用 it+n，也不能喂给需要随机访问的算法**。

> 人话总结：算法认迭代器不认容器，谓词当条件，仿函数当工具。

---

# 配套代码逐行走读

## 1. string and vector code/mycode.cpp（test01~test21）

文件含 20 个测试函数，按课件顺序对应：
- **test01~test05**（string 基础）：初始化/输入输出/比较/拼接/获取字符，对应课件 P7-P13 演示，逐行逻辑与课件代码一致；
- **test06~test08**：子串拷贝构造（`string s2(s1,1)` 系列）、substr、insert，对应 P14-P16；
- **test09~test11**：erase 三种形态、append、replace，对应 P17-P19；
- **test12**：去标点练习（ispunct），对应 P21-P22；
- **test13~test17**（vector）：初始化五方式、遍历（at/front/back/正反向迭代器）、插入四方式、删除四方式、empty/size/capacity，对应 P25-P35；
- **test18~test20**：assign、swap、随机数最大最小案例，对应 P36-P39；
- **test21**：综合演示。

**走读示例**（随机数案例核心段）：

```cpp
srand(time(0));                    // 用当前时间做随机种子
for (int i = 1; i <= n; i++)
    v.push_back(rand() % 100 + 1); // rand()%100 得 0~99，+1 得 1~100 入容器
int max = v[0], min = v[0];        // 以首元素为基准
for (int i = 0; i < n; i++) {      // 逐个比较更新
    if (max < v[i]) max = v[i];
    if (min > v[i]) min = v[i];
}
```

## 2. stack queue list/mycode.cpp（test01~test20 + Guest/Person 类）

- **test01~test04**：stack 的 push/pop/top、empty/size、十进制转二进制案例（对应 P41-P47）；
- **test05~test08**：queue 构造、push/pop/front/back、扑克牌案例（对应 P48-P54）；
- **test09~test13**：deque 构造、两端增删、任意插入、访问、容量（对应 P55-P68）；
- **test14**：Guest VIP 插队练习（对应 P69-P70，`deque<Guest> deque;` 变量名与类型同名是课件写法，建议避免）；
- **test15~test19**：list 初始化、迭代器遍历、两端增删、sort/自定义排序、reverse（对应 P71-P84）；
- **test20 + Person 类**：Person 年龄升序/身高降序排序练习（对应 P87-P89）。

**走读示例**（十进制转二进制）：

```cpp
while (n) {            // n 非 0 就继续：对 13，依次得余数 1,0,1,1 入栈
    s.push(n % 2);
    n /= 2;
}
while (!s.empty()) {   // 出栈顺序正好反转 → 1101
    cout << s.top();
    s.pop();
}
```

## 3. list set map/mycode.cpp（test01~test19）

- **test01~test05**：set 构造插入（自动排序+去重）、删除、大小交换、find/count（对应 P91-P98）；
- **test06~test08**：set vs multiset 区别（count 返回 2、find 返回第一个）（对应 P99-P100）；
- **test09~test12**：pair 初始化/访问、make_pair、map 构造插入（对应 P102-P108）；
- **test13~test16**：map 大小交换、四种插入方式（含 `m[4]=40`）、删除、find/count（对应 P109-P115）；
- **test17**：multimap 一键多值（学生多成绩）（对应 P116-P117）；
- **test18~test19**：自定义类型排序、综合。

**走读示例**（map 四种插入）：

```cpp
m.insert(pair<int, int>(1, 10));              // 匿名二元组
m.insert(make_pair(2, 20));                   // make_pair 简写
m.insert(map<int, int>::value_type(3, 30));   // value_type 写法（不建议）
m[4] = 40;   // [] 写法：4 不存在 → 自动创建 {4, 默认0} 再赋 40
```

## 4. algorithm/mycode.cpp（test01~test22）

- **test01~test02**：for_each（普通函数+仿函数）、transform（+100 搬运），对应 P119-P123；
- **test03~test08**：find、find_if（GreaterFive/Five 谓词类）、adjacent_find、binary_search、count、count_if（Greater10），对应 P124-P136；
- **test09**：greater09 模板仿函数演示自定义比较；
- **test10~test13**：sort 升降序（`greater<int>()`）、random_shuffle、merge、reverse，对应 P137-P145；
- **test130/Greater20/Greater130**：replace/replace_if 谓词替换，对应 P149-P152；
- **test14~test17**：copy、replace、replace_if、swap，对应 P146-P154；
- **test18~test20**：accumulate、fill（`<numeric>`），对应 P155-P159；
- **test21~test22**：set_intersection/union/difference 三集合算法，对应 P160-P166。

**走读示例**（set_intersection 的空间准备）：

```cpp
vTarget.resize(min(v1.size(), v2.size()));  // 交集最多 = 小容器大小
auto itEnd = set_intersection(...);          // 返回值 = 交集实际末尾迭代器
for_each(vTarget.begin(), itEnd, myPrint);   // 只打印到 itEnd，后面是无效空间
```

## 5. 表达式括号匹配.cpp（P170 作业实现）

```cpp
#include <iostream>
#include <stack>
using namespace std;
stack<char> stk;          // 全局栈：存放未匹配的 '('
char str[256];
int main() {
    cin >> str;                       // 读入表达式（如 2*(x+y)/(1-x)@）
    int slen = strlen(str);
    for (int i = 0; i < slen; i++) {
        if (str[i] == '@') break;     // 结束符，停止扫描
        else if (str[i] == '(')
            stk.push(str[i]);         // 左括号：入栈等待匹配
        else if (str[i] == ')') {     // 右括号：尝试与栈顶匹配
            if (stk.top() == '(')     // ⚠️ 见下方警告
                stk.pop();
            else if (stk.empty()) {
                cout << "NO" << endl;
                return 0;
            }
        }
    }
    if (!stk.empty()) cout << "NO" << endl;  // 栈里还有 '(' → 不匹配
    else cout << "YES";
    return 0;
}
// 输入：2*(x+y)/(1-x)@  输出：YES
// 文件末尾注释 (() )@ 是测试用例（不匹配 → NO）
```

⚠️ **代码审查发现（课件代码的隐藏 bug）**：`if (stk.top() == '(')` 在栈空时先调 `top()` 再判 `empty()`——顺序反了！遇到多余右括号（如 `)@`）会对空栈取 top，属未定义行为。**正确写法**：

```cpp
else if (str[i] == ')') {
    if (stk.empty()) { cout << "NO" << endl; return 0; }  // 先判空
    stk.pop();                                            // 再弹栈匹配
}
```

这正是"读代码要审查、不能只看运行结果"的活教材。

[✅ 模块6/6 已完成]

---

# 第二阶段：查（五项检查）

| 检查项 | 结果 |
|--------|------|
| 1. 页码覆盖（P1-P171） | ✅ 全覆盖：P1-5 概述/组成、P6-22 string、P23-39 vector、P40-47 stack、P48-54 queue、P55-70 deque、P71-89 list、P90-100 set/multiset、P101-117 map/multimap、P118-166 算法、P167-168 约瑟夫练习、P169 总结、P170 括号匹配作业 |
| 2. 九个重点四步法展开 | ✅ string/vector/stack/queue/deque/list/set/map/算法全部四步法 |
| 3. 示例配齐 | ✅ 每个容器均配课件原例 + 输出标注 |
| 4. 比喻覆盖 | ✅ 宜家、钥匙包、鸡蛋盒、盘子、排队窗口、双门走廊、火车车厢、名片夹、字典、通用家电 |
| 5. 错误演示 | ✅ 迭代器失效、list 用 sort、map 用 [] 判存在、set 改值、空栈 top 均有错误代码 |

# 第三阶段：补

## 难点重讲一：迭代器失效（放慢节奏）

迭代器本质是"指向容器某位置的指针"。容器内部结构一变，旧指针就可能悬空。

**场景1：vector 扩容**。`push_back` 触发扩容 → 整块内存搬家 → 所有旧迭代器失效。规避：`reserve` 预留、插入后重新取迭代器、用 `erase` 返回值。

**场景2：vector 中间 erase**。被删元素之后的迭代器全部前移一位。`it = v.erase(it)` 是标准删法。

**场景3：边遍历边删的经典错误**：

```cpp
// 错误：删除后 it++ 会跳过元素甚至越界
for (auto it = v.begin(); it != v.end(); it++)
    if (*it % 2 == 0) v.erase(it);   // 危险！
// 正确：
for (auto it = v.begin(); it != v.end(); )
    if (*it % 2 == 0) it = v.erase(it);   // 删除返回下一个位置
    else ++it;
```

**场景4：list/set/map**。erase 只让被删节点的迭代器失效，其他安全——链表/树结构的局部修改不波及邻居。

## 难点重讲二：红黑树容器与哈希容器的选型

```
需要有序输出 / 范围查询（>=x 的元素）？
   ├─ 是 → set / map（红黑树，O(log n)，天然有序）
   └─ 否 → 只要快速增删查？
            ├─ 是 → unordered_set / unordered_map（哈希，平均 O(1)，无序）
            └─ 需要稳定最坏复杂度 → 还是 set/map（哈希最坏 O(n)）
```

红黑树五大性质（面试要点）：①节点非红即黑；②根是黑；③叶子（NIL）是黑；④红节点的子必黑（无连续红）；⑤任一节点到其所有叶子的路径黑节点数相同 → 最长路径不超过最短的 2 倍 → 树平衡。

## 常见陷阱专题（3 个最易错点）

### 陷阱1：vector 扩容导致迭代器失效

- **错误写法**：保存迭代器后继续 push_back
- **后果**：迭代器悬空，未定义行为
- **正确写法**：每次插入后重新获取迭代器，或先 reserve
- **如何记住**：vector 一搬家，旧车票（迭代器）全作废

### 陷阱2：对 list 使用 std::sort

- **错误写法**：`std::sort(li.begin(), li.end())`
- **后果**：编译错误（需要随机访问迭代器）
- **正确写法**：成员函数 `li.sort()`
- **如何记住**：链表自带排序技，std::sort 只爱数组

### 陷阱3：map 的 [] 运算符副作用

- **错误写法**：用 `m[key]` 判断键是否存在
- **后果**：键不存在时悄悄插入默认值，map 被污染
- **正确写法**：查找用 `find()` / `count()` / `at()`
- **如何记住**：中括号是"没有就造一个"，查岗请用 find

## 易错点速查卡

| 错误现象 | 错误原因 | 正确写法 | 后果 |
|----------|----------|----------|------|
| 遍历中删除后崩溃/跳元素 | 迭代器失效仍使用 | `it = v.erase(it)` | 未定义行为 |
| vector 扩容后旧迭代器报错 | 内存搬家 | reserve 或重新取 | 悬空 |
| `std::sort(list)` 编译错 | 双向迭代器 | `list.sort()` | 编译失败 |
| `m[key]` 判断存在 | 不存在会插入默认值 | `m.find(key) != m.end()` | map 被污染 |
| `v[100]` 崩溃 | [] 不查边界 | `v.at(100)` 或先判长度 | 未定义行为 |
| 空栈调用 top() | 未先判空 | 先 `stk.empty()` | 未定义行为 |
| transform/copy 目标越界 | 目标容器未开辟空间 | 先 `resize` | 越界写入 |
| binary_search 结果不对 | 容器无序 | 先 sort | 结果不可靠 |
| set 元素值修改 | 元素是 const | erase 后重新 insert | 编译失败 |
| string substr pos 越界 | pos > size | 先判断 | 抛异常/UB |

## 新手最常问的5个问题

**Q1：vector 的扩容机制到底是什么？**
当 size == capacity 时，申请 2 倍（或 1.5 倍，取决于实现）新内存，搬移旧元素，释放旧内存。所以频繁追加前先 `reserve` 能避免多次搬家。

**Q2：map 和 unordered_map 有什么区别？**
map 底层红黑树、按键有序、增删查 O(log n)；unordered_map 底层哈希表、无序、平均 O(1)。需要有序或范围查询选 map，只求快选 unordered。

**Q3：为什么 list 不能用 std::sort？**
std::sort 要求随机访问迭代器（需要 `it + n` 跳着访问），list 是双向链表只有双向迭代器。list 提供了自己的成员 `sort()`，专为链表设计。

**Q4：迭代器失效的场景有哪些？**
vector：扩容全失效、中间删除后续失效、中间插入后续失效；deque：中间增删全失效、两端增删仅头尾迭代器失效；list/set/map：只有被删节点的迭代器失效。

**Q5：emplace_back 和 push_back 区别？（现代 C++ 补充）**
push_back 接收现成对象（可能触发拷贝/移动）；emplace_back 直接在容器内存里原地构造，少一次临时对象。自定义类型频繁追加时 emplace_back 更优。

## 专项补充

**性能基准测试框架**（`<chrono>` 实测）：

```cpp
#include <chrono>
#include <iostream>
#include <vector>
#include <list>
using namespace std;
using Clock = chrono::steady_clock;
int main() {
    const int N = 100000;
    auto t0 = Clock::now();
    vector<int> v;
    for (int i = 0; i < N; i++) v.push_back(i);   // 尾部插入
    auto t1 = Clock::now();
    cout << "vector: " << chrono::duration_cast<chrono::milliseconds>(t1 - t0).count() << "ms" << endl;
    auto t2 = Clock::now();
    list<int> l;
    for (int i = 0; i < N; i++) l.push_front(i);  // list 头部插入 O(1)
    auto t3 = Clock::now();
    cout << "list: " << chrono::duration_cast<chrono::milliseconds>(t3 - t2).count() << "ms" << endl;
    return 0;
}
```

**面试高频考点**：

| # | 考题 | 答案要点 |
|---|------|----------|
| 1 | vector 扩容机制 | 2倍/1.5倍、搬移、迭代器失效、reserve 优化 |
| 2 | map 与 unordered_map 区别 | 红黑树有序 O(log n) vs 哈希无序平均 O(1) |
| 3 | list 为何不能用 std::sort | 迭代器类别：双向 ≠ 随机访问 |
| 4 | 迭代器失效场景 | 按容器分三类记忆（见难点重讲一） |
| 5 | string 的 SSO 优化 | 短字符串直接存在对象内部，不占堆 |
| 6 | emplace_back vs push_back | 原地构造 vs 传入对象 |
| 7 | 红黑树性质 | 五性质，最长路径 ≤ 2×最短 |
| 8 | deque 为什么能做 stack/queue 底层 | 两端 O(1)、分段内存、随机访问 |
| 9 | set 元素为何不可修改 | 改值破坏树的有序性 |
| 10 | reserve 与 resize 区别 | capacity vs size |

**与第24章文件操作的衔接**：文件读写常以 string 为缓冲、vector 批量存放读入数据；`ifstream`/`ofstream` 本身可配合流迭代器，让 STL 算法直接作用于文件流产生的区间。

**现代 C++ STL 扩展预告**：C++11 emplace 系列与 unordered 容器；C++17 `string_view`（零拷贝字符串视图）；C++20 `span`（轻量区间视图）与 `ranges` 库（算法的管道化写法）。

# 第四阶段：测（4 道测试题，答案留空待你作答）

**题目1（★）**：用 string 完成拼接、查找、截取子串各一个操作；用 vector 完成增、删、查各一个操作。
考察点：string + vector 基本操作。

你的答案：________________

**题目2（★★）**：说明 stack 与 queue 的区别，并各写一个使用示例；解释为什么它们不提供迭代器。
考察点：容器适配器。

你的答案：________________

**题目3（★★★）**：用 map 统计一段文本中每个单词出现的次数并按字典序输出。
考察点：map 的使用。

你的答案：________________

**题目4（★★★★ 综合题）**：用 map 统计词频，把结果存入 `vector<pair<string,int>>`，用 sort 按频率降序排序输出 Top 3；并说明容器选型理由和算法复杂度。
考察点：容器 + 算法 + 选型联动。

你的答案：________________

**代码审查题**（作答上题后使用）：找出所有 bug 并改正：

```cpp
vector<int> v;
auto it = v.begin();
for (int i = 0; i < 100; i++) v.push_back(i);   // 问题1
*it = 1;

list<int> li = {3,1,2};
sort(li.begin(), li.end());                       // 问题2

map<string,int> m;
if (m["key"] > 0) { /* ... */ }                   // 问题3

vector<int> w = {1,2,3,4,5};
cout << w[10] << endl;                            // 问题4
```

# 第五阶段：收

## 代码自测清单

- [ ] 手写 string 的初始化/拼接/查找/替换/子串五个操作
- [ ] 用三种方式遍历 vector（下标、迭代器、范围for），说出扩容与迭代器失效
- [ ] 用 stack 实现十进制转二进制、用 queue 实现扑克牌问题
- [ ] 用 deque 实现头部插入、随机访问
- [ ] 用 list 自定义排序规则（成员 sort）
- [ ] 用 set 去重排序、用 map 做词频统计
- [ ] 用 for_each + 仿函数、sort + 谓词、accumulate 处理容器
- [ ] 说出每类容器的底层结构和复杂度

## 复习计划

| 时间 | 复习内容 | 方式 |
|------|----------|------|
| 1天后 | string + vector 全部操作 | 重做随机数案例与去标点练习 |
| 3天后 | stack/queue/deque + 括号匹配作业 | 默写括号匹配并修掉空栈 top 的 bug |
| 5天后 | list + set + map 三大容器 | 重做 Person 排序与词频统计 |
| 7天后 | 六类算法 + 容器选型决策表 | 看树状图回忆 + 做综合题（题目4） |

## 树状图（全章知识体系）

```
STL
├── 三大核心
│   ├── 容器（装数据）
│   │   ├── 序列式
│   │   │   ├── string（字符动态数组）
│   │   │   ├── vector（动态数组，尾部快）
│   │   │   ├── deque（分段，两端快）
│   │   │   ├── list（双向链表，中间快）
│   │   │   ├── stack（适配器，LIFO）
│   │   │   └── queue（适配器，FIFO）
│   │   └── 关联式（红黑树，自动排序）
│   │       ├── set / multiset（去重）
│   │       └── map / multimap（键值）
│   ├── 迭代器（五类：输入/输出/前向/双向/随机访问）
│   └── 算法（<algorithm>/<numeric>/<functional>）
│       ├── 遍历 for_each/transform
│       ├── 查找 find/find_if/binary_search/count
│       ├── 排序 sort/merge/reverse/random_shuffle
│       ├── 拷贝替换 copy/replace/replace_if/swap
│       ├── 算术 accumulate/fill
│       └── 集合 intersection/union/difference
├── 仿函数与谓词（operator()，返回bool）
└── 专题
    ├── 迭代器失效（扩容/删除/容器差异）
    ├── 容器选型决策表
    └── 实战：括号匹配、进制转换、词频统计、约瑟夫
```

## 速查表

### 精简版速查表（一页速查）

| 容器 | 头文件 | 核心操作 |
|------|--------|----------|
| string | `<string>` | `+`、find、substr、insert、erase、replace |
| vector | `<vector>` | push_back、insert、erase、[]/at、size/capacity |
| stack | `<stack>` | push/pop/top |
| queue | `<queue>` | push/pop/front/back |
| deque | `<deque>` | push_front/back、pop_front/back、[] |
| list | `<list>` | push_front/back、insert、erase、sort、reverse |
| set | `<set>` | insert、erase、find、count |
| map | `<map>` | insert、[]、erase、find、count |

| 算法 | 用途 | 关键前提 |
|------|------|----------|
| for_each | 遍历 | 函数或仿函数 |
| find/find_if | 查找 | 有序可更快 |
| sort | 排序 | 随机访问迭代器 |
| merge | 合并 | 两容器有序+目标预扩容 |
| copy/transform | 拷贝搬运 | 目标预扩容 |
| accumulate | 求和 | `<numeric>`，第三参起始值 |
| set_* | 交并差 | 两集合有序 |

### 详细版速查表（语法 + 示例 + 注意事项）

| 主题 | 语法 | 示例 | 注意事项 |
|------|------|------|----------|
| vector 构造 | `vector<T> v(n, val)` | `vector<int> v(10, 2)` | 区间构造传两迭代器 |
| vector 预留 | `v.reserve(n)` | 频繁追加前调用 | 只扩 capacity |
| stack 使用 | `stk.push/pop/top` | 括号匹配 | 无迭代器 |
| list 排序 | `li.sort(cmp)` | Person 双条件 | 禁用 std::sort |
| set 插入 | `s.insert(x)` | 自动排序去重 | 元素不可改 |
| map 插入 | `m[k]=v` / insert | 词频统计 | [] 有插入副作用 |
| sort 降序 | `sort(b, e, greater<int>())` | `<functional>` | 需随机访问 |
| 集合算法 | `set_intersection(...)` | 目标取 min/max size | 集合必须有序 |

## 3条随身速记口诀

1. **数组尾快 vector，两头快是 deque；链表中间插删快，随机访问它不在。**
2. **栈后进先出队列先，适配器里没有迭代器；括号匹配用栈做，排队约瑟夫用队列。**
3. **set 去重 map 存键，红黑树里自动排；算法只认迭代器，谓词仿函数随身带。**

## 术语中英对照表

| 英文 | 中文 | 英文 | 中文 |
|------|------|------|------|
| STL (Standard Template Library) | 标准模板库 | container | 容器 |
| iterator | 迭代器 | algorithm | 算法 |
| functor / function object | 仿函数/函数对象 | predicate | 谓词 |
| adaptor | 适配器 | allocator | 空间配置器 |
| sequential container | 序列式容器 | associative container | 关联式容器 |
| dynamic array | 动态数组 | doubly linked list | 双向链表 |
| red-black tree | 红黑树 | hash table | 哈希表 |
| LIFO / FIFO | 后进先出/先进先出 | key-value pair | 键值对 |
| instantiation | 实例化 | iterator invalidation | 迭代器失效 |
| reserve / resize | 预留容量/调整大小 | emplace | 原地构造 |
| specialization | 特化 | SSO (Small String Optimization) | 小字符串优化 |

## 错题记录（待你作答后填写）

| 题号 | 题目 | 我的错误答案 | 正确答案 | 错误原因 | 涉及知识点 | 复习建议 |
|------|------|-------------|----------|----------|-----------|----------|
| 1 | string+vector 基本操作 | （待填写） | （待批改） | | 基本操作 | 建议1天后复习 |
| 2 | stack/queue 对比 | （待填写） | （待批改） | | 容器适配器 | 建议3天后复习 |
| 3 | map 词频统计 | （待填写） | （待批改） | | map | 建议3天后复习 |
| 4 | 词频 Top3 综合 | （待填写） | （待批改） | | 容器+算法 | 建议7天后复习 |

## 学习心态自评（请自评）

1. 我理解本章核心概念的程度：____星（1-5）
2. 我能独立写出本章示例代码的程度：____星（1-5）
3. 我能识别并避免常见错误的程度：____星（1-5）
4. 最需要再复习的3个知识点：________

## 知识蒸馏总结

STL 是 C++ 的标准零件库：容器装数据、迭代器当手、算法干活，三者即插即用。

> **附加指令——知识蒸馏检查**：STL 就是现成的数据结构和算法工具箱，选对容器、用对算法，代码少写一大半。

---

**本章关联**
- 前置章节：第22章 模板（vector<int> 就是类模板实例化）
- 后置章节：第24章 文件操作（string 做缓冲、vector 批量读数据、流迭代器喂算法）

*笔记生成完毕。全部内容基于《23 STL》课件（171页）与 5 组配套代码；表达式括号匹配的隐藏 bug 已在走读中指出并给出修正。*
