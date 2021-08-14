from flask import Blueprint, request, redirect, jsonify
import app.models as models

auth = Blueprint("auth", __name__)
session = []


@auth.route("/login", methods=["GET","POST"])
def login():
    cred = request.get_json()
    if cred is not None:
        username = cred["username"]
        password = cred["password"]
        if models.session_manager(username, password):
            session.append(username)
            return f"<h1>Welcome to the Web Store. {username} logged in</h1>"
        else:
            return f"<h1>Invalid Username/Password. Please login again."
    return "<h1>Welcome to the Web Store. Please login to continue</h1>"


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    user = request.get_json()
    username = user["username"]
    session.remove(username)
    return f"<p>{username} logged out</p>"


@auth.route("/signup", methods=["GET", "POST"])
def add_customer():
    user = request.get_json()
    if user is not None:
        name = user["name"]
        username = user["username"]
        password = user["password"]
        level = user["level"]
        retval = models.add_customer(name, username, password, level)
        if retval:
            return f"Successfully added {username}"
        else:
            return f"Error. Please check logs."
    return f"<h1>Sign Up. Please provide details.</h1>", 404


@auth.route("/register/vendor", methods=["GET","POST"])
def add_vendor():
    vendor = request.get_json()
    if vendor is not None:
        cid = vendor["customer_id"]
        store_name = vendor["store_name"]
        val = models.add_vendor(cid, store_name)
        if val:
            return f"Vendor added"
        else:
            return f"Error. Please check logs."
    else:
        return f"<h1>Please provide vendor details</h1>", 404


@auth.route("/register/item", methods=["GET", "POST"])
def add_item():
    item = request.get_json()
    if item is not None:
        dish_name = item["dish_name"]
        item_name = item["item_name"]
        vid = item["vendor_id"]
        store_id = item["store_id"]
        qty = item["available_quantity"]
        unit_price=item["unit_price"]
        username = models.get_vendor_from_vid(vid)
        if username in session:
            value = models.add_item(dish_name, item_name, vid, store_id, qty, unit_price)
            if value:
                return f"Item added"
            else:
                return f"Error. Please check logs."
        else:
            return ("<h1>Please login as vendor.</h1>")
    else:

        return f"<h1>Please provide item details</h1>", 404


@auth.route("/search/item", methods=["GET", "POST"])
def search_item_by_name():
    item = request.get_json()
    if item is not None:
        cid = item["customer_id"]
        item_name = item["item_name"]
        username = models.get_customer_from_cid(cid)
        if username in session:
            value = models.search_item_by_name(item_name)
            return f"[item_id, vid, name, unit_price, qty] = {value}"
        else:
            return f"<h1>Login please.</h1>"
    else:
        return f"<h1>Please provide item details.</h1>"


@auth.route("/order/place", methods=["POST"])
def place_order():
    order = request.get_json()
    if order is not None:
        cid = order["customer_id"]
        username = models.get_customer_from_cid(cid)
        if username in session:
            item_id = order["item_id"]
            qty = order["quantity"]
            value = models.place_order(cid, item_id, qty)
            if value:
                return f"<h1>Order placed successfully</h1>"
            else:
                return f"<h1>Unable to place order. Check logs.</h1>"
        else:
            return f"<h1>Please Login</h1>"
    else:
        return f"<h1>Please provide order details</h1>"


@auth.route("/order/get", methods=["GET"])
def get_all_orders_by_customer():
    orders = request.get_json()
    if orders is not None:
        cid = orders["customer_id"]
        username = models.get_customer_from_cid(cid)
        if username in session:
            val = models.get_all_orders_by_customer(cid)    
            return f"[order_id, cid, items_id, qty, unit_price, total_amount] = {val}"
        else:
            return f"<h1>Please login.</h1>"
    else:
        return f"<h1>Please place order.</h1>"


@auth.route("/order/get_all", methods=["GET"])
def get_all_orders():
    user = request.get_json()
    if user is not None:
        username = user["username"]
        if username in session:
            value = models.check_user_level(username)
            print(value)
            if value == 2:
                row = models.get_all_orders()
                return f"[order_id, customer_id, items_id, qty, unit_price], {row}"
            else:
                return f"<h1>Access denied.<>/h1"
    else:
        return f"<h1>Please enter details.</h1>" 


@auth.route("/vendor", methods=["GET"])
def get_all_vendors():
    user = request.get_json()
    if user is not None:
        username = user["username"]
        if username in session:
            value = models.get_all_vendors()
            return f"<h1>[vendor_id, store_name, item_name, qty, unit_price]: {value}</h1>"
        else:
            return f"<h1>Please login.</h1>"

    else:
        return f"<h1>Please enter details.</h1>"