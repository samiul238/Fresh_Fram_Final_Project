from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
# from django.http import HttpResponse
from products.models import *
from base.models import Subscribe
from base.views import printer, dictionary_merger


def index(request):
    one_page = False
    products = list(Product.objects.all())
    products.reverse()
    num_of_post = 16
    page_no = request.GET.get('page', 1)

    if int(page_no) > 1:
        one_page = True
    paginator = Paginator(products, num_of_post)
    try:
        page_products = paginator.page(page_no)
    except EmptyPage:
        page_products = paginator.page(1)

    data = {
        'title': 'Shop | Fresh Farm',
        'products': page_products,
        'num_pages': paginator.num_pages,
        'one_page': one_page,
    }
    data = dictionary_merger(data, request)
    return render(request, 'products/products.html', data)


def cat_products(request, cat):
    if request.method == 'GET':
        cat = Category.objects.get(name=cat)
        cat_products = Product.objects.filter(category=cat.id)
        one_page = False

        priceRange = request.GET.get('priceRange', None)
        if not priceRange is None:
            pr = priceRange.split('$')
            up = float(pr[-1])
            down = float(pr[1].split(' ')[0])
            cat_products = cat_products.filter(
                discount_price__range=(down, up))

        cat_products = list(cat_products)
        cat_products.reverse()

        rating = request.GET.get('rating', None)

        if not rating is None:
            tem_list = []
            for product in cat_products:
                if type(product.rating()) == float:
                    if float(rating) <= float(product.rating()) <= float(rating) + 0.99:
                        tem_list.append(product)
                    if len(tem_list) > 300:
                        break
            cat_products = tem_list

        num_of_post = 48
        page_no = request.GET.get('page', 1)

        if int(page_no) > 1:
            one_page = True

        paginator = Paginator(cat_products, num_of_post)
        try:
            page_products = paginator.page(int(page_no))
        except EmptyPage:
            page_products = paginator.page(1)

        data = {
            'title': 'Shop | Fresh Farm',
            'products': page_products,
            'cate': cat,
            'one_page': one_page,
        }
        data = dictionary_merger(data, request)
        return render(request, 'products/cat_products.html', data)

    elif request.method == "POST":
        # printer(request.POST)
        subscribe = Subscribe(email=request.POST['email'])
        subscribe.save()
        return redirect('products:cat_products', cat)


def sub_cat_products(request, sub_cat):
    sub_cat = Sub_Category.objects.get(name=sub_cat)
    cat_products = Product.objects.filter(sub_category=sub_cat.id)
    one_page = False

    priceRange = request.GET.get('priceRange', None)
    if not priceRange is None:
        pr = priceRange.split('$')
        up = float(pr[-1])
        down = float(pr[1].split(' ')[0])
        cat_products = cat_products.filter(
            discount_price__range=(down, up))

    cat_products = list(cat_products)
    cat_products.reverse()

    rating = request.GET.get('rating', None)

    if not rating is None:
        tem_list = []
        for product in cat_products:
            if type(product.rating()) == float:
                if float(rating) <= float(product.rating()) <= float(rating) + 0.99:
                    tem_list.append(product)
                if len(tem_list) > 300:
                    break
        cat_products = tem_list

    num_of_post = 48
    page_no = request.GET.get('page', 1)
    if int(page_no) > 1:
        one_page = True
    paginator = Paginator(cat_products, num_of_post)
    try:
        page_products = paginator.page(page_no)
    except EmptyPage:
        page_products = paginator.page(1)

    data = {
        'title': 'Shop | Fresh Farm',
        'products': page_products,
        'one_page': one_page,
        'cate': sub_cat,
    }
    data = dictionary_merger(data, request)
    return render(request, 'products/sub_cat_pro.html', data)


def product_details(request, pk):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=pk)
        reviews = list(Review.objects.filter(product=pk))
        reviews.reverse()

        # related_products = list(Product.objects.filter(
        #     sub_category=product.sub_category))
        related_products = list(Product.objects.all())
        related_products.reverse()

        data = {
            'title': str(product.name) + ' | Fresh Farm',
            'product': product,
            'reviews': reviews,
            'reviews_count': len(reviews),
            'related_products': related_products[0:10],
        }

        data = dictionary_merger(data, request)
        return render(request, 'products/product_details.html', data)


def add_to_cart(request):
    if not request.user.is_authenticated:
        return redirect('base:login_user')

    if request.method == 'POST':
        product = get_object_or_404(Product, pk=request.POST['product_id'])
        quantity = request.POST['quantity']
        cart = Cart(
            product=product,
            user=request.user,
            quantity=quantity
        )
        cart.save()
        product.count_in_stock -= int(quantity)
        product.order_count += 1
        product.save()

        try:
            red = request.POST['redirect']
        except:
            red = None

        try:
            argu = request.POST['argu']
        except:
            argu = None

        if red:
            if argu:
                return redirect(red, argu)
            return redirect(red)

        return redirect('products:product_details', product.id)


def edit_cart(request):
    if not request.user.is_authenticated:
        return redirect('base:login_user')

    if request.method == 'POST':
        d = request.POST
        cart = Cart.objects.get(pk=d['cart_id'])
        product = Product.objects.get(pk=cart.product.id)

        if d['type'] == 'increase':
            if product.count_in_stock > 0:
                cart.quantity += int(d['quantity'])
                product.count_in_stock -= int(d['quantity'])
        elif d['type'] == 'decrease':
            if cart.quantity > 1:
                cart.quantity -= int(d['quantity'])
                product.count_in_stock += int(d['quantity'])
        else:
            printer('cart edit gone wrong')

        product.save()
        cart.save()

        return redirect('base:checkout')


def add_to_reviews(request):
    if not request.user.is_authenticated:
        return redirect('base:login_user')

    if request.method == 'POST':
        d = request.POST

        review = Review(
            product=Product.objects.get(pk=d['product_id']),
            user=request.user,
            comment=d['comment']
        )
        review.save()

        try:
            star = d['star']
            printer(star)
            if len(Rating.objects.filter(product=d['product_id'], user=request.user)) < 1:
                rating = Rating(
                    product=Product.objects.get(pk=d['product_id']),
                    user=request.user,
                    star=star
                )
                rating.save()

            else:
                rating = Rating.objects.get(
                    product=d['product_id'],
                    user=request.user
                )
                rating.star = star
                rating.save()
        except:
            pass

        return redirect('products:product_details', d['product_id'])


def add_rep_rev(request, rev_pk, pro_pk):
    if not request.user.is_authenticated:
        return redirect('base:login_user')

    if request.method == 'POST':
        review = Review.objects.get(pk=rev_pk)
        d = request.POST

        reply = ReplyReview(
            review=review,
            user=request.user,
            rep_comment=d['repCom']
        )
        reply.save()
    return redirect('products:product_details', pro_pk)


def reply_delete(request, rep_pk, pro_pk):
    if not request.user.is_authenticated:
        return redirect('base:login_user')

    if request.method == 'POST':
        reply = ReplyReview.objects.get(pk=rep_pk)

        if request.user == reply.user:
            reply.delete()

    return redirect('products:product_details', pro_pk)
