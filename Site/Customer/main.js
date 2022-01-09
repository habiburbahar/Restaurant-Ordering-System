let v = new Vue({
	el: `#app-base`,
	data: {
		restaurantName: `Theta Fast Food`,

		/** The category that is being displayed in the menu area */
		selectedCategory: null,

		/** The item that was clicked on and is being displayed in the modal */
		selectedItem: null,

		/**
		 * The quantity value that is used and modified in the item addition
		 * modal, and the order modification modal
		 */
		targetQuantity: 1,

		/**
		 * An array of objects representing an order, the object consists of:
		 * ```json
		 * {
		 * 	"item": Item,
		 * 	"quantity": number
		 * }
		 * ```
		 */
		order: [],

		/** The items received from the server */
		items: [],

		/** If the user is currently selecting a payment method */
		isPaying: false,

		/** The payment response for success/failure of order placement */
		paymentMessage: ``,

		/**
		 * The item that is being modified which is already in the order list.
		 */
		editingItem: null,

		/**
		 * This is used to disable the buttons of the payment modal while the
		 * server is processing the order
		 */
		paymentProcessing: false,
	},
	computed: {
		/** Get the list of categories that exist */
		categories() {
			let categories = [];
			for (var item of this.items) {
				if (!categories.includes(item.category)) {
					categories.push(item.category);
				};
			};
			return categories;
		},

		/** Get the list of menu items for the currently selected category */
		menuItems() {
			return this.items.filter(i => i.category === this.selectedCategory);
		},

		/** Calculate grand total for the entire order */
		orderTotal() {
			let sum = 0;
			this.order.map(x => sum += x.item.cost * x.quantity);
			return sum;
		},
	},
	methods: {
		/**
		 * Resets the data which is assigned dynamically to allow cancelling
		 * the order at any time
		 */
		resetSite() {
			this.getMenu();
			this.order = [];
			this.isPaying = false;
			this.selectedItem = null;
			this.paymentMessage = ``;
			this.selectedCategory = null;
			this.selectedCategory = null;
			this.paymentProcessing = false;
		},

		/**
		 * Sends the customer's menu thus far to the server, this should only be
		 * called when the customer has finished ordering and payment is
		 * received.
		 */
		sendOrder() {
			this.paymentProcessing = true;
			axios.post(
				`/order`,
				this.order.map(orderItem => [orderItem.item.name, orderItem.quantity])
			)
			.then(response => {
				let data = response.data;

				if (!data.success) {
					this.paymentMessage = `Something went wrong processing your order, try again.`;
					return;
				};

				this.paymentMessage = `Order Placed! Your order number is: #${data.order_number}`;
				setTimeout(this.resetSite, 5000);
			})
			.catch(error => {
				console.error(error);
				this.paymentMessage = `Something went wrong processing your order, try again.`;
			});
		},

		/**
		 * Hides the item modal from view and resets the data so that the user
		 * doesn't get hit with unexpected data
		 */
		hideModal() {
			this.targetQuantity = 1;
			this.selectedItem = null;
		},

		/**
		 * Adds the currently selected to the order with the quantity chosen in
		 * the item modal and then hides the modal to prevent accidentally
		 * ordering it twice with the same modal.
		 */
		addToCart() {
			let orderItem = this.order.find(i => i.item == this.selectedItem);

			// The item has already been ordered, so just sum the two quantities
			if (orderItem) {
				orderItem.quantity += this.targetQuantity;
			}

			// The item hasn't been ordered yet, so add it as a new array item
			else {
				this.order.push({
					quantity: this.targetQuantity,
					item: this.selectedItem
				});
			};

			// Remove the amount of items ordered from the item's quantity to
			// prevent unintentional over-ordering
			this.selectedItem.quantity -= this.targetQuantity;

			this.targetQuantity = 1;
			this.selectedItem = null;
		},

		/**
		 * Converts the given price integer into a human-friendly string
		 *
		 * @param price The number of cents to convert to the string
		 */
		stringifyPrice(price) {
			let dollars = Math.floor(price / 100);
			let cents = price % 100;
			return `\$${dollars}.${cents < 10 ? '0' : ''}${cents}`;
		},

		/**
		 * Creates the URL path for the image of the item. Taking into account
		 * if it out of stock or not in order to grayscale it.
		 *
		 * @param {Object} item The item that the image path is desired for
		 * @param {boolean} grayscale Allow grayscaling the image based on the
		 * stock level of it
		 * @returns string
		 */
		itemImage(item, grayscale = true) {
			let name = item.name.toLowerCase().replace(/\s/g, `-`);

			// If the item is sold out, we want to display a grayed out version
			if (grayscale && item.quantity <= 0) {
				name += `-grayscale`;
			};

			return `../public/images/${name}.png`;
		},

		/**
		 * Changes the state of the edit item modal so that the user can
		 * continue adding items to their cart or modify what is already in it,
		 * if `item` remains null then the user is cancelling the modal and we
		 * need to reset the quantity variable and hide the modal.
		 *
		 * @param {Item} item The orderItem to edit
		 */
		editCartItem(item = null) {
			this.targetQuantity = item?.quantity || 1;
			this.editingItem = item;
		},

		/** Updates the cart with the item data that's currently being edited */
		updateCart() {
			let newInStock = (this.editingItem.quantity + this.editingItem.item.quantity) - this.targetQuantity;
			this.editingItem.item.quantity = newInStock;
			this.editingItem.quantity = this.targetQuantity;
			this.editingItem = null;
			this.targetQuantity = 1;
		},

		/**
		 * Removes the given item from the order. Does not adjust quantity of
		 * the order, just completely removes it.
		 *
		 * @param {orderItem} item The item to remove from the order
		 */
		removeItemFromOrder(item) {
			this.order = this.order.filter(i => i !== item);
			item.item.quantity += item.quantity;
			this.editCartItem();
		},

		/**
		 * Converts a string to Title Case (first letter of each word capitalized)
		 *
		 * @param {string} str The string that is being converted
		 * @return The title-cased string
		 */
		toTitleCase(str) {
			let string_parts = str.split(` `);

			for (var index in string_parts) {
				let word = string_parts[index];
				string_parts[index] = word.slice(0, 1).toUpperCase() + word.slice(1);
			};

			return string_parts.join(` `);
		},

		/**
		 * Gets the menu data from the API and sets the data in the Vue object
		 * appropriately.
		 */
		getMenu() {
			this.items = this.items.filter(x => false);
			axios.get(`/menu`)
			.then(response => {
				for (var item of response.data) {
					this.items.push(item);
				};
			})
			.catch(error => {
				alert(`Something went wrong while getting the list of items`);
				console.error(error);
			});
		},
	},
	mounted() {
		this.getMenu();
	},
});