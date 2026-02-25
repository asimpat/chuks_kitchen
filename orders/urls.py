from django.urls import path
from .views import (
    PlaceOrderView,
    CustomerOrderListView,
    CustomerOrderDetailView,
    CustomerCancelOrderView,
    AdminOrderListView,
    AdminUpdateOrderStatusView,
    AdminUpdatePaymentStatusView
)

urlpatterns = [
    # Create order from cart
    path('', PlaceOrderView.as_view(), name='create-order'),

    # View cart (list all my orders)
    path('my-orders/', CustomerOrderListView.as_view(), name='my-orders'),

    # Fetch order details & status
    path('<int:pk>/',
         CustomerOrderDetailView.as_view(), name='order-detail'),

    # clear cart (cancel pending order)
    path('clear-cart/<int:pk>/',
         CustomerCancelOrderView.as_view(), name='clear-cart'),


    # Admin role
    path('admin/all/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/<int:pk>/status/', AdminUpdateOrderStatusView.as_view(),
         name='admin-update-status'),
    path('admin/<int:pk>/payment-status/', AdminUpdatePaymentStatusView.as_view(),
         name='admin-update-payment-status'),

]
