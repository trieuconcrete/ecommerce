from django.shortcuts import render

from .models import ShippingAddress
from cart.cart import Cart
from .models import Order, OrderItem

from django.http import JsonResponse
from django.core.mail import send_mail

from django.conf import settings

# Create your views here.

def checkout(request):

    # Users with accounts -- Pre-fill the form

    if request.user.is_authenticated:

        try:

            # Authenticated users WITH shipping information
            shipping_address = ShippingAddress.objects.get(user=request.user.id)

            context = {'shipping': shipping_address}

            return render(request, 'order/checkout.html', context)
        except:

            # Authenticated users with No shipping information
            return render(request, 'order/checkout.html')
    
    # Guest users
    return render(request, 'order/checkout.html')


def complete_order(request):

    if request.POST.get('action') == 'post':

        status = request.POST.get('status')
        payment_method = request.POST.get('payment_method')
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # All-in-one shipping address
        shipping_address = (address1 + '\n' + address2 + '\n' + 
                            city + '\n' + state + '\n' + zipcode
                            )

        cart = Cart(request)

        # Get the total price of items
        total_cost = cart.get_total()

        '''
        
            Order variations
            1. Create order -> Account users WITH + WITHOUT shipping information
            2. Create order -> Guest users without an account

        '''

        # # 1. Create order -> Account users WITH + WITHOUT shipping information
        # if request.user.is_authenticated:
            
        #     order = Order.objects.create(
        #         full_name = name,
        #         email = email,
        #         shipping_address = shipping_address,
        #         amount_paid = total_cost,
        #         user = request.user,
        #     )
        #     order_id = order.pk

        #     for item in cart:
        #         OrderItem.objects.create(
        #             order_id = order_id,
        #             product = item['product'],
        #             quantity = item['qty'],
        #             price = item['price'],
        #             user = request.user
        #         )
        # # 2. Create order -> Guest users without an account
        # else:

        #     order = Order.objects.create(
        #         full_name = name,
        #         email = email,
        #         shipping_address = shipping_address,
        #         amount_paid = total_cost,
        #     )
        #     order_id = order.pk

        #     for item in cart:
        #         OrderItem.objects.create(
        #             order_id = order_id,
        #             product = item['product'],
        #             quantity = item['qty'],
        #             price = item['price'],
        #         )

        # Create order data
        order_data = {
            "full_name": name,
            "email": email,
            "shipping_address": shipping_address,
            "amount_paid": total_cost,
            "status": status,
            "payment_method": payment_method,
        }

        # Add user for authenticated users
        if request.user.is_authenticated:
            order_data["user"] = request.user

        # Create the order
        order = Order.objects.create(**order_data)
        order_id = order.pk

        # Create OrderItems in bulk
       
        order_items = [
            OrderItem(
                order_id=order_id,
                product=item["product"],
                quantity=item["qty"],
                price=item["price"],
                user=request.user if request.user.is_authenticated else None
            )
            for item in cart
        ]
        
        OrderItem.objects.bulk_create(order_items)

        product_list = []
        for item in cart:

            product_list.append(item['product'])

        all_products = product_list
        # Email order
        send_mail('Order receied', 'Hi!' + '\n\n' + 'Thanh you for placing your order' + '\n\n' +
                    'Please see your order below:' + '\n\n' + str(all_products) + '\n\n' + 'Total price: $' +
                    str(cart.get_total()), settings.EMAIL_HOST_USER, [email], fail_silently=False)

        order_success = True
        response = JsonResponse({'success': order_success})

        return response


def order_success(request):

    for key in list(request.session.keys()):

        if key == 'session_key':
            del request.session[key]

    return render(request, 'order/success.html')


def order_failed(request):

    return render(request, 'order/failed.html')
