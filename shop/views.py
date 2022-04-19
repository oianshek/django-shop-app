from django.shortcuts import get_object_or_404, render

from .models import Category, Item


def item_list(request):
    items = Item.items.all()
    return render(request, 'shop/home.html', {'items': items})


def item_detail(request, slug):
    item = get_object_or_404(Item, slug=slug, in_stock=True)
    return render(request, 'shop/items/detail.html', {'item': item})


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    items = Item.objects.filter(category=category, in_stock=True)
    return render(request, 'shop/items/category.html', {'category': category, 'items': items})
