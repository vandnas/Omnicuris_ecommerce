# -*-coding:utf8-*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ecommerce_app.models import Item, Order
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm, ItemForm
from django.views.decorators.csrf import csrf_exempt
import json


# API: http://localhost:8000/ecommerce_app/place_single_order/
def insert_in_order_table(request):
    """
    Place a single order
    It calls save_order_in_db() function to save the order in Order table if it's valid.
    :param request: POST/GET
    :return: blank form (GET), save form information in db (POST)
    """
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            message = save_order_in_db(request)
            return HttpResponse(message)
    else:
        order_form = OrderForm()

    return render(request, 'order.html', {'form': order_form})


# Get order information from form and save it in Order table.
def save_order_in_db(request):
    item_name = request.POST.get("item_name")
    quantity = int(request.POST.get("quantity"))
    email_id = request.POST.get("email_id")

    message = save_order(item_name, quantity, email_id)
    return message


# Save order information in Order Table
# Various cases are handled while placing order like:
# If the item ordered doesn't exist in Item table, will give a message.
# The quantity ordered of the item should be atleast one.
# The quantity ordered cannot be more than the number of items present in Items table.
# If the item ordered is out of stock i.e. ) in Item table.
# If none of the above conditions are true, order is successfully placed and saved in Order table.
# Also, the number of items ordered are decremented from Item table for that item.
def save_order(item_name, quantity, email_id):
    try:
        item_row = Item.objects.get(item_name = item_name)
    except ObjectDoesNotExist:
        return "The item:%s you have ordered is not available!!" % item_name

    if quantity <= 0:
         return "Please order atleast one item. Quantity cannot be zero or negative!!"

    if int(item_row.no_of_items) == 0:
        return "Sorry this item:%s is out of stock!!" % item_name
    elif int(item_row.no_of_items) < quantity:
        return "Sorry we are left only with %s items for item: %s.Please reduce your quantity" \
               % (int(item_row.no_of_items), item_name)
    else:
        order_obj = Order(item_name = item_row.item_name, quantity = quantity, email_id = email_id)
        order_obj.save()
        items_left = int(item_row.no_of_items) - quantity
        Item.objects.filter(item_name = item_name).update(no_of_items = items_left)
        return "Congratulations ! Your Order is successfully placed."


# API: http://localhost:8000/ecommerce_app/place_bulk_order
@csrf_exempt
def save_bulk_order_in_db(request):
    """
    Place bulk order
    The client in this case is another python script, which on execution places bulk order in Order table.
    It iterates over item and their quantity, and saves information in table.
    :param request: POST
    :return:
    """
    message_list = []
    if request.method == 'POST':
        msg = request.body
        string_msg=str(msg)
        json_data = json.loads(string_msg)
        item_names = json_data["item_names"]
        no_of_items = json_data["no_of_items"]
        email_id = json_data["email_id"]

        for item_name, quantity in zip(item_names, no_of_items):
            item_name = str(item_name)
            quantity = int(quantity)
            message = save_order(item_name, quantity, email_id)
            message_list.append("%s \n" % str(message))
        return HttpResponse(message_list)


# API: http://localhost:8000/ecommerce_app/add_item/
def upsert_in_item_table(request):
    """
    Add items in item table
    It does the work of upsert (insert + update)
    In case the item is not present in Item table, It is added to Item table.
    In case it's already present, it's attributes are updated in Item table.
    :param request: GET/POST
    :return: blank form (GET), save form information in db (POST)
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        item_form = ItemForm(request.POST)
        # check whether it's valid:
        if item_form.is_valid():
            message = save_item_in_db(request)
            return HttpResponse(message)
       
    # if a GET (or any other method) we'll create a blank form
    else:
        item_form = ItemForm()

    return render(request, 'item.html', {'form': item_form})


# Save item information in Item Table.
# The quantity of added items should not be negative.
# It can be zero just to let the end user know that it is currently out of stock
# instead of unavailability of that item entirely.
# In case the item is not present in Item table, It is added to Item table.
# In case it's already present, it's attributes (no_of_tems) is updated in Item table.
def save_item_in_db(request):
    item_name = request.POST.get("item_name")
    no_of_items = int(request.POST.get("no_of_items"))

    if no_of_items < 0:
        return "Quantity of Items cannot be negative!!"

    item_exists = Item.objects.filter(item_name = item_name).count()
    if item_exists > 0:
        # update
        Item.objects.filter(item_name = item_name).update(no_of_items = no_of_items)
    else:
        # insert
        item_obj = Item(item_name = item_name, no_of_items = no_of_items)
        item_obj.save()
    return "Item: %s information saved in database successfully!" % item_name


# API: http://localhost:8000/ecommerce_app/get_all_items/
def get_entries_from_item_table(request):
    """
    Get all items from Item table
    :param request: GET
    :return:  List of available items in Item table
    """
    if request.method == 'GET':
        item_list = []
        items = Item.objects.all()
        for item in items:
            item_list.append("%s" % item)
        return HttpResponse("List of available items: <br> %s" % item_list)


# API: http://localhost:8000/ecommerce_app/get_all_orders/
def get_entries_from_order_table(request):
    """
    Get all entries from Order table.
    :param request: GET
    :return: List of all orders in Order table.
    """
    if request.method == 'GET':
        order_list = []
        orders = Order.objects.all()
        for order in orders:
            order_string = "Item name: %s,  Quantity: %s,  Email Id: %s <br>" % \
                           (str(order.item_name), str(order.quantity), str(order.email_id))
            order_list.append(order_string)
        return HttpResponse("List of all orders: <br> %s" % order_list)


# API: http://localhost:8000/ecommerce_app/delete_item?item_name=ball
def delete_entry_from_item_table(request):
    """
    Delete item from Item table.
    :param request: GET
    :return: Deletion message
    """
    if request.method == 'GET':
        item_name = request.GET["item_name"]
        try:
            row = Item.objects.get(item_name = item_name)
            row.delete()
            return HttpResponse("Deleted item: %s successfully" % item_name)
        except ObjectDoesNotExist:
            return HttpResponse("This item: %s is not present in Item table.!!" % item_name)


# API: http://localhost:8000/ecommerce_app/get_item/wickets/
def get_entry_from_item_table(request, item_name):
    """
    Get a specific entry from item table.
    :param request:GET
    :param item_name:
    :return: Item details
    """
    if request.method == 'GET':
        try:
            row = Item.objects.get(item_name = item_name)
            return HttpResponse("Item name: %s  Number of items: %s"
                                % (row.item_name, str(row.no_of_items)))
        except ObjectDoesNotExist:
            return HttpResponse("This item: %s is not present in Item table.!!" % item_name)

