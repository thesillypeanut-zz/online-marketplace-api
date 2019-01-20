# Online Marketplace API

A simple server side web API that uses CRUD operations to query products and simulate shopping cart transactions in an online marketplace, built using the Flask microframework and SQLite database. 

## Requirements

On a Linux environment, run the following commands:
```bash
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6 python3.6-dev
sudo apt-get update
sudo apt-get install curl
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install virtualenv
```

## Getting Started

```bash
# Clone this repository and cd into it:
git clone https://github.com/thesillypeanut/online-marketplace-api.git
cd online-marketplace-api/

# Create and activate your virtual environment:
virtualenv venv
source venv/bin/activate

# Install your project dependencies:
pip install -r requirements.txt

# Start the server:
python3 run.py
```

## Try Out the API

This is a sample testing flow of creating and completing a cart by placing an order on the cart. Commands for the 
following API requests can be found in the "Database Models and API Usage" section.

1. Database: Initialize DB
2. Database: Fill db with sample products
3. User: Create a user
4. User: Login the user
   * You will receive an authentication token
5. Product: Fetch products to check what is available
6. Cart-Item: Create cart-item(s) using product id(s) to add product(s) to your cart
   * The first cart-item posted will automatically create a cart
7. Order: Create an order on a cart
8. Product: Fetch products to check updated inventory counts 


## Database Models and API Usage

<img src="/database_design.png">

### Database
```bash
# Initialize db:
curl -X GET http://localhost:5000/api/v1/db/init

# Fill db with sample products:
curl -X GET http://localhost:5000/api/v1/db/fill
```

### Product
```bash
# Fetch all products:
curl -X GET http://localhost:5000/api/v1/products/

# Fetch all available (inventory count > 0) products:
curl -X GET http://localhost:5000/api/v1/products/available

# Filter products using queries in the route (only "equal to" queries are supported):
curl -X GET http://localhost:5000/api/v1/products/?price=10.4\&inventory_count=300

# Fetch a single product by id:
curl -X GET http://localhost:5000/api/v1/products/<product_id>

# Create a product with title, price (float) and inventory_count (int):
curl -H "Content-Type: application/json" -X POST -d '{"title":"TITLE", "price":<float_price>, "inventory_count":<inven_int>}' http://localhost:5000/api/v1/products/

# Edit a product's title, price (float) and/or inventory_count (int):
curl -H "Content-Type: application/json" -X PUT -d '{"title":"NEWTITLE", "price":<new_float_price>, "inventory_count":<new_inven_int>}' http://localhost:5000/api/v1/products/<product_id>

# Delete a product:
curl -X DELETE http://localhost:5000/api/v1/products/<product_id>
```

### User (and Token Authentication)
```bash
# Create a user with a username and password:
curl -H "Content-Type: application/json" -X POST -d '{"username":"USERNAME", "password":"PASSWORD"}' http://localhost:5000/api/v1/users/

# Login with the username and password you selected:
curl --user <USERNAME>:<PASSWORD> http://localhost:5000/api/v1/users/login
```

Please note that you need to use the token you received in the previous step to perform most requests from here on.
For your convenience, you can save the token in an environment variable:
```bash
export TOKEN="YOUR-TOKEN-HERE"
echo "$TOKEN"
```
Your token will expire in 1 hour. Login again to get a new token and update your environment variable as necessary.

```bash
# Fetch all users:
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/users/

# Fetch a single user with id:
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/users/<user_id>

# Edit your username and/or password:
curl -H "x-access-token: $TOKEN" -H "Content-Type: application/json" -X PUT -d '{"username":"NEWUSERNAME", "password":"NEWPASSWORD"}' http://localhost:5000/api/v1/users/<user_id>

# Delete your user record:
curl -H "x-access-token: $TOKEN" -X DELETE http://localhost:5000/api/v1/users/<user_id>
```

### Cart-Item
```bash
# Create a cart-item with a product id and quantity (int):
curl -H "x-access-token: $TOKEN" -H "Content-Type: application/json" -X POST -d '{"product_id":"PRODUCTID", "quantity":<quantity_int>}' http://localhost:5000/api/v1/cart-items/

# Fetch all cart-items associated with a cart_id (note that a user can have multiple "ordered" 
# carts and only one "unordered" cart):
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/cart-items/?cart_id=<cart_id>

# Fetch a single cart-item with id:
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/cart-items/<cart-item-id>

# Edit a cart item quantity:
curl -H "x-access-token: $TOKEN" -H "Content-Type: application/json" -X PUT -d '{"quantity":<new_quantity_int>}' http://localhost:5000/api/v1/cart-items/<cart-item-id>

# Delete a cart item:
curl -H "x-access-token: $TOKEN" -X DELETE http://localhost:5000/api/v1/cart-items/<cart_item_id>
```

### Cart
```bash
# Fetch all carts (note that a user can have multiple "ordered" carts and only one "unordered" cart):
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/carts/

# Fetch a single cart with id:
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/carts/<cart_id>

# Delete a cart:
curl -H "x-access-token: $TOKEN" -X DELETE http://localhost:5000/api/v1/carts/<cart_id>
```

### Order
```bash
# Create an order on a cart with cart_id:
curl -H "x-access-token: $TOKEN" -H "Content-Type: application/json" -X POST -d '{"cart_id":"CARTID"}' http://localhost:5000/api/v1/orders/

# Fetch all orders:
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/orders/

# Fetch a single order with id:
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/orders/<order_id>
```
