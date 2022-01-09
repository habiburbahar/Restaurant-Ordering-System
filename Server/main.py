"""
CMPT 370, Group Theta
Main file of the server.
Creates all components, then starts recieving HTTP requests
"""
from ThetaDatabase.DBInterface import Database
from ThetaDatabase.ThetaDB import ThetaDB
from Auth import Authentication
from flask import Flask, request, send_file, abort, jsonify
from Inventory import Inventory
from utils.GenerateMenu import menu_items
from item import Item
from Orders import Orders
# Create the database component, then create all other components, supplying
# them with a reference to the database

# "_restaurant_data" is the name of the directory where restaurant_db will store
# its tables.
# This is a relative path, so its location will depend on where
# you ran this .py file from. In a real application, this should probably
# be an absolute path
restaurant_db: Database = ThetaDB("_restaurant_data")

# Authentication object is given a reference to the Database, so that it
# can store authentication information.
restaurant_auth: Authentication = Authentication(restaurant_db)
# Create a test user
if not restaurant_auth.user_exists("admin"):
    restaurant_auth.add_user("admin", "admin")


# Create the store's inventory for all of the food items
inventory: Inventory = Inventory(restaurant_db)
# Construct the menu within the system if it doesn't exist yet

if len(inventory.get_listOfItems()) == 0:
    for menu_item in menu_items():
        inventory.add_item(Item(**menu_item))

# Instantiate the order storage system
orders: Orders = Orders(restaurant_db)


# ***
# TODO Set up Flask server here
# ***
# main.py
# methods = ['GET','POST']
# authentication = Authentication
app = Flask(__name__)
# defining a route

#The catch-all endpoint for returning all of the JS, CSS, and HTML files that the browser requests.
@app.route('/<path:filepath>')
def catch_all(filepath):
    """
    ### Description:
    The catch-all endpoint for returning all of the JS, CSS, and HTML files
    that the browser requests.

    ### Response:
    The file that was requested
    """
    try:
        # If it's a directory, add the index of the folder onto it
        if filepath.endswith("/"):
            filepath += "/index.html"

        return send_file(f"../Site/{filepath}")
    except FileNotFoundError:
        abort(404)


#The endpoint for verifying an employee's login information
@app.route('/login', methods=['POST'])
def loginEmployee():
    data = request.json

    try:
        user = data["uname"]
        password = data["pwd"]
    except KeyError:
        return { "success": False }

    try:
        if (restaurant_auth.is_login_valid(user,password)):
            return { "success": True, }
        else:
            return { "success": False, }

    except:
        return { "success": False, }



#Returns the data relating to the menu. (List of items, including category attribute and quantity information)
@app.route('/menu', methods = ['GET'])
def getMenu():
    return jsonify(inventory.get_listOfItems())

#Returns the list of orders and their status' to display on the web page.
@app.route('/orders', methods = ['GET'])
def list_of_orders():
    """
    ### Description
    Returns the list of all orders within the system.

    ### Response Body:
    ```py
    [
        {
            "id": int,
            "items": [
                {
                    "id": int,
                    "name": str,
                    "quantity": int,
                },
                # ... snip ...
            ],
            "total": int,
            "status": str
        },
        # ... snip ...
    ]
    ```
    """
    return jsonify(orders.get_list())


@app.route('/order', methods = ['POST'])
def place_order():
    """
    ### Description
    Adds an order to the database that can be retrieved from `GET /orders`,
    this endpoint returns the order number assigned from the database. The data
    that is passed to this endpoint in the request in body is an array of arrays
    which contains the item name and the quantity being ordered by the customer
    in order to prevent large amounts of data from being sent across the network
    allowing the request to be fulfilled faster than sending the full item
    object through the network.

    ### Request Body:
    ```py
    [
        [item_name:str, quantity:int],
        # ... snip ...
    ]
    ```

    ### Response Body:
    ```py
    {
        "success": bool,
        "order_number": int
    }
    ```
    """
    try:
        order_items = []
        grand_total = 0

        # Assert that the order isn't empty
        if len(request.json) <= 0:
            return { "success": False }

        # Adjust all quantities of the items that the person ordered and add to
        # to the order data
        for order_item in request.json:
            item = inventory.search_item(order_item[0])[0]
            order_items.append({
                "name": item["name"],
                "quantity": order_item[1],
                "id": item["id"],
            })

            grand_total += item["cost"] * order_item[1]

            new_quantity = item["quantity"] - order_item[1]
            inventory.changeItemQuantity(
                max(new_quantity, 0),
                item["id"]
            )

        # Saves the order data to the database
        order_number = orders.add_order({
            "total": grand_total,
            "items": order_items,
            "status": "In-Progress"
        })

        return {
            "success": True,
            "order_number": order_number
        }

    # Something went wrong, respond as needed
    except:
        return { "success": False, }


@app.route('/order/<int:id>', methods = ['PATCH'])
def update_order(id: int):
    """
    ### Description
    Updates the given order with the data provided in the body of the request.

    Note: The ID field is not able to be updated, and will be ignored silently
    if included in the fields to update.

    ### Request body:
    All fields listed below are optional, if you include the `items` field, it
    will replace all items in the order, in order to just replace one you must
    account for that in your request
    ```py
    {
        "items": list,
        "total": int,
        "status": str
    }
    ```

    ### Response Body:
    ```py
    {
        "success": bool
    }
    ```
    """
    try:
        orders.edit_order(id, **request.json)
        return { "success": True }
    except:
        return { "success": False }


@app.route('/order/<int:id>', methods = ['DELETE'])
def delete_order(id: int):
    """
    ### Description:
    Deletes the specified order from the database. This also adds the quantity
    of items ordered back into the stock so that they can be ordered by others.

    ### Response Body:
    ```py
    {
        "success": bool
    }
    ```
    """
    try:
        order = orders.get_order(id)

        # Update all items that were cancelled from the server
        for item in order["items"]:
            stock = inventory.search_item(item["name"])[0]
            inventory.changeItemQuantity(
                item["quantity"] + stock["quantity"],
                item["id"]
            )

        orders.delete_order(id)
        return { "success": True }
    except:
        return { "success": False }


if __name__ == '__main__':
    app.run(debug = True)