from django.shortcuts import render
from .models import Category, Product
from django.shortcuts import get_object_or_404

# Create your views here.

def store(request):
    all_products = Product.objects.all()

    context = {'all_products': all_products}

    return render(request, 'store/store.html', context)

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    context = {'product': product}

    return render(request, 'store/product_detail.html', context)


def categories(request):
    all_categories = Category.objects.all()

    return {'all_categories': all_categories}

def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products
    }

    return render(request, 'store/category_list.html', context)