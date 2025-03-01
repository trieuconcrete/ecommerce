from django.shortcuts import render
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)

    context = {
        'cart': cart
    }

    return render(request, 'cart/cart_summary.html', context)


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, product_qty=product_quantity)

        cart_quantity = cart.__len__()

        response = JsonResponse({
            'cart_quantity': cart_quantity
        })
        return response
    else:
        return JsonResponse({'error': 'Invalid or missing action'}, status=400)



def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)

        cart_quantity = cart.__len__()
        cart_total = cart.get_total()

        response = {
            'qty': cart_quantity,
            'total': cart_total
        }

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid or missing action'}, status=400)


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        print(product_quantity)

        cart.update(product=product_id, qty=product_quantity)

        cart_quantity = cart.__len__()
        cart_total = cart.get_total()

        response = {
            'qty': cart_quantity,
            'total': cart_total
        }

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid or missing action'}, status=400) 