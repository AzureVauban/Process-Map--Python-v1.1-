#include "Node.h"
int main()
{
    std::ofstream generatedunittest("autogenerated_unittest.py");
    //prompt name of head item
    std::cout << "What is the name of the item:" << std::endl;
    std::string headname = "";
    std::getline(std::cin,headname);
    Node head(headname);
    //test output of string formatter function
    std::cout << "Formatted String: " << NodeUtility::parsestringformat(head) << std::endl;
    // 
    return 0;
}
