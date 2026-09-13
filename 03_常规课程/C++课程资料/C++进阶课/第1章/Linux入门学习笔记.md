# C++进阶课 第1章：Linux入门 -- 完整学习笔记

> **前置章节**：C++基础篇
> **预计学习时间**：5.5小时
> **配套材料**：第一章linux入门.pdf + day1/day2/day3/CMake代码
> **本章定位**：承上启下——将C++基础落地到Linux开发环境，为后续IO、进程、线程、网络编程打基础

---

## 知识蒸馏总结（50字以内）

本章教你在Linux上搭环境、用Vim写代码、四步编译C++程序、GDB调试、制作静态/动态库、用Makefile自动化构建。

---

## 一、全部知识点（黄金四步法 + 生活比喻 + 人话总结）

### 模块一：Linux环境搭建与基本操作（P1-P25）

#### 1.1 VMware虚拟机安装【熟悉】

**是什么**：VMware是一款虚拟化软件，能在一台物理电脑上模拟出多台独立的虚拟计算机。就像在你的大房子里隔出若干个小房间，每个小房间都有独立的门窗、水电，互不干扰。

**为什么**：
- 为什么需要虚拟机？学习Linux不能直接在Windows上操作，需要独立的Linux环境。
- 为什么不装双系统？双系统切换麻烦且有风险，虚拟机可以随时快照、回滚、克隆。
- 为什么选VMware？兼容性好、社区资源丰富、支持CentOS等主流发行版。

**怎么用**：
```bash
# 1. 从网盘下载VMware安装包并安装
# 2. 激活虚拟机（使用提供的许可证）
# 3. 桌面出现VMware图标即表示安装成功
# 输出：桌面上显示VMware Workstation图标
```

**注意事项**：
- 错误示范：安装路径含中文 → 可能导致部分功能异常
- 正确做法：安装路径使用纯英文，如 `D:\VMware`
- 安装完成后务必确认VT-x/AMD-V已在BIOS中开启，否则虚拟机无法启动64位系统

> **人话总结**：虚拟机就是电脑里的电脑。

#### 1.2 CentOS 8安装与配置【熟悉】

**是什么**：CentOS是免费的企业级Linux发行版，是Red Hat Enterprise Linux的社区复刻版。好比Windows有正版和开源替代版，CentOS就是RHEL的"平价替代品"。

**为什么**：
- 为什么选CentOS？服务器市场占有率高，教程丰富，适合学习系统编程。
- 为什么用8.x版本？内核较新，软件包兼容性较好。
- 为什么要配sudoers？普通用户默认没有管理员权限，开发时需要安装软件、修改系统文件。

**怎么用**：
```bash
# 切换到管理员用户
su root
# 输入root密码后进入管理员模式
# 输出：[root@localhost ~]#

# 赋予普通用户管理员权限
chmod u+w /etc/sudoers           # 给sudoers文件加写权限
vi /etc/sudoers                  # 编辑sudoers文件
# 找到 root ALL=(ALL) ALL 这一行
# 按yy复制该行，按p粘贴
# 将复制行中的root改成你的用户名，如 zpp
# ESC → shift+: → wq 保存退出

chmod u-w /etc/sudoers           # 恢复只读权限
exit                             # 退回普通用户
# 输出：[zpp@localhost ~]$
```

**注意事项**：
- 错误示范：修改完sudoers忘记去掉写权限 → 安全风险，系统可能警告
- 正确做法：改完立刻 `chmod u-w /etc/sudoers`
- 编辑sudoers时不要直接用vim，生产环境建议用 `visudo` 命令（自带语法检查）

> **人话总结**：装好系统先给自己开管理员权限。

#### 1.3 阿里云镜像源切换【熟悉】

**是什么**：镜像源是软件仓库的国内副本服务器。就像官方快递太慢，你在本地设了一个中转仓，下载速度飞快。

**为什么**：
- 为什么换源？CentOS 8官方源已停止维护，默认源不可用。
- 为什么选阿里云？速度快、稳定、同步及时。
- 为什么要备份原文件？万一出问题可以回退。

**怎么用**：
```bash
# 备份原有仓库配置
sudo mkdir /etc/yum.repos.d/backup
sudo mv /etc/yum.repos.d/CentOS-* /etc/yum.repos.d/backup

# 下载阿里云镜像文件
sudo curl -o /etc/yum.repos.d/CentOS-Base.repo \
  https://mirrors.aliyun.com/repo/Centos-vault-8.5.2111.repo

# 清除缓存并重建元数据
sudo dnf clean all
sudo dnf makecache
# 输出：Metadata cache created.
```

**注意事项**：
- 错误示范：不备份直接覆盖 → 原始配置丢失无法恢复
- 正确做法：先mkdir备份再mv移动
- curl下载的repo版本号要和你的CentOS版本匹配

> **人话总结**：换个国内仓库，装软件快十倍。

#### 1.4 网络问题排查【了解】

**是什么**：虚拟机网络问题的系统化排查流程。就像家里断网了，你先看路由器灯亮不亮，再看网线插没插，最后才打电话给运营商。

**常见问题与解决**：
| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 无IP地址 | 网络管理冲突/VM服务未启动 | 检查VMware服务、重启network |
| 主机与虚拟机不通 | 网络适配器异常 | 检查虚拟网络编辑器设置 |
| 有IP但无外网 | 静态IP配置错误 | 检查三个IP段是否一致 |

```bash
# 查看IP地址
ifconfig
# 或
ip addr

# 重启网络服务
systemctl restart network

# 查看网卡配置
cat /etc/sysconfig/network-scripts/ifcfg-ens33
# 关键配置项：ONBOOT=yes, BOOTPROTO=dhcp/static
```

> **人话总结**：断网六步查：服务→模式→配置→IP→DNS→重置。

#### 1.5 用户管理与常用指令【熟悉】

**是什么**：Linux是多用户操作系统，分为管理员(root)和普通用户。好比公司有老板(全权)和员工(受限)。

**为什么**：
- 为什么分用户？安全隔离，防止普通用户误操作破坏系统。
- 为什么用su/sudo？临时获取权限比一直用root更安全。
- 为什么推荐日常用普通用户？减少误删系统文件的风险。

**怎么用**：
```bash
# 普通用户 → 管理员
su root          # 输入root密码
# 输出：[root@localhost ~]#

# 管理员 → 普通用户
exit             # 或按 Ctrl+D
# 输出：[zpp@localhost ~]$

# 以管理员身份执行单条命令
sudo yum install gcc
# 输入当前用户密码即可
```

**注意事项**：
- 错误示范：一直用root登录开发 → 一条rm -rf可能毁掉整个系统
- 正确做法：日常用普通用户，需要时sudo提权

> **人话总结**：平时用小号，干活切大号。

#### 1.6 Xshell远程连接【了解】

**是什么**：Xshell是Windows平台的SSH客户端，通过加密通道远程控制Linux服务器。就像用手机远程操控家里的电脑。

**为什么**：SSH协议对传输数据加密，防止密码和内容被窃听；远程操作比虚拟机窗口更方便。

**怎么用**：
```
1. 安装Xshell（官网或网盘下载）
2. 新建会话 → 填写主机IP（ifconfig查看）、端口22
3. 用户身份验证 → 输入用户名和密码
4. 连接成功后即可在终端操作CentOS
```

> **人话总结**：Xshell让你用Windows舒服地操作Linux。

#### 1.7 Vim编辑器【重点】

**是什么**：Vim是Linux下的文本编辑器，有三种工作模式：命令行模式、插入模式、底行模式。好比一把瑞士军刀，不同模式对应不同的刀片功能。

**为什么**：
- 为什么学Vim？Linux服务器通常没有图形界面，Vim是标配编辑器。
- 为什么有三种模式？分离"浏览/编辑/命令"操作，效率远高于单一模式编辑器。
- 为什么命令行模式是默认模式？安全第一，防止误编辑。

**怎么用**：

**三种模式切换关系**：
```
                    i/a/o/s等键
  命令行模式 ──────────────────→ 插入模式
      ↑                              │
      │          ESC                 │
      └──────────────────────────────┘
      
      shift+:
  命令行模式 ──────────────────→ 底行模式
      ↑                              │
      │          ESC                 │
      └──────────────────────────────┘
```

**命令行模式核心命令**：
```
yy       复制当前行
nyy      复制从光标起n行
p        粘贴剪切板内容
dd       删除(剪切)当前行
ndd      删除从光标起n行
u        撤销上一步
Ctrl+r   反撤销
gg       跳到首行
nG       跳到第n行
0        光标到行首
$        光标到行尾
```

**进入插入模式的键**：
```
i    光标前进入
I    行首进入
a    光标后进入
A    行尾进入
o    下一行进入
O    上一行进入
s    删除当前字符后进入
S    删除整行后进入
INSERT  同i键
```

**底行模式核心命令**：
```
:w              保存
:q              退出
:q!             强制退出不保存
:wq             保存并退出
:x              保存并退出
:set number     显示行号
:set nonumber   隐藏行号
/string         向下查找string
:%s/old/new/g   全文替换old为new
:m,ns/old/new/g 替换m到n行中的old为new
```

**完整示例**：
```bash
# 创建并编辑文件
touch test.txt
vim test.txt
# 进入vim后默认为命令行模式
# 按i进入插入模式，输入内容
# 按ESC回到命令行模式
# 按shift+:进入底行模式
# 输入 :wq 保存退出
# 输出：文件test.txt已保存并退出vim
```

**注意事项**：

**错误示范1**：底行模式替换漏掉 `/g`
```vim
:%s/old/new       " 只替换每行第一个匹配
```
**正确写法**：
```vim
:%s/old/new/g     " g=global，全局替换才安心
```

**错误示范2**：在插入模式直接输入 `:wq`
```
# 结果：:wq被当作文本输入到文件中
```
**正确做法**：先按ESC回到命令行模式，再按shift+:进底行模式

**错误示范3**：不能从底行模式直接进入插入模式
```
# 必须先ESC回命令行模式，再按i/a等键
```

> **人话总结**：Vim三模式，ESC是万能钥匙。

---

### 模块二：C++开发环境与第一个程序（P25-P45）

#### 2.1 gcc/g++编译环境安装【重点】

**是什么**：gcc是GNU C编译器，g++是GNU C++编译器。它们是把源代码翻译成机器能执行的二进制程序的翻译官。

**为什么**：
- 为什么装两个？gcc编译C语言，g++编译C++语言，g++会自动链接C++标准库。
- 为什么要验证版本？确保安装成功且版本兼容。
- 为什么用yum安装？自动处理依赖关系，避免手动配置的坑。

**怎么用**：
```bash
# 安装gcc和g++
sudo yum install gcc            # C编译器
sudo yum install gcc-c++        # C++编译器

# 验证安装
gcc --version                   # 输出版本号如 gcc (GCC) 8.5.0
g++ --version                   # 输出版本号如 g++ (GCC) 8.5.0

# 安装GDB调试工具
sudo yum install gdb
gdb --version                   # 验证

# 安装CMake
sudo yum install cmake
cmake --version                 # 验证
```

**注意事项**：
- 错误示范：用gcc编译.cpp文件 → 不会自动链接C++标准库，报一堆undefined reference
- 正确做法：C++程序一律用g++编译
- 卸载命令：`sudo yum remove gcc` / `sudo yum remove gcc-c++`

> **人话总结**：C用gcc，C++用g++，别搞混。

#### 2.2 C++程序框架详解【熟悉】

**是什么**：一个标准C++程序的骨架结构，包含头文件引入、命名空间、主函数三大要素。就像写信要有称呼、正文、落款。

**代码走读**（配套文件 day1/02demo.cpp）：
```cpp
#include<iostream>
// #是预处理标识，include是文件包含指令
// iostream = i(input) + o(output) + stream(流)
// 预处理阶段会将iostream的全部内容在此处展开

#include<string>
// string类所在的头文件，C++中头文件名通常就是类名

using namespace std;
// using：使用命名空间的关键字
// namespace：命名空间关键字
// std：标准命名空间，所有C++标准库的类名、函数名都在其中
// 同一作用域可以有多个同名namespace，但内部名字不能重复

int main(int argc, const char *argv[])
// main：程序入口函数，有且仅有一个
// argc：外部传参个数（包括程序名本身）
// argv：字符指针数组，每个元素是一个参数字符串
{
    cout << "hello world" << endl;
    // cout是ostream类的对象，<<是重载的输出运算符
    // endl输出换行并刷新缓冲区
    return 0;
    // 返回0表示程序正常结束
}
```

**编译运行**：
```bash
g++ 02demo.cpp -o demo
./demo
# 输出：hello world
```

**注意事项**：
- 错误示范：忘记 `using namespace std;` 又不加 `std::` 前缀 → 编译报错 `cout was not declared`
- 正确做法：要么用using，要么每次写 `std::cout`

> **人话总结**：include引工具，using开门，main是入口。

#### 2.3 四步编译过程【重点】

**是什么**：C++源码变成可执行程序要经过预处理→编译→汇编→链接四个阶段。就像做菜要经过洗菜→切菜→炒菜→装盘四步。

**为什么**：
- 为什么分四步？每步职责单一，便于定位问题和增量编译。
- 为什么预处理单独一步？宏替换和头文件展开是纯文本操作，不涉及语法分析。
- 为什么链接最后做？只有所有.o文件都生成后才能解析跨文件的符号引用。

**四步编译流程图**：
```
源文件(.cpp)
    │ g++ -E
    ▼
预处理文件(.i)  ← 头文件展开、删除注释、宏替换
    │ g++ -S
    ▼
汇编文件(.s)    ← 将C++翻译为汇编语言
    │ g++ -c
    ▼
目标文件(.o)    ← 将汇编翻译为机器码(二进制)
    │ g++ xxx.o -o
    ▼
可执行程序      ← 链接库文件和多个.o，解析符号
```

**完整示例**：
```bash
# 方法一：一步到位
g++ 02demo.cpp -o demo          # 自动生成可执行程序demo
./demo
# 输出：hello world

# 方法二：分步编译（重要！面试必考）
# 第1步：预处理
g++ -E 02demo.cpp -o 02demo.i
# 产物：.i文件，头文件已展开，注释已删除，宏已替换
# 文件体积会膨胀很多倍

# 第2步：编译
g++ -S 02demo.i -o 02demo.s
# 产物：.s文件，内容是汇编语言（人类可读的底层指令）

# 第3步：汇编
g++ -c 02demo.s -o 02demo.o
# 产物：.o文件，二进制机器码，但外部符号未解析

# 第4步：链接
g++ 02demo.o -o demo
# 产物：可执行程序demo，所有符号已解析，可直接运行

./demo
# 输出：hello world
```

**各阶段输入输出对照表**：
| 阶段 | 命令选项 | 输入文件 | 输出文件 | 核心操作 |
|------|---------|---------|---------|---------|
| 预处理 | -E | .cpp | .i | 展开头文件、删注释、宏替换 |
| 编译 | -S | .i | .s | C++翻译为汇编语言 |
| 汇编 | -c | .s | .o | 汇编翻译为二进制机器码 |
| 链接 | (默认) | .o + 库 | 可执行文件 | 解析符号、合并段 |

**内存布局补充**（链接后的可执行程序）：
```
高地址 ┌──────────────┐
       │   栈(stack)   │ ← 局部变量、函数调用帧，向下增长
       ├──────────────┤
       │     ↓↑       │
       ├──────────────┤
       │   堆(heap)    │ ← malloc/new分配，向上增长
       ├──────────────┤
       │   .bss段      │ ← 未初始化全局变量(占位)
       ├──────────────┤
       │   .data段     │ ← 已初始化全局变量
       ├──────────────┤
       │   .text段     │ ← 程序代码(只读)
低地址 └──────────────┘
```

**注意事项**：
- 错误示范：`g++ -c 02demo.cpp -o 02demo.o` 后直接 `./02demo.o` → 报错"cannot execute binary file"，因为.o不是可执行文件
- 正确做法：.o必须经过链接才能运行
- 分步编译的价值：修改一个.cpp只需重新编译该文件再链接，大幅节省大型项目编译时间

> **人话总结**：E预S编c汇链接成，四步变程序。

#### 2.4 man手册使用【熟悉】

**是什么**：man手册是Linux自带的函数/命令帮助文档，相当于离线版的API文档。就像买了一本电器说明书，随时查阅。

**为什么**：
- 为什么用man？网络不稳定时也能查，内容权威准确。
- 为什么分七章？不同类型的文档归类存放，精准查找。
- 为什么重点看第2、3章？第2章是系统调用（内核接口），第3章是库函数，都是编程核心。

**man手册七章结构**：
| 章节 | 内容 | 重要性 |
|------|------|--------|
| 1 | Shell命令 | 常用 |
| 2 | 系统调用函数 | **重点** |
| 3 | C库函数 | **重要** |
| 4 | 设备文件 | 了解 |
| 5 | 文件格式 | 了解 |
| 6 | 游戏 | 了解 |
| 7 | 杂项 | 了解 |

**怎么用**：
```bash
# 安装C库函数的man页面
sudo yum install man-pages man-pages-devel

# 查看open系统调用（第2章）
man 2 open
# 显示：函数签名、参数含义、返回值、errno说明

# 查看printf库函数（第3章）
man 3 printf

# 查看ls命令（第1章）
man ls

# 退出手册
# 按 q 键退出
```

**man手册式函数签名示例**（以open为例）：
```c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int open(const char *pathname, int flags);
int open(const char *pathname, int flags, mode_t mode);

// 参数：
//   pathname: 文件路径字符串
//   flags:    打开标志(O_RDONLY/O_WRONLY/O_RDWR/O_CREAT/O_TRUNC等)
//   mode:     创建文件时的权限(如0664)，仅在flags含O_CREAT时需要
// 返回值：
//   成功：文件描述符(非负整数)
//   失败：-1，同时设置errno
```

> **人话总结**：man是Linux的程序员工具书。

#### 2.5 sys库常用函数概览【了解】

**是什么**：sys库是Linux内核提供给用户空间的系统调用接口集合。就像餐厅的服务窗口，你通过它向厨房(内核)下单。

**四大类函数**：
| 类别 | 代表函数 | 用途 |
|------|---------|------|
| 文件操作 | open/read/write/close/lseek | 读写文件 |
| 进程控制 | fork/exit/wait/execl | 创建和管理进程 |
| 信号操作 | kill/signal | 进程间通信 |
| 网络通信 | socket/bind/listen | 网络编程 |

**代码走读**（配套文件 day1/03file.cpp）：
```cpp
#include<iostream>
#include<sys/types.h>    // 系统数据类型定义
#include<sys/stat.h>     // 文件状态相关
#include<fcntl.h>        // open函数的flags定义
#include<string.h>       // strlen等字符串函数
#include<stdio.h>        // perror等
#include<unistd.h>       // write/close等POSIX函数
using namespace std;

int main()
{
    // 1. 打开文件
    int fd = -1;         // 文件描述符初始化为-1(无效值)
    if((fd = open("./test.txt", O_WRONLY|O_CREAT|O_TRUNC, 0664)) == -1)
    // open参数：路径、写-only|创建|截断、权限rw-rw-r--
    // 返回-1表示失败，此时errno被设置
    {
        perror("open error");  // 打印"open error: 具体错误描述"
        return -1;
    }

    // 2. 写入数据
    write(fd, "hello", strlen("hello"));
    // write(文件描述符, 数据指针, 字节数)
    // 将"hello"5个字节写入文件

    // 3. 关闭文件
    close(fd);
    // 释放文件描述符资源

    return 0;
}
```

**系统调用三件套**（每个系统调用都要掌握）：
1. **参数含义**：每个参数的类型和作用
2. **返回值**：成功返回什么，失败返回什么
3. **errno错误处理**：失败时如何用perror/strerror获取具体原因

> **人话总结**：sys库是你跟内核对话的翻译器。

---

### 模块三：GDB调试与库的制作（P45-P90）

#### 3.1 GDB调试【重点】

**是什么**：GDB(GNU Debugger)是Linux下的程序调试器，能让你看到程序运行时内部发生了什么。就像给程序装了X光机，能看到每一行代码执行时变量的状态。

**为什么**：
- 为什么不用printf调试？printf只能看到某个点的值，GDB能暂停、回溯、修改变量。
- 为什么编译要加-g？-g选项把调试信息(变量名、行号映射)嵌入可执行文件，没有它GDB看不到源码。
- 为什么GDB能做四件事？启动程序、条件断点、检查状态、运行时修改——覆盖了调试的所有场景。

**GDB四大能力**：
1. 启动程序并传递参数
2. 使程序在指定条件下停止（断点）
3. 检查程序停止时的状态（变量、调用栈）
4. 运行时修改变量值，尝试修复并继续

**代码走读**（配套文件 day2/03gdb.cpp）：
```cpp
#include<iostream>
#include<stdio.h>
using namespace std;

void print()               // 自定义函数，用于演示step跳入
{
    cout<<"hello world"<<endl;
    cout<<"这是我想要说给大家听的!!!"<<endl;
}

int main(int argc, const char *argv[])
{
    int arr[5] = {1,2,3,4,5};   // 数组，可用print arr@5查看
    int i = 0;

    for(i=0; i<5; i++)
    {
        cout << arr[i] << " ";  // 循环输出数组元素
    }
    cout << endl;

    print();                    // 调用自定义函数
    return 0;
}
```

**完整GDB调试流程**：
```bash
# 第1步：编译时加-g选项
g++ -g 03gdb.cpp -o gdb_demo

# 第2步：启动GDB
gdb ./gdb_demo
# 输出：GNU gdb (GDB) ... Reading symbols from ./gdb_demo...done.

# 第3步：查看源码
(gdb) list                     # 显示前10行
(gdb) list 1,25                # 显示第1到25行
(gdb) list print               # 显示print函数附近代码

# 第4步：设置断点
(gdb) break 20                 # 在第20行设断点
(gdb) break print              # 在print函数入口设断点
(gdb) info break               # 查看所有断点
# 输出：Num Type Disp Enb Address What
#       1   breakpoint keep y   0x... at 03gdb.cpp:20

# 第5步：运行程序
(gdb) run                      # 开始执行，遇到断点暂停
# 输出：Breakpoint 1, main (...) at 03gdb.cpp:20

# 第6步：单步调试
(gdb) next                     # 执行下一行(不跳入函数)
(gdb) step                     # 执行下一行(跳入函数内部)
(gdb) continue                 # 继续执行到下一个断点

# 第7步：查看和修改变量
(gdb) print i                  # 打印变量i的值
(gdb) print arr                # 打印数组首元素
(gdb) print arr@5              # 打印数组全部5个元素
# 输出：$1 = {1, 2, 3, 4, 5}
(gdb) set variable i=3         # 修改i的值为3

# 第8步：退出
(gdb) quit                     # 或 q
```

**GDB常用指令速查**：
| 指令 | 缩写 | 功能 |
|------|------|------|
| quit | q | 退出GDB |
| run | r | 运行程序 |
| list | l | 显示源码 |
| break | b | 设置断点 |
| next | n | 单步执行(不跳入) |
| step | s | 单步执行(跳入函数) |
| continue | c | 继续执行 |
| print | p | 打印变量 |
| info break | - | 查看断点 |
| delete breakpoint N | - | 删除第N号断点 |
| set variable var=val | - | 修改变量值 |
| shell cmd | - | 执行终端命令 |
| set logging on | - | 开启调试日志 |

**Watchpoint观察点**：
```bash
(gdb) watch i                  # 监视变量i
# 当i的值发生变化时自动暂停，显示旧值和新值
# 输出：Hardware watchpoint 2: i
#        Old value = 0
#        New value = 1
```

**Core Dump调试**：
```bash
# 查看当前core文件限制
ulimit -a
# core file size 通常为0（不生成）

# 开启core dump
ulimit -c unlimited

# 运行出错程序后会产生core文件
./crash_program
# 输出：Segmentation fault (core dumped)

# 用GDB分析core文件
gdb ./crash_program core
(gdb) bt                       # 查看崩溃时的调用栈
# 输出：#0 0x... in main () at crash.cpp:10
```

**调试运行中的进程**：
```bash
# 后台运行程序
./a.out &
# 输出：[1] 26837    （作业号和进程号）

# 附加到运行中的进程
gdb -p 26837
# 输出：Attaching to process 26837
# 此时程序暂停，可以进行调试操作
```

**注意事项**：
- 错误示范：编译不加-g → GDB无法显示源码行号和变量名
- 正确做法：开发阶段始终 `g++ -g` 编译
- 错误示范：next和step混淆 → next跳过函数调用，step进入函数内部
- 正确做法：想进函数用step，想跳过用next
- release版本记得去掉-g，否则增大二进制体积

> **人话总结**：GDB就是程序的X光机。

#### 3.2 静态库制作与使用【重点】

**是什么**：静态库(.a)是将目标文件打包成的归档文件，链接时整个库被嵌入可执行程序。就像把参考书的内容全部抄进你的笔记本里，笔记本变厚了但随时能看。

**为什么**：
- 为什么用库？保护知识产权，交付时不需要给源码。
- 为什么叫"静态"？链接时就把库代码复制进可执行文件，运行时不再依赖库文件。
- 为什么体积大？每个使用它的程序都嵌入了一份完整的库代码副本。

**man手册式函数签名**：
```bash
# ar命令 - 创建静态库
ar -crs lib库名.a 目标文件.o [...]
# c: create，创建新的归档文件
# r: replace，替换归档中同名文件
# s: 创建/更新归档索引

# gcc/g++链接静态库
g++ main.cpp -L库路径 -l库名 -I头文件路径
# -L: 指定库搜索路径
# -l: 指定库名(省略lib前缀和.a后缀)
# -I: 指定头文件搜索路径
```

**完整制作流程**（配套文件 day2/static/）：

```bash
# === 准备源码 ===
# header/add.h
#ifndef _ADD_H_
#define _ADD_H_
int add(int m, int n);      // 函数声明
#endif

# src/add.cpp
int add(int m, int n)
{
    return m+n;
}

# src/main.cpp
#include<iostream>
#include<stdio.h>
#include "add.h"
using namespace std;
int main(int argc, const char *argv[])
{
    cout << add(3,8) << endl;   // 调用外部库中的函数
    return 0;
}

# === 制作静态库 ===
# 第1步：编译生成目标文件（只编译不链接）
gcc -c src/add.cpp -o add.o

# 第2步：打包成静态库
ar -crs libadd.a add.o
# 产物：libadd.a

# === 使用静态库 ===
g++ src/main.cpp -L. -ladd -Iheader -o static_demo
# -L. 表示在当前目录找库
# -ladd 表示链接libadd.a
# -Iheader 表示在header目录找头文件

./static_demo
# 输出：11
```

**注意事项**：
- 错误示范：`ar -crs add.a add.o` → 库名不以lib开头，链接时-ladd找不到
- 正确做法：库名必须是 `lib***.a` 格式
- 错误示范：链接时 `-ladd` 写成 `-llibadd` → 编译器会自动加lib前缀，导致找liblibadd.a
- 正确做法：`-l` 后面只写库名核心部分

> **人话总结**：静态库就是把代码抄进程序里。

#### 3.3 动态库制作与使用【重点】

**是什么**：动态库(.so)在编译时只记录函数索引表，运行时才加载实际代码。就像笔记本里只写了图书馆的书目编号，用的时候再去图书馆借书。

**为什么**：
- 为什么用动态库？多个程序共享同一份库代码，节省磁盘和内存。
- 为什么叫"动态"/"共享"？运行时才加载，多进程共享同一物理内存页。
- 为什么会有"找不到.so"的问题？运行时加载器在默认路径(/lib64, /usr/lib64)找不到你的库。

**man手册式函数签名**：
```bash
# 编译生成位置无关的目标文件
g++ -fPIC -c ***.cpp -o ***.o
# -fPIC: Position Independent Code，生成位置无关代码
# 动态库加载地址不固定，必须用-fPIC

# 生成动态库
g++ -shared ***.o -o lib***.so
# -shared: 生成共享库

# 一步到位
g++ -fPIC -shared ***.cpp -o lib***.so

# 链接动态库（编译命令与静态库相同）
g++ main.cpp -L库路径 -l库名 -I头文件路径

# 设置运行时库搜索路径
export LD_LIBRARY_PATH=库的路径
```

**完整制作流程**（配套文件 day2/dynamic/）：

```bash
# === 制作动态库 ===
# 方法一：两步走
g++ -fPIC -c src/add.cpp -o add.o
g++ -shared add.o -o libadd.so

# 方法二：一步到位
g++ -fPIC -shared src/add.cpp -o libadd.so

# === 使用动态库 ===
g++ src/main.cpp -L. -ladd -Iheader -o dynamic_demo

# 直接运行会报错！
./dynamic_demo
# 输出：./dynamic_demo: error while loading shared libraries:
#        libadd.so: cannot open shared object file: No such file or directory

# === 解决方法 ===
# 方法1：设置环境变量（临时有效）
export LD_LIBRARY_PATH=.
./dynamic_demo
# 输出：11

# 方法2：拷贝到系统库目录（永久有效）
sudo cp libadd.so /lib64/
./dynamic_demo
# 输出：11

# 方法3：写入/etc/ld.so.conf并刷新
echo "/your/lib/path" | sudo tee -a /etc/ld.so.conf
sudo ldconfig
```

**注意事项**：
- 错误示范：编译动态库不加-fPIC → 链接时报错"relocation R_X86_64_32 against `.text'"
- 正确做法：动态库必须加-fPIC
- 错误示范：编译通过了就以为万事大吉 → 运行时还要能找到.so
- 正确做法："编过不算完，运行还得找路"

> **人话总结**：动态库是运行时才去借的书。

#### 3.4 静态库 vs 动态库对比【重点】

| 对比维度 | 静态库(.a) | 动态库(.so) |
|---------|-----------|------------|
| 链接时机 | 编译链接时 | 程序运行时 |
| 可执行文件大小 | 较大（嵌入完整库代码） | 较小（只含索引表） |
| 执行效率 | 较高（无需运行时加载） | 较低（首次调用有加载开销） |
| 内存占用 | 每个进程独立副本 | 多进程共享同一物理页 |
| 部署便利性 | 独立运行，无需额外库文件 | 需确保.so在搜索路径中 |
| 更新方式 | 重新编译链接整个程序 | 替换.so即可（接口不变时） |
| Windows对应 | .lib | .dll |
| Linux文件后缀 | .a | .so |
| 制作工具 | ar -crs | g++ -fPIC -shared |
| 面试题频率 | 高频 | 高频 |

**面试高频题：ldd命令**
```bash
ldd ./dynamic_demo
# 输出：
#   linux-vdso.so.1 =>  (0x00007fff...)
#   libadd.so => /path/to/libadd.so (0x00007f...)
#   libstdc++.so.6 => /lib64/libstdc++.so.6 (0x00007f...)
#   libc.so.6 => /lib64/libc.so.6 (0x00007f...)
# ldd列出程序依赖的所有动态库及其路径
# 如果某库显示 "not found"，说明运行时找不到
```

> **人话总结**：静态胖而快，动态瘦而省。

#### 3.5 第三方库使用【了解】

**是什么**：C/C++标准库之外，需要额外安装和链接的函数库。就像手机出厂自带通话功能(标准库)，但拍照App需要你另外安装(第三方库)。

**常见第三方库**：
```bash
# 数学库
#include<math.h>
# 编译时需链接：g++ main.cpp -lm
# pow/sqrt/sin/cos等函数

# 线程库
#include<pthread.h>
# 编译时需链接：g++ main.cpp -lpthread
# pthread_create/pthread_join等函数
```

**代码走读**（配套文件 day3/01math.cpp）：
```cpp
#include<iostream>
#include<math.h>
using namespace std;
int main(int argc, const char *argv[])
{
    cout << pow(2,3) << endl;   // 计算2的3次方
    return 0;
}
// 编译：g++ 01math.cpp -o math_demo -lm
// 输出：8
```

**代码走读**（配套文件 day3/02pthread.cpp）：
```cpp
#include<iostream>
#include<pthread.h>
#include<unistd.h>
using namespace std;

// 线程体函数：返回值void*，参数void*
void *task(void *arg)
{
    while(1)
    {
        cout << "hello world" << endl;
        sleep(1);              // 休眠1秒
    }
}

int main(int argc, const char *argv[])
{
    pthread_t tid;             // 线程号变量
    // 创建线程：&tid接收线程号, NULL默认属性, task线程体, NULL传参
    if(pthread_create(&tid, NULL, task, NULL) != 0)
    {
        cout << "pthread_create error" << endl;
    }
    while(1);                  // 主线程死循环保持进程存活
    return 0;
}
// 编译：g++ 02pthread.cpp -o pthread_demo -lpthread
// 输出：每秒打印一行 hello world
```

> **人话总结**：第三方库要装还要链，-l别忘掉。

---

### 模块四：Makefile工程化管理（P70-P105）

#### 4.1 Makefile概述【重点】

**是什么**：Makefile是描述项目编译规则的文本文件，make是执行Makefile的解释器。就像工厂的生产流水线说明书，告诉工人先做什么后做什么。

**为什么**：
- 为什么用Makefile？手动敲编译命令容易出错且效率低，尤其是多文件项目。
- 为什么make能增量编译？基于文件时间戳判断哪些文件需要重新编译。
- 为什么是必备技能？Linux/Unix开发、阅读开源项目、研究内核都离不开Makefile。

**核心概念**：
```
make  → 执行Makefile的工具（解释器），位于/usr/bin
Makefile → 描述编译规则的文本文件
makefile → 小写也可以，两者共存时优先用小写
```

**安装与验证**：
```bash
sudo yum install make
make --version
# 输出：GNU Make 4.2.1
```

> **人话总结**：Makefile是编译的自动化脚本。

#### 4.2 Makefile工作过程与依赖思想【重点】

**是什么**：Makefile的核心思想是"面向依赖"——定义目标与依赖的关系，make根据依赖树和时间戳决定编译顺序。就像做蛋糕要先有面粉，面粉要先买小麦。

**依赖关系图**：
```
单文件项目：
可执行程序 ← .o文件 ← .s文件 ← .i文件 ← .cpp文件

多文件项目：
可执行程序 ← main.o ← main.cpp
           ← func.o ← func.cpp
           ← util.o ← util.cpp
```

**make执行流程**：
```
1. 读取Makefile，建立依赖关系树
2. 从默认目标（第一个目标）开始
3. 检查依赖文件的时间戳
4. 如果依赖比目标新 → 执行命令重新生成目标
5. 如果依赖不比目标新 → 跳过（增量编译的核心）
6. 递归处理所有依赖
```

> **人话总结**：谁变了编谁，没变就跳过。

#### 4.3 第一个Makefile【重点】

**代码走读**（配套文件 day3/02make/Makefile）：
```makefile
# 注释以#开头

# 默认目标（第一个目标）
all:hello

# 目标:依赖
# [TAB]命令
hello:hello.o
	g++ $< -o $@
	# $< = 第一个依赖(hello.o)
	# $@ = 目标(hello)
	# 等价于：g++ hello.o -o hello

hello.o:hello.cpp
	g++ -c $< -o $@
	# 等价于：g++ -c hello.cpp -o hello.o

# 伪目标：不对应真实文件，无条件执行
.PHONY:clean
clean distclean:
	rm hello.o hello
```

**执行方式**：
```bash
make              # 执行默认目标(all→hello)
make hello        # 指定目标
make clean        # 清理编译产物
# 输出：rm hello.o hello
```

**注意事项**：
- 错误示范：命令前用空格代替tab
```makefile
hello:hello.o
    g++ hello.o -o hello    # 4个空格 → 报错！
```
- 正确写法：
```makefile
hello:hello.o
[TAB]g++ hello.o -o hello   # 必须是tab键
```
- 错误后果：`Makefile:3: *** missing separator. Stop.`
- 记忆口诀："Make只认tab，空格是路人"

> **人话总结**：目标冒号依赖，tab开头写命令。

#### 4.4 Makefile语法规则【重点】

**规则的三要素**：
```
目标(target)：目标依赖(prerequisites)
[TAB]命令(commands)
```

- 命令必须以tab键开头
- 一个规则必须有目标
- 可以没有依赖（如clean）
- 可以没有命令（仅描述依赖关系）

**目标详解**：

**(1) 默认目标**：Makefile中第一个目标，make不带参数时执行它。

**(2) 多目标**：一个规则多个目标共享同一命令和依赖。
```makefile
clean distclean:
	rm hello.[^cpp] hello
```

**(3) 多规则目标**：多个规则指向同一目标。
```makefile
all:test1
all:test2
test1:
	@echo "hello"
test2:
	@echo "world"
```
配套文件 day3/03make/Makefile 演示了此用法。

**(4) 伪目标**：不对应真实文件，永远执行。
```makefile
.PHONY:clean          # 声明clean为伪目标
clean:
	rm -f *.o operator
```
为什么需要伪目标？如果目录下恰好有个叫clean的文件，make会认为目标已是最新而不执行命令。`.PHONY`确保无条件执行。

**自动变量**：
| 变量 | 含义 | 示例 |
|------|------|------|
| `$@` | 目标文件名 | hello |
| `$^` | 所有依赖文件(去重) | main.o operator.o |
| `$<` | 第一个依赖文件 | main.o |
| `%` | 模式匹配通配符 | %.o:%.cpp |
| `*` | 普通通配符(仅命令中) | rm *.o |

注意：`%`是Makefile规则中的通配符，`*`是shell通配符，两者不能互换。

#### 4.5 变量与模式匹配【重点】

**代码走读**（配套文件 day3/04make/Makefile）：
```makefile
var1 = main.o           # 延迟展开变量
var1 += operator.o      # 追加赋值

# 条件选择
ifeq ($(COMPILE), g++)
    CC:=g++             # 立即展开变量
else
    CC:=gcc
endif

# 默认目标
all:operator

operator:$(var1)
	$(CC) $^ -o $@      # $^=所有依赖, $@=目标

# 模式匹配规则：统一处理所有.cpp→.o
%.o:%.cpp
	$(CC) -c $< -o $@   # $<=第一个依赖

clean:
	rm -f *.o operator   # *是shell通配符
```

**变量分类**：
| 类型 | 操作符 | 特点 | 使用场景 |
|------|--------|------|---------|
| 延迟展开 | `=` | 使用时才展开，取最后一次赋值 | 命令中 |
| 立即展开 | `:=` | 定义时立即展开为常量 | 目标、依赖中 |
| 追加赋值 | `+=` | 在原值后追加 | 添加依赖/选项 |
| 条件赋值 | `?=` | 仅在变量未定义时赋值 | 默认值设置 |

**条件执行**：
```makefile
ifeq ($(COMPILE), g++)      # 括号紧跟关键字，内部无多余空格
    CC:=g++
else
    CC:=gcc
endif
```

**使用方式**：
```bash
# 通过命令行传递变量
make COMPILE=g++
# 此时CC被赋值为g++

make COMPILE=gcc
# 此时CC被赋值为gcc
```

**配套文件 day3/04make/operator.h 注意点**：
```cpp
#ifndef _OPERATOR_H
#define _OPERATOE_H     // 注意：这里有个拼写错误，少了一个R
                          // 应为 _OPERATOR_H
int add(int m, int n);
#endif
```
这个拼写错误在实际项目中会导致头文件保护失效，多次包含时可能出现重复定义错误。

> **人话总结**：变量让Makefile灵活，模式匹配让它通用。

#### 4.6 CMake基础【了解】

**是什么**：CMake是跨平台的构建系统生成器，通过CMakeLists.txt描述构建规则，自动生成Makefile。就像用模板生成合同，你只需填关键信息。

**为什么**：手写Makefile复杂且不可移植，CMake一套配置可在Linux/Windows/Mac上生成对应的构建文件。

**简单项目**（配套文件 CMake/test1/）：
```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 2.8)   # 最低CMake版本
project(HELLO)                         # 项目名称
add_executable(hello_cmake hello.cpp)  # 生成可执行程序
```

```bash
# 构建步骤
mkdir build && cd build               # 创建构建目录（推荐out-of-source）
cmake ..                               # 生成Makefile
make                                   # 编译
./hello_cmake
# 输出：Hello, World!
```

**多文件项目**（配套文件 CMake/test2/）：
```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 2.8)
project(SWAP)
include_directories(include)           # 指定头文件路径(等价于-I)
add_executable(swap_cmake main.cpp src/swap.cpp)
```

> **人话总结**：CMake是Makefile的高级模板。

---

## 二、所有对比表格汇总

### 表1：Vim三种模式对比
| 模式 | 进入方式 | 主要功能 | 退出方式 |
|------|---------|---------|---------|
| 命令行模式 | 默认/ESC | 复制、删除、移动光标 | shift+:进底行/i/a等进插入 |
| 插入模式 | i/a/o/s等键 | 编辑文本内容 | ESC回命令行 |
| 底行模式 | shift+: | 保存、退出、查找替换 | ESC回命令行 |

### 表2：四步编译对比
| 阶段 | 选项 | 输入 | 输出 | 核心操作 |
|------|------|------|------|---------|
| 预处理 | -E | .cpp | .i | 展开、删注释、宏替换 |
| 编译 | -S | .i | .s | C++→汇编 |
| 汇编 | -c | .s | .o | 汇编→二进制 |
| 链接 | (默认) | .o+库 | 可执行文件 | 符号解析、合并 |

### 表3：静态库vs动态库
| 维度 | 静态库(.a) | 动态库(.so) |
|------|-----------|------------|
| 链接时机 | 编译时 | 运行时 |
| 文件大小 | 大 | 小 |
| 执行效率 | 高 | 略低 |
| 内存共享 | 否 | 是 |
| 部署 | 独立 | 需带.so |
| 更新 | 重新编译 | 替换.so |
| 制作 | ar -crs | g++ -fPIC -shared |

### 表4：Makefile变量类型
| 类型 | 符号 | 展开时机 | 适用场景 |
|------|------|---------|---------|
| 延迟展开 | = | 使用时 | 命令中 |
| 立即展开 | := | 定义时 | 目标/依赖中 |
| 追加 | += | 立即 | 累加列表 |
| 条件 | ?= | 定义时(仅首次) | 默认值 |

### 表5：GDB next vs step
| 指令 | 缩写 | 行为 | 适用场景 |
|------|------|------|---------|
| next | n | 执行下一行，不进入函数 | 信任函数内部逻辑 |
| step | s | 执行下一行，进入函数内部 | 怀疑函数有bug |

---

## 三、配套文件完整逐行讲解（代码走读）

### 3.1 day1/02demo.cpp -- C++程序框架
> 已在2.2节详细走读，此处补充关键点：
- `argc` 至少为1（argv[0]是程序名本身）
- `const char *argv[]` 也可写作 `char **argv`
- `cout << endl` 等价于 `cout << '\n' << flush`

### 3.2 day1/03file.cpp -- sys库文件操作
> 已在2.5节详细走读，补充系统调用三件套：
- `open()`：成功返回fd>=0，失败返回-1设errno
- `write()`：成功返回写入字节数，失败返回-1
- `close()`：成功返回0，失败返回-1

### 3.3 day2/01test.cpp -- C/C++混合编程注意
```cpp
#include<iostream>
//#include<stdio.h>            // 被注释掉了！
using namespace std;
int main(int argc, const char *argv[])
{
    printf("hello world\n");   // C语言函数
    return 0;
}
```
**关键点**：stdio.h被注释了，但g++编译仍可通过，因为iostream间接包含了stdio相关声明。但这是不可靠的隐式依赖，实际项目中应该显式包含所需头文件。如果用gcc编译则会报错。

### 3.4 day2/02test.c -- 纯C版本对比
与01test.cpp功能相同，但用gcc编译。体现了g++比gcc更严格的特点。

### 3.5 day2/03gdb.cpp -- GDB调试示例
> 已在3.1节详细走读。

### 3.6 day2/04test.cpp -- Core Dump触发示例
```cpp
int *ptr = NULL;       // 空指针
*ptr = 520;            // 解引用空指针 → Segmentation Fault
```
**运行时行为**：程序崩溃产生SIGSEGV信号。如果设置了`ulimit -c unlimited`，会生成core文件供GDB分析。

### 3.7 day2/05test.cpp -- 后台进程调试示例
```cpp
void test() {}                    // 空函数
void test1() {
    int num = 520;
    num++;                        // 用于GDB观察变量变化
}
int main(int argc, const char *argv[]) {
    for(;;) {                     // 无限循环
        test();
        test1();
    }
    return 0;
}
```
**用途**：演示 `gdb -p PID` 附加到运行中的进程进行调试。`for(;;)` 使程序持续运行，方便附加。

### 3.8 day2/static/ -- 静态库完整示例
> 已在3.2节详细走读。

### 3.9 day2/dynamic/ -- 动态库完整示例
> 已在3.3节详细走读。

### 3.10 day3/01math.cpp -- 数学库使用
> 已在3.5节详细走读。

### 3.11 day3/02pthread.cpp -- 线程库使用
> 已在3.5节详细走读。

### 3.12 day3/02make/ -- 基础Makefile
> 已在4.3节详细走读。

### 3.13 day3/03make/Makefile -- 多规则目标
```makefile
all:test1
all:test2
test1:
	@echo "hello"       # @抑制命令本身的输出
test2:
	@echo "world"
```
**注意**：`all:test1` 和 `all:test2` 是两个独立的规则，都表示all依赖于对应目标。make只会执行第一个all规则中的依赖(test1)，test2需要通过 `make test2` 单独执行。

### 3.14 day3/04make/ -- 完整Makefile（变量+条件+模式匹配）
> 已在4.5节详细走读。

### 3.15 CMake/test1/ -- CMake最简项目
> 已在4.6节详细走读。

### 3.16 CMake/test2/ -- CMake多文件项目
> 已在4.6节详细走读。补充swap.h中引用了 `<myhead.h>`，这是一个自定义头文件，实际编译时需要确保该文件存在于include路径中，否则会报错。

---

## 四、两套速查表

### 精简版速查表（一页速查）

**Vim**：ESC=命令行 | i=插入 | shift:+:=底行 | yy/dd/p/u | :wq保存退出 | :%s/a/b/g替换

**四步编译**：`-E`预处理.i → `-S`编译.s → `-c`汇编.o → 链接可执行

**GDB**：`g++ -g`编译 → `b`断点 → `r`运行 → `n/s`单步 → `p`打印 → `c`继续 → `q`退出

**静态库**：`gcc -c → ar -crs lib*.a → g++ -L -l -I`

**动态库**：`g++ -fPIC -shared → g++ -L -l -I → export LD_LIBRARY_PATH`

**Makefile**：`目标:依赖[TAB]命令` | `$@$^$<` | `%.o:%.cpp` | `.PHONY:clean`

**CMake**：`cmake_minimum_required → project → add_executable → mkdir build → cmake .. → make`

### 详细版速查表

| 操作 | 命令/语法 | 示例 |
|------|----------|------|
| 预处理 | `g++ -E file.cpp -o file.i` | 展开头文件 |
| 编译 | `g++ -S file.i -o file.s` | 生成汇编 |
| 汇编 | `g++ -c file.s -o file.o` | 生成二进制 |
| 链接 | `g++ file.o -o prog` | 生成可执行 |
| GDB编译 | `g++ -g file.cpp -o prog` | 带调试信息 |
| GDB启动 | `gdb ./prog` | 进入调试 |
| 设断点 | `b 行号` / `b 函数名` | b 20 / b main |
| 查看变量 | `p 变量名` | p arr@5 |
| 修改变量 | `set variable x=10` | 运行时修改 |
| Core dump | `ulimit -c unlimited` | 开启core |
| 静态库制作 | `ar -crs libname.a *.o` | 打包.o |
| 动态库制作 | `g++ -fPIC -shared src.cpp -o libname.so` | 生成.so |
| 链接库 | `g++ main.cpp -L路径 -lname -I头文件路径` | 使用库 |
| 动态库路径 | `export LD_LIBRARY_PATH=路径` | 运行时查找 |
| Makefile规则 | `target:deps[TAB]cmd` | hello:hello.o |
| 自动变量 | `$@`=目标 `$^`=全部依赖 `$<`=首个依赖 | g++ $^ -o $@ |
| 模式匹配 | `%.o:%.cpp` | 批量编译 |
| 伪目标 | `.PHONY:clean` | 无条件执行 |
| CMake构建 | `mkdir build; cd build; cmake ..; make` | 标准流程 |

---

## 五、易错点速查卡

| 错误现象 | 错误原因 | 正确写法 | 后果 |
|---------|---------|---------|------|
| Vim中输入:wq变成文本 | 在插入模式输入了底行命令 | 先ESC再shift+:再:wq | 文件内容被污染 |
| `:%s/old/new` 只替换每行第一个 | 缺少/g标志 | `:%s/old/new/g` | 替换不完整 |
| gcc编译.cpp报undefined reference | 未链接C++标准库 | 用g++编译.cpp文件 | 链接失败 |
| `./a.out: error while loading shared libraries` | 运行时找不到.so | `export LD_LIBRARY_PATH=库路径` | 程序无法启动 |
| Makefile报missing separator | 命令前用了空格 | 命令必须以tab键开头 | make终止 |
| 编译动态库报relocation错误 | 缺少-fPIC选项 | `g++ -fPIC -shared ...` | 链接失败 |
| `-llibadd` 找不到库 | -l后多加了lib前缀 | `-ladd`（编译器自动加lib） | 链接失败 |
| GDB看不到源码和变量 | 编译没加-g | `g++ -g file.cpp -o prog` | 无法源码级调试 |
| 解引用空指针Segfault | 对NULL指针写操作 | 使用前检查指针非NULL | 程序崩溃 |
| core文件不生成 | ulimit -c默认为0 | `ulimit -c unlimited` | 无法事后调试 |

---

## 六、常见陷阱专题

### 陷阱1：Vim底行模式替换命令写错导致文件损坏

**错误写法**：
```vim
:%s/old/new          " 漏掉末尾/g，只替换每行第一个匹配
```
**后果**：大量文本未被替换，如果后续操作基于替换结果，可能导致逻辑错误或数据不一致。

**正确写法**：
```vim
:%s/old/new/g        " g=global，全局替换
```
**如何记住**："g=global，全局才安心"

### 陷阱2：动态库链接成功但运行时报找不到.so

**错误写法**：
```bash
g++ main.cpp -L./lib -ladd -o demo   # 编译通过
./demo                                 # 运行报错！
# error while loading shared libraries: libadd.so: cannot open shared object file
```
**后果**：编译阶段-L只管编译时找库，运行时加载器不看-L，只在默认路径和环境变量中搜索。

**正确写法**：
```bash
# 方法1：设置环境变量
export LD_LIBRARY_PATH=./lib
./demo

# 方法2：拷贝到系统目录
sudo cp libadd.so /lib64/
./demo

# 方法3：配置ld.so.conf
echo "$(pwd)/lib" | sudo tee -a /etc/ld.so.conf
sudo ldconfig
./demo
```
**如何记住**："编过不算完，运行还得找路"

### 陷阱3：Makefile命令前用空格代替tab

**错误写法**：
```makefile
hello:hello.o
    g++ hello.o -o hello     # 4个空格缩进
```
**后果**：`Makefile:3: *** missing separator. Stop.` make直接报错退出。

**正确写法**：
```makefile
hello:hello.o
[TAB]g++ hello.o -o hello    # 必须是真正的tab字符
```
**如何记住**："Make只认tab，空格是路人"

---

## 七、新手最常问的5个问题

**Q1：g++和gcc有什么区别？**
A：gcc是GNU C编译器，只编译C语言；g++是GNU C++编译器，编译C++并自动链接C++标准库(libstdc++)。用gcc编译.cpp文件不会链接C++库，导致大量undefined reference错误。简单记：C用gcc，C++用g++。

**Q2：为什么我的动态库编译通过了但运行报错？**
A：编译时的-L只告诉编译器去哪找库来完成链接，但运行时动态链接器(ld-linux)在默认路径(/lib64, /usr/lib64)和LD_LIBRARY_PATH环境变量指定的路径中搜索.so。你需要 `export LD_LIBRARY_PATH=你的库路径` 或将.so拷贝到/lib64。用 `ldd ./程序` 可以检查依赖库是否都能找到。

**Q3：Vim怎么从插入模式保存退出？**
A：不能直接在插入模式保存退出。正确步骤：(1)按ESC回到命令行模式；(2)按shift+:进入底行模式；(3)输入wq回车。很多人卡在第一步忘了按ESC，导致:wq被当成文字输入到文件中。

**Q4：Makefile中$@、$^、$<分别是什么？**
A：这三个是自动变量。`$@`是当前规则的目标文件名；`$^`是所有依赖文件列表（去重）；`$<`是第一个依赖文件。例如规则 `hello:main.o util.o` 中，`$@`=hello，`$^`=main.o util.o，`$<`=main.o。模式规则 `%.o:%.cpp` 中，`$<`自动匹配对应的.cpp文件。

**Q5：GDB中next和step有什么区别？**
A：next(n)执行下一行代码，如果遇到函数调用会把它当作一步执行完（不进入函数内部）。step(s)执行下一行代码，如果遇到函数调用会跳入函数内部逐行调试。如果你确信函数没问题用next快速跳过；如果怀疑函数有bug用step进去看。

---

## 八、代码自测清单

学完本章后，你应该能独立完成以下操作：

- [ ] 独立完成四步编译（预处理→编译→汇编→链接）并说出每步产物文件名和后缀
- [ ] 制作并使用静态库：gcc -c → ar -crs → g++ -L -l -I
- [ ] 制作并使用动态库：g++ -fPIC -shared → 解决运行时找不到.so的问题
- [ ] 用GDB完成完整调试流程：-g编译 → 设断点 → 单步 → 查看变量 → 分析core dump
- [ ] 编写一个包含变量、模式匹配(%.o:%.cpp)、伪目标(.PHONY)的Makefile
- [ ] 用Vim完成文件的编辑、查找替换(:%s)、保存退出(:wq)全流程
- [ ] 区分静态库和动态库的区别并能口头表述
- [ ] 使用man 2/man 3查阅系统调用和库函数文档
- [ ] 使用CMake构建一个多文件C++项目

---

## 九、复习计划

| 时间 | 复习内容 | 方式 |
|------|----------|------|
| 1天后 | Vim常用命令、四步编译流程 | 默写命令 + 实际操作一遍 |
| 3天后 | 静态库/动态库制作与GDB调试 | 重做配套代码实验 |
| 7天后 | 全章回顾 | 看树状图回忆 + 做综合练习题 |
| 14天后 | Makefile变量与模式匹配 | 手写一个多文件项目的Makefile |
| 30天后 | 全章综合实战 | 从零搭建一个含库+Makefile的项目 |

---

## 十、树状图（全章知识体系）

```
第1章 Linux入门
├── 1. Linux环境搭建
│   ├── VMware虚拟机安装
│   ├── CentOS 8安装与配置
│   │   ├── sudoers权限配置
│   │   └── 阿里云镜像源切换
│   ├── 网络问题排查
│   │   ├── 无IP地址
│   │   ├── 主机不通
│   │   └── 无外网
│   ├── 用户管理(su/sudo/exit)
│   └── Xshell远程连接(SSH)
├── 2. Vim编辑器【重点】
│   ├── 命令行模式(yy/dd/p/u/gg/G/0/$)
│   ├── 插入模式(i/a/o/s/I/A/O/S)
│   └── 底行模式(:w/:q/:wq/:%s//g)
├── 3. C++开发环境
│   ├── gcc/g++安装与验证
│   ├── C++程序框架(#include/using/main)
│   ├── 四步编译【重点】
│   │   ├── 预处理(-E → .i)
│   │   ├── 编译(-S → .s)
│   │   ├── 汇编(-c → .o)
│   │   └── 链接(→ 可执行)
│   └── man手册(第2章系统调用/第3章库函数)
├── 4. sys库函数概览
│   ├── 文件操作(open/read/write/close)
│   ├── 进程控制(fork/exit/wait)
│   ├── 信号(kill/signal)
│   └── 网络(socket/bind/listen)
├── 5. GDB调试【重点】
│   ├── 编译-g选项
│   ├── 常用指令(b/r/n/s/c/p/set)
│   ├── Watchpoint观察点
│   ├── Core dump调试(ulimit -c)
│   └── 调试运行中进程(gdb -p)
├── 6. 库的制作【重点】
│   ├── 静态库(.a): ar -crs
│   ├── 动态库(.so): -fPIC -shared
│   ├── 对比：大小/效率/共享/部署
│   └── 第三方库(-lm/-lpthread)
├── 7. Makefile【重点】
│   ├── 依赖思想与增量编译
│   ├── 规则(目标:依赖[TAB]命令)
│   ├── 自动变量($@/$^/$</%)
│   ├── 变量(=/:=/+=/?=)
│   ├── 模式匹配(%.o:%.cpp)
│   ├── 伪目标(.PHONY)
│   └── 条件执行(ifeq/else/endif)
└── 8. CMake基础
    ├── CMakeLists.txt语法
    └── 构建流程(mkdir build→cmake→make)
```

---

## 十一、3条随身速记口诀

1. **"E预S编c汇链接成，四步变程序"** -- 四步编译选项和产物
2. **"Make只认tab，空格是路人"** -- Makefile命令缩进必须用tab
3. **"编过不算完，运行还得找路"** -- 动态库编译通过后还需配置运行时路径

---

## 十二、4道练习题（答案留空）

### 题目1（★）
请写出将hello.cpp进行四步编译生成可执行程序hello的完整命令序列，并注明每步生成的文件后缀。

考察知识点：四步编译过程

答：_______________________________________________

### 题目2（★★）
请写出制作名为libcalc.a的静态库并在main.cpp中使用它的完整命令流程。假设源文件为calc.cpp，头文件为calc.h，三者均在当前目录。

考察知识点：静态库制作与使用

答：_______________________________________________

### 题目3（★★★）
你用g++ -fPIC -shared math.cpp -o libmath.so制作了动态库，并用g++ main.cpp -L. -lmath -o app编译成功。但运行./app时报错"error while loading shared libraries: libmath.so: cannot open shared object file"。请解释原因并给出至少两种解决方案。

考察知识点：动态库运行时路径问题

答：_______________________________________________

### 题目4（★★★★·综合题）
请为一个包含main.cpp、utils.cpp、utils.h三个文件的C++项目编写一个完整的Makefile，要求：
(1) 使用变量CC定义编译器
(2) 使用模式匹配规则统一处理.cpp到.o的编译
(3) 使用自动变量$@、$^、$<
(4) 包含伪目标clean和all
(5) 支持通过命令行传入COMPILE变量切换gcc/g++

考察知识点：Makefile变量、模式匹配、伪目标、条件执行、自动变量

答：_______________________________________________

---

## 十三、错题记录 + 复习建议

> 说明：此表在完成第四阶段测试后由学习者自行填写。以下为模板。

| 题号 | 题目 | 我的错误答案 | 正确答案 | 错误原因 | 涉及知识点 | 复习建议 |
|------|------|-------------|----------|----------|-----------|----------|
| 1 | | | | | | 建议1天后复习 |
| 2 | | | | | | 建议3天后复习 |
| 3 | | | | | | 建议3天后复习 |
| 4 | | | | | | 建议7天后复习 |

---

## 十四、术语中英对照表

| 中文术语 | 英文术语 | 说明 |
|---------|---------|------|
| 虚拟机 | Virtual Machine (VM) | 模拟硬件的软件 |
| 预处理 | Preprocessing | 编译第一阶段 |
| 编译 | Compiling | 编译第二阶段 |
| 汇编 | Assembling | 编译第三阶段 |
| 链接 | Linking | 编译第四阶段 |
| 目标文件 | Object File (.o) | 汇编阶段的产物 |
| 可执行文件 | Executable | 链接阶段的产物 |
| 静态库 | Static Library (.a) | 链接时嵌入的库 |
| 动态库/共享库 | Dynamic/Shared Library (.so) | 运行时加载的库 |
| 调试器 | Debugger (GDB) | GNU项目调试器 |
| 断点 | Breakpoint | 程序暂停的位置 |
| 观察点 | Watchpoint | 变量变化时暂停 |
| 核心转储 | Core Dump | 崩溃时的内存快照 |
| 文件描述符 | File Descriptor (fd) | 内核分配的文件标识 |
| 系统调用 | System Call | 用户态请求内核服务 |
| 命名空间 | Namespace | C++的作用域管理机制 |
| 头文件 | Header File | 声明和定义的包含文件 |
| 构建系统 | Build System | 自动化编译工具链 |
| 增量编译 | Incremental Build | 只编译变化的文件 |
| 伪目标 | Phony Target | 不对应文件的Makefile目标 |
| 位置无关代码 | Position Independent Code (PIC) | 动态库必需 |
| 环境变量 | Environment Variable | 进程继承的配置变量 |
| 远程连接 | Remote Connection (SSH) | 加密的远程终端协议 |
| 文本编辑器 | Text Editor (Vim) | Linux下的命令行编辑器 |
| 命令行模式 | Command Mode | Vim的默认操作模式 |
| 插入模式 | Insert Mode | Vim的文本编辑模式 |
| 底行模式 | Last-line/Ex Mode | Vim的命令输入模式 |

---

## 附录：VSCode配置要点（课件1.4节）

课件还介绍了VSCode作为替代开发环境的配置：
1. 下载安装VSCode并安装汉化插件
2. 下载MinGW-w64编译工具并配置PATH环境变量
3. 安装C/C++扩展(C/C++ Extension Pack)
4. 单文件调试：F5启动，自动生成launch.json和tasks.json
5. 多文件编译：在tasks.json中配置g++参数，包含所有源文件

VSCode适合Windows本地开发，但本章核心内容仍以Linux终端+Vim为主，VSCode作为辅助工具了解即可。

---

> **本章关联**
> - 前置章节：C++基础篇
> - 后置章节：第2章 IO操作（open/read/write/close将在第2章深入讲解）
> - 本章是后续所有章节的环境基础，务必扎实掌握
