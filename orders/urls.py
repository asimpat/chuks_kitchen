from django.urls import path
from .views import (
    PlaceOrderView,
    CustomerOrderListView,
    CustomerOrderDetailView,
    CustomerCancelOrderView,
    AdminOrderListView,
    AdminUpdateOrderStatusView
)

urlpatterns = [
    path('place/', PlaceOrderView.as_view(), name='place-order'),
    path('my-orders/', CustomerOrderListView.as_view(), name='my-orders'),
    path('my-orders/<int:pk>/',
         CustomerOrderDetailView.as_view(), name='order-detail'),
    path('cancel/<int:pk>/', CustomerCancelOrderView.as_view(), name='cancel-order'),

  
    path('admin/all/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/<int:pk>/status/', AdminUpdateOrderStatusView.as_view(),
         name='admin-update-status'),
]
