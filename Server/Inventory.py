from typing import Collection
from ThetaDatabase.DBInterface import Database
from ThetaDatabase.ThetaDB import ThetaDB
from item import Item

class Inventory:
    """Inventory Object
    """
    def __init__(self,Database):
        """
        Inventory constructor
        
        Paramter:
            Database :  a database
        """
        self.database = Database
        
        if not self.database.table_exists("inventory"):     # if table doesn't exist create new table
            self.database.create_table("inventory")
            
    def add_item(self,item):
        """
        :param
            item - an object of item
        return:
            an unique id of the new item object
        """
        item_dict=vars(item)                                # vars() will convert object into dictionary
        
        return self.database.insert("inventory",item_dict)
        
    def search_item(self,item_name):
        """Search item in the inventory
        :param:
                item_name[string]: name of the item
                matchval[int]: value of the item to match 
        Returns:
            all the matching entries from the inventory
        """
        return self.database.select("inventory","name",item_name)  
    
    def changeItemQuantity(self,quantity,id):
        """ change quantity of an item in the inventory
        :param
            quantity ([int]): quantity to set for an item
            id ([int]): an unique id of the item
        """
        
        item_dict = self.database.get_entry("inventory",id)
        
        item_dict['quantity']=quantity
        try:
            self.database.replace_entry("inventory",id, item_dict)
        except:
            pass
        return item_dict
        
    def get_listOfItems(self):
        """
            returns list of item from the inventory
        """
        return self.database.get_all_entries("inventory")                               

if __name__ == '__main__':
    test_db: Database = ThetaDB("testdir")      
    inventory = Inventory(test_db)          # create inventory table
    
    # two item object
    item1 = Item("Baked Mustard Horse",["Mustard", "Horse", "Paprika"],"entree",1099,15)
    item2 = Item("Ginger Yogurt",["Ginger", "Vanilla", "Yogurt"],"drink",599,60)
    
    # test cases for add item 
    item1_id = inventory.add_item(item1)        # add item to the inventory
    item2_id = inventory.add_item(item2)
    
    # item dictionary from the database
    item1_dict= inventory.database.get_entry("inventory",item1_id)
    if item1.get_name() == item1_dict["name"]:
        print("Test Passed: add_item")
    else:
        print("Test failed: add_item")
    
    # test cases for search item
    search = inventory.search_item("Baked Mustard Horse")
    for item in search:
        item_search = item
    if item_search["id"] == item1_id:
        print("Test Passed: search_item")
    else:
        print("Test failed: search_item")
    
    # test cases for change item quantity
    inventory.changeItemQuantity(7,item2_id)
    item2_dict=inventory.database.get_entry("inventory",item2_id)
    
    if item2_dict["quantity"] == 7:
        print("Test Passed: changeItemQuantity")
    else:
        print("Test Failed: changeItemQuantity")
    
    # test cases for get_listOfItems
    count = 0
    for item in inventory.get_listOfItems():
        count +=1
    if (count == 2):
        print("Test Passed: get_listOfItems")
    else:
        print("Test Failed: get_listOfItems")
    
    test_db.drop_table("inventory")