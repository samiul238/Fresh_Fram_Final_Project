from django.contrib.admin import site
from .models import *

site.register(Sub_Category)
site.register(Category)
site.register(Product)
site.register(Cart)
site.register(DeliveryAddress)
site.register(Order)
site.register(Review)
site.register(Rating)
site.register(ReplyReview)
