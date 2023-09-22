from django.urls import path

from .views import ProductViewList, ProductListAPI, ProductViewDetail

# The urls of products app.
urlpatterns = [
    path('', ProductViewList.as_view(), name='product_list'),
    path('<int:pk>/', ProductViewDetail.as_view(), name='product_detail'),
    path('api/', ProductListAPI.as_view(), name='product_list_api'),
    # path('price-api/', ProductPriceApi.as_view(), name='product_price_api'),

]
