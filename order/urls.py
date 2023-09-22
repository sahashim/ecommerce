from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order.views import AddCard, OrderItemList, DeleteOrderItem, UpdateOrderItem, CouponView, CouponImplantView

router = DefaultRouter()
router.register('orderitem', AddCard)
# urlpatterns = router.urls

# The urls of orders app
urlpatterns = [
    path('', include(router.urls), ),
    path('order/', OrderItemList.as_view(), name='orders_list'),
    path('delete/<int:pk>', DeleteOrderItem.as_view(), name='delete_item'),
    path('update/<int:pk>', UpdateOrderItem.as_view(), name='update_item'),
    path('coupon_get/<int:pk>', CouponView.as_view(), name='coupon_get'),
    path('coupon/<int:pk>', CouponImplantView.as_view(), name='coupon'),

]
