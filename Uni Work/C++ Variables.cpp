#include <iostream>
#include <string>
using namespace std;

std::string name = "Alice";
int Age = 20;
float Height = 1.65;
char Grade = 'D';
int print() {
    std::cout << "\n" << "Printing User Info" << "\n";
    std::cout << "Name: " << name << "\n";
    std::cout << "Age: " << Age << "\n";
    std::cout << "Height: " << Height << "\n";
    std::cout << "Grade: " << Grade << "\n";
    return 0;
}

int main()
{

    print();
    name = "Bob";
    Age = 22;
    Height = 1.75;
    Grade = 'A';
    print();

}


