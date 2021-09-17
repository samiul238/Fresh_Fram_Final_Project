from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from .models import *
from products.models import Product, Category
from base.views import printer, dictionary_merger


def index(request):
    blogs = Blog.objects.all().order_by('-id')
    one_page = False
    num_of_post = 10

    search = request.GET.get('search', None)
    if search is not None:
        blogs = blogs.filter(title__icontains=search)
        num_of_post = 50

    page_no = request.GET.get('page', 1)

    if int(page_no) > 1:
        one_page = True

    paginator = Paginator(blogs, num_of_post)
    try:
        page_blogs = paginator.page(page_no)
    except EmptyPage:
        page_blogs = paginator.page(1)

    # printer(paginator.num_pages)

    data = {
        'blogs': page_blogs,
        'num_pages': paginator.num_pages,
        'title': 'Blog | Fresh farm',
        'Pfeeds': blogs[2:10],
        'one_page': one_page,
    }

    data = dictionary_merger(data, request)
    return render(request, 'blog/index.html', data)


def blog_details(request, pk):
    if request.method == 'GET':
        comments = Comment.objects.filter(blog=pk)
        blog = get_object_or_404(Blog, pk=pk)

        comments = list(comments)
        comments.reverse()

        data = {
            'title': blog.title,
            'blog': blog,
            'comments': comments,
            'num_comments': len(comments)
        }

        data = dictionary_merger(data, request)
        return render(request, "blog/blog_details.html", data)


def add_to_comments(request, pk):
    if request.user.is_authenticated:
        redirect('base:login_user')

    if request.method == 'POST':
        comment = Comment(
            blog=Blog.objects.get(pk=pk),
            user=request.user,
            comment=request.POST['comment']
        )
        comment.save()
        return redirect('blog:blog_details', pk)


def add_to_reply(request, cpk, bpk):
    if request.user.is_authenticated:
        redirect('base:login_user')

    if request.method == 'POST':
        comment = Comment.objects.get(pk=cpk)
        d = request.POST
        reply = ReplyComment(
            comment=comment,
            user=request.user,
            rep_comment=d['repCom']
        )
        reply.save()

    return redirect('blog:blog_details', bpk)


def reply_delete(request, rpk, bpk):
    if request.user.is_authenticated:
        redirect('base:login_user')

    if request.method == 'GET':
        return redirect('blog:blog_details', bpk)

    reply = ReplyComment.objects.get(pk=rpk)

    if request.user == reply.user:
        reply.delete()

    return redirect('blog:blog_details', bpk)
