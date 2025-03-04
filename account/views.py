from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from order.forms import ShippingForm
from order.models import ShippingAddress, Order, OrderItem

from .token import user_tokenizer_generate
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Create your views here.
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            # Email verification setup (template)
            current_site = get_current_site(request)
            subject = 'Account verification email'
            message = render_to_string('account/registration/email_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user)
            })
            user.email_user(subject=subject, message=message)


            return redirect('account.email-verification-sent')
    
    context = {'form': form}

    return render(request, 'account/registration/register.html', context=context)


def email_verification(request, uidb64, token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    # Success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()

        return render(request, 'account/registration/email_verification_success.html')
    else:

        return render(request, 'account/registration/email_verification_failed.html')


def email_verification_sent(request):
    
    return render(request, 'account/registration/email_verification_sent.html')


def email_verification_success(request):
    
    return render(request, 'account/registration/email_verification_success.html')


def email_verification_failed(request):
    
    return render(request, 'account/registration/email_verification_failed.html')


def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('account.dashboard')
    
    context = {
        'form': form
    }

    return render(request, 'account/my_login.html', context)


def user_logout(request):
    # auth.logout(request)
    try :
        for key in list(request.session.keys()):
            if key == 'session_key':

                continue
            else:

                del request.session[key]
    except KeyError:

        pass

    messages.success(request, 'Logout success!')

    return redirect('store')


@login_required(login_url='account.my-login')
def dashboard(request):

    return render(request, 'account/dashboard.html')


@login_required(login_url='account.my-login')
def profile_management(request):
    user_form = UpdateUserForm(instance=request.user)


    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            messages.info(request, 'Account updated!')

            return redirect('account.dashboard')

    context = {'user_form': user_form}

    return render(request, 'account/profile_management.html', context)


@login_required(login_url='account.my-login')
def delete_account(request):

    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        user.delete()

        return redirect('store')

    return render(request, 'account/delete_account.html')


# Shipping view
@login_required(login_url='account.my-login')
def manage_shipping(request):
    
    try:

        # Account user with shipment information
        shipping = ShippingAddress.objects.get(user=request.user.id)

    except ShippingAddress.DoesNotExist:

         # Account user with no shipment information
        shipping = None

    form = ShippingForm(instance=shipping)

    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping)

        if form.is_valid():
            
            # Assign the user FK on the object
            shipping_user = form.save(commit=False)

            # Adding the FK itself
            shipping_user.user = request.user

            shipping_user.save()

            return redirect('account.dashboard')

    context = {'form': form}

    return render(request, 'account/manage_shipping.html', context)


@login_required(login_url='account.my-login')
def track_orders(request):

    try:
        orders = OrderItem.objects.filter(user=request.user)
        context = {'orders': orders}

        return render(request, 'account/track_orders.html', context)
    except:

        return render(request, 'account/track_orders.html')

    