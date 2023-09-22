# Create your views here.

from django.views import generic
from rest_framework import generics

from product.models import Product, Category, Brand
from product.serializers import ProductSerializer, CategorySerializer


class ProductViewList(generic.ListView):
    """
    A view to show the product list and categories for shop section.
    """
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['product'] = Product.objects.all()
        kwargs['brand'] = Brand.objects.all()
        # cat_id = self.request.GET['cat_id']
        # products = Product.objects.filter(category_id=cat_id)
        return super().get_context_data(object_list=object_list, **kwargs)

    # context_object_name = 'product_list'
    queryset = Category.objects.filter(is_active=True, is_delete=False).order_by('name')[:5]
    template_name = 'product/product_list.html'
    extra_context = {'title': 'Products'}


class ProductListAPI(generics.ListCreateAPIView):
    """
    API view to filter the products.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.filter()

    def get_queryset(self):
        # cat_id = self.request.GET['cat_id']
        # q = Product.objects.filter()
        # print('a',q)
        fil = dict(self.request.GET)
        try:
            for k, v in fil.items():
                fil[k] = ''.join(v)
            queryset = Product.objects.filter(**fil)
        except Exception:
            return super().get_queryset()
        # print(queryset)
        # maxi = self.request.GET['to']
        # print('hi', cat_id)
        # print('hi', mini)
        # print('hi', maxi)
        # products = Product.objects.filter(category_id=cat_id).filter(price__gt=maxi).filter(price__lte=mini)
        # products = Product.objects.filter(category_id=cat_id)
        return queryset


# class ProductPriceApi(generics.ListCreateAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.filter()
#
#     def get_queryset(self):
#         mini = self.request.GET['from']
#         maxi = self.request.GET['to']
#         print(mini, maxi)
#         products = Product.objects.filter(price=2000)
#
#         return products


class CategoryListAPI(generics.ListCreateAPIView):
    """
    A view for showing the categories on shop.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductViewDetail(generic.DetailView):
    """
    The detail view for each product.
    """
    model = Product
    template_name = 'product/product_detail.html'
