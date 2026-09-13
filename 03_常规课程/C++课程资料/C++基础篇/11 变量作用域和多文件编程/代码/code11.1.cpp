
#include <iostream>

using namespace std;

int num = 1;

int func() {
	static int num = 5;
	return num--;
}

void func2() {

	static int v1 = 0;
	int v2 = 0;
	v1++;
	v2++;
	cout << "v1=" << v1 << "  v2=" << v2 << endl;
}

int total = 0;
void func3() {
	total++;
}

int main() {


	func3();
	func3();
	func3();
	func3();

	cout << total << endl;

	/*func2();
	func2();
	func2()*/;

	/*for (; num <= 5; num++)
		cout << num << "   " << func() << endl;*/


	/*int num = 888;
	cout << "main num:" << num << endl;
	func();*/

	



	//int num = 2;
	//func1();
	//cout << "main num:" << num << endl;


//	int num = 100;  //局部变量
//
//	//cout << v1 << endl;
//	int v2 = 121;
//	if (1 > 0) {
//		int v2 = 10;
//		cout << "v2 if:" << v2 << endl;
//	}
//
//	cout << "v2 main:" << v2 << endl;
//
	return 0;
}

