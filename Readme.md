## **Web Store Backend service**

The following web application is  purely a backend service for the online web store.
This web store provides basic functionality for CRUD operations for 
1. login
2. registration (customer, vendor, admin)
3. accessing items/orders/vendor lists
4. placing orders
5. logout.

### Using blueprints
Two blueprints are used
1. views.py
2. auth.py

As most of the API's involve authentication requests, nearly all blueprints are through auth.py

### Assumptions
As there is no front end service available, it is assumed that all client requests are provided through json files. The format for sending such requests are explained in API.txt.