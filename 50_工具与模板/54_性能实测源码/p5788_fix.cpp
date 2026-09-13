// g++ -std=c++17 -O2 -o p5788_fix p5788_fix.cpp
// 验证 P5788 修正代码的算法正确性
// 注意：此处使用显式头文件而非 bits/stdc++.h
//       因为本地 MinGW-W64 g++ 8.1.0 的 bits/stdc++.h 会拉入 filesystem 而编译失败
#include <cstdio>
#include <stack>
#include <iostream>
using namespace std;

const int MAXN = 3000000 + 5;
int n;
int a[MAXN];
int ans[MAXN];
stack<int> s;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    for (int i = 1; i <= n; ++i) cin >> a[i];

    for (int i = n; i >= 1; --i) {
        while (!s.empty() && a[s.top()] <= a[i]) s.pop();
        ans[i] = s.empty() ? 0 : s.top();
        s.push(i);
    }
    for (int i = 1; i <= n; ++i) cout << ans[i] << " \n"[i == n];
    return 0;
}
