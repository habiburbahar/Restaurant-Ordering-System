from typing import List


class Item:
    """ Item Object
    """
    
    def __init__(self, name:str,ingredients:list, category:str, cost:int, quantity:int):
      
        """Constructor of the item object
        """
        self.category = category
        self.cost = cost
        self.name = name
        self.ingredients = ingredients
        self.quantity = quantity

    def get_name(self):
        """get name of the item

        Returns:
            [string]: [item name]
        """
        return self.name
    def get_cost(self):
        """get cost of the item

        Returns:
            [int]: [item cost]
        """
        return self.cost
    def get_category(self):
        """get category of the item

        Returns:
            [string]: [item_category]
        """
        return self.category

    def get_ingredients(self):
        """get ingredients of item

        Returns:
            [list]: [item ingredients]
        """
        return self.ingredients

    def get_quantity(self):
        """get quantity of the item

        Returns:
            [int]: [item quantity]
        """
        return self.quantity
    
    def set_quantity(self,quantity):
        """
            quantity ([int]):items quantity can be set
        """
        self.quantity = quantity
    def set_cost(self,cost):
        """
            cost ([int]): [items cost can be set]
        """
        self.cost = cost
    
    def set_category(self,category):
        """
            category ([string]): [category can be set]
        """
        self.category = category
    