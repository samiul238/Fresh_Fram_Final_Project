import string
import random
from django.conf import settings

from sslcommerz_lib import SSLCOMMERZ
from .models import PaymentGatewaySettings


def sslcommerz_payment_gateway(request, amount, tran_id):

    gateway_auth_details = PaymentGatewaySettings.objects.all().first()
    settings = {'store_id': gateway_auth_details.store_id,
                'store_pass': gateway_auth_details.store_pass, 'issandbox': True}

    # url = 'https://himelbikon.pythonanywhere.com/'
    url = "http://127.0.0.1:8000/"

    sslcommez = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = tran_id
    post_body['success_url'] = url
    post_body['fail_url'] = url + 'error/'
    post_body['cancel_url'] = url
    post_body['emi_option'] = 0
    post_body['cus_name'] = request.user.username
    post_body['cus_email'] = request.user.email
    post_body['cus_phone'] = 'request.data["phone"]'
    post_body['cus_add1'] = 'request.data["address"]'
    post_body['cus_city'] = 'request.data["address"]'
    post_body['cus_country'] = 'Bangladesh'
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"

    # OPTIONAL PARAMETERS
    post_body['value_a'] = request.user.username

    response = sslcommez.createSession(post_body)
    return 'https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY=' + response["sessionkey"]
