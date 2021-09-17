from django.contrib.admin import site
from .models import *

site.register(Blog)
site.register(Comment)
site.register(ReplyComment)
