# C++ STL 学习笔记（教材《23 STL》全解）

> 依据教材《23 STL.pdf》（171页）与配套代码（mycode.cpp v1-v4、Test002、表达式括号匹配.cpp）整理。
> 讲解顺序严格跟随教材页码 P4 → P171；每个知识点按「是什么 → 为什么 → 怎么用 → 注意事项」四步展开，
> 配有可运行代码、预期输出与人话总结。文末附代码全景索引、易混对比、迭代器专题、全章体系树、
> 随身口诀与 4 道随堂测验（测验答案等你作答后由教练批改）。

**教材掌握度分级**：STL概述【了解】｜STL基本组成【熟悉】｜string/vector/stack/queue/deque/list/
set·multiset/map·multimap/STL常用算法【重点】。

---

## 📑 快速跳转目录

> 提示：在支持 Markdown 锚点的编辑器（如 VS Code、Typora、GitHub、obsidian）中点击章节标题可直接跳转到对应位置。

### 一、容器篇（教材 P4–P117）

| 章节 | 主题 | 教材页码 | 跳转 |
|------|------|----------|------|
| 第 1 章 | STL 概述 + string 容器 | P4-P22 | [→ 跳转](#第1章-stl概述与string容器教材p4-p22) |
| 第 2 章 | vector 动态数组 | P23-P39 | [→ 跳转](#第2章-vector容器教材p23-p39) |
| 第 3 章 | stack 栈 + queue 队列 | P40-P54 | [→ 跳转](#第3章-stack与queue容器教材p40-p54) |
| 第 4 章 | deque 双端队列 + list 双向链表 | P55-P89 | [→ 跳转](#第4章-deque与list容器教材p55-p89) |
| 第 5 章 | set / multiset + map / multimap | P90-P117 | [→ 跳转](#第5章-setmultiset与mapmultimap容器教材p90-p117) |

### 二、算法篇（教材 P118–P136：遍历与查找）

| 章节 | 主题 | 教材页码 | 跳转 |
|------|------|----------|------|
| 6.1 | 算法概述：三件套头文件 | P118 | [→ 跳转](#61-算法概述三件套头文件p118) |
| 6.2 | for_each 遍历 | P119-P121 | [→ 跳转](#62-foreach最常用的遍历p119-p121) |
| 6.3 | transform 搬运 | P122-P123 | [→ 跳转](#63-transform搬运容器到另一个容器p122-p123) |
| 6.4 | 查找算法总览 | P124 | [→ 跳转](#64-查找算法总览p124) |
| 6.5 | find 按值查找 | P125-P126 | [→ 跳转](#65-find按值查找p125-p126) |
| 6.6 | find_if 按条件查找 | P127-P128 | [→ 跳转](#66-find_if按条件查找p127-p128) |
| 6.7 | adjacent_find 查相邻重复 | P129-P130 | [→ 跳转](#67-adjacent_find查找相邻重复元素p129-p130) |
| 6.8 | binary_search 二分查找 | P131-P132 | [→ 跳转](#68-binary_search二分查找p131-p132) |
| 6.9 | count 统计元素 | P133-P134 | [→ 跳转](#69-count统计元素个数p133-p134) |
| 6.10 | count_if 按条件统计 | P135-P136 | [→ 跳转](#610-count_if按条件统计p135-p136) |
| 6.11 | 易混算法对比 | - | [→ 跳转](#611-易混算法对比) |

### 三、算法篇（教材 P137–P171：排序、拷贝、替换、集合）

| 章节 | 主题 | 教材页码 | 跳转 |
|------|------|----------|------|
| 第 7 章 | 排序/拷贝/替换/集合算法 + 综合练习 | P137-P171 | [→ 跳转](#第7章-stl常用算法排序拷贝替换与集合--综合练习教材p137-p171) |

### 四、补充与练习

| 章节 | 主题 | 跳转 |
|------|------|------|
| 第 8 章 | 深度补充：代码全景、易混对比、迭代器专题 | [→ 跳转](#第8章-深度补充代码全景易混对比与迭代器专题) |
| 第 9 章 | 全章知识体系回顾 + 随身口诀 | [→ 跳转](#第9章-全章知识体系回顾与随身口诀) |
| 第 10 章 | 随堂测验（4 题·难度递进） | [→ 跳转](#第10章-随堂测验4题难度递进) |

### 🗺️ 学习路线建议

```
入门路线（必学）：
  第1章 string → 第2章 vector → 第3章 stack/queue
  → 第4章 deque/list → 第5章 set/map
  → 第6章 find/sort → 第10章 测验

进阶路线（选学）：
  第7章 算法综合（merge/reverse/copy/replace/accumulate/fill/集合算法）
  → 第8章 迭代器专题 + 易混对比

复习路线：
  第9章 体系树 + 随身口诀（考前必看）
```

---

## 第1章 STL概述与string容器（教材P4-P22）

### 1.1 STL概述（P4）【了解】

**是什么**：STL（Standard Template Library）即标准模板库——C++ 借助模板把常用的数据结构及其算法都实现了一遍，并且做到了数据结构和算法的分离。

一句话概括：STL = 容器集合 + 算法集合。例如 vector 底层是顺序表（数组）、list 底层是双向链表、deque 底层是循环队列、set 底层是红黑树、hash_set 底层是哈希表；`<algorithm>` 里的 sort 函数、`<string>` 里的 string 类都属于 STL。

**人话总结**：STL 是现成的"数据结构+算法"工具箱。

### 1.2 STL基本组成（P5）【熟悉】

STL 从广义上讲分为三类：

| 组件 | 是什么 | 类比 |
|---|---|---|
| 容器 Container | 存放数据的数据结构（list、vector、deque…），以模板类提供 | 仓库 |
| 迭代器 Iterator | 访问容器中对象的方法，如同一支"指针"，可以指定容器中一定范围的对象 | 仓库管理员 |
| 算法 Algorithm | 操作容器中数据的模板函数（sort、find…），与数据类型无关 | 搬运工 |

要点：C++ 的指针本身也是一种迭代器；迭代器也可以是定义了 `operator*()` 等指针操作的类对象。算法函数与它们操作的数据结构和类型无关，因此可以从简单数组到高度复杂容器通用。

**人话总结**：容器存数据、迭代器找数据、算法改数据。

### 1.3 string容器概述（P6）【重点】

**是什么**：string 是 C++ 标准模板库专门用于字符串处理的数据类型。

**为什么**：用字符数组存放字符串容易发生数组越界错误，而且往往难以察觉。string 封装了内存管理，越界由标准库负责检查，更安全、更简单。

**怎么用**：须包含头文件 `<string>`。

```cpp
#include <string>
using namespace std;

int main() {
    string s = "hello";   // 声明+初始化
    return 0;
}
```

**注意事项**：
1. 忘写 `#include <string>` 会报"未声明的标识符"。
2. 用 C++ 编程时优先用 string，而不是 char 数组。

**人话总结**：string 是安全的字符串。

### 1.4 string的构造与初始化（P7-P8）【重点】

**是什么**：string 对象可用默认构造、拷贝构造、字面值、n 个相同字符、临时对象等多种方式初始化。

**为什么**：string 是类，初始化除了普通方式外还可以利用构造函数，写法灵活。

**怎么用**（配套代码 test01）：

```cpp
string s1;              // 空字符串
string s2(s1);          // 拷贝构造：s2是s1的副本
string s3 = s1;         // 等价于 s3(s1)，也是副本
string s4("hello");     // 字面值初始化
string s5 = "hello";    // 等价于上行
string s6(11, 'a');     // 11个字符'a'组成的串 -> "aaaaaaaaaaa"
string s7 = string("wolrd");   // 临时对象初始化
string s8(string("kjlj"));     // 临时对象初始化
```

**运行输出**（test01 依次打印）：

```text
abc
abc
abc
hello
hello
aaaaaaaaaaa
wolrd
kjlj
```

**注意事项**：
1. `string s6(n, 'a')` 的第二个参数必须是字符（单引号），写 `"a"`（双引号字符串）会编译错误。
2. 教材 P8 的 `s7 = string("hello")` 先用构造函数生成临时 string 对象，再用它初始化——临时对象用完即销毁，不影响 s7。

**人话总结**：构造方式八仙过海，拷贝最常用。

### 1.5 string的输入输出（P9）【重点】

**是什么**：`cin >>` 遇空格/换行停止读取；`getline` 读取一整行（含空格）。

**为什么**：输入含空格的句子时 cin 会"半途而废"，getline 才能读全。

**怎么用**（配套代码 test02 / test03）：

```cpp
// test02：cin 输入
string s1;
cin >> s1;          // 输入 "hello world" 只读到 "hello"
cout << s1 << endl;

// test03：getline 输入
string s2;
getline(cin, s2);   // 输入 "hello world" 读入整行
cout << s2 << endl;
```

**对比表**：

| 方式 | 遇空格 | 遇换行 | 适用场景 |
|---|---|---|---|
| `cin >> s` | 停止 | 停止 | 单个单词 |
| `getline(cin, s)` | 继续 | 停止 | 整行含空格 |

**注意事项**：
1. VS 中使用 getline 必须包含 `<string>`。
2. cin 和 getline 混用时要小心：cin 读完会在输入流留下换行符，直接 getline 会读到空行（可用 `cin.ignore()` 清掉）。

**人话总结**：读单词用 cin，读整行用 getline。

### 1.6 string的比较大小（P10）【重点】

**是什么**：string 可以直接用 `>`、`<`、`<=`、`>=`、`==`、`!=` 比较，按字典序（ASCII 码）逐字符比较。

**为什么**：字符串比较是高频操作（排序、查找、字典序），运算符重载让代码直观。

**怎么用**（配套代码 test04）：

```cpp
string s1 = "abc", s2 = "edf";
if (s1 < s2) {              // 'a'(97) < 'e'(101)，成立
    cout << "s1 < s2" << endl;
}
```

**运行输出**：

```text
s1 < s2
```

**注意事项**：
1. 比较按字典序：先比第一个不同字符的 ASCII 码。"abc" < "abd"；"abc" > "ab"（短的更小）。
2. 大小写敏感：'A'(65) < 'a'(97)，所以 "Apple" < "apple"。

**人话总结**：字典序比较，直接写运算符。

### 1.7 string的连接（P11）【重点】

**是什么**：string 可以用 `+` 直接连接。

**为什么**：字符数组拼接要 strcat 且小心缓冲区溢出，string 的 `+` 安全省心。

**怎么用**（配套代码 test05）：

```cpp
string s1 = "23432", s2 = "abdjf", s3;
s3 = s1 + s2;
cout << s3 << endl;

// string s4 = "xiaoming" + "china";  // 错误！两个字面值不能+
```

**运行输出**：

```text
23432abdjf
```

**注意事项**：
1. **两个字符串字面值不能直接用 + 连接**："xiaoming" + "china" 编译错误（都是 const char*，没有 operator+）。
2. 至少一边是 string 才能 +：`"xiaoming" + string("china")` 或 `s1 + "china"` 都合法。

**人话总结**：连接用加号，字面值要配 string。

### 1.8 string的遍历（P12-P13）【重点】

**是什么**：三种遍历方式：C++11 range-for、下标+size()、迭代器。

**为什么**：遍历是字符串处理的基础操作，三种方式覆盖不同场景。

**怎么用**（配套代码 test06，教材 P12-13 代码）：

```cpp
string s1 = "abcdefghijk";

// 方式1：C++11 range-for
for (auto c : s1) {
    cout << c << " ";
}
cout << endl;

// 方式2：下标 + size()
for (int i = 0; i < s1.size(); i++) {
    cout << s1[i] << " ";
}
cout << endl;

// 方式3：迭代器
for (auto i = s1.begin(); i != s1.end(); i++) {
    cout << *i << " ";
}
```

**运行输出**（三次遍历结果相同）：

```text
a b c d e f g h i j k
a b c d e f g h i j k
a b c d e f g h i j k
```

**注意事项**：
1. range-for 里的 `auto c` 是拷贝，改 c 不影响原字符串；要修改元素用 `auto &c`。
2. `s1.size()` 返回无符号整数，`i < s1.size()` 时 i 最好用 `size_t`，避免符号比较警告。

**人话总结**：遍历三兄弟，for最省事。

### 1.9 string的子串构造（P14）【重点】

**是什么**：`string s(s1, pos)` 从 pos 拷贝到结尾；`string s(s1, pos, len)` 从 pos 拷贝 len 个。

**为什么**：按位置截取字符串的一部分。

**怎么用**（配套代码 test07）：

```cpp
string s1 = "hello";

string s2(s1, 1);        // 从下标1到结尾 -> "ello"
string s4(s1, 5);        // pos==size()，空串 -> ""
string s5(s1, 0, 3);     // 从0拷3个 -> "hel"
string s6(s1, 2, 10);    // 从2拷10个，超长只拷到结尾 -> "llo"
string s7(s1, 5, 3);     // pos==size()，空串 -> ""
// string s3(s1, 8);      // 错误示范：pos>size() 未定义行为
// string s8(s1, 6, 2);   // 错误示范：pos>size() 未定义行为
```

**运行输出**：

```text
ello

hel
llo

```

**注意事项**：
1. **pos > size() 是未定义行为**（通常抛 `std::out_of_range` 异常），这是配套代码里 test07 注释掉 s3/s8 的原因——它们是"错误示范"。
2. pos == size() 合法：拷贝到空串。
3. len 超长不报错：最多拷到结尾。

**人话总结**：pos 越界要不得，len 超长没事。

### 1.10 string的substr子串提取（P15）【重点】

**是什么**：`s.substr(pos, n)` 返回从 pos 开始的 n 个字符组成的新 string。pos 默认 0，n 默认到结尾。

**为什么**：只读不改地取出子串，比构造方式更直观。

**怎么用**（配套代码 test08）：

```cpp
string s = "value";
string s1 = s.substr();      // "value"
string s2 = s.substr(3);     // 从3到结尾 -> "ue"
string s3 = s.substr(5);     // pos==size() -> 空串
string s5 = s.substr(2, 3);  // 从2拷3个 -> "lue"
string s7 = s.substr(3, 10); // 超长只到结尾 -> "ue"
string s8 = s.substr(5, 10); // pos==size() -> 空串
// string s4 = s.substr(10);  // 错误示范：pos>size() 抛异常
// string s6 = s.substr(6, 2);// 错误示范：pos>size() 抛异常
```

**运行输出**：

```text
value
ue

lue
ue

```

**注意事项**：
1. substr 的 pos 越界（>size()）会抛 `std::out_of_range`——test08 注释掉 s4/s6 同样是错误示范。
2. substr 返回**新对象**，修改返回值不影响原字符串。

**人话总结**：substr 取子串，pos 别越界。

### 1.11 string的insert插入（P16）【重点】

**是什么**：insert 在指定位置插入字符/多个字符/区间字符/初始化列表。

**为什么**：在字符串中间"加塞"内容。

**怎么用**（配套代码 test09）：

```cpp
string s1 = "value";
s1.insert(s1.begin(), 's');            // 头部插1个字符 -> "svalue"
s1.insert(s1.begin(), 3, 'a');         // 头部插3个'a' -> "aaasvalue"
s1.insert(s1.begin(), s1.begin(), ++s1.begin()); // 头部插入区间(1个字符) -> "aaaasvalue"
s1.insert(s1.end(), { 'e','f' });      // 尾部插初始化列表 -> "aaaasvalueef"
cout << s1 << endl;
```

**运行输出**：

```text
aaaasvalueef
```

**注意事项**：
1. 迭代器插入是"在迭代器指向位置**之前**插入"。
2. 区间插入 `insert(it, first, last)` 是左闭右开 `[first, last)`。
3. 在自己身上做区间插入时，区间迭代器可能失效（教材用 `s1.begin(), ++s1.begin()` 只插1个字符没问题，复杂情况先拷贝再插）。

**人话总结**：insert 加塞，位置用迭代器。

### 1.12 string的erase删除（P17）【重点】

**是什么**：erase 删除字符串内容，有四种重载。

**为什么**：删除字符是字符串处理的基本需求。

**怎么用**（配套代码 test10）：

```cpp
string s1 = "value", s2 = "value", s3 = "value", s4 = "value";

s1.erase();                 // 删除全部 -> ""
s2.erase(1, 2);             // 从下标1删2个('a','l') -> "vue"
s3.erase(s3.begin() + 1);   // 删除迭代器指向的字符('a') -> "vlue"
s4.erase(s4.begin(), s4.begin() + 2); // 删除区间[begin,begin+2)('v','a') -> "lue"
```

**运行输出**：

```text
（空行）
vue
vlue
lue
```

**注意事项**：
1. `erase(pos, n)` 的 pos 越界会报错（pos > size()）。
2. 区间删除是左闭右开 `[first, last)`：`erase(begin(), begin()+2)` 只删前2个。
3. erase 返回删除后的字符串/下一个字符的迭代器（教材强调这点，迭代器删除常用于遍历中删除）。

**人话总结**：erase 删字符，区间左闭右开。

### 1.13 string的append追加（P18）【重点】

**是什么**：`append()` 在 string 末尾追加内容。

**为什么**：追加字符串用 append 或 `+` 都可以，append 更明确。

**怎么用**（配套代码 test11）：

```cpp
string s1 = "C++";
s1.append(" program");
cout << s1 << endl;
```

**运行输出**：

```text
C++ program
```

**注意事项**：
1. append 与 `+` 的区别：`+` 生成新对象，append 直接修改原对象（更高效）。
2. 两个字面值同样不能用 append 互相拼：`"a".append("b")` 不合法，字面值没有成员函数。

**人话总结**：末尾追加用 append。

### 1.14 string的replace替换（P19）【重点】

**是什么**：`replace(pos, n, str)` 把从 pos 开始的 n 个字符删除，再在该位置插入新内容。

**为什么**：字符串中间替换一段内容。

**怎么用**（配套代码 test12，教材 P19 五连替换）：

```cpp
string s = "i very love china";
const char* cp1 = "truly";
const char* cp2 = "truly!!!!!";
string str1 = "really";
string str2 = "really";

s.replace(2, 4, cp1);        // 删"very"插"truly" -> "i truly love china"
s.replace(2, 5, cp2, 5);     // 删5个插cp2前5个 -> "i truly love china"
s.replace(2, 5, str1);       // 删5个插"really" -> "i really love china"
s.replace(2, 6, str2, 0, 6); // 删6个插str2[0,6) -> "i really love china"
s.replace(2, 6, 6, '*');     // 删6个插6个'*' -> "i ****** love china"
```

**运行输出**（每行一个 replace 后的结果）：

```text
i truly love china
i truly love china
i really love china
i really love china
i ****** love china
```

**注意事项**：
1. replace 语义 = 先删后插：`replace(pos, n, str)` 中 n 是要删除的字符数。
2. 重载 `replace(pos, n, cp, len)` 只插入 const char* 的前 len 个字符。
3. 重载 `replace(pos, n, str, pos2, len2)` 插入 str 从 pos2 开始的 len2 个字符。

**人话总结**：replace 先删后插，n 是删除数。

### 1.15 课堂练习：去除标点符号（P21-P22）

**题目**：输入一串带有标点符号的字符串，去除字符串中的标点符号后输出。

**解题思路**：遍历字符串，用 `<cctype>` 的 `ispunct()` 判断每个字符是否为标点，不是标点就输出。

**怎么用**（配套代码 test13，对应教材 P22 代码）：

```cpp
#include <iostream>
#include <cctype>   // ispunct 在这里
using namespace std;

int main() {
    string s;
    getline(cin, s);           // 读取整行（含空格）
    for (auto c : s) {
        if (!ispunct(c)) {     // 不是标点才输出
            cout << c;
        }
    }
    return 0;
}
```

**运行示例**（输入 `hello, world!`）：

```text
hello world
```

**注意事项**：
1. `ispunct()` 在 `<cctype>` 头文件中，漏包含会编译错误。
2. ispunct 判断的是标点字符：`! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~`。
3. 用 range-for 遍历 + 过滤输出，比"原地删除"更简单安全（迭代器删除会失效）。

**人话总结**：ispunct 判标点，非标点输出。

### 本章人话总结

1. string 是 C++ 优先使用的字符串类型，安全且功能全。
2. 构造、连接、比较、遍历、子串、增删改查六大操作要熟练。
3. 越界（pos > size()）是 string 新手最大的坑：substr/erase/构造子串都会踩。
4. 迭代器区间一律左闭右开 `[first, last)`。

---

## 第2章 vector容器（教材P23-P39）

### 2.1 vector概述（P23-P24）【重点】

**是什么**：vector 是一个能够存放任意类型的动态数组，是同一种类型对象的集合，每个对象有对应的整数索引。

**为什么**：普通数组定长、易越界；vector 由标准库自动管理内存，可动态增长，还能存放各种类型（int、char、string、自定义类…）。

**怎么用**：须包含头文件 `<vector>`。

```cpp
#include <vector>
using namespace std;

int main() {
    vector<int> v;   // 空 vector
    return 0;
}
```

**注意事项**：
1. 一个容器中的所有对象必须是同一种类型。
2. vector 元素在内存中连续存储，支持随机访问（下标 O(1)）。

**人话总结**：vector 是能自动长大的数组。

### 2.2 vector的声明与初始化（P25-P26）【重点】

**是什么**：vector 可以声明各种类型，初始化方式有列表初始化、构造函数初始化、拷贝、区间。

**为什么**：不同的初始化方式对应不同的使用场景（已知值/已知个数/拷贝/截取）。

**怎么用**（配套代码 test14、test15）：

```cpp
// 列表初始化（test14）
vector<int> v1 = { 1,2,3,4 };
vector<char> v2 = { 'h','e','l','l','o' };
vector<string> v3 = { "hello","abc","world" };
cout << v1[0] << endl;   // 1

// 构造函数初始化（test15）
vector<int> a1(10);          // 10个元素，默认值0
vector<int> a2(10, 6);       // 10个元素，值都为6
vector<int> a3(a2);          // 拷贝构造，复制a2
vector<int> a4(a2.begin(), a2.begin() + 1);  // 区间[a2.begin(), a2.begin()+1) 共1个元素
```

**运行输出**：

```text
1
0
6
6
1
```

（说明：`a1[0]` 输出 0，`a2[0]` 输出 6，`a3[1]` 输出 6，`a4.size()` 输出 1）

**注意事项**：
1. 教材 P26 代码写的是 `vec(a.begin(), a.begin+1)`——**少写了括号**，正确的是 `a.begin() + 1`（begin 是函数不是变量）。
2. `vector<int> v(10)` 的圆括号与 `vector<int> v{10}` 的花括号不同：花括号是列表初始化，只有一个元素 10。
3. 区间构造是左闭右开 `[first, last)`：`a2.begin() + 1` 只复制第一个元素。

**人话总结**：初始化四件套：列表、个数、拷贝、区间。

### 2.3 vector的遍历与访问（P27-P28）【重点】

**是什么**：访问元素用 at()/front()/back()/下标，遍历用 begin()/end()/rbegin()/rend()。

**为什么**：随机访问是 vector 的核心优势（连续内存，下标直达）。

**怎么用**（配套代码 test16，教材 P28 代码）：

```cpp
vector<int> v = { 1,2,3,4,5,6 };
cout << v.at(3) << endl;      // 下标3的元素 -> 4（at会检查越界）
cout << v.front() << endl;    // 首元素 -> 1
cout << v.back() << endl;     // 尾元素 -> 6

for (auto i = v.begin(); i != v.end(); i++) {   // 正向遍历
    cout << *i << " ";
}
cout << endl;

for (auto i = v.rbegin(); i != v.rend(); i++) { // 反向遍历
    cout << *i << " ";
}
```

**运行输出**：

```text
4
1
6
1 2 3 4 5 6
6 5 4 3 2 1
```

**对比表**：

| 方式 | 检查越界 | 返回 | 场景 |
|---|---|---|---|
| `v[i]` | 不检查（UB） | 引用 | 确定不越界时，最快 |
| `v.at(i)` | 检查，越界抛 out_of_range | 引用 | 不确定时，安全 |
| `v.front()` / `v.back()` | — | 首/尾引用 | 取两端 |
| `begin()/end()` | — | 正向迭代器 | 正向遍历 |
| `rbegin()/rend()` | — | 反向迭代器 | 反向遍历 |

**注意事项**：
1. end() 指向最后一个元素的**下一个位置**，不能解引用。
2. 用下标 `v[i]` 越界是未定义行为（不报错但结果垃圾）；`at()` 越界会抛异常。

**人话总结**：下标最快、at 最安全、rbegin 反着走。

### 2.4 vector的插入（P29-P30）【重点】

**是什么**：push_back 尾部添加；insert 在迭代器指向位置前插入。

**为什么**：vector 尾部插入 O(1) 摊销，中间插入 O(n)（要搬移元素）。

**怎么用**（配套代码 test17，教材 P30 代码）：

```cpp
vector<int> v = { 1,2 };
vector<int> v2 = { 111,222 };

v.push_back(3);                 // 尾部加3 -> {1,2,3}
v.insert(v.begin(), 66);        // 头部前插66 -> {66,1,2,3}
v.insert(v.begin() + 1, 10, 99);// 第1个位置前插10个99
v.insert(v.begin(), v2.begin(), v2.end());  // 头部前插v2全部 -> {111,222,...}

for (auto i = v.begin(); i != v.end(); i++) {
    cout << *i << " ";
}
```

**运行输出**：

```text
111 222 66 99 99 99 99 99 99 99 99 99 99 1 2 3
```

**注意事项**：
1. insert 是"在迭代器指向元素**之前**插入"。
2. 中间/头部插入会搬移后续元素，频繁头部插入请考虑 deque。
3. 插入可能导致迭代器失效（扩容/搬移后旧迭代器指向未知位置）。

**人话总结**：尾部 push_back，任意位置 insert。

### 2.5 vector的删除（P31-P32）【重点】

**是什么**：erase 按迭代器/区间删除，pop_back 删尾部，clear 清空。

**为什么**：删除元素是动态数组的基本操作。

**怎么用**（配套代码 test18，教材 P32 代码）：

```cpp
vector<int> v = { 1,2,3,4,5,6 };
cout << v.empty() << endl;              // 0（非空）

v.erase(v.begin() + 1);                 // 删除下标1的2 -> {1,3,4,5,6}
v.erase(v.begin() + 2, v.begin() + 4);  // 删除区间[2,4)即4,5 -> {1,3,6}
v.pop_back();                           // 删除最后一个6 -> {1,3}
// v.clear();                           // 注释掉：清空所有元素

cout << v.empty() << endl;              // 0（非空）
for (auto i = v.begin(); i != v.end(); i++) {
    cout << *i << " ";
}
```

**运行输出**：

```text
0
0
1 3
```

**注意事项**：
1. 区间删除左闭右开：`erase(begin()+2, begin()+4)` 删的是下标 2、3 两个元素。
2. erase 之后，被删位置之后的迭代器全部失效；要边遍历边删，用 `it = v.erase(it)`（erase 返回下一个有效迭代器）。
3. clear() 清空元素但**不释放容量**（capacity 不变）。

**人话总结**：erase 删指定，pop_back 删尾，clear 全清。

### 2.6 vector的大小与容量（P33-P35）【重点】

**是什么**：size() 元素个数；capacity() 当前容量；max_size() 最大可容纳数；empty() 判空。

**为什么**：size 和 capacity 是 vector 最容易被混淆的一对——size 是"住了几个人"，capacity 是"房子能住几个人"。

**怎么用**（配套代码 test19，教材 P35 代码）：

```cpp
vector<int> v = { 1,2,3,4,5,6 };
cout << v.size() << endl;      // 6
cout << v.capacity() << endl;  // 6（列表初始化精确分配）
cout << v.max_size() << endl;  // 1073741823（MSVC x86 典型值）
```

**运行输出**：

```text
6
6
1073741823
```

**注意事项**：
1. **capacity ≥ size 恒成立**；push_back 导致 size 超 capacity 时，capacity 按约 1.5~2 倍翻倍扩容（教材/常见实现：1→2→4→8…），旧元素全部搬移。
2. max_size 与编译器/平台有关，正常场景用不到。
3. clear() 后 size 变 0，capacity 不变；C++11 可用 `v.shrink_to_fit()` 释放多余容量（教材扩展）。
4. 提前知道元素数量时用 `v.reserve(n)` 预留容量，避免多次扩容搬移。

**人话总结**：size 是实际个数，capacity 是已分配空间。

### 2.7 vector的赋值与交换（P36-P37）【重点】

**是什么**：assign 重新赋值（覆盖原内容），swap 交换两个同类型 vector 的内容。

**为什么**：批量重置数据、快速交换两个容器。

**怎么用**（配套代码 test20，教材 P37 代码）：

```cpp
vector<int> v1 = { 1,2,3,4 };
vector<int> v2 = { 100,200,300 };

// v.assign(10, 22)       // 注释掉的用法：前10个元素设为22
// v2.assign(v1.begin(), v1.end());  // 注释掉：用v1区间覆盖v2

v1.swap(v2);              // 交换v1、v2内容

for (auto i = v2.begin(); i != v2.end(); i++) {
    cout << *i << " ";    // 交换后v2是原来的v1
}
cout << endl;
for (auto i = v1.begin(); i != v1.end(); i++) {
    cout << *i << " ";    // 交换后v1是原来的v2
}
```

**运行输出**：

```text
1 2 3 4
100 200 300
```

**注意事项**：
1. 配套代码 test20 把 assign 两段注释掉、只演示 swap——设计意图是重点掌握 swap；assign 的两种重载在教材 P36 有说明。
2. assign(n, x)：清空后放 n 个 x；assign(first, last)：清空后用区间元素覆盖。
3. swap 只交换内部指针，O(1) 高效，常用于"清空并释放容量"（`vector<int>().swap(v)`）。

**人话总结**：assign 覆盖赋值，swap 一键互换。

### 2.8 课堂练习：随机数找最大最小值（P38-P39）

**题目**：输入 n，随机 n 个 1-100 的数字装入 vector，找出最大值和最小值。

**解题思路**：push_back 填充随机数 → 遍历比较更新 max/min。

**怎么用**（配套代码 test21，对应教材 P39 代码）：

```cpp
int n;
vector<int> v;
cin >> n;
srand((unsigned)time(0));          // 随机种子
for (int i = 1; i <= n; i++) {
    v.push_back(rand() % 100 + 1); // 1~100
}
int max = v[0], min = v.front();
for (int i = 0; i < n; i++) {
    cout << v[i] << " ";
}
cout << endl;
for (int i = 0; i < n; i++) {
    if (max < v[i]) max = v[i];
    if (min > v[i]) min = v[i];
}
cout << "max = " << max << "   min = " << min << endl;
```

**运行示例**（输入 5，可能输出）：

```text
23 87 5 56 41
max = 87   min = 5
```

**注意事项**：
1. 必须 `srand((unsigned)time(0))` 设置随机种子，否则每次运行结果相同；需要 `#include <ctime>`。
2. `rand() % 100 + 1` 生成 1~100。
3. **隐患**：n=0 时 `v[0]` 越界（未定义行为）。稳妥写法是先判 `v.empty()` 或保证 n≥1。
4. max/min 初值取 `v[0]`，从 i=1 开始比更严谨。

**人话总结**：随机数入 vector，遍历比大小。

### 本章人话总结

1. vector 是动态数组：连续存储、随机访问、自动扩容。
2. 下标 vs at()：一个不查越界、一个查越界抛异常。
3. size vs capacity：实际元素 vs 已分配空间，扩容会搬移元素。
4. 插入删除用迭代器，区间一律左闭右开。
5. 练习题的 n=0 越界是最常见的"隐藏地雷"。

---

## 第3章 stack与queue容器（教材P40-P54）

### 3.1 stack概述（P40-P41）【重点】

**是什么**：stack（栈）是先进后出（LIFO, Last In First Out）的容器，只有一个开口，只能从这一个开口插入和删除数据。

**为什么**：递归、函数调用、括号匹配、撤销操作等场景天然是"后进先出"的结构，栈把这些逻辑封装成极简接口。

**怎么用**：包含 `<stack>`，构造和赋值三种方式（配套代码 test01）：

```cpp
#include <stack>
using namespace std;

stack<int> s1;      // 默认构造
stack<int> s2(s1);  // 拷贝构造
stack<int> s3 = s1; // 赋值
```

**注意事项**：
1. **stack 不允许遍历**：没有 begin()/end()，只能通过 top() 看栈顶。
2. stack 底层默认用 deque 实现（容器适配器，教材扩展），所以接口极简。

**人话总结**：栈是先进后出，只开一个口。

### 3.2 stack的数据存取（P42-P43）【重点】

**是什么**：push 入栈、pop 出栈、top 取栈顶。

**为什么**：三个操作构成栈的全部数据访问——开口处进出。

**怎么用**（配套代码 test02，教材 P43 代码）：

```cpp
stack<int> s;

cout << "s.empty():" << s.empty() << endl;  // 1（空）
s.push(11);
s.push(22);
s.push(33);                                 // 栈：底11 22 33顶
cout << "s.empty():" << s.empty() << endl;  // 0
cout << "s.size():" << s.size() << endl;    // 3

int n = s.top();      // 取栈顶33，不删除
cout << n << endl;    // 33
cout << "s.size():" << s.size() << endl;    // 3（top不删元素）

s.pop();              // 删除栈顶33
cout << "s.size():" << s.size() << endl;    // 2

int n2 = s.top();     // 22
cout << "s.size():" << s.size() << endl;    // 2
cout << n2 << endl;   // 22

/* 注释段示范（危险示范）：
stack<char> s1;
s1.push('a');
s1.top();   // 栈非空时取top没问题；若空栈top()是未定义行为
*/
```

**运行输出**：

```text
s.empty():1
s.empty():0
s.size():3
33
s.size():3
s.size():2
s.size():2
22
```

**注意事项**：
1. **pop() 只删除不返回，top() 只返回不删除**——"取走栈顶"要 `int x = s.top(); s.pop();` 两步连招。
2. **空栈调用 top()/pop() 是未定义行为**（可能崩溃），使用前先判 `!s.empty()`。

**人话总结**：push 进、pop 出、top 偷看，取走要两步。

### 3.3 stack的大小操作（P44-P45）【重点】

**是什么**：empty() 判空，size() 返回元素个数。

**为什么**：遍历栈的唯一合法方式就是"循环判空 + 取顶出栈"。

**怎么用**（教材 P45 代码）：

```cpp
stack<int> s;
s.push(111);
s.push(222);
s.push(333);
cout << s.empty() << endl;   // 0（非空）
cout << s.size() << endl;    // 3

while (!s.empty()) {         // 循环弹出直到空
    cout << s.top() << " ";  // 333 222 111
    s.pop();
}
```

**运行输出**：

```text
0
3
```

**注意事项**：
1. 判空永远在取 top/pop 之前，这是栈代码的"安全带"。
2. 弹栈顺序与入栈相反：先入的先在底部，最后才出来。

**人话总结**：empty 判空、size 数数，循环弹栈是遍历。

### 3.4 课堂练习：十进制转二进制（P46-P47）

**题目**：输入一个十进制整数，输出对应的二进制数。

**解题思路**：不断对 n 取余 2 入栈，n 除以 2，最后依次弹栈输出——余数逆序输出正是二进制的构成，栈的 LIFO 天然匹配。

**怎么用**（配套代码 test03，对应教材 P47 代码）：

```cpp
int n, temp, temp2;
stack<int> s;         // 装余数0/1的栈
cin >> n;

while (n) {           // n不为0循环
    temp = n % 2;     // 取余数
    s.push(temp);     // 余数入栈
    n /= 2;           // n缩小一半
}
while (!s.empty()) {  // 弹栈输出
    temp2 = s.top();
    cout << temp2;
    s.pop();
}
```

**运行示例**（输入 13）：余数序列 1,0,1,1（先算出的先入栈），弹栈输出 1101。

```text
13
1101
```

**顺带扩展**（配套代码 test04，教材未列）：同样的思路可以转十六进制，只是取余 16，且 10-15 要映射成 A-F（switch 分支）——输入 255 输出 FF。这是二进制练习的延伸【教材扩展】。

**注意事项**：
1. n=0 时 while(n) 一次都不进，输出为空——严格应特判输出 0。
2. 弹栈顺序 = 二进制的高位到低位，这正是"先算出的余数是低位、后弹出"的反转效果。

**人话总结**：取余入栈再弹栈，逆序变正序。

### 3.5 queue概述（P48-P49）【重点】

**是什么**：queue（队列）是先进先出（FIFO, First In First Out）的数据结构，有两个出口：从一端（队尾）新增元素，从另一端（队头）移除元素。

**为什么**：排队叫号、任务调度、BFS 广度优先搜索等场景都是"先来先服务"。

**怎么用**：包含 `<queue>`，定义队列（教材 P48）：

```cpp
#include <queue>
using namespace std;
queue<int> q1;
queue<double> q2;
```

**注意事项**：
1. 队列中只有队头和队尾可以被外界使用，**不允许遍历**。
2. 进数据叫入队 push，出数据叫出队 pop。
3. queue 同样是容器适配器，底层默认 deque（教材扩展）。

**人话总结**：队列先进先出，一头进一头出。

### 3.6 queue的构造（P50）

**是什么**：默认构造与拷贝构造。

**怎么用**（配套代码 test05）：

```cpp
queue<int> q1;    // 默认构造
queue<int> q2(q1);// 拷贝构造
queue<int> q3 = q1; // 赋值
```

**人话总结**：队列构造简单，默认+拷贝即可。

### 3.7 queue的相关函数（P51-P52）【重点】

**是什么**：push 队尾入队、pop 队头出队、front 取队头、back 取队尾、empty 判空、size 大小。

**为什么**：六个函数覆盖队列全部操作。

**怎么用**（配套代码 test06，教材 P52 代码）：

```cpp
queue<int> q;
cout << "q.empty():" << q.empty() << endl;   // 1

q.push(11); q.push(22); q.push(33); q.push(44); q.push(55);

cout << "q.empty():" << q.empty() << endl;   // 0
cout << "q.size():" << q.size() << endl;     // 5

int n1 = q.front();   // 队头 11
cout << n1 << endl;
int n2 = q.back();    // 队尾 55
cout << n2 << endl;

q.pop();              // 队头11出队
int n3 = q.front();   // 22
cout << n3 << endl;

while (!q.empty()) {  // 循环出队
    cout << q.front() << " ";
    q.pop();
}
```

**运行输出**：

```text
q.empty():1
q.empty():0
q.size():5
11
55
22
22 33 44 55
```

**注意事项**：
1. **空队列调用 front()/back()/pop() 是未定义行为**。
2. front 是队头（先来的），back 是队尾（后来的）——别搞反。
3. 队列遍历的唯一方式：循环 `front()+pop()`。

**人话总结**：队尾进 push、队头出 pop，front 先 back 后。

### 3.8 课堂练习：扑克牌（P53-P54）

**题目**：有一堆 n 张扑克牌。第一次从牌堆顶上拿出一张牌并输出，第二次把牌放回牌堆底下，重复直到没牌。即：奇数张输出，偶数张放回。

**解题思路**：用 queue 模拟牌堆：一个 bool 标志位（b）翻转控制当前是"输出"还是"移回队尾"。奇数次输出队首并 pop，偶数次把队首 push 回队尾再 pop，然后 b 取反。

**怎么用**（配套代码 test07，对应教材 P54 代码）：

```cpp
int n;
char card;            // 每张牌
queue<char> q;        // 装牌的队列
cin >> n;
for (int i = 0; i < n; i++) {
    cin >> card;
    q.push(card);
}

bool flag = 1;        // 控制奇偶次
while (!q.empty()) {
    if (flag) {                 // 奇数次：输出
        cout << q.front() << " ";
        q.pop();
    }
    else {                      // 偶数次：放回牌堆底
        q.push(q.front());
        q.pop();
    }
    flag = !flag;               // 翻转
}
```

**运行示例**（教材 P53 样例，输入 4 张 1 2 3 4）：

```text
4
1 2 3 4
1 3 2 4
```

推演：第1次输出1；第2次把2放底（3 4 2）；第3次输出3；第4次把4放底（2 4）；第5次输出2；第6次把4放底（4）；第7次输出4。

**注意事项**：
1. flag 每轮取反是关键——用 `bool` + `!` 比 `int` + 取模更直观。
2. "放回牌堆底"= `push(q.front()); pop();` 两步（先复制队首到队尾，再删除队首）。
3. 输入数量必须和 n 一致，否则队列内容不对。

**人话总结**：flag 翻转控制，奇数输出偶数回底。

### 本章人话总结

1. stack：先进后出，只有一个开口，top+pop 连招取栈顶。
2. queue：先进先出，队尾进队头出，front 是队头。
3. 两者都不允许遍历；判空后再取元素是铁律。
4. 栈适合"逆序还原"（进制转换），队列适合"轮流循环"（扑克牌、约瑟夫）。

---

## 第4章 deque与list容器（教材P55-P89）

### 4.1 deque概述（P55-P56）【重点】

**是什么**：deque（双端队列）可以对头端和尾端进行插入删除操作；像 vector 一样能快速随机访问任意元素，又能高效插入删除头部和尾部。

**为什么**：vector 头部插入是 O(n)（要搬移全部元素），deque 头尾插入删除都是 O(1)，是"既要随机访问又要头尾增删"场景的最优解。

**怎么用**：包含 `<deque>`。

```cpp
#include <deque>
using namespace std;
deque<int> d;
```

**注意事项**：
1. deque 底层是"分段连续缓冲区 + 中控器"（教材扩展一句），所以随机访问 O(1) 但常数比 vector 略大。
2. deque 没有 capacity()（教材 P65 标题虽写容量函数，实际只有 size/max_size/resize/empty）。

**人话总结**：deque 是头尾都能快速进出的 vector。

### 4.2 deque的构造（P57-P58）【重点】

**是什么**：四种构造：默认、区间、n 个 elem、拷贝。

**怎么用**（配套代码 test08，教材 P58 代码）：

```cpp
deque<int> d1;                          // 默认构造
deque<int> d2(10);                      // 10个元素，默认0
deque<int> d3(10, 1);                   // 10个元素，值都为1
deque<int> d4(d3);                      // 拷贝构造
deque<int> d5(d3.begin(), d3.begin() + 3);  // 区间[d3.begin(), +3) 共3个元素

for (auto i = d5.begin(); i != d5.end(); i++) {
    cout << *i << " ";                  // 1 1 1
}
```

**运行输出**：

```text
1 1 1
```

**注意事项**：
1. 区间构造左闭右开：`d3.begin() + 3` 只取前 3 个元素。
2. `deque<int> d2(10)` 与 `deque<int> d2{10}` 区别同 vector：圆括号 10 个元素，花括号 1 个元素 10。

**人话总结**：构造四兄弟，区间左闭右开。

### 4.3 deque的添加（P59-P60）【重点】

**是什么**：push_front/push_back 头尾添加，insert 任意位置插入。

**为什么**：push_front 是 deque 相对 vector 的核心优势。

**怎么用**（配套代码 test09，教材 P60 代码）：

```cpp
deque<int> d1;
d1.push_front(4);                  // 头部加4 -> {4}
d1.push_back(5);                   // 尾部加5 -> {4,5}

deque<int>::iterator it = d1.begin();
d1.insert(it, 2);                  // begin前插2 -> {2,4,5}

d1.insert(d1.begin(), 3, 9);       // 头部插3个9 -> {9,9,9,2,4,5}

deque<int> d2 = { 11,22 };
d1.insert(d1.begin(), d2.end() - 1, d2.end());  // 头部插d2尾元素22 -> {22,9,9,9,2,4,5}

for (auto i = d1.begin(); i != d1.end(); i++) {
    cout << *i << " ";
}
```

**运行输出**：

```text
22 9 9 9 2 4 5
```

**注意事项**：
1. `d2.end() - 1` 是最后一个元素（deque 迭代器支持 ±n 运算，list 不行）。
2. 区间插入左闭右开 `[first, last)`：`end()-1 到 end()` 只有 1 个元素。
3. 教材 P60 原代码用 `d2(5,8)`，效果一样，都是尾部元素 8；配套代码用 {11,22} 插 22。

**人话总结**：头尾 push，任意 insert。

### 4.4 deque的删除（P61-P62）【重点】

**是什么**：pop_front/pop_back 头尾删除，erase 任意/区间删除，clear 清空。

**怎么用**（配套代码 test10，教材 P62 代码）：

```cpp
deque<int> d1;
for (int i = 0; i < 10; i++) {
    d1.push_back(i);               // {0,1,2,...,9}
}

d1.pop_front();                    // 删头部0
d1.pop_back();                     // 删尾部9
deque<int>::iterator it = d1.begin();
d1.erase(it);                      // 删begin处的1

d1.erase(d1.begin(), d1.begin() + 2);  // 删区间[begin,begin+2)即2,3

for (auto i = d1.begin(); i != d1.end(); i++) {
    cout << *i << " ";             // 4 5 6 7 8
}
cout << endl;
d1.clear();                        // 清空
for (auto i = d1.begin(); i != d1.end(); i++) {
    cout << *i << " ";             // 无输出
}
```

**运行输出**：

```text
4 5 6 7 8

```

**注意事项**：
1. pop_front 在 vector 上不存在——这是 deque 专属。
2. 区间删除左闭右开；clear 等价 `erase(begin(), end())`。

**人话总结**：头尾 pop，erase 区间，clear 全清。

### 4.5 deque的访问（P63-P64）【重点】

**是什么**：下标访问（不检查越界）、at()（检查越界抛异常）、front()/back() 取首尾。

**为什么**：deque 支持随机访问，所以三种取法都可用；at 更安全。

**怎么用**（配套代码 test11，教材 P64 代码）：

```cpp
deque<int> d1 = { 1,2,3,4,5,6 };
cout << d1[2] << endl;                 // 3（下标不检查越界）

try {
    cout << d1.at(40) << endl;         // at越界抛异常
}
catch (exception e) {
    cout << e.what() << endl;          // 输出异常信息
}

cout << d1.front() << endl;            // 1
cout << d1.back() << endl;             // 6
```

**运行输出**（异常信息随编译器不同，形如 "invalid deque subscript"）：

```text
3
invalid deque subscript
1
6
```

**注意事项**：
1. `d[40]` 越界是未定义行为（不报错，读出垃圾值）；`d.at(40)` 越界抛 `std::out_of_range`。
2. 生产代码优先 at() 或先判 `i < d.size()`。

**人话总结**：下标快但野，at 慢但稳。

### 4.6 deque的容量与其他（P65-P68）【重点】

**是什么**：size/max_size/resize/empty/assign/swap/shrink_to_fit。

**怎么用**（配套代码 test12、test13，教材 P66、P68 代码）：

```cpp
// test12：大小与判空
deque<int> d1 = { 1,2,3,4,5 };
cout << d1.size() << endl;      // 5
cout << d1.max_size() << endl;  // 1073741823（MSVC典型值）
d1.resize(0);                   // 元素个数改为0
cout << d1.size() << endl;      // 0
if (d1.empty()) {
    cout << "没有元素了" << endl;
}

// test13：赋值与交换
deque<int> d2;
d2.assign(3, 1);                // 3个1
deque<int> d3;
d3.assign(3, 2);                // 3个2
d2.swap(d3);                    // 交换
```

**运行输出**（test12）：

```text
5
1073741823
0
没有元素了
```

（test13 交换前 d2: 1 1 1、d3: 2 2 2；交换后 d2: 2 2 2、d3: 1 1 1）

**注意事项**：
1. resize(0) 效果等价 clear()——都让 size 变 0（教材 P65 提到 shrink_to_fit 释放多余空间）。
2. deque 没有 capacity()：resize 扩大时会自动分配。
3. assign 覆盖原内容；swap 只交换内部结构，O(1)。

**人话总结**：size 数数、resize 改大小、swap 互换。

### 4.7 课堂练习：VIP排队（P69-P70）

**题目**：排队程序，VIP 客人不排队（插入队头），普通客人排队尾。将已有 guest1、guest2 放入队列（guest1 在 guest2 前），并把 VIP 客人新增到队列头部。

**解题思路**：deque 头尾都能插——VIP 用 push_front，普通用 push_back。

**怎么用**（配套代码 test14，对应教材 P70 代码）：

```cpp
class Guest {
public:
    string name;
    bool vip;
    Guest(string name, bool vip) {
        this->name = name;
        this->vip = vip;
    }
};

Guest g1("小明", 0);   // 普通
Guest g2("小张", 0);   // 普通
Guest g3("小刚", 1);   // VIP
Guest g4("小强", 1);   // VIP

deque<Guest> dq;
dq.push_front(g3);     // 队头插小刚 -> [小刚]
dq.push_front(g4);     // 队头插小强 -> [小强,小刚]（后插的VIP在最前）
dq.push_back(g2);      // 队尾插小张 -> [小强,小刚,小张]
dq.push_back(g1);      // 队尾插小明 -> [小强,小刚,小张,小明]

for (Guest g : dq) {
    cout << g.name << " ";
}
```

**运行输出**（已用 g++ 实测锁定）：

```text
小强 小刚 小张 小明
```

**注意事项**：
1. 多个 push_front 时，**后插的 VIP 排最前**（每次插到头部）。
2. 教材 P69 的题目描述是 guest1 在 guest2 前；配套代码的数据是 g3/g4 VIP + g2/g1 普通，输出以实际代码推演为准。

**人话总结**：VIP 走队头 push_front，普通排尾 push_back。

### 4.8 list概述（P71-P72）【重点】

**是什么**：list 是序列式容器，本质是双向链表——数据元素通过链表指针串连成逻辑上的线性表。

**为什么**：链表的优点：**任意位置插入、删除都很快**（O(1)，只要你有迭代器）；缺点是**不支持随机访问**（不能下标取元素）。

**怎么用**：包含 `<list>`。

```cpp
#include <list>
using namespace std;
list<int> l;
```

**注意事项**：
1. list **没有 `[]` 和 `at()`**——想取第 k 个元素只能遍历/advance。
2. 底层双向链表，每个节点额外存前后指针，内存开销比 vector 大。

**人话总结**：list 是双向链表，插删快、不能下标。

### 4.9 list的构造（P73）

**是什么**：五种构造：空、n 个默认、n 个指定值、区间、拷贝。

**怎么用**（配套代码 test15，教材 P73 代码）：

```cpp
list<int> l1;                  // 空链表
list<int> l2(10);              // 10个空元素（默认0）
list<int> l3(5, 20);           // 5个20
list<int> l4(l3.begin(), l3.end());  // 区间构造（内容同l3）
list<int> l5(l4);              // 拷贝构造
list<int> l6 = l5;             // 赋值
```

**注意事项**：
1. `list<int> l2(10)`：10 个元素；花括号 `{10}` 则是 1 个元素。
2. list 的迭代器是**双向迭代器**：支持 ++/--/==/!=，不支持 `it + n`、`it1 < it2`、`it1 - it2`（教材 P74 强调）。

**人话总结**：构造五连，注意迭代器不能 +n。

### 4.10 list的插入与删除（P75-P81）【重点】

**是什么**：push_front/pop_front、push_back/pop_back、insert 三兄弟、erase 两兄弟、remove 按值删、clear。

**怎么用**（配套代码 test16、test17、test18）：

```cpp
// test16：头尾插删
list<int> lst = { 1,2,3,4,5 };
lst.push_front(100);     // 头插100 -> {100,1,2,3,4,5}
lst.pop_front();         // 头删100 -> {1,2,3,4,5}
lst.push_back(66);       // 尾插66
lst.pop_back();          // 尾删66
cout << "lst.size():" << lst.size() << endl;   // 5
if (lst.empty()) cout << "lst为空" << endl;
else cout << "lst不为空" << endl;

// test17：插入三兄弟
list<int> l2 = { 1,2,3 };
l2.insert(l2.begin(), 100);        // 头插1个100
l2.insert(l2.begin(), 5, 200);     // 头插5个200
list<int> l3(2, 300);
l2.insert(l2.begin(), l3.begin(), l3.end());  // 头插l3全部

// test18：区间删除（用--移动，不能it-2！）
list<int> l4 = { 1,2,3,4,5 };
l4.erase(l4.begin());              // 删1 -> {2,3,4,5}
list<int>::iterator it = l4.end();
it--;                              // 指向5
it--;                              // 指向4
l4.erase(l4.begin(), it);          // 删[begin,it)即2,3 -> {4,5}
```

**运行输出**：

```text
lst.size():5
lst不为空
（test17: 300 300 200 200 200 200 200 100 1 2 3）
（test18: 4 5）
```

**注意事项**：
1. **list 迭代器不能 `it - 2`、不能 `it + n`**——test18 用两次 `it--` 移动（编译期就能验证：`l4.end() - 2` 会编译错误）。
2. erase 区间左闭右开 `[first, last)`。
3. 教材 P81 示例 `li.erase(li.begin(), li.begin() + 4)` 在 list 上**编译不过**（list 迭代器不支持 +n），正确写法是逐个 ++ 移动或 erase 单元素循环——这是教材笔误，以 P74 的迭代器规则为准。
4. 头尾插删 O(1)，这是 list 相对 vector 的优势。

**人话总结**：头尾 push/pop，插入 erase 用迭代器。

### 4.11 list的排序与反转（P82-P84）【重点】

**是什么**：`l.sort()` 升序、`l.sort(cmp)` 自定义排序、`l.reverse()` 反转。

**为什么**：list 不支持随机访问，**不能使用 std::sort（算法版）**，必须用 list 的成员函数 sort。

**怎么用**（配套代码 test19，教材 P83 代码）：

```cpp
int cmp(const int& v1, const int& v2) {
    return v1 > v2;    // 自定义降序
}

list<int> lst1 = { 11,2,5,3,1,9 };
list<int> lst2(lst1);

lst1.sort();                // 升序 -> 1 2 3 5 9 11
lst1.reverse();             // 反转 -> 11 9 5 3 2 1
lst2.sort(cmp);             // 自定义降序 -> 11 9 5 3 2 1
```

**运行输出**：

```text
11 2 5 3 1 9
lst1 从小到大:1 2 3 5 9 11
lst1.reverse() 从大到小:11 9 5 3 2 1
lst2:11 9 5 3 2 1
```

**注意事项**：
1. **`std::sort(l.begin(), l.end())` 对 list 编译不过**（需要随机访问迭代器）——必须用成员函数 `l.sort()`。
2. `l.sort(cmp)` 的 cmp 是严格弱序：返回 a>b 即降序；`l.reverse()` 是无条件反转。
3. reverse 与降序 sort 结果不同：reverse 不排序只倒序。

**人话总结**：list 排序用成员 sort，反转用 reverse。

### 4.12 list的函数列表（P85-P86）

教材给出了 list 完整函数列表，核心速查：

| 操作 | 函数 |
|---|---|
| 赋值 | assign() |
| 首尾访问 | front() / back() |
| 首尾插删 | push_front/pop_front/push_back/pop_back |
| 插入删除 | insert() / erase() / remove() / remove_if() / clear() |
| 大小 | size() / empty() / resize() / max_size() |
| 排序反转 | sort() / reverse() |
| 合并 | merge() / splice() |
| 去重 | unique() |
| 交换 | swap() |
| 迭代器 | begin/end/rbegin/rend |

**人话总结**：函数全家福，按"插删查改排"记忆。

### 4.13 课堂练习：自定义类型排序（P87-P89）

**题目**：用 list 对 Person 自定义类型排序。Person 有姓名、年龄、身高；排序规则：年龄升序，年龄相同按身高降序。

**解题思路**：写一个自定义比较函数 compare，传给 `L.sort(compare)`。list 的 sort 支持传入比较函数，这是标准 sort 用不了时的标配方案。

**怎么用**（配套代码 test20，对应教材 P88-P89 代码，数据来自配套代码）：

```cpp
class Person {
public:
    int age;
    string name;
    float height;
    Person(string name, int age, float height) {
        this->name = name;
        this->age = age;
        this->height = height;
    }
};

bool compare(Person& p1, Person& p2) {
    if (p1.age == p2.age) {
        return p1.height > p2.height;   // 年龄相同：身高降序
    }
    else {
        return p1.age < p2.age;         // 年龄不同：年龄升序
    }
}

list<Person> lst;
Person p1("王昭君", 500, 199);
Person p2("李白", 500, 182);
Person p3("孙悟空", 300, 180);
Person p4("沙僧", 500, 186);
lst.push_back(p1); lst.push_back(p2); lst.push_back(p3); lst.push_back(p4);

lst.sort(compare);      // 自定义排序

for (auto p = lst.begin(); p != lst.end(); p++) {
    cout << "姓名:" << (*p).name << "  年龄:" << (*p).age << " 身高:" << (*p).height << endl;
}
```

**运行输出**（已用 g++ 实测锁定）：

```text
姓名:孙悟空  年龄:300 身高:180
姓名:王昭君  年龄:500 身高:199
姓名:沙僧  年龄:500 身高:186
姓名:李白  年龄:500 身高:182
```

**注意事项**：
1. compare 必须返回 bool 且满足"严格弱序"：相等时返回 false（a==b 时 compare(a,b) 和 compare(b,a) 都为 false）。
2. 年龄相同组内按身高降序：王昭君199 > 沙僧186 > 李白182。
3. 教材 P88 的 Person 用 `m_name/m_age/m_height` 成员名，配套代码用 name/age/height——理解思路即可，成员名不影响排序逻辑。

**人话总结**：自定义类型排序，写比较函数传 sort。

### 本章人话总结

1. deque：头尾 O(1) 插删 + 随机访问，替代"vector 头插"场景。
2. list：双向链表，任意位置插删快，但无下标、无 std::sort。
3. list 迭代器只能 ++/--，区间移动要逐步走。
4. 自定义排序 = 比较函数 + l.sort(compare)，年龄升序+身高降序的组合规则要写清楚。

---

## 第5章 set/multiset与map/multimap容器（教材P90-P117）

### 5.1 set/multiset概述（P90）【重点】

**是什么**：set/multiset 是关联式容器，底层用二叉树（红黑树）实现；所有元素在插入时**自动排序**。set 不允许重复元素，multiset 允许重复。

**为什么**：自动排序+快速查找（O(log n)）让"集合去重""判断存在"等操作一行搞定。

**怎么用**：包含 `<set>`。

```cpp
#include <set>
using namespace std;
set<int> s;
```

**注意事项**：
1. set 插入自动升序；**只有 insert 一种插入方式**（没有 push_back/push_front）。
2. set 元素不可修改（const），要改先删再插。

**人话总结**：set 自动排序去重，multiset 允许重复。

### 5.2 set的构造与赋值（P91-P92）

**是什么**：默认构造、拷贝构造、等号赋值。

**怎么用**（配套代码 test01，教材 P92 代码）：

```cpp
set<int> s1 = { 3,1,5,4,2,2,3,1 };   // 重复元素自动去重
for (auto i = s1.begin(); i != s1.end(); i++) {
    cout << *i << " ";               // 自动升序：1 2 3 4 5
}
cout << endl;

set<int> s2(s1);   // 拷贝构造
set<int> s3 = s2;  // 赋值
```

**运行输出**（三次遍历结果相同）：

```text
1 2 3 4 5
1 2 3 4 5
1 2 3 4 5
```

**注意事项**：
1. 初始化的 `{3,1,5,4,2,2,3,1}` 有重复：插入后只剩 1,2,3,4,5。
2. set 不允许重复值——重复 insert 会被静默忽略（教材 P92 强调）。

**人话总结**：构造照抄，去重自动完成。

### 5.3 set的插入与删除（P93-P94）【重点】

**是什么**：insert 插入（自动排序去重）、erase(pos)/erase(elem)/erase(beg,end)、clear。

**怎么用**（配套代码 test02，教材 P94 代码）：

```cpp
set<int> s;
s.insert(20); s.insert(10); s.insert(50); s.insert(30); s.insert(40); s.insert(20);
// 打印：10 20 30 40 50（自动排序，20重复被忽略）

s.erase(s.begin());        // 删除最小元素10 -> 20 30 40 50
s.erase(40);               // 按值删除40 -> 20 30 50
s.erase(s.begin(), --s.end());  // 删除[begin, --end) 即20,30 -> 50
s.clear();                 // 清空
```

**运行输出**：

```text
10 20 30 40 50
20 30 40 50
20 30 50
50
（空行）
```

**注意事项**：
1. `erase(elem)` 按值删除；`erase(pos)` 按迭代器删除，都返回下一个元素的迭代器（教材 P93）。
2. `--s.end()` 是最后一个元素；`erase(begin(), --end())` 左闭右开，删到倒数第二个为止。
3. clear() 等价 `erase(begin(), end())`。

**人话总结**：insert 进、erase 删、clear 清。

### 5.4 set的大小与交换（P95-P96）【重点】

**是什么**：size()/empty()/swap()。

**怎么用**（配套代码 test03，教材 P96 代码）：

```cpp
set<int> s = { 1,2,3,5,4,1 };
if (s.empty()) {
    cout << "s.empty():" << s.empty() << endl;
}
else {
    cout << "s.empty():" << s.empty() << endl;   // 0
    cout << "s.size():" << s.size() << endl;     // 5
    printSet(s);                                 // 1 2 3 4 5
}

set<int> s2 = { 11,33,22,55,44 };
cout << "交换之前:" << endl;
printSet(s);    // 1 2 3 4 5
printSet(s2);   // 11 22 33 44 55
s.swap(s2);
cout << "交换之后:" << endl;
printSet(s);    // 11 22 33 44 55
printSet(s2);   // 1 2 3 4 5
```

**运行输出**：

```text
s.empty():0
s.size():5
1 2 3 4 5
交换之前:
1 2 3 4 5
11 22 33 44 55
交换之后:
11 22 33 44 55
1 2 3 4 5
```

**注意事项**：
1. empty() 返回 bool：空=1（true），非空=0。
2. swap 交换的是整个集合内容（O(1) 指针交换）。

**人话总结**：size 数、empty 判、swap 换。

### 5.5 set的查找与统计（P97-P98）【重点】

**是什么**：find(key) 返回迭代器（找不到返回 end()）、count(key) 统计个数。

**为什么**：红黑树 O(log n) 查找，比线性查找快得多。

**怎么用**（配套代码 test04，教材 P98 代码）：

```cpp
set<int> s = { 3,2,1,5,4 };

auto pos = s.find(3);          // 找到3
if (pos != s.end()) {
    cout << "找到了" << endl;   // 找到了
}
else {
    cout << "未找到" << endl;
}

s.insert(3);                   // 重复插入3，无效
s.insert(3);                   // 再插3，仍无效
int cnt = s.count(3);          // set不重复，count只能是0或1
cout << cnt << endl;           // 1
```

**运行输出**：

```text
找到了
1
```

**注意事项**：
1. **set 的 count 只能是 0 或 1**（不允许重复）；multiset 的 count 才可能 >1。
2. find 找不到返回 end()，必须先判 `pos != s.end()` 再解引用。

**人话总结**：find 找位置、count 数个数，set 只有 0/1。

### 5.6 set与multiset的区别（P99-P100）【重点】

**是什么**：multiset 拥有 set 的全部内容，额外允许重复元素。

**对比表**：

| 特性 | set | multiset |
|---|---|---|
| 重复元素 | 不允许 | 允许 |
| insert 行为 | 重复时插入失败（忽略） | 总是成功 |
| count(key) | 0 或 1 | 可为任意 ≥0 |
| find(key) | 返回匹配迭代器 | 返回第一个匹配的迭代器 |
| lower_bound/upper_bound | 返回首个 ≥/>/key 的位置 | 同左（返回第一个发现值） |

**怎么用**（配套代码 test05-test08，教材 P100 代码）：

```cpp
multiset<int> ms = { 3,1,4,5,4,2,1,3,9,11,4,5 };
// 自动排序（保留重复）：1 1 2 3 3 4 4 4 5 5 9 11
cout << "5的个数:" << ms.count(5) << endl;   // 2

int pos = 0;
for (auto i = ms.begin(); i != ms.find(3); i++, pos++);
cout << pos << endl;    // 第一个3前面的元素数 = 3（1,1,2）

auto pos2 = ms.lower_bound(8);   // 第一个≥8的位置 -> 9
cout << *pos2 << endl;           // 9
auto pos3 = ms.upper_bound(8);   // 第一个>8的位置 -> 9
cout << *pos3 << endl;           // 9
```

**运行输出**：

```text
5的个数:2
3
9
9
```

**注意事项**：
1. 教材 P100 注释："{10,20,10,20,30,50} → {10,10,20,20,30,50} 插入时即自动排序"，find(20) 返回**第一个** 20；`*ms.find(20)` 打印的是值本身（20），看不出位置，所以教材说"这样是找不出来的"——要数位置得用迭代器循环。
2. **lower_bound(8)=upper_bound(8)=9**：因为 8 不在集合中，两者都指向第一个 >8 的元素；若查存在的 4：lower_bound(4) 指向第一个4，upper_bound(4) 指向第一个5。【教材扩展】
3. test08 里 `cout << *ms.find(50)` 被注释掉——因为 50 不存在，find 返回 end()，解引用 end() 是未定义行为（错误示范）。

**人话总结**：multiset 能重复，find 返回第一个。

### 5.7 map/multimap概述（P101）【重点】

**是什么**：map 中所有元素都是 pair（键值对）：first 是 key（键值，起索引作用），second 是 value（实值）。所有元素根据 key 自动排序；底层二叉树（红黑树）。map 不允许重复 key，multimap 允许。

**为什么**：需要"按 key 快速找 value"的映射场景（学号→姓名、单词→次数），O(log n) 查找。

**怎么用**：包含 `<map>`。

```cpp
#include <map>
using namespace std;
map<int, int> m;
```

**注意事项**：
1. map 与 set 区别类似：map 不允许重复 key，multimap 允许重复 key。
2. 插入的数据必须是 pair。

**人话总结**：map 是 key→value 字典，自动按 key 排序。

### 5.8 pair对组（P102-P106）【重点】

**是什么**：pair 只含有两个元素（first/second），可以看作只有两个元素的结构体；用于成对数据和 map 插入。

**为什么**：map 的元素就是 pair；pair 也能替代简单的二元结构体。

**怎么用**（配套代码 test09-test11，教材 P104-P106 代码）：

```cpp
// 三种创建方式
pair<int, int> p1;           // 默认构造
pair<int, char> p2;
pair<int, int> p3(10, 20);   // 带值构造

// 访问
pair<string, int> p4("孙悟空", 300);
cout << "姓名:" << p4.first << "  积分:" << p4.second << endl;

// make_pair 赋值（自动推导类型）
pair<int, int> p5;
p5 = make_pair(100, 200);
cout << p5.first << " " << p5.second << endl;   // 100 200

p5 = make_pair(1.342, 3.2343);   // double隐式转int，截断
cout << p5.first << " " << p5.second << endl;   // 1 3

pair<double, double> p6 = make_pair(1.232, 3.2342);  // 类型匹配
pair<char, int> p7 = make_pair('c', 200);
```

**运行输出**：

```text
姓名:孙悟空  积分:300
100 200
1 3
1.232  3.2342
c 200
```

**注意事项**：
1. **make_pair 会自动类型转换**：pair<int,int> 接收 make_pair(1.342, 3.2343) 时 double 截断为 1 和 3——灵活但有小坑（教材 P106 原文提醒）。
2. 标准头文件是 `<utility>`（教材 P103 提示：VS 中某些编译器不声明也能用，因为 pair 在 std 命名空间且 map 间接包含）。
3. 用 `.first`/`.second` 访问，和结构体类似。

**人话总结**：pair 是两个元素的"结构体"，make_pair 自动配类型。

### 5.9 map的构造与赋值（P107-P108）

**是什么**：默认构造、拷贝构造、等号赋值；元素按 key 自动排序。

**怎么用**（配套代码 test12，教材 P108 代码）：

```cpp
map<int, int> m = { pair<int,int>(1,10), pair<int,int>(2,20) };
// 等价写法：map<int, int> m = { {1,10},{2,20} };
// 或 insert：m.insert(pair<int,int>(1,10)); m.insert(pair<int,int>(2,20));

map<int, int> m2(m);    // 拷贝构造
auto mt2 = m2.begin();
cout << mt2->first << "  " << mt2->second << endl;   // 1  10

map<int, int> m3 = m2;  // 赋值
auto mt3 = m3.begin();
cout << mt3->first << "  " << mt3->second << endl;   // 1  10
```

**运行输出**：

```text
1  10
1  10
```

**注意事项**：
1. 遍历 map 时 `it->first` 是 key、`it->second` 是 value（it 是迭代器，-> 访问 pair 成员）。
2. 插入顺序无关紧要，输出永远按 key 升序。

**人话总结**：map 构造拷贝赋值，遍历按 key 排序。

### 5.10 map的大小与交换（P109-P111）【重点】

**是什么**：size()/empty()/swap()。

**怎么用**（配套代码 test13，教材 P111 代码）：

```cpp
map<int, int> m1 = { {6,600}, {1,100},{2,200},{3,300} };
printMap(m1);   // 按key排序：key:1 value:100 / key:2 value:200 / key:3 value:300 / key:6 value:600

if (m1.empty()) cout << "m1为空" << endl;
else {
    cout << "m1 不为空" << endl;
    cout << "m1.size():" << m1.size() << endl;   // 4
}

map<int, int> m2 = { {66,666}, {11,111},{22,222},{3,333} };
m1.swap(m2);    // 交换内容
```

**运行输出**：

```text
key:1 value:100
key:2 value:200
key:3 value:300
key:6 value:600
m1 不为空
m1.size():4
（交换后 m1: key:11 value:111 / key:22 value:222 / key:66 value:666）
（交换后 m2: key:1 value:100 / key:2 value:200 / key:3 value:300 / key:6 value:600）
```

**注意事项**：
1. 注意 test13 的 m2 只有 3 个元素（11/22/66），swap 后 m1 变 3 个元素。
2. swap 交换两个 map 的全部键值对。

**人话总结**：size 数键值对，swap 整体互换。

### 5.11 map的插入与删除（P112-P113）【重点】

**是什么**：四种插入方式 + 三种删除方式。

**对比表（四种插入）**：

| 方式 | 写法 | 特点 |
|---|---|---|
| 1. 匿名 pair | `m.insert(pair<int,int>(1,10))` | 标准写法 |
| 2. make_pair | `m.insert(make_pair(2,20))` | 不用写类型 |
| 3. value_type | `m.insert(map<int,int>::value_type(3,30))` | 教材标注"不建议使用" |
| 4. [] 下标 | `m[4] = 40` | 最简单；key 不存在会**自动创建** |

**怎么用**（配套代码 test14，教材 P113 代码）：

```cpp
map<int, int> m1;

// 四种插入
m1.insert(pair<int, int>(1, 11));            // 方式1
m1.insert(make_pair(2, 22));                 // 方式2
m1.insert(map<int, int>::value_type(3, 33)); // 方式3
m1[1] = 66;                                  // 方式4：key=1已存在，修改value为66

printMap(m1);   // key:1 value:66 / key:2 value:22 / key:3 value:33

// 三种删除
m1.erase(m1.begin());   // 删第一个键值对(1,66)
printMap(m1);           // key:2 value:22 / key:3 value:33

m1.erase(2);            // 按key删除(2,22)
printMap(m1);           // key:3 value:33

m1.erase(m1.begin(), m1.end());  // 区间删除（等价clear）
printMap(m1);           // 空
```

**运行输出**：

```text
key:1 value:66
key:2 value:22
key:3 value:33
key:2 value:22
key:3 value:33
key:3 value:33
（空）
```

**注意事项**：
1. **`m[key]` 的双重身份**：key 不存在→自动创建（value 为默认值0）并返回引用；key 存在→修改 value。用它查询不存在的 key 会**意外插入**——教材 P113 注释："[] 不建议插入"。
2. 删除用 `m.erase(key)` 按 key 删最方便；`erase(pos)` 返回下一个元素的迭代器。
3. clear() 等价 `erase(begin(), end())`。

**人话总结**：插入四法，[] 最简但会偷建，删除按 key。

### 5.12 map的查找与统计（P114-P115）【重点】

**是什么**：find(key) 返回迭代器、count(key) 统计（map 只有 0/1）。

**怎么用**（配套代码 test15，教材 P115 代码）：

```cpp
map<int, int> m = { {1,11},{2,22},{3,33} };

auto it = m.find(3);
if (it != m.end()) {
    cout << it->first << "  " << it->second << endl;   // 3  33
}
else {
    cout << "未找到" << endl;
}

int pos = 0;
for (auto i = m.begin(); i != m.find(2); i++, pos++);  // 数2前面有几个
cout << pos + 1 << endl;   // 2（key=2是第2个）

int num = m.count(10);
cout << num << endl;       // 0（不存在）
```

**运行输出**：

```text
3  33
2
0
```

**注意事项**：
1. find 找不到返回 end()，先判再解引用。
2. map 的 count 只能是 0 或 1；统计重复 key 要用 multimap。
3. 遍历"数位置"的循环：`for (auto i = m.begin(); i != m.find(2); i++, pos++);` 分号结尾表示空循环体，只数不做事。

**人话总结**：find 查、count 数，map 的 count 只有 0/1。

### 5.13 multimap的特点（P116-P117）【重点】

**是什么**：multimap 拥有 map 的全部内容，额外允许重复 key——一个 key 对应多个 value（如一个学生有多门考试成绩）。

**怎么用**（配套代码 test16-test19，教材 P117 代码）：

```cpp
// 基础操作：test16 构造、test17 插入删除（按key删/迭代器删/区间删）
multimap<int, int> m;
m.insert(make_pair(1, 11));  // 插入总是成功，允许重复key
// ...

// 查找同key的所有value：find + count（教材P117）
multimap<string, int> m_map;
string name = "XiaoMing";
m_map.insert(make_pair(name, 50));
m_map.insert(make_pair(name, 55));
m_map.insert(make_pair(name, 60));
m_map.insert(make_pair("zhangsan", 30));

multimap<string, int>::iterator it = m_map.find(name);
for (int k = 0; k != m_map.count(name); k++, it++) {
    cout << it->first << "--" << it->second << endl;
}
```

**运行输出**（教材 P117）：

```text
XiaoMing--50
XiaoMing--55
XiaoMing--60
```

**注意事项**：
1. **multimap 没有 `[]` 和 `at()`**（无法用 key 下标访问，因为一个 key 对应多个 value）。
2. 遍历同一 key 的所有 value：`find()` 拿第一个 + `count()` 拿数量，循环迭代；或 `equal_range()` 一次性拿区间【教材扩展】。
3. 配套代码 test18 有个小笔误：打印"交换后"前漏调了 `m.swap(m2)`，两次输出相同——正确代码应先 swap 再打印。
4. test19 的 `count(2)` 输出 7（键值对 {2,22},{2,22},{2,23},{2,21},{2,22},{2,22},{2,234} 共 7 个，已实测）；`lower_bound(2)` 指向第一个 key≥2 的 (2,22)，`upper_bound(2)` 指向第一个 key>2 的 (3,33)。【教材扩展】

**人话总结**：multimap 一 key 多值，find+count 或 equal_range 遍历。

### 本章人话总结

1. set 自动排序去重，multiset 允许重复；count 前者 0/1、后者可多。
2. map 是 key→value 字典，自动按 key 排序；multimap 一 key 多值。
3. pair 是 map 的元素类型，make_pair 自动推导类型（小心隐式截断）。
4. `m[key]` 会偷建不存在的键——查询用 find，别用 []。
5. 自定义类型进 set/map 需要提供比较规则（教材未展开，扩展提示）。

---

# 第6章 STL常用算法——遍历与查找（教材P118-P136）

## 6.1 算法概述：三件套头文件（P118）

**是什么**：STL 的算法不挂在容器身上，而是集中放在头文件里，主要由 `<algorithm>`、`<numeric>`、`<functional>` 三件套提供。

**为什么**：容器负责存数据，算法负责处理数据。算法写成模板函数独立出来，vector、list、deque 等任何容器都能共用同一套遍历、查找、排序代码，不必每个容器重写一遍。

**怎么用**：

```cpp
#include <algorithm>  // 最大：比较、交换、查找、遍历、复制、修改等
#include <numeric>    // 很小：accumulate、fill 等序列上的简单数学运算
#include <functional> // 仿函数模板类：greater 等函数对象
```

**注意事项**：
1. 本章所有遍历、查找算法都在 `<algorithm>` 里，忘写这个 include 会报"未声明的标识符"。
2. `<functional>` 平时存在感弱，但只要用到仿函数（如 `greater<int>()`）就必须包含它。

**人话总结**：算法住在这三个头文件里。

## 6.2 for_each：最常用的遍历（P119-P121）

**是什么**：`for_each(iterator beg, iterator end, _func)` 对区间 `[beg, end)` 内每个元素执行一次 `_func`，是最常用的遍历算法。

**为什么**："对每个元素做同一件事"（比如打印）如果手写 for 循环又长又重复，for_each 一行搞定，而且普通函数和仿函数都能接收。

**怎么用**：

```cpp
//普通函数
void print01(int val) { cout << val << " "; }
//仿函数：重载 operator() 的类
class print02 {
public:
    void operator()(int val) { cout << val << " "; }
};

void test01() {
    vector<int> v = { 2, 1, 3, 4, 5 };
    for_each(v.begin(), v.end(), print01);   //传普通函数：不带括号
    cout << endl;
    for_each(v.begin(), v.end(), print02()); //传仿函数：必须带括号
    cout << endl;
}
```

预期输出（打印两遍）：

```
2 1 3 4 5
2 1 3 4 5
```

**注意事项**：
1. 传仿函数必须写 `print02()` 带括号——括号表示创建一个临时对象传进去；只写类名 `print02` 编译不过。
2. 传普通函数写函数名 `print01` 即可，不要带括号；写成 `print01()` 就变成"先调用它再传返回值"，类型对不上。
3. `_func` 的形参是元素值，只打印用值传递即可；想修改元素需要传引用。

**人话总结**：挨个把元素喂给函数。

## 6.3 transform：搬运容器到另一个容器（P122-P123）

**是什么**：`transform(iterator beg1, iterator end1, iterator beg2, _func)` 把源容器 `[beg1, end1)` 的每个元素经 `_func` 加工后，放进目标容器从 `beg2` 开始的位置。

**为什么**：想"基于旧容器生成新容器"（例如全体元素+100）时，不用自己写循环再 push_back，transform 一句话同时完成运算和搬运。

**怎么用**：

```cpp
class Transform {
public:
    int operator()(int v) { return v + 100; } //每个元素+100
};
class Myprint {
public:
    void operator()(int val) { cout << val << " "; }
};

void test02() {
    vector<int> v = { 1, 2, 3, 4, 5 };
    vector<int> vTarget;              //目标容器
    vTarget.resize(v.size());         //必须提前开辟空间！
    transform(v.begin(), v.end(), vTarget.begin(), Transform());
    for_each(vTarget.begin(), vTarget.end(), Myprint());
    cout << endl;
}
```

预期输出：

```
101 102 103 104 105
```

**注意事项**：
1. 目标容器必须提前 `resize()` 开好空间。transform 是直接往 `beg2` 指向的位置写数据，不会自动 push_back；不开空间程序直接崩溃。
2. 仿函数 `Transform` 的 `operator()` 要有返回值（加工结果），这与 6.2 节只打印不返回的 print 类不同。
3. 搬运是"复制+加工"，源容器保持不变。

**人话总结**：加工后搬进新容器，先 resize。

## 6.4 查找算法总览（P124）

STL 常用查找算法共五个（外加两个统计）：`find` 按值查找元素、`find_if` 按条件查找元素、`adjacent_find` 查找相邻重复元素、`binary_search` 二分查找、`count` 统计元素个数、`count_if` 按条件统计元素个数。下面逐个击破。

## 6.5 find：按值查找（P125-P126）

**是什么**：`find(iterator beg, iterator end, value)` 按值查找元素，找到返回指向该元素的迭代器，找不到返回结束迭代器 `end()`。

**为什么**：想知道"容器里有没有某个值"，find 是最直接的办法，而且对各种容器通用。

**怎么用**：

```cpp
void test03() {
    vector<int> v = { 2, 3, 4, 1 };
    //查找容器中是否有11这个元素
    vector<int>::iterator it = find(v.begin(), v.end(), 11);
    if (it == v.end()) {
        cout << "not found" << endl; //11不在容器里
    }
    else {
        cout << "found: " << *it << endl;
    }
}
```

预期输出：

```
not found
```

**注意事项**：
1. 判断成败只有一个标准：`it == v.end()` 就是没找到，这是 find 的固定约定。
2. 找到之后 `*it` 才是元素值；对 `end()` 解引用是未定义行为，必须先判断再用。
3. find 用 `==` 从头逐个比较，找到第一个就停；数据无序也能用，但效率是 O(n)。

**人话总结**：按值找，找不到给 end()。

## 6.6 find_if：按条件查找（P127-P128）

**是什么**：`find_if(iterator beg, iterator end, _Pred)` 按条件查找元素，`_Pred` 是返回 bool 的仿函数（谓词），返回第一个满足条件的元素的迭代器。

**为什么**：find 只能找"等于某个值"，当判断规则是自己定的（比如"找出第一个5"），就要用 find_if 把条件作为谓词传进去。

**怎么用**：

```cpp
class Five {  //谓词：判断是否等于5
public:
    bool operator()(int val) {
        return val == 5;
    }
};

void test04() {
    vector<int> v = { 2, 3, 5, 5, 5, 4, 1, 5, 6, 7 };
    vector<int>::iterator it = find_if(v.begin(), v.end(), Five());
    if (it == v.end()) {
        cout << "not found" << endl;
    }
    else {
        cout << "found: " << *it << endl; //返回第一个满足条件的
    }
}
```

预期输出：

```
found: 5
```

**注意事项**：
1. 谓词必须写 `Five()` 带括号创建临时对象，且 `operator()` 返回值必须是 bool。
2. find_if 只返回第一个满足条件的元素；容器里有多个 5，也只给你第一个。
3. 找不到同样返回 `end()`，判断方式与 find 完全相同。

**人话总结**：条件当参数，找到第一个算数。

## 6.7 adjacent_find：查找相邻重复元素（P129-P130）

**是什么**：`adjacent_find(iterator beg, iterator end)` 查找相邻且相等的重复元素，返回第一对中前一个元素的迭代器。

**为什么**：想检测"有没有两个挨着的元素相等"（如重复录入检查），手写循环要比较 v[i] 和 v[i+1]，adjacent_find 一行完成。

**怎么用**：

```cpp
void test05() {
    vector<int> v = { 2, 2, 3, 3, 4, 5 };
    vector<int>::iterator pos = adjacent_find(v.begin(), v.end());
    if (pos == v.end()) {
        cout << "not found" << endl;
    }
    else {
        cout << "found: " << *pos << endl; //第一对相邻重复的第一个
    }
}
```

预期输出：

```
found: 2
```

**注意事项**：
1. 只比较"紧挨着"的两个元素，`{1, 2, 1, 2}` 这种间隔出现的重复不算。
2. 只返回第一对相邻重复的位置，后面还有 `3, 3` 也不再返回。
3. 找不到返回 `end()`，判断方式同 find。

**人话总结**：专抓挨在一起的重复元素。

## 6.8 binary_search：二分查找（P131-P132）

**是什么**：`bool binary_search(iterator beg, iterator end, value)` 用二分法查找指定元素是否存在，查到返回 true，否则返回 false。

**为什么**：数据量大且有序时，二分查找比逐个比较快得多（O(log n)），一行代码就能用。

**怎么用**：

```cpp
void test06() {
    vector<int> v;
    for (int i = 0; i < 10; i++) {
        v.push_back(i);              //0 1 2 ... 9，有序序列
    }
    //注意：容器必须是有序序列
    bool ret = binary_search(v.begin(), v.end(), 66);
    if (ret) {
        cout << "found" << endl;
    }
    else {
        cout << "not found" << endl;
    }
}
```

预期输出：

```
not found
```

**注意事项**：
1. **容器必须有序**！教材明确强调"在无序序列中不可用"。如果往有序数据里混入乱序值（如教材注释的 `v.push_back(2)` 那样），结果未知——可能明明有却说没有，也可能明明没有却说有。
2. 返回值是 bool 不是迭代器，想知道元素位置请用 find。
3. binary_search 只回答"有没有"，find 告诉你"在哪"，用途不同别混用。

**人话总结**：先有序，再二分，只答有无。

## 6.9 count：统计元素个数（P133-P134）

**是什么**：`count(iterator beg, iterator end, value)` 统计区间内等于 value 的元素出现次数。

**为什么**：想知道"某个值出现了几次"，本来要一个循环加一个 if，count 一个函数搞定。

**怎么用**：

```cpp
void test07() {
    vector<int> v = { 2, 2, 3, 3, 5, 5, 5, 4, 1, 1, 5, 6, 6, 7 };
    //统计容器中6元素有几个
    int num = count(v.begin(), v.end(), 6);
    cout << "num = " << num << endl;
}
```

预期输出：

```
num = 2
```

**注意事项**：
1. 返回值是 int（元素个数），一个都没有就返回 0，不会报错。
2. 统计依据是 `==` 比较，自定义类型需要重载 `==` 才能使用。

**人话总结**：数一数某值出现几次。

## 6.10 count_if：按条件统计（P135-P136）

**是什么**：`count_if(iterator beg, iterator end, _Pred)` 按谓词条件统计满足条件的元素个数。

**为什么**：要数的是"大于10的有几个"这类条件个数时，count 帮不上忙，count_if 把判断规则交给谓词完成。

**怎么用**：

```cpp
class Greater10 {  //谓词：大于10
public:
    bool operator()(int val) {
        return val > 10;
    }
};

void test08() {
    vector<int> v = { 2, 12, 3, 3, 5, 5, 5, 4, 11, 1, 5, 6, 6, 7, 10 };
    int num = count_if(v.begin(), v.end(), Greater10());
    cout << "num = " << num << endl; //大于10的只有12和11
}
```

预期输出：

```
num = 2
```

**注意事项**：
1. 谓词 `Greater10()` 同样要带括号创建临时对象，返回 bool。
2. 注意 10 本身不满足"大于10"，本例中 10 不计入，所以结果是 2 而不是 3。
3. 与 count 一样返回 int 个数，没有满足条件的元素返回 0。

**人话总结**：数满足条件的元素个数。

## 6.11 易混算法对比

| 对比 | 区别 | 共同点 |
|------|------|--------|
| find vs find_if | find 按值查找（给具体值）；find_if 按谓词条件查找（给判断规则） | 找不到都返回 `end()`，都用 `it == end()` 判断 |
| count vs count_if | count 按值统计个数；count_if 按谓词条件统计个数 | 都返回 int 个数，没有则 0 |
| for_each vs transform | for_each 只遍历处理（如打印），不搬数据；transform 把加工结果搬进另一个容器 | 都能接普通函数或仿函数；传仿函数都要带括号 |

**记忆口诀**：名字带 `if` 的用谓词（find_if、count_if）；用 transform 先给目标容器 resize。

### 本章人话总结

1. 算法三件套：`<algorithm>` 是主力管遍历查找排序，`<numeric>` 管数学运算，`<functional>` 管仿函数（P118）。
2. for_each 遍历打印、transform 搬运加工；transform 的目标容器必须提前 resize，否则崩溃（P119-123）。
3. find/count 按值干活，find_if/count_if 按谓词干活；找不到一个返回 end()、一个返回 0（P125-128、P133-136）。
4. binary_search 的前提是容器必须有序，无序序列结果未定义，这是高频考点（P131-132）。
5. adjacent_find 只认紧挨着的重复元素，返回第一对中前一个的位置（P129-130）。

---

## 第7章 STL常用算法——排序、拷贝替换与集合 + 综合练习（教材P137-P171）

### 7.1 常用排序算法总览（P137）

| 算法 | 功能 |
|---|---|
| sort | 对容器内元素排序 |
| random_shuffle | 洗牌：随机调整元素次序 |
| merge | 合并两个有序容器到另一容器 |
| reverse | 反转指定范围元素 |

### 7.2 sort（P138-P139）【重点】

**是什么**：sort 对容器内元素排序，默认升序，可传谓词（仿函数/函数指针）降序。

**为什么**：排序是最高频算法，sort 基于快排+插入排序优化，平均 O(n log n)。

**怎么用**（配套代码 v4 test09，教材 P139 代码）：

```cpp
template<typename T>
class greater09 {          // 自定义仿函数：降序比较
public:
    bool operator()(T& a, T& b) {
        return a > b;
    }
};

vector<int> v = { 2,3,1,5,4,6 };
sort(v.begin(), v.end());              // 默认升序
for_each(v.begin(), v.end(), print01); // 1 2 3 4 5 6

sort(v.begin(), v.end(), greater09<int>());  // 自定义降序
for_each(v.begin(), v.end(), print01);       // 6 5 4 3 2 1
```

**运行输出**：

```text
1 2 3 4 5 6
6 5 4 3 2 1
```

**注意事项**：
1. `sort(beg, end, greater<int>())` 也是标准降序写法（需 `<functional>`）。
2. **sort 需要随机访问迭代器**——只能用于 vector/deque/string/数组，不能用于 list（list 用成员函数 l.sort()）。
3. 自定义仿函数类要重载 `operator()` 返回 bool。

**人话总结**：sort 升序默认，传比较器降序。

### 7.3 random_shuffle（P140-P141）

**是什么**：洗牌，把指定范围元素随机打乱。

**为什么**：抽奖、出题乱序、模拟等场景需要随机排列。

**怎么用**（配套代码 v4 test10，教材 P141 代码）：

```cpp
srand((unsigned)time(0));          // 随机种子（必须！）
vector<int> v = { 1,2,3,4,5,6 };
random_shuffle(v.begin(), v.end());
for_each(v.begin(), v.end(), print01);   // 每次运行顺序不同
```

**运行示例**（每次不同）：

```text
4 1 6 3 5 2
```

**注意事项**：
1. **必须 srand 设置随机种子**（配合 `#include <ctime>`），否则每次运行洗牌结果相同。
2. C++11 起推荐 `std::shuffle` + 随机引擎（教材扩展）。
3. 需要 `<algorithm>`。

**人话总结**：洗牌前先 srand 播种。

### 7.4 merge（P142-P143）

**是什么**：两个有序容器合并（归并）到一个目标容器。

**为什么**：归并排序、合并有序数据流。

**怎么用**（配套代码 v4 test11，教材 P143 代码）：

```cpp
vector<int> v1 = { 1,2,5,6 };
vector<int> v2 = { 3,4,7,9 };
vector<int> vt;
vt.resize(v1.size() + v2.size());          // 目标容器必须提前开空间！
merge(v1.begin(), v1.end(), v2.begin(), v2.end(), vt.begin());
for_each(vt.begin(), vt.end(), print01);   // 1 2 3 4 5 6 7 9
```

**运行输出**：

```text
1 2 3 4 5 6 7 9
```

**注意事项**：
1. **两个源容器必须有序**（升序），否则结果错误。
2. **目标容器必须提前 resize**（大小至少 v1+v2），否则越界/崩溃。
3. 结果仍是有序的。

**人话总结**：两个有序容器 merge，目标先 resize。

### 7.5 reverse（P144-P145）

**是什么**：反转指定范围的元素。

**怎么用**（配套代码 v4 test12，教材 P145 代码）：

```cpp
vector<int> v = { 1,3,5,8,9,12,16,20 };
reverse(v.begin(), v.end());
for_each(v.begin(), v.end(), print01);   // 20 16 12 9 8 5 3 1
```

**运行输出**：

```text
20 16 12 9 8 5 3 1
```

**注意事项**：
1. reverse 是原地反转，不返回新容器。
2. 需要 `<algorithm>`。

**人话总结**：reverse 原地倒序。

### 7.6 常用拷贝和替换算法总览（P146）

| 算法 | 功能 |
|---|---|
| copy | 范围拷贝到另一容器 |
| replace | 旧值替换为新值 |
| replace_if | 满足条件的元素替换 |
| swap | 交换两个容器 |

### 7.7 copy（P147-P148）

**是什么**：把指定范围元素拷贝到目标容器。

**怎么用**（配套代码 v4 test13，教材 P148 代码）：

```cpp
vector<int> v1 = { 1,2,3,45,6,7,89 };
vector<int> v2;
v2.resize(v1.size());                    // 目标先resize
copy(v1.begin(), v1.end(), v2.begin());
for_each(v2.begin(), v2.end(), print01); // 1 2 3 45 6 7 89
```

**运行输出**：

```text
1 2 3 45 6 7 89
```

**扩展**（配套代码 v4 test130）：copy_if 按条件拷贝（`copy_if(v1.begin(), v1.end(), v2.begin(), Greater130())`，Greater130 是 v>2 的仿函数，输出 3 45 6 7 89）【教材扩展】。

**注意事项**：
1. **目标容器必须提前 resize**（至少源的大小）。
2. 需要 `<algorithm>`。

**人话总结**：copy 搬家，先给新家腾地方。

### 7.8 replace（P149-P150）

**是什么**：把区间内所有等于旧值的元素替换为新值。

**怎么用**（配套代码 v4 test14，教材 P150 代码）：

```cpp
vector<int> v = { 1,2,3,1,2,4,1,2,5 };
replace(v.begin(), v.end(), 1, 1111);    // 所有1 → 1111
for_each(v.begin(), v.end(), print01);   // 1111 2 3 1111 2 4 1111 2 5
```

**运行输出**：

```text
1111 2 3 1111 2 4 1111 2 5
```

**注意事项**：
1. replace 按"值相等"匹配（`==` 比较）。
2. 需要 `<algorithm>`。

**人话总结**：replace 按值替换所有旧元素。

### 7.9 replace_if（P151-P152）

**是什么**：把区间内**满足谓词条件**的元素替换为新值。

**怎么用**（配套代码 v4 test15，教材 P152 代码）：

```cpp
class Greater20 {              // 谓词仿函数
public:
    bool operator()(int v) {
        return v > 20;
    }
};

vector<int> v = { 1,20,31,1,20,41,1,20,51 };
replace_if(v.begin(), v.end(), Greater20(), 9999);   // >20 的 → 9999
for_each(v.begin(), v.end(), print01);   // 1 20 9999 1 20 9999 1 20 9999
```

**运行输出**：

```text
1 20 9999 1 20 9999 1 20 9999
```

**对比表（replace vs replace_if）**：

| 特性 | replace | replace_if |
|---|---|---|
| 匹配方式 | 值相等（==） | 谓词条件（自定义） |
| 参数 | oldvalue, newvalue | _Pred, newvalue |
| 典型场景 | 固定值替换 | 范围条件替换（>x、==x…） |

**注意事项**：
1. 谓词是返回 bool 的仿函数（或函数指针/lambda）。
2. 教材 P152 的 Greater20 实为 `val == 20`（按题意"大于20"其实应写 `val > 20`）——配套代码用 `v > 20` 更贴近题意，两者都能跑，注意区分。

**人话总结**：replace_if 按条件替换，谓词说了算。

### 7.10 swap（P153-P154）

**是什么**：交换两个容器的元素。

**怎么用**（配套代码 v4 test16，教材 P154 代码）：

```cpp
vector<int> v1 = { 1,2,3 }, v2 = { 5,6,7 };
swap(v1, v2);    // 交换后 v1={5,6,7}，v2={1,2,3}
```

**运行输出**：

```text
1 2 3
5 6 7
5 6 7
1 2 3
```

**注意事项**：
1. 两个容器类型必须相同。
2. vector 的 swap 是 O(1)（只换内部指针）。

**人话总结**：swap 互换两个容器。

### 7.11 算术生成算法：accumulate 与 fill（P155-P159）

**是什么**：accumulate 计算区间元素累计总和；fill 向容器填充指定元素。**头文件是 `<numeric>`**（不是 algorithm！）。

**怎么用**（配套代码 v4 test17、test18，教材 P157、P159 代码）：

```cpp
#include <numeric>

vector<int> v = { 1,2,3,4,5 };
int total = accumulate(v.begin(), v.end(), 0);   // 初始值0
cout << total << endl;    // 15（1+2+3+4+5）

fill(v.begin(), v.end(), 100);   // 全部填充100
for_each(v.begin(), v.end(), print01);  // 100 100 100 100 100
```

**运行输出**：

```text
15
100 100 100 100 100
```

**注意事项**：
1. **accumulate/fill 在 `<numeric>`**，不是 `<algorithm>`——漏包含会报错（教材 P155 特别强调）。
2. accumulate 第三个参数是初始值：`accumulate(..., 100)` 结果 = 100+15 = 115。
3. fill 之前容器要有元素（先 resize 或已有数据），否则填充无效/越界。

**人话总结**：求和用 accumulate，填充用 fill，都在 numeric 里。

### 7.12 常用集合算法总览（P160）

| 算法 | 功能 |
|---|---|
| set_intersection | 求两个有序容器交集 |
| set_union | 求两个有序容器并集 |
| set_difference | 求两个有序容器差集 |

**共同前提**：两个容器必须是有序序列；目标容器必须提前 resize；返回值是结果尾迭代器（不是 begin）。

### 7.13 set_intersection 交集（P161-P162）

**怎么用**（配套代码 v4 test19，教材 P162 代码）：

```cpp
vector<int> v1 = { 1,3,4,5,6,7,8 };
vector<int> v2 = { 2,3,5,6,8 };
vector<int> v3;
v3.resize(min(v1.size(), v2.size()));      // 预留：取较小size

auto pos = set_intersection(v1.begin(), v1.end(), v2.begin(), v2.end(), v3.begin());
// 交集：3 5 6 8（教材代码把打印注释了，若解开：）
for_each(v3.begin(), pos, print01);        // 用pos不是v3.end()！
```

**运行输出**（若解开注释）：

```text
3 5 6 8
```

**注意事项**：
1. **目标容器大小取 min(v1.size(), v2.size())**（交集最多不超过小容器）。
2. 打印范围是 `[v3.begin(), pos)`——pos 是返回值，不是 v3.end()（教材注释里就藏着这个知识点）。

**人话总结**：交集取小者容量，返回尾迭代器。

### 7.14 set_union 并集（P163-P164）

**怎么用**（配套代码 v4 test20，教材 P164 代码）：

```cpp
vector<int> v1 = { 1,2,3,4 };
vector<int> v2 = { 3,4,5,6 };
vector<int> v3;
v3.resize(v1.size() + v2.size());          // 预留：两者size之和

auto pos = set_union(v1.begin(), v1.end(), v2.begin(), v2.end(), v3.begin());
for_each(v3.begin(), pos, print01);        // 1 2 3 4 5 6
```

**运行输出**：

```text
1 2 3 4 5 6
```

**注意事项**：
1. **目标容器大小取 v1.size() + v2.size()**（并集最多是两者之和，最坏情况无交集）。
2. 并集结果自动去重且有序。

**人话总结**：并集取两容器之和，自动去重排序。

### 7.15 set_difference 差集（P165-P166）

**是什么**：v1-v2 = 在 v1 中但不在 v2 中的元素；**v1-v2 与 v2-v1 结果不同**。

**怎么用**（配套代码 v4 test21，教材 P166 代码）：

```cpp
vector<int> v1 = { 1,2,3,4,5 };
vector<int> v2 = { 2,4,5,6,8 };
vector<int> v3;
v3.resize(max(v1.size(), v2.size()));      // 预留：取较大size

auto pos1 = set_difference(v1.begin(), v1.end(), v2.begin(), v2.end(), v3.begin());
for_each(v3.begin(), pos1, print01);       // v1-v2：1 3

auto pos2 = set_difference(v2.begin(), v2.end(), v1.begin(), v1.end(), v3.begin());
for_each(v3.begin(), pos2, print01);       // v2-v1：6 8
```

**运行输出**（修正版）：

```text
1 3
6 8
```

**⚠️ 配套代码 bug 提示**：v4 test21 第二段打印误写成 `for_each(v3.begin(), pos1, print01)`（用了 pos1 而不是 pos2），实际运行会**把第一段的结果 1 3 再打印一遍**。正确应改为 `pos2`。这是很好的"拷贝粘贴改一半"典型错误。

**对比表（三个集合算法）**：

| 算法 | 结果 | 目标容器预留 | 要求 |
|---|---|---|---|
| set_intersection | 交集 | min(size1, size2) | 两容器有序 |
| set_union | 并集（去重） | size1 + size2 | 两容器有序 |
| set_difference | v1 有 v2 无 | max(size1, size2) | 两容器有序 |

**注意事项**：
1. 差集方向敏感：v1-v2 ≠ v2-v1。
2. 三个算法都要 `<algorithm>`，都要有序，都要 resize，都用返回的尾迭代器遍历。

**人话总结**：交集 min、并集和、差集 max，方向别搞反。

### 7.16 课堂练习：约瑟夫问题（P167-P168）

**题目**：共 n 个人，每次数到第 m 个人时出圈，出圈后从 1 重新数，直到所有人都出圈，按顺序输出出圈人编号。

**解题思路**：用 queue 模拟围成一圈的人。从队头开始报数：没到 m 的人"先读入再弹出"（移到队尾，继续下一轮报数）；数到 m 的人输出编号并弹出（出圈）；然后重新从 1 报数。

**怎么用**（配套代码 v4 test22，对应教材 P168 代码）：

```cpp
queue<int> q;
int n, m, num = 1;      // n个人，数到m出圈，num报数器
cin >> n >> m;
for (int i = 1; i <= n; i++) {
    q.push(i);          // 1~n全部入队
}
while (!q.empty()) {    // 队列非空时模拟报数
    if (num == m) {                 // 报数到m：出圈
        cout << q.front() << " ";   // 输出
        q.pop();                    // 出队
        num = 1;                    // 重新计数
    }
    else {                          // 没到m：移到队尾
        num++;                      // 报数+1
        q.push(q.front());          // 队首复制到队尾
        q.pop();                    // 队首出队
    }
}
```

**运行示例**（n=6, m=3，已用 g++ 实测锁定）：

```text
6 3
3 6 4 2 5 1
```

推演：1 2 3 4 5 6 → 报1(1)报2(2)报3(3出圈) → 4 5 6 1 2 → 报1(4)报2(5)报3(6出圈) → 1 2 4 5 → 报1(1)报2(2)报3(4出圈) → 5 1 2 → 报1(5)报2(1)报3(2出圈) → 5 1 → 报1(5)报2(1)报3(5出圈) → 1 → 报1(1)报2(1)报3(1出圈)。

**注意事项**：
1. "移到队尾"= `push(q.front()); pop();` 两步连招（先复制后删除）。
2. num 到 m 后必须重置为 1，否则报数不会重新开始。
3. 这个写法在 n=1 时也能正确输出（自己数自己出圈）。

**人话总结**：队列转圈报数，到 m 出圈，其余回队尾。

### 7.17 课堂练习：表达式括号匹配（P170 + 表达式括号匹配.cpp）

**题目**：表达式由英文字母（小写）、运算符（+、-、*、/）和左右圆括号构成，以 '@' 结束。检查左右括号是否匹配：匹配输出 YES，否则 NO。表达式长度 <255，左括号 <20 个。

**输入样例**：`2*(x+y)/(1-x)@` → 输出 YES

**解题思路**：用 stack：遇 '(' 入栈；遇 ')' 时若栈顶是 '(' 则配对弹出（否则不匹配）；最后栈空则全部配对 → YES，栈非空（有未配对的 '('）→ NO。

**怎么用**（配套代码 表达式括号匹配.cpp 逐行讲解）：

```cpp
#include <iostream>
#include <cstdio>
#include <stack>
#include <cstring>
using namespace std;

stack<char> stk;        // 存左括号的栈
char str[256];          // 存表达式

int main() {
    cin >> str;                    // 读表达式（cin遇空格停，符合题目"一行"）
    int slen = strlen(str);
    for (int i = 0; i < slen; i++) {
        if (str[i] == '@')         // 结束符
            break;
        else if (str[i] == '(')    // 左括号入栈
            stk.push(str[i]);
        else if (str[i] == ')') {  // 右括号：配对
            if (stk.top() == '(')
                stk.pop();
            else if (stk.empty()) {
                cout << "NO" << endl;
                return 0;
            }
        }
    }
    if (!stk.empty())
        cout << "NO" << endl;
    else
        cout << "YES";
    return 0;
}
```

**运行验证**（已用 g++ 实测）：

```text
输入 2*(x+y)/(1-x)@  → 输出 YES
输入 ()@             → 输出 YES
输入 (())@           → 输出 YES
输入 )@              → 无输出（原代码缺陷，见下）
```

**⚠️ 原代码的两处缺陷（必看）**：

1. **判空顺序错误**：`if (stk.top() == '(') ... else if (stk.empty())` —— 遇到 ')' 时**先调用了 top()**，此时若栈为空（如输入 `)@`），top() 是未定义行为（实测会无输出/崩溃，正确应输出 NO）。**必须先判空再取 top()**。
2. **栈顶不是 '(' 时不处理**：`else if (stk.empty())` 分支只有在栈顶不是 '(' 且栈空时才触发——若栈非空但栈顶不是 '('（本题只有 '(' 入栈，不会出现，但严谨写法应处理），逻辑会漏判。

**修正版代码（推荐）**：

```cpp
#include <iostream>
#include <stack>
#include <cstring>
using namespace std;

stack<char> stk;
char str[256];

int main() {
    cin >> str;
    for (int i = 0; str[i] != '@'; i++) {   // 遇@结束
        if (str[i] == '(') {
            stk.push(str[i]);
        }
        else if (str[i] == ')') {
            if (stk.empty()) {              // 先判空！
                cout << "NO" << endl;
                return 0;
            }
            stk.pop();                      // 栈顶必然是'('，直接配对
        }
    }
    cout << (stk.empty() ? "YES" : "NO") << endl;   // 栈空=全配对
    return 0;
}
```

**验证**（修正版）：`)@` → NO；`(())@` → YES；`2*(x+y)/(1-x)@` → YES；`(()))@` → NO。

**注意事项**：
1. 右括号的处理顺序是铁律：**先 empty() 后 top()**。
2. 栈最后非空说明有左括号没配对（如 `(( )@`）→ NO。
3. 输出格式：YES/NO（大小写敏感，原代码 YES 没换行、NO 有换行——修正版统一加 endl）。

**人话总结**：左括号入栈右括号弹，先判空再取顶，栈空 YES。

### 7.18 知识点总结页（P169）

教材 P169 汇总了本章 11 个知识点及掌握程度：STL概述（了解）、STL基本组成（熟悉）、string/vector/stack/queue/deque/list/set·multiset/map·multimap/STL常用算法（重点）——即本笔记 1-7 章的全部内容。

### 7.19 下节课预告（P171）

下节课内容：**文件操作**（文件读写流），为 STL 章节之后的内容。

### 本章人话总结

1. 排序四件套：sort（排）、random_shuffle（洗）、merge（并）、reverse（反）。
2. 拷贝替换：copy 先 resize、replace 按值、replace_if 按谓词、swap 互换。
3. accumulate/fill 在 `<numeric>`，别的算法都在 `<algorithm>`。
4. 集合三兄弟：有序+resize+用返回迭代器，容量口诀 min/和/max。
5. 约瑟夫（queue 模拟）与括号匹配（stack 模拟）是"容器适配器"的经典应用，务必亲手写一遍。

---

## 第8章 深度补充：代码全景、易混对比与迭代器专题

### 8.1 配套代码全景索引（全部 test 函数逐一说明）

用户配套代码共 4 个版本（v1-v4 mycode.cpp）+ 表达式括号匹配.cpp，覆盖教材全部知识点。下表按文件分组，标注每个 test 函数演示的功能、对应教材页、被注释代码段的原因。

#### 8.1.1 v1_mycode.cpp（string + vector，教材 P6-P39）

| test | 演示功能 | 教材页 | 被注释代码段及原因 |
|---|---|---|---|
| test01 | string 八种初始化 | P7-8 | 无 |
| test02 | cin 输入（遇空格停） | P9 | 无 |
| test03 | getline 读整行 | P9 | 无 |
| test04 | string 比较（<） | P10 | 无 |
| test05 | string 连接（+） | P11 | `string s4 = "xiaoming" + "china"` 被注释：两个字面值不能 +，编译错误（错误示范） |
| test06 | string 三种遍历 | P12-13 | 无 |
| test07 | string 子串构造 | P14 | `s3(s1,8)`、`s8(s1,6,2)` 被注释：pos>size() 未定义行为（错误示范） |
| test08 | substr 子串提取 | P15 | `s4 = s.substr(10)`、`s6 = s.substr(6,2)` 被注释：pos 越界抛 out_of_range（错误示范） |
| test09 | insert 四种插入 | P16 | 无 |
| test10 | erase 四种删除 | P17 | 无 |
| test11 | append 追加 | P18 | 无 |
| test12 | replace 五连替换 | P19 | 无 |
| test13 | 去除标点练习（ispunct） | P21-22 | 无 |
| test14 | vector 三种类型列表初始化 | P25 | 无 |
| test15 | vector 构造函数初始化 | P26 | 无 |
| test16 | vector 遍历与访问 | P27-28 | 无 |
| test17 | vector 四种插入 | P29-30 | 无 |
| test18 | vector 三种删除 | P31-32 | `v.clear()` 被注释：演示完 erase/pop_back 后若再 clear 就没元素可打印了（按演示步骤设计） |
| test19 | size/capacity/max_size | P34-35 | 无 |
| test20 | assign/swap | P36-37 | `v.assign(10,22)` 和 `v2.assign(v1.begin(),v1.end())` 被注释：本节重点是 swap，assign 放在注释里作对照 |
| test21 | 随机数找最大最小 | P38-39 | 无 |

#### 8.1.2 v2_mycode.cpp（stack/queue/deque/list，教材 P40-P89）

| test | 演示功能 | 教材页 | 被注释代码段及原因 |
|---|---|---|---|
| test01 | stack 三种构造 | P41 | 无 |
| test02 | stack push/pop/top/size/empty | P42-45 | 底部 `stack<char> s1; s1.push('a'); s1.top();` 注释：空栈/普通 top 演示（提示 top 只取不删） |
| test03 | 十进制转二进制（练习） | P46-47 | 无 |
| test04 | 十进制转十六进制（扩展） | P46-47 | 无（switch 0-15 → '0'-'F' 映射） |
| test05 | queue 三种构造 | P50 | 无 |
| test06 | queue 六个函数 | P51-52 | 无 |
| test07 | 扑克牌（练习） | P53-54 | 无 |
| test08 | deque 五种构造 | P57-58 | 无 |
| test09 | deque 四种添加 | P59-60 | 无 |
| test10 | deque 五种删除 | P61-62 | 无 |
| test11 | deque 访问 []/at/front/back | P63-64 | 无（at(40) 用 try-catch 捕获越界异常） |
| test12 | deque size/max_size/resize/empty | P65-66 | 无 |
| test13 | deque assign/swap | P67-68 | 无 |
| test14 | VIP 排队（练习） | P69-70 | 无 |
| test15 | list 五种构造 | P73 | 无 |
| test16 | list 头尾插删 | P77-78 | 无 |
| test17 | list insert 三兄弟 | P79-80 | 无 |
| test18 | list erase 两兄弟 | P81 | 无（演示 list 迭代器只能 -- 不能 -2） |
| test19 | list sort/reverse | P82-84 | 无 |
| test20 | Person 自定义排序（练习） | P87-89 | 无 |

#### 8.1.3 v3_mycode.cpp（set/map，教材 P90-P117）

| test | 演示功能 | 教材页 | 被注释代码段及原因 |
|---|---|---|---|
| test01 | set 构造/拷贝/赋值 | P91-92 | 无 |
| test02 | set 插入删除 | P93-94 | 无 |
| test03 | set 大小交换 | P95-96 | 无 |
| test04 | set 查找统计 | P97-98 | 无（重复 insert 3 验证 count=1） |
| test05 | multiset 三种构造 | P99 | 无 |
| test06 | multiset 插入 | P99 | `ms.erase(ms.begin())`、区间删、`ms.erase(5)`、`ms.clear()` 整段被注释：删除四兄弟的对照演示（每个若解开都会减少元素） |
| test07 | multiset 大小交换 | P99 | 无（printMulset 正序 + printMulset2 反向） |
| test08 | multiset 查找统计/lower_bound/upper_bound | P99-100 | `cout << *ms.find(50)` 被注释：50 不存在，find 返回 end()，解引用 end() 是未定义行为（错误示范） |
| test09 | pair 三种声明 | P104 | 无 |
| test10 | pair 数据访问 | P105 | 无 |
| test11 | make_pair | P106 | 无（演示 double→int 截断） |
| test12 | map 构造/拷贝/赋值 | P107-108 | 无 |
| test13 | map 大小交换 | P109-111 | 无 |
| test14 | map 四种插入+删除 | P112-113 | 无 |
| test15 | map 查找统计 | P114-115 | 无 |
| test16 | multimap 构造 | P116 | 无 |
| test17 | multimap 插入删除 | P116-117 | 无 |
| test18 | multimap 大小（含小笔误） | P116 | ⚠️ 代码笔误：打印"交换后"前漏调 `m.swap(m2)`，两次输出相同——正确应先 swap 再打印 |
| test19 | multimap 查找/count/equal_range | P116-117 | 无 |

#### 8.1.4 v4_mycode.cpp（算法，教材 P118-P171）

| test | 演示功能 | 教材页 | 被注释代码段及原因 |
|---|---|---|---|
| test01 | for_each 普通函数 vs 仿函数 | P120-121 | 无 |
| test02 | transform 搬运 | P122-123 | 无（vTarget.resize 先开空间） |
| test03 | find 按值查找 | P125-126 | 无 |
| test04 | find_if 按条件查找 | P127-128 | 无 |
| test05 | adjacent_find 相邻重复 | P129-130 | 无 |
| test06 | binary_search 二分查找 | P131-132 | 无 |
| test07 | count 统计 | P133-134 | 无 |
| test08 | count_if 按条件统计 | P135-136 | 无 |
| test09 | sort 升序/降序 | P138-139 | 无 |
| test10 | random_shuffle 洗牌 | P140-141 | 无 |
| test11 | merge 合并 | P142-143 | 无 |
| test12 | reverse 反转 | P144-145 | 无 |
| test13 | copy 拷贝 | P147-148 | 无 |
| test130 | copy_if 条件拷贝（扩展） | P148 扩展 | 无（Greater130 v>2 → 3 45 6 7 89） |
| test14 | replace 替换 | P149-150 | 无 |
| test15 | replace_if 条件替换 | P151-152 | 无 |
| test16 | swap 交换 | P153-154 | 无 |
| test17 | accumulate 求和 | P156-157 | 无 |
| test18 | fill 填充 | P158-159 | `v.resize(10)` 被注释：若保留则 fill 填满 10 个元素；注释后容器保持 {1,2,3,4,5} 填 5 个 |
| test19 | set_intersection 交集 | P161-162 | 两行 for_each 打印被注释：演示"返回尾迭代器"的用法（若解开：3 5 6 8） |
| test20 | set_union 并集 | P163-164 | 无 |
| test21 | set_difference 差集 | P165-166 | ⚠️ 代码笔误：第二段 `for_each(v3.begin(), pos1, ...)` 应为 `pos2`（实际会重复打印 v1-v2 的 1 3） |
| test22 | 约瑟夫问题（练习） | P167-168 | 无 |

#### 8.1.5 表达式括号匹配.cpp（教材 P170 作业）

完整讲解见 7.17 节。两处缺陷：①`')'` 分支先 top() 后 empty()（空栈 UB）；②栈顶非 '(' 时无处理分支。修正版代码见 7.17。

### 8.2 六组易混对比

#### 8.2.1 vector vs deque vs list（底层结构与复杂度）

| 维度 | vector | deque | list |
|---|---|---|---|
| 底层结构 | 连续内存数组 | 分段连续缓冲区+中控器 | 双向链表 |
| 随机访问（下标） | O(1) 支持 | O(1) 支持 | ❌ 不支持 |
| 头部插入/删除 | O(n) 极慢 | O(1) 快 | O(1) 快 |
| 尾部插入/删除 | O(1) 摊销 | O(1) 快 | O(1) 快 |
| 中间插入/删除 | O(n)（搬移） | O(n)（搬移） | O(1)（只要迭代器） |
| 迭代器类型 | 随机访问 | 随机访问 | 双向（只能++/--） |
| 内存开销 | 最小 | 中 | 最大（每节点双指针） |
| 适用场景 | 尾部增删+下标访问 | 头尾都要增删+下标 | 频繁中间插删 |

**一句话选择**：下标访问多→vector；头尾都要进出→deque；中间插删频繁→list。

#### 8.2.2 set vs multiset

| 特性 | set | multiset |
|---|---|---|
| 重复元素 | 不允许（insert 重复被忽略） | 允许 |
| count(key) | 0 或 1 | 0~n |
| insert 返回值 | pair<iterator,bool>（bool 表示是否插入成功） | 迭代器（总成功） |
| find | 唯一匹配 | 第一个匹配 |

#### 8.2.3 map vs multimap

| 特性 | map | multimap |
|---|---|---|
| 重复 key | 不允许 | 允许 |
| m[key] / at() | ✅ 支持（key 不存在会创建） | ❌ 不支持 |
| count(key) | 0 或 1 | 0~n |
| 一 key 多 value 遍历 | 不适用 | find+count 或 equal_range |

#### 8.2.4 find vs find_if

| 特性 | find | find_if |
|---|---|---|
| 查找依据 | 值相等（==） | 谓词条件（自定义） |
| 语法 | `find(beg, end, value)` | `find_if(beg, end, _Pred)` |
| 返回 | 第一个匹配迭代器 / end() | 第一个满足条件迭代器 / end() |
| 场景 | 找固定值 | 找"第一个>50的"等条件 |

#### 8.2.5 set_intersection vs set_union vs set_difference

| 特性 | set_intersection | set_union | set_difference |
|---|---|---|---|
| 结果 | 交集 | 并集（去重） | v1 有 v2 无 |
| 目标容器预留 | min(s1,s2) | s1+s2 | max(s1,s2) |
| 前提 | 两容器有序 | 两容器有序 | 两容器有序 |
| 方向 | 对称 | 对称 | **不对称**（v1-v2≠v2-v1） |

#### 8.2.6 replace vs replace_if

| 特性 | replace | replace_if |
|---|---|---|
| 匹配 | 值相等（==） | 谓词条件 |
| 参数 | oldvalue, newvalue | _Pred, newvalue |
| 场景 | 把 1 换成 1111 | 把 >20 的换成 9999 |

### 8.3 迭代器专题

#### 8.3.1 什么是迭代器？为什么需要它？

**是什么**：迭代器是访问容器中元素的"通用指针"，提供 `*`（解引用）、`++`（前进）、`==/!=`（比较）等操作。

**为什么**：STL 的核心设计是"数据结构与算法分离"（呼应教材 P4）：算法只认迭代器，不认具体容器。同一份 `sort` 代码能作用于 vector 也能作用于数组，靠的就是迭代器这个"中间层"。

**怎么用**：

```cpp
vector<int> v = {1,2,3,4,5};
for (auto it = v.begin(); it != v.end(); ++it) {
    cout << *it << " ";   // 解引用取元素
}
```

**注意事项**：
1. 迭代器不是指针，但行为像指针；C++ 的指针本身就是一种迭代器。
2. 迭代器失效：vector 插入/删除后旧迭代器可能失效（扩容搬移、元素前移）。

**人话总结**：迭代器是算法和容器之间的万能插头。

#### 8.3.2 begin()/end()/rbegin()/rend() 的区别

| 函数 | 指向 | 遍历方向 |
|---|---|---|
| begin() | 第一个元素 | 正向起点 |
| end() | 最后一个元素的**下一个位置** | 正向终点（不可解引用） |
| rbegin() | 最后一个元素 | 反向起点 |
| rend() | 第一个元素的**前一个位置** | 反向终点（不可解引用） |

```cpp
vector<int> v = {1,2,3};
for (auto it = v.rbegin(); it != v.rend(); ++it) {
    cout << *it << " ";   // 3 2 1
}
```

**注意事项**：区间一律左闭右开 `[begin, end)`——这是 STL 所有算法和循环的统一约定。

**人话总结**：end 是"最后一个的下一个"，rbegin 反着走。

#### 8.3.3 迭代器的五种类别

| 类别 | 支持操作 | 典型容器 |
|---|---|---|
| 输入迭代器 | 读、++、==/!= | istream_iterator |
| 输出迭代器 | 写、++ | ostream_iterator |
| 前向迭代器 | 输入+输出，可多遍 | forward_list |
| 双向迭代器 | 前向 + -- | list、set、multiset、map、multimap |
| 随机访问迭代器 | 双向 + it+n、it-n、it1-it2、it[i]、it1<it2 | string、vector、deque、数组 |

**关键推论**：
- **std::sort 需要随机访问迭代器** → 不能用于 list（list 只能用成员函数 sort）。
- list/set/map 的迭代器只能 `++`/`--`，不能 `it + 2`（配套代码 test18 用两次 `--` 移动就是为此）。

**人话总结**：迭代器分五级，随机访问最全能。

#### 8.3.4 迭代器失效问题（新手必踩）

**是什么**：容器结构变化（插入/删除）后，已保存的迭代器可能指向无效位置。

**典型错误**（删除偶数时直接 erase 不更新迭代器）：

```cpp
// ❌ 错误：erase 后 it 失效，it++ 是未定义行为
for (auto it = v.begin(); it != v.end(); it++) {
    if (*it % 2 == 0) v.erase(it);
}

// ✅ 正确：用 erase 的返回值更新迭代器
for (auto it = v.begin(); it != v.end(); ) {
    if (*it % 2 == 0) it = v.erase(it);   // erase 返回下一个有效迭代器
    else ++it;
}
```

**注意事项**：
1. vector/deque：插入删除会使**之后位置**的迭代器全部失效（vector 扩容时全部失效）。
2. list/set/map：插入不影响其他迭代器；erase 只失效被删位置的迭代器。
3. 边遍历边删除：统一用 `it = container.erase(it)` 模式。

**人话总结**：删元素要接住 erase 的返回值，别让迭代器悬空。

### 8.4 易错点速查卡

| # | 易错点 | 正确姿势 |
|---|---|---|
| 1 | 空栈/空队列 top()/front()/pop() | 先判 empty() 再操作 |
| 2 | vector 下标越界不报错 | 用 at() 或先判 size() |
| 3 | size vs capacity 混淆 | size=元素数，capacity=容量 |
| 4 | end() 解引用 | end() 是哨兵，不可解引用 |
| 5 | 两个字面值字符串用 + | 至少一边是 string 对象 |
| 6 | substr/子串构造 pos 越界 | pos>size() 抛异常/UB，先检查 |
| 7 | erase 后迭代器失效 | it = v.erase(it) |
| 8 | list 用 std::sort | 用成员函数 l.sort() |
| 9 | list 迭代器 it+n | 只支持 ++/-- |
| 10 | binary_search 用无序容器 | 必须有序，否则结果未定义 |
| 11 | transform/merge/copy 目标容器没 resize | 目标先 resize 再操作 |
| 12 | accumulate/fill 忘包含 <numeric> | 这两个在 numeric 不在 algorithm |
| 13 | set 重复 insert 以为会成功 | set 去重，multiset 才行 |
| 14 | map 用 m[key] 查询 | 不存在会创建{key,0}，查询用 find |
| 15 | multimap 用 m[key] | multimap 没有 [] 和 at() |
| 16 | 集合算法忘有序/忘 resize | 有序+resize+用返回迭代器 |
| 17 | random_shuffle 忘 srand | 否则每次结果一样 |
| 18 | replace_if 谓词写错方向 | >x 用 v>x，==x 用 v==x |
| 19 | map 遍历顺序 | 永远按 key 升序，别假设插入序 |
| 20 | vector 扩容搬移 | 大量插入前 reserve 预留 |

### 本章人话总结

1. 代码全景表：每个 test 对应教材哪页、注释为何——复习时按表回查。
2. 六组对比：容器选型看"随机访问/头尾/中间"三问；算法对比看"按值还是按条件"。
3. 迭代器：五类别决定容器能用哪些算法；失效问题决定删除写法。
4. 20 条速查卡覆盖了初学者 80% 的坑，考前过一遍。

---

## 第9章 全章知识体系回顾与随身口诀

### 9.1 STL 全章知识体系树

```text
STL（标准模板库）
├── 三大组件
│   ├── 容器 Container（存数据）
│   ├── 迭代器 Iterator（访数据）
│   └── 算法 Algorithm（改数据）
├── 序列式容器（按顺序存，值不排序）
│   ├── string ── 动态字符串（安全、优先用）
│   ├── vector ── 动态数组（尾部增删+随机访问）
│   ├── deque  ── 双端队列（头尾增删+随机访问）
│   ├── list   ── 双向链表（任意位置插删快，无下标）
│   ├── stack  ── 栈（LIFO，适配器，底层deque）
│   └── queue  ── 队列（FIFO，适配器，底层deque）
├── 关联式容器（自动按 key/值排序，红黑树）
│   ├── set       ── 集合（去重+排序）
│   ├── multiset  ── 可重复集合
│   ├── map       ── 键值对字典（key→value）
│   ├── multimap  ── 一key多值字典
│   └── pair      ── 对组（map的元素类型）
├── 迭代器
│   ├── begin/end/rbegin/rend（左闭右开）
│   ├── 输入/输出/前向/双向/随机访问 五类别
│   └── 失效问题（erase返回值接住）
├── 算法（<algorithm> / <numeric> / <functional>）
│   ├── 遍历：for_each、transform
│   ├── 查找：find、find_if、adjacent_find、binary_search、count、count_if
│   ├── 排序：sort、random_shuffle、merge、reverse
│   ├── 拷贝替换：copy、replace、replace_if、swap
│   ├── 算术生成：accumulate、fill（<numeric>）
│   └── 集合：set_intersection、set_union、set_difference
└── 经典练习（容器+算法的实战）
    ├── 去除标点（string+遍历+ispunct）
    ├── 随机数最值（vector）
    ├── 十进制转二进制（stack）
    ├── 扑克牌（queue）
    ├── VIP排队（deque）
    ├── Person排序（list+自定义比较）
    ├── 约瑟夫问题（queue模拟）
    └── 括号匹配（stack模拟）
```

### 9.2 核心速查表

#### 9.2.1 容器速查表

| 容器 | 头文件 | 构造示例 | 增 | 删 | 取 | 大小/其他 | 最易错 |
|---|---|---|---|---|---|---|---|
| string | `<string>` | `string s(10,'a')` | `+`/append/insert | erase | `s[i]`/at/substr | size()/empty() | pos 越界、字面值+字面值 |
| vector | `<vector>` | `vector<int> v(10,2)` | push_back/insert | pop_back/erase/clear | `v[i]`/at/front/back | size()/capacity/max_size | 下标越界、迭代器失效 |
| stack | `<stack>` | `stack<int> s` | push | pop | top | size()/empty() | 空栈 top/pop、top不删 |
| queue | `<queue>` | `queue<int> q` | push(队尾) | pop(队头) | front/back | size()/empty() | 空队 front/pop |
| deque | `<deque>` | `deque<int> d(10,1)` | push_front/back/insert | pop_front/back/erase/clear | `d[i]`/at/front/back | size()/resize/empty/swap | 无capacity |
| list | `<list>` | `list<int> l(5,20)` | push_front/back/insert | pop_front/back/erase/remove | front/back（无[]！） | size()/empty/sort/reverse | 无下标、不能std::sort |
| set | `<set>` | `set<int> s` | insert | erase/clear | find（无[]） | size()/empty/count/swap | 重复insert无效、count只0/1 |
| multiset | `<set>` | `multiset<int> ms` | insert（总成功） | erase/clear | find（第一个） | count可>1 | find返回第一个 |
| map | `<map>` | `map<int,int> m` | insert/m[key]=v | erase(key)/clear | m[key]/find/at | size()/empty/count/swap | m[key]会偷建、按key排序 |
| multimap | `<map>` | `multimap<int,int> mm` | insert | erase | find+count遍历 | count可>1 | 无[]和at |

#### 9.2.2 算法速查表

| 算法 | 头文件 | 语法 | 要点 |
|---|---|---|---|
| for_each | `<algorithm>` | `for_each(beg,end,func)` | 仿函数要加()：func() |
| transform | `<algorithm>` | `transform(b1,e1,b2,func)` | 目标先 resize |
| find | `<algorithm>` | `find(beg,end,val)` | 找不到返回 end() |
| find_if | `<algorithm>` | `find_if(beg,end,pred)` | 谓词返回 bool |
| adjacent_find | `<algorithm>` | `adjacent_find(beg,end)` | 相邻重复 |
| binary_search | `<algorithm>` | `binary_search(beg,end,val)` | 必须有序，返回 bool |
| count / count_if | `<algorithm>` | `count(beg,end,val)` / `count_if(beg,end,pred)` | 返回个数 |
| sort | `<algorithm>` | `sort(beg,end)` / `sort(beg,end,greater<int>())` | 需随机访问迭代器 |
| random_shuffle | `<algorithm>` | `random_shuffle(beg,end)` | 先 srand |
| merge | `<algorithm>` | `merge(b1,e1,b2,e2,dest)` | 有序+目标resize |
| reverse | `<algorithm>` | `reverse(beg,end)` | 原地反转 |
| copy / copy_if | `<algorithm>` | `copy(beg,end,dest)` | 目标先 resize |
| replace / replace_if | `<algorithm>` | `replace(beg,end,old,new)` / `replace_if(beg,end,pred,new)` | 按值/按条件 |
| swap | `<algorithm>` | `swap(c1,c2)` | 同类型容器 |
| accumulate | `<numeric>` | `accumulate(beg,end,init)` | 初始值要写 |
| fill | `<numeric>` | `fill(beg,end,val)` | 容器要有元素 |
| set_intersection/union/difference | `<algorithm>` | 见 7.13-7.15 | 有序+resize+返回迭代器 |

### 9.3 随身速记口诀

**口诀一（容器选择）**：
> 下标访问用 vector，头尾进出用 deque，中间插删用 list，先进后出栈、先进先出队，去重排序 set，键值对应 map。

白话解释：先问"要不要下标访问、插删在哪头"——尾部增删+下标=vector；头尾都要=deque；中间频繁= list；LIFO=stack、FIFO=queue；自动排序去重=set；key 查 value=map。

**口诀二（迭代器）**：
> 左闭右开记心间，end 永远不碰面；删完元素接返回值，先判空再取头尾。

白话解释：区间 `[begin, end)` 左闭右开，end() 不可解引用；erase 后要接返回值（it = erase(it)）；空容器取 top/front 前先判 empty。

**口诀三（算法）**：
> 排序查找在 algorithm，求和填充找 numeric；有序、resize、返回尾迭代器——集合算法三件套。

白话解释：绝大多数算法在 `<algorithm>`，accumulate/fill 在 `<numeric>`；集合算法（交并差）必须有序、目标容器先 resize、用返回值遍历结果。

### 本章人话总结

1. 树状图把 11 个知识点织成一张网：组件→容器→迭代器→算法→练习。
2. 两张速查表覆盖全部 API：容器看"增删取大小"，算法看"头文件+要点"。
3. 三句口诀是考前的最后一遍：选型、迭代器安全、算法三件套。

---

## 第10章 随堂测验（4题·难度递进）

> 说明：先独立完成，把你的答案贴在对话里发给教练。教练会逐题批改、指出错误原因并给出标准答案。

### 第1题【★ 概念题】填空/判断（8小问）

判断正误（对的打√，错的打×并说明原因）：

1. STL 的三大组件是容器、迭代器、算法。 （ ）
2. vector 和 deque 都支持随机访问（下标）。 （ ）
3. stack 和 queue 都允许遍历所有元素。 （ ）
4. set 容器插入重复元素时不会报错，而是被忽略。 （ ）
5. map 中的元素是按插入顺序存储的。 （ ）
6. binary_search 可以在无序容器上使用。 （ ）
7. accumulate 算法所在的头文件是 `<algorithm>`。 （ ）
8. list 支持 `it + 2` 这样的迭代器运算。 （ ）

### 第2题【★★ 容器操作】写出代码片段

有一个 `vector<int> v = {1, 2, 3, 4, 5};`，请写出代码完成：

1. 在末尾追加一个元素 6；
2. 删除第 2 个元素（值为 2）；
3. 在头部插入元素 0（提示：vector 没有 push_front，怎么办？）；
4. 输出当前 size() 和 capacity()；
5. 判断容器是否为空。

### 第3题【★★★ 算法应用】写出代码及预期输出

给定 `vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};`，用 STL 算法完成以下任务，写出每段代码和它的输出：

1. 用 sort 升序排序后输出；
2. 用 sort + greater<int>() 降序排序后输出；
3. 用 find_if + 仿函数找第一个大于 5 的元素（提示：仿函数类要重载 operator()）；
4. 用 count_if + 仿函数统计奇数的个数；
5. 用 reverse 反转后输出。

### 第4题【★★★★ 综合编程】完整程序

**题目：学生成绩统计**

用 `map<string, int>` 存储 4 名学生的姓名和成绩：

| 姓名 | 成绩 |
|---|---|
| 张三 | 85 |
| 李四 | 92 |
| 王五 | 85 |
| 赵六 | 78 |

要求写一个完整可编译的程序，完成：

1. 用 map 存储上述数据（至少使用两种插入方式，其中一种用 `m[key] = value`）；
2. 用 set 收集所有**不重复的成绩**并输出（应输出 78 85 92）；
3. 用 accumulate 求出总成绩并输出平均值（保留一位小数）；
4. 用 count 统计成绩为 85 的学生人数；
5. 找出最高分学生（遍历 map 比较 value），输出姓名和成绩；
6. 把学生按成绩降序输出（提示：把 map 的键值对放入 vector<pair<string,int>>，用 sort + 自定义比较函数）。

输出格式参考：

```text
不重复成绩: 78 85 92
总成绩: 340 平均分: 85.0
85分人数: 2
最高分: 李四 92
成绩降序: 李四(92) 张三(85) 王五(85) 赵六(78)
```

> 提示：自定义比较函数比较 pair 的 second 时，注意"分数相同按姓名升序"的次规则，严格弱序要处理好相等情况。

### 批改流程说明

把 4 题答案贴在对话中后，教练将：
1. 逐题核对答案是否正确；
2. 指出错误之处并解释原因（重点看：容器的选择、迭代器使用、算法参数、边界条件）；
3. 给出标准答案供参考；
4. 如果第 3、4 题有代码，会检查编译与运行结果。

---

