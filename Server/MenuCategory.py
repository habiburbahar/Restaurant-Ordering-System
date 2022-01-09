from item import Item


class MenuCategory(object):
    """
    A menu category object
    """
    def __init__(self, name):
        """
        constructor for menu category
        """
        self._name = name        # name of the category
        self._listOfItems = []   # list of items in the category

    def addItem(self, i: Item):
        """
        Add item in the menu category

        i: given item to be added in the list of items
        """
        if Item.get_category(i) != self.getName():
            raise Exception("Tried to add item from a different category")
        self._listOfItems.append(i)

    def getName(self):
        """
        Returns the name of the category
        """
        return self._name

    def get_list_of_items(self):
        """
        Returns the list of all items in the category
        """
        return self._listOfItems

    def toString(self):
        """
        Convert the MenuCategory object into string format
        """
        result = ''
        result += "-- Category: " + self._name + " --\n"
        x = "1"
        for item in self._listOfItems:
            result += "item no. "
            result += x + "\n"
            result += "Name: " + Item.get_name(item) + "\nCost: " + Item.get_cost(item) + "\n"
            x = int(x)
            x += 1
            x = str(x)
        return result

    def convert_to_dictionary(self):
        """
        Convert menu category into a dictionary format and return it
        """
        temp = self._listOfItems    # save the current list of item objects
        itemDictionary = []
        for item in self._listOfItems:
            itemDictionary.append(item.__dict__)  # convert each item object into dictionary and add it in the dict list
        self._listOfItems = itemDictionary
        dictionaryVersion = {}
        dictionaryVersion.update(self.__dict__)      # now convert the entire menu category object into dictionary
        self._listOfItems = temp    # restore the original list of items (before conversion)
        return dictionaryVersion    # return the dictionary version


# test the methods
if __name__ == '__main__':
    category = MenuCategory("Dessert")
    item1 = Item("cheesecake", ['cheese, flour'], "Dessert", "10.0", "10")
    item2 = Item("ice cream", ['milk', 'sugar', 'cream'], "Dessert", "5.0",  "14")

    # testing addItem()
    category.addItem(item1)
    category.addItem(item2)

    expected_str = "-- Category: Dessert --\nitem no. 1\nName: cheesecake\nCost: 10.0\nitem no. 2"
    expected_str += "\nName: ice cream\nCost: 5.0\n"

    test = category.toString()

    if test != expected_str:
        print("Testing Failed!")
    else:
        print("Test Passed.")

    # check if the exception is being raised if item from different category is being added
    category2 = MenuCategory("Main Course")
    item3 = Item("Donuts", ['flour', 'sugar', 'yeast'], "Dessert", "15.0", "13")
    try:
        category2.addItem(item3)
        print("Test Failed!")
    except:
        print("Test Passed.")

    # check if the category is being converted into dictionary successfully
    dictionary = category.convert_to_dictionary()
    if dictionary['_name'] != category.getName():
        print("Test Failed!")
    else:
        print("Test Passed.")
    print("\n" + category.toString())
