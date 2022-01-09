from random import randint, choice

# The names of items that will be generated every time
ITEM_NAMES = [
	"Fire Roasted Herbs & Duck","Baked Mustard Horse"
	,"Raspberry and Elderberry Pancakes","Ginger Yogurt","Caramel Fruitcake",
	"Braised Sour Yak","Pepperoni Pizza","Orange Ice Cream","Almond Fudge",
	"Infused Olives & Mustard Lobster","Roasted Honey & Thyme Venisin",
	"Tea-Smoked Fennel & Lemon Pasta","Sauteed Oregano Frog","Chocolate Cake",
	"Small Fries","Medium Fries","Large Fries","Curly Fries","Cinnamon Pizza",
	"Hawaiian Pizza","Soy Sauce - 16L",
]

MAX_PRICE = 354
MAX_QUANTITY = 50
MIN_QUANTITY = 2
MIN_INGREDIENTS = 2
MAX_INGREDIENTS = 7

POSSIBLE_INGREDIENTS = [
	"Herbs", "Spices", "Duck", "Mustard", "Horse", "Paprika", "Raspberry",
	"Elderberry", "Flour", "Water", "Eggs", "Ginger", "Vanilla", "Yogurt",
	"Caramel", "Fruit", "Flour", "Eggs", "Icing Sugar", "Yak Meat", "Lemon",
	"Flour", "Eggs", "Yeast", "Tomato Paste", "Pepperoni", "Cheese", "Cream",
	"Artificial Orange Flavouring", "Ice", "Almonds", "Eggs", "Flour", "Cream",
	"Lobster", "Olives", "Butter", "Venison", "Honey", "Thyme", "Butter",
	"Flour", "Eggs", "Green Tea", "Fennel", "Lemon", "Frog", "Oregano",
	"Butter", "Milk Chocolate", "Flour", "Eggs", "Icing Sugar", "Potato",
	"Sodium Chloride", "Flour", "Eggs", "Yeast", "Tomato Paste", "Cinnamon",
	"Flour", "Eggs", "Yeast", "Tomato Paste", "Cheese", "Pineapple", "Ham", "Soy"
]

POSSIBLE_CATEGORIES = [
	"entree", "pizza", "side", "drink", "dessert"
]


def menu_items() -> dict:
	"""
	A generator that dynamically creates unique menu data for each time the
	server is restarted. This returns a dictionary of the item and the item
	should be constructed from it using the kwargs system.
	"""
	# Construct the menu item's dictionary
	for name in ITEM_NAMES:
		price = randint(1, MAX_PRICE)
		quantity = randint(MIN_QUANTITY, MAX_QUANTITY)
		ingredient_count = randint(MIN_INGREDIENTS, MAX_INGREDIENTS)

		yield {
			"name": name,
			"cost": price,
			"ingredients": [ choice(POSSIBLE_INGREDIENTS) for _ in range(ingredient_count) ],
			"category": choice(POSSIBLE_CATEGORIES),
			"quantity": quantity
		}