from django import template
from products.models import Product, Sub_Category
from base.views import printer

register = template.Library()


@register.filter
def category_product_counter(cate):
    products = Product.objects.all()
    cate_count = []

    for product in products:
        if str(product.category) == str(cate):
            cate_count.append(product)
            # printer(str(product.category))

    if len(cate_count) < 10:
        return '0' + str(len(cate_count))
    else:
        return str(len(cate_count))


@register.filter
def sub_cat_finder(cat):
    sub_cat = Sub_Category.objects.filter(category=cat)
    return sub_cat


@register.filter
def product_finder(_id):
    product = Product.objects.get(pk=_id)
    return product


@register.filter
def looper(limit):
    '''<option>2</option>'''
    options = ''
    for r in range(1, 1 + int(limit)):
        if r == 1:
            options += f'<option selected>{r}</option>'
        else:
            options += f'<option>{r}</option>'

    return options
