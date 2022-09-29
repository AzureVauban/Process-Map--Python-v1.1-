"""rework this fit current development progress on V2
- This is a reworked version of the Process Map (Python) V1, use as base for future versions
- Mode A : The user figures out how much of item A can they make given the their supply of item
B,C,D...
- Mode B: The user figures out how much of item B,C,D... they need to get their desired amount of A
"""
import math
import sys

programmodetype: int = 0


class NodeB:
    """class for storing simple data about an item such as its name and how much is needed to create
    its parent
    """
    ingredient: str = ''
    amountonhand: int = 0
    amountneeded: int = 0
    amountmadepercraft: int = 0
    amountresulted: int = 0
    queueamountresulted: dict = {}

    def __init__(self, name: str = '', red: int = 0, blue: int = 1, yellow: int = 1) -> None:
        """_summary_

        Args:
            name (str, optional): name of the item. Defaults to ''.
            red (int, optional): amount of the item you have on hand. Defaults to 0.
            blue (int, optional): amount of the parent item you create each time you craft it.
            Defaults to 1.
            yellow (int, optional): amount of item needed to craft the parent item one time.
            Defaults to 1.
        """
        self.amountonhand = red
        self.amountmadepercraft = blue
        self.amountneeded = yellow
        self.queueamountresulted = {}
        self.ingredient = name
        self.amountresulted = 0


class Node(NodeB):
    """stores identifiable features of an item, such as the parent and children instances
    Args:
        primary (_type_): parent class of item
    """
    parent = None
    children: dict = {}
    generation: int = 0
    instances: int = 0
    instancekey: int = 0
    endpoints: dict = {}  # only to be use with recursive reverse arithmetic method

    def __init__(self, name: str = '', par=None, red: int = 0, blue: int = 1, yellow: int = 1) -> None:
        """default constructor for Node instance, stores identifying features of an item's
        information

        Args:
            name (str, optional): name of the item. Defaults to ''.
            pare (class, optional): parent instance of declared Node. Defaults to None
            red (int, optional): amount of the item you have on hand. Defaults to 0.
            blue (int, optional): amount of the parent item you create each time you craft it.
            Defaults to 1.
            yellow (int, optional): amount of item needed to craft the parent item one time.
            Defaults to 1.
        """
        super().__init__(name, red, blue, yellow)
        self.endpoints = {}
        self.instancekey = Node.instances
        self.children = {}
        self.parent = par
        if self.parent is not None:
            self.generation = self.parent.generation + 1
            self.parent.children.update({self.instancekey: self})
        else:
            self.generation = 0
        Node.instances += 1
        if __name__ == '__main__':
            #! this line is added so that it doesn't mess up the Node instance unit testing
            self.__inputnumerics()

    def __inputnumerics(self):
        """prompt input of the numeric data for the instance from the user"""
        while True and programmodetype == 0:
            #! ^^^ tentative, might have to update based on whichever mode:
            print('How much',self.ingredient,'do you have on hand: ')
            self.amountonhand = self.__promptint()
            if self.amountonhand < 0:
                print('That number is not valid')
            else:
                break
        if self.parent is not None:
            while True:
                print('How much',self.ingredient,'do you need to craft',self.parent.ingredient,'1 time: ')
                self.amountneeded = self.__promptint()
                if self.amountneeded < 1:
                    print('That number is not valid')
                else:
                    break
            while True:
                print('How much',self.parent.ingredient,'do you create each time you craft it: ')
                self.amountmadepercraft = self.__promptint()
                if self.amountmadepercraft < 1:
                    print('That number is not valid')
                else:
                    break

    def __promptint(self) -> int:
        """prompt the user to input a returnable integer

        Returns:
            int: an interger that is used to set the amountneeded, amount on hand, and
            the amount made per craft for a Node instance
        """
        mynum: int = 0
        while True:
            temp = input('')
            if not temp.isdigit():
                print('you can only type in a postive interger')
            else:
                mynum = int(temp)
                break
        return mynum
    def clearentirequeue(self):
        """clears out the entire amount resulted queue, utilized in Mode B
        """
        if len(self.children) > 0:
            for child in self.children.items():
                if isinstance(child[1],Node):
                    child[1].queueamountresulted.clear()
                    child[1].clearentirequeue()            
                else:
                    raise TypeError('Child is not an instance of',Node)
        
            
    def findlocalendpoints(self) -> dict:
        """look for endpoints connected to the tree at this node
        """
        Node.endpoints.clear()
        if len(self.children) > 0:
            for childinstance in self.children.items():
                if isinstance(childinstance[1], Node):
                    childinstance[1].findlocalendpoints()
        else:
            Node.endpoints.update({self.instancekey: self})
        return Node.endpoints


def recursivearithmetic(cur: Node) -> int:
    """figure out the amount resulted of the augment Node instance,
    math function used: D = (B/C)A + (B/C)(min(Dqueue))
    - if there is no values in the queue it will default to 0
    Returns:
        int: returns the amount resulted of augment Node instance
    """
    # check and set minimum if queue is not empty
    tentativeinterger: int = sys.maxsize
    if len(cur.queueamountresulted) == 0:
        tentativeinterger = 0
    else:
        for myinterger in cur.queueamountresulted.items():
            if myinterger[1] < tentativeinterger:
                tentativeinterger = myinterger[1]
    # tenative arithmetic code
    red = (cur.amountmadepercraft / cur.amountneeded)
    black = (red*cur.amountonhand) + (red*tentativeinterger)
    black = round(math.floor(black))
    cur.amountresulted = black
    # recursively call the method
    if cur.parent is not None:
        cur.parent.queueamountresulted.update({cur.ingredient: cur.amountresulted})
        recursivearithmetic(cur.parent)
    elif cur.parent is None and programmodetype == 1:
        #todo clear out entire tree resulted queue
        cur.clearentirequeue()
    return cur.amountresulted


def reversearithmetic(cur: Node,desirednum : int) -> int:
    """figure out how much of the endpoint nodes you need to get the desired amount of
    the head most item
    """
    #todo edit/fix method docstring, 
    #todo always results in 0 - potential cause is the amount resulted queue buffer not being reset when 
    #     head.amountresulted comparison is made, check/debug that code
    # set cur to head node
    while cur.parent is not None:
        cur = cur.parent
    # set and utilize the searching method to find the endpoints of the head node
    endpoints: dict = cur.findlocalendpoints()
    # ? increase the amount on hand of each endpoint item until amount resulted of the head node is
    # ? the same as the desired amount, which is the amount resulted just in Mode B
    while recursivearithmetic(cur) <= desirednum:
        for endpoint in endpoints.items():
            if isinstance(endpoint, Node):
                endpoint[1].amountonhand += 1
            if isinstance(endpoint[1].parent, Node):
                recursivearithmetic(endpoint[1])
            elif cur.amountresulted >= desirednum:
                break
            else:
                raise TypeError('endpoint parent is not an instance of', Node)
    return cur.amountresulted


def searchforendpoint(cur: Node):
    """looks for endpoint nodes to start the math method from
    """
    if len(cur.children) > 0:
        for childinstance in cur.children.items():
            searchforendpoint(childinstance[1])
    elif len(cur.children) == 0 and programmodetype == 1:
        pass
    else:  # default mode (mode A)
        recursivearithmetic(cur)


def populate(cur: Node):
    """creates new child instances during script runtime

    Args:
        cur (Node): parent instance, creates children instances for this node

    Raises:
        TypeError: this method continues recursively, if the child is not an instance
        of the same class as the augment, this is unintended behavior and will raise an error
        to catch it
    """
    inputqueue: dict = {}
    checkstring: str = cur.ingredient
    # output ingredient trail
    if cur.parent is not None:
        temp: Node = cur
        print('TRAIL: ', end='')
        while True:
            if temp.parent is not None:
                print(temp.ingredient, '-> ', end='')
                temp = temp.parent
            else:
                print(temp.ingredient)
                break
        checkstring = temp.ingredient
    # prompt user to input ingredienta
    print('What ingredients do you need to create', cur.ingredient, end=':\n')
    while True:
        myinput = input('')
        myinput = myinput.strip()
        #! input checking
        duplicated: bool = False
        if len(inputqueue) > 0:
            for word in inputqueue.items():
                duplicated = word[1] == checkstring
                if duplicated:
                    break
        if duplicated:
            print('You already typed that in')
        elif myinput == checkstring:
            print('Invalid input, we are trying to make that item!')
        elif myinput == cur.ingredient:
            print('You cannot type that in')
        elif len(myinput) == 0:
            break
        else:
            inputqueue.update({len(inputqueue): myinput})
    # create new child instances
    for newnodename in inputqueue.items():
        newchild: Node = Node(newnodename[1], cur)  # pylint:disable=W0612
    # continue method runtime
    for childinstance in cur.children.items():
        if isinstance(childinstance[1], Node):
            populate(childinstance[1])
        else:
            raise TypeError('child is not an instance of', Node)


if __name__ == '__main__':
    # Mode B: How much of Item B,C,D (endpoint instances), would I need to make X amount of item A
    # prompt user which mode they want to run the program in
    while True:
        print('Which mode do you want to use:')
        print('Mode A - You are trying to figure out how much of your desired item you can make with the current supply of materials (Type in A)')
        print('Mode B - You are trying to figure out how much base materials you need to create a certain amount of your desired item, (Type in B)')
        usermode = (input(''))
        usermode = usermode.strip()
        #todo add comparison through uppercase
        if usermode != 'A' and usermode != 'B':
            print('That input is not valid')
        elif usermode == 'B':
            programmodetype = 1
            break
        else:
            programmodetype = 0
            break
    # prompt user to type in the name of the item they want to create
    while True:
        itemname = input('What is the name of the item you want to create: ')
        itemname = itemname.strip()
        if len(itemname) == 0:
            print('You must type something in')
        else:
            break
    head = Node(itemname, None)
    if programmodetype == 0:  # ? normal program mode
        populate(head)
        searchforendpoint(head)
        print('# resulted of', head.ingredient, '',
              end=str(head.amountresulted)+'\n')
    else:  # ? current developing program mode
        desirednumber: int = 0
        print('How much', head.ingredient, 'do you want to create:')
        desirednumber = int(input(''))
        #todo add input validatin for desired number
        populate(head)
        #todo rework reverse arithmetic method
        reversearithmetic(head, desirednumber)
        # output resulted numbers for endpoints
        print('Needed amounts of your basemost ingredients to get',
              desirednumber, 'x', head.ingredient, ':')
        # print amount needed of endpoint items, format input smiliarily to a list
        for child in head.findlocalendpoints().items():
            if isinstance(child[1], Node):
                print(child[1].ingredient, ':', child[1].amountonhand, 'x')
            else:
                raise TypeError('child is not an instance of', Node)
    # prompt the user if they want to figure out the amount resulted of another item
    print('terminating process')
