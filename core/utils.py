import json

from customer.models import Customer
from order.models import OrderItem, Order


def set_product_cookie(request):
    """
    Reads cookie from request and creates/modifies based on the products.
    :param request:
    :return: Json
    """
    product_id = request.data['product']
    product_count = int(request.data['count'])
    product = request.COOKIES.get('product')
    if product:
        my_dict = json.loads(product)
        if product_id in my_dict.keys():
            my_dict[product_id] = my_dict[product_id] + product_count
            return json.dumps(my_dict)
        my_dict[product_id] = product_count
        return json.dumps(my_dict)
    return json.dumps({product_id: product_count})


def get_cookie(request):
    """
    Reads orders data from cookie and creates an OrderItem models for anonymous user to be shown.
    :param request:
    :return: a list of orders.
    """
    product = request.COOKIES.get('product')
    if product:
        jsoned = json.loads(product)
        order_list = list()
        for product_id, count in jsoned.items():
            order = OrderItem(product_id=int(product_id), count=count)
            order_list.append(order)
        return order_list
    else:
        return 1


def cookie_to_database(request):
    """
    Reads cookie from request and saves OrderItem in database for the current user.
    :param request:
    """
    product = request.COOKIES.get('product')
    jsoned = json.loads(product)
    customer = Customer.objects.get(user=request.user)
    order = Order.objects.get_or_create(customer=customer, status_id=1)
    for product_id, count in jsoned.items():
        OrderItem.objects.create(order=order[0], product_id=product_id, count=count)


def change_cart_item_count(request, product_id, count):
    """"
    Reads cookie data from user request and changes OrderItem count for the current user.
    :param count:
    :param product_id:
    :param request:
    """
    product = request.COOKIES.get('product')
    jsoned = json.loads(product)
    if product_id in jsoned.keys():
        jsoned[product_id] = count
        return json.dumps(jsoned)


def remove_cart_item_count(request, product_id):
    """
    Reads cookie data from user request and removes OrderItem for the current user.
    :param product_id:
    :param request:
    """
    product = request.COOKIES.get('product')
    jsoned = json.loads(product)
    print('proid', product_id)
    if product_id in jsoned.keys():
        print('proid', product_id)
        print('jsoned', jsoned)
        print('product', product)
        del jsoned[str(product_id)]
        print('jsoned2', jsoned)
        return json.dumps(jsoned)
