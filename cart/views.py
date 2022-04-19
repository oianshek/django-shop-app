from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .cart import Cart
from shop.models import *


def cart_summary(request):
    cart = Cart(request)
    return render(request, 'shop/cart/summary.html', {'cart': cart})

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        item_id = int(request.POST.get('item_id'))
        item_qty = int(request.POST.get('item_qty'))
        item = get_object_or_404(Item, id=item_id)
        cart.add(item=item, item_qty=item_qty)
        
        cart_qty = cart.__len__()
        response = JsonResponse({'item_qty': cart_qty})
        return response

def cart_delete(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        item_id = int(request.POST.get('item_id'))
        cart.delete(item=item_id)

        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()

        response = JsonResponse({'item_qty': cart_qty, 'total_price': cart_total})
        return response

def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        item_id = int(request.POST.get('item_id'))
        item_qty = int(request.POST.get('item_qty'))
        cart.update(item=item_id, item_qty=item_qty)

        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()

        response = JsonResponse({'item_qty': cart_qty, 'total_price': cart_total})
        return response