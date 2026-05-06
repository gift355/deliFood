
from django.contrib import admin
from django.urls import path, include
from users.views import landing_view
from django.conf import settings
from django.conf.urls.static import static


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('users/', include('users.urls')),
#     path('driver/', include('drivers.urls')),
# ]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_view),  
    path('users/', include('users.urls')),
    path('driver/', include('drivers.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('menu/', include('menu.urls')),
    path('orders/', include('orders.urls')),
    path('cart/', include('cart.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)