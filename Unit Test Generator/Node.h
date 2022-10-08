#pragma once
#include <iostream>
#include <string>
#include <vector>
struct SimpleData
{
    std::string ingredient = "";
    int amountonhand = 0,
        amountneeded = 1,
        amountresulted = 0,
        amountmadepercraft = 1;
    SimpleData(std::string I = "", int A = 0, int B = 1, int C = 1)
    {
        ingredient = I;
        amountonhand = A;
        amountmadepercraft = B;
        amountneeded = C;
    }
};
struct Node : public SimpleData
{
    Node(std::string I2 = "")
    {
        ingredient = I2;
    }
};
namespace NodeUtility
{
    // include functions that are needed to be used with the Node class here here
    // todo create function for formatting ingredient name to be used
    enum format { purple = 0, blue = 1, green = 2,yellow =3};
    formatSTRINGmode 
    std::string parsestringformat(Node &red)
    {
        /*
        0, default mode, formats string for variable declaration and to be utilized
        in math asseration method declaration.
            input: advanced alloy, output : advancedalloyN
            where N is an integer number used to help make the declaration unique in the event there are multple instances
                the same ingredient name.
        1, formats string to be utilized in docstring of math asseration method.
            input: advanced alloy, output : Advanced Alloy
        2, formats string to exclude leading and trailing whitespace
            input:   advanced alloy    , output: advanced alloy
        3, formats string to
        */
        switch (formatmode)
        {
        case /* constant-expression */:
            /* code */
            break;
        
        default:
            break;
        }
        return red.ingredient;
    }
}