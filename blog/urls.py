from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>/', blog_details, name='blog_details'),

    # post method
    path('add_to_comments/<int:pk>/', add_to_comments, name='add_to_comments'),
    path('add_to_reply/<int:cpk>/<int:bpk>/',
         add_to_reply, name="add_to_reply"),
    path('rep/del/<int:rpk>/<int:bpk>/', reply_delete, name="reply_delete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
