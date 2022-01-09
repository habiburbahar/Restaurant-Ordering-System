import unittest
from item import Item

class TestItem(unittest.TestCase):
    """Test case for the Item class
    """
    # test case for get_item method   
    def test_get_name(self):
        t = Item("Baked Mustard Horse",["Mustard", "Horse", "Paprika"],"entree",1099,15)
        output = t.get_name()
        if self.assertEqual(output, "Baked Mustard Horse") == None:
            print("Test Passed: get_item")
        else: 
            print("Test Failed: get_item") 
    
    # test case for get_ingredients method    
    def test_get_ingredients(self):
        t = Item("Baked Mustard Horse",["Mustard", "Horse", "Paprika"],"entree",1099,15)
        output = t.get_ingredients()
        if self.assertEqual(output,["Mustard", "Horse", "Paprika"]) == None:
            print("Test Passed: get_ingredients")
        else:
            print("Test Failed: get_ingredients")
    
    # test case for get_category method    
    def test_get_category(self):
        t = Item("Baked Mustard Horse",["Mustard", "Horse", "Paprika"],"entree",1099,15)
        output = t.get_category()
        if self.assertEqual(output,"entree") == None:
            print("Test Passed: get_category")
        else:
            print("Test Failed: get_category")
            
    # test case for get_cost method    
    def test_get_cost(self):
        t = Item("Baked Mustard Horse",["Mustard", "Horse", "Paprika"],"entree",1099,15)
        output = t.get_cost()
        if self.assertEqual(output, 1099) == None:
            print("Test Passed: get_cost")
        else:
            print("Test Failed: get_cost")
    
    # test case for get_quantity method    
    def test_get_quantity(self):
        t = Item("Baked Mustard Horse",["Mustard", "Horse", "Paprika"],"entree",1099,15)
        output = t.get_quantity()
        if self.assertEqual(output, 15) == None:
            print("Test Passed: get_quantity")
        else:
            print("Test failed: get_quantity")
    
    # test case for set_cost method    
    def test_set_cost(self):
        t = Item("Baked Mustard Horse",["Mustard", "Horse", "Paprika"],"entree",1099,15)
        t.set_cost(1200)
        output = t.get_cost()
        if self.assertEqual(output, 1200) == None:
            print("Test Passed: set_cost")
        else:
            print("Test failed: set_cost")
            
    # test case for set_quantity method    
    def test_set_quantity(self):
        t = Item("Baked Mustard Horse",["Mustard", "Horse", "Paprika"],"entree",1099,15)
        t.set_quantity(7)
        output = t.get_quantity()
        if self.assertEqual(output, 7) == None:
            print("Test Passed: set_quantity")
        else:
            print("Test Failed: set_quantity")
            
    # test case for set_category method    
    def test_set_category(self):
        t = Item("Baked Mustard Horse",["Mustard", "Horse", "Paprika"],"entree",1099,15)
        t.set_category("side")
        output = t.get_category()
        if self.assertEqual(output, "side") == None:
            print("Test Passed: set_category")
        else:
            print("Test Failed: set_category")
        
t = TestItem()
t.test_get_name()
t.test_get_ingredients()
t.test_get_category()
t.test_get_cost()
t.test_get_quantity()
t.test_set_quantity()
t.test_set_cost()      
t.test_set_category()