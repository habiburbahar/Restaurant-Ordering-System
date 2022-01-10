# Restaurant-Ordering-System

## Goal: To enable customers to get an effective and efficient user interface for any restaurants they would visit.

## Product Description:
- The Kiosk would facilitate clients ( potential customers) and operational management team at any restaurants. 
- It provides an interface for clients to order from the Kiosk and wait for the order to be ready. 
- The Kiosk sends the order right to the kitchen where it prepared and sent back to the customer.
- Allows management to analyze the inventory and make food items available accordingly.

## Product Architecture:
 ### Server: 
  - Written in Python with Flask as the web server framework
  - Data stored in JSON files, using the ThetaDB interface so that it can be easily swapped out in the future if needed.
  - API endpoints are designed in a RESTful manner
  - All communication between the server and client is done through JSON objects as needed.

 ### Client:
  - Two different web clients, one for the customer kiosk and one for the employees.
  - Written in Javascript, HTML, and CSS. With Vue.js as the library used for DOM manipulation and reactivity.
  - Axios used for performing the HTTP requests to the server and parsing the responses.
