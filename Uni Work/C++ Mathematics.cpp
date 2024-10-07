#include <iostream>
#include <string>
using namespace std;

float input1;
float input2;

int calc() {
    float add = input1 + input2;
    float sub = input1 - input2;
    float mult = input1 * input2;
    float div = input1 / input2;
    int inputint1 = input1;
    int inputint2 = input2;
    int mod = inputint1 % inputint2;
    std::cout << "Added: " << add << "\n";
    std::cout << "Subtracted: " << sub << "\n";
    std::cout << "Multiplied: " << mult << "\n";
    std::cout << "Divided: " << div << "\n";
    std::cout << "Modulated: " << mod << "\n";
    return 0;
}

int main()
{
    std::cout << "Enter First Number: ";
    cin >> input1;
    std::cout << "Enter Second Number: ";
    cin >> input2;
    calc();



}


