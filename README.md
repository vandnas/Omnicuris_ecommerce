# Omnicuris_ecommerce
Sample backend application for e commerce website.


Framework : Django
Database : PostgreSQL



Tables in PostgreSQL Database:
-------------------------------
2 tables created in PostgreSQL:
Item
For storing item details.

Order
For storing order placed.




Ecommerce Django API’s
-----------------------

CRUD operations on items
*************************

1. Create/Update Item
>> API: http://localhost:8000/ecommerce_app/add_item/
>> Description:
-----Add items in item table
-----It does the work of upsert (insert + update)
-----In case the item is not present in Item table, It is added to Item table.
-----In case it's already present, it's attributes are updated in Item table.
-----Save item information in Item Table.
-----It can be zero just to let the end user know that it is currently out of stock
-----instead of unavailability of that item entirely.
>> Param request: GET/POST
>> Return: blank form (GET), save form information in db (POST)


2. Delete Item
>> API: http://localhost:8000/ecommerce_app/delete_item?item_name=ball
>> Description:
-----Delete item from Item table.
-----In case item is not present in item table, it gives below message.
>> Param request: GET
>> Return: Deletion message


3. Get a specific Item
>> API: http://localhost:8000/ecommerce_app/get_item/wickets/
>> Description:
-----Get a specific entry from item table.
-----In case item is not present in item table, it gives below message.
>> Param request:GET
>> Return: Item details


All items listing
*******************

1. Get all items
>> API: http://localhost:8000/ecommerce_app/get_all_items/
>> Description:
-----Get all items from Item table
>> Param request: GET
>> Return:  List of available items in Item table


Single & bulk ordering (Just consider the item, no. of items & email ids as params for ordering)
**************************************************************************************************

1. Single Order
>> API: http://localhost:8000/ecommerce_app/place_single_order/
>> Description :
-----Place a single order
-----Save order information in Order Table
-----Get order information from form and save it in Order table.
-----Various cases are handled while placing order like:
-----If the item ordered doesn't exist in Item table, will give a message.
-----The quantity ordered of the item should be atleast one.
-----The quantity ordered cannot be more than the number of items present in Items table.
-----If the item ordered is out of stock i.e. in Item table.
-----If none of the above conditions are true, order is successfully placed and saved in Order table.
>> Param request: POST/GET
>> Return: blank form (GET), save form information in db (POST)


2. Bulk Order
>> API: http://localhost:8000/ecommerce_app/place_bulk_order
>> Description:
-----Place bulk order
-----The client in this case is another python script, which on execution places bulk order in Order table.
-----It iterates over item and their quantity, and saves information in Order table.
>> Param request: POST


All orders
**************

1. Get all orders 
>> API: http://localhost:8000/ecommerce_app/get_all_orders/
>> Description:
-----Get all entries from Order table.
>> Param request: GET
>> Return: List of all orders in Order table.
