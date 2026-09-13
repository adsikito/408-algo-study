// g++ -std=c++17 -O2 -o outbench outbench.cpp
// 用途：对比 endl 与 "\n" 在 10^6 次输出下的耗时
// 运行：outbench 1   使用 endl
//       outbench 2   使用 "\n"

#include <cstdio>
#include <cstdlib>
#include <chrono>
#include <iostream>

static const int N = 1000000;

static std::chrono::steady_clock::time_point t0;
static void tic() { t0 = std::chrono::steady_clock::now(); }
static long long toc() {
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count();
}

int main(int argc, char** argv) {
    int mode = (argc > 1) ? atoi(argv[1]) : 1;
    std::ios::sync_with_stdio(false);   // 两种模式都关闭同步，只对比换行符的影响
    std::cin.tie(nullptr);

    std::cout << "# 输出 " << N << " 行，" << (mode == 1 ? "endl" : "\\n") << "\n";
    tic();
    if (mode == 1) {
        for (int i = 0; i < N; ++i) std::cout << i << std::endl;   // 换行并强制刷新
    } else {
        for (int i = 0; i < N; ++i) std::cout << i << "\n";        // 只换行，不刷新
    }
    long long ms = toc();
    std::cout << "elapsed_ms\t" << ms << "\n";
    return 0;
}
