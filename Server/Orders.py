from ThetaDatabase.DBInterface import Database


class Orders:
    """
    The information relating to Orders that the system has accepted
    """


    def __init__(self, database: Database, table = "orders"):
        """
        Creates an instance of the Orders object that can be manipulated

        :param `database`: The database controller that the server is using
        :param `table`?: The name of the table that the orders object will use.
        """
        self.db = database
        self.table = table

        if not database.table_exists(table):
            database.create_table(table)


    def add_order(self, order: dict) -> int:
        """
        Adds the given order data to the database

        :param `order`: The order data
        """
        return self.db.insert(self.table, order)


    def delete_order(self, order_id: int):
        """
        Deletes all data associated with the order ID

        :param order_id: The ID of the order to delete
        """
        self.db.delete_entry(self.table, order_id)


    def get_list(self) -> list:
        """
        Return an array of all of the orders that are in the database
        """
        return self.db.get_all_entries(self.table)


    def get_order(self, order_id: int) -> dict:
        """
        Gets the order data for the given ID

        :param order_id: The ID of the order to find
        """
        order = self.db.get_entry(self.table, order_id)

        # Assert the order was found
        if not order:
            raise ValueError("Invalid Order ID")

        return order


    def edit_order(self, order_id: int, **kwargs):
        """
        Edits the item with the given ID, each keyword argument provided is a
        field of the order item with the value of it being the new value.

        If one of the kwargs is attempting to modify the order's ID, it will be
        discarded silently without erroring.

        :param order_id: The ID of the order that is being modified
        :param kwargs: All fields of the order are an acceptable keyword argument
            except the ID.
        """
        order = self.get_order(order_id)

        # Modify all the corresponding kwargs that are allowed to be modified
        for key, value in kwargs.items():
            if key != "id":
                order[key] = value
        self.db.replace_entry(self.table, order_id, order)


    def change_status(self, order_id: int, status: str):
        """
        Changes the status of the order specified

        :param order_id: The ID of the order to change the status of
        :param status: The new status of the order
        """
        self.edit_order(order_id, status=status)


    def __iter__(self):
        """
        Iterate through all the orders in the database. This is a pretty simple
        linear iteration, nothing complicated.
        """
        orders = self.db.get_all_entries(self.table)

        for order in orders:
            yield order