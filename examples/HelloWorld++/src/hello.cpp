#include <string>
#include <vector>
#include <iostream>

int main(int argc, char* argv[])
{
	std::vector<std::string> parameters(argc, argv + argc);
	std::cout << "Hello, World!" << std::endl;
}
