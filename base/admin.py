from django.contrib.admin import site
from .models import *


# site.register(Transaction)
site.register(PaymentGatewaySettings)

# site.register(Offer)
site.register(Contact)
site.register(Subscribe)
# site.register(Home_Banner)
site.register(Custom_User)
# site.register(Brand)
# site.register(Contact_Number)
