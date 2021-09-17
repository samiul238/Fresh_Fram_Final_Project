from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', index, name='index'),

    path('add/category/', add_category, name='add_category'),
    path('edit/category/<int:pk>/', edit_category, name='edit_category'),
    path('delete/category/<int:pk>/', delete_category, name="delete_category"),

    path('add/sub/category/', add_sub_category, name='add_sub_category'),
    path('edit/sub/category/<int:pk>/',
         edit_sub_category, name='edit_sub_category'),
    path('delete/sub/category/<int:pk>/',
         delete_sub_category, name="delete_sub_category"),

    path('products/', products, name='products'),
    path('edit/products/<int:pk>/', edit_product, name='edit_product'),
    path('delete/product/<int:pk>/', delete_product, name='delete_product'),


    path('banner/', banner, name='banner'),
    path('edit/banner/<int:pk>/', edit_banner, name='edit_banner'),
    path('delete/banner/<int:pk>/', delete_banner, name='delete_banner'),

    path('blogs/', blogs, name='blogs'),
    path('edit/blog/<int:pk>/', edit_blog, name='edit_blog'),
    path('delete/blog/<int:pk>/', delete_blog, name='delete_blog'),

    path('brands/', brands, name='brands'),
    path('delete/brands/<int:pk>/', delete_brands, name='delete_brands'),

    path('orders/', orders, name='orders'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
