// Unit Test Generator.cpp : This file contains the 'main' function. Program execution begins and ends there.
#include "Node.h"
#include <cmath>
void populate(Node *current);
void recursivearithmetic(Node *current);
void inverserecursivearithmetic(Node *current);
int main()
{
    std::ofstream generatedunittest("autogeneratedtest.py");
    // prompt name of head item
    std::cout << "Name of Linked List:" << std::endl;
    std::string headname = "";
    std::getline(std::cin, headname);
    auto head = new Node(headname,nullptr);
    // prompt ingredient
    populate(head);
    // set assert values
    inverserecursivearithmetic(head);
    // cleanup and terminate process
    NodeUtility::generatateunittest(head, generatedunittest);
    NodeUtility::destroy(head);
    return 0;
}
void populate(Node *current)
{
    std::vector<std::string> userinputs;
    std::cout << "What do you need to create " << current->ingredient << ":" << std::endl;
    std::string myinput = "";
    do {
        std::getline(std::cin,myinput);
        if (not myinput.empty())
        {
            userinputs.emplace_back(myinput);
        }
    } while (not myinput.empty());
    std::cout << "ad\n";
}
void inverserecursivearithmetic(Node *current)
{
    // create assert values
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started:
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
