# C++ 常用新特性学习笔记（C++11 / C++17 / C++20）

> **前置章节**：第23章 STL、第24章 文件操作（C++ 基础篇）
> **预计学习时间**：8 小时
> **编译器要求**：Visual Studio 2019 及以上，需设置对应 C++ 语言标准（/std:c++11、/std:c++17、/std:c++20）

---

## 第一部分：C++11 核心语言特性

---

### 1. 自动类型推导 auto【重点】（P2-P8）

#### ① 是什么
`auto` 是一个类型占位符，通知编译器根据初始化表达式自动推断变量的真实类型。生活比喻：就像快递单上写"内件详见实物"，快递员（编译器）打开包裹才知道里面具体是什么。

#### ② 为什么
在没有 `auto` 之前，STL 迭代器声明极其冗长：`vector<int>::iterator it = vc.begin();`，类型名又长又容易拼错。`auto` 让编译器替你写类型，代码更简洁、更安全。

旧写法 vs 新写法：
```cpp
// 旧写法（C++98）：迭代器类型冗长
for (vector<int>::iterator it = vc.begin(); it != vc.end(); it++) {
    cout << *it << " ";
}

// 新写法（C++11）：auto 自动推导
for (auto it = vc.begin(); it != vc.end(); it++) { // auto 推导为 vector<int>::iterator
    cout << *it << " ";
}
```

#### ③ 怎么用
```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> vc = {1, 2, 3, 4, 5, 6};
    // auto 推导为 vector<int>::iterator
    for (auto it = vc.begin(); it != vc.end(); it++) {
        cout << *it << " "; // 输出：1 2 3 4 5 6
    }

    // auto 与 const 的规则演示
    int x = 0;
    const auto n = x;       // n 是 const int，auto 推导为 int
    auto f = n;             // f 是 int（非引用时丢弃 const）
    const auto& r1 = x;     // r1 是 const int&，auto 推导为 int
    auto& r2 = r1;          // r2 是 const int&（引用时保留 const）

    // auto 混合使用
    auto* pt1 = &x;         // pt1 为 int*，auto 推导为 int
    auto pt2 = &x;          // pt2 为 int*，auto 推导为 int*
    auto& r3 = x;           // r3 为 int&，auto 推导为 int

    return 0;
}
```

#### ④ 注意事项与常见错误

| 规则 | 说明 |
|------|------|
| 非引用推导 | auto 丢弃 const/volatile 顶层限定符 |
| 引用推导 | auto 保留 const/volatile 限定符 |
| 函数参数 | C++11 不允许（C++14 起支持返回值推导） |
| 类非静态成员 | 不允许 |
| 模板参数 | 不允许，如 `Student<auto>` 编译报错 |
| 数组推导 | 不允许，如 `auto arr[10] = ...` 编译报错 |

错误示范：
```cpp
const int c = 10;
auto a = c;   // a 是 int，不是 const int！修改 a 不影响 c，但语义可能误导
a = 20;       // 合法，但你可能以为 a 也是 const

// 正确写法：需要保留 const 时用引用
const auto& a2 = c; // a2 是 const int&
```

> **人话总结**：auto 像脱衣服，非引用脱掉 const，引用则穿着。

---

### 2. decltype 类型查询【重点】（P8-P12）

#### ① 是什么
`decltype` 是一个运算符，用于查询表达式的类型但不实际计算该表达式的值。生活比喻：就像查看菜谱上的菜品名称（类型），但不需要真的做这道菜（不求值）。

#### ② 为什么
`auto` 只能从初始化表达式推导变量类型，无法处理"我需要知道某个表达式的类型但不想执行它"的场景。在泛型编程中，函数返回值类型可能依赖参数运算结果，`decltype` 配合尾置返回类型解决了这个问题。

#### ③ 怎么用
```cpp
#include <iostream>
using namespace std;

// 尾置返回类型：解决泛型返回值推导问题
template <typename T, typename U>
auto add(T t, U u) -> decltype(t + u) { // 用 decltype 推导 t+u 的类型作为返回值类型
    return t + u;
}

int main() {
    int a = 1;
    float b = 2.0f;
    auto c = add(a, b);      // c 的类型由 decltype(a+b) 推导为 float
    cout << c << endl;        // 输出：3

    // decltype 不计算表达式
    auto num1 = 100;
    auto num2 = 200;
    decltype(num1 + num2) num3; // num3 类型为 int，num1+num2 不会被实际计算
    cout << typeid(num3).name() << endl; // 输出：int 对应的类型名

    return 0;
}
```

#### ④ 注意事项
- `decltype` 括号内可以是任意表达式，包括函数调用、成员访问等
- C++14 起可以直接写 `auto add(T t, U u) { return t+u; }` 省略尾置返回类型
- 错误示范：`decltype(t+u) add(T t, U u)` 会报错，因为返回值位置参数尚未声明

> **人话总结**：decltype 只看不算，专治泛型返回值难题。

---

### 3. 右值引用与移动语义【重点】（P12-P18）

#### ① 是什么
右值引用 `&&` 是一种只能绑定到右值（临时对象）的引用类型；移动语义利用右值引用将资源从一个对象"转移"而非"拷贝"到另一个对象。生活比喻：移动语义就像搬家——把家具从旧房子搬到新房子，而不是买一套全新的家具。

#### ② 为什么
当函数返回临时对象或传递大对象时，传统拷贝构造会触发深拷贝，造成不必要的内存分配和释放。移动语义通过"窃取"临时对象的资源来避免这些开销，大幅提升性能。

左值 vs 右值判断标准：
- **左值**：能取地址（`&obj`）、有名字、可放在赋值号左边
- **右值**：不能取地址、没有名字（临时量）、只能放在赋值号右边

#### ③ 怎么用
```cpp
#include <iostream>
#include <cstring>
using namespace std;

class MyString {
private:
    char* data;
    size_t len;
public:
    // 普通构造函数
    MyString(const char* s) : len(strlen(s)) {
        data = new char[len + 1];
        strcpy(data, s);
        cout << "普通构造: " << data << endl;
    }

    // 移动构造函数：参数必须是 &&，且不能是 const
    MyString(MyString&& str) noexcept {
        cout << "移动构造 from " << str.data << endl;
        len = str.len;
        data = str.data;      // 直接接管资源指针
        str.len = 0;
        str.data = nullptr;   // 必须置空，否则析构时会释放已转移的资源
    }

    ~MyString() {
        delete[] data;
        cout << "析构" << endl;
    }
};

int main() {
    MyString s1("hello");           // 普通构造
    MyString s2(std::move(s1));     // std::move 将左值 s1 转为右值引用，触发移动构造
    // s1 此时 data==nullptr, len==0，处于"有效但未指定"状态
    return 0;
}
// 输出：
// 普通构造: hello
// 移动构造 from hello
// 析构
// 析构
```

#### ④ 注意事项
- `std::move` 只是类型转换，不移动任何东西
- 被 move 后的对象仍可访问，但状态不确定（不是 NULL，只是资源被转走了）
- 移动构造的参数不能是 `const`，因为需要修改源对象
- 必须将源对象的资源标记置空，否则双重释放

错误示范：
```cpp
string s = "hello";
string s2 = std::move(s);
cout << s.length(); // 未定义行为！s 的内容已被移走
// 正确做法：move 后不再读取原对象，或仅对其赋值/析构
```

> **人话总结**：move 如搬家，搬走后旧房还在但东西没了。

---

### 4. 列表初始化【熟悉】（P18-P20）

#### ① 是什么
统一使用花括号 `{}` 初始化所有类型（内置类型、数组、STL容器、自定义类），可省略等号。生活比喻：就像一个万能收纳盒，不管装什么都用同一种方式打包。

#### ② 为什么
C++98 中不同类型的初始化语法不一致（数组用 `{}`，类用构造函数，vector 要 push_back），学习成本高且容易出错。C++11 统一了初始化语法。

#### ③ 怎么用
```cpp
#include <iostream>
#include <vector>
#include <map>
using namespace std;

class ClassNum {
public:
    ClassNum(int n1 = 0, int n2 = 0) : _x(n1), _y(n2) {}
    void printInfo() { cout << _x << "  " << _y << endl; }
private:
    int _x, _y;
};

int main() {
    int num1 = {100};     // 内置类型，带等号
    int num2{3};          // 内置类型，不带等号

    int arr1[5] = {1, 3, 4, 5, 6};
    int arr2[] = {4, 5, 6, 7, 8};

    vector<int> v{12, 2};                // STL 容器
    map<int, int> mp{{1, 2}, {3, 4}};   // map 嵌套初始化

    ClassNum p{1, 2};                    // 自定义类型
    p.printInfo();                        // 输出：1  2

    return 0;
}
```

#### ④ 注意事项
- `vector<int> v{10}` 表示包含一个元素 10，而 `vector<int> v(10)` 表示包含 10 个默认元素
- 列表初始化禁止窄化转换（如 `int x{3.14}` 编译报错）

> **人话总结**：花括号万能初始化，写法统一不出错。

---

### 5. 范围 for（For each）【熟悉】（P20-P21）

#### ① 是什么
基于范围的 for 循环，类似 Python 的 `for x in list` 语法，自动遍历容器中每个元素。生活比喻：就像传送带上的物品逐个经过你面前，不需要自己数第几个。

#### ② 为什么
传统 for 循环需要手动管理迭代器或下标，代码冗长且容易越界。范围 for 消除了这些隐患。

#### ③ 怎么用
```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v1 = {1, 2, 3, 4, 5, 6};
    for (auto i : v1) {        // auto 推导为 int，i 是值的拷贝
        cout << i << " ";      // 输出：1 2 3 4 5 6
    }
    cout << endl;

    // 如果需要修改元素，用引用
    for (auto& i : v1) {       // i 是 int&，修改会影响原容器
        i *= 2;
    }
    for (const auto& i : v1) { // 只读引用，避免拷贝开销
        cout << i << " ";      // 输出：2 4 6 8 10 12
    }
    return 0;
}
```

#### ④ 注意事项
- 遍历时不要修改容器大小（增删元素会导致迭代器失效）
- 大对象建议用 `const auto&` 避免不必要的拷贝

> **人话总结**：范围 for 像传送带，自动遍历不用管下标。

---

### 6. Lambda 表达式【重点】（P21-P30）

#### ① 是什么
Lambda 是一个匿名函数对象，编译器将其转换为仿函数类。生活比喻：就像便签纸上随手写的备忘指令，用完即弃，不需要专门创建一个正式的"说明书"（类）。

#### ② 为什么
在使用 STL 算法（如 sort、for_each）时，经常需要传入简单的比较或操作逻辑。手写仿函数类太繁琐，lambda 一行搞定。

#### ③ 怎么用

**语法拆解**：`[捕获列表](参数列表) mutable -> 返回类型 { 函数体 }`

| 部分 | 说明 | 是否可省略 |
|------|------|-----------|
| `[capture]` | 捕获上下文变量 | 不可省略（至少写 `[]`） |
| `(params)` | 参数列表 | 无参时可省略 |
| `mutable` | 取消 const 性质（允许修改值捕获的变量） | 可省略 |
| `-> ret` | 返回类型 | 可省略（编译器推导） |
| `{body}` | 函数体 | 不可省略 |

**捕获列表五种形式**：

| 写法 | 含义 |
|------|------|
| `[a, &b]` | a 值捕获，b 引用捕获 |
| `[this]` | 捕获当前对象的 this 指针 |
| `[&]` | 引用捕获所有自动变量 |
| `[=]` | 值捕获所有自动变量 |
| `[]` | 不捕获任何变量 |

完整示例：
```cpp
#include <iostream>
#include <algorithm>
using namespace std;

struct Goods {
    string name;
    double price;
};

int main() {
    // 基本 lambda
    int num1 = 3, num2 = 4;
    auto fun1 = [&num1, &num2](int num3) { num2 = num1 + num3; };
    fun1(100);
    cout << num1 << " " << num2 << endl; // 输出：3 103

    // 值捕获 + mutable
    int x = 10;
    auto add_x = [x](int a) mutable { x *= 2; return a + x; }; // x 是副本，mutable 允许修改副本
    cout << add_x(10) << endl; // 输出：30（x副本变为20，10+20=30）
    cout << x << endl;         // 输出：10（原始 x 不受影响）

    // lambda 替代仿函数排序
    Goods gds[] = {{"苹果", 5.1}, {"橙子", 9.2}, {"香蕉", 3.6}, {"菠萝", 9.6}};
    sort(gds, gds + 4, [](const Goods& l, const Goods& r) -> bool {
        return l.price < r.price; // 按价格升序
    });
    for (int i = 0; i < 4; i++) {
        cout << gds[i].name << "  " << gds[i].price << endl;
    }
    // 输出：香蕉 3.6 → 苹果 5.1 → 橙子 9.2 → 菠萝 9.6

    return 0;
}
```

**Lambda 等价仿函数对照**：
```cpp
// Lambda 写法
double rate = 0.6;
auto r2 = [=](double money, int year) -> double { return money * rate * year; };
cout << r2(20000, 2) << endl; // 输出：24000

// 等价仿函数写法
class Rate {
    double _rate;
public:
    Rate(double rate) : _rate(rate) {}
    double operator()(double money, int year) {
        return money * _rate * year;
    }
};
Rate r1(0.6);
cout << r1(20000, 2) << endl; // 输出：24000
```

#### ④ 注意事项
- 不同 lambda 即使代码相同也是不同类型，不能互相赋值（但可以拷贝构造同类型的副本）
- 值捕获的变量默认是 const，需要 `mutable` 才能修改
- Lambda 可以赋值给函数指针（仅限无捕获的 lambda）

> **人话总结**：Lambda 就是随手写的匿名小函数，替代仿函数神器。

---

### 7. 智能指针【重点】（P30-P42）

#### ① 是什么
智能指针是封装了指针的类模板，能在适当时机自动释放堆内存，防止内存泄漏。生活比喻：普通指针是你借的书忘了还就丢了；智能指针是图书馆自动催还系统，到期自动归还。

#### ② 为什么
手动 `new/delete` 容易忘记释放或在异常路径中泄漏。智能指针利用 RAII 机制，对象离开作用域时自动析构释放内存。

#### ③ 怎么用

**三种智能指针对比**：

| 特性 | shared_ptr | unique_ptr | weak_ptr |
|------|-----------|------------|----------|
| 所有权 | 共享 | 独占 | 无所有权 |
| 引用计数 | 有 | 无 | 不增加计数 |
| 可否复制 | 可以 | 不可以（只能移动） | 可以 |
| 典型场景 | 多对象共享资源 | 独占资源 | 打破循环引用 |
| 头文件 | `<memory>` | `<memory>` | `<memory>` |

**shared_ptr 所有权关系图（文字版）**：
```
shared_ptr<A> p1(new A())  ──→  [A对象] ← 引用计数 = 1
shared_ptr<A> p2(p1)       ──→  [A对象] ← 引用计数 = 2
p2.reset()                      [A对象] ← 引用计数 = 1
p1.reset()                      [A对象] ← 引用计数 = 0 → 自动delete
```

```cpp
#include <iostream>
#include <memory>
using namespace std;

// 自定义删除器（处理数组）
void deleteInt(int* p) { delete[] p; }

int main() {
    // === shared_ptr ===
    shared_ptr<int> p1;                       // 空指针，引用计数=0
    shared_ptr<int> p2(nullptr);              // 同上
    shared_ptr<int> p3(new int(5));           // 指向值为5的int
    shared_ptr<int> p4 = make_shared<int>(5); // 推荐方式，一次分配
    shared_ptr<int> p5(p4);                   // 拷贝，引用计数+1
    shared_ptr<int> p6(move(p5));             // 移动，p5变空

    // 自定义删除器处理数组
    shared_ptr<int> pa1(new int[3], default_delete<int[]>());
    shared_ptr<int> pa2(new int[3], deleteInt);
    shared_ptr<int> pa3(new int[2], [](int* p) { delete[] p; }); // lambda删除器

    // === unique_ptr ===
    unique_ptr<int> up1(new int(10));
    // unique_ptr<int> up2 = up1;            // 编译错误！不可复制
    unique_ptr<int> up2 = move(up1);          // 只能移动
    cout << *up2 << endl;                     // 输出：10

    return 0;
}
```

**weak_ptr 解决循环引用**：
```cpp
#include <iostream>
#include <memory>
using namespace std;

class CB;
class CA {
public:
    CA() { cout << "CA() called!" << endl; }
    ~CA() { cout << "~CA() called!" << endl; }
    void set_ptr(shared_ptr<CB>& ptr) { m_ptr_b = ptr; } // 改为 weak_ptr 即可解决
private:
    weak_ptr<CB> m_ptr_b;  // 用 weak_ptr 打破循环
};

class CB {
public:
    CB() { cout << "CB() called!" << endl; }
    ~CB() { cout << "~CB() called!" << endl; }
    void set_ptr(shared_ptr<CA>& ptr) { m_ptr_a = ptr; }
private:
    shared_ptr<CA> m_ptr_a;
};

int main() {
    shared_ptr<CA> ptr_a(new CA());
    shared_ptr<CB> ptr_b(new CB());
    ptr_a->set_ptr(ptr_b);
    ptr_b->set_ptr(ptr_a);
    return 0;
}
// 输出：CA() called! → CB() called! → ~CB() called! → ~CA() called!
// 两个对象都被正确析构
```

#### ④ 注意事项
- 优先使用 `make_shared` 创建 shared_ptr（单次内存分配，更高效）
- shared_ptr 默认删除器不支持数组，需用 `default_delete<int[]>()` 或自定义删除器
- weak_ptr 使用前需调用 `lock()` 获取 shared_ptr，检查对象是否仍存活
- 循环引用时引用计数永远不为 0，导致内存泄漏

> **人话总结**：智能指针自动管内存，shared共享unique独占weak旁观。

---

### 8. 可变参数模板【熟悉】（P42-P46）

#### ① 是什么
允许函数模板或类模板接受任意数量、任意类型的参数。生活比喻：就像一台万能榨汁机，无论你放几种水果进去都能处理。

#### ② 为什么
C++11 之前模板参数个数固定，要实现 printf 那样的可变参数功能只能用 C 风格的 `va_list`，类型不安全。可变参数模板提供了类型安全的可变参数方案。

#### ③ 怎么用
```cpp
#include <iostream>
using namespace std;

// 基本用法：sizeof... 获取参数个数
template<class... T>
void funcName(T... args) {
    cout << sizeof...(args) << endl; // sizeof... 是固定语法，计算参数包元素个数
    cout << sizeof...(T) << endl;
}

// 展开方式1：递归展开
void funcPrint() {
    cout << "递归终止" << endl;
}
template<class T, class... U>
void funcPrint(T first, U... others) {
    cout << "收到参数: " << first << endl;
    funcPrint(others...); // 注意 others 后面的 ... 不能省略
}

// 展开方式2：if constexpr（C++17）
template<class T, class... U>
void funcPrint2(T first, U... args) {
    cout << "收到参数: " << first << endl;
    if constexpr (sizeof...(args) > 0) { // 编译期判断，必须有 constexpr
        funcPrint2(args...);
    }
}

int main() {
    funcName(100, 200, 300, 400, 600); // 输出：5 和 5
    funcPrint(1, 2, 3, 4, 5, 6);       // 依次打印 1~6，最后打印"递归终止"
    funcPrint2(1, 2, 3, 4, 5, 6);      // 依次打印 1~6
    return 0;
}
```

#### ④ 注意事项
- `sizeof...(args)` 中的 `...` 是语法的一部分，不可省略
- 递归展开必须有终止条件（无参数的重载版本）
- 参数包展开时 `args...` 的 `...` 不可省略

> **人话总结**：可变参数模板让模板也能"吃自助餐"，想吃多少吃多少。

---

### 9. 默认成员函数控制【熟悉】（P46-P48）

#### ① 是什么
`= default` 显式要求编译器生成默认版本的特殊成员函数；`= delete` 禁止编译器生成或使用某个函数。生活比喻：`= default` 是说"这个活还是你来干"，`= delete` 是说"这个活不许干"。

#### ② 为什么
一旦用户定义了任何构造函数，编译器就不再生成默认构造函数，容易造成混乱。`= default` 和 `= delete` 让程序员精确控制哪些函数由编译器生成、哪些被禁用。

#### ③ 怎么用
```cpp
#include <iostream>
using namespace std;

class ClassTest {
public:
    ClassTest(int num) : n(num) {}
    ClassTest() = default;                        // 显式要求生成默认构造函数
    ClassTest(const ClassTest&) = delete;          // 禁止拷贝构造
    ClassTest& operator=(const ClassTest& a);      // 类内声明
private:
    int n;
};
ClassTest& ClassTest::operator=(const ClassTest& a) = default; // 类外定义=default

int main() {
    ClassTest c1;          // OK，使用默认构造
    // ClassTest c2(c1);  // 编译错误！拷贝构造被 delete
    return 0;
}
```

#### ④ 注意事项
- `= default` 只能用于编译器能隐式生成的特殊成员函数
- `= delete` 可用于任何函数，包括普通函数（阻止特定重载）

> **人话总结**：default 让编译器干活，delete 把门焊死不让用。

---

### 10. 新增容器 std::array【熟悉】（P48-P52）

#### ① 是什么
固定大小的数组封装，保存在栈内存中，不会退化为指针。生活比喻：就像一个定长的收纳格，格子数量出厂就定好了，不像 vector 那样可以动态伸缩。

#### ② 为什么
C 风格数组会退化为指针、无法知道自身大小、不能作为函数返回值。`std::array` 保留了数组的高性能同时提供了容器的安全性。

#### ③ 怎么用
```cpp
#include <iostream>
#include <array>
using namespace std;

int main() {
    array<int, 5> arr = {1, 2, 3, 4, 5};

    cout << arr[0] << endl;      // 输出：1（不检查越界）
    cout << arr.at(1) << endl;   // 输出：2（越界抛 out_of_range 异常）
    cout << get<2>(arr) << endl; // 输出：3（编译期检查越界）
    cout << arr.front() << endl; // 输出：1
    cout << arr.back() << endl;  // 输出：5

    // 注意：大小必须是编译期常量
    // int len = 3;
    // array<int, len> arr2;     // 编译错误！len 不是常量表达式
    constexpr int clen = 3;
    array<int, clen> arr3 = {4, 5, 6}; // OK

    return 0;
}
```

#### ④ 注意事项
- 大小必须是编译期常量
- `[]` 不检查越界（未定义行为），`at()` 检查越界（抛异常）
- 性能优于 vector（栈上分配，无堆分配开销）

> **人话总结**：array 是穿了盔甲的 C 数组，安全又高效。

---

### 11. 新增容器 std::forward_list【了解】（P52-P56）

单向链表实现的容器，提供 O(1) 插入，不提供 `size()` 方法，只能向前遍历。适合频繁头部插入的场景。头文件 `<forward_list>`。

> **人话总结**：forward_list 是只会往前走的单向链表。

---

### 12. 新增容器 unordered 系列【熟悉】（P56-P57）

#### ① 是什么
基于哈希表的无序关联容器：`unordered_set`、`unordered_multiset`、`unordered_map`、`unordered_multimap`。平均 O(1) 查找。

#### ② 为什么
`map/set` 基于红黑树，查找 O(logN)；哈希表平均 O(1)，适合不需要排序但追求查找速度的场景。

#### ③ 怎么用
```cpp
#include <iostream>
#include <unordered_map>
#include <unordered_set>
using namespace std;

int main() {
    unordered_map<string, int> mp = {{"aa", 1}, {"bb", 2}, {"cc", 3}};
    cout << mp.at("aa") << endl; // 输出：1
    for (auto it = mp.begin(); it != mp.end(); it++) {
        cout << it->first << "  " << it->second << endl;
    }
    // 注意：输出顺序不确定（哈希表无序）

    unordered_set<int> set1 = {11, 22, 55, 33, 88};
    cout << set1.count(66) << endl; // 输出：0（不存在）
    set1.insert(100);

    return 0;
}
```

#### ④ 注意事项
- 元素无序，不能用于需要有序遍历的场景
- 头文件：`<unordered_map>`、`<unordered_set>`

> **人话总结**：unordered 系列就是哈希表，查得快但不排序。

---

### 13. C++11 课后练习【重点】（P57-P58）

**练习**：利用 lambda 统计字符串中某字符出现次数。

配套代码走读（`C++11 hw.cpp`）：
```cpp
#include <algorithm>
#include <iostream>
#include <memory>
using namespace std;

int main() {
    char s[100] = "hello world!";
    int len = strlen(s);
    int i = 0;
    int n = 0;
    cin >> n;                                // 输入偏移量 n
    unique_ptr<char[]> ts(new char[len + 1]); // 智能指针管理动态数组
    while (i < len) {
        ts[(i + n) % len] = s[i];            // 循环移位
        i++;
    }
    ts[len] = '\0';                          // 字符串结尾
    puts(ts.get());                           // 输出移位后的字符串
    return 0;
}
```

逐行解读：`unique_ptr<char[]>` 管理动态字符数组，离开作用域自动释放。`(i+n)%len` 实现循环移位效果。

**lambda 统计字符解法**（来自 `mycode.cpp test28`）：
```cpp
#include <iostream>
#include <algorithm>
using namespace std;

int getCharNum(string s, char c) {
    int cnt = 0;
    for_each(s.begin(), s.end(), [&](char ch) { // & 引用捕获 cnt
        if (c == ch) {
            cnt++;                               // 修改外部变量 cnt
        }
    });
    return cnt;
}

int main() {
    string s1;
    cin >> s1;   // 输入：abcstringabc
    char ch;
    cin >> ch;   // 输入：a
    cout << getCharNum(s1, ch) << endl; // 输出：2
    return 0;
}
```

---

## 第二部分：C++17 语言特性

---

### 14. 折叠表达式【重点】（P2-P4）

#### ① 是什么
对可变参数包进行折叠运算的简化语法，无需手动递归展开。生活比喻：就像收银台自动累加购物车里所有商品的价格，不需要你一个个手动加。

#### ② 为什么
C++11 的可变参数模板展开需要递归或 if constexpr，代码复杂。折叠表达式一行搞定。

#### ③ 怎么用

四种形式：

| 形式 | 语法 | 展开方式 |
|------|------|---------|
| 一元右折叠 | `(args op ...)` | `E1 op (... op (EN-1 op EN))` |
| 一元左折叠 | `(... op args)` | `((E1 op E2) op ...) op EN` |
| 二元右折叠 | `(args op ... op init)` | `E1 op (... op (EN op init))` |
| 二元左折叠 | `(init op ... op args)` | `((init op E1) op ...) op EN` |

```cpp
#include <iostream>
using namespace std;

template<typename... Args>
bool all(Args... args) {
    return (... && args); // 一元左折叠：((true && true) && true) && false
}

template<typename... Args>
auto sum(Args... args) {
    return (args + ...); // 一元右折叠
}

int main() {
    bool b = all(true, true, true, false);
    cout << b << endl; // 输出：0（false）

    cout << sum(1, 2, 3, 4, 5) << endl; // 输出：15
    return 0;
}
```

#### ④ 注意事项
- 折叠表达式是 C++17 特性，需设置 `/std:c++17`
- 运算符必须是 C++ 支持的二元运算符

> **人话总结**：折叠表达式一键展开参数包，告别递归烦恼。

---

### 15. 类模板参数推导【熟悉】（P4-P5）

#### ① 是什么
实例化类模板时可省略尖括号中的类型参数，由构造函数参数自动推导。

#### ② 怎么用
```cpp
#include <iostream>
using namespace std;

template<class T>
class ClassTest {
public:
    ClassTest(T, T) {};
};

int main() {
    auto y = new ClassTest{100, 200}; // 自动推导为 ClassTest<int>
    // 等价于 new ClassTest<int>{100, 200}
    return 0;
}
```

> **人话总结**：类模板也能像函数模板一样自动推导类型了。

---

### 16. auto 占位的非类型模板形参【了解】（P5）

`template <auto T>` 允许非类型模板参数自动推导类型：`func1<100>()` 自动推导 T 为 int。

---

### 17. 编译期 constexpr if【重点】（P5-P6）

#### ① 是什么
`if constexpr` 在编译期求值条件，未选中的分支完全不生成代码。生活比喻：就像装修时根据户型图直接决定哪个房间装什么，没选的方案连图纸都不画。

#### ② 为什么
替代 SFINAE 和模板特化来实现编译期条件分支，大幅简化模板元编程。

#### ③ 怎么用
```cpp
#include <iostream>
using namespace std;

template <bool ok>
constexpr void func2() {
    if constexpr (ok == true) {   // 编译期判断
        cout << "ok" << endl;     // ok=true 时只有这行生成代码
    } else {
        cout << "not ok" << endl; // ok=false 时只有这行生成代码
    }
}

int main() {
    func2<true>();  // 输出：ok
    func2<false>(); // 输出：not ok
    return 0;
}
```

#### ④ 注意事项
- 圆括号内的表达式必须是编译期常量
- `constexpr` 关键字不可省略

> **人话总结**：if constexpr 编译期做选择，不要的代码压根不生成。

---

### 18. inline 变量【熟悉】（P6-P7）

#### ① 是什么
扩展 inline 到变量，允许在头文件中定义全局变量和类内静态成员初始化，避免多重定义错误。

#### ② 怎么用
```cpp
// mycode.h（头文件）
inline int value = 100; // 多个翻译单元包含此头文件不会报重复定义

// 类内静态成员
class AAA {
    inline static int value2 = 200; // C++17 可直接在类内初始化
};
```

> **人话总结**：inline 变量让头文件定义全局变量不再报错。

---

### 19. 结构化绑定【重点】（P7-P9）

#### ① 是什么
一行代码将 tuple/pair/结构体的成员解包到独立变量中。生活比喻：就像拆开快递包裹，一次性把所有物品拿出来分别放好。

#### ② 为什么
C++11 需要用 `tie<>` 提前声明变量再接收，繁琐且不直观。结构化绑定一步到位。

#### ③ 怎么用
```cpp
#include <iostream>
#include <tuple>
using namespace std;

int main() {
    // C++11 旧写法
    auto student = make_tuple(string{"Zhangsan"}, 19, string{"man"});
    string name; size_t age; string gender;
    tie(name, age, gender) = student;
    cout << name << ", " << age << ", " << gender << endl;

    // C++17 新写法：结构化绑定
    auto [n, a, g] = student; // 一行解包
    cout << n << ", " << a << ", " << g << endl;
    // 输出：Zhangsan, 19, man

    return 0;
}
```

#### ④ 注意事项
- 绑定变量个数必须与元素个数一致
- 可以用 `auto&` 或 `const auto&` 绑定引用

> **人话总结**：结构化绑定一行拆包，告别 tie 的繁琐。

---

### 20. if/switch 初始化语句【熟悉】（P9-P10）

#### ① 是什么
在 if/switch 的条件前添加初始化语句，将变量声明和判断合并。

#### ② 怎么用
```cpp
#include <iostream>
#include <unordered_map>
using namespace std;

int main() {
    unordered_map<string, int> stu1{{"zhangsan", 18}, {"wangwu", 19}};

    // C++11 写法
    auto iter = stu1.find("wangwu");
    if (iter != stu1.end()) {
        cout << iter->second << endl;
    }

    // C++17 写法：缩小 iter 的作用域
    if (auto it = stu1.find("wangwu"); it != stu1.end()) {
        cout << it->second << endl; // 输出：19
    }
    // it 在此处已不可见

    return 0;
}
```

> **人话总结**：if 里顺便声明变量，作用域更小更安全。

---

### 21. 简化的嵌套命名空间【熟悉】（P10）

```cpp
// C++17 之前
namespace A { namespace B { namespace C { void func1() {} }}}

// C++17
namespace A::B::C { void func1() {} } // 一行搞定
```

---

### 22. using 声明多个名称【了解】（P10）

`using std::cout, std::cin;` 一行导入多个名称。

---

### 23. lambda 捕获 *this【熟悉】（P11-P12）

#### ① 是什么
`[*this]` 捕获对象的副本而非 this 指针，避免多线程下悬空指针。

#### ② 怎么用
```cpp
#include <iostream>
using namespace std;

class ClassTest {
public:
    int num;
    void func1() {
        auto lamfunc = [*this]() { cout << num << endl; }; // 捕获对象副本
        lamfunc();
    }
};

int main() {
    ClassTest a;
    a.num = 100;
    a.func1(); // 输出：100
    return 0;
}
```

> **人话总结**：[*this] 拷一份对象进 lambda，不怕原对象被销毁。

---

### 24. 属性列表与新增属性【熟悉】（P12-P15）

| 属性 | 作用 |
|------|------|
| `[[fallthrough]]` | switch 中故意穿透不警告 |
| `[[nodiscard]]` | 返回值不可忽略，忽略则警告 |
| `[[maybe_unused]]` | 抑制未使用变量/函数的警告 |
| `[[using ns: attr1, attr2]]` | C++17 简化重复命名空间 |

```cpp
[[nodiscard]] auto func(int a, int b) { return a + b; }
int main() {
    func(2, 3); // 警告：返回值被忽略
    [[maybe_unused]] int num = 0; // 不警告
    return 0;
}
```

---

### 25. __has_include【了解】（P13）

预处理阶段检测头文件是否存在，用于跨平台兼容：
```cpp
#if __has_include(<optional>)
    #include <optional>
#endif
```

---

### 26. charconv【熟悉】（P15-P19）

#### ① 是什么
高性能数值-字符串互转库，不分配内存、不抛异常、locale 无关。替代 atoi/sprintf。

#### ② 怎么用
```cpp
#include <iostream>
#include <charconv>
using namespace std;

int main() {
    // 字符串转整数
    string s1{"123456789"};
    int val = 0;
    auto res = from_chars(s1.data(), s1.data() + 4, val); // 只转前4个字符
    if (res.ec == errc()) {
        cout << "val: " << val << endl;           // 输出：val: 1234
        cout << "distance: " << res.ptr - s1.data() << endl; // 输出：distance: 4
    }

    // 字符串转浮点
    s1 = "12.34";
    double value = 0;
    res = from_chars(s1.data(), s1.data() + s1.size(), value, chars_format::general);
    cout << "value: " << value << endl; // 输出：value: 12.34

    // 整数转字符串
    s1 = "xxxxxxxx";
    int v = 1234;
    auto result = to_chars(s1.data(), s1.data() + s1.size(), v);
    cout << "str: " << s1 << endl; // 输出：str: 1234xxxx
    cout << "filled: " << result.ptr - s1.data() << " characters." << endl; // 输出：filled: 4 characters.

    return 0;
}
```

> **人话总结**：charconv 是最快的数字字符串转换器，零开销。

---

### 27. std::variant【熟悉】（P19-P20）

类型安全的联合体，同一时间只存一种类型。`index()` 查当前类型索引，`holds_alternative<T>()` 检查类型。

```cpp
#include <iostream>
#include <variant>
#include <string>
using namespace std;

int main() {
    variant<int, double, string> d; // int=0, double=1, string=2
    cout << d.index() << endl;      // 输出：0（默认第一个类型）
    d = 3.14;
    cout << d.index() << endl;      // 输出：1
    d = "hi";
    cout << d.index() << endl;      // 输出：2
    cout << holds_alternative<string>(d) << endl; // 输出：1
    return 0;
}
```

---

### 28. std::optional【重点】（P21-P23）

#### ① 是什么
表示"可能有值也可能没有"的类型安全容器。生活比喻：就像一个可能装着礼物的盒子，打开之前你不知道里面有没有东西。

#### ② 为什么
用裸指针表示 nullable 语义容易出空指针崩溃，用哨兵值（如 -1）不够通用。optional 以类型安全的方式表达"可能有值"。

#### ③ 怎么用
```cpp
#include <iostream>
#include <optional>
using namespace std;

int main() {
    optional<int> o1;             // 默认无值（nullopt）
    optional<int> o2 = nullopt;   // 显式无值
    optional<int> o3 = 10;        // 有值
    optional<int> o4 = o3;        // 拷贝

    // 判断有无值
    if (o3) { cout << "o3 has value" << endl; }         // 输出：o3 has value
    if (o3.has_value()) { cout << "yes" << endl; }       // 输出：yes

    // 取值
    cout << *o3 << endl;           // 输出：10
    cout << o3.value() << endl;    // 输出：10（无值时抛 bad_optional_access）

    // 字符串取值
    optional<string> o5 = "orange";
    cout << o5->c_str() << endl;   // 输出：orange

    // 清空
    o3.reset();
    cout << o3.has_value() << endl; // 输出：0

    return 0;
}
```

#### ④ 注意事项
- `*o` 在无值时是未定义行为，`o.value()` 在无值时抛异常
- 用 `has_value()` 或 `operator bool` 先检查再取值

> **人话总结**：optional 是安全的"可能有值"盒子，告别 nullptr。

---

### 29. std::any【熟悉】（P23-P25）

可存储任意类型且运行时可变类型的容器，类似 Python 的动态变量。用 `any_cast<T>` 取值，类型不匹配抛 `bad_any_cast`。

```cpp
#include <any>
#include <iostream>
using namespace std;

int main() {
    any a;
    cout << a.has_value() << endl; // 输出：0
    a = 2;                         // 存 int
    a = 3.14;                      // 改为 double
    try {
        auto v = any_cast<double>(a);
        cout << v << endl;         // 输出：3.14
    } catch (const bad_any_cast& e) {
        cout << e.what() << endl;
    }
    a.reset();                     // 清空
    return 0;
}
```

---

### 30. std::apply 与 make_from_tuple【了解】（P25-P26）

- `apply(func, tuple)` 将 tuple 解包作为函数参数调用
- `make_from_tuple<ClassTest>(tuple)` 将 tuple 解包作为构造函数参数

---

### 31. std::string_view【重点】（P27-P28）

#### ① 是什么
只读字符串视图，零拷贝构造，避免 `char*` 到 `string` 的不必要内存分配。生活比喻：就像透过窗户看风景，不需要把风景搬进屋里。

#### ② 为什么
`char*` 传给 `string` 参数会触发拷贝构造，如果只需读取则完全浪费。`string_view` 只记录指针和长度，零开销。

#### ③ 怎么用
```cpp
#include <iostream>
#include <string_view>
using namespace std;

void func1(string_view str_v) { // 零拷贝接收字符串
    cout << str_v << endl;
}

int main() {
    const char* charStr = "hello world";
    string str{charStr};                              // 拷贝了一份
    string_view str_v(charStr, strlen(charStr));       // 零拷贝
    cout << "str: " << str << endl;                    // 输出：str: hello world
    cout << "str_v: " << str_v << endl;                // 输出：str_v: hello world
    func1(str_v);                                      // 零拷贝传参
    return 0;
}
```

#### ④ 注意事项
- string_view 只有读权限，没有写权限
- 必须确保原始字符串的生命周期长于 string_view
- 不要对 string_view 做修改操作

> **人话总结**：string_view 只看不拷贝，读字符串零开销。

---

### 32. std::as_const【了解】（P28）

将左值转为 const 引用，方便在 range-for 中避免不必要的拷贝。

---

### 33. std::filesystem【重点】（P29-P34）

#### ① 是什么
标准化的文件系统操作库，提供路径处理、目录遍历、文件信息查询等功能。生活比喻：就像操作系统自带的文件管理器 API，终于有了跨平台的 C++ 标准接口。

#### ② 为什么
C++17 之前处理文件路径和目录遍历需要平台相关 API（Windows 用 `_finddata`，Linux 用 `dirent`），移植性差。

#### ③ 怎么用

四大核心类：`path`、`directory_entry`、`directory_iterator`、`file_status`

配套代码走读（`C++17 案例代码/mycode.cpp test21`）：
```cpp
#include <iostream>
#include <filesystem>
using namespace std;

int main() {
    namespace fs = std::filesystem;
    auto testdir = fs::path("./testdir");

    if (!fs::exists(testdir)) { // 判断路径是否存在
        cout << "file or directory is not exists!" << endl;
    }

    fs::directory_options opt(fs::directory_options::none);
    fs::directory_entry dir(testdir);

    // 遍历当前目录（不递归）
    cout << "show:\t" << dir.path().filename() << endl;
    for (fs::directory_entry const& entry : fs::directory_iterator(testdir, opt)) {
        if (entry.is_regular_file()) {
            cout << entry.path().filename()
                 << "\t size: " << entry.file_size() << endl;
        } else if (entry.is_directory()) {
            cout << entry.path().filename() << "\t dir" << endl;
        }
    }

    // 递归遍历所有子目录
    cout << "show all:" << endl;
    for (fs::directory_entry const& entry : fs::recursive_directory_iterator(testdir, opt)) {
        if (entry.is_regular_file()) {
            cout << entry.path().filename()
                 << "\t size: " << entry.file_size()
                 << "\t parent: " << entry.path().parent_path() << endl;
        } else if (entry.is_directory()) {
            cout << entry.path().filename() << "\t dir" << endl;
        }
    }
    return 0;
}
```

常用函数速查：`exists()`、`copy()`、`create_directory()`、`create_directories()`、`file_size()`、`absolute()`

**C++17 作业**（`C++ 17 hw.cpp`）——遍历目录树函数：
```cpp
void DisplayDirTree(const fs::path& pathToShow, int level) {
    if (fs::exists(pathToShow) && fs::is_directory(pathToShow)) {
        auto lead = std::string(level * 3, ' '); // 缩进
        for (const auto& entry : fs::directory_iterator(pathToShow)) {
            auto filename = entry.path().filename();
            if (fs::is_directory(entry.status())) {
                cout << lead << "[+] " << filename << "\n";
                DisplayDirTree(entry, level + 1); // 递归进入子目录
                cout << "\n";
            } else if (fs::is_regular_file(entry.status())) {
                // DisplayFileInfo(entry, lead, filename); // 显示文件信息
            } else {
                cout << lead << " [?]" << filename << "\n";
            }
        }
    }
}
```

#### ④ 注意事项
- 必须设置 C++17 标准（`/std:c++17`）
- VS 中可能需要链接 `stdc++fs` 库
- `recursive_directory_iterator` 遍历时跳过符号链接可用 `follow_directory_symlink` 选项

> **人话总结**：filesystem 让 C++ 终于有了跨平台的文件操作标准库。

---

## 第三部分：C++20 新特性

---

### 34. 模块 Modules【重点】（P2-P7）

#### ① 是什么
替代 `#include` 的模块化机制，通过 `export module` 声明模块、`import` 导入、`export` 导出。生活比喻：`#include` 就像把整本参考书复印粘贴到你的笔记里；模块就像只在笔记本上写一个索引号，需要时再去查阅原书。

#### ② 为什么
`#include <iostream>` 仅约 70 字符的代码会产生 419909 字符供编译器处理。头文件的文本替换机制导致宏污染、编译慢、顺序依赖等问题。

#### ③ 怎么用
```cpp
// mymodule.ixx —— 模块文件（约定后缀 .ixx）
export module helloworld;    // 模块声明
import <iostream>;           // 导入标准库模块

export void hello() {        // export 导出函数
    std::cout << "Hello world!\n";
}

// main.cpp —— 使用模块
import helloworld;           // 导入自定义模块

int main() {
    hello(); // 输出：Hello world!
}
```

#### ④ 八大优点
1. 没有头文件
2. 声明实现仍然可分离，但非必要
3. 可以显式指定导出哪些类或函数
4. 不需要 include guards
5. 模块之间名称可以相同且不冲突
6. 模块只处理一次，编译更快
7. 预处理宏只在模块内有效
8. 模块的引入与引入顺序无关

#### ⑤ 注意事项
- `.ixx` 是 VS 约定的模块文件后缀，非强制
- 目前各编译器对模块的支持程度不一
- C++20 作业答案即上述八大优点

> **人话总结**：模块是头文件的终结者，编译更快更干净。

---

### 35. 协程 Coroutines【重点】（P7-P8）

#### ① 是什么
可以挂起（suspend）和恢复（resume）的函数。生活比喻：就像视频播放器的暂停键——按下暂停保存当前画面，之后按继续从暂停处恢复播放。

#### ② 为什么
异步编程用回调或 future/promise 链式调用代码可读性差。协程让你用同步的方式写异步代码，逻辑清晰。

#### ③ 怎么用

三个关键字：
- `co_yield some_value`：产出值并挂起
- `co_await some_awaitable`：等待异步操作完成
- `co_return some_value`：结束协程

**重要强调**：C++20 只提供协程机制，不提供协程库。需要自己实现 promise_type 等基础设施。

配套代码走读（`协程案例.cpp`）——斐波那契数列生成器：
```cpp
#include <coroutine>
#include <exception>
#include <iostream>
using namespace std;

template<typename T>
struct Generator {
    struct promise_type;
    using handle_type = coroutine_handle<promise_type>;

    struct promise_type {
        T value_;
        exception_ptr exception_;

        Generator get_return_object() {
            return Generator(handle_type::from_promise(*this));
        }
        suspend_always initial_suspend() { return {}; }   // 创建后立即挂起
        suspend_always final_suspend() noexcept { return {}; } // 结束时挂起
        void unhandled_exception() { exception_ = current_exception(); }

        template<std::convertible_to<T> From>
        suspend_always yield_value(From&& from) {
            value_ = forward<From>(from); // 在 promise 中存储产出的值
            return {};                     // 挂起
        }
        void return_void() {}
    };

    handle_type h_;
    Generator(handle_type h) : h_(h) {}
    ~Generator() { h_.destroy(); }

    explicit operator bool() {
        fill();
        return !h_.done(); // 协程是否还有值
    }
    T operator()() {
        fill();
        full_ = false;
        return move(h_.promise().value_); // 取出 promise 中存储的值
    }

private:
    bool full_ = false;
    void fill() {
        if (!full_) {
            h_(); // 恢复协程执行到下一个 co_yield
            if (h_.promise().exception_)
                rethrow_exception(h_.promise().exception_);
            full_ = true;
        }
    }
};

// 斐波那契协程
Generator<uint64_t> fibonacci_sequence(unsigned n) {
    if (n == 0) co_return;
    if (n > 94) throw runtime_error("too large");
    co_yield 0;
    if (n == 1) co_return;
    co_yield 1;
    if (n == 2) co_return;

    uint64_t a = 0, b = 1;
    for (unsigned i = 2; i < n; i++) {
        uint64_t s = a + b;
        co_yield s;   // 产出值并挂起
        a = b;
        b = s;
    }
}

int main() {
    try {
        auto gen = fibonacci_sequence(10);
        for (int j = 0; gen; j++)
            cout << "fib(" << j << ")=" << gen() << '\n';
    } catch (const exception& ex) {
        cerr << "异常：" << ex.what() << '\n';
    }
}
// 输出：fib(0)=0, fib(1)=1, fib(2)=1, fib(3)=2, ..., fib(9)=34
```

#### ④ 注意事项
- C++20 只提供机制不提供库，需自行实现 Generator 等包装类
- 协程是无栈协程，本身不抢占内核调度
- 不能在 main 函数中使用协程关键字

> **人话总结**：协程是可暂停恢复的函数，用同步写法做异步事。

---

### 36. 三向比较运算符 <=>【重点】（P8-P10）

#### ① 是什么
一次比较得到小于/等于/大于三种结果的运算符。生活比喻：就像天平秤，一次称重就知道哪边重、哪边轻还是一样重。

#### ② 为什么
以前实现完整比较需要重载 6 个运算符（<、<=、>、>=、==、!=）。`<=>` 一个搞定，还能 `= default` 自动生成。

#### ③ 怎么用
```cpp
#include <iostream>
using namespace std;

int main() {
    int num1 = 100, num2 = 100;
    if ((num1 <=> num2) < 0) {
        cout << "num1 < num2" << endl;
    } else if ((num1 <=> num2) > 0) {
        cout << "num1 > num2" << endl;
    } else {
        cout << "num1 = num2" << endl; // 输出：num1 = num2
    }
    return 0;
}

// 自定义类自动生成所有比较运算符
struct Point {
    int x, y;
    auto operator<=>(const Point&) const = default; // 自动生成全部6个比较运算符
};
```

#### ④ 注意事项
- `<=>` 类似 strcmp 返回 -1/0/1 的思路，但返回的是强序/弱序/偏序类型
- `= default` 对结构体逐成员比较

> **人话总结**：<=> 一个顶六个，比较运算符全家桶。

---

### 37. 范围 Ranges【重点】（P10-P12）

#### ① 是什么
管道式组合的数据处理视图，直接对整个容器操作，惰性求值。生活比喻：就像工厂流水线，原材料进去经过筛选、加工、包装，出来的就是成品，中间不需要暂存。

#### ② 为什么
STL 算法需要 begin/end 迭代器对，嵌套使用时代码嵌套深、可读性差。Ranges 用 `|` 管道符串联操作，直观优雅。

#### ③ 怎么用
```cpp
#include <vector>
#include <ranges>
#include <iostream>
using namespace std;

int main() {
    auto ints = views::iota(0, 10);               // 生成 0~9
    auto even = [](int i) { return 0 == i % 2; }; // 偶数过滤
    auto square = [](int i) { return i * i; };     // 平方变换

    for (int i : ints | views::filter(even) | views::transform(square)) {
        cout << i << ' '; // 输出：0 4 16 36 64
    }
    return 0;
}
```

#### ④ 注意事项
- 需要 C++20 标准和 `<ranges>` 头文件
- views 是惰性求值，不会立即执行
- 也可以直接对整个容器排序：`sort(s)` 代替 `sort(s.begin(), s.end())`

> **人话总结**：Ranges 用管道符串起数据处理，像流水线一样优雅。

---

### 38. 日期和时区【熟悉】（P12-P13）

```cpp
#include <iostream>
#include <chrono>
using namespace std;
using namespace std::chrono;

int main() {
    auto y1 = year{2019};       auto y2 = 2019y;      // 年
    auto m1 = month{9};         auto m2 = September;   // 月
    auto d1 = day{18};          auto d2 = 18d;         // 日

    year_month_day date1{2022y, July, 21d};
    auto date2 = 2022y / July / 21d;
    year_month_day date3{Monday[3] / July / 2022};     // 2022年7月第三个周一

    cout << date1 << endl; // 输出：2022-07-21
    cout << date2 << endl; // 输出：2022-07-21
    cout << date3 << endl; // 输出：2022-07-18
    return 0;
}
```

---

### 39. 格式化 format【熟悉】（P14）

类 printf 但类型安全的字符串格式化：
```cpp
#include <iostream>
#include <format>
using namespace std;

int main() {
    string s1 = "C++";
    cout << format("The string '{}' has {} chars", s1, s1.size()) << endl;
    // 输出：The string 'C++' has 3 chars

    // 位置参数
    cout << format("'{0}' has {1} chars, '{1}' then '{0}'", s1, s1.size()) << endl;
    // 输出：'C++' has 3 chars, '3' then 'C++'
    return 0;
}
```

---

### 40. 跨度 span【熟悉】（P14-P15）

携带指针+长度的轻量视图，替代原始指针+长度参数对，防止缓冲区溢出：
```cpp
#include <iostream>
#include <span>
using namespace std;

void func(span<int> a) {   // span 包含指针和大小信息
    for (int& x : a) {     // 范围 for 自动提取范围
        x = 7;
    }
}

int main() {
    int arr[] = {1, 2, 3, 4, 5};
    func(arr); // 自动推导 span<int>
    for (int x : arr) cout << x << " "; // 输出：7 7 7 7 7
    return 0;
}
```

---

### 41. 并发 promise/future/jthread【重点】（P16-P20）

#### ① 是什么
`promise` 设置值、`future` 获取值、`jthread` 自动 join 的线程。生活比喻：promise 是寄件人把包裹放进快递柜，future 是收件人从快递柜取包裹，jthread 是快递员下班前自动确认所有包裹都送达了。

#### ② 为什么
传统的线程间通信方式（全局变量+mutex）复杂且易出错。promise/future 提供了类型安全的异步值传递机制。

#### ③ 怎么用
```cpp
#include <iostream>
#include <future>
#include <format>
using namespace std;

void product(promise<int>&& intPromise, int v1, int v2) {
    intPromise.set_value(v1 * v2); // 设置值
}

int main() {
    int num1 = 200, num2 = 300;
    promise<int> productPromise;
    future<int> productResult = productPromise.get_future(); // 获取 future
    jthread productThread(product, move(productPromise), num1, num2); // jthread 自动 join
    cout << format("product is {}\n", productResult.get()); // 输出：product is 60000
    return 0;
}
```

**wait_for 超时等待**：
```cpp
void getAnswer(promise<int> intPromise) {
    this_thread::sleep_for(2s);
    intPromise.set_value(100);
}

int main() {
    promise<int> answerPromise;
    auto fut = answerPromise.get_future();
    jthread t(getAnswer, move(answerPromise));
    future_status status{};
    do {
        status = fut.wait_for(0.5s); // 每0.5秒检查一次
        cout << "结果未准备完成" << endl;
    } while (status != future_status::ready);
    cout << format("answer is {}\n", fut.get()); // 输出：answer is 100
    return 0;
}
```

`future_status` 枚举：`ready`（成功）、`timeout`（超时）、`deferred`（延迟）

#### ④ 注意事项
- `promise` 只能 set_value 一次，多次调用抛异常
- `jthread` 析构时自动 join，避免忘记 join 导致的 terminate
- `future::get()` 只能调用一次

> **人话总结**：promise寄包裹future取包裹，jthread自动签收。

---

## 第四部分：配套代码完整走读

### C++11 案例代码走读要点

`Test002.cpp` 中 test01-test28 覆盖了所有 C++11 知识点，main 函数中通过注释切换测试。关键走读：
- **test01**：auto 推导迭代器，对比旧写法
- **test07**：右值引用绑定常量和函数返回值
- **test11**：lambda 各种捕获方式演示，含 mutable、函数指针赋值
- **test14**：lambda 替代仿函数排序 Goods
- **test17**：weak_ptr 解决循环引用（CA 中 m_ptr_b 改为 weak_ptr）
- **test28**：for_each + lambda 引用捕获统计字符

### C++17 案例代码走读要点

- **test01**：折叠表达式 `(... && args)`
- **test06**：结构化绑定解包 tuple
- **test07**：if 初始化语句
- **test13**：charconv 数值转换
- **test15**：optional 构造、判值、取值、reset
- **test21**：filesystem 遍历目录（directory_iterator + recursive_directory_iterator）

### C++20 案例代码走读要点

- **test01**：三向比较运算符 `<=>`
- **test02**：ranges 管道式 filter + transform
- **test03**：日期字面量 2022y/July/12d
- **test04**：format 格式化输出
- **test05/test06**：promise/future/jthread 并发
- **test09**：concepts 约束（requires 子句）

---

## 第五部分：对比表格汇总

### 旧写法 vs 新写法对比表

| 场景 | 旧写法（C++98/03） | 新写法 | 版本 |
|------|-------------------|--------|------|
| 迭代器声明 | `vector<int>::iterator it = v.begin()` | `auto it = v.begin()` | C++11 |
| 容器遍历 | `for(it=v.begin();it!=v.end();++it)` | `for(auto x : v)` | C++11 |
| 排序比较 | 手写 Compare 仿函数类 | `[](const T&a,const T&b){return a<b;}` | C++11 |
| 内存管理 | `new/delete` 手动管理 | `make_shared/make_unique` | C++11 |
| 泛型返回值 | 需额外模板参数 R | `auto f()->decltype(t+u)` | C++11 |
| 解包 tuple | `tie(a,b,c)=t` | `auto [a,b,c]=t` | C++17 |
| 数值转换 | `atoi/sprintf` | `from_chars/to_chars` | C++17 |
| 文件操作 | 平台相关 API | `std::filesystem` | C++17 |
| 头文件包含 | `#include "xxx.h"` | `import xxx` | C++20 |
| 比较运算符 | 重载6个运算符 | `operator<=>=default` | C++20 |
| 数据管道 | 嵌套 begin/end 算法 | `views::filter\|transform` | C++20 |

### 智能指针对比表

| 特性 | shared_ptr | unique_ptr | weak_ptr |
|------|-----------|------------|----------|
| 所有权模型 | 共享 | 独占 | 观察者 |
| 引用计数 | 维护 | 不维护 | 不增加 |
| 复制 | 允许（计数+1） | 禁止 | 允许 |
| 移动 | 允许 | 允许 | 允许 |
| 自定义删除器 | 支持 | 支持 | 不支持 |
| 循环引用 | 会导致泄漏 | 不会 | 用于解决 |
| 线程安全 | 引用计数原子操作 | 不保证 | lock()返回shared_ptr |
| 推荐创建方式 | make_shared | make_unique(C++14) | 从shared_ptr构造 |

### auto vs decltype 对比表

| 特性 | auto | decltype |
|------|------|----------|
| 用途 | 从初始化表达式推导变量类型 | 查询任意表达式类型 |
| 是否求值 | 需要初始化表达式 | 不求值 |
| 函数参数 | C++11不支持 | 可用于尾置返回类型 |
| const处理 | 非引用丢弃，引用保留 | 精确保留表达式类型 |
| 典型场景 | 简化变量声明 | 泛型编程返回值推导 |

---

## 第六部分：两套速查表

### 精简版速查表（一页速查）

| 特性 | 版本 | 一句话定位 | 核心语法 |
|------|------|-----------|---------|
| auto | C++11 | 类型自动推导 | `auto x = expr;` |
| decltype | C++11 | 查询表达式类型 | `decltype(expr)` |
| 右值引用/移动 | C++11 | 资源转移避免拷贝 | `T(T&&)` `std::move()` |
| 列表初始化 | C++11 | 统一花括号初始化 | `T{args}` |
| 范围for | C++11 | 简洁容器遍历 | `for(auto x : c)` |
| Lambda | C++11 | 匿名函数对象 | `[cap](p)->r{body}` |
| shared_ptr | C++11 | 共享所有权智能指针 | `make_shared<T>()` |
| unique_ptr | C++11 | 独占所有权智能指针 | `make_unique<T>()` |
| weak_ptr | C++11 | 弱引用打破循环 | `weak_ptr<T>` |
| 可变参数模板 | C++11 | 任意数量模板参数 | `template<class...T>` |
| =default/=delete | C++11 | 控制默认函数生成 | `Func()=default/delete` |
| array | C++11 | 固定大小安全数组 | `array<T,N>` |
| unordered系列 | C++11 | 哈希表O(1)查找 | `unordered_map/set` |
| 折叠表达式 | C++17 | 参数包运算展开 | `(... op args)` |
| 类模板推导 | C++17 | 省略模板参数 | `ClassTest{100,200}` |
| constexpr if | C++17 | 编译期条件分支 | `if constexpr(cond)` |
| inline变量 | C++17 | 头文件全局变量 | `inline int x=0;` |
| 结构化绑定 | C++17 | 一行解包 | `auto[a,b]=pair` |
| if初始化 | C++17 | 缩小作用域 | `if(init;cond)` |
| string_view | C++17 | 零拷贝字符串视图 | `string_view sv` |
| optional | C++17 | 类型安全nullable | `optional<T>` |
| variant | C++17 | 类型安全union | `variant<T1,T2>` |
| filesystem | C++17 | 跨平台文件操作 | `fs::path/exists/copy` |
| Modules | C++20 | 替代头文件 | `export/import` |
| 协程 | C++20 | 可挂起恢复函数 | `co_yield/co_await` |
| <=> | C++20 | 三向比较 | `a<=>b` |
| Ranges | C++20 | 管道式数据处理 | `views::filter\|transform` |
| format | C++20 | 类型安全格式化 | `format("{} {}",a,b)` |
| span | C++20 | 带长度指针视图 | `span<T>` |
| jthread | C++20 | 自动join线程 | `jthread t(f,args)` |

### 详细版速查表

（上方精简表中每项均已在正文"怎么用"部分给出了完整语法和示例代码，此处不再重复。）

---

## 第七部分：易错点速查卡

| 错误现象 | 错误原因 | 正确写法 | 后果 |
|----------|---------|---------|------|
| `auto a = const_var;` 后修改 a 不影响原变量 | auto 非引用推导丢弃 const | `const auto& a = const_var;` | 语义不符预期 |
| move 后访问原对象得到不确定值 | moved-from 对象资源已被转走 | move 后不再读取原对象 | 未定义行为 |
| shared_ptr 互相持有导致内存泄漏 | 循环引用使引用计数永不为0 | 一方改用 weak_ptr | 内存泄漏 |
| `vector<int> v{10}` 只有一个元素10 | 列表初始化优先匹配 initializer_list | `vector<int> v(10)` 才是10个元素 | 逻辑错误 |
| lambda 值捕获变量无法修改 | 值捕获默认 const | 加 mutable 关键字 | 编译错误 |
| string_view 指向已销毁的字符串 | string_view 不拥有数据 | 确保原始字符串生命周期更长 | 悬空指针 |
| optional 无值时调用 *o | 未检查 has_value | 先 `if(o)` 再 `*o` | 未定义行为 |
| any_cast 类型不匹配 | 存储类型与请求类型不一致 | 用 try-catch 包裹 | 抛 bad_any_cast |
| `array<int,len>` len 为变量 | 大小必须是编译期常量 | 用 constexpr 修饰 len | 编译错误 |
| 协程在 main 中使用 co_yield | main 不能是协程 | 封装到普通协程函数中 | 编译错误 |

---

## 第八部分：常见陷阱专题

### 陷阱1：auto 推导丢失 const

**错误写法**：
```cpp
const int c = 10;
auto a = c;  // a 是 int，不是 const int
a = 20;      // 合法！但你以为 a 也是 const
```
**正确写法**：
```cpp
const auto& a = c; // a 是 const int&
// 或
decltype(c) a = c; // a 是 const int
```
**如何记住**：auto 像"脱衣服"，非引用时脱掉 const；引用时保留。

### 陷阱2：std::move 后的对象状态不确定

**错误写法**：
```cpp
string s = "hello";
string s2 = std::move(s);
cout << s.length(); // 结果未定义（可能是0，也可能崩溃）
```
**正确写法**：move 后不再使用原对象，或只对其做赋值/析构操作。
**如何记住**：move 就像"搬家"，房子还在但东西搬走了。

### 陷阱3：shared_ptr 循环引用导致内存泄漏

**错误写法**：
```cpp
class A { shared_ptr<B> b_ptr; };
class B { shared_ptr<A> a_ptr; };
// A 和 B 互相持有 shared_ptr，引用计数永远 >= 1，永不释放
```
**正确写法**：其中一方改用 `weak_ptr`。
**如何记住**：shared_ptr 是"手拉手"，环状拉手谁也松不开；weak_ptr 是"看一眼"，不算拉手。

---

## 第九部分：新手最常问的5个问题

**Q1：auto 和 decltype 有什么区别？**
A：auto 从初始化表达式推导变量类型，必须有初始值；decltype 查询任意表达式类型但不求值，可用于尾置返回类型。面试回答思路：auto 是"看值猜类型"，decltype 是"看表达式知类型"。

**Q2：什么时候用 shared_ptr，什么时候用 unique_ptr？**
A：默认优先用 unique_ptr（零开销、独占语义明确）。只有在确实需要多个所有者共享同一资源时才用 shared_ptr（引用计数有额外开销）。面试回答思路：unique_ptr 是首选，shared_ptr 是"确实需要共享时"的选择。

**Q3：lambda 的值捕获和引用捕获怎么选？**
A：需要修改外部变量用引用捕获 `&`；lambda 生命周期可能超过外部变量用值捕获 `=`（或 `[*this]`）；只读访问且担心悬空引用也用值捕获。面试回答思路：安全第一选值捕获，性能敏感且确定安全选引用捕获。

**Q4：optional 和指针表示 nullable 有什么区别？**
A：optional 是值语义，存储在栈上，不会出现空指针解引用的未定义行为；指针是引用语义，需要手动检查 nullptr。面试回答思路：optional 是类型安全的 nullable，指针是不安全的 nullable。

**Q5：C++20 协程为什么不能直接用？**
A：C++20 只提供了协程的三个关键字（co_await/co_yield/co_return）和底层机制，没有提供标准库级别的 Generator/Task 等高层抽象。需要自行实现 promise_type 等基础设施或使用第三方库（如 cppcoro）。面试回答思路：机制和库分离，给了最大灵活性但增加了使用门槛。

---

## 第十部分：代码自测清单

学完本章后，你应该能独立写出以下代码：

- [ ] 用 auto 和 decltype 正确推导变量和函数返回值类型
- [ ] 编写移动构造函数和移动赋值运算符，正确使用 std::move
- [ ] 用 lambda 表达式替代仿函数完成排序/遍历等操作
- [ ] 选择合适的智能指针（shared/unique/weak）管理动态内存
- [ ] 用结构化绑定解包 tuple，用 optional 表示可空返回值
- [ ] 用 filesystem 遍历目录、判断文件存在、获取文件大小
- [ ] 用 C++20 模块(.ixx)组织代码，用 ranges 管道式处理数据
- [ ] 用三向比较运算符 <=> 简化类的比较逻辑

---

## 第十一部分：复习计划

| 时间 | 复习内容 | 方式 |
|------|----------|------|
| 1天后 | auto/decltype 推导规则、lambda 捕获列表 | 重做练习题 + 默写语法 |
| 3天后 | 移动语义、智能指针、optional/variant | 阅读笔记 + 写小 demo 验证 |
| 7天后 | 全章回顾（C++11→17→20 特性脉络） | 看树状图回忆 + 面试题自测 |
| 14天后 | 综合实战（filesystem + ranges + 协程） | 完成 mini 项目 |

---

## 第十二部分：树状图（全章知识体系）

```
C++ 常用新特性
├── C++11 核心语言特性
│   ├── 自动类型推导
│   │   ├── auto（类型占位符）
│   │   └── decltype（类型查询）
│   ├── 右值引用与移动语义
│   │   ├── 左值 vs 右值
│   │   ├── 右值引用 &&
│   │   ├── 移动构造函数
│   │   └── std::move
│   ├── 列表初始化 {}
│   ├── 范围 for
│   ├── Lambda 表达式
│   │   ├── 捕获列表（5种形式）
│   │   ├── mutable
│   │   └── 等价仿函数对照
│   ├── 智能指针
│   │   ├── shared_ptr（共享+引用计数）
│   │   ├── unique_ptr（独占）
│   │   └── weak_ptr（打破循环引用）
│   ├── 可变参数模板
│   │   ├── sizeof...
│   │   ├── 递归展开
│   │   └── if constexpr 展开
│   ├── 默认成员函数控制（=default/=delete）
│   └── 新增容器
│       ├── std::array
│       ├── std::forward_list
│       └── unordered 系列
├── C++17 语言特性
│   ├── 折叠表达式（4种形式）
│   ├── 类模板参数推导
│   ├── auto 非类型模板形参
│   ├── constexpr if
│   ├── inline 变量
│   ├── 结构化绑定
│   ├── if/switch 初始化语句
│   ├── 嵌套命名空间简化
│   ├── lambda 捕获 *this
│   ├── 属性（fallthrough/nodiscard/maybe_unused）
│   └── __has_include
├── C++17 库相关
│   ├── charconv（高性能数值转换）
│   ├── variant（类型安全 union）
│   ├── optional（类型安全 nullable）
│   ├── any（动态类型容器）
│   ├── apply / make_from_tuple
│   ├── string_view（零拷贝字符串视图）
│   ├── as_const
│   └── filesystem（文件操作）
└── C++20 新特性
    ├── Modules（模块化）
    ├── Coroutines（协程）
    ├── <=> 三向比较运算符
    ├── Ranges（管道式数据处理）
    ├── 日期和时区
    ├── format（类型安全格式化）
    ├── span（带长度指针视图）
    └── 并发（promise/future/jthread）
```

---

## 第十三部分：口诀

1. **auto 脱衣引穿衣，非引丢 const 引保留**（auto 推导规则）
2. **move 搬家不搬房，shared 拉手 weak 旁观**（移动语义 + 智能指针）
3. **折叠一行替递归，管道串联 ranges 飞**（C++17 折叠表达式 + C++20 ranges）

---

## 第十四部分：练习题（答案留空）

### 题目1（★）考察：auto + 范围 for
```cpp
// 补全代码，用 auto 和范围 for 遍历并打印 vector 中所有元素的平方
#include <iostream>
#include <vector>
using namespace std;
int main() {
    vector<int> v = {1, 2, 3, 4, 5};
    // 请在此补全：用范围 for + auto 遍历并输出每个元素的平方
    return 0;
}
```

### 题目2（★★）考察：lambda + 智能指针
```cpp
// 用 lambda 和 unique_ptr 实现：创建一个动态 int 数组，用 lambda 填充 1~10，再打印
#include <iostream>
#include <memory>
using namespace std;
int main() {
    // 请在此补全：用 unique_ptr<int[]> 管理数组
    // 请在此补全：用 lambda 填充和打印
    return 0;
}
```

### 题目3（★★★）考察：optional + structured bindings + filesystem
```cpp
// 编写函数：给定路径，返回文件大小（optional<size_t>），文件不存在返回 nullopt
// 然后在 main 中用结构化绑定展示结果
#include <optional>
#include <filesystem>
#include <iostream>
using namespace std;
// 请在此补全：实现 getFileSize 函数
// 请在此补全：在 main 中调用并用 if 检查结果
```

### 题目4（★★★★ 综合题）考察：ranges + format + 三向比较 + lambda
```cpp
// 定义 Student 结构体（name, score），用 <=> 自动生成比较
// 创建 vector<Student>，用 ranges 过滤及格学生并按分数降序排列
// 用 format 输出每位及格学生的信息
#include <vector>
#include <ranges>
#include <format>
#include <iostream>
#include <compare>
using namespace std;

struct Student {
    string name;
    int score;
    // 请在此补全：添加 <=> 运算符
};

int main() {
    vector<Student> students = {{"Alice", 85}, {"Bob", 42}, {"Charlie", 91}, {"Dave", 58}};
    // 请在此补全：用 ranges 过滤 score >= 60 的学生
    // 请在此补全：用 format 输出结果
    return 0;
}
```

---

## 第十五部分：知识蒸馏

> C++11/17/20 让 C++ 写得更短、更安全、更快：auto 省打字，move 省拷贝，智能指针省心智，lambda 省类，optional 省空指针检查，ranges 省迭代器，模块省头文件。

---

## 第十六部分：错题记录

| 题号 | 题目 | 我的错误答案 | 正确答案 | 错误原因 | 涉及知识点 | 复习建议 |
|------|------|-------------|----------|----------|-----------|----------|
| （待填写） | | | | | | 建议1天后复习 |
| （待填写） | | | | | | 建议3天后复习 |
| （待填写） | | | | | | 建议7天后复习 |

> 注：错题记录在完成练习题并批改后填写。

---

## 第十七部分：术语中英对照表

| 中文 | 英文 | 备注 |
|------|------|------|
| 自动类型推导 | Automatic Type Deduction | auto |
| 类型查询 | Type Query | decltype |
| 右值引用 | Rvalue Reference | && |
| 移动语义 | Move Semantics | std::move |
| 列表初始化 | List Initialization | {} |
| 范围for | Range-based For Loop | for(auto x : c) |
| Lambda表达式 | Lambda Expression | Anonymous Function Object |
| 捕获列表 | Capture List | [] |
| 仿函数 | Functor / Function Object | operator() |
| 智能指针 | Smart Pointer | RAII |
| 共享指针 | Shared Pointer | shared_ptr |
| 独占指针 | Unique Pointer | unique_ptr |
| 弱指针 | Weak Pointer | weak_ptr |
| 引用计数 | Reference Count | use_count() |
| 可变参数模板 | Variadic Template | template<class...T> |
| 参数包 | Parameter Pack | T... args |
| 折叠表达式 | Fold Expression | (... op args) |
| 类模板参数推导 | Class Template Argument Deduction | CTAD |
| 编译期if | Constexpr If | if constexpr |
| 结构化绑定 | Structured Bindings | auto [a,b] = ... |
| 可选类型 | Optional | std::optional |
| 变体类型 | Variant | std::variant |
| 字符串视图 | String View | std::string_view |
| 文件系统 | Filesystem | std::filesystem |
| 模块 | Modules | export/import |
| 协程 | Coroutines | co_yield/co_await |
| 三向比较 | Three-way Comparison | <=> |
| 范围/视图 | Ranges/Views | std::ranges |
| 跨度 | Span | std::span |
| 格式化 | Format | std::format |
| 承诺/未来 | Promise/Future | std::promise/std::future |
| 连接线程 | Joining Thread | std::jthread |

---

## 附录：C++11/17/20 各版本特性一张图速记

### C++11 最重要的5个特性
1. **auto/decltype**：类型推导基石，所有后续特性的基础
2. **移动语义**：性能革命，消除不必要的拷贝
3. **Lambda**：函数式编程入门，STL 算法最佳搭档
4. **智能指针**：RAII 内存管理标准化，告别手动 delete
5. **统一初始化**：花括号走遍天下

### C++17 最重要的5个特性
1. **结构化绑定**：解包神器，代码简洁度飞跃
2. **constexpr if**：模板元编程平民化
3. **optional/variant/any**：类型安全的"动态类型"三件套
4. **filesystem**：跨平台文件操作标准化
5. **string_view**：零拷贝字符串，性能优化利器

### C++20 最重要的5个特性
1. **Modules**：编译模型革新，告别头文件地狱
2. **Coroutines**：异步编程范式变革
3. **Ranges**：STL 算法现代化，管道式组合
4. **Concepts**：模板约束标准化（补充知识点）
5. **<=>**：比较运算符大一统

---

## 附录：面试常见问法及回答思路

**Q：auto 和 decltype 的区别？**
A：auto 从初始化表达式推导变量类型（必须有初始值），decltype 查询任意表达式类型但不求值。auto 用于简化声明，decltype 用于泛型返回值推导。

**Q：移动语义的本质是什么？**
A：本质是将资源的所有权从一个对象转移到另一个对象，避免深拷贝。std::move 只是类型转换（将左值转为右值引用），真正的"移动"发生在移动构造/赋值函数中。

**Q：shared_ptr 的线程安全性？**
A：引用计数的增减是原子操作（多线程安全），但对所指向对象的访问不是线程安全的。多线程同时读写同一对象仍需 mutex。

**Q：C++20 协程和 Python 生成器的区别？**
A：C++20 协程是无栈协程，只提供底层机制不提供库，需自行实现 promise_type；Python 生成器是有栈的，语言层面直接支持 yield。C++ 更灵活但更复杂。

---

> **学习笔记生成完毕。** 本笔记覆盖提示词清单全部 43 个知识点，包含完整的14项结构。
