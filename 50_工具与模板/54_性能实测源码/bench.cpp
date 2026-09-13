// g++ -std=c++17 -O2 -o bench bench.cpp
// 用途：对比四种输入方式读取 3×10^6 个整数的耗时
// 运行：bench 0 > in.txt   （生成测试数据）
//       bench 1 < in.txt   （cin 默认同步）
//       bench 2 < in.txt   （cin 关闭同步 + 解绑）
//       bench 3 < in.txt   （scanf）
//       bench 4 < in.txt   （手写快读）

#include <cstdio>
#include <cstdlib>
#include <chrono>
#include <iostream>
#include <string>

static const int N = 3000000;   // 与 P5788 的 n 上界一致

// ---------- 工具：毫秒计时 ----------
static std::chrono::steady_clock::time_point t0;
static void tic() { t0 = std::chrono::steady_clock::now(); }
static long long toc() {
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count();
}

// ---------- 模式 0：生成测试数据 ----------
static void gen() {
    std::ios::sync_with_stdio(false);
    std::string out;
    out.reserve((size_t)N * 8);
    unsigned int seed = 12345u;
    for (int i = 0; i < N; ++i) {
        seed = seed * 1103515245u + 12345u;      // 线性同余，保证可复现
        int v = (int)((seed >> 16) % 1000000);
        out += std::to_string(v);
        out += (i + 1 == N) ? '\n' : ' ';
    }
    fwrite(out.data(), 1, out.size(), stdout);
}

// ---------- 模式 1：cin，保持默认同步 ----------
static void mode_cin_plain() {
    tic();
    long long sum = 0;
    for (int i = 0; i < N; ++i) { int x; std::cin >> x; sum += x; }
    long long ms = toc();
    std::cout << "cin_default\t" << ms << "\tsum=" << sum << "\n";
}

// ---------- 模式 2：cin，关闭同步并解绑 ----------
static void mode_cin_sync_off() {
    std::ios::sync_with_stdio(false);   // 关闭与 C 标准流的同步
    std::cin.tie(nullptr);              // 解绑 cin 与 cout，避免每次读入前刷新 cout
    tic();
    long long sum = 0;
    for (int i = 0; i < N; ++i) { int x; std::cin >> x; sum += x; }
    long long ms = toc();
    std::cout << "cin_sync_off\t" << ms << "\tsum=" << sum << "\n";
}

// ---------- 模式 3：scanf ----------
static void mode_scanf() {
    tic();
    long long sum = 0;
    for (int i = 0; i < N; ++i) { int x; scanf("%d", &x); sum += x; }
    long long ms = toc();
    printf("scanf\t\t%lld\tsum=%lld\n", ms, sum);
}

// ---------- 模式 4：手写快读（getchar 逐字符） ----------
static inline int read_int() {
    int x = 0, f = 1;
    char c = (char)getchar();
    while (c < '0' || c > '9') { if (c == '-') f = -1; c = (char)getchar(); }
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = (char)getchar(); }
    return x * f;
}
static void mode_fast_read() {
    tic();
    long long sum = 0;
    for (int i = 0; i < N; ++i) sum += read_int();
    long long ms = toc();
    printf("fast_read\t%lld\tsum=%lld\n", ms, sum);
}

int main(int argc, char** argv) {
    int mode = (argc > 1) ? atoi(argv[1]) : 1;
    switch (mode) {
        case 0: gen();            break;
        case 1: mode_cin_plain(); break;
        case 2: mode_cin_sync_off(); break;
        case 3: mode_scanf();     break;
        case 4: mode_fast_read(); break;
        default: fprintf(stderr, "mode 0-4\n"); return 1;
    }
    return 0;
}
