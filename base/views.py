from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth import login, logout, authenticate
from .models import *
from products.models import *
from blog.models import Blog
from .sslcommerz import sslcommerz_payment_gateway
from django.views.decorators.csrf import csrf_exempt
import string
import random


def dictionary_merger(dictionary, request):
    dic = {
        'categories': Category.objects.all(),
        'sub_category': Sub_Category.objects.all(),
    }

    if request.user.is_authenticated:
        carts = list(Cart.objects.filter(user=request.user))
        carts.reverse()
        dic['carts'] = carts
        dic['num_of_product_in_cart'] = len(carts)
        dic['custom_user'] = Custom_User.objects.get(user=request.user)

        total_price = 0
        for cart in carts:
            total_price += cart.product.discount_price * cart.quantity
        dic['total_price'] = total_price

    dictionary.update(dic)
    return dictionary


@csrf_exempt
def index(request):
    products = Product.objects.all().order_by('-id')
    top_rated = Product.objects.all().order_by('star_rating')
    top_discount = Product.objects.all().order_by('-discount_percent')
    top_order = Product.objects.all().order_by('-order_count')

    # printer(top_discount)

    sold_items = []
    featured_products = []
    new_products = []
    for x in products:
        if 'sale' in x.include and len(sold_items) <= 10:
            sold_items.append(x)
        if 'featured' in x.include and len(featured_products) <= 10:
            featured_products.append(x)
        if 'new' in x.include and len(new_products) <= 10:
            new_products.append(x)
        if len(sold_items) >= 10 and len(featured_products) >= 10 and len(new_products) >= 10:
            break

    blogs = list(Blog.objects.all())[-3::]
    blogs.reverse()

    data = {
        'title': 'Fresh Farm',
        'home_banners': Home_Banner.objects.all(),
        'sold_items': sold_items,
        'featured_products': featured_products,
        'new_products': new_products,
        'blogs': blogs,
        'brands': Brand.objects.all(),
        'top_rated': top_rated,
        'top_discount': top_discount,
        'top_order': top_order,
    }

    data = dictionary_merger(data, request)
    return render(request, 'base/index.html', data)


def search(request):
    search = request.GET.get('search', None)

    if search is None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(name__icontains=search)

    priceRange = request.GET.get('priceRange', None)
    if not priceRange is None:
        pr = priceRange.split('$')
        up = float(pr[-1])
        down = float(pr[1].split(' ')[0])
        products = products.filter(
            discount_price__range=(down, up))

    products = list(products)
    products.reverse()

    rating = request.GET.get('rating', None)

    if not rating is None:
        tem_list = []
        for product in products:
            if type(product.rating()) == float:
                if float(rating) <= float(product.rating()) <= float(rating) + 0.99:
                    tem_list.append(product)
                if len(tem_list) > 300:
                    break
        products = tem_list

    num_of_post = 200
    page_no = request.GET.get('page', 1)
    paginator = Paginator(products, num_of_post)
    try:
        page_products = paginator.page(page_no)
    except EmptyPage:
        page_products = paginator.page(1)

    data = {
        'title': 'search | Fresh Farm',
        'products': page_products,
        'num_pages': paginator.num_pages,
    }
    data = dictionary_merger(data, request)
    return render(request, 'products/products.html', data)


def search_filter(request):
    # try:
    #     printer(request.POST['rating'])
    #     products = list(Product.objects.filter(rating=float(5)))
    # except:
    #     products = list(Product.objects.all())

    # products.reverse()

    # num_of_post = 48
    # page_no = request.GET.get('page', 1)
    # paginator = Paginator(products, num_of_post)
    # try:
    #     page_products = paginator.page(page_no)
    # except EmptyPage:
    #     page_products = paginator.page(1)

    data = {
        'title': 'search | Fresh Farm',
        # 'products': page_products,
        # 'num_pages': paginator.num_pages,
    }
    data = dictionary_merger(data, request)
    return render(request, 'products/products.html', data)


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('base:login_user')
    else:
        data = dictionary_merger({}, request)
        data['title'] = 'checkout'

        total_price = 0
        for cart in data['carts']:
            total_price += cart.product.discount_price * cart.quantity
        data['total_price'] = total_price

        if request.method == 'GET':
            cu = Custom_User.objects.get(user=request.user)
            data['address'] = cu.delivery_address

            return render(request, 'base/checkout.html', data)
        elif request.method == 'POST':
            d = request.POST

            product_ids = {}
            for cart in data['carts']:
                product_ids[cart.product.id] = cart.quantity
                # printer(f"id: {cart.product.id} ; quantity: {cart.quantity}")

            cu = Custom_User.objects.get(user=request.user)

            if float(d['totalPrice']) == float(data['total_price']):
                tran_id = str(request.user.id)
                tran_id += unique_trangection_id_generator()
                order = Order(
                    user=request.user,
                    product_ids=product_ids,
                    total_price=d['totalPrice'],
                    delivery_address=cu.delivery_address,
                    tran_id=tran_id
                )
                order.save()
                amount = float(d['totalPrice'])
                return redirect(sslcommerz_payment_gateway(request, amount, tran_id))
            else:
                return redirect('base:orders')  # Will add some error
            return redirect('base:orders')


def unique_trangection_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def del_cart(request, pk):
    if not request.user.is_authenticated:
        return redirect('base:login_user')

    if request.method == 'POST':
        cart = Cart.objects.get(pk=pk)
        if request.user == cart.user:
            product = Product.objects.get(pk=cart.product.id)
            product.count_in_stock += int(cart.quantity)
            cart.delete()
            product.save()
            return redirect('base:checkout')


def orders(request):
    data = {
        'orders': Order.objects.filter(user=request.user),
        'title': 'order',
    }

    data = dictionary_merger(data, request)
    return render(request, 'base/order.html', data)


@csrf_exempt
def error(request):
    return render(request, 'error.html')


def order_details(request, pk):
    if not request.user.is_authenticated:
        return redirect('base:login_user')

    order = Order.objects.get(pk=pk)
    if request.user != order.user and not request.user.is_superuser:
        return redirect('base:index')

    order.product_ids = eval(order.product_ids)
    order.product_ids = order.product_ids.items()

    data = {
        'order': order,
        'title': 'Order details',
    }

    data = dictionary_merger(data, request)
    return render(request, 'base/order_details.html', data)


def offers(request):
    offers = Offer.objects.all()

    data = {
        'offers': offers,
        'title': 'title',
    }

    data = dictionary_merger(data, request)
    return render(request, 'base/offers.html', data)


def need_help(request):
    data = {
        'title': 'Help',
    }
    data = dictionary_merger(data, request)
    return render(request, 'base/help.html', data)


def contact(request):
    data = dictionary_merger({}, request)
    data['title'] = 'Contact'

    if request.method == "GET":
        return render(request, 'base/contact.html', data)
    elif request.method == 'POST':
        data = request.POST
        message = Contact(name=data['name'], email=data['email'],
                          subject=data['subject'], message=data['message'])
        message.save()
        return render(request, 'base/contact.html', data)


def subscribe(request):
    if request.method == "POST":
        subscribe = Subscribe(email=request.POST['email'])
        subscribe.save()
    return redirect('base:index')


def login_user(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            data = {'title': 'Login | Fresh Farm'}
            data = dictionary_merger(data, request)
            return render(request, 'login_user.html', data)
        elif request.method == 'POST':
            d = request.POST
            try:
                user = User.objects.get(email=d['email'])
            except:
                return render(request, 'login_user.html', {'error': 'No user with this email'})

            user_to_login = authenticate(
                request, username=user.username, password=d['password'])

            if user_to_login is None:
                return render(request, 'login_user.html', {'error': 'Username or password is not valid'})
            else:
                login(request, user_to_login)
                return redirect('base:index')
    else:
        return redirect('base:profile')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('base:index')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('base:profile')

    if request.method == 'GET':
        data = {'title': 'Register | Fresh Farm'}
        data = dictionary_merger(data, request)
        return render(request, 'register_user.html', data)

    elif request.method == 'POST':
        d = request.POST

        if d['password'] != d['password1']:
            return render(request, 'register_user.html', {'error': 'passwords did not matched !'})

        if len(User.objects.filter(username=d['username'])) > 0:
            error = 'username {} is all ready taken, try another'.format(
                d['username'])
            return render(request, 'register_user.html', {'error': error})

        if len(User.objects.filter(email=d['email'])) > 0:
            error = 'Email {} is all ready registered, try another'.format(
                d['email'])
            return render(request, 'register_user.html', {'error': error})

        user = User.objects.create_user(
            first_name=d['firstName'],
            last_name=d['lastName'],
            password=d['password'],
            email=d['email'],
            username=d['username']
        )
        user.save()
        cu = Custom_User(user=user)
        cu.save()

        login(request, user)

        return redirect('base:profile')


def profile(request):
    if request.user.is_authenticated:
        data = {
            'title': 'Profile',
            'custom_user': Custom_User.objects.get(user=request.user),
            'contact_number': Contact_Number.objects.filter(user=request.user)
        }
        data = dictionary_merger(data, request)
        return render(request, 'profile.html', data)
    else:
        return redirect('base:login_user')


def change_password(request):
    if not request.user.is_authenticated:
        return redirect('base:login_user')

    data = {'title': 'Fresh Farm-Change Password'}
    if request.method == 'GET':
        return render(request, 'change_password.html', data)

    elif request.method == 'POST':
        d = request.POST

        if d['newPassword'] != d['repeatPassword']:
            data['error'] = 'New passwords did not match !'
            return render(request, 'change_password.html', data)

        user = authenticate(
            request, username=request.user.username,
            password=d['oldPassword']
        )
        if user is None:
            data['error'] = 'Old password did not match !'
            return render(request, 'change_password.html', data)
        else:
            user.set_password(d['newPassword'])
            user.save()
            return redirect('base:login_user')


def add_to_custom_user(request):
    if not request.user.is_authenticated:
        return redirect('base:login_user')

    if request.method == 'POST':
        cu = Custom_User.objects.get(user=request.user)

        d = request.POST
        first_name = d['first_name']
        last_name = d['last_name']
        email = d['email']
        try:
            avatar = request.FILES['avatar']
            if not 'default_profile320.png' in str(cu.avatar):
                cu.avatar.delete()
            cu.avatar = avatar
        except:
            pass

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        cu.save()

    return redirect('base:profile')


def add_to_contact_number(request):
    if not request.user.is_authenticated:
        return redirect('base:login_user')

    d = request.POST
    number_type = d['number_type']
    number = d['number']

    cn = Contact_Number(
        user=request.user,
        number=number,
        number_type=number_type
    )
    cn.save()
    return redirect('base:profile')


def delete_contact_number(request):
    number = Contact_Number.objects.get(pk=request.POST['number'])
    number.delete()
    return redirect('base:profile')


def add_to_delivery_address(request):
    if not request.user.is_authenticated:
        return redirect('base:login_user')

    if request.method == "POST":
        cu = Custom_User.objects.get(user=request.user)
        cu.delivery_address = request.POST['deliveryAddress']
        cu.save()
        return redirect('base:profile')


def printer(x):
    x = str(x)
    separator = '-------------------------------------'
    print(separator)
    print(x)
    print(separator)
