import sqlite3

        

def session_manager(username, passwd):
    conn = sqlite3.connect("webStore.db") #create or open the FILE
    cur = conn.cursor()
    users = dict(cur.execute("select username, password from customer"))
    conn.close()
    if username in users:
        if users[username]==passwd:
            return True
        else:
            return False
    return False

def add_customer(name, username, password, level):
    try:
        conn = sqlite3.connect("webStore.db") #create or open the FILE
        cur = conn.cursor()
        cur.execute("insert into customer(name, username, password, lvl) values(?, ?, ?, ?)",(name, username, password, level))
        conn.commit()
        cur.close()
        val = True
    except sqlite3.Error as err:
        print("Failed to insert customer, ", err)
        val = False
    finally:
        if conn:
            conn.close()
            print("Closed connection")   
    
    return val



def add_vendor(cid, store_name):
    try:
        conn = sqlite3.connect("webStore.db") #create or open the FILE
        cur = conn.cursor()
        cur.execute("pragma foreign_keys = on")
        cur.execute("insert into vendor(cid, store_name) values(?,?)", (cid, store_name))
        conn.commit()
        val = True
    except sqlite3.Error as err:
        print("Failed to insert vendor, ", err)
        val = False
    finally:
        if conn:
            conn.close()
            print("Closed connection")
    return val



    
def add_item(dish_name, item_name, vendor_id, store_id, available_quantity, unit_price):
    try:
        conn = sqlite3.connect("webStore.db") #create or open the FILE
        cur = conn.cursor()
        cur.execute("pragma foreign_keys = on")
        cur.execute("insert into items(vid, name, unit_price, qty) values(?,?,?,?)", (vendor_id, item_name, unit_price, available_quantity))
        conn.commit()
        val = True
       
    except sqlite3.Error as err:
        print("Failed to insert items, ", err)
        val = False
    finally:
        if conn:
            conn.close()
            print("Closed connection")
    return val


def get_vendor_from_vid(vid):
    try:
        conn = sqlite3.connect("webStore.db") #create or open the FILE
        cur = conn.cursor()
        cur.execute("pragma foreign_keys = on")
        (cur.execute("select customer.username from customer inner join vendor on vendor.cid=customer.cid where vendor.vid = ?",(vid,)))
        username = cur.fetchall()[0][0]
    except sqlite3.Error as err:
        print("Unable to retrieve username, ", err)
    finally:
        if conn:
            conn.close()
    return username


def get_customer_from_cid(cid):
    try:
        conn = sqlite3.connect("webStore.db") #create or open the FILE
        cur = conn.cursor()
        cur.execute("pragma foreign_keys = on")
        (cur.execute("select customer.username from customer where customer.cid = ?",(cid,)))
        username = cur.fetchall()[0][0]
    except sqlite3.Error as err:
        print("Unable to retireve username, ", err)
    finally:
        if conn:
            conn.close()
            print("Closed connection")
    return username


def search_item_by_name(item_name):
    try:
        conn = sqlite3.connect("webStore.db") #create or open the FILE
        cur = conn.cursor()
        cur.execute("pragma foreign_keys = on")
        cur.execute("select * from items where items.name = ?",(item_name,))
        row = cur.fetchall()
    except sqlite3.Error as err:
        print("Error. ", err)
    finally:
        if conn:
            conn.close()
            print("Closed connection.")
    return row


def place_order(cid, item_id, qty):
    try:
        conn = sqlite3.connect("webStore.db") #create or open the FILE
        cur = conn.cursor()
        cur.execute("pragma foreign_keys = on")
        cur.execute("insert into orders_request(cid, items_id, qty) values(?,?,?)", (cid, item_id, qty))
        conn.commit()
        val = True
    except sqlite3.Error as err:
        print("Failed to place order, ", err)
        val = False
    finally:
        if conn:
            conn.close()
            print("Closed connection")
    return val


def get_all_orders_by_customer(cid):
    try:
        conn = sqlite3.connect("webStore.db") #create or open the FILE
        cur = conn.cursor()
        cur.execute("pragma foreign_keys = on")
        cur.execute("drop table if exists orders")
        cur.execute("create table orders as select orders_request.rid, orders_request.cid, orders_request.items_id, orders_request.qty, items.unit_price from orders_request inner join items on items.items_id = orders_request.items_id")
        cur.execute("select * from orders where cid=?", (cid,))
        row = cur.fetchall()
    except sqlite3.Error as err:
        print("Failed to place order, ", err)
    finally:
        if conn:
            conn.close()
            print("Closed connection.")
    return row
        
def get_all_orders():
    try:
        conn = sqlite3.connect("webStore.db") #create or open the FILE
        cur = conn.cursor()
        cur.execute("pragma foreign_keys = on")
        cur.execute("drop table if exists orders")
        cur.execute("create table orders as select orders_request.rid, orders_request.cid, orders_request.items_id, orders_request.qty, items.unit_price from orders_request inner join items on items.items_id = orders_request.items_id")
        cur.execute("select * from orders")
        row = cur.fetchall()
    except sqlite3.Error as err:
        print("Failed to place order, ", err)
    finally:
        if conn:
            conn.close()
            print("Closed connection.")
    return row


def check_user_level(username):
    try:
        conn = sqlite3.connect("webStore.db")
        cur = conn.cursor()
        cur.execute("pragma foreign_keys = on")
        cur.execute("select lvl from customer where username = ?", (username,))
        level = cur.fetchall()[0][0]
    except sqlite3.Error as err:
        print("Error in query, ", err)
    finally:
        if conn:
            conn.close()
            print("Connection closed.")

    return level


def get_all_vendors():
    try:
        conn = sqlite3.connect("webStore.db")
        cur = conn.cursor()
        cur.execute("pragma foreign_keys = on")
        cur.execute("select vendor.vid, vendor.store_name, items.name, items.qty, items.unit_price from vendor inner join items on items.vid = vendor.vid")
        rows = cur.fetchall()
    except sqlite3.Error as err:
        print("Error in query, ", err)
    finally:
        if conn:
            conn.close()
            print("Connection closed")
    return rows
        