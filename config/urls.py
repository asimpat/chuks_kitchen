from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auths.urls')),
    path('foods/', include('foods.urls')),
    path('orders/', include('orders.urls'))
]
