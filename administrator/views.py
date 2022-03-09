from django.shortcuts import render, get_object_or_404, redirect
from .models import post, category
from accounts.views import user_posts


# Create your views here.

def posts(requests):
    context = {
        "post": post.objects.filter(status="p").order_by("-publish"),
        "category": category.objects.filter(status=True),
    }
    return render(requests, "administrator/index.html", context)


def detail(requests, slug):
    context = {
        "post": get_object_or_404(post, slug=slug, status="p"),
        "category": category.objects.filter(status=True),
    }
    return render(requests, "administrator/product-detail.html", context)


def categry(requests, slug):
    context = {
        'cate': get_object_or_404(category, slug=slug, status=True),
        "category": category.objects.filter(status=True),
    }
    return render(requests, "administrator/category.html", context)
