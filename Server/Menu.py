from ThetaDatabase.DBInterface import Database
from ThetaDatabase.ThetaDB import ThetaDB
from MenuCategory import MenuCategory
from item import Item


class Menu(object):
    """
    A menu object
    """
    def __init__(self, db_ref: Database):
        """
        Constructor of the menu object
        """
        self.database = db_ref
        if not self.database.table_exists("Menu"):
            self.database.create_table("Menu")

    def addCategory(self, c: MenuCategory):
        """
        Add category in the menu (each of which has items)
        """
        dict = MenuCategory.convert_to_dictionary(c)
        category = {"CategoryName": dict['_name'], "ListOfItems": dict['_listOfItems']}
        self.database.insert("Menu", category)

    def list_of_categories(self):
        """
        Returns all categories in the menu
        """
        return self.database.get_all_entries("Menu")


# Testing all the methods
if __name__ == '__main__':
    test_db: Database = ThetaDB("testdir")
    menu = Menu(test_db)   # create an instance of the Menu

    # create 1st category & add items in the category
    category1 = MenuCategory("Dessert")
    item1 = Item("cheesecake", ['cheese, flour'], "Dessert", "10.0", "10")
    item2 = Item("ice cream", ['milk', 'sugar', 'cream'], "Dessert", "5.0",  "14")
    category1.addItem(item1)
    category1.addItem(item2)

    # add first category in the menu
    menu.addCategory(category1)
    # create 2nd category & add items in the category
    category2 = MenuCategory("Main Course")
    item3 = Item("Pizza", ['flour', 'cheese', 'yeast'], "Main Course", "15.0",  "13")
    item4 = Item("Burger", ['cheese', 'bun', 'patty'], "Main Course", "13.0",  "10")
    category2.addItem(item3)
    category2.addItem(item4)

    # add second category in the menu
    menu.addCategory(category2)

    # check if table for menu exists
    result = menu.database.table_exists("Menu")
    if result is False:
        print("Test failed: database does not have a table for \"Menu\"!")
    else:
        print("Test passed: table for \"Menu\" exists in the database.")

    # check if categories have been added to the database
    categories = menu.list_of_categories()

    if categories[0]['CategoryName'] != MenuCategory.getName(category1):
        print("Test failed: database does not have the category with name: " + MenuCategory.getName(category1) + "!")
    else:
        print("Test passed: category with name \"" + MenuCategory.getName(category1) + "\" has been added to database.")

    if categories[1]['CategoryName'] != MenuCategory.getName(category2):
        print("Test failed: database does not have the category with name: " + MenuCategory.getName(category2) + "!")
    else:
        print("Test passed: category with name \"" + MenuCategory.getName(category2) + "\" has been added to database.")

    # drop the menu table
    test_db.drop_table("Menu")

