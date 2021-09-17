from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

app_name = 'base'

urlpatterns = [
    path('', index, name='index'),
    path('offers/', offers, name='offers'),
    path('search/', search, name='search'),
    path('filter/', search_filter, name='search_filter'),
    path('help/', need_help, name='help'),
    path('contact/', contact, name='contact'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', orders, name='orders'),
    path('error/', error, name='error'),
    path('orders/<int:pk>/', order_details, name='order_details'),
    path('subscribe/', subscribe, name='subscribe'),
    path('login/', login_user, name='login_user'),
    path('register/', register_user, name='register_user'),
    path('logout/', logout_user, name='logout_user'),
    path('profile/', profile, name='profile'),
    path('change/password/', change_password, name='change_password'),

    # add urls
    path('add_to_custom_user/', add_to_custom_user, name="add_to_custom_user"),
    path('add_to_contact_number/', add_to_contact_number,
         name="add_to_contact_number"),
    path('add_to_delivery_address/', add_to_delivery_address,
         name="add_to_delivery_address"),

    # delete urls
    path('delete_contact_number/', delete_contact_number,
         name="delete_contact_number"),
    path('delete/cart/<int:pk>/', del_cart, name="del_cart"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
