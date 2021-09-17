from django.shortcuts import render, redirect, get_object_or_404
from base.views import printer, dictionary_merger
from base.models import *
from base.forms import *
from products.models import *
from .forms import *
from blog.models import *
from blog.forms import *


def index(request):
    if not request.user.is_superuser:
        return redirect('base:index')

    data = {
        'categories': Category.objects.all(),
        'sub_categories': Sub_Category.objects.all(),
        'title': 'fresh farm- Dashboard',
    }
    data = dictionary_merger(data, request)
    return render(request, 'dashboard/index.html', data)


def banner(request):
    if not request.user.is_superuser:
        return redirect('base:login_user')

    if request.method == 'GET':
        banners = Home_Banner.objects.all()
        data = {
            'banners': banners,
            'form': Home_BannerForm()
        }
        data = dictionary_merger(data, request)
        return render(request, 'dashboard/banner.html', data)

    if request.method == 'POST':
        form = Home_BannerForm(request.POST, request.FILES)
        form.save()
        return redirect('dashboard:banner')


def edit_banner(request, pk):
    if not request.user.is_superuser:
        return redirect('base:login_user')

    hb = Home_Banner.objects.get(pk=pk)
    if request.method == 'GET':
        banners = Home_Banner.objects.all()
        data = {
            'form': Home_BannerForm(instance=hb)
        }
        data = dictionary_merger(data, request)
        return render(request, 'dashboard/banner.html', data)

    if request.method == 'POST':
        form = Home_BannerForm(request.POST, request.FILES, instance=hb)
        try:
            image = request.FILES['image']
            hb.image.delete()
        except:
            pass

        form.save()
        return redirect('dashboard:banner')


def delete_banner(request, pk):
    if not request.user.is_superuser:
        return redirect('base:login_user')

    if request.method == 'POST':
        banner = Home_Banner.objects.get(pk=pk)
        banner.delete()

    return redirect('dashboard:banner')


def products(request):
    if not request.user.is_superuser:
        return redirect('base:index')

    if request.method == 'GET':
        products = list(Product.objects.all())
        products.reverse()
        data = {
            'form': ProductForm(),
            'products': products,
        }
        data = dictionary_merger(data, request)
        return render(request, 'dashboard/products.html', data)

    elif request.method == 'POST':
        product = ProductForm(request.POST, request.FILES)
        product.save()
        return redirect('dashboard:products')


def edit_product(request, pk):
    if not request.user.is_superuser:
        return redirect('base:index')

    product = Product.objects.get(pk=pk)
    if request.method == 'GET':
        data = {
            'form': ProductForm(instance=product),
        }
        data = dictionary_merger(data, request)
        return render(request, 'dashboard/products.html', data)

    elif request.method == 'POST':

        try:
            image = request.FILES['image']
            product.image.delete()
        except:
            pass

        try:
            video = request.FILES['video']
            product.video.delete()
        except:
            pass

        update = ProductForm(request.POST, request.FILES, instance=product)
        update.save()
        return redirect('dashboard:products')


def delete_product(request, pk):
    if not request.user.is_superuser:
        return redirect('base:index')

    if request.method == 'POST':
        product = Product.objects.get(pk=pk)
        product.delete()

    return redirect('dashboard:products')


def add_category(request):
    if not request.user.is_superuser:
        return redirect('base:index')

    if request.method == 'GET':
        data = {'form': Addcat_Form()}
        data = dictionary_merger(data, request)
        return render(request, 'dashboard/add_category.html', data)

    elif request.method == 'POST':
        form = Addcat_Form(request.POST, request.FILES)
        form.save()
        return redirect('dashboard:index')


def edit_category(request, pk):
    if not request.user.is_superuser:
        return redirect('base:index')

    category = get_object_or_404(Category, pk=pk)

    if request.method == 'GET':

        data = {
            'form': Addcat_Form(instance=category),
        }
        data = dictionary_merger(data, request)
        return render(request, 'dashboard/add_category.html', data)

    elif request.method == 'POST':
        category.name = request.POST['name']

        try:
            image = request.FILES['image']
            category.image.delete()
            category.image = image
        except:
            pass

        category.save()

        return redirect('dashboard:index')


def delete_category(request, pk):
    if not request.user.is_superuser:
        return redirect('base:index')

    if request.method == 'POST':
        category = Category.objects.get(pk=pk)
        category.delete()

    return redirect('dashboard:index')


def add_sub_category(request):
    if not request.user.is_superuser:
        return redirect('base:index')

    if request.method == 'GET':
        data = {'form': Sub_CategoryForm()}
        data = dictionary_merger(data, request)
        return render(request, 'dashboard/sub_cat.html', data)

    if request.method == 'POST':
        sc = Sub_CategoryForm(request.POST)
        sc.save()
        return redirect('dashboard:index')


def edit_sub_category(request, pk):
    if not request.user.is_superuser:
        return redirect('base:index')

    sc = Sub_Category.objects.get(pk=pk)
    if request.method == 'GET':
        data = {'form': Sub_CategoryForm(instance=sc)}
        data = dictionary_merger(data, request)
        return render(request, 'dashboard/sub_cat.html', data)

    if request.method == 'POST':
        form = Sub_CategoryForm(request.POST, instance=sc)
        form.save()
        return redirect('dashboard:index')


def delete_sub_category(request, pk):
    if not request.user.is_superuser:
        return redirect('base:index')

    if request.method == 'POST':
        sc = Sub_Category.objects.get(pk=pk)
        sc.delete()
        return redirect('dashboard:index')


def blogs(request):
    if not request.user.is_superuser:
        return redirect('base:login_user')

    if request.method == "GET":
        blogs = list(Blog.objects.all())
        blogs.reverse()

        data = {
            'blogs': blogs,
            'form': BlogForm(),
        }
        data = dictionary_merger(data, request)
        return render(request, 'dashboard/blogs.html', data)

    elif request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        update = form.save(commit=False)

        update.user = request.user
        update.save()

        return redirect('dashboard:blogs')


def edit_blog(request, pk):
    if not request.user.is_superuser:
        return redirect('base:login_user')

    blog = Blog.objects.get(pk=pk)
    if request.method == "GET":
        data = {
            'form': BlogForm(instance=blog),
        }
        data = dictionary_merger(data, request)
        return render(request, 'dashboard/blogs.html', data)

    elif request.method == "POST":
        try:
            image = request.FILES['image']
            blog.image.delete()
        except:
            pass

        form = BlogForm(request.POST, request.FILES, instance=blog)
        form.save()
        return redirect('dashboard:blogs')


def delete_blog(request, pk):
    if not request.user.is_superuser:
        return redirect('base:login_user')

    if request.method == "POST":
        blog = Blog.objects.get(pk=pk)
        blog.delete()
        return redirect('dashboard:blogs')


def brands(request):
    if not request.user.is_superuser:
        return redirect('base:login_user')

    if request.method == "GET":
        brands = list(Brand.objects.all())
        brands.reverse()

        data = {
            'brands': brands,
            'form': BrandForm(),
        }
        data = dictionary_merger(data, request)
        return render(request, 'dashboard/brands.html', data)

    elif request.method == "POST":
        form = BrandForm(request.POST, request.FILES)
        form.save()
        return redirect('dashboard:brands')


def delete_brands(request, pk):
    if not request.user.is_superuser:
        return redirect('base:login_user')

    if request.method == 'POST':
        brand = Brand.objects.get(pk=pk)
        brand.delete()
        return redirect('dashboard:brands')


def orders(request):
    orders = list(Order.objects.all())
    orders.reverse()

    data = {
        'orders': orders,
    }
    data = dictionary_merger(data, request)
    return render(request, 'base/order.html', data)
