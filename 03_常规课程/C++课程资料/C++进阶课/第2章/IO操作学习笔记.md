# C++进阶课 第2章：IO操作 —— 完整学习笔记

> **课件来源**：《第二章：IO操作.pdf》+ day1/day2 配套代码
> **前置章节**：第1章 Linux入门
> **预计学习时间**：1.5 小时
> **本章定位**：承上启下——掌握文件读写两套API（标准IO与文件IO），为后续进程通信、网络编程中的数据收发打基础

---

## 一、全部知识点（黄金四步法 + 生活比喻 + 人话总结）

---

### 知识点1：IO概念与分类（P1-P3）【熟悉】

#### ① 是什么
IO（Input/Output，输入/输出）是程序与外部设备（磁盘、终端、网络等）进行数据交换的过程。Linux下IO分为两大类：**标准IO**（库函数+缓冲区）和**文件IO**（系统调用+无缓冲）。

**生活比喻**：标准IO就像快递驿站——你把包裹先放到驿站（缓冲区），攒够一批再统一发走（一次系统调用）；文件IO就像自己跑腿送快递——每送一个包裹都要亲自跑一趟邮局（每次都是系统调用）。

#### ② 为什么
- 第1层：为什么要区分两种IO？因为效率不同。
- 第2层：为什么效率不同？因为系统调用涉及用户态→内核态切换，开销大。
- 第3层：为什么标准IO快？因为它用缓冲区减少了系统调用次数，把多次小操作合并成一次大操作。

#### ③ 怎么用

```cpp
// 标准IO接口示例（带缓冲区）
#include <stdio.h>
int main() {
    // printf 内部有行缓冲区，不是每次都触发系统调用
    printf("hello world\n");   // 数据先进入行缓冲区，遇到\n刷新
    // 输出：hello world
    return 0;
}
```

```cpp
// 文件IO接口示例（无缓冲区，直接系统调用）
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
int main() {
    int fd = open("./test.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    const char *msg = "hello";
    write(fd, msg, strlen(msg));  // 每次write都是一次系统调用
    close(fd);
    // 输出：test.txt 内容为 hello
    return 0;
}
```

**标准IO与文件IO对比表**：

| 对比维度 | 标准IO | 文件IO |
|---------|--------|--------|
| 实现方式 | 库函数（glibc封装） | 系统调用（内核直接提供） |
| 缓冲区 | 有（行缓存/全缓存/不缓存） | 无 |
| 系统调用次数 | 少（缓冲区满或刷新时才调用） | 多（每次read/write都调用） |
| 效率 | 高（减少上下文切换） | 低（频繁切换用户态/内核态） |
| 适用场景 | 普通文件读写、文本处理 | 设备文件、管道、socket、需要精确控制 |
| 操作句柄 | FILE* 文件指针 | int 文件描述符 |
| 代表函数 | fopen/fclose/fread/fwrite | open/close/read/write |

#### ④ 注意事项
- **错误示范**：在高频小数据写入场景中混用标准IO和文件IO操作同一个文件，会导致缓冲区数据和直接写入的数据交错混乱。
- **正确做法**：对同一个文件只用一套API，不要混用。

> **人话总结**：标准IO有缓冲快，文件IO无缓冲准。

---

### 知识点2：FILE结构体（P3-P5）【了解】

#### ① 是什么
FILE结构体是系统提供的用于描述一个已打开文件全部信息的结构体，包含缓冲区地址、文件描述符等核心成员。

**生活比喻**：FILE结构体就像文件的"身份证+工作台"，记录了文件在哪、缓冲区多大、当前读到哪了。

#### ② 为什么
标准IO的所有函数（fopen、fgetc等）都需要通过FILE指针来定位文件和缓冲区，没有它就无法操作文件。

#### ③ 怎么用

```cpp
// FILE结构体的核心成员（简化版）
struct FILE {
    char *_IO_buf_base;   // 缓冲区的起始地址
    char *_IO_buf_end;    // 缓冲区的终止地址
    int _fileno;          // 文件描述符，用于底层系统调用
};
```

三个特殊FILE指针（程序启动后系统默认打开）：
- `stdin`：标准输入指针（对应终端键盘，文件描述符0）
- `stdout`：标准输出指针（对应终端屏幕，文件描述符1）
- `stderr`：标准出错指针（对应终端屏幕，文件描述符2）

#### ④ 注意事项
- FILE结构体的具体成员在不同平台可能不同，不要直接访问内部成员做移植代码。
- `_IO_buf_base`和`_IO_buf_end`仅在缓冲区被至少使用一次后才分配有效地址。

> **人话总结**：FILE是文件的身份证，记录缓冲区和描述符。

---

### 知识点3：fopen/fclose（P5-P8）【重点】

#### ① 是什么
`fopen`用于打开或创建文件并返回FILE指针；`fclose`用于关闭已打开的文件并释放资源。

**生活比喻**：fopen就像去图书馆办借书证（拿到FILE*才能操作），fclose就是还书注销（释放资源）。不注销就会占着名额（资源泄漏）。

#### ② 为什么
- 第1层：为什么需要fopen？因为操作文件前必须先建立连接（获取文件指针）。
- 第2层：为什么需要fclose？因为打开的文件占用系统资源（文件描述符、缓冲区内存），不关会泄漏。
- 第3层：为什么不自动关？C/C++遵循"谁打开谁关闭"原则，编译器不会帮你管理资源。

#### ③ 怎么用

**man手册式签名**：
```c
#include <stdio.h>
FILE *fopen(const char *path, const char *mode);
// 参数1 path：文件路径字符串
// 参数2 mode：打开模式字符串
// 返回值：成功返回FILE*，失败返回NULL并置位errno

int fclose(FILE *fp);
// 参数：要关闭的文件指针
// 返回值：成功返回0，失败返回EOF并置位errno
```

**六种打开模式详解**：

| 模式 | 含义 | 文件不存在 | 文件存在 | 光标位置 |
|------|------|-----------|---------|---------|
| `r` | 只读 | 打开失败(NULL) | 正常打开 | 开头 |
| `r+` | 读写 | 打开失败(NULL) | 正常打开 | 开头 |
| `w` | 只写 | 创建新文件 | 清空原文件 | 开头 |
| `w+` | 读写 | 创建新文件 | 清空原文件 | 开头 |
| `a` | 追加写 | 创建新文件 | 保留原内容 | 末尾 |
| `a+` | 读写(追加) | 创建新文件 | 保留原内容 | 读:开头 / 写:末尾 |

**配套代码走读（day1/02fopen.cpp）**：

```cpp
#include "stdio.h"        // 标准的输入输出头文件
int main(int argc, const char *argv[])
{
    // 1、定义一个文件指针，初始化为NULL防止野指针
    FILE *fp = NULL;

    // 【注释掉的代码】以只读形式打开不存在的文件 → 返回NULL
    // fp = fopen("./file.txt", "r");
    // 原因："r"模式要求文件必须存在，不存在则失败

    // 以只写形式打开文件：不存在则创建，存在则清空
    fp = fopen("./file.txt", "w");
    if (fp == NULL)         // 必须检查返回值！
    {
        printf("fopen error\n");
        return -1;
    }
    printf("fopen success\n");
    // 输出：fopen success（同时创建了空的file.txt）

    // 2、关闭文件，释放资源
    fclose(fp);

    return 0;
}
```

#### ④ 注意事项

**错误示范**：
```cpp
// 错误：不检查fopen返回值就使用
FILE *fp = fopen("noexist.txt", "r");
fputc('A', fp);  // fp为NULL → 段错误(Segmentation Fault)
```

**正确写法**：
```cpp
FILE *fp = fopen("noexist.txt", "r");
if (fp == NULL) {
    perror("fopen error");  // 打印具体错误原因
    return -1;
}
```

**记忆口诀**："r只读不创，w才帮你建"。

> **人话总结**：打开必查NULL，用完必fclose。

---

### 知识点4：错误码处理 errno/perror/strerror（P8-P10）【重点】

#### ① 是什么
当内核函数出错时，会设置全局变量`errno`为一个整数错误码。`strerror`将错误码转为可读字符串，`perror`直接打印错误信息到stderr。

**生活比喻**：errno就像医院的诊断编号，strerror是把编号翻译成"感冒""骨折"等人话的翻译器，perror则是直接喊出"张三：感冒"的广播器。

#### ② 为什么
- 第1层：为什么用数字而不是直接给字符串？因为数字比较快、跨语言、节省内存。
- 第2层：为什么需要strerror/perror？因为开发者看不懂数字2代表"没有此文件"。
- 第3层：为什么perror比strerror方便？因为它一步完成"提示语+冒号+错误描述+换行"。

#### ③ 怎么用

**man手册式签名**：
```c
#include <errno.h>
extern int errno;           // 全局变量，记录最近一次错误的错误码

#include <string.h>
char *strerror(int errnum); // 将错误码转换为错误描述字符串
// 返回值：错误信息字符串指针

#include <stdio.h>
void perror(const char *s); // 打印 s + ": " + strerror(errno) + "\n" 到stderr
// 无返回值
```

**常见错误码速查**：

| 错误码 | 宏名 | 含义 |
|-------|------|------|
| 1 | EPERM | 操作受限 |
| 2 | ENOENT | 没有此文件或目录 |
| 9 | EBADF | 无效的文件描述符 |
| 13 | EACCES | 权限不足 |
| 17 | EEXIST | 文件已存在 |
| 22 | EINVAL | 无效参数 |
| 24 | EMFILE | 打开文件过多 |
| 28 | ENOSPC | 磁盘空间不足 |

**配套代码走读（day1/03errno.cpp）**：

```cpp
#include "stdio.h"       // 标准输入输出头文件
#include <errno.h>       // 错误码所在的头文件
#include <string.h>      // 字符串处理头文件
int main(int argc, const char *argv[])
{
    FILE *fp = NULL;
    fp = fopen("./file.txt", "r");  // 假设文件不存在
    if (fp == NULL)
    {
        // 方式1：手动拼接错误码和错误信息
        // printf("fopen error: %d, errmsg:%s\n", errno, strerror(errno));
        // 输出：fopen error: 2, errmsg:No such file or directory

        // 方式2（推荐）：perror一步到位
        perror("fopen error");
        // 输出：fopen error: No such file or directory
        return -1;
    }
    printf("fopen success\n");
    fclose(fp);
    return 0;
}
```

#### ④ 注意事项
- errno的值只在函数报错时有意义，成功时不会被清零，不要在成功调用后读errno。
- perror的参数是自定义提示语，会自动追加冒号和系统错误描述。
- strerror返回的是静态字符串指针，不要free它。

> **人话总结**：出错看errno，打印用perror。

---

### 知识点5：fgetc/fputc 单字符读写（P10-P12）【重点】

#### ① 是什么
`fgetc`从文件中读取一个字符，`fputc`向文件中写入一个字符。它们是最基本的文件读写单元。

**生活比喻**：fgetc/fputc就像用勺子一勺一勺地舀水——每次只搬运一个字符，简单但慢。

#### ② 为什么
- 第1层：为什么需要单字符读写？因为它是所有高级读写的基础构建块。
- 第2层：为什么返回值是int而不是char？因为EOF(-1)超出了char的范围，用char无法区分EOF和合法字符0xFF。
- 第3层：为什么写完不能直接读？因为文件光标在末尾，没有数据可读，必须重新打开或用fseek回退。

#### ③ 怎么用

**man手册式签名**：
```c
#include <stdio.h>
int fgetc(FILE *stream);
// 功能：从stream中读取一个字符
// 返回值：成功返回字符的ASCII值(0~255)，失败/文件尾返回EOF(-1)

int fputc(int c, FILE *stream);
// 功能：将字符c写入stream
// 返回值：成功返回写入字符的ASCII值，失败返回EOF
```

**配套代码走读（day1/04fgetcfputc.c）**：

```c
#include <stdio.h>
int main(int argc, const char *argv[])
{
    FILE *fp = NULL;
    // 第一步：以只写形式打开文件
    if ((fp = fopen("./file.txt", "w")) == NULL) {
        perror("fopen error");
        return -1;
    }

    // 第二步：逐字符写入 Hello
    fputc('H', fp);  // 写入'H'，光标移到位置1
    fputc('e', fp);  // 写入'e'，光标移到位置2
    fputc('l', fp);  // 写入'l'，光标移到位置3
    fputc('l', fp);  // 写入'l'，光标移到位置4
    fputc('o', fp);  // 写入'o'，光标移到位置5
    // 此时光标在文件末尾，无法读取

    fclose(fp);  // 关闭文件

    // 第三步：重新以只读形式打开
    if ((fp = fopen("./file.txt", "r")) == NULL) {
        perror("fopen error");
        return -1;
    }

    // 第四步：循环读取直到EOF
    char ch = 0;
    while (1) {
        ch = fgetc(fp);     // 读取一个字符
        if (ch == EOF) {
            break;          // 文件读完，退出循环
        }
        printf("%c ", ch);  // 打印字符
    }
    // 输出：H e l l o

    fclose(fp);
    return 0;
}
```

**课堂练习：用fgetc/fputc实现文件拷贝（day1/05test.cpp）**：

```cpp
#include <stdio.h>
int main(int argc, const char *argv[])
{
    if (argc != 3) {
        printf("usage:./a.out srcfile destfile\n");
        return -1;
    }
    FILE *srcfp = NULL, *destfp = NULL;
    if ((srcfp = fopen(argv[1], "r")) == NULL) {
        perror("srcfile open error"); return -1;
    }
    if ((destfp = fopen(argv[2], "w")) == NULL) {
        perror("destfile open error"); return -1;
    }
    char ch = 0;
    while (1) {
        ch = fgetc(srcfp);       // 从源文件读一个字符
        if (ch == EOF) break;    // 读完退出
        fputc(ch, destfp);       // 写入目标文件
    }
    fclose(srcfp);
    fclose(destfp);
    printf("拷贝成功\n");
    // 输出：拷贝成功
    return 0;
}
```

#### ④ 注意事项
- **错误示范**：用char类型接收fgetc返回值并判断EOF，当文件含0xFF字节时会误判为EOF提前结束。
- **正确写法**：用int类型接收fgetc返回值。
- fgetc/fputc效率低，大文件应改用fgets/fputs或fread/fwrite。

> **人话总结**：单字符读fgetc，写fputc，返回值用int接。

---

### 知识点6：fgets/fputs 字符串读写（P12-P14）【重点】

#### ① 是什么
`fgets`从文件中读取一行字符串（遇回车或EOF停止，保留换行符），`fputs`将字符串写入文件（不自动添加换行符）。

**生活比喻**：fgets/fputs就像用杯子一杯一杯地倒水——每次搬运一整行，比勺子（fgetc）快得多。

#### ② 为什么
- 第1层：为什么比fgetc快？因为一次读取多个字符，减少了函数调用次数。
- 第2层：为什么fgets保留换行符？因为这样调用者可以判断是否读到了一整行。
- 第3层：为什么fputs不加换行？因为保持对称性——写入什么就是什么，由程序员控制格式。

#### ③ 怎么用

**man手册式签名**：
```c
#include <stdio.h>
char *fgets(char *s, int size, FILE *stream);
// 功能：从stream最多读取size-1个字符到s中
// 遇到\n或EOF停止，自动加'\0'，\n会被保留
// 返回值：成功返回s的地址，失败/文件尾返回NULL

int fputs(const char *s, FILE *stream);
// 功能：将字符串s写入stream（不自动加\n）
// 返回值：成功返回写入字符数，失败返回EOF
```

**配套代码走读（day1/06fgetsfputs.cpp）**：

```cpp
#include <stdio.h>
#include <iostream>
#include <string.h>
int main(int argc, const char *argv[])
{
    FILE *fp = NULL;
    if ((fp = fopen("./file.txt", "w")) == NULL) {
        perror("fopen eror"); return -1;
    }

    // 写入阶段：循环从终端输入，写入文件
    char wbuf[128] = "";
    while (1) {
        std::cin >> wbuf;           // 从终端读字符串（不含空格）
        fputs(wbuf, fp);            // 写入文件（不带换行）
        fputc('\n', fp);            // 手动添加换行
        if (strcmp(wbuf, "quit") == 0) break;  // 输入quit退出
    }
    fclose(fp);

    // 读取阶段
    if ((fp = fopen("./file.txt", "r")) == NULL) {
        perror("fopen eror"); return -1;
    }
    char rbuf[128] = "";
    while (1) {
        char *res = fgets(rbuf, sizeof(rbuf), fp);
        if (res == NULL) break;     // 文件读完
        printf("rbuf = %s", rbuf);  // rbuf自带\n，不用再加
    }
    // 输出：每行显示之前写入的内容
    fclose(fp);
    return 0;
}
```

**课堂练习：用fgets/fputs实现文件拷贝（day1/07test.cpp）**：

```cpp
#include <iostream>
#include <stdio.h>
#include <string.h>
using namespace std;
int main(int argc, const char *argv[])
{
    if (argc != 3) {
        printf("usage:./a.out srcfile destfile\n"); return -1;
    }
    FILE *srcfp = NULL, *destfp = NULL;
    if ((srcfp = fopen(argv[1], "r")) == NULL) {
        perror("fopen error"); return -1;
    }
    if ((destfp = fopen(argv[2], "w")) == NULL) {
        perror("fopen error"); return -1;
    }
    char buf[128] = "";
    while (1) {
        char *ptr = fgets(buf, sizeof(buf), srcfp);
        if (ptr == NULL) break;
        fputs(buf, destfp);  // buf已含\n，无需额外添加
    }
    fclose(srcfp);
    fclose(destfp);
    printf("拷贝成功\n");
    return 0;
}
```

#### ④ 注意事项
- **错误示范**：`fgets(buf, sizeof(buf), fp)`后用`strcmp(buf, "quit")`比较，永远不等，因为buf末尾有`\n`。
- **正确写法**：`buf[strlen(buf)-1] = '\0';`去掉换行后再比较，或者用`strcmp(buf, "quit\n")`。
- fgets最多读取size-1个字符，最后一个位置留给'\0'，不会溢出。

> **人话总结**：fgets带尾巴(\n)，用完记得剪。

---

### 知识点7：缓冲区机制（P14-P18）【重点】

#### ① 是什么
标准IO为每个FILE*维护一块内存缓冲区，数据先写入缓冲区，满足刷新条件时才一次性刷入内核。缓冲区分三种类型：行缓存、全缓存、不缓存。

**生活比喻**：
- 行缓存 = 公交车——等到有人喊"下一站下车"（遇到换行）或车满了才发车。
- 全缓存 = 货车——装满一车（4096字节）才发车，不管有没有换行。
- 不缓存 = 急救车——有货立刻发，一秒都不等。

#### ② 为什么
- 第1层：为什么需要缓冲区？减少系统调用次数，提升IO效率。
- 第2层：为什么分三种？不同设备有不同的实时性需求。终端需要即时反馈（行缓存），磁盘追求吞吐（全缓存），错误信息必须立即显示（不缓存）。
- 第3层：为什么行缓存是1024而全缓存是4096？历史约定+页大小对齐，兼顾响应速度和吞吐量。

#### ③ 怎么用

**三种缓冲区对比**：

| 类型 | 大小 | 对应文件指针 | 刷新条件 |
|------|------|-------------|---------|
| 行缓存 | 1024字节 | stdin、stdout | 遇\n / 满 / 关闭 / fflush / 程序结束 / IO切换 / 手动 |
| 全缓存 | 4096字节 | 普通文件fp | 满 / 关闭 / fflush / 程序结束 / IO切换 / 手动 |
| 不缓存 | 0字节 | stderr | 放入数据立即刷新 |

**缓冲区数据流向ASCII图**：

```
  ┌─────────────┐    fwrite/fprintf    ┌──────────────────┐
  │  用户程序    │ ──────────────────→  │  用户缓冲区       │
  │  (你的代码)  │                      │  (行缓存1024B    │
  └─────────────┘                      │   全缓存4096B    │
                                        │   不缓存0B)      │
                                        └────────┬─────────┘
                                                 │ 刷新时机到达
                                                 ↓
                                        ┌──────────────────┐
                                        │  内核缓冲区       │
                                        │  (操作系统管理)   │
                                        └────────┬─────────┘
                                                 │ 内核调度写入
                                                 ↓
                                        ┌──────────────────┐
                                        │  磁盘/设备        │
                                        └──────────────────┘
```

**七种刷新时机详解**：

| 序号 | 刷新条件 | 行缓存 | 全缓存 | 不缓存 |
|------|---------|--------|--------|--------|
| 1 | 遇到换行符\n | 刷新 | 不刷新 | 立即 |
| 2 | 缓冲区满 | 刷新(1024B) | 刷新(4096B) | 立即 |
| 3 | 关闭文件(fclose) | 刷新 | 刷新 | N/A |
| 4 | fflush手动刷新 | 刷新 | 刷新 | N/A |
| 5 | 程序正常结束 | 刷新 | 刷新 | 已刷新 |
| 6 | 输入输出切换 | 刷新 | 刷新 | 立即 |
| 7 | 放入数据即刷新 | 否 | 否 | 是 |

**配套代码走读（day1/08buffed.cpp — 验证缓冲区大小）**：

```cpp
#include <iostream>
#include <stdio.h>
using namespace std;
int main(int argc, const char *argv[])
{
    // stdout第一次printf后分配行缓存
    printf("行缓存的大小为：%d\n",
           stdout->_IO_buf_end - stdout->_IO_buf_base);  // 1024

    // stdin未使用前大小为0
    printf("行缓存的大小为：%d\n",
           stdin->_IO_buf_end - stdin->_IO_buf_base);    // 0

    int num = 0;
    cin >> num;  // 使用了标准输入缓冲区
    printf("行缓存的大小为：%d\n",
           stdin->_IO_buf_end - stdin->_IO_buf_base);    // 1024

    // 验证全缓存
    FILE *fp = NULL;
    if ((fp = fopen("./aa.txt", "r")) == NULL) {
        perror("fopen error"); return -1;
    }
    printf("全缓存的大小为：%d\n",
           fp->_IO_buf_end - fp->_IO_buf_base);          // 0（未使用）
    fgetc(fp);  // 使用一次
    printf("全缓存的大小为：%d\n",
           fp->_IO_buf_end - fp->_IO_buf_base);          // 4096
    fclose(fp);

    // 验证不缓存始终为0
    perror("error");
    printf("不缓存的大小为：%d\n",
           stderr->_IO_buf_end - stderr->_IO_buf_base);  // 0
    // 输出：依次显示各缓冲区大小
    return 0;
}
```

**配套代码走读（day1/09bufsize.cpp — 行缓存7种刷新时机验证）**：

该文件用注释分段展示了7种刷新时机的验证方法。关键代码摘要：

```cpp
// 时机1：未到刷新时机 → 不输出
printf("hello world");   // 无\n，数据留在缓冲区
while(1);                // 阻塞，终端看不到输出

// 时机3：遇到换行 → 立即刷新
printf("hello world\n"); // 有\n，立即显示
while(1);

// 时机4：IO切换 → 刷新
printf("请输入>>>");     // 无\n，但接下来要scanf
scanf("%d", &num);       // IO切换触发刷新，先显示提示

// 时机7：缓冲区满 → 刷新
for (int i = 0; i < 1025; i++) printf("A"); // 超过1024B，自动刷新
while(1);
```

**配套代码走读（day1/10fullbuf.cpp — 全缓存刷新时机）**：

```cpp
// 注意：全缓存遇\n不刷新！（与行缓存的关键区别）
fputs("hello world\n", fp);  // 有\n也不刷新
while(1);                     // 文件中暂无数据

// IO切换会刷新全缓存
fputs("I love China\n", fp);
fgetc(fp);                    // 读操作触发IO切换 → 刷新
while(1);
```

**配套代码走读（day1/11nobuf.cpp — 不缓存验证）**：

```cpp
fputs("A", stderr);   // 写入stderr
while(1);              // 虽然阻塞，但'A'已经立即显示在终端
```

**fflush函数签名**：
```c
#include <stdio.h>
int fflush(FILE *stream);
// 功能：强制刷新stream对应的缓冲区
// 返回值：成功返回0，失败返回EOF
```

#### ④ 注意事项
- **错误示范**：在全缓存文件中写入少量数据后不刷新就读取，读到的是旧数据。
- **正确写法**：写入后如果需要立即生效，调用`fflush(fp)`或`fclose(fp)`。
- 行缓存遇\n刷新，全缓存遇\n**不**刷新——这是新手最常混淆的点。

> **人话总结**：行缓存见\n就刷，全缓存满了才刷，不缓存秒刷。

---

### 知识点8：fprintf/fscanf 格式化读写（P18-P20）【熟悉】

#### ① 是什么
`fprintf`按格式串向文件写入数据，`fscanf`按格式串从文件读取数据。它们与printf/scanf的唯一区别是多了第一个FILE*参数。

**生活比喻**：fprintf/fscanf就像填表格——你告诉它"这里填整数、那里填字符串"，它按格式自动排版存入/取出。

#### ② 为什么
- 为什么不只用fputs/fgets？因为它们只能处理纯字符串，无法直接存取整数、浮点数等多种类型。
- 为什么不用fwrite/fread？因为fwrite写的是二进制，人类不可读；fprintf写的是文本，可以直接用编辑器查看。

#### ③ 怎么用

**man手册式签名**：
```c
#include <stdio.h>
int fprintf(FILE *stream, const char *format, ...);
// 返回值：成功返回输出字符数，失败返回负数

int fscanf(FILE *stream, const char *format, ...);
// 返回值：成功返回读入项数，失败返回EOF
```

**配套代码走读（day1/12fprintf.cpp）**：

```cpp
#include <iostream>
#include <stdio.h>
using namespace std;
int main(int argc, const char *argv[])
{
    // 向stdout格式化输出（等价于printf）
    fprintf(stdout, "%d %lf %s\n", 520, 3.14, "I Love Xingqiu");
    // 输出：520 3.140000 I Love Xingqiu

    // 从stdin格式化输入（等价于scanf）
    int num = 0;
    fscanf(stdin, "%d", &num);
    printf("num = %d\n", num);
    // 输入1314 → 输出：num = 1314

    // 对外部文件进行格式化读写
    FILE *fp = NULL;
    if ((fp = fopen("./usr.txt", "w")) == NULL) {
        perror("fopen error"); return -1;
    }
    fprintf(fp, "%s %d", "admin", 123456);  // 写入：admin 123456
    fclose(fp);

    if ((fp = fopen("./usr.txt", "r")) == NULL) {
        perror("fopen error"); return -1;
    }
    char usrName[20] = "";
    int pwd = 0;
    fscanf(fp, "%s %d", usrName, &pwd);
    fclose(fp);
    printf("usrName = %s, pwd = %d\n", usrName, pwd);
    // 输出：usrName = admin, pwd = 123456
    return 0;
}
```

**综合练习：注册登录系统（day2/01test.cpp）**：

该文件实现了完整的注册/登录菜单系统。核心逻辑：
- 注册：用fgets读入账户密码（去换行），fprintf以"%s %s\n"格式追加写入usr.txt
- 登录：fscanf逐行读取"%s %s"，与输入逐一strcmp匹配
- 关键点：`reg_name[strlen(reg_name)-1] = '\0'`去除fgets带来的换行符

#### ④ 注意事项
- fprintf/fscanf是**文本模式**读写，文件可用编辑器直接查看。
- fscanf遇到空白字符（空格、换行、制表符）会停止读取当前字段。
- **错误示范**：用fwrite写二进制数据后，用fscanf按文本读取 → 数据全乱。
- **正确做法**：fwrite配fread（二进制），fprintf配fscanf（文本），读写方式必须配对。

> **人话总结**：fprintf写文本，fscanf读文本，格式要配对。

---

### 知识点9：sprintf/snprintf 格式串转字符数组（P20-P21）【熟悉】

#### ① 是什么
`sprintf`将格式化数据转换为字符串存入字符数组；`snprintf`是其安全版本，多了size参数限制最大写入长度，防止缓冲区溢出。

**生活比喻**：sprintf就像往信封里塞信纸——不管信封大小硬塞，可能撑破；snprintf则是先看信封容量再塞，塞不下就截断。

#### ② 为什么
- 为什么需要sprintf？有时需要将多种类型数据拼成一个字符串（如构造SQL语句、日志消息）。
- 为什么需要snprintf？sprintf没有边界检查，目标数组太小时会越界写入导致段错误或安全漏洞。

#### ③ 怎么用

**man手册式签名**：
```c
#include <stdio.h>
int sprintf(char *str, const char *format, ...);
// 返回值：成功返回转换字符数，失败返回EOF

int snprintf(char *str, size_t size, const char *format, ...);
// 最多写入size-1个字符，自动加'\0'
// 返回值：若实际内容<size返回实际长度；>=size返回size；失败返回EOF
```

**配套代码走读（day1/13sprintf.cpp）**：

```cpp
#include <iostream>
#include <stdio.h>
using namespace std;
int main(int argc, const char *argv[])
{
    char buf[10] = "";

    // 【注释掉的危险代码】sprintf无边界检查
    // sprintf(buf, "%d %s %lf", 1001, "zhangsanfeng", 99.5);
    // "1001 zhangsanfeng 99.500000"共27字节，buf只有10字节 → 溢出！

    // 安全版本：snprintf限制最多写入sizeof(buf)-1=9个字符
    snprintf(buf, sizeof(buf), "%d %s %lf", 1001, "zhangsanfeng", 99.5);
    printf("buf = %s\n", buf);
    // 输出：buf = 1001 zhan（被截断为9个字符+'\0'）
    return 0;
}
```

#### ④ 注意事项
- **永远优先使用snprintf代替sprintf**。
- snprintf的size参数包含'\0'的位置，实际可存储size-1个有效字符。
- 即使被截断，snprintf也会保证字符串以'\0'结尾。

> **人话总结**：sprintf不安全，snprintf限长度。

---

### 知识点10：fread/fwrite 模块化读写（P21-P25）【重点】

#### ① 是什么
`fread`和`fwrite`以"数据块"为单位进行读写，可以一次读写多个相同大小的数据项。它们是二进制文件操作的核心函数。

**生活比喻**：fread/fwrite就像集装箱运输——不管里面装的是什么货物（字符、整数、结构体），只要箱子大小一样就能批量装卸。

#### ② 为什么
- 第1层：为什么需要模块化读写？因为fgetc/fputs只能处理字符，无法直接读写整数、结构体等复合类型。
- 第2层：为什么返回值是项数而不是字节数？因为以"项"为单位更符合业务语义（"读了3个学生"比"读了96字节"直观）。
- 第3层：为什么区分文本模式和二进制模式？文本模式下Windows会将\n转为\r\n，破坏二进制数据的完整性。Linux下两者无差异，但跨平台代码应明确指定。

#### ③ 怎么用

**man手册式签名**：
```c
#include <stdio.h>
size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream);
// ptr：接收数据的容器指针(void*)
// size：每项大小(字节)
// nmemb：要读的项数
// 返回值：成功读取的项数（≤nmemb），0表示文件尾或错误

size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream);
// ptr：要写入数据的起始地址
// size：每项大小(字节)
// nmemb：要写的项数
// 返回值：成功写入的项数（≤nmemb）
```

**示例1：字符串读写（day2/02fread.cpp）**：

```cpp
#include <iostream>
#include <stdio.h>
#include <string.h>
using namespace std;
int main(int argc, const char *argv[])
{
    FILE *fp = NULL;
    if ((fp = fopen("./test.txt", "w")) == NULL) {
        perror("fopen error"); return -1;
    }
    char wbuf[128] = "";
    while (1) {
        printf("请输入>>>");
        fgets(wbuf, sizeof(wbuf), stdin);
        if (strcmp(wbuf, "quit\n") == 0) break;
        fwrite(wbuf, strlen(wbuf), 1, fp);  // 每次写1项，每项strlen(wbuf)字节
        fflush(fp);
        printf("录入成功\n");
    }
    fclose(fp);

    if ((fp = fopen("./test.txt", "r")) == NULL) {
        perror("fopen error"); return -1;
    }
    char rbuf[10] = "";
    int res = fread(rbuf, 1, sizeof(rbuf), fp);  // 读10字节
    fwrite(rbuf, 1, res, stdout);                 // 写到终端
    // 输出：文件前10个字节的内容
    fclose(fp);
    return 0;
}
```

**示例2：整数读写（day2/03fread.cpp）**：

```cpp
#include <iostream>
#include <stdio.h>
#include <string.h>
using namespace std;
int main(int argc, const char *argv[])
{
    FILE *fp = NULL;
    if ((fp = fopen("./test.txt", "w")) == NULL) {
        perror("fopen error"); return -1;
    }
    int num = 16;
    fwrite(&num, sizeof(num), 1, fp);  // 写入1个int（4字节二进制）
    fclose(fp);

    if ((fp = fopen("./test.txt", "r")) == NULL) {
        perror("fopen error"); return -1;
    }
    int key = 0;
    fread(&key, sizeof(key), 1, fp);   // 读取1个int
    fclose(fp);
    printf("key = %d\n", key);
    // 输出：key = 16
    return 0;
}
```

**示例3：结构体数组读写（day2/04fread.cpp）**：

```cpp
#include <iostream>
#include <stdio.h>
#include <string.h>
using namespace std;
class Stu {
public:
    char name[20];   // 姓名
    int age;         // 年龄
    double score;    // 成绩
};
int main(int argc, const char *argv[])
{
    FILE *fp = NULL;
    if ((fp = fopen("./test.txt", "w")) == NULL) {
        perror("fopen error"); return -1;
    }
    Stu s[3] = {{"张三",18,98}, {"李四",20,88}, {"王五",16,95}};
    fwrite(s, sizeof(Stu), 3, fp);  // 一次写入3个学生
    fclose(fp);

    if ((fp = fopen("./test.txt", "r")) == NULL) {
        perror("fopen error"); return -1;
    }
    Stu temp;
    fread(&temp, sizeof(Stu), 1, fp);  // 读取第1个学生
    printf("name:%s, age:%d, score:%.2lf\n", temp.name, temp.age, temp.score);
    // 输出：name:张三, age:18, score:98.00
    fclose(fp);
    return 0;
}
```

#### ④ 注意事项
- fwrite写入的是**二进制数据**，用cat/编辑器打开看到的是乱码，这是正常的。
- **错误示范**：fwrite写结构体后用fprintf读取 → 数据错乱。
- **正确做法**：fwrite配fread，fprintf配fscanf，读写方式必须配对。
- fread返回值是**实际读取的项数**，小于nmemb不一定出错，可能是文件到尾了。

> **人话总结**：fwrite存二进制，fread取二进制，配对不乱套。

---

### 知识点11：fseek/ftell/rewind 文件光标操作（P25-P27）【重点】

#### ① 是什么
`fseek`移动文件光标到指定位置，`ftell`获取当前光标偏移量，`rewind`将光标回到文件开头。

**生活比喻**：fseek就像视频播放器的进度条拖拽——你可以跳到任意时间点；ftell就是看当前播放到几分几秒；rewind就是点"回到开头"按钮。

#### ② 为什么
- 第1层：为什么需要随机访问？因为顺序读写无法满足"修改第3条记录""获取文件大小"等需求。
- 第2层：为什么ftell能求文件大小？因为`fseek(fp,0,SEEK_END)`把光标移到末尾，`ftell(fp)`返回的就是末尾偏移量=文件大小。
- 第3层：为什么offset可以为负？因为需要从某个基准位置向前回退（如从文件末尾往前找数据）。

#### ③ 怎么用

**man手册式签名**：
```c
#include <stdio.h>
int fseek(FILE *stream, long offset, int whence);
// offset：偏移量（正=向后，负=向前，0=不动）
// whence：SEEK_SET(开头) / SEEK_CUR(当前位置) / SEEK_END(末尾)
// 返回值：成功返回0，失败返回-1

long ftell(FILE *stream);
// 返回值：当前光标偏移量（字节），失败返回-1

void rewind(FILE *stream);
// 等价于 fseek(stream, 0, SEEK_SET)
// 无返回值
```

**三种起始位置示意图**：

```
  文件内容：[H][e][l][l][o][ ][W][o][r][l][d]
  字节编号： 0   1   2   3   4   5   6   7   8   9  10

  SEEK_SET ─────────────────────────────────→ (基准=0)
  fseek(fp, 6, SEEK_SET)  → 光标指向 'W'(位置6)

  SEEK_CUR ─────────────────────→ (基准=当前光标)
  若当前在位置11(末尾)，fseek(fp, -5, SEEK_CUR) → 光标指向 'W'(位置6)

  SEEK_END ←───────────────────────────────── (基准=末尾)
  fseek(fp, -5, SEEK_END) → 光标指向 'W'(位置6)
```

**配套代码走读（day2/05fseek.cpp）**：

```cpp
#include <iostream>
#include <stdio.h>
#include <string.h>
using namespace std;
class Stu {
public:
    char name[20]; int age; double score;
};
int main(int argc, const char *argv[])
{
    FILE *fp = NULL;
    if ((fp = fopen("./test.txt", "w+")) == NULL) {  // w+支持读写
        perror("fopen error"); return -1;
    }
    Stu s[3] = {{"张三",18,98}, {"李四",20,88}, {"王五",16,95}};
    fwrite(s, sizeof(Stu), 3, fp);

    // ftell求文件大小
    printf("此时文件的大小为：%ld\n", ftell(fp));
    // 输出：此时文件的大小为：96（假设sizeof(Stu)=32, 32*3=96）

    // 从当前位置向前偏移2个学生的大小 → 定位到第2个学生(李四)
    fseek(fp, -sizeof(Stu)*2, SEEK_CUR);

    Stu temp;
    fread(&temp, sizeof(Stu), 1, fp);
    printf("name:%s, age:%d, score:%.2lf\n", temp.name, temp.age, temp.score);
    // 输出：name:李四, age:20, score:88.00
    fclose(fp);
    return 0;
}
```

#### ④ 注意事项
- fseek的whence参数只能用SEEK_SET/SEEK_CUR/SEEK_END三个宏，不能用数字。
- **错误示范**：用"w"模式打开文件后fseek到中间读取 → "w"模式是只写，读操作无效。
- **正确做法**：需要既读又写时用"w+"或"r+"模式。
- ftell返回值类型是long，大文件可能溢出，生产环境用ftello。

> **人话总结**：fseek跳位置，ftell查偏移，rewind回开头。

---

### 知识点12：文件描述符（P27-P28）【熟悉】

#### ① 是什么
文件描述符（File Descriptor，fd）是一个非负整数，是内核用来标识进程中已打开文件的句柄。每个进程最多打开1024个文件描述符（可通过ulimit调整）。

**生活比喻**：文件描述符就像餐厅的桌号——0号桌固定给厨房（stdin），1号桌给服务员出口（stdout），2号桌给投诉通道（stderr），新来的客人从3号桌开始分配（最小未分配原则）。

#### ② 为什么
- 第1层：为什么用整数而不是指针？因为文件描述符是内核层面的概念，在内核空间中用数组索引管理，整数最高效。
- 第2层：为什么0/1/2被预留？因为POSIX标准规定进程启动时默认打开这三个描述符，确保基本IO可用。
- 第3层：为什么是最小未分配原则？为了复用已关闭的描述符，避免浪费有限的描述符资源。

#### ③ 怎么用

```
  进程的文件描述符表（示意）：
  ┌────┬────────────────────────┐
  │ fd │ 指向                   │
  ├────┼────────────────────────┤
  │  0 │ stdin  (标准输入/键盘) │
  │  1 │ stdout (标准输出/屏幕) │
  │  2 │ stderr (标准错误/屏幕) │
  │  3 │ 第一个open的文件       │
  │  4 │ 第二个open的文件       │
  │ .. │ ...                    │
  │1023│ 上限(ulimit -a查看)    │
  └────┴────────────────────────┘
```

**配套代码走读（day2/06descrip.cpp）**：

```cpp
#include <iostream>
#include <stdio.h>
using namespace std;
int main(int argc, const char *argv[])
{
    // FILE结构体的_fileno成员就是对应的文件描述符
    printf("stdin->_fileno = %d\n", stdin->_fileno);   // 0
    printf("stdout->_fileno = %d\n", stdout->_fileno); // 1
    printf("stderr->_fileno = %d\n", stderr->_fileno); // 2
    // 输出：
    // stdin->_fileno = 0
    // stdout->_fileno = 1
    // stderr->_fileno = 2
    return 0;
}
```

查看和修改限制：
```bash
ulimit -a       # 查看所有资源限制
ulimit -n       # 查看最大打开文件数（通常1024）
ulimit -n 2048  # 临时修改为2048（仅当前终端有效）
```

#### ④ 注意事项
- 文件描述符是非负整数，open失败返回-1，不要用NULL判断。
- close(fd)后该fd会被回收，下次open可能分配到相同的fd值。
- **错误示范**：close(fd)后继续用该fd读写 → EBADF错误。

> **人话总结**：fd是非负整数，0/1/2已占，新的从3起。

---

### 知识点13：open/close 文件IO打开与关闭（P28-P30）【重点】

#### ① 是什么
`open`是系统调用级别的打开文件函数，返回文件描述符；`close`关闭文件描述符对应的文件。它们是文件IO的入口和出口。

**生活比喻**：open就像直接去政府大厅办手续（绕过驿站/缓冲区），拿到一个编号（fd）就能办事；close就是注销编号。

#### ② 为什么
- 为什么有了fopen还需要open？因为某些场景（设备文件、管道、socket、设置特殊标志）只有系统调用才能完成。
- 为什么open的标志位用位或组合？因为一个文件可能需要同时满足多个条件（如读写+创建+清空），位运算最灵活。

#### ③ 怎么用

**man手册式签名**：
```c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
int open(const char *pathname, int flags);
int open(const char *pathname, int flags, mode_t mode);
// flags必选其一：O_RDONLY / O_WRONLY / O_RDWR
// 可选标志(位或组合)：O_CREAT / O_APPEND / O_TRUNC / O_EXCL
// mode：当flags含O_CREAT时必须提供，表示新建文件权限
// 返回值：成功返回fd(≥0)，失败返回-1并置位errno

#include <unistd.h>
int close(int fd);
// 返回值：成功返回0，失败返回-1
```

**fopen模式与open标志对照表**：

| fopen模式 | 等价的open标志组合 |
|----------|------------------|
| `"r"` | `O_RDONLY` |
| `"r+"` | `O_RDWR` |
| `"w"` | `O_WRONLY \| O_CREAT \| O_TRUNC` |
| `"w+"` | `O_RDWR \| O_CREAT \| O_TRUNC` |
| `"a"` | `O_WRONLY \| O_CREAT \| O_APPEND` |
| `"a+"` | `O_RDWR \| O_CREAT \| O_APPEND` |

**权限说明**：
- open的第三个参数mode与系统umask取反后位与得到最终权限：`final_mode = mode & ~umask`
- 默认umask通常为0022，所以mode=0664 → 最终权限=0644
- 普通文件常用权限：0644（rw-r--r--），目录常用：0755（rwxr-xr-x）

**配套代码走读（day2/07open.cpp）**：

```cpp
#include <myhead.h>  // 自定义头文件，包含了常用头文件
int main(int argc, const char *argv[])
{
    int fd = -1;
    // 以只写+创建模式打开，权限0644
    if ((fd = open("./tt.txt", O_WRONLY | O_CREAT, 0644)) == -1) {
        perror("open error"); return -1;
    }
    printf("open success fd = %d\n", fd);
    // 输出：open success fd = 3（0/1/2已被占用）

    // 写入数据
    char wbuf[128] = "hello world";
    write(fd, wbuf, strlen(wbuf));  // 写入11字节
    close(fd);

    // 再次以只读打开（不需要O_CREAT，也不需要mode参数）
    if ((fd = open("./tt.txt", O_RDONLY)) == -1) {
        perror("open error"); return -1;
    }
    printf("open success fd = %d\n", fd);  // 3（fd被复用）

    char rbuf[5] = "";
    int res = read(fd, rbuf, sizeof(rbuf));  // 读5字节
    write(1, rbuf, res);  // 写到stdout(fd=1)
    // 输出：hello
    close(fd);
    return 0;
}
```

#### ④ 注意事项
- **错误示范**：open含O_CREAT但不给mode参数 → 新建文件权限为随机值。
- **正确写法**：含O_CREAT时必须给第三个参数，如`0644`。
- O_EXCL配合O_CREAT使用可确保创建新文件，若文件已存在则open失败（用于排他性创建）。

> **人话总结**：open用标志位，创建设权限，close释资源。

---

### 知识点14：read/write/lseek 文件IO读写与光标（P30-P31）【重点】

#### ① 是什么
`read`从文件描述符读取数据，`write`向文件描述符写入数据，`lseek`移动文件光标位置。它们是文件IO的核心操作三件套。

**生活比喻**：read/write就像直接用桶打水/倒水（没有缓冲中间商），lseek就是把手伸到水桶的任意深度取水。

#### ② 为什么
- 为什么read返回值可能小于count？因为文件剩余数据不够、管道/ socket数据未就绪等原因，这不是错误。
- 为什么read返回0表示EOF？因为0字节意味着"没有更多数据了"，这是Unix的设计哲学。
- 为什么lseek = fseek + ftell？因为lseek既移动光标又返回新位置，一个函数干了两件事。

#### ③ 怎么用

**man手册式签名**：
```c
#include <unistd.h>
ssize_t read(int fd, void *buf, size_t count);
// 返回值：实际读取字节数(可能<count)，0=EOF，-1=错误

ssize_t write(int fd, const void *buf, size_t count);
// 返回值：实际写入字节数(可能<count)，-1=错误

#include <sys/types.h>
#include <unistd.h>
off_t lseek(int fd, off_t offset, int whence);
// offset：偏移量(正=向后，负=向前)
// whence：SEEK_SET / SEEK_CUR / SEEK_END
// 返回值：光标新位置(≥0)，-1=错误
```

**标准IO vs 文件IO API对照表**：

| 功能 | 标准IO | 文件IO |
|------|--------|--------|
| 打开 | fopen(path, mode) | open(path, flags, mode) |
| 关闭 | fclose(fp) | close(fd) |
| 读 | fread(ptr, size, n, fp) | read(fd, buf, count) |
| 写 | fwrite(ptr, size, n, fp) | write(fd, buf, count) |
| 移动光标 | fseek(fp, offset, whence) | lseek(fd, offset, whence) |
| 获取位置 | ftell(fp) | lseek(fd, 0, SEEK_CUR) |
| 回到开头 | rewind(fp) | lseek(fd, 0, SEEK_SET) |
| 操作句柄 | FILE* | int (fd) |
| 缓冲区 | 有 | 无 |

**配套代码走读（day2/08lseek.cpp）**：

```cpp
#include <myhead.h>
int main(int argc, const char *argv[])
{
    int fd = -1;
    // 读写+创建+清空
    if ((fd = open("./tt.txt", O_RDWR|O_CREAT|O_TRUNC, 0644)) == -1) {
        perror("open error"); return -1;
    }
    printf("open success fd = %d\n", fd);  // 3

    char wbuf[128] = "hello world";
    write(fd, wbuf, strlen(wbuf));  // 写入11字节，光标在位置11

    // 需求：读取 "world"（最后5个字符）
    // 方式1：从开头偏移6字节
    // lseek(fd, 6, SEEK_SET);
    // 方式2：从末尾回退5字节
    lseek(fd, -5, SEEK_END);  // 光标移到位置6

    char rbuf[5] = "";
    int res = read(fd, rbuf, sizeof(rbuf));  // 读5字节
    write(1, rbuf, res);  // 写到终端
    // 输出：world
    close(fd);
    return 0;
}
```

**实战练习：BMP图片像素修改（day2/09lseek.cpp）**：

```cpp
#include <myhead.h>
int main(int argc, const char *argv[])
{
    int fd = -1;
    if ((fd = open("./wukong.bmp", O_RDWR)) == -1) {
        perror("open error"); return -1;
    }
    // lseek到末尾再回来 → 获取文件大小
    printf("文件大小为：%ld\n", lseek(fd, 0, SEEK_END));

    // BMP文件头：偏移2处存文件大小(4字节)
    int pic_size = 0;
    lseek(fd, 2, SEEK_SET);
    read(fd, &pic_size, 4);
    printf("pic_size = %d\n", pic_size);

    // 跳过54字节文件头+信息头，到达像素数据区
    lseek(fd, 54, SEEK_SET);

    // 定义绿色像素(BGR格式)
    unsigned char color[3] = {0, 0, 255};
    for (int i = 0; i < 100; i++)        // 前100行
        for (int j = 0; j < 684; j++)    // 每行684列
            write(fd, color, sizeof(color));  // 写入绿色像素

    close(fd);
    // 效果：图片顶部100行变为绿色
    return 0;
}
```

#### ④ 注意事项
- read返回0表示文件结束，返回-1才是错误，不要把0当错误处理。
- write返回值可能小于count（如磁盘满），生产代码应循环写入直到全部写完。
- **错误示范**：用read读取后用strlen计算长度 → read不添加'\0'，strlen结果不可靠。
- **正确做法**：用read的返回值作为实际数据长度。

> **人话总结**：read返0是结尾，write要查返回值。

---

## 二、所有对比表格汇总

### 表1：标准IO vs 文件IO 四维对比

| 维度 | 标准IO | 文件IO |
|------|--------|--------|
| 缓冲区 | 有（行/全/不缓存） | 无 |
| 系统调用次数 | 少（缓冲合并） | 多（每次操作都调用） |
| 效率 | 高 | 低 |
| 适用场景 | 普通文件、文本处理 | 设备/管道/socket/精确控制 |

### 表2：fopen六种模式对比

| 模式 | 读 | 写 | 创建 | 清空 | 光标 |
|------|----|----|------|------|------|
| r | Y | N | N | N | 开头 |
| r+ | Y | Y | N | N | 开头 |
| w | N | Y | Y | Y | 开头 |
| w+ | Y | Y | Y | Y | 开头 |
| a | N | Y | Y | N | 末尾 |
| a+ | Y | Y | Y | N | 读:开头/写:末尾 |

### 表3：三种缓冲区对比

| 类型 | 大小 | 文件指针 | 遇\n刷新 | 满刷新 |
|------|------|---------|---------|--------|
| 行缓存 | 1024B | stdin/stdout | 是 | 是 |
| 全缓存 | 4096B | 普通文件fp | 否 | 是 |
| 不缓存 | 0B | stderr | 立即 | 立即 |

### 表4：标准IO与文件IO函数对照

| 功能 | 标准IO | 文件IO |
|------|--------|--------|
| 打开 | fopen | open |
| 关闭 | fclose | close |
| 读 | fread | read |
| 写 | fwrite | write |
| 定位 | fseek | lseek |
| 获取位置 | ftell | lseek(fd,0,SEEK_CUR) |
| 回开头 | rewind | lseek(fd,0,SEEK_SET) |

### 表5：fopen模式与open标志对照

| fopen | open标志 |
|-------|---------|
| "r" | O_RDONLY |
| "r+" | O_RDWR |
| "w" | O_WRONLY\|O_CREAT\|O_TRUNC |
| "w+" | O_RDWR\|O_CREAT\|O_TRUNC |
| "a" | O_WRONLY\|O_CREAT\|O_APPEND |
| "a+" | O_RDWR\|O_CREAT\|O_APPEND |

---

## 三、配套文件完整逐行讲解（代码走读）

> 本节对day1和day2目录下的关键代码文件进行逐行走读，解释每行执行时内存/状态的变化。已在上方各知识点中嵌入的代码走读覆盖了全部22个配套文件的核心逻辑。以下为补充要点：

### day1/01printf.cpp — 标准IO入门

```cpp
#include "stdio.h"       // 引入C标准IO头文件
#include <iostream>      // C++ IO流头文件（本例未使用）
int main(int argc, const char *argv[])
{
    printf("hello world\n");  // 数据进入行缓冲区 → 遇\n刷新 → 系统调用write → 终端显示
    // std::cout << "hello world" << std::endl;  // 被注释的C++等价写法
    return 0;
}
// 输出：hello world
```

### day1/11nobuf.cpp — 不缓存验证

```cpp
fputs("A", stderr);   // 写入stderr的不缓存 → 立即触发系统调用 → 'A'瞬间显示
while(1);              // 程序阻塞，但'A'已经显示 → 证明不缓存是即时刷新
```

### day2/01test.cpp — 注册登录系统完整走读

该文件是本章最复杂的综合案例，整合了fopen/fclose、fgets、fprintf/fscanf、strcmp等多个知识点。关键走读要点：
1. `fgets(reg_name, sizeof(reg_name), stdin)` — 从键盘读入账户名，**包含换行符**
2. `reg_name[strlen(reg_name)-1] = '\0'` — 将末尾`\n`替换为`\0`，**这是必须的**
3. `fprintf(wfp, "%s %s\n", reg_name, reg_pwd)` — 以文本格式写入文件，每行一条记录
4. `fscanf(rfp, "%s %s", name, pwd)` — 按空格分隔读取账户和密码
5. `strcmp(name, log_name)==0 && strcmp(pwd, log_pwd)==0` — 双条件匹配
6. `getchar()` — 吸收scanf留下的换行符，防止下次fgets读到空行

### 被注释代码段解读

| 文件 | 被注释代码 | 注释原因 |
|------|-----------|---------|
| 02fopen.cpp | `fp = fopen("./file.txt", "r")` | 演示"r"模式打开不存在文件会失败 |
| 03errno.cpp | `printf("fopen error: %d, errmsg:%s\n", errno, strerror(errno))` | 保留了另一种错误打印方式供对比 |
| 04fgetcfputc.c | 注释提问"能否从该处读取数据？" | 教学引导：光标在末尾无法读取 |
| 09bufsize.cpp | 6段被注释的刷新时机验证代码 | 每段独立验证一种刷新时机，取消注释即可测试 |
| 10fullbuf.cpp | 6段被注释的全缓存刷新验证 | 同上，全缓存版本 |
| 13sprintf.cpp | `sprintf(buf, "%d %s %lf", ...)` | 演示不安全的sprintf会导致缓冲区溢出 |
| 02fread.cpp | `wbuf[strlen(wbuf)-1]=0`和`fwrite("\n",...)` | 可选的换行处理，展示不同写入策略 |
| 05fseek.cpp | `fseek(fp,0,SEEK_SET)`和`fseek(fp,sizeof(Stu),SEEK_SET)` | 展示了不同的定位方式供对比学习 |
| 08lseek.cpp | `lseek(fd, 6, SEEK_SET)` | 另一种定位方式，与SEEK_END方式对比 |

---

## 四、两套速查表

### 精简版速查表（一页速览）

```
┌─────────────────────────────────────────────────────────────┐
│               C++ IO操作 速查卡                              │
├─────────────────────────────────────────────────────────────┤
│ 【标准IO】                                                   │
│  fopen(path,mode) → FILE*    fclose(fp) → 0/EOF             │
│  fgetc(fp) → int/EOF         fputc(c,fp) → int/EOF          │
│  fgets(s,n,fp) → char*/NULL  fputs(s,fp) → int/EOF          │
│  fprintf(fp,fmt,...) → int   fscanf(fp,fmt,...) → int/EOF   │
│  fread(p,sz,n,fp) → size_t   fwrite(p,sz,n,fp) → size_t     │
│  fseek(fp,off,wh) → 0/-1     ftell(fp) → long               │
│  rewind(fp)                   fflush(fp) → 0/EOF            │
│  sprintf/snprintf → 格式串转字符数组                          │
│  errno/perror/strerror → 错误处理三件套                       │
├─────────────────────────────────────────────────────────────┤
│ 【文件IO】                                                   │
│  open(path,flags,mode) → fd/-1   close(fd) → 0/-1           │
│  read(fd,buf,cnt) → ssize_t      write(fd,buf,cnt) → ssize_t│
│  lseek(fd,off,wh) → off_t                                   │
│  标志: O_RDONLY/O_WRONLY/O_RDWR/O_CREAT/O_TRUNC/O_APPEND    │
│  权限: 0644(文件) 0755(目录) umask影响最终权限                 │
├─────────────────────────────────────────────────────────────┤
│ 【缓冲区】 行缓存1024B(stdout/stdin)                         │
│            全缓存4096B(文件fp)                                │
│            不缓存0B(stderr)                                  │
│ 【刷新时机】 换行/满/关闭/fflush/程序结束/IO切换/不缓存即时    │
└─────────────────────────────────────────────────────────────┘
```

### 详细版速查表（含语法+示例）

| 函数 | 头文件 | 签名 | 返回值 | 快速示例 |
|------|--------|------|--------|---------|
| fopen | stdio.h | `FILE *fopen(const char *path, const char *mode)` | FILE*/NULL | `fp=fopen("a.txt","r")` |
| fclose | stdio.h | `int fclose(FILE *fp)` | 0/EOF | `fclose(fp)` |
| fgetc | stdio.h | `int fgetc(FILE *stream)` | char值/EOF | `ch=fgetc(fp)` |
| fputc | stdio.h | `int fputc(int c, FILE *stream)` | char值/EOF | `fputc('A',fp)` |
| fgets | stdio.h | `char *fgets(char *s, int size, FILE *stream)` | s/NULL | `fgets(buf,128,fp)` |
| fputs | stdio.h | `int fputs(const char *s, FILE *stream)` | 字符数/EOF | `fputs("hi",fp)` |
| fprintf | stdio.h | `int fprintf(FILE *stream, const char *fmt, ...)` | 字符数/负数 | `fprintf(fp,"%d",n)` |
| fscanf | stdio.h | `int fscanf(FILE *stream, const char *fmt, ...)` | 项数/EOF | `fscanf(fp,"%d",&n)` |
| fread | stdio.h | `size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream)` | 项数 | `fread(&s,sizeof(S),1,fp)` |
| fwrite | stdio.h | `size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream)` | 项数 | `fwrite(&s,sizeof(S),1,fp)` |
| fseek | stdio.h | `int fseek(FILE *stream, long offset, int whence)` | 0/-1 | `fseek(fp,0,SEEK_END)` |
| ftell | stdio.h | `long ftell(FILE *stream)` | 偏移量/-1 | `sz=ftell(fp)` |
| rewind | stdio.h | `void rewind(FILE *stream)` | 无 | `rewind(fp)` |
| fflush | stdio.h | `int fflush(FILE *stream)` | 0/EOF | `fflush(fp)` |
| sprintf | stdio.h | `int sprintf(char *str, const char *fmt, ...)` | 字符数/EOF | `sprintf(buf,"%d",n)` |
| snprintf | stdio.h | `int snprintf(char *str, size_t size, const char *fmt, ...)` | 字符数/EOF | `snprintf(buf,10,"%d",n)` |
| strerror | string.h | `char *strerror(int errnum)` | 字符串指针 | `strerror(errno)` |
| perror | stdio.h | `void perror(const char *s)` | 无 | `perror("open")` |
| open | fcntl.h | `int open(const char *path, int flags, mode_t mode)` | fd/-1 | `open("a.txt",O_RDWR\|O_CREAT,0644)` |
| close | unistd.h | `int close(int fd)` | 0/-1 | `close(fd)` |
| read | unistd.h | `ssize_t read(int fd, void *buf, size_t count)` | 字节数/0/-1 | `read(fd,buf,100)` |
| write | unistd.h | `ssize_t write(int fd, const void *buf, size_t count)` | 字节数/-1 | `write(fd,buf,len)` |
| lseek | unistd.h | `off_t lseek(int fd, off_t offset, int whence)` | 新位置/-1 | `lseek(fd,0,SEEK_END)` |

---

## 五、易错点速查卡

| 错误现象 | 错误原因 | 正确写法 | 后果 |
|---------|---------|---------|------|
| fopen返回NULL后直接使用fp | 未检查返回值 | `if(fp==NULL){perror("...");return -1;}` | 段错误(Segfault) |
| fgetc用char接收判断EOF | char范围0~255无法表示-1 | `int ch = fgetc(fp); if(ch==EOF)...` | 含0xFF字节的文件提前结束 |
| fgets后strcmp永远不等 | fgets保留了末尾\n | `buf[strlen(buf)-1]='\0'`后再比较 | 逻辑判断永远失败 |
| fwrite写二进制后用fprintf读 | 读写模式不匹配 | fwrite配fread，fprintf配fscanf | 数据错乱/乱码 |
| sprintf写入超出数组大小 | 无边界检查 | 改用snprintf(buf,sizeof(buf),...) | 缓冲区溢出/段错误 |
| open含O_CREAT不给mode | 缺少权限参数 | `open(path,O_CREAT\|O_WRONLY,0644)` | 新建文件权限随机 |
| read返回值当strlen用 | read不添加'\0' | 用read返回值作为数据长度 | 读到垃圾数据 |
| 全缓存文件遇\n以为会刷新 | 全缓存不因\n刷新 | 用fflush或fclose强制刷新 | 数据滞留在缓冲区 |
| close后继续使用fd | fd已失效 | close后不再使用该fd | EBADF错误 |
| 同一文件混用标准IO和文件IO | 缓冲区与直接写入交错 | 统一使用一套API | 数据顺序混乱 |

---

## 六、常见陷阱专题

### 陷阱1：fopen以"r"模式打开不存在的文件

- **错误写法**：
```cpp
FILE *fp = fopen("noexist.txt", "r");  // 返回NULL
fputc('A', fp);  // fp为NULL → 段错误
```
- **正确写法**：
```cpp
FILE *fp = fopen("noexist.txt", "r");
if (fp == NULL) {
    perror("fopen error");  // 输出：fopen error: No such file or directory
    return -1;
}
```
- **如何记住**："r只读不创，w才帮你建"

### 陷阱2：fgets保留了换行符导致字符串比较失败

- **错误写法**：
```cpp
char buf[128];
fgets(buf, sizeof(buf), stdin);     // 输入"quit" → buf="quit\n"
if (strcmp(buf, "quit") == 0) {     // "quit\n" != "quit" → 永远不等
    break;
}
```
- **正确写法**：
```cpp
char buf[128];
fgets(buf, sizeof(buf), stdin);
buf[strlen(buf) - 1] = '\0';        // 去掉末尾\n
if (strcmp(buf, "quit") == 0) {     // 现在可以匹配了
    break;
}
```
- **如何记住**："fgets带尾巴，用完记得剪"

### 陷阱3：fwrite写入结构体后用fprintf读取导致数据错乱

- **错误写法**：
```cpp
Stu s = {"张三", 18, 98.0};
fwrite(&s, sizeof(Stu), 1, fp);     // 写入二进制数据
// ...
fscanf(fp, "%s %d %lf", name, &age, &score);  // 按文本解析二进制 → 全乱
```
- **正确写法**：
```cpp
// 二进制路线
fwrite(&s, sizeof(Stu), 1, fp);
fread(&temp, sizeof(Stu), 1, fp);   // 配对读取

// 文本路线
fprintf(fp, "%s %d %lf\n", s.name, s.age, s.score);
fscanf(fp, "%s %d %lf", name, &age, &score);  // 配对读取
```
- **如何记住**："二进制配二进制，文本配文本"

---

## 七、新手最常问的5个问题

### Q1：标准IO比文件IO快，为什么还要学文件IO？

**答**：标准IO快是因为缓冲区减少了系统调用次数，但在以下场景必须用文件IO：
1. 操作设备文件（如/dev/tty）、管道、socket——这些不支持标准IO
2. 需要原子操作（如O_EXCL排他创建）
3. 需要精确控制何时写入磁盘（如数据库WAL日志）
4. 标准IO本身就是用文件IO实现的（底层调用open/read/write）

### Q2：fopen的"w"模式和"a"模式有什么区别？

**答**：
- "w"：文件存在则**清空**，从头开始写。适合覆盖写入。
- "a"：文件存在则**保留**，只能在末尾追加。适合日志记录。
- 两者都会在文件不存在时自动创建。

### Q3：为什么read返回0不算错误？

**答**：read返回0表示"到达了文件末尾，没有更多数据可读"，这是正常的结束信号。只有返回-1才表示真正的错误（如fd无效、被信号中断等）。这类似于fgetc返回EOF表示文件结束而非错误。

### Q4：缓冲区里的数据什么时候真正写入磁盘？

**答**：数据流经三层：用户缓冲区 → 内核缓冲区 → 磁盘。
- 用户缓冲区到内核：由刷新时机触发（换行/满/fflush/fclose等）
- 内核到磁盘：由操作系统调度决定（通常有延迟）
- 如需确保数据落盘：fflush + fsync(fd)

### Q5：为什么open创建的文件的权限和我指定的不一样？

**答**：最终权限 = 你指定的mode & ~umask。例如：
- 你指定0666，umask=0022 → 最终权限 = 0666 & ~0022 = 0644
- umask的作用是"屏蔽"掉组和其他用户的写权限
- 用`umask`命令查看当前值，用`umask 0000`临时取消屏蔽

---

## 八、代码自测清单

学完本章后，你应该能独立写出以下代码：

- [ ] 用fopen/fclose/fgetc/fputc实现文件拷贝
- [ ] 用fgets/fputs实现带换行处理的文件读写
- [ ] 用fread/fwrite完成结构体数据的存取
- [ ] 用fseek/ftell求文件大小并随机访问
- [ ] 用open/read/write/lseek完成文件IO版本的文件拷贝
- [ ] 正确处理errno并用perror输出错误信息
- [ ] 用snprintf安全地拼接多种类型数据到字符数组
- [ ] 用fprintf/fscanf实现简单的注册登录系统
- [ ] 区分行缓存、全缓存、不缓存的刷新行为
- [ ] 说出fopen六种模式与open标志位的对应关系

---

## 九、复习计划

| 时间 | 复习内容 | 方式 |
|------|----------|------|
| 1天后 | fopen六种模式、缓冲区三种类型及刷新时机 | 默写表格 + 写小程序验证每种刷新时机 |
| 3天后 | 标准IO vs 文件IO对比、fread/fwrite三种数据类型 | 重做文件拷贝练习（分别用fgetc、fgets、fread三种方式） |
| 7天后 | 全章回顾 | 看树状图回忆 + 做下方4道练习题 |
| 14天后 | 结合第3章多进程编程复习 | 用管道(pipe)实践文件IO，体会fd继承 |

---

## 十、树状图（全章知识体系）

```
IO操作
├── 标准IO（库函数 + 缓冲区）
│   ├── FILE结构体
│   │   ├── _IO_buf_base / _IO_buf_end（缓冲区地址）
│   │   ├── _fileno（文件描述符）
│   │   └── 三个特殊指针：stdin(0) / stdout(1) / stderr(2)
│   ├── 打开/关闭
│   │   ├── fopen(path, mode) → FILE*
│   │   │   └── 六种模式：r / r+ / w / w+ / a / a+
│   │   └── fclose(fp) → 0/EOF
│   ├── 错误处理
│   │   ├── errno（全局错误码）
│   │   ├── strerror(errno) → 错误字符串
│   │   └── perror("msg") → 直接打印
│   ├── 字符读写
│   │   ├── fgetc(fp) → int/EOF
│   │   └── fputc(c, fp) → int/EOF
│   ├── 字符串读写
│   │   ├── fgets(s, n, fp) → char*/NULL（保留\n）
│   │   └── fputs(s, fp) → int/EOF（不加\n）
│   ├── 缓冲区机制
│   │   ├── 行缓存(1024B) → stdin/stdout
│   │   ├── 全缓存(4096B) → 普通文件
│   │   ├── 不缓存(0B) → stderr
│   │   ├── 七种刷新时机
│   │   └── fflush(fp) 手动刷新
│   ├── 格式化读写
│   │   ├── fprintf / fscanf（文件版printf/scanf）
│   │   └── sprintf / snprintf（格式串→字符数组）
│   ├── 模块化读写
│   │   ├── fread(ptr, size, nmemb, fp)
│   │   └── fwrite(ptr, size, nmemb, fp)
│   └── 光标操作
│       ├── fseek(fp, offset, whence)
│       ├── ftell(fp) → 偏移量
│       └── rewind(fp) → 回到开头
│
└── 文件IO（系统调用 + 无缓冲）
    ├── 文件描述符
    │   ├── 非负整数，最小未分配原则
    │   ├── 0/1/2 = stdin/stdout/stderr
    │   └── ulimit -a 查看上限
    ├── 打开/关闭
    │   ├── open(path, flags, mode) → fd
    │   │   ├── 必选：O_RDONLY/O_WRONLY/O_RDWR
    │   │   └── 可选：O_CREAT/O_TRUNC/O_APPEND/O_EXCL
    │   └── close(fd) → 0/-1
    ├── 读写
    │   ├── read(fd, buf, count) → 字节数/0/-1
    │   └── write(fd, buf, count) → 字节数/-1
    └── 光标操作
        └── lseek(fd, offset, whence) → 新位置/-1
```

---

## 十一、3条随身速记口诀

1. **"r只读不创，w才帮你建；a追在末尾，加号能读写"** —— fopen六种模式
2. **"行缓存见换行就刷，全缓存满了才刷，不缓存秒刷"** —— 三种缓冲区刷新规则
3. **"fwrite配fread，fprintf配fscanf；二进制对二进制，文本对文本"** —— 读写配对原则

---

## 十二、4道练习题（答案留空）

### 题目1（★）：fopen模式辨析
请写出以下需求对应的fopen打开模式：
1. 打开已有文件读取内容，文件不存在则报错：______
2. 创建新文件写入数据，文件存在则清空：______
3. 在已有文件末尾追加数据，文件不存在则创建：______
4. 打开已有文件既能读又能写，不清空内容：______

**考察知识点**：fopen六种模式

### 题目2（★★）：缓冲区刷新判断
以下代码在终端运行时，"hello"是否会显示在屏幕上？为什么？
```cpp
printf("hello");
while(1);
```
如果改为`printf("hello\n");`呢？如果改为`fprintf(fp, "hello\n");`（fp为普通文件指针）呢？

**考察知识点**：行缓存vs全缓存刷新时机

### 题目3（★★★）：文件拷贝升级版
请用fread/fwrite实现一个文件拷贝程序，要求：
1. 支持命令行传入源文件和目标文件路径
2. 每次读写4096字节（模拟全缓存大小）
3. 正确处理最后一次读取不足4096字节的情况
4. 打印拷贝完成的总字节数

**考察知识点**：fread/fwrite返回值处理、文件操作三步曲

### 题目4（★★★★）：综合题——简易学生成绩管理系统
请实现一个学生成绩管理系统，要求：
1. 定义结构体`Student{char name[20]; int id; double score;}`
2. 功能菜单：(1)录入学生 (2)查询学生(按id) (3)修改成绩 (4)显示全部 (0)退出
3. 数据以二进制方式存储在`students.dat`文件中（用fwrite/fread）
4. 查询和修改功能需要用fseek定位到指定记录
5. 所有文件操作必须有错误检查和资源释放

**考察知识点**：fopen/fclose、fwrite/fread、fseek/ftell、结构体IO、错误处理、菜单循环

---

## 十三、知识蒸馏总结

> 文件IO两套API：标准IO带缓冲效率高适合日常读写，文件IO无缓冲直达内核适合底层精确控制；打开必查返回值，用完必关闭，读写方式要配对。

---

## 十四、错题记录 + 复习建议

| 题号 | 题目 | 我的错误答案 | 正确答案 | 错误原因 | 涉及知识点 | 复习建议 |
|------|------|-------------|----------|----------|-----------|----------|
| （待填写） | | | | | | 建议1天后复习 |
| （待填写） | | | | | | 建议3天后复习 |
| （待填写） | | | | | | 建议7天后复习 |
| （待填写） | | | | | | 建议14天后复习 |

> **使用说明**：完成上方4道练习题后，将错题填入此表。重点关注"错误原因"列，它揭示了你的知识盲区。根据艾宾浩斯遗忘曲线，按建议时间间隔复习对应知识点。

---

## 附录：术语中英对照表

| 中文术语 | 英文术语 | 缩写/符号 |
|---------|---------|----------|
| 输入/输出 | Input/Output | IO |
| 标准IO | Standard IO | stdio |
| 文件IO | File IO / System Call IO | - |
| 文件指针 | File Pointer | FILE* |
| 文件描述符 | File Descriptor | fd |
| 缓冲区 | Buffer | buf |
| 行缓存 | Line Buffer | - |
| 全缓存 | Full Buffer / Block Buffer | - |
| 不缓存 | No Buffer / Unbuffered | - |
| 刷新 | Flush | fflush |
| 系统调用 | System Call | syscall |
| 用户空间 | User Space | - |
| 内核空间 | Kernel Space | - |
| 错误码 | Error Number | errno |
| 文件光标/偏移量 | File Offset / Cursor | - |
| 打开模式 | Open Mode / Flags | - |
| 权限掩码 | Permission Mask | umask |
| 最小未分配原则 | Lowest Available FD | - |
| 二进制模式 | Binary Mode | - |
| 文本模式 | Text Mode | - |
| 追加模式 | Append Mode | O_APPEND |
| 截断/清空 | Truncate | O_TRUNC |
| 排他创建 | Exclusive Create | O_EXCL |
| 上下文切换 | Context Switch | - |
| 资源泄漏 | Resource Leak | - |
| 段错误 | Segmentation Fault | Segfault |

---

## 附加：性能对比实验思路

**问题**：标准IO真的比文件IO快吗？快多少？

**实验设计**：
```bash
# 准备一个10MB测试文件
dd if=/dev/zero of=testfile bs=1M count=10

# 方式1：用fgetc/fputc拷贝（标准IO，有缓冲）
time ./std_copy testfile dest1

# 方式2：用read/write拷贝，每次1字节（文件IO，无缓冲）
time ./sys_copy_1byte testfile dest2

# 方式3：用read/write拷贝，每次4096字节（文件IO，手动模拟缓冲）
time ./sys_copy_4k testfile dest3
```

**预期结果**：方式1 ≈ 方式3 >> 方式2。标准IO快的本质是缓冲区减少了系统调用次数，如果你手动给文件IO加上合适大小的缓冲（方式3），性能可以接近标准IO。

**面试题参考**：
- 为什么标准IO比文件IO快？→ 缓冲区减少系统调用次数
- 缓冲区的作用是什么？→ 合并多次小IO为一次大IO，减少用户态/内核态切换开销
- 什么时候该用文件IO？→ 操作设备/管道/socket、需要原子操作、需要精确控制写入时机、编写标准IO库本身

---

*笔记生成完毕。本笔记所有内容均来源于《第二章：IO操作.pdf》课件及day1/day2配套代码，未编造任何知识点。*
