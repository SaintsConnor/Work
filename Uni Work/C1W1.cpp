// Creator: Connor Pester
// Date: 4th September 2024
// Title: COMP100 - C1W1 - Exercise 1
// Description: Completes the tasks outlined in the COMP1000 - C1W1 - Exercise 1 document.


#include <iostream>
#include <string>


// Variables 
int num1 = 5;
int num2 = 3; 
int sum;

// Sub Functions
int Task1() {
	// C++ program to declare two integer variables, initialize them with values, and then output their sum.
	sum = num1 + num2; 
	std::cout << "The sum of " << num1 << " and " << num2 << " is " << sum << std::endl; 
	std::cout << "\n";
	return 0;
}

int Task2() {
	// C++ program that calculates and prints the product of two numbers (5 and 3) using a multiplication operator.
	sum = num1 * num2; 
	std::cout << "The product of " << num1 << " and " << num2 << " is " << sum << std::endl;
	std::cout << "\n";
	return 0;
}

int Task3() {
	// C++ program that uses a for loop to print numbers from 1 to 10.
	for (int i = 1; i <= 10; i++) 
		std::cout << "The number is: " << i << std::endl;
	std::cout << "\n";
	return 0;
	}


// Main Function
int main() {
	// Calls each function in order

	std::cout << "Task 1: " << std::endl;
	Task1();

	std::cout << "Task 2: " << std::endl;
	Task2();

	std::cout << "Task 3: " << std::endl;
	Task3();
	
	return 0;


}