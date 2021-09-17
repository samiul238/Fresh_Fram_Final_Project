from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

app_name = 'products'

urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>/', product_details, name='product_details'),
    path('cat/<str:cat>/', cat_products, name='cat_products'),
    path('subcat/<str:sub_cat>/', sub_cat_products, name='sub_cat_products'),

    # post url
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('edit_cart/', edit_cart, name='edit_cart'),
    path('add_to_reviews/', add_to_reviews, name='add_to_reviews'),
    path('add/rev/pro/<int:rev_pk>/<int:pro_pk>/',
         add_rep_rev, name='add_rep_rev'),
    path('del/rep/<int:rep_pk>/<int:pro_pk>/',
         reply_delete, name='reply_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
