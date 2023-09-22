# Create your views here.
from django.http import HttpResponse
from django.views.generic import ListView
from rest_framework import viewsets, generics
from rest_framework.response import Response

from core.utils import set_product_cookie, get_cookie, change_cart_item_count, remove_cart_item_count
from customer.models import Customer, Address
from order.serilizers import OrderSerializer, CouponSerializer
from .models import OrderItem, Order, Coupon
from .serilizers import OrderItemSerializer


class AddCard(viewsets.ModelViewSet):
    """
    A multipurpose view for order for cart.
    """
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def partial_update(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().partial_update(request, *args, **kwargs)
        else:
            product = self.request.data['product']
            count = self.request.data['count']
            cookie = change_cart_item_count(request, product, count)
            response = Response(status=201)
            response.set_cookie('product', cookie)
            return response

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().destroy(request, *args, **kwargs)
        else:
            product = self.request.data['product']
            cookie = remove_cart_item_count(self.request, product)
            response = Response(status=201)
            response.set_cookie('product', cookie)
            return response

    def create(self, request, *args, **kwargs):
        """
        Overriding this method for getting/creating the orders
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if self.request.user.is_authenticated:
            product = self.request.data['product']
            # If user is authenticated
            try:
                # If the order item doesn't exist.
                order_item = OrderItem.objects.get(product_id=product, order__customer__user=self.request.user,
                                                   order__status_id=1)
                order_item.count += 1
                order_item.save()
                return HttpResponse('done!', status=200)
            except:
                # If the order item doesn't exist
                user = request.user
                customers = Customer.objects.get_or_create(user=user)
                order = Order.objects.get_or_create(customer=customers[0], status_id=1)[0]
                request.data._mutable = True
                request.data['order'] = order.id
                return super().create(request, *args, **kwargs)
        else:
            # If the user is not authenticated and uses cookies(anonymous user).
            cookie = set_product_cookie(request)
            response = Response(status=201)
            response.set_cookie('product', cookie)
            return response


class DeleteOrderItem(generics.DestroyAPIView):
    """
    A view for deleting order items.
    """
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()


class UpdateOrderItem(generics.UpdateAPIView):
    """
    A view for updating order items.
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def partial_update(self, request, *args, **kwargs):
        request.data._mutable = True
        final_price = int(float(request.data['final_price']))
        total_price = int(float(request.data['total_price']))
        coupon_id = request.data['coupon']
        calc_total = 0
        for item in OrderItem.objects.filter(order__status_id=1, order__customer__user=self.request.user):
            calc_total += item.total
        if coupon_id:
            print('coupon_id', coupon_id)
            coupon = Coupon.objects.filter(pk=coupon_id)[0]
            final = coupon.discounted_price(calc_total)
            if final_price == final:
                request.data['status'] = 2
                return super().partial_update(request, *args, **kwargs)
            else:
                print('400')
                return HttpResponse(status=400)
        else:
            print(final_price)
            print(calc_total)

            if final_price == calc_total:
                print('if final_price == calc_total')
                request.data['status'] = 2
                return super().partial_update(request, *args, **kwargs)
            else:
                print('else2')
                return HttpResponse(status=400)


class OrderItemList(ListView):
    """
    A view for showing order items.
    """
    template_name = 'oder/view_card.html'
    model = OrderItem
    context_object_name = 'items'

    def get_queryset(self):
        """
        Overriding this method, so it will get a list of order items if the user is authenticated. Otherwise,
        it will get the list of order items from cookies.
        :return:
        """
        if self.request.user.is_authenticated:
            user = self.request.user
            customers = Customer.objects.get_or_create(user=user)
            order = Order.objects.get_or_create(customer=customers[0], status_id=1)[0]
            return order.orderitem_set.all()
        else:
            if get_cookie(self.request) == 1:
                return 'new_user'
            else:
                return get_cookie(self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Calculates and sends the total and final price to cart
        :param object_list:
        :param kwargs:
        :return:
        """
        if self.request.user.is_authenticated:
            total = 0
            for item in OrderItem.objects.filter(order__customer__user=self.request.user, order__status_id=1):
                total += item.total
            kwargs['total'] = total
            kwargs['order'] = Order.objects.filter()
            kwargs['address'] = Address.objects.filter(customer__user=self.request.user)
            kwargs['final'] = total
            return super().get_context_data(object_list=object_list, **kwargs)
        elif self.request.user.is_anonymous:
            total = 0
            try:
                for item in get_cookie(self.request):
                    total += item.total
                kwargs['total'] = total
                kwargs['order'] = Order.objects.filter()
                # kwargs['address'] = Address.objects.filter(customer__user=self.request.user)
                kwargs['final'] = total
                return super().get_context_data(object_list=object_list, **kwargs)
            except:
                kwargs['new'] = 'new'
                return super().get_context_data(object_list=object_list, **kwargs)


class CouponView(generics.RetrieveAPIView):
    """
    A view for getting coupon objects
    """
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()


class CouponImplantView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view for validating coupon code
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def partial_update(self, request, *args, **kwargs):
        """
        Updating order for the current user if the code is valid
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            self.request.data._mutable = True
            coupon = Coupon.objects.get(code=self.request.data['coupon'])
            request.data['coupon'] = coupon.id
            print('coupon', coupon.id)
            return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return HttpResponse('No such code', status=400)
