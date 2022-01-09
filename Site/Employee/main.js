let v = new Vue({
	el: `#app-base`,
	data: {
		restaurantName: "Theta Fast Food",
		isLoggedIn: false,
		loginErrorMessage: "",
		// User input data:
		uname: "",
		pwd: "",

		displayClosedOrders: false,

		// Current data from the server about all orders, updated in
		// updateOrders().
		orders: [],
	},
	computed: {
	},
	methods: {

		/**
		 * Tell the server to change the status of the given orderID to
		 * newStatus, or delete the order if the new status is 'Canceled'
		 * @param orderID id of the order to change
		 * @param newStatus New status of the order. If newStatus is 'Canceled',
		 * 	the order is instead deleted.
		 */
		changeOrderStatus(orderID, newStatus) {
			console.log("Changing order status of order " + String(orderID) +
				" to " + newStatus);

			if (newStatus == "Canceled") {
				// Delete the order
				axios.delete('/order/' + String(orderID))
				.then(response => {
					if (response.data["success"]) {
						console.log("Deleted order successfully.");
						this.updateOrders();
					}
					else {
						console.error("Failed to delete order.", error);
					}
				})
				.catch(error => {
					console.error("Failed to delete order.", error);
				});
			}
			else {
				// Modify the order' status
				axios.patch('/order/' + String(orderID), {status: newStatus})
				.then(response => {
					if (response.data["success"]) {
						console.log("Changed order status successfully.");
						this.updateOrders();
					}
					else {
						console.error("Failed to change order status.", error);
					}
				})
				.catch(error => {
					console.error("Failed to change order status.", error);
				});
			}
		},

		/**
		 * Request the updated set of orders from the server.
		 * Modifies this.orders if successful.
		 */
		updateOrders() {
			axios.get('/orders').then(response => {
				this.orders = response.data
			})
			.catch(error => {
				console.error("Failed to retrieve orders.", error);
			});
		},

		/**
		 * This method is called when the user presses the login button,
		 * or presses enter while one of the input fields is focused
		 */
		loginAction() {
			if (this.uname === "" || this.pwd === "") {
				this.loginErrorMessage = "Please supply a username and password."
			}
			else {
				axios.post('/login', {uname: this.uname, pwd: this.pwd})
					.then(response => {
						// Successful response from server
						if (response.data["success"]) {
							// Switch away from the login page and retrieve
							// orders
							this.isLoggedIn = true;
							this.updateOrders();
						}
						else {
							this.loginErrorMessage = "Incorrect username or password."
						}
					})
					.catch(error => {
						this.loginErrorMessage = "There was an error while validating the login."
						console.error("There was an error while validating the login.", error);
					});

			}
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
	},

	/**
	 * When created, start an interval to poll the server with new orders
	 * every 5 seconds when we are logged in
	 */
	created () {
		setInterval(() => {
			if (this.isLoggedIn) this.updateOrders();
		}, 5000)
	},
});